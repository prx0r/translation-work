"""Unit tests for tools/audit_draft.py (exit codes + receipt shape)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import audit_draft  # noqa: E402


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "draft.md").write_text(
            'He says "I resort to You" [paramarthasara:param-p01-v01].\n',
            encoding="utf-8")
        self.refs = json.dumps([{"kind": "chunk", "work": "paramarthasara",
                                 "target": "param-p01-v01"}])

    def run_cli(self, *argv):
        out = io_capture = __import__("io").StringIO()
        with mock.patch("sys.stdout", io_capture):
            code = audit_draft.main(list(argv))
        return code, json.loads(io_capture.getvalue())

    def test_pass_exit_zero(self):
        code, receipt = self.run_cli("--text-file", str(self.tmp / "draft.md"),
                                 "--refs", self.refs)
        self.assertEqual(code, 0)
        self.assertEqual(receipt["verdict"], "PASS")
        self.assertEqual(len(receipt["content_sha256"]), 64)

    def test_fail_exit_one(self):
        code, receipt = self.run_cli("--text", "A claim [frobnicate:x9] stands.",
                                 "--refs", self.refs)
        self.assertEqual(code, 1)
        self.assertEqual(receipt["verdict"], "FAIL")

    def test_bad_json_exit_two(self):
        with mock.patch("sys.stdout", __import__("io").StringIO()):
            self.assertEqual(audit_draft.main(["--text", "x", "--refs", "{bad"]), 2)


if __name__ == "__main__":
    unittest.main()
