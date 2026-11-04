"""Unit tests for tools/essay_starters.py. Fixture trees; archives untouched."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import essay_starters  # noqa: E402


def write(p: Path, s: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    return p


ESSAY = """# Why Rebirth

Dyczkowski backbone, my stitches in brackets.

## The objection

> "must Kashmir Shaivism depend on rebirth?" [karma-01]

Caterpillar [karma-02, 00:19:02-->00:19:10]. The self (ātman) returns.

## Images
"""


class StartersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        r = self.tmp
        write(r / "te" / "essay_MEDIUM.md", ESSAY)
        write(r / "te" / "essay_COPY.md", ESSAY)
        write(r / "te" / "README.md", "# readme")
        write(r / "rl" / "note.md", "# Note\n\nPlain note, no refs.\n")
        pack = r / "xp" / "pack_01" / "pack_01"
        write(pack / "manifest.json", json.dumps({
            "title": "the body remembers", "key_concepts": ["body", "memory"]}))
        write(pack / "01_body.md", "# Body\n\nśarīra (the body) remembers.\n")
        write(pack / "SOURCES.md", "# Sources\n")
        write(r / "ws" / "w1.json", json.dumps({
            "id": "w1", "title": "W1", "author": "A", "concepts": ["X"],
            "body": [{"kind": "ai", "text": "hello world"},
                     {"kind": "source", "text": "old words"}]}))
        write(r / "bc" / "essay-objects" / "eo1" / "eo.json", json.dumps({
            "eo_id": "eo:test", "title": "EO", "status": "active",
            "question": {"tension_point": "the crux here"}}))
        write(r / "bc" / "contentions" / "c1.json", json.dumps({
            "question_id": "q1", "title": "C1", "tradition": "trika",
            "central_reading": "reading", "claims": [{}, {}]}))
        write(r / "bc" / "essay-seeds" / "s1.json", json.dumps({
            "seed_id": "seed:1", "title": "S1", "sharp_question": "sharp?"}))
        write(r / "tw" / "w1" / "passages.jsonl",
              '{"locator": "s1", "verses": "1.1"}\n')
        write(r / "tw" / "w1" / "T1-s1.md", "light of ātman shines")
        write(r / "tw" / "w1" / "T1-s2.md", "freedom elsewhere")
        self.env = {"TANTRAESSAYS_ROOT": str(r / "te"),
                    "RESEARCH_LIBS": str(r / "rl"),
                    "EXPANSION_ROOT": str(r / "xp"),
                    "WORKSHOP_ROOT": str(r / "ws"),
                    "BASECAMP_ROOT": str(r / "bc"),
                    "TRANSLATION_WORK_ROOT": str(r / "tw")}
        self.out = r / "out"

    def run_index(self):
        with mock.patch.dict(os.environ, self.env):
            self.assertEqual(essay_starters.main(
                ["index", "--out", str(self.out)]), 0)
        return json.loads((self.out / "INDEX.json").read_text())

    def test_index_kinds_and_dedupe(self):
        starters = self.run_index()
        kinds = {}
        for s in starters:
            kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
        self.assertEqual(kinds.get("essay-md"), 2)  # te essay + rl note; dup collapsed, README skipped
        self.assertEqual(kinds.get("expansion-essay"), 1)
        self.assertEqual(kinds.get("workshop-essay"), 1)
        self.assertEqual(kinds.get("essay-object"), 1)
        self.assertEqual(kinds.get("contention"), 1)
        self.assertEqual(kinds.get("essay-seed"), 1)
        essay = next(s for s in starters
                       if s["kind"] == "essay-md" and s["refs"])
        self.assertEqual(essay["title"], "Why Rebirth")
        self.assertEqual(essay["refs"], ["karma-01", "karma-02"])
        self.assertEqual(essay["timestamps"], 1)
        self.assertEqual(essay["headings"], ["The objection", "Images"])
        eo = next(s for s in starters if s["kind"] == "essay-object")
        self.assertEqual(eo["crux"], "the crux here")
        ws = next(s for s in starters if s["kind"] == "workshop-essay")
        self.assertEqual(ws["body_kinds"], {"ai": 1, "source": 1})
        self.assertTrue((self.out / "INDEX.md").is_file())

    def test_glossary_apparatus_filtered(self):
        import essay_starters as es
        self.assertFalse(es.gloss_ok("BRANCHES", "the next ones"))
        self.assertFalse(es.gloss_ok("in-the-sūtra", "sūtre"))
        self.assertFalse(es.gloss_ok("Fuller", "Syn 700.01"))
        self.assertFalse(es.gloss_ok("MARK", "archive"))
        self.assertTrue(es.gloss_ok("śarīra", "the body"))
        self.assertTrue(es.gloss_ok("Abhinava", "Abhinavagupta the teacher"))

    def test_glossary_ranking_and_filters(self):
        with mock.patch.dict(os.environ, self.env):
            self.assertEqual(essay_starters.main(
                ["glossary", "--out", str(self.out), "--top", "50"]), 0)
        props = json.loads((self.out / "glossary-proposals.json").read_text())
        by_term = {p["term"]: p for p in props}
        self.assertIn("śarīra", by_term)
        self.assertEqual(by_term["śarīra"]["rendering"], "the body")
        self.assertNotIn("self", by_term)  # all-ASCII lowercase, filtered
        self.assertNotIn("backbone", by_term)  # no paren gloss, never mined
        self.assertNotIn("stitches", by_term)
        self.assertTrue(all(p["status"] == "proposed" for p in props))
        self.assertTrue(all(p["refs"] for p in props))

    def test_anchor_math(self):
        self.run_index()
        with mock.patch.dict(os.environ, self.env):
            with mock.patch("sys.argv", ["x"]):
                pass
        gloss = [{"term": "ātman", "rendering": "the self", "files": 1,
                  "occurrences": 1, "refs": [], "status": "proposed"},
                 {"term": "freedom", "rendering": "release", "files": 1,
                  "occurrences": 1, "refs": [], "status": "proposed"}]
        (self.out / "glossary-proposals.json").write_text(json.dumps(gloss))
        with mock.patch.dict(os.environ, self.env):
            self.assertEqual(essay_starters.main(
                ["anchor", "--out", str(self.out),
                 "--index", str(self.out / "INDEX.json"),
                 "--glossary", str(self.out / "glossary-proposals.json")]), 0)
        rep = {r["path"]: r for r in json.loads(
            (self.out / "anchor-report.json").read_text())}
        essay = next(r for r in rep.values() if r["terms_anchored"])
        # clip refs karma-01/02 are external (not tw chunks); ātman anchors to w1:s1
        self.assertEqual(essay["locators_resolved"], [])
        self.assertIn("ātman", essay["terms_anchored"])
        self.assertEqual(essay["terms_anchored"]["ātman"], ["w1:s1"])
        self.assertEqual(essay["coverage"], round(1 / 3, 3))


if __name__ == "__main__":
    unittest.main()
