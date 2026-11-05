"""Regression tests for Scholar version import and historical snapshots."""
from __future__ import annotations

import contextlib
import http.client
import io
import json
import multiprocessing
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import agent_contract  # noqa: E402
import emit_scholar  # noqa: E402
import emit_site_general  # noqa: E402
import intake  # noqa: E402
import scholar  # noqa: E402
import scholar_service  # noqa: E402
import style_profile  # noqa: E402
from schemas import registry  # noqa: E402


class ScholarImportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.root = Path(self.temp.name)
        self.old_root = scholar.ROOT
        scholar.ROOT = self.root
        self.data = self.root / "paramarthasara" / "data"
        self.data.mkdir(parents=True)
        shutil.copy(ROOT / "paramarthasara/data/param-p01.l3.json", self.data)
        shutil.copy(ROOT / "paramarthasara/data/param-p01.l0.json", self.data)
        self.original = scholar.load_original("paramarthasara", "l3", "param-p01-v01")[0]

    def tearDown(self):
        scholar.ROOT = self.old_root
        self.temp.cleanup()

    def submission(self):
        common = {"work": "paramarthasara", "layer": "l3", "target": "param-p01-v01",
                  "author": "a scholar", "base_sha256": scholar.sha(self.original)}
        first = {**common, "version_id": "local:first", "parent": None,
                 "content": {"lines": ["A first rendering."]}}
        second = {**common, "version_id": "local:second", "parent": "local:first",
                  "content": {"lines": ["A revised rendering."]}}
        return {"format": "scholar-submission/v1", "work": "paramarthasara",
                "versions": [first, second]}

    def run_import(self, payload):
        path = self.root / "submission.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            scholar.cmd_import(SimpleNamespace(file=str(path)))
        return json.loads(output.getvalue())

    def test_import_preserves_chain_objects_and_retry(self):
        payload = self.submission()
        result = self.run_import(payload)
        rows = scholar.load_versions("paramarthasara")
        self.assertEqual(result["imported"], 2)
        self.assertEqual(rows[1]["parent"], rows[0]["version_id"])
        self.assertEqual(rows[0]["author_kind"], "human")
        self.assertEqual(rows[0]["content"]["verse_id"], "param-p01-v01")
        for row in rows:
            path = scholar.object_path("paramarthasara", row["content_sha256"])
            self.assertEqual(path.read_bytes(), scholar.canon(row["content"]))
        ledger = scholar.vpath("paramarthasara").read_bytes()
        self.assertEqual(self.run_import(payload)["imported"], 0)
        self.assertEqual(scholar.vpath("paramarthasara").read_bytes(), ledger)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(scholar.verify("paramarthasara"), 0)

        # The new version retains its original base after the canonical row moves.
        path = self.data / "param-p01.l3.json"
        source = json.loads(path.read_text())
        source[0]["lines"] = ["The original was corrected later."]
        path.write_text(json.dumps(source), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(scholar.verify("paramarthasara"), 0)

    def test_invalid_batch_does_not_append_or_create_objects(self):
        payload = self.submission()
        payload["versions"][1]["content"] = {"lines": []}
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_import(payload)
        self.assertFalse(scholar.vpath("paramarthasara").exists())
        self.assertFalse((self.root / "paramarthasara/scholar/objects").exists())

    def test_l0_version_validates_and_snapshots_the_whole_verse(self):
        original = scholar.load_original("paramarthasara", "l0", "param-p01-v01")[0]
        edited = json.loads(json.dumps(original))
        edited[0]["options"][0]["gloss"] = "a revised lexical choice"
        payload = {"format": "scholar-submission/v1", "work": "paramarthasara",
                   "versions": [{"version_id": "local:l0", "parent": None,
                                 "work": "paramarthasara", "layer": "l0",
                                 "target": "param-p01-v01", "author": "a scholar",
                                 "base_sha256": scholar.sha(original), "content": edited}]}
        self.assertEqual(self.run_import(payload)["imported"], 1)
        row = scholar.load_versions("paramarthasara")[0]
        self.assertEqual(len(row["content"]), len(original))
        saved_schema = json.loads(scholar.object_path("paramarthasara", row["structural_schema_sha256"]).read_text())
        self.assertEqual(saved_schema["type"], "array")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(scholar.verify("paramarthasara"), 0)

    def test_stale_base_and_reused_local_id_are_rejected(self):
        payload = self.submission()
        payload["versions"][0]["base_sha256"] = "0" * 64
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_import(payload)
        payload = self.submission()
        self.run_import(payload)
        payload["versions"][0]["content"] = {"lines": ["Changed after submission."]}
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_import(payload)

    def test_concurrent_retries_do_not_duplicate_versions(self):
        path = self.root / "concurrent.json"
        path.write_text(json.dumps(self.submission()))
        ctx = multiprocessing.get_context("fork")
        start, results = ctx.Event(), ctx.Queue()

        def worker():
            start.wait()
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    scholar.cmd_import(SimpleNamespace(file=str(path)))
                results.put(json.loads(output.getvalue())["imported"])
            except Exception as exc:
                results.put(str(exc))

        processes = [ctx.Process(target=worker) for _ in range(2)]
        for process in processes:
            process.start()
        start.set()
        for process in processes:
            process.join(10)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual(sorted([results.get(timeout=1), results.get(timeout=1)]), [0, 2])
        self.assertEqual(len(scholar.load_versions("paramarthasara")), 2)

    def test_contract_is_repeatable_and_contains_all_layers(self):
        first = agent_contract.describe()
        self.assertEqual(agent_contract.content_hash(first),
                         agent_contract.content_hash(agent_contract.describe()))
        self.assertEqual([row["id"] for row in first["layers"]],
                         ["t1", "l0", "argmap", "l2", "c1", "l3", "l4", "c2"])
        for layer in first["layers"]:
            content = layer["example"]["content"]
            self.assertEqual(registry.structural_errors(content, layer["schema"], "example"), [])
            self.assertEqual(registry.validate(layer["id"], content), [])
        paths = {item["path"] for item in first["process_files"]}
        self.assertIn("skills/l4-song/SKILL.md", paths)
        self.assertIn("lore/bank/songcraft-bank.json", paths)

    def test_schema_release_detects_drift(self):
        self.assertEqual(registry.snapshot_errors(), [])
        with mock.patch.object(registry, "snapshot", return_value={"changed": True}):
            self.assertTrue(registry.snapshot_errors())

    def test_existing_layer_examples_are_discoverable_and_paginated(self):
        first = agent_contract.examples_catalog("l4", "paramarthasara", 0, 1)
        second = agent_contract.examples_catalog("l4", "paramarthasara", 1, 1)
        self.assertGreaterEqual(first["total_files"], 2)
        self.assertNotEqual(first["files"][0]["file"], second["files"][0]["file"])
        item = first["files"][0]
        self.assertEqual(item["song"], "param-p01")
        self.assertEqual(item["sha256"], agent_contract.file_hash(ROOT / item["file"]))
        self.assertIn("not human review", first["note"])

    def test_verify_reports_missing_v2_schema_field(self):
        self.run_import(self.submission())
        path = scholar.vpath("paramarthasara")
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        del rows[0]["structural_schema_sha256"]
        path.write_text("".join(json.dumps(row) + "\n" for row in rows))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertNotEqual(scholar.verify("paramarthasara"), 0)

    def test_intake_preserves_utf8_source_and_rejects_omissions(self):
        raw = "शिवः\nशक्तिः".encode("utf-8")
        split = len("शिवः".encode("utf-8"))
        segments = [{"song": "test-p01", "verse": 1, "verse_id": "test-p01-v01",
                     "start": 0, "end": split},
                    {"song": "test-p01", "verse": 2, "verse_id": "test-p01-v02",
                     "start": split + 1, "end": len(raw)}]
        self.assertEqual(intake.validate_segments(raw, segments), [])
        work = intake.initialize(self.root, "testwork", raw, segments, "Test edition", "unknown")
        self.assertEqual((work / "source/edition.txt").read_bytes(), raw)
        broken = [dict(row) for row in segments]
        broken[1]["start"] += len("श".encode("utf-8"))
        self.assertTrue(intake.validate_segments(raw, broken))
        old_root = style_profile.workcfg.ROOT
        style_profile.workcfg.ROOT = self.root
        try:
            self.assertEqual(style_profile.workcfg.song_verses("testwork", "test-p01"), [1, 2])
            self.assertEqual(style_profile.workcfg.source_spans("testwork")[1], ["शिवः"])
            (work / "source/edition.txt").write_bytes(raw + b"x")
            with self.assertRaises(ValueError):
                style_profile.workcfg.source_spans("testwork")
        finally:
            style_profile.workcfg.ROOT = old_root
            style_profile.workcfg.WORKS.pop("testwork", None)

    def test_style_context_uses_exact_intake_span_on_shared_line(self):
        raw = "शिवः शक्तिः".encode("utf-8")
        path = self.root / "edition.txt"
        path.write_bytes(raw)
        start = len("शिवः ".encode("utf-8"))
        cfg = {"source": path, "kind": "segments", "source_bytes": raw,
               "segments": [{"verse_id": "test-p01-v02", "start": start, "end": len(raw)}]}
        base = {"verse_id": "test-p01-v02", "lines": ["Power"]}
        old_root = style_profile.ROOT
        style_profile.ROOT = self.root
        try:
            with mock.patch.object(style_profile.workcfg, "work_config", return_value=cfg), \
                 mock.patch.object(style_profile, "original", side_effect=[base, {"source_lines": [1, 1]}]):
                context = style_profile.source_context("testwork", "test-p01-v02", "l3")
            self.assertEqual(context["source_excerpt"], "शक्तिः")
            self.assertEqual(context["source_byte_span"], [start, len(raw)])
        finally:
            style_profile.ROOT = old_root

    def test_audited_legacy_source_lines_cover_the_correct_verses(self):
        examples = {}
        for work in ("paramarthasara", "kramastotra"):
            cfg = style_profile.workcfg.work_config(work)
            spans = style_profile.workcfg.source_spans(work)
            for path in sorted((ROOT / work / "data").glob("*.t1.json")):
                for row in json.loads(path.read_text(encoding="utf-8")):
                    examples[row["verse_id"]] = emit_site_general.legacy_verse_source(cfg, spans, row)
            self.assertEqual(len([key for key in examples if key.startswith(
                "param-" if work == "paramarthasara" else "kram-")]), len(spans))
        self.assertIn("ekaṃ niviṣṭaṃ bahudhā guhāsu", examples["param-p01-v01"])
        self.assertTrue(examples["kram-p02-v02"].startswith("vimṛśya svātmānaṃ"))
        self.assertNotIn("[AgKs_", examples["kram-p29-v29"])
        self.assertTrue(examples["kram-p30-v30"].startswith("ṣaṭṣaṣṭinām"))
        cfg = style_profile.workcfg.work_config("kramastotra")
        spans = style_profile.workcfg.source_spans("kramastotra")
        wrong = json.loads((ROOT / "kramastotra/data/kram-p02.t1.json").read_text())[0]
        wrong["source_lines"] = [10, 12]
        with self.assertRaises(ValueError):
            emit_site_general.legacy_verse_source(cfg, spans, wrong)

    def test_review_signature_covers_reasoning(self):
        event = scholar.ReviewEvent(
            review_id="test-review", reasoning="original reasoning", decision="ACCEPT").emit()
        secret = bytes(range(32))
        public = scholar.ed25519.pubkey(secret)
        signature = scholar.ed25519.sign(secret, scholar.review_signature_message(event))
        self.assertTrue(scholar.ed25519.verify(public, scholar.review_signature_message(event), signature))
        event["reasoning"] = "different reasoning"
        event["event_hash"] = scholar.contract_sha({key: value for key, value in event.items()
                                                    if key != "event_hash"})
        self.assertFalse(scholar.ed25519.verify(public, scholar.review_signature_message(event), signature))

    def test_scholar_projection_withholds_blocked_layer_contents(self):
        self.run_import(self.submission())
        proof_dir = self.root / "paramarthasara/proof"
        proof_dir.mkdir()
        proof = {"work": "paramarthasara", "song": "param-p01", "deterministic_gate": "BLOCKED"}
        (proof_dir / "proof-param-p01.json").write_text(json.dumps(proof))
        old_root = emit_scholar.ROOT
        emit_scholar.ROOT = self.root
        try:
            projection = emit_scholar.build("paramarthasara")
            self.assertEqual(projection["withheld_songs"], ["param-p01"])
            self.assertEqual(projection["versions"], [])
            self.assertNotIn("A revised rendering", json.dumps(projection))
            for layer in ("t1", "argmap", "l2", "c1"):
                shutil.copy(ROOT / f"paramarthasara/data/param-p01.{layer}.json", self.data)
            proof["deterministic_gate"] = "PASS"
            proof["layer_sha256"] = {
                layer: scholar.sha(json.loads((self.data / f"param-p01.{layer}.json").read_text()))
                for layer in ("t1", "l0", "argmap", "l2", "c1", "l3")}
            (proof_dir / "proof-param-p01.json").write_text(json.dumps(proof))
            first = emit_scholar.build("paramarthasara")
            second = emit_scholar.build("paramarthasara")
            self.assertEqual(first["projection_sha256"], second["projection_sha256"])
            self.assertEqual(len(first["versions"]), 2)
            # No manifest exists: stale legacy proofs must still withhold originals and versions.
            stale = self.data / "param-p01.l2.json"
            data = json.loads(stale.read_text()); data[0]["plain_english"] += " Changed."
            stale.write_text(json.dumps(data))
            projection = emit_scholar.build("paramarthasara")
            self.assertEqual(projection["withheld_songs"], ["param-p01"])
            self.assertEqual(projection["versions"], [])
        finally:
            emit_scholar.ROOT = old_root

    def test_l4_craft_requires_exact_match_to_the_public_layer(self):
        path = self.root / 'paramarthasara/L4-test.DRAFT.json'
        l4 = {'verse_id':'param-p01-v01','lines':['A song']}
        path.write_text(json.dumps({'l4':l4,'craft':'Keep the turn'}))
        old_root = emit_scholar.ROOT
        emit_scholar.ROOT = self.root
        try:
            self.assertEqual(emit_scholar.song_craft('paramarthasara',{'l4':{}}),{})
            self.assertEqual(emit_scholar.song_craft('paramarthasara',{'l4':{'param-p01-v01':{'verse_id':'param-p01-v01','lines':['Changed']}}}),{})
            result=emit_scholar.song_craft('paramarthasara',{'l4':{'param-p01-v01':l4}})
            self.assertEqual(result['param-p01-v01'][0]['notes']['craft'],'Keep the turn')
        finally:
            emit_scholar.ROOT = old_root

    def test_legacy_single_passage_target(self):
        self.assertEqual(scholar.song_of('pan-p01','l3'),'pan-p01')
        self.assertEqual(scholar.song_of('param-p01-v01','l3'),'param-p01')

    def test_intake_emitter_uses_complete_source_and_withholds_stale_proof(self):
        raw = "शिवः शक्तिः".encode("utf-8")
        split = len("शिवः".encode("utf-8"))
        segments = [{"song": "test-p01", "verse": 1, "verse_id": "test-p01-v01",
                     "start": 0, "end": split},
                    {"song": "test-p01", "verse": 2, "verse_id": "test-p01-v02",
                     "start": split + 1, "end": len(raw)}]
        work = intake.initialize(self.root, "testwork", raw, segments, "Test edition", "CC0-1.0")
        data = work / "data"
        t1 = [{"verse": 1, "verse_id": "test-p01-v01", "tokens": [{"quick_gloss": "Śiva"}]},
              {"verse": 2, "verse_id": "test-p01-v02", "tokens": [{"quick_gloss": "power"}]}]
        l2 = [{"verse": 1, "plain_english": "Śiva", "sanskrit_cite": "शि"},
              {"verse": 2, "plain_english": "Power", "sanskrit_cite": "श"}]
        for layer, rows in (("t1", t1), ("l2", l2)):
            (data / f"test-p01.{layer}.json").write_text(json.dumps(rows, ensure_ascii=False))
        proof = {"work": "testwork", "song": "test-p01", "deterministic_gate": "PASS",
                 "source_sha": scholar.hashlib.sha256("शिवः शक्तिः".encode()).hexdigest()[:16],
                 "layer_sha256": {"t1": scholar.sha(t1), "l2": scholar.sha(l2)}}
        (work / "proof/proof-test-p01.json").write_text(json.dumps(proof))
        site = self.root / "site"
        (site / "translations").mkdir(parents=True)
        old_root, old_site, old_cfg = emit_site_general.ROOT, emit_site_general.SITE, style_profile.workcfg.ROOT
        old_argv = sys.argv
        emit_site_general.ROOT, emit_site_general.SITE = self.root, site
        style_profile.workcfg.ROOT = self.root
        try:
            sys.argv = ["emit_site_general.py", "--work", "testwork"]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(emit_site_general.main(), 0)
            out = site / "translations/testwork.json"
            rows = json.loads(out.read_text())
            self.assertEqual([row["sanskrit"] for row in rows], ["शिवः", "शक्तिः"])
            self.assertEqual(rows[0]["gate"], "PASS")
            l2[0]["plain_english"] = "A changed reading"
            (data / "test-p01.l2.json").write_text(json.dumps(l2, ensure_ascii=False))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(emit_site_general.main(), 0)
            rows = json.loads(out.read_text())
            self.assertEqual(rows[0]["gate"], "BLOCKED")
            self.assertEqual(rows[0]["l2"], "")
            out.write_text(json.dumps([{"chunk": "old", "en_variants": []}]))
            sys.argv.append("--force")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(emit_site_general.main(), 2)
            self.assertEqual(json.loads(out.read_text())[0]["chunk"], "old")
        finally:
            emit_site_general.ROOT, emit_site_general.SITE = old_root, old_site
            style_profile.workcfg.ROOT = old_cfg
            style_profile.workcfg.WORKS.pop("testwork", None)
            sys.argv = old_argv

    def test_private_examples_generate_attributed_agent_submission(self):
        for layer in ("t1", "l0", "argmap", "l2", "c1", "l4"):
            shutil.copy(ROOT / f"paramarthasara/data/param-p01.{layer}.json", self.data)
        old_style_root = style_profile.ROOT
        old_source = style_profile.workcfg.WORKS["paramarthasara"]["source"]
        style_profile.ROOT = self.root
        style_profile.workcfg.WORKS["paramarthasara"]["source"] = (
            ROOT.parent / "ipvv/site/data/sanskrit/paramarthasara.txt")
        try:
            originals = json.loads((self.data / "param-p01.l3.json").read_text())
            drafts = []
            for index, row in enumerate(originals[:3]):
                drafts.append({"version_id": f"local:private-{index}",
                               "work": "paramarthasara", "layer": "l3",
                               "target": row["verse_id"], "parent": None,
                               "author": "a scholar", "author_kind": "human",
                               "content": {**row, "lines": [f"Private example {index}."]}})
            path = self.root / "private.json"
            path.write_text(json.dumps({"work": "paramarthasara", "versions": drafts}))
            profile = style_profile.prepare("a scholar", "paramarthasara", "param-p01-v01",
                                            "l3", [str(path)])
            self.assertTrue(profile["ready"])
            self.assertIn("ekaṃ niviṣṭaṃ bahudhā guhāsu", profile["target"]["source_excerpt"])
            script = ('import json,sys; json.load(sys.stdin); '
                      'print(json.dumps({"model":"test-model","content":{"lines":["A new draft."]}}))')
            runner = shlex.join([sys.executable, "-c", script])
            submission = style_profile.render(profile, runner, "test-agent")
            entry = submission["versions"][0]
            self.assertEqual(entry["author_kind"], "agent")
            self.assertEqual(entry["provenance"]["style_author"], "a scholar")
            self.assertNotIn("Private example", json.dumps(submission))
            self.assertEqual(self.run_import(submission)["imported"], 1)
        finally:
            style_profile.ROOT = old_style_root
            style_profile.workcfg.WORKS["paramarthasara"]["source"] = old_source

    def test_authenticated_submission_creates_idempotent_git_branch(self):
        repo = self.root / "repo"
        (repo / "tools").mkdir(parents=True)
        shutil.copy(ROOT / "tools/scholar.py", repo / "tools")
        shutil.copytree(ROOT / "tools/human_authority", repo / "tools/human_authority")
        shutil.copytree(ROOT / "schemas", repo / "schemas")
        target = repo / "paramarthasara/data"
        target.mkdir(parents=True)
        shutil.copy(ROOT / "paramarthasara/data/param-p01.l3.json", target)
        def git(*args):
            return subprocess.run(["git", "-C", str(repo), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init", "-b", "main")
        git("config", "user.name", "Test")
        git("config", "user.email", "test@example.invalid")
        git("add", ".")
        git("commit", "-m", "Initial source")
        original_head = git("rev-parse", "HEAD")
        payload = self.submission()
        first = scholar_service.submit(repo, payload, "authenticated scholar")
        second = scholar_service.submit(repo, payload, "authenticated scholar")
        self.assertEqual(first["commit"], second["commit"])
        self.assertEqual(git("rev-parse", "HEAD"), original_head)
        ledger = git("show", first["branch"] + ":paramarthasara/scholar/versions.jsonl")
        rows = [json.loads(line) for line in ledger.splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["author"], "authenticated scholar")
        self.assertEqual(rows[0]["author_kind"], "human")
        objects = git("ls-tree", "-r", "--name-only", first["branch"],
                      "paramarthasara/scholar/objects").splitlines()
        self.assertGreaterEqual(len(objects), 3)
        token = "x" * 40
        users = [{"author": "authenticated scholar", "token_sha256":
                  scholar.hashlib.sha256(token.encode()).hexdigest()}]
        self.assertEqual(scholar_service.authenticated_author(token, users), "authenticated scholar")
        self.assertIsNone(scholar_service.authenticated_author("bad", users))
        server = scholar_service.ThreadingHTTPServer(("127.0.0.1", 0),
            scholar_service.handler_for(repo, users, "https://svread.pages.dev", None))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            body = json.dumps(payload)
            connection.request("POST", "/v1/scholar/submissions", body,
                               {"Authorization": "Bearer bad", "Content-Type": "application/json"})
            self.assertEqual(connection.getresponse().status, 401)
            connection.close()
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            connection.request("POST", "/v1/scholar/submissions", body,
                               {"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read())["commit"], first["commit"])
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_configured_style_runner_uses_selected_endpoint(self):
        seen = {}
        class ModelHandler(scholar_service.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            def do_POST(self):
                seen["auth"] = self.headers.get("Authorization")
                seen["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                response = json.dumps({"model": "local-test", "choices": [{"message": {
                    "content": json.dumps({"content": {"lines": ["A draft."]}})}}]}).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
        server = scholar_service.ThreadingHTTPServer(("127.0.0.1", 0), ModelHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            env = {**os.environ, "STYLE_API_URL": f"http://127.0.0.1:{server.server_port}/chat/completions",
                   "STYLE_MODEL": "local-test", "STYLE_API_KEY": "test-key"}
            result = subprocess.run([sys.executable, str(ROOT / "tools/style_runner_openai.py")],
                input=json.dumps({"target": {"layer": "l3"}, "examples": []}), text=True,
                capture_output=True, env=env, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["content"]["lines"], ["A draft."])
            self.assertEqual(seen["auth"], "Bearer test-key")
            self.assertEqual(seen["body"]["model"], "local-test")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
