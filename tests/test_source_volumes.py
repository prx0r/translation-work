#!/usr/bin/env python3
"""Unit tests for the versioned add-source path (no fixtures, no network)."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import source_volumes as sv


class VolumeTests(unittest.TestCase):
    def test_round_trip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            with patch.object(sv, 'ROOT', Path(d)):
                raw = 'alpha\nbeta\ngamma\n'.encode()
                p = sv.record_volume('w', 'V1', raw,
                                     [{'passage_id': 'cA', 'start': 0, 'end': 6,
                                       'text': 'alpha\n'},
                                      {'passage_id': 'cB', 'start': 6, 'end': 11,
                                       'text': 'beta\n'}],
                                     edition='ed', source_license='lic')
                self.assertTrue(p.is_file())
                with self.assertRaises(sv.VolumeError):
                    sv.record_volume('w', 'V1', raw,
                                     [{'passage_id': 'cA', 'start': 0, 'end': 6,
                                       'text': 'alpha\n'}],
                                     edition='ed', source_license='lic')

    def test_byte_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            with patch.object(sv, 'ROOT', Path(d)):
                with self.assertRaises(sv.VolumeError):
                    sv.record_volume('w', 'V1', b'alpha\n',
                                     [{'passage_id': 'cA', 'start': 0, 'end': 5,
                                       'text': 'ALPHA'}],
                                     edition='ed', source_license='lic')

    def test_shared_boundary_overlap_is_recorded_not_refused(self):
        # Commentary chunks may share a boundary line: record the overlap.
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            with patch.object(sv, 'ROOT', Path(d)):
                p = sv.record_volume('w', 'V1', b'0123456789',
                                     [{'passage_id': 'a', 'start': 0, 'end': 5,
                                       'text': '01234'},
                                      {'passage_id': 'b', 'start': 4, 'end': 9,
                                       'text': '45678'}],
                                     edition='ed', source_license='lic')
                import json
                m = json.loads(p.read_text())
                self.assertEqual(len(m['overlaps']), 1)
                self.assertEqual((m['overlaps'][0]['start'],
                                  m['overlaps'][0]['end']), (4, 5))


if __name__ == '__main__':
    unittest.main()
