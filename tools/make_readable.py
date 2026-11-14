#!/usr/bin/env python3
"""tools/make_readable.py — prove+expose button: audited source → served projection.

Deterministic, NO beam. For each target work it:
  1. checks the byte-pinned source audit (emit_scholar._source_audited);
     unaudited works are reported BLOCKED (never served unverified source);
  2. runs tools/emit_scholar.py --work W (writes svread/data/scholar/<W>.json,
     populating source_verses — the condition scholar__passage_evidence reads);
  3. reports proj_src (0 = no proof-complete/eligible songs yet; not an error).

--publish then runs the svread publish chain once at the end (traces → verify →
claim → discovery → release_manifest LAST). Traces themselves are produced by
trika-x trace_bundle (see make_traces) — this only re-emits what exists.

Usage:
  python3 tools/make_readable.py --work tantrasara-a13
  python3 tools/make_readable.py --all [--publish]
  python3 tools/make_readable.py --work kularnavatantra --json
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVREAD = ROOT.parent / "svread"
sys.path.insert(0, str(ROOT / "tools"))
import serve_audit as sa  # noqa: E402


def _emit(work: str, timeout: int = 900) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "tools/emit_scholar.py", "--work", work],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=timeout)
    ps = sa.projection_source_verses(work)
    if r.returncode != 0:
        return ps, (r.stderr or r.stdout).strip().splitlines()[-1][:160] if (r.stderr or r.stdout).strip() else f"rc={r.returncode}"
    return ps, ""


def publish() -> dict:
    """Run the svread publish chain (deterministic). release_manifest LAST."""
    steps = [["tools/emit_traces.py"], ["tools/emit_verify.py"],
             ["tools/emit_claim_pages.py"], ["tools/emit_discovery.py"],
             ["scripts/release_manifest.py", "--write"]]
    out = {}
    for cmd in steps:
        r = subprocess.run([sys.executable] + cmd, cwd=str(SVREAD),
                           capture_output=True, text=True, timeout=1800)
        out[cmd[0].split("/")[-1]] = r.returncode
        if r.returncode != 0:
            return {"ok": False, "failed": cmd[0], "stderr": (r.stderr or r.stdout)[-400:]}
    return {"ok": True, "steps": out}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    targets = [a.work] if a.work else (sa.universe() if a.all else [])
    if not targets:
        print("nothing to do: pass --work W or --all", file=sys.stderr)
        return 2

    rows, blocked = [], []
    for w in targets:
        if not sa.emit_scholar._source_audited(w):
            blocked.append(w)
            rows.append({"work": w, "audited": False, "proj_src": sa.projection_source_verses(w)})
            continue
        ps, err = _emit(w)
        rows.append({"work": w, "audited": True, "proj_src": ps, "error": err})

    served = sum(1 for r in rows if r.get("proj_src", -1) > 0)
    summary = {"targets": len(rows), "served": served,
               "blocked_unaudited": len(blocked),
               "empty_no_eligible_songs": sum(1 for r in rows if r.get("audited") and r.get("proj_src") == 0)}
    result = {"summary": summary, "blocked": blocked, "rows": rows}
    if a.publish:
        result["publish"] = publish()
    if a.json:
        print(json.dumps(result, indent=1, ensure_ascii=False))
    else:
        print(f"targets {summary['targets']} | served {served} | "
              f"blocked-unaudited {summary['blocked_unaudited']} | "
              f"empty(no eligible songs) {summary['empty_no_eligible_songs']}")
        for w in blocked:
            print(f"  BLOCKED(unaudited) {w}")
        if a.publish:
            print(f"publish: {result['publish']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
