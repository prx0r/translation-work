"""Unit tests for tools/scholar_memo.py. API mocked; fixture trees on disk."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import scholar_memo  # noqa: E402


def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    return p


class MemoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        r = self.tmp
        for mod, val in (("TW", r / "tw"), ("SVREAD", r / "sv"),
                         ("TANTRAESSAYS", r / "te"), ("RESEARCH_LIB", r / "rl"),
                         ("LEVIN", r / "lev"), ("IPVV", r / "ipvv")):
            setattr(scholar_memo, mod, val)
        write(r / "tw" / "w1" / "STATUS.json", "{}")
        write(r / "tw" / "w1" / "GATE.json", json.dumps({
            "s1": {"deterministic_gate": "BLOCKED", "blocking": ["ABSTENTION"]},
            "s2": {"deterministic_gate": "PASS", "blocking": []}}))
        write(r / "tw" / "w1" / "ARGMAP.md",
              "# Arg\n\n## s1\nSome reasoning.\nUnresolved: who perceives?\n"
              "Unresolved: none.\n")
        write(r / "tw" / "w1" / "T1-s1.md", "light of freedom shines")
        write(r / "tw" / "w1" / "T1-s2.md", "freedom of movement here")
        write(r / "tw" / "w1" / "T1-s9.l0.roundtrip.md", "freedom roundtrip")
        write(r / "tw" / "w2" / "STATUS.json", "{}")
        write(r / "tw" / "w2" / "T1-x1.md", "freedom and light together")
        write(r / "sv" / "data" / "scholar" / "w1.json", '{"work":"w1"}')
        write(r / "sv" / "data" / "pushing-catalog.json", json.dumps(
            {"format": "f", "revision": "r", "records": [
                {"file": "w1/LOGICVID-a.md", "git_blob": "b",
                 "question": "why light?", "title": "T", "work": "w1"}]}))
        write(r / "te" / "metadata.json", json.dumps({"lectures": [
            {"file": "kundalini.mp3", "topics": ["freedom", "breath"],
             "summary": "on liberation"}]}))
        write(r / "rl" / "freedom-and-grace.md", "x")
        write(r / "lev" / "levin_freedom_paper.pdf", "")
        write(r / "ipvv" / "site" / "data" / "variants" / "w1.json",
              '{"s1": ["v"], "other": ["s1", "s1"]}')
        self.state = r / "state.json"

    def tearDown(self):
        import importlib
        importlib.reload(scholar_memo)

    def docs(self, rows):
        return {"documents": rows}

    def test_gate_argmap_pushing_variants(self):
        self.assertEqual(scholar_memo.gate_objections("w1", "s1-v02"),
                         ["gate BLOCKED: ABSTENTION"])
        self.assertEqual(scholar_memo.gate_objections("w1", "s2"), [])
        self.assertEqual(scholar_memo.gate_objections("w9", "s1"), [])
        self.assertIn("who perceives",
                      scholar_memo.argmap_open("w1", "s1-v01")[0])
        self.assertEqual(scholar_memo.argmap_open("w1", "s9"), [])
        self.assertEqual(len(scholar_memo.pushing_open("w1")), 1)
        self.assertEqual(scholar_memo.variant_mentions("w1", "s1"),
                         ["3 variant record(s) mention this target"])
        self.assertEqual(scholar_memo.variant_mentions("w9", "s1"), [])

    def test_t1_hits_skip_self_and_cap(self):
        hits = scholar_memo.t1_hits(["freedom"], skip_work="w1",
                                    skip_target="s1", cap=8)
        self.assertTrue(any(h.startswith("w1:s2") for h in hits))
        self.assertTrue(any(h.startswith("w2:x1") for h in hits))
        self.assertFalse(any("w1:s1" in h for h in hits))
        self.assertFalse(any("roundtrip" in h for h in hits))

    def test_crossover_leads_file_refs_only(self):
        leads = scholar_memo.crossover_leads(["freedom"])
        joined = "\n".join(leads)
        self.assertIn("tantraessays:kundalini.mp3", joined)
        self.assertIn("research-library:freedom-and-grace.md", joined)
        self.assertIn("levin:levin_freedom_paper.pdf", joined)
        self.assertTrue(all("unverified" in l for l in leads))

    def test_title_keywords(self):
        keys = scholar_memo.title_keywords("Why Freedom Matters Here",
                                           ["grace"])
        self.assertIn("freedom", keys)
        self.assertIn("grace", keys)
        self.assertNotIn("why", keys)

    def test_suggested_works_ranked_unprojected_only(self):
        sug = scholar_memo.suggested_works(["freedom", "light"])
        self.assertEqual(len(sug), 1)
        self.assertTrue(sug[0].startswith("w2"))

    def router(self, docs_by_work, decisions_by_work):
        def run(api_base, cookie, method, path, payload=None):
            if method == "GET" and path.startswith("/api/scholar/documents?work="):
                return 200, self.docs(docs_by_work.get(path.split("work=")[1], []))
            if method == "GET" and path.startswith("/api/scholar/decisions?work="):
                return 200, {"decisions": decisions_by_work.get(path.split("work=")[1], [])}
            if method == "PUT":
                self.posted = (path, payload)
                return 200, {"document": {"id": "note-x", "revision": 1}}
            raise AssertionError(f"unexpected {method} {path}")
        return run

    def base_args(self, **kw):
        d = {"api": "http://x", "cookie": "c", "work": ["w1"], "doc": None,
             "all": False, "post": False, "out": None, "suggest_works": False,
             "state": str(self.state), "no_state": False}
        d.update(kw)
        return type("A", (), d)()

    def test_memo_new_then_nothing_new(self):
        doc = {"id": "translation:l2:s1", "kind": "translation", "work": "w1",
               "target": "s1", "layer": "l2", "revision": 2,
               "content_json": "{}"}
        dec = {"id": "decision:1", "subject": "term: freedom",
               "after_text": "release", "reason": "g", "work": "w1", "target": "s1"}
        with mock.patch.object(scholar_memo, "api",
                               side_effect=self.router({"w1": [doc]}, {"w1": [dec]})):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(scholar_memo.cmd_memo(self.base_args()), 0)
            out = buf.getvalue()
        self.assertIn("## Objections", out)
        self.assertIn("ABSTENTION", out)
        self.assertIn("## Related passages", out)
        self.assertIn("w2:x1", out)
        self.assertIn("## Crossover leads", out)
        self.assertEqual(json.loads(self.state.read_text())["translation:l2:s1"], 2)
        with mock.patch.object(scholar_memo, "api",
                               side_effect=self.router({"w1": [doc]}, {"w1": [dec]})):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(scholar_memo.cmd_memo(self.base_args()), 0)
            self.assertIn("nothing new", buf.getvalue())

    def test_essay_memo_variant_briefs_and_post(self):
        content = json.dumps({"text": "x" * 50,
                              "citations": [{"target": "s1"}, {"target": "s2"}]})
        doc = {"id": "essay:e1", "kind": "essay", "work": "w1", "target": "s1",
               "layer": "", "title": "On Freedom", "revision": 1,
               "content_json": content}
        with mock.patch.object(scholar_memo, "api",
                               side_effect=self.router({"w1": [doc]}, {"w1": []})):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(scholar_memo.cmd_memo(
                    self.base_args(post=True, all=True)), 0)
            out = buf.getvalue()
        self.assertIn("## Variant briefs", out)
        self.assertIn("2/10 pinned citations", out)
        path, payload = self.posted
        self.assertTrue(path.endswith("memo-essay:e1-r1"))
        self.assertEqual(payload["kind"], "note")
        self.assertFalse(payload["content"]["assisted"])
        self.assertEqual(payload["content"]["agent_source"], "scholar-memo/1")

    def test_doc_filter_and_unknown_doc(self):
        with mock.patch.object(scholar_memo, "api",
                               side_effect=self.router({"w1": []}, {"w1": []})):
            with self.assertRaises(SystemExit):
                scholar_memo.cmd_memo(self.base_args(doc="translation:l2:zzz"))


if __name__ == "__main__":
    unittest.main()
