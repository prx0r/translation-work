"""Unit tests for tools/scholar_apply.py. API is mocked; no network, no writes."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import scholar_apply  # noqa: E402


def decision(subject, after, reason="", did="decision:1", work="w", target="t"):
    return {"id": did, "subject": subject, "after_text": after, "reason": reason,
            "work": work, "target": target}


class GlossaryTest(unittest.TestCase):
    def api(self, rows):
        return mock.patch.object(scholar_apply, "api",
                                 return_value=(200, {"decisions": rows}))

    def test_latest_wins_and_malformed_ignored(self):
        rows = [decision("term: light", "new-light", "new grounds", "decision:2"),
                decision("term: light", "old-light", "old grounds", "decision:1"),
                decision("a normal choice", "x", "y"),
                decision("term: empty", "", "no after"),
                decision("term:   ", "x", "blank term")]
        with self.api(rows):
            g = scholar_apply.fetch_glossary("http://x", "c")
        self.assertEqual(g["light"]["after"], "new-light")
        self.assertEqual(g["light"]["decision_id"], "decision:2")
        self.assertNotIn("a normal choice", g)
        self.assertNotIn("empty", g)

    def test_non_list_response_is_empty(self):
        with self.api({}):
            self.assertEqual(scholar_apply.fetch_glossary("http://x", "c"), {})


class SubstituteTest(unittest.TestCase):
    def test_longest_first_and_whole_word(self):
        g = {"freedom": {"after": "F", "reason": "", "decision_id": "",
                         "work": "", "target": ""},
             "freedom of": {"after": "FO", "reason": "", "decision_id": "",
                            "work": "", "target": ""}}
        text, applied = scholar_apply.substitute_prose(
            "freedom of movement and freedom, not freedoms", g)
        self.assertEqual(text, "FO movement and F, not freedoms")
        self.assertEqual({a["term"]: a["count"] for a in applied},
                         {"freedom of": 1, "freedom": 1})

    def test_unknown_terms_pass_through(self):
        g = {"known": {"after": "K", "reason": "", "decision_id": "",
                       "work": "", "target": ""}}
        text, applied = scholar_apply.substitute_prose("known and unknown", g)
        self.assertEqual(text, "K and unknown")
        self.assertEqual(len(applied), 1)


class ReplayL0Test(unittest.TestCase):
    def tokens(self):
        return [{"surface": "sva", "chosen_index": 0,
                 "options": [{"gloss": "own"}, {"gloss": "one's own"}]},
                {"surface": "tantra", "chosen_index": 0,
                 "options": [{"gloss": "loom"}]}]

    def test_replay_sets_index_and_carries_grounds(self):
        g = {"sva": {"after": "one's own", "reason": "reflexive, not possessive",
                     "decision_id": "decision:9", "work": "w", "target": "t"}}
        toks, applied, skipped = scholar_apply.replay_l0(self.tokens(), g)
        self.assertEqual(toks[0]["chosen_index"], 1)
        self.assertEqual(applied[0]["decision_id"], "decision:9")
        self.assertIn("reflexive", applied[0]["reason"])
        self.assertEqual(skipped, [])

    def test_missing_option_reported_not_forced(self):
        g = {"tantra": {"after": "system", "reason": "", "decision_id": "",
                        "work": "", "target": ""}}
        toks, applied, skipped = scholar_apply.replay_l0(self.tokens(), g)
        self.assertEqual(toks[1]["chosen_index"], 0)
        self.assertEqual(applied, [])
        self.assertEqual(skipped[0]["term"], "tantra")

    def test_non_list_base_refused(self):
        with self.assertRaises(SystemExit):
            scholar_apply.replay_l0({"nope": 1}, {})


class ApplyFlowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.proj = Path(self.tmp.name) / "svread" / "data" / "scholar"
        self.proj.mkdir(parents=True)
        self.proj.joinpath("w.json").write_text(json.dumps({
            "work": "w",
            "originals": {"l2": {"t1": {"plain_english": "the light of freedom"}},
                          "l0": {"t1": []}},
            "original_hashes": {"l2": {"t1": "a" * 64}, "l0": {"t1": "b" * 64}}}))
        self.old_svread = scholar_apply.SVREAD
        scholar_apply.SVREAD = Path(self.tmp.name) / "svread"
        self.calls = []
        self.docs = []

    def tearDown(self):
        scholar_apply.SVREAD = self.old_svread
        self.tmp.cleanup()

    def fake_api(self, status, payload):
        def run(api_base, cookie, method, path, body=None):
            self.calls.append((method, path, body))
            if isinstance(payload, Exception):
                raise payload
            return status, payload() if callable(payload) else payload
        return mock.patch.object(scholar_apply, "api", side_effect=run)

    def _router(self):
        def run(api_base, cookie, method, path, body=None):
            self.calls.append((method, path, body))
            if method == "GET" and path.startswith("/api/scholar/documents"):
                return 200, self.docs
            if method == "PUT":
                return 200, {"document": {"id": "translation:l2:t1", "revision": 3}}
            if method == "POST":
                return 201, {"id": f"decision:{len(self.calls)}"}
            raise AssertionError(f"unexpected call {method} {path}")
        return run

    def test_full_flow(self):
        glossary = {"freedom": {"after": "svātantrya",
                                "reason": "keep the Sanskrit",
                                "decision_id": "decision:7",
                                "work": "w", "target": "t0"}}
        with mock.patch.object(scholar_apply, "fetch_glossary", return_value=glossary):
            with mock.patch.object(scholar_apply, "api", side_effect=self._router()):
                args = type("A", (), {"api": "http://x", "cookie": "c",
                                      "base": "w:t1:l2", "title": ""})()
                self.assertEqual(scholar_apply.cmd_apply(args), 0)
        puts = [c for c in self.calls if c[0] == "PUT"]
        self.assertEqual(len(puts), 1)
        method, path, payload = puts[0]
        self.assertEqual(path, "/api/scholar/documents/translation:l2:t1")
        self.assertEqual(payload["expected_revision"], 0)
        self.assertFalse(payload["content"]["assisted"])
        self.assertEqual(payload["content"]["agent_source"], "scholar-apply/1")
        self.assertEqual(payload["content"]["text"], "the light of svātantrya")
        self.assertEqual(payload["content"].get("render_field"), None)  # wire format unchanged
        self.assertEqual(payload["content"]["base_sha256"], "a" * 64)
        posts = [c for c in self.calls if c[0] == "POST"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0][2]["subject"], "term: freedom")
        self.assertEqual(posts[0][2]["before"], "freedom")
        self.assertIn("decision:7", posts[0][2]["reason"])
        self.assertEqual(posts[0][2]["revision"], 3)

    def test_dict_layer_reports_render_field(self):
        glossary = {"freedom": {"after": "svātantrya",
                                "reason": "keep the Sanskrit",
                                "decision_id": "decision:7",
                                "work": "w", "target": "t0"}}
        with mock.patch.object(scholar_apply, "fetch_glossary", return_value=glossary):
            with mock.patch.object(scholar_apply, "api", side_effect=self._router()):
                args = type("A", (), {"api": "http://x", "cookie": "c",
                                      "base": "w:t1:l2", "title": ""})()
                with mock.patch("builtins.print") as p:
                    self.assertEqual(scholar_apply.cmd_apply(args), 0)
        report = json.loads(p.call_args[0][0])
        self.assertEqual(report["render_field"], "plain_english")

    def test_unrenderable_dict_refuses(self):
        self.proj.joinpath("w.json").write_text(json.dumps({
            "work": "w", "originals": {"l2": {"t9": {"lines": ["a"]}}},
            "original_hashes": {"l2": {"t9": "c" * 64}}}))
        glossary = {"a": {"after": "b", "reason": "", "decision_id": "",
                          "work": "", "target": ""}}
        with mock.patch.object(scholar_apply, "fetch_glossary", return_value=glossary):
            with mock.patch.object(scholar_apply, "api", side_effect=self._router()):
                args = type("A", (), {"api": "http://x", "cookie": "c",
                                      "base": "w:t9:l2", "title": ""})()
                with self.assertRaises(SystemExit):
                    scholar_apply.cmd_apply(args)

    def test_no_match_means_no_write(self):
        glossary = {"absent": {"after": "X", "reason": "", "decision_id": "",
                               "work": "", "target": ""}}
        with mock.patch.object(scholar_apply, "fetch_glossary", return_value=glossary):
            with mock.patch.object(scholar_apply, "api", side_effect=self._router()):
                args = type("A", (), {"api": "http://x", "cookie": "c",
                                      "base": "w:t1:l2", "title": ""})()
                self.assertEqual(scholar_apply.cmd_apply(args), 0)
        self.assertEqual([c for c in self.calls if c[0] in ("PUT", "POST")], [])

    def test_no_glossary_refuses(self):
        with mock.patch.object(scholar_apply, "fetch_glossary", return_value={}):
            args = type("A", (), {"api": "http://x", "cookie": "c",
                                  "base": "w:t1:l2", "title": ""})()
            with self.assertRaises(SystemExit):
                scholar_apply.cmd_apply(args)

    def test_unknown_base_refuses(self):
        with mock.patch.object(scholar_apply, "fetch_glossary",
                               return_value={"x": {"after": "y", "reason": "",
                                                   "decision_id": "",
                                                   "work": "", "target": ""}}):
            args = type("A", (), {"api": "http://x", "cookie": "c",
                                  "base": "w:nope:l2", "title": ""})()
            with self.assertRaises(SystemExit):
                scholar_apply.cmd_apply(args)


if __name__ == "__main__":
    unittest.main()
