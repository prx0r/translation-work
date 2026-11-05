"""Regression tests for the read-only lineage and heuristic benchmark adapter."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import lineage_audit as audit
import passage_adapter as adapter

BENCH = ROOT.parent / 'sanskritbench-audit'
OPENPATALA = ROOT.parent / 'openpatala-audit'
ESSAY = ROOT / 'paramarthasara/scholar/essays/62e62283ac8d5aa4a927ecbdcc064eeac4a38d8291a5dcd39db976f1b794e51b.json'
IPVV_VOL1 = ROOT.parent / 'ipvv/site/data/sanskrit/ipvv-vol1.txt'

NEEDS_IPVV_VOL = unittest.skipUnless(
    IPVV_VOL1.is_file(), 'requires the ipvv volume sibling')


class PassageAdapterTests(unittest.TestCase):
    def test_unknown_prose_chunk_is_rejected(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.resolve('ipvv', 'no-such-chunk')

    def test_verse_id_is_never_a_prose_chunk(self):
        # A verse proof must never resolve as a commentary chunk.
        with self.assertRaises(adapter.AdapterError):
            adapter.resolve('ipvv', 'param-p01-v01')

    @NEEDS_IPVV_VOL
    def test_prose_chunkA_resolves_pinned_bytes(self):
        for pid in ('chunkA-svatyandya', 'chunkA-svatyandya.md'):
            r = adapter.resolve('ipvv', pid)
            self.assertEqual(r['kind'], 'prose')
            self.assertEqual(r['source_evidence_state'], 'CANDIDATE_LINE_MATCH')
            self.assertEqual((r['spans'][0]['start'], r['spans'][0]['end']),
                             (10902, 38625))

    @NEEDS_IPVV_VOL
    def test_prose_dotted_ids_resolve(self):
        # On-disk files replace dots with dashes; both forms must resolve.
        r = adapter.resolve('ipvv', 'chunkG-k1.2.7-1.8-citsvarupam')
        self.assertEqual(r['kind'], 'prose')
        self.assertEqual(r['source_evidence_state'], 'CANDIDATE_LINE_MATCH')

    @NEEDS_IPVV_VOL
    def test_prose_audit_is_incomplete_never_pass(self):
        r = audit.audit('ipvv', 'chunkA-svatyandya', BENCH, OPENPATALA)
        self.assertEqual(r['format'], audit.PROSE_FORMAT)
        self.assertEqual(r['scope'].get('passage_kind'), 'prose')
        self.assertEqual(r['overall'], 'INCOMPLETE')
        self.assertEqual(r['translation']['historical_record']['status'],
                         'PROSE_NO_VERSE_PROOF')
        self.assertFalse(r['claims']['publication_authorized'])


class LineageUnitTests(unittest.TestCase):
    def test_kernel_must_match_pin_before_execution(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            root = Path(d)
            (root / 'pipeline').mkdir()
            (root / 'pipeline/translation_proof.py').write_text('raise RuntimeError("must not execute")')
            with self.assertRaisesRegex(audit.AuditError, 'pinned SHA-256'):
                audit.load_benchmark(root)

    def test_missing_layers_and_changed_record_are_not_current(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            root = Path(d)
            (root / 'w/data').mkdir(parents=True)
            (root / 'w/proof').mkdir()
            (root / 'w/data/s.t1.json').write_text('[{"a":1}]')
            (root / 'w/proof/proof-s.json').write_text(json.dumps({
                'source_sha': audit.digest(b'word')[:16],
                'layer_sha256': {'t1': 'not-the-current-hash'}, 'deterministic_gate': 'PASS'}))
            with patch.object(audit, 'ROOT', root):
                _, result = audit.layer_snapshot('w', 's', {1: ['word']}, [1])
            self.assertEqual(result['status'], 'STALE_OR_INCOMPLETE')
            self.assertEqual(result['changed_layers'], ['t1'])
            self.assertIn('l2', result['missing_required_layers'])

    def test_bad_work_or_target_is_rejected(self):
        for work, target in [('../ipvv', 'param-p01-v01'), ('paramarthasara', '../bad')]:
            with self.assertRaises(audit.AuditError):
                audit.audit(work, target, BENCH, OPENPATALA)

    def test_json_hash_is_order_independent_and_uses_all_content(self):
        self.assertEqual(audit.object_sha({'a': 1, 'b': 2}), audit.object_sha({'b': 2, 'a': 1}))
        self.assertNotEqual(audit.object_sha({'text': 'a' * 40 + 'x'}),
                            audit.object_sha({'text': 'a' * 40 + 'y'}))

    def test_essay_citation_resolves_its_historical_git_tree(self):
        # A synthetic public essay and source live only in this temporary Git repo.
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            root = Path(d)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'w/data').mkdir(parents=True)
            (root / 'w/proof').mkdir()
            (root / 'w/scholar/essays').mkdir(parents=True)
            target, song = 's-v01', 's'
            row = {'verse_id': target, 'text': 'fixture'}
            values = {'t1': [row], 'l0': [], 'argmap': [], 'l2': [], 'c1': {}}
            for name, val in values.items():
                (root / f'w/data/{song}.{name}.json').write_text(json.dumps(val))
            proof = {'work': 'w', 'song': song, 'deterministic_gate': 'PASS',
                     'layer_sha256': {name: audit.object_sha(val) for name, val in values.items()}}
            (root / 'w/proof/proof-s.json').write_text(json.dumps(proof))
            subprocess.run(['git', '-C', str(root), 'add', 'w/data', 'w/proof'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                            'commit', '-q', '-m', 'source'], check=True)
            commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            citation = {'work': 'w', 'target': target, 't1_sha256': audit.object_sha(row),
                        'projection_sha256': 'a' * 64}
            snapshot = {'kind': 'essay', 'work': 'w', 'target': target, 'title': 'Fixture',
                        'content': {'text': 'Example text.', 'citations': [citation]}}
            essay = {'format': 'scholar-essay/1', 'work': 'w', 'target': target, 'title': 'Fixture',
                     'text': 'Example text.', 'author': 'Test', 'author_id': 'test',
                     'identity_state': 'SELF_ATTESTED', 'rights': 'cc-by-4.0',
                     'signoff': {'id': 'signoff:test', 'rights': 'cc-by-4.0',
                                 'snapshot_sha256': audit.object_sha(snapshot)},
                     'snapshot': snapshot, 'assisted': False, 'model': '', 'source_git_commit': commit}
            def write_essay(value):
                value = dict(value)
                sha = audit.object_sha(value)
                value['essay_id'] = 'essay:' + sha
                path = root / 'w/scholar/essays' / (sha + '.json')
                path.write_text(json.dumps(value))
                return path
            projection = {'status': 'MATCH', 'projection_sha256': 'a' * 64}
            with patch.object(audit, 'ROOT', root):
                path = write_essay(essay)
                result = audit.essay_link(path, 'w', song, target, audit.object_sha(row), projection)
                self.assertEqual(result['status'], 'LINKED_COMMITTED_T1_AND_PROJECTION')
                self.assertEqual(result['historical_citation']['proof_layer_hashes'], 'MATCH')
                partial = audit.essay_link(path, 'w', song, target, audit.object_sha(row),
                                           {'status': 'NOT_REQUESTED'})
                self.assertEqual(partial['status'], 'PARTIAL_COMMITTED_T1')
                missing = write_essay({**essay, 'source_git_commit': 'f' * 40})
                self.assertEqual(audit.essay_link(missing, 'w', song, target, audit.object_sha(row), projection)['status'],
                                 'HISTORICAL_T1_UNAVAILABLE')
                (root / 'w/data/s.l2.json').write_text('[{"changed":true}]')
                subprocess.run(['git', '-C', str(root), 'add', 'w/data/s.l2.json'], check=True)
                subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                                'commit', '-q', '-m', 'stale proof'], check=True)
                stale_commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD',
                                                         ], text=True).strip()
                stale = write_essay({**essay, 'source_git_commit': stale_commit})
                self.assertEqual(audit.essay_link(stale, 'w', song, target, audit.object_sha(row), projection)['status'],
                                 'HISTORICAL_PROOF_NOT_CURRENT')


@unittest.skipUnless((BENCH / 'pipeline/translation_proof.py').is_file()
                     and (OPENPATALA / 'data/gold/PTCND_sa_abhinavagupta-pa.json').is_file()
                     and (ROOT.parent / 'ipvv/site/data/sanskrit/paramarthasara.txt').is_file(),
                     'requires the pinned companion checkouts')
class LineageIntegrationTests(unittest.TestCase):
    def test_benchmark_pass_is_not_semantic_proof(self):
        verify, _ = audit.load_benchmark(BENCH)
        raw = verify('rāmaḥ vanam gacchati', 'He does not go into the woods')
        self.assertEqual(raw['deterministic_gate'], 'PASS')

    def test_real_chain_and_unlinked_editorial_essay(self):
        result = audit.audit('paramarthasara', 'param-p01-v01', BENCH, OPENPATALA, ESSAY)
        self.assertEqual(result['source']['openpatala']['status'], 'CANDIDATE')
        self.assertTrue(result['source']['openpatala']['language_conflict'])
        self.assertEqual(result['source']['openpatala']['witness'], 'UNKNOWN')
        self.assertEqual(result['translation']['structural_validation']['status'], 'PASS')
        self.assertEqual(result['translation']['historical_record']['status'],
                         'RECORDED_LAYER_AND_SOURCE_HASHES_MATCH')
        self.assertEqual(result['benchmark']['usage'], 'ADVISORY_HEURISTICS_ONLY')
        self.assertEqual(result['claims']['semantic_fidelity'], 'UNKNOWN')
        self.assertFalse(result['claims']['publication_authorized'])
        self.assertEqual(result['essay']['status'], 'UNLINKED')
        self.assertEqual(result['overall'], 'INCOMPLETE')

    @unittest.skipUnless((ROOT.parent / 'svread-audit/data/scholar/paramarthasara.json').exists(),
                         'requires the svread reader checkout')
    def test_reader_projection_matches_real_layers(self):
        result = audit.audit('paramarthasara', 'param-p01-v01', BENCH, OPENPATALA, ESSAY,
                             ROOT.parent / 'svread-audit/data/scholar/paramarthasara.json')
        projection = result['reader_projection']
        self.assertEqual(projection['status'], 'MATCH')
        self.assertTrue(all(v == 'MATCH' for v in projection['layers'].values()))
        self.assertTrue(projection['source_matches_parser_ignoring_whitespace_and_pada_bars'])

    def test_cli_replay_and_tampering(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            receipt = Path(d) / 'receipt.json'
            common = ['--bench-root', str(BENCH), '--openpatala-root', str(OPENPATALA)]
            cli = [sys.executable, str(ROOT / 'tools/lineage_audit.py')]
            def call(args):
                return subprocess.run(cli + args, capture_output=True, text=True)
            run = call(['run', '--work', 'paramarthasara', '--target', 'param-p01-v01',
                        '--output', str(receipt), *common])
            self.assertEqual(run.returncode, 0, run.stderr)
            verify = call(['verify', str(receipt), *common])
            self.assertEqual(verify.returncode, 0, verify.stderr)
            again = call(['run', '--work', 'paramarthasara', '--target', 'param-p01-v01',
                          '--output', str(receipt), *common])
            self.assertNotEqual(again.returncode, 0, 'must never overwrite a receipt')
            value = json.loads(receipt.read_text())
            original = dict(value)
            value['overall'] = 'PASS'
            receipt.write_text(json.dumps(value))
            verify = call(['verify', str(receipt), *common])
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn('schema invalid', verify.stderr)
            original['source']['openpatala']['language_conflict'] = False
            receipt.write_text(json.dumps(original))
            verify = call(['verify', str(receipt), *common])
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn('digest', verify.stderr)


if __name__ == '__main__':
    unittest.main()
