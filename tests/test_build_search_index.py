"""Unit tests for tools/build_search_index.py (mocked embeddings)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_search_index as bsi  # noqa: E402


def write(p: Path, s: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    return p


class IndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for mod, val in (("TW", self.tmp / "tw"), ("SVREAD", self.tmp / "sv"),
                         ("IPVV", self.tmp / "ipvv"), ("NIB", self.tmp / "nib")):
            setattr(bsi, mod, val)
        write(self.tmp / "tw" / "w1" / "GATE.json", json.dumps({
            "s1": {"deterministic_gate": "PASS", "blocking": []},
            "s2": {"deterministic_gate": "BLOCKED", "blocking": ["X"]}}))
        write(self.tmp / "tw" / "w1" / "passages.jsonl", "")
        write(self.tmp / "sv" / "data" / "scholar" / "w1.json", json.dumps({
            "work": "w1", "projection_sha256": "x",
            "source_verses": {"s1-v01": "src one", "s2-v01": "src two"},
            "originals": {"t1": {"s1-v01": "gloss one",
                                 "s2-v01": "gloss two"},
                          "l2": {"s1-v01": "plain ENGLISH one",
                                 "s2-v01": "plain ENGLISH two"}},
            "original_hashes": {}, "essays": []}))
        write(self.tmp / "sv" / "data" / "pushing-catalog.json", json.dumps(
            {"format": "f", "revision": "r", "records": [
                {"file": "w1/LOGICVID-q.md", "git_blob": "b",
                 "question": "why?", "title": "T", "work": "w1"}]}))
        write(self.tmp / "ipvv" / "site" / "data" / "themes" / "adjudication-cl3.json",
              json.dumps({"theme_id": "CL-3",
                          "proposed_theme": {"label": "L", "core_claim": "C"}}))
        self.fake_vecs = [[float(i)] * 4 for i in range(60)]

    def fake_embed(self, texts, token, account):
        return [[float(len(t))] * 4 for t in texts]

    def test_records_gate_and_resume(self):
        with mock.patch.object(bsi, "embed_batch", side_effect=self.fake_embed):
            self.assertEqual(bsi.main(["--out", str(self.tmp / "idx")]), 0)
        recs = [json.loads(l) for l in
                (self.tmp / "idx" / "records.jsonl").read_text().splitlines()]
        by_id = {r["id"]: r for r in recs}
        p1 = by_id["chunk:w1:s1-v01"]
        self.assertEqual(p1["gate"], "PASS")
        self.assertIn("ENGLISH", p1["text"])
        p2 = by_id["chunk:w1:s2-v01"]
        self.assertEqual(p2["gate"], "BLOCKED")
        self.assertNotIn("ENGLISH", p2["text"])
        self.assertIn("withheld", p2["text"])
        self.assertIn("crux:w1:LOGICVID-q", by_id)
        self.assertIn("theme:adjudication-cl3.json:0", by_id)
        # resume: second run reuses cached vectors, no embed calls needed
        with mock.patch.object(bsi, "embed_batch",
                               side_effect=AssertionError("should not embed")) as m:
            self.assertEqual(bsi.main(["--out", str(self.tmp / "idx")]), 0)
        self.assertEqual(m.call_count, 0)
        meta = json.loads((self.tmp / "idx" / "meta.json").read_text())
        self.assertEqual(meta["count"], len(recs))


if __name__ == "__main__":
    unittest.main()
