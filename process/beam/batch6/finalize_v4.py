#!/usr/bin/env python3
"""Validation and artifact builder for cumulative Muktabodha bibliography, v1+v2+v3+v4.
Do not modify previous editions, do not mutate GitHub, never infer a negative translation claim.
"""
import csv,json,pathlib,zipfile,hashlib,collections,re
P=pathlib.Path(__file__).resolve().parent; ZIP=P.parent/(P.name+'.zip')
cols='catalog,title,author,verses,tier,tw_status,known_T,T_why,has_translation,translator,year,scope_full_partial_chapters,access_tier,download_url,publisher,info_url,evidence_notes,researcher,verified_at'.split(',')
def loadcsv(f):
 with f.open(encoding='utf-8-sig',newline='') as stream:
  d=csv.DictReader(stream);return list(d.fieldnames),list(d)
def jsonlines(f):return [json.loads(s) for s in f.read_text(encoding='utf8').splitlines() if s.strip()]
h,rows=loadcsv(P/'burn_research.csv');h0,baseline=loadcsv(P/'burn_research.source-PR18.csv')
assert h==h0==cols,(h,h0)
assert len(rows)==len(baseline)==499
assert all([r[x] for x in cols[:8]]==[s[x] for x in cols[:8]] for r,s in zip(rows,baseline))
assert all(r['has_translation'] in ('','TRUE') for r in rows)
assert all(not r['download_url'] or r['access_tier']=='DIRECT' for r in rows)
assert all(not r['info_url'] or re.match('^https://[^ ]+$',r['info_url']) for r in rows)
assert all(not r['has_translation'] or all(r[x] for x in ('translator','scope_full_partial_chapters','info_url','researcher','verified_at')) for r in rows)
eds=jsonlines(P/'translation_editions.jsonl');leads=jsonlines(P/'manual_leads_and_exceptions.jsonl');watch=jsonlines(P/'forthcoming_watch.jsonl')
assert len(eds)==143,len(eds)
assert all(e['publication_status']=='published' for e in eds)
assert len({(e['catalog'],e['translator'],e['year'],e['scope'],e['info_url']) for e in eds})==len(eds)
allids={r['catalog'] for r in rows if r['catalog']};counts=collections.Counter(e['catalog'] for e in eds)
assert all(e['catalog'] in allids for e in eds)
assert all(e['info_url'].startswith('https://') and e['language'] for e in eds)
assert all((not e['download_url']) or e['access_tier']=='DIRECT' for e in eds)
assert all(r['has_translation']=='TRUE' for r in rows if counts[r['catalog']])
assert all(counts[r['catalog']]>=1 for r in rows if r['has_translation']=='TRUE')
positive={r['catalog'] for r in rows if r['has_translation']=='TRUE'}
assert len(positive)==113,len(positive)
# Earlier turn's pre-v4 ZIP provides a local immutable comparison for previous 83 positively classified work rows.
if ZIP.exists():
 with zipfile.ZipFile(ZIP) as z:
  oldcsv=z.read(P.name+'/burn_research.csv').decode('utf8').splitlines()
  oldrows={r['catalog']:r for r in csv.DictReader(oldcsv)}
  oldpos={cid for cid,r in oldrows.items() if r['has_translation']=='TRUE'}
  assert len(oldpos)==83,len(oldpos)
  current={r['catalog']:r for r in rows}
  assert all(current[cid]==oldrows[cid] for cid in oldpos),'Old positively classified work data overwritten'
