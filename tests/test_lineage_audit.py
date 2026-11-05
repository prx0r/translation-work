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

BENCH = ROOT.parent / 'sanskritbench-audit'
OPENPATALA = ROOT.parent / 'openpatala-audit'
ESSAY = ROOT / 'paramarthasara/scholar/essays/62e62283ac8d5aa4a927ecbdcc064eeac4a38d8291a5dcd39db976f1b794e51b.json'


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
            value['claims']['human_review'] = 'PASS'
            receipt.write_text(json.dumps(value))
            verify = call(['verify', str(receipt), *common])
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn('digest', verify.stderr)


if __name__ == '__main__':
    unittest.main()
