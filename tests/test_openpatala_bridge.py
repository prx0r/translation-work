#!/usr/bin/env python3
"""Bridge tests: no network, live local checkouts only."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import openpatala_bridge as bridge


class BridgeTests(unittest.TestCase):
    def test_resolve_known_candidate(self):
        r = bridge.resolve('paramarthasara')
        self.assertEqual(r['mapping']['mapping_status'], 'CANDIDATE')
        self.assertEqual(r['mapping']['openpatala_work_id'],
                         'PTCND_sa_abhinavagupta-paramArthasAra')
        self.assertEqual(r['mapping']['witness'], 'UNKNOWN')
        self.assertEqual(r['record_status'], 'RECORDED')

    def test_resolve_unmapped_and_sourceless(self):
        r = bridge.resolve('tantraloka-a01')
        self.assertEqual(r['mapping']['mapping_status'], 'UNMAPPED')
        self.assertIsNone(r['mapping']['openpatala_work_id'])
        self.assertEqual(r['record_status'], 'NO-SOURCE-RECORD')

    def test_unknown_work_is_an_error_not_a_guess(self):
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve('no-such-work-xyz')

    def test_verify_candidate_is_consistent(self):
        v = bridge.verify('paramarthasara')
        self.assertEqual(v['status'], 'CONSISTENT', v['blocking'])
        self.assertEqual(v['witness'], 'UNKNOWN')

    def test_verify_part_scope_reports_part(self):
        v = bridge.verify('tantrasara-a22')
        r = bridge.resolve('tantrasara-a22')
        self.assertEqual(r['mapping']['scope'], 'part')
        self.assertIn(v['status'], ('CONSISTENT', 'INCONSISTENT'))

    def test_ipvv_maps_to_volumes_without_dossier(self):
        r = bridge.resolve('ipvv')
        self.assertEqual(r['mapping']['mapping_status'], 'UNMAPPED')
        self.assertEqual(r['record_status'], 'RECORDED')
        self.assertEqual(len(r['record']['volumes']), 3)


if __name__ == '__main__':
    unittest.main()