first=42
v2='ChatGPT manual bibliography research, continuation v2'
v3='ChatGPT bibliography continuation v3 (verified published records)'
v4='ChatGPT manual bibliography research, continuation v4'
counts_round={v:sum(e['researcher']==v for e in eds) for v in (v2,v3,v4)}
assert first+sum(counts_round.values())==len(eds)
assert counts_round[v4]==32
leadids={e['catalog'] for e in leads}|{e['catalog'] for e in watch}
with (P/'catalog_research_status.csv').open('w',encoding='utf8',newline='') as f:
 fields=['catalog','title','audit_status','has_translation','known_T','documented_edition_count','action_needed'];w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader()
 for r in rows:
  cid=r['catalog'];has=r['has_translation']=='TRUE'
  if not cid: st='MISSING_MERGE_KEY';nxt='Resolve original Muktabodha catalog ID; cannot merge by title'
  elif has: st='VERIFIED_EXISTENCE';nxt='Import edition records; inspect translation scope and Sanskrit recension alignment'
  elif cid in leadids: st='RESEARCH_LEAD_REQUIRES_FOLLOWUP';nxt='Review specific lead, source and edition identity; no verified root translation established'
  else: st='NOT_INDIVIDUALLY_RESEARCHED';nxt='Per-work translation bibliography search pending; no claim of absence'
  w.writerow({'catalog':cid,'title':r['title'],'audit_status':st,'has_translation':r['has_translation'],'known_T':r['known_T'],'documented_edition_count':counts[cid],'action_needed':nxt})
with (P/'research_continuation_2026-11-11.jsonl').open('w',encoding='utf8') as f:
 for e in eds:
  if e['researcher'] in (v2,v3,v4):
   f.write(json.dumps({'catalog':e['catalog'],'title':e['title'],'translator':e['translator'],'year':e['year'],'language':e['language'],'scope':e['scope'],'info_url':e['info_url'],'corroboration_url':e['corroboration_url'],'confidence':e['confidence'],'researcher':e['researcher']},ensure_ascii=False,sort_keys=True)+'\n')
