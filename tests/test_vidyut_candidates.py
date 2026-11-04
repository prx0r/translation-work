import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import vidyut_candidates as candidate


class VidyutCandidateTests(unittest.TestCase):
    def test_known_incomplete_source_is_withheld_without_importing_optional_library(self):
        with self.assertRaisesRegex(ValueError, 'withheld'):
            candidate.analyze('ghatakarpara', 'ghat-p01-v01', 'iast')

    @unittest.skipUnless(importlib.util.find_spec('vidyut'), 'optional Vidyut is not installed')
    def test_real_passage_is_read_only_and_records_source(self):
        result = candidate.analyze('paramarthasara', 'param-p01-v01', 'iast')
        self.assertEqual(result['status'], 'machine-generated-unreviewed')
        self.assertIn('paraṃ', result['source_excerpt'])
        self.assertIn('paraM', result['slp1_candidate'])
        self.assertEqual(len(result['source_sha256']), 64)
        self.assertNotIn('meter_candidate', result)

    @unittest.skipUnless(importlib.util.find_spec('vidyut'), 'optional Vidyut is not installed')
    def test_meter_file_is_pinned_and_output_is_only_a_candidate(self):
        source = {'source_excerpt': 'mātaḥ samastajagatāṃ madhukaiṭabhāreḥ',
                  'source_sha256': 'a' * 64, 'source_lines': [1, 1]}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'meters.tsv'
            path.write_text('vasantatilakA\tvrtta\tGGLGLLLGLLGLGG\n', encoding='utf-8')
            with mock.patch.object(candidate.style_profile, 'source_context', return_value=source):
                result = candidate.analyze('testwork', 'test-p01-v01', 'iast', str(path))
            meter = result['meter_candidate']
            self.assertEqual(meter['name_slp1'], 'vasantatilakA')
            self.assertEqual(meter['meter_data_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertIn('not a verified', meter['warning'])

if __name__ == '__main__':
    unittest.main()
