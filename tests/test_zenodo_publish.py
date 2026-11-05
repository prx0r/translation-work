"""Unit tests for tools/zenodo_publish.py. Local HTTP fixture, no real network."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import zenodo_publish as zp  # noqa: E402


def write(p: Path, s: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    return p


ESSAY = {
    "essay_id": "essay:" + "a" * 64, "title": "T", "author": "A Scholar",
    "author_id": "u1", "text": "Some text here.", "rights": "cc-by-4.0",
    "target": "", "work": "w1", "format": "scholar-essay/1",
    "identity_state": "SELF_ATTESTED", "model": "",
    "signoff": {"id": "signoff:1"}, "snapshot": {}, "assisted": False,
    "validation_scope": "s",
}


class ZenodoTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.tmp = Path(self.temp.name)
        for mod, val in (("SVREAD", self.tmp / "sv"), ("TW", self.tmp / "tw")):
            setattr(zp, mod, val)
        write(self.tmp / "sv" / "data" / "scholar" / "w1.json",
              json.dumps({"work": "w1", "essays": [ESSAY]}))
        self.out = self.tmp / "bundle"
        self.args = lambda **kw: type("A", (), {"work": "w1", "essay": ESSAY["essay_id"],
                                                "out": str(self.out), "pub_type": "preprint",
                                                "sandbox": False, "confirm_live": True,
                                                "creator": None, "affiliation": None,
                                                "orcid": None, **kw})()

    def test_bundle_dry_run_writes_files(self):
        self.assertEqual(zp.cmd_bundle(self.args()), 0)
        for name in ("essay.md", "essay.json", "provenance.json"):
            self.assertTrue((self.out / name).is_file())
        prov = json.loads((self.out / "provenance.json").read_text())
        self.assertEqual(prov["rights"], "cc-by-4.0")
        self.assertEqual(prov["essay_id"], ESSAY["essay_id"])

    def test_metadata_open_vs_closed(self):
        m = zp.deposition_metadata("w1", dict(ESSAY, rights="all-rights-reserved"), self.args())
        self.assertEqual(m["metadata"]["access_right"], "closed")
        self.assertIsNone(m["metadata"]["license"])
        m2 = zp.deposition_metadata("w1", dict(ESSAY, rights="cc0"), self.args())
        self.assertEqual(m2["metadata"]["access_right"], "open")
        self.assertIn("Peer-review status is not established", m2["metadata"]["notes"])
        self.assertIn("AI assistance: none declared", m2["metadata"]["description"])
        assisted = zp.deposition_metadata("w1", dict(ESSAY, assisted=True, model=""), self.args())
        self.assertIn("AI assistance: yes (model not recorded)", assisted["metadata"]["description"])

    def test_publish_refuses_without_confirm_or_token(self):
        with self.assertRaises(SystemExit):
            zp.cmd_publish(self.args(confirm_live=False))
        with mock.patch.dict("os.environ", {}, clear=False):
            with mock.patch.object(zp, "token", return_value=""):
                with self.assertRaises(SystemExit):
                    zp.cmd_publish(self.args())

    def test_publish_flow_against_fixture_server(self):
        seen = {}

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _json(self, obj, code=200):
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(obj).encode())

            def do_POST(self):
                n = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(n) if n else b""
                seen.setdefault("post", []).append((self.path, body[:200].decode(errors="replace")))
                if self.path == "/api/deposit/depositions":
                    port = self.server.server_address[1]
                    return self._json({"id": 7, "links": {"bucket": f"http://127.0.0.1:{port}/b"}})
                if self.path.endswith("/actions/publish"):
                    return self._json({"doi": "10.5281/zenodo.7", "conceptdoi": "10.5281/zenodo.6"})
                return self._json({}, 404)

            def do_PUT(self):
                n = int(self.headers.get("Content-Length", 0))
                self.rfile.read(n)
                seen.setdefault("put", []).append(self.path)
                if self.path.startswith("/api/deposit/depositions/7"):
                    return self._json({"id": 7})
                return self._json({}, 200)

        srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}/api"
        reg = self.tmp / "dois.json"
        with mock.patch.object(zp, "token", return_value="tok"):
            with mock.patch.object(zp, "DOI_REGISTRY", reg):
                with mock.patch.object(zp, "LIVE_API", base):
                    with mock.patch.object(zp, "SANDBOX_API", base):
                        buf = io.StringIO()
                        with mock.patch("sys.stdout", buf):
                            self.assertEqual(zp.cmd_publish(self.args()), 0)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["doi"], "10.5281/zenodo.7")
        self.assertEqual(json.loads(reg.read_text())[ESSAY["essay_id"]]["doi"],
                         "10.5281/zenodo.7")
        paths = [p for p, _ in seen.get("post", [])]
        self.assertTrue(any(p.endswith("/actions/publish") for p in paths))
        srv.shutdown()
        srv.server_close()


if __name__ == "__main__":
    unittest.main()
