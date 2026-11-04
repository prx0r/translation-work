"""Exercise exact author approval and HMAC publication bridge with real Git."""
import hashlib
import hmac
import http.client
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import scholar  # noqa: E402
import scholar_service  # noqa: E402


class AccountSubmissionTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.repo=self.root/'translation-work';self.repo.mkdir()
        for folder in ('tools','schemas','paramarthasara'):
            shutil.copytree(ROOT/folder,self.repo/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        os.symlink(ROOT.parent/'ipvv',self.root/'ipvv')
        self.git('init','-b','main');self.git('config','user.name','Test');self.git('config','user.email','test@example.invalid')
        self.git('add','.');self.git('commit','-m','Canonical source');self.head=self.git('rev-parse','HEAD')
    def tearDown(self):self.temp.cleanup()
    def git(self,*args):return subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True,text=True).stdout.strip()
    def payload(self,kind='translation'):
        original=json.loads((self.repo/'paramarthasara/data/param-p01.l3.json').read_text())[0]
        content={'text':'A distinct human rendering of this passage.','base_sha256':scholar.sha(original),
                 'parent':None,'assisted':True,'model':'qwen-test'}
        snap={'kind':kind,'work':'paramarthasara','target':'param-p01-v01','layer':'l3',
              'title':'A scholarly essay' if kind=='essay' else '', 'content':content}
        return {'format':'scholar-account-submission/1','account_id':'account-1','author':'A Scholar',
                'document_id':'draft-1','revision':1,'snapshot':snap,
                'signoff':{'id':'signoff:example','snapshot_sha256':scholar.sha(snap),
                           'rights':'all-rights-reserved','created_at':'2026-11-03T00:00:00Z'}}

    def test_translation_is_validated_and_author_approval_targets_exact_git_version(self):
        payload=self.payload();first=scholar_service.submit_account(self.repo,payload);again=scholar_service.submit_account(self.repo,payload)
        self.assertEqual(first['commit'],again['commit']);self.assertFalse(first['remote_pushed']);self.assertEqual(self.git('rev-parse','HEAD'),self.head)
        versions=[json.loads(x) for x in self.git('show',first['branch']+':paramarthasara/scholar/versions.jsonl').splitlines()]
        version=versions[-1];self.assertEqual(version['author_kind'],'human');self.assertIn('AI-assisted (qwen-test)',version['note'])
        reviews=[json.loads(x) for x in self.git('show',first['branch']+':paramarthasara/scholar/reviews.jsonl').splitlines()]
        review=reviews[-1];self.assertTrue(scholar.ReviewEvent.verify(review))
        self.assertEqual(review['review_target']['object_ref'],version['version_id'])
        self.assertEqual(review['review_target']['hash'],version['content_sha256'])
        self.assertEqual(review['reviewer']['identity_state'],'SELF_ATTESTED');self.assertEqual(review['conflict_of_interest'],'AUTHOR')
        payload['snapshot']['content']['text']='Changed after sign-off.'
        with self.assertRaises(ValueError):scholar_service.submit_account(self.repo,payload)

    def test_new_signoff_of_same_snapshot_does_not_collide_after_merge(self):
        payload=self.payload();first=scholar_service.submit_account(self.repo,payload)
        self.git('merge','--no-ff','--no-edit',first['branch'])
        payload['signoff']['id']='signoff:another'
        second=scholar_service.submit_account(self.repo,payload)
        self.assertNotEqual(first['branch'],second['branch'])
        rows=[json.loads(x) for x in self.git('show',second['branch']+':paramarthasara/scholar/versions.jsonl').splitlines()]
        self.assertEqual(rows[-1]['author'],'A Scholar')

    def test_essay_citations_are_signed_and_checked_against_a_pinned_git_commit(self):
        payload=self.payload('essay')
        t1=json.loads((self.repo/'paramarthasara/data/param-p01.t1.json').read_text())[0]
        citation={'work':'paramarthasara','target':t1['verse_id'],'t1_sha256':scholar.sha(t1),'projection_sha256':'a'*64}
        payload['snapshot']['content']['citations']=[citation]
        payload['signoff']['snapshot_sha256']=scholar.sha(payload['snapshot'])
        result=scholar_service.submit_account(self.repo,payload);digest=result['essay_id'].split(':',1)[1]
        essay=json.loads(self.git('show',result['branch']+f':paramarthasara/scholar/essays/{digest}.json'))
        self.assertEqual(essay['source_git_commit'],self.head)
        self.assertEqual(essay['snapshot']['content']['citations'],[citation])
        self.assertEqual(scholar.essay_errors(essay,'paramarthasara',digest+'.json'),[])
        self.assertIn('client-reported',essay['citation_note'])
        for invalid in [{**citation,'t1_sha256':'0'*64},{**citation,'target':'missing-v01'},
                        {**citation,'work':'ghatakarpara'},{**citation,'work':'../outside'}]:
            with self.subTest(invalid=invalid):
                payload['snapshot']['content']['citations']=[invalid]
                payload['signoff']['snapshot_sha256']=scholar.sha(payload['snapshot'])
                with self.assertRaises(ValueError):scholar_service.submit_account(self.repo,payload)
        payload['snapshot']['content']['citations']=[citation,citation]
        payload['signoff']['snapshot_sha256']=scholar.sha(payload['snapshot'])
        with self.assertRaisesRegex(ValueError,'duplicate'):scholar_service.submit_account(self.repo,payload)

    def test_essay_and_hmac_bridge(self):
        payload=self.payload('essay');secret=b'x'*40
        server=scholar_service.ThreadingHTTPServer(('127.0.0.1',0),
            scholar_service.handler_for(self.repo,[],'https://svread.pages.dev',None,secret))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            body=json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode();stamp=str(int(time.time()))
            message=f'scholar-bridge/v1\n{stamp}\n{hashlib.sha256(body).hexdigest()}'.encode()
            signature=hmac.new(secret,message,hashlib.sha256).hexdigest()
            def send(sig):
                connection=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=15)
                connection.request('POST','/v1/scholar/account-submissions',body,
                    {'X-Scholar-Time':stamp,'X-Scholar-Signature':sig,'Content-Type':'application/json'})
                response=connection.getresponse();result=(response.status,json.loads(response.read()));connection.close();return result
            self.assertEqual(send('bad')[0],401);status,result=send(signature);self.assertEqual(status,200)
            digest=result['essay_id'].split(':',1)[1]
            essay=json.loads(self.git('show',result['branch']+f':paramarthasara/scholar/essays/{digest}.json'))
            self.assertEqual(scholar.essay_errors(essay,'paramarthasara',digest+'.json'),[])
            essay['text']='Tampered';self.assertTrue(scholar.essay_errors(essay,'paramarthasara',digest+'.json'))
            self.assertEqual(self.git('rev-parse','HEAD'),self.head)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
