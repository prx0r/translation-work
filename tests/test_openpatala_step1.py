#!/usr/bin/env python3
"""Step-1 acceptance: uniform records, mapping, bridge, emit source_ref, proposal."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))


class Step1Tests(unittest.TestCase):
    def test_records_cover_mapped_works(self):
        mp = json.loads((ROOT / 'source-maps' / 'openpatala.json').read_text(encoding='utf-8'))
        self.assertEqual(mp['format'], 'svatantrya-openpatala-map/1')
        rec = json.loads((ROOT / 'paramarthasara' / 'source' / 'record.json').read_text(encoding='utf-8'))
        self.assertEqual(rec['format'], 'svatantrya-source-record/1')
        self.assertEqual(rec['status'], 'RECORDED')
        self.assertEqual(rec['openpatala']['mapping_status'], 'CANDIDATE')
        self.assertEqual(rec['witness'], {'id': None, 'status': 'UNKNOWN'})
        self.assertIn('NC', rec['rights']['status'])

    def test_emit_carries_source_ref(self):
        import emit_scholar as e
        doc = e.build('paramarthasara')
        self.assertIn('source_ref', doc)
        self.assertEqual(doc['source_ref']['mapping_status'], 'CANDIDATE')
        self.assertTrue(doc['source_ref']['record_sha256'])

    def test_registration_proposal_is_shaped(self):
        doc = json.loads((ROOT / 'openpatala-registration.json').read_text(encoding='utf-8'))
        self.assertEqual(doc['format'], 'svatantrya-openpatala-registration-proposal/1')
        self.assertGreaterEqual(len(doc['works']), 100)
        by_key = {w['key']: w for w in doc['works']}
        self.assertEqual(by_key['ipvv']['mapping_status'], 'UNMAPPED')
        self.assertEqual(by_key['ipvv']['proposed_translation']['tier'], 'C')
        self.assertFalse(by_key['ipvv']['proposed_translation']['complete'])
        p = by_key['paramarthasara']
        self.assertEqual(p['proposed_translation']['tier'], 'A')
        self.assertTrue(p['proposed_translation']['complete'])


if __name__ == '__main__':
    unittest.main()
