#!/usr/bin/env python3
"""mcp_smoke — verify the shastra MCP surface is actually callable.

Catches the class of bug where a tool is registered but its subprocess
command is wrong (bad path, stray '--') or returns a shape the caller
cannot read (bare list, rc=2 with empty body).

Two layers:
  1. STATIC — every name in mcp_server.TOOLS resolves to a callable tool.
  2. LIVE   — a curated set of SAFE, read-only calls must return a dict
              without an error payload. Never executes a write tool;
              recycle is forced dry-run, queue_guard runs read-only.

Usage: python3 tools/mcp_smoke.py [--quick]   (--quick = static + fast reads)
Exit 0 = all green. Never writes repo state.
"""
from __future__ import annotations
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mcp_server as M  # noqa: E402

# (tool_name, kwargs) — all MUST be safe/read-only.
FAST = [
    ("status", {"work": "tantraloka-a27", "song": "tal-a27"}),
    ("recon", {"work": "tantraloka-a27"}),
    ("lore", {"work": "mukta-m00125"}),
    ("skill", {"name": "proof"}),
    ("schema", {}),
    ("stats", {}),
    ("bibliography", {"catalog": "M00031"}),
    ("bibliography", {"q": "kularnava"}),
    ("priority", {"limit": 1}),
    ("works", {"limit": 1}),
    ("editions", {"catalog": "M00031"}),
    ("links", {"limit": 1}),
    ("availability", {"limit": 1}),
    ("swarm_status", {}),
    ("progress", {}),
    ("quota", {}),
    ("supervise", {}),
    ("swarm_workers", {"action": "status"}),
    ("queue_guard", {}),
    ("recycle", {"dry_run": True}),
    ("concepts", {"term": "śiva"}),
    ("burn_status", {}),
]

# Heavier but still read-only; skipped under --quick.
SLOW = [
    ("serve_status", {"work": "tantraloka-a27"}),
    ("verify_core", {"work": "tantraloka-a27"}),
    ("validate", {"work": "tantraloka-a27", "song": "tal-a27"}),
    ("audit_align", {"work": "tantraloka-a27"}),
]

BAD_MARKERS = ("can't open file", "Traceback", "[Errno 2]", "command not found")


def _bad(res: object) -> str | None:
    if not isinstance(res, dict):
        return f"non-dict return ({type(res).__name__})"
    blob = json.dumps(res, default=str)
    for m in BAD_MARKERS:
        if m in blob:
            return f"error text: {m}"
    if res.get("_rc") == 2 and set(res) <= {"_rc"}:
        return "rc=2 with empty payload"
    if "error" in res and res.get("error") and not res.get("_rc"):
        return f"error: {res['error']}"
    return None


def main() -> int:
    quick = "--quick" in sys.argv
    fails: list[str] = []

    registered = {n for n in M.TOOLS if callable(getattr(M, n, None))}
    missing = [n for n in M.TOOLS if n not in registered]
    if missing:
        fails.append(f"static: unregistered tools: {missing}")
    print(f"static: {len(registered)}/{len(M.TOOLS)} tools registered", flush=True)

    # BURN-MODE contract: the burn seeds T1+L0 only (tal_gloss/tal_cm), never a
    # triple. This is the invariant that keeps shallow argmap/L2 out of the
    # corpus (BEAM-FLOW §0.0). Pure in-memory check; writes nothing.
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import auto_burn
        q: list = []
        auto_burn.seed(q, "__smoke__", "__smoke-song__", [1, 2], "smoke")
        kinds = {t.get("kind") for t in q}
        if not kinds <= {"tal_gloss", "tal_cm"} or "tal_triple" in kinds:
            fails.append(f"burn-mode: seeded non-T1/L0 kinds {sorted(kinds)}")
        else:
            print(f"PASS burn-mode seeds {sorted(kinds)} only", flush=True)
    except Exception as e:  # noqa: BLE001
        fails.append(f"burn-mode: {type(e).__name__}: {e}")

    calls = FAST + ([] if quick else SLOW)
    passed = 0
    for name, kwargs in calls:
        fn = getattr(M, name, None)
        if not callable(fn):
            fails.append(f"{name}: not callable")
            continue
        try:
            res = fn(**kwargs)
            why = _bad(res)
        except Exception as e:  # noqa: BLE001
            why = f"raised {type(e).__name__}: {e}"
            traceback.print_exc()
        if why:
            fails.append(f"{name}{kwargs}: {why}")
            print(f"FAIL {name} {kwargs}: {why}", flush=True)
        else:
            passed += 1
            print(f"PASS {name}", flush=True)

    print(f"mcp-smoke: {passed}/{len(calls)} live calls green"
          + (f"; {len(fails)} failures" if fails else ""), flush=True)
    for f in fails:
        print("  - " + f, flush=True)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
