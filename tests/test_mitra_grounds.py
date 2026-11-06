#!/usr/bin/env python3
"""Tests for tools/mitra_grounds.py. Reads the shipped subset (committed
data, deterministic) — no network, no fixtures needed."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import mitra_grounds as mg  # noqa: E402


class MitraGroundsTest(unittest.TestCase):
    def test_known_headwords_ranked(self):
        g = mg.grounds("tattva")
        self.assertTrue(g)
        self.assertEqual(g[0]["en"], "truth")
        self.assertGreater(g[0]["count"], 0)
        self.assertTrue(g[0]["attestations"])
        m = mg.grounds("mala")
        self.assertIn("impurity", [s["en"] for s in m])

    def test_unknown_headword_never_invented(self):
        self.assertEqual(mg.grounds("zzqx_notaword"), [])
        self.assertEqual(mg.grounds(""), [])
        self.assertEqual(mg.grounds(None), [])

    def test_provenance_and_license(self):
        prov = json.loads((ROOT / "lore" / "mitra-trika-subset.PROVENANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(prov["license"], "CC BY-SA 4.0")
        self.assertGreaterEqual(prov["trika_hits"], 200)
        n = sum(1 for _ in (ROOT / "lore" / "mitra-trika-subset.jsonl").open(encoding="utf-8"))
        self.assertEqual(n, prov["trika_hits"])


if __name__ == "__main__":
    unittest.main()
