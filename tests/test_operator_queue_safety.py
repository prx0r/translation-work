"""Regression checks for the live MCP queue-maintenance controls."""
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class OperatorWrappersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class StubMCP:
            def __init__(self, *_args, **_kwargs):
                pass

            def tool(self, *_args, **_kwargs):
                return lambda fn: fn

        class StubMiddleware:
            pass

        class StubToolError(Exception):
            pass

        fastmcp = types.ModuleType("fastmcp")
        fastmcp.FastMCP = StubMCP
        fastmcp_exceptions = types.ModuleType("fastmcp.exceptions")
        fastmcp_exceptions.ToolError = StubToolError
        fastmcp_server = types.ModuleType("fastmcp.server")
        fastmcp_middleware = types.ModuleType("fastmcp.server.middleware")
        fastmcp_middleware.Middleware = StubMiddleware
        fastmcp_dependencies = types.ModuleType("fastmcp.server.dependencies")
        fastmcp_dependencies.get_http_request = lambda: None

        spec = importlib.util.spec_from_file_location("operator_under_test", ROOT / "mcp_server.py")
        cls.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {
            "fastmcp": fastmcp,
            "fastmcp.exceptions": fastmcp_exceptions,
            "fastmcp.server": fastmcp_server,
            "fastmcp.server.middleware": fastmcp_middleware,
            "fastmcp.server.dependencies": fastmcp_dependencies,
        }):
            spec.loader.exec_module(cls.module)

    def test_maintenance_tools_use_repository_paths(self):
        with patch.object(self.module, "_run", return_value={}) as run:
            self.module.recycle(dry_run=True)
            run.assert_called_with(["tools/recycle_failed.py", "--dry"])
            self.module.queue_guard(fix=True)
            run.assert_called_with(["tools/queue_guard.py", "--fix"])

    def test_failed_subprocess_reports_stderr_even_without_stdout(self):
        result = self.module._run(["-c", "import sys; sys.stderr.write('diagnostic'); sys.exit(2)"])
        self.assertEqual(result["_rc"], 2)
        self.assertIn("diagnostic", result["stderr"])

    def test_swarm_decisions_use_locked_queue_update(self):
        queue = [{"id": "draft", "kind": "tal_brief", "status": "done",
                  "attempts": 1, "max_attempts": 3, "note": ""}]
        calls = []

        def update(fn):
            calls.append(True)
            updated, result = fn(queue)
            self.assertIs(updated, queue)
            return result

        with patch.dict(sys.modules, {"beam_swarm": types.SimpleNamespace(queue_update=update)}):
            result = self.module.swarm_decide("draft", "bounce", "Explain missing verse coverage")
        self.assertEqual(calls, [True])
        self.assertEqual(result["status"], "pending")
        self.assertIn("missing verse", result["note"])

    def test_beam_review_bounces_through_shared_queue_update(self):
        queue = [{"id": "draft", "status": "done", "attempts": 1,
                  "max_attempts": 3, "note": "", "worker": "w1"}]
        calls = []

        def update(fn):
            calls.append(True)
            current, result = fn(queue)
            self.assertIs(current, queue)
            return result

        fake = types.SimpleNamespace(load_q=lambda: queue, queue_update=update)
        spec = importlib.util.spec_from_file_location("beam_review_under_test", ROOT / "tools" / "beam_review.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"beam_swarm": fake}):
            spec.loader.exec_module(module)
        result = module._apply_bounce("draft", "add the missing source span")
        self.assertEqual(calls, [True])
        self.assertEqual(result, "bounced")
        self.assertEqual(queue[0]["status"], "pending")
        self.assertEqual(queue[0]["worker"], "")
        self.assertIn("missing source span", queue[0]["note"])
        queue[0]["status"] = "claimed"
        self.assertEqual(module._apply_bounce("draft", "do not overwrite a live claim"), "changed")
        self.assertEqual(queue[0]["status"], "claimed")

    def test_validate_reports_gates_without_recording_proof(self):
        with patch.object(self.module, "_run", return_value={"_rc": 0}) as run:
            result = self.module.validate("work", "song")
        run.assert_called_once_with(["tools/validate_song.py", "--song", "song", "--work", "work"])
        self.assertFalse(result["proof_recorded"])
        self.assertIn("owner review", result["note"])

    def test_promotion_fails_closed_without_owner_authentication(self):
        with patch.object(self.module, "_run", side_effect=AssertionError("must not run proof")):
            result = self.module.promote("work", "song")
        self.assertFalse(result["promoted"])
        self.assertIn("owner approval", result["reason"])

    def _call_middleware(self, tool_name):
        async def run():
            context = types.SimpleNamespace(message=types.SimpleNamespace(name=tool_name))
            async def next_call(_context):
                return {"called": True}
            return await self.module.OwnerWriteAuthorizationMiddleware().on_call_tool(context, next_call)
        return __import__("asyncio").run(run())

    def test_read_allowlist_is_public_without_request_authentication(self):
        with patch.object(self.module, "get_http_request", side_effect=AssertionError("read should not fetch auth")):
            self.assertEqual(self._call_middleware("bibliography"), {"called": True})

    def test_latest_work_named_lore_lookup_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lore = root / "process" / "beam" / "lore"
            lore.mkdir(parents=True)
            work_brief = lore / "mukta-m00124.md"
            tal_brief = lore / "tal-a18.md"
            work_brief.write_text("work brief")
            tal_brief.write_text("tantraloka brief")
            with patch.object(self.module, "ROOT", root):
                self.assertEqual(self.module._lore_path("mukta-m00124"), work_brief)
                self.assertEqual(self.module._lore_path("tantraloka-a18"), tal_brief)

    def test_current_tool_inventory_is_fully_classified_and_sets_are_disjoint(self):
        public = self.module.PUBLIC_READ_TOOLS
        writes = self.module.OWNER_WRITE_TOOLS
        self.assertFalse(public & writes)
        self.assertEqual(set(self.module.TOOLS), public | writes)

    def test_unknown_tools_are_denied_even_with_valid_owner_bearer(self):
        token = "owner-secret-0123456789abcdef0123456789"
        request = types.SimpleNamespace(headers={"authorization": f"Bearer {token}"})
        with patch.dict(os.environ, {"SHASTRA_ENABLE_WRITES": "1", "SHASTRA_WRITE_BEARER": token}), \
             patch.object(self.module, "get_http_request", return_value=request):
            with self.assertRaises(self.module.ToolError):
                self._call_middleware("unrecognized_future_tool")

    def test_writes_require_opt_in_token_and_http_request(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(self.module.ToolError):
                self._call_middleware("swarm_seed")
        with patch.dict(os.environ, {"SHASTRA_ENABLE_WRITES": "1"}, clear=True):
            with self.assertRaises(self.module.ToolError):
                self._call_middleware("swarm_seed")
        with patch.dict(os.environ, {"SHASTRA_ENABLE_WRITES": "1", "SHASTRA_WRITE_BEARER": "short"}), \
             patch.object(self.module, "get_http_request", return_value=types.SimpleNamespace(
                 headers={"authorization": "Bearer short"})):
            with self.assertRaises(self.module.ToolError):
                self._call_middleware("swarm_seed")
        token = "owner-secret-0123456789abcdef0123456789"
        with patch.dict(os.environ, {"SHASTRA_ENABLE_WRITES": "1", "SHASTRA_WRITE_BEARER": token}), \
             patch.object(self.module, "get_http_request", side_effect=RuntimeError("no HTTP request")):
            with self.assertRaises(self.module.ToolError):
                self._call_middleware("swarm_seed")

    def test_write_bearer_is_exact_and_authorized_calls_continue(self):
        token = "owner-secret-0123456789abcdef0123456789"
        with patch.dict(os.environ, {"SHASTRA_ENABLE_WRITES": "1", "SHASTRA_WRITE_BEARER": token}):
            wrong = types.SimpleNamespace(headers={"authorization": "Bearer wrong"})
            with patch.object(self.module, "get_http_request", return_value=wrong):
                with self.assertRaises(self.module.ToolError):
                    self._call_middleware("swarm_seed")
            exact = types.SimpleNamespace(headers={"authorization": f"bEaReR {token}"})
            with patch.object(self.module, "get_http_request", return_value=exact):
                self.assertEqual(self._call_middleware("swarm_seed"), {"called": True})

    def test_supervisors_do_not_stage_commit_push_or_create_proofs(self):
        for name in ("ralph.sh", "continue.sh", "tal_run_all.sh"):
            with self.subTest(script=name):
                lines = (ROOT / "tools" / name).read_text().splitlines()
                active = '\n'.join(line for line in lines if not line.lstrip().startswith('#'))
                self.assertNotRegex(active, r'\bgit\s+(?:add|reset|commit|push)\b')
                self.assertNotIn('tools/ralph_convert.py', active)
                self.assertNotIn('tools/proof_record.py', active)
                self.assertNotRegex(active, r"\[['\"]proof['\"]\]\s*=")

    def test_assembly_validates_without_running_the_proof_recorder(self):
        spec = importlib.util.spec_from_file_location("tal_stage_under_test", ROOT / "tools" / "tal_stage.py")
        stage = importlib.util.module_from_spec(spec)
        fake_modules = {"workcfg": types.SimpleNamespace(),
                        "shastra_merge": types.SimpleNamespace(is_paratext=lambda _x: False)}
        with patch.dict(sys.modules, fake_modules):
            spec.loader.exec_module(stage)
        sample = [{"verse": 1}]
        fake_result = types.SimpleNamespace(returncode=0, stdout="valid", stderr="")
        with patch.object(stage, "stage_parse", return_value=sample), \
             patch.object(stage, "counts", return_value={"gloss": 1, "cm": 1, "am": 1}), \
             patch.object(stage, "stage_assemble") as assemble, \
             patch.object(stage.subprocess, "run", return_value=fake_result) as run, \
             patch.object(sys, "argv", ["tal_stage", "--work", "work", "--song", "song"]):
            self.assertEqual(stage.main(), 0)
            assemble.assert_called_once_with("work", "song")
            self.assertIn([sys.executable, "tools/validate_song.py", "--song", "song", "--work", "work"],
                          [call.args[0] for call in run.call_args_list])
            self.assertNotIn("tools/proof_record.py", [arg for call in run.call_args_list for arg in call.args[0]])
            fake_result.returncode = 1
            self.assertEqual(stage.main(), 1)
            self.assertEqual(sum(1 for call in run.call_args_list
                                 if "tools/validate_song.py" in call.args[0]), 2)

    def test_converter_only_validates_and_never_records_proof_or_pass(self):
        source = (ROOT / "tools" / "shastra_convert_chunk.py").read_text()
        self.assertNotIn("tools/proof_record.py", source)
        self.assertNotRegex(source, r"CONVERTED.*PASS")


class QueueMaintenanceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "tools").mkdir()
        for name in ("beam_swarm.py", "queue_guard.py", "recycle_failed.py", "assessor_sweep.py"):
            shutil.copy2(ROOT / "tools" / name, self.root / "tools" / name)
        (self.root / "process" / "beam").mkdir(parents=True)
        (self.root / "worka").mkdir()
        self.queue = self.root / "process" / "beam" / "queue.json"

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def task(task_id, status, verses, note=""):
        return {"id": task_id, "kind": "tal_triple", "status": status,
                "args": {"work": "worka", "song": "p01", "verses": verses},
                "attempts": 0, "max_attempts": 3, "note": note}

    def write_queue(self, tasks):
        self.queue.write_text(json.dumps(tasks))

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(self.root / "tools" / name), *args],
                              cwd=self.root, text=True, capture_output=True, timeout=10)

    def test_dry_recycle_does_not_write_queue(self):
        self.write_queue([self.task("failed", "failed", list(range(1, 25)), "question rejected")])
        before = self.queue.read_bytes()
        result = self.run_script("recycle_failed.py", "--dry")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2 halved tasks", result.stdout)
        self.assertEqual(self.queue.read_bytes(), before)

    def test_maintenance_fails_closed_if_queue_is_missing(self):
        for script, args in (("recycle_failed.py", ()), ("queue_guard.py", ("--fix",)),
                             ("assessor_sweep.py", ())):
            with self.subTest(script=script):
                result = self.run_script(script, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("queue does not exist", result.stderr)
                self.assertFalse(self.queue.exists())

    def test_recycle_does_not_overlap_an_existing_partial_window(self):
        self.write_queue([self.task("failed", "failed", list(range(1, 25)), "question rejected"),
                          self.task("active", "pending", list(range(4, 7)), "tail")])
        result = self.run_script("recycle_failed.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        retries = [t for t in json.loads(self.queue.read_text()) if t["id"].startswith("rc2-")]
        self.assertEqual([t["args"]["verses"] for t in retries], [list(range(13, 25))])

    def test_both_mutating_scripts_wait_for_worker_lock_and_preserve_new_tasks(self):
        for script, args, initial in (
            ("recycle_failed.py", (), [self.task("failed", "failed", list(range(1, 25)), "question rejected")]),
            ("queue_guard.py", ("--fix",), [self.task("first", "pending", list(range(1, 25))),
                                               self.task("overlap", "pending", list(range(13, 37)))]),
        ):
            with self.subTest(script=script):
                self.write_queue(initial)
                lock_path = Path(str(self.queue) + ".lock")
                with lock_path.open("a+") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    child = subprocess.Popen([sys.executable, str(self.root / "tools" / script), *args],
                                             cwd=self.root, text=True,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    try:
                        time.sleep(1)
                        self.assertIsNone(child.poll(), "maintenance did not wait for the worker lock")
                        concurrent = initial + [{"id": "concurrent", "kind": "lore_queries",
                                                  "status": "pending", "args": {}}]
                        replacement = self.queue.with_suffix(".replacement")
                        replacement.write_text(json.dumps(concurrent))
                        os.replace(replacement, self.queue)
                    finally:
                        fcntl.flock(lock, fcntl.LOCK_UN)
                    try:
                        stdout, stderr = child.communicate(timeout=10)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.communicate()
                        self.fail("maintenance did not complete after the lock was released")
                self.assertEqual(child.returncode, 0, stderr)
                current = json.loads(self.queue.read_text())
                self.assertIn("concurrent", [t["id"] for t in current], stdout)

    def test_init_queue_waits_for_worker_lock_and_preserves_concurrent_tasks(self):
        self.write_queue([{"id": "base", "kind": "lore_queries", "status": "pending", "args": {}}])
        lock_path = Path(str(self.queue) + ".lock")
        with lock_path.open("a+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            child = subprocess.Popen([sys.executable, str(self.root / "tools" / "beam_swarm.py"), "init-queue"],
                                     cwd=self.root, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                time.sleep(0.5)
                self.assertIsNone(child.poll(), "queue init did not wait for the worker lock")
                concurrent = [{"id": "base", "kind": "lore_queries", "status": "pending", "args": {}},
                              {"id": "concurrent", "kind": "lore_queries", "status": "pending", "args": {}}]
                replacement = self.queue.with_suffix(".replacement")
                replacement.write_text(json.dumps(concurrent))
                os.replace(replacement, self.queue)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
            stdout, stderr = child.communicate(timeout=10)
        self.assertEqual(child.returncode, 0, stderr)
        tasks = json.loads(self.queue.read_text())
        self.assertIn("concurrent", [t["id"] for t in tasks], stdout)
        self.assertIn("tal-a18-brief", [t["id"] for t in tasks])

    def test_assessor_sweep_waits_for_worker_lock_and_preserves_concurrent_tasks(self):
        initial = [{"id": "source", "kind": "tal_triple", "status": "pending",
                    "args": {"work": "tantraloka-a18", "song": "p01", "verses": [1]},
                    "attempts": 0, "max_attempts": 3, "note": ""}]
        self.write_queue(initial)
        (self.root / "process" / "beam" / "runs").mkdir()
        (self.root / "process" / "beam" / "lore").mkdir()
        lock_path = Path(str(self.queue) + ".lock")
        with lock_path.open("a+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            child = subprocess.Popen([sys.executable, str(self.root / "tools" / "assessor_sweep.py")],
                                     cwd=self.root, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                time.sleep(0.5)
                self.assertIsNone(child.poll(), "assessor sweep did not wait for the worker lock")
                concurrent = initial + [{"id": "concurrent", "kind": "lore_queries",
                                          "status": "pending", "args": {}}]
                replacement = self.queue.with_suffix(".replacement")
                replacement.write_text(json.dumps(concurrent))
                os.replace(replacement, self.queue)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
            stdout, stderr = child.communicate(timeout=10)
        self.assertEqual(child.returncode, 0, stderr)
        tasks = json.loads(self.queue.read_text())
        self.assertIn("concurrent", [t["id"] for t in tasks], stdout)
        self.assertIn("lore-q-18", [t["id"] for t in tasks])

    def test_watchdog_queue_mutations_use_shared_lock_and_preserve_concurrent_tasks(self):
        source = (ROOT / "tools" / "watchdog.sh").read_text()
        blocks = re.findall(r"python3 - <<'PY'[^\n]*\n(.*?)\nPY", source, re.S)
        self.assertGreaterEqual(len(blocks), 3)
        for script in (blocks[0], blocks[2]):  # stale-claim reap and stalled-worker reset
            with self.subTest(script=script[:40]):
                initial = [self.task("claimed", "claimed", [1])]
                self.write_queue(initial)
                lock_path = Path(str(self.queue) + ".lock")
                with lock_path.open("a+") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    child = subprocess.Popen([sys.executable, "-c", script], cwd=self.root,
                                             text=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    try:
                        time.sleep(0.5)
                        self.assertIsNone(child.poll(), "watchdog mutation bypassed the worker lock")
                        concurrent = initial + [{"id": "concurrent", "kind": "lore_queries",
                                                  "status": "pending", "args": {}}]
                        replacement = self.queue.with_suffix(".replacement")
                        replacement.write_text(json.dumps(concurrent))
                        os.replace(replacement, self.queue)
                    finally:
                        fcntl.flock(lock, fcntl.LOCK_UN)
                    stdout, stderr = child.communicate(timeout=10)
                self.assertEqual(child.returncode, 0, stderr)
                tasks = json.loads(self.queue.read_text())
                self.assertIn("concurrent", [t["id"] for t in tasks], stdout)
                self.assertEqual(tasks[0]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