report={'source_repo':'https://github.com/prx0r/translation-work/pull/18','source_branch':'burn/muktabodha','source_head_commit':'5b102c18b785e689bdacc949db7cc299d7019e89','date':'2026-11-11','original_catalog_rows':499,'final_catalog_rows':499,'original_headers':cols,'final_headers':h,'all_baseline_columns_unchanged':True,'row_order_preserved':True,'previous_v3_work_count':83,'previous_v3_edition_count':111,'individual_works_with_verified_translation':113,'verified_published_edition_records':143,'new_works_in_v4':30,'new_editions_in_v4':32,'continuation_v2_new_published_edition_records':counts_round[v2],'continuation_v3_new_published_edition_records':counts_round[v3],'continuation_v4_new_published_edition_records':counts_round[v4],'languages_in_edition_records':dict(sorted(collections.Counter(e['language'] for e in eds).items())),'research_lead_or_exception_records':len(leads),'works_with_exception_or_forthcoming_leads':len(set(x for x in leadids if x in allids)),'unresolved_rows':386,'blank_catalog_ids':[r['title'] for r in rows if not r['catalog']],'false_translation_flags_created':0,'direct_download_links_count':sum(bool(r['download_url']) for r in rows),'evidence_model':'TRUE indicates presence of documented published translation of root or named commentary or part, not full Muktabodha-edition alignment','critical_blockers':['One blank catalog ID (saundaryalaharī), cannot merge by catalog','At least 386 rows unresolved; none labeled untranslated','Unit counts and source edition alignment have not been exhaustively collated','Mañjuśrīmūlakalpa three printed source volumes not independently chapter-aligned to 84000 translation','Some Āgama translation languages and multiple catalog IDs not edition-aligned','Some scholarly French articles may translate excerpts rather than every root verse; see medium confidence notes','Guhyasamājatantra Fremantle thesis covers 1–17, not chapter 18; no full coverage claim','No 499-work exhaustive bibliography completed']}
(P/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
readme=P/'README.md';s=readme.read_text(encoding='utf8')
s=s.replace('## Cumulative continuation summary (2026-11-11, v3)','## Cumulative continuation summary (2026-11-11, v4)')
s=s.replace('**83 of 499 catalog rows**','**113 of 499 catalog rows**').replace('**111 separate published-edition records**','**143 separate published-edition records**').replace('**416 rows remain unresolved**','**386 rows remain unresolved**')
s=s.replace('`continue_v2.py` and `continue_v3.py`','`continue_v2.py`, `continue_v3.py`, and `continue_v4.py`').replace('`finalize_cumulative.py` regenerates this package','`finalize_v4.py` regenerates this package')
s=s.replace('**111 independently represented published translation records for 83 works**','**143 independently represented published translation records for 113 works**')
s=s.replace('(83 verified works, 416 unresolved)','(113 documented works, 386 unresolved)')
s=s.replace('New high-value discoveries include a 20-Upaniṣad','Early high-value discoveries included a 20-Upaniṣad')
s=s.replace('## Deliverables','''### Continuation v4 discoveries

- **30 new catalog IDs** flagged with published translation evidence, **32 new edition entries**, including sources in English, Hindi, French, and Russian (plus three language-undetermined Agama editions).
- The 84000 Mañjuśrīmūlakalpa translation cites the very three-volume Sanskrit source from which the three Muktabodha IDs arise; those print-volume chapter boundaries still need crosswalks.
- Fremantle's Guhyasamājatantra doctoral thesis: **chapters I–XVII only**, not an automatic translation of Uttaratantra (XVIII), despite its own abstract using "entirety".
- Sources also document Kāmikāgama Pūrvapāda/Uttarapāda English parts, Sarvajñānottara, Gorakṣayogaśāstra Russian, Sanskrit/Sadyojyoti treatises in French, Kaula texts, and the Mātṛkābhedatantra.
- **Not proof of 113 fully translated works**: multiple rows are only excerpt/section translations, and some are duplicate IDs for one root text; `translation_editions.jsonl` carries exact evidence and notes.

## Deliverables''')
readme.write_text(s,encoding='utf8')
notes=P/'PROCESS_NOTES.md';s=notes.read_text(encoding='utf8')
s+='''\n## Cumulative continuation v4 (2026-11-11)\n\n**30 newly documented catalog rows and 32 new bibliographic edition records**, cumulative 113/499 work rows, 143 edition records, 386 unresolved. Clusters: Buddhist tantras (Mañjuśrīmūlakalpa three source volumes; Guhyasamājatantra 1–17); Hindi and English published Śaiva āgama portions; 1980s–1990s French translations of Sadyojyoti treatises; Karpūrādistotra 1922 and 2012 English; 2026 Vijñānabhairava with Ānandabhaṭṭa commentary; Yogacintāmaṇi āsanas only; Russian Gorakṣayogaśāstra; 2011 Mātṛkābhedatantra.\n\n**Counterexamples excluded:** Nareśvaraparīkṣāprakāśa excerpts are not proof that root Nareśvaraparīkṣā was directly translated; Sādhanamālā selected sādhana translation cannot be projected onto both printed volumes; Ratnatrayaparīkṣā commentary excerpt not proof of full root; no negative claims. Language 'und' for three Agama records pending source language verification; edition labels are deliberately conservative. The publisher-specific URL and bibliographic corroboration for each is preserved in JSONL, and all 83 pre-existing positive CSV rows match the previous package byte-for-byte after CSV parsing.\n\nNo GitHub write or background task. The same 499-row, 19-column PR #18 CSV is used.\n'''
notes.write_text(s,encoding='utf8')
files=sorted(x for x in P.iterdir() if x.is_file() and x.name!='FILES_MANIFEST.json')
manifest={'created':'2026-11-11','source_pr':18,'source_head':report['source_head_commit'],'cumulative_works_with_translation':113,'edition_records':143,'files':[{'name':x.name,'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in files]}
(P/'FILES_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for x in sorted(P.iterdir()):
  if x.is_file():z.write(x,arcname=P.name+'/'+x.name)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(list(P.iterdir()))
 assert z.read(P.name+'/burn_research.csv')==(P/'burn_research.csv').read_bytes()
 assert z.read(P.name+'/translation_editions.jsonl')==(P/'translation_editions.jsonl').read_bytes()
print(json.dumps({'zip':str(ZIP),'bytes':ZIP.stat().st_size,'works':113,'new_works':30,'edition_records':143,'new_editions':32,'unresolved':386,'leads':len(leads),'languages':report['languages_in_edition_records'],'zip_integrity':'PASSED','baseline_preserved':'PASSED'},ensure_ascii=False,indent=2))
