#!/usr/bin/env python3
"""tools/make_traces.py — batch trika-x trace_bundle per passage (the trace fan-out).

Deterministic, NO beam. trace_bundle compiles one trika-trace/1 bundle per
chunk from: translation-work ledgers/layers/proofs/STATUS, the openpatala box
DB, trika-x EVIDENCE + runs ledger. This driver batches it across a whole work
(or every work with a passage ledger) and re-verifies each bundle.

  python3 tools/make_traces.py --work mukta-m00027
  python3 tools/make_traces.py --served-untraced     # every served work with 0 traces
  python3 tools/make_traces.py --all                 # every work with a ledger
  python3 tools/make_traces.py --work ipvv --rebuild  # force rebuild

Idempotent: bundles that already exist AND pass --verify are skipped unless
--rebuild. Fails closed: compile and verify are both required; nothing is
written past a failing case. Per-bundle timeout 180s via trace_bundle's own
verify. serve_audit/serve_status measures the result; make_readable --publish
carries verified bundles into verify packs + claim pages.

Exit 0 with a summary even when some bundles fail (they are listed, not
hidden); exit 2 on bad usage.
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIKA = Path(os.environ.get("TRIKA_X_ROOT", str(ROOT.parent / "trika-x")))
TOOL = TRIKA / "formal-trika" / "tools" / "trace_bundle.py"
OUTDIR = TRIKA / "formal-trika" / "data" / "traces"
sys.path.insert(0, str(ROOT / "tools"))
import serve_audit as sa  # noqa: E402


def locators(work: str) -> list[str]:
    p = ROOT / work / "passages.jsonl"
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        try:
            out.append(json.loads(ln)["locator"])
        except (ValueError, KeyError):
            pass
    return out


def verify(path: Path) -> bool:
    r = subprocess.run([sys.executable, str(TOOL), "--verify", str(path)],
                       capture_output=True, text=True, timeout=180)
    return r.returncode == 0


def build(work: str, target: str) -> tuple[bool, str]:
    """Compile one bundle; return (verified_ok, note)."""
    out = OUTDIR / f"{work}-{target}.json"
    r = subprocess.run([sys.executable, str(TOOL), "--work", work,
                        "--target", target, "--out", str(out)],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        tail = (r.stderr or r.stdout).strip().splitlines()
        return False, f"compile rc={r.returncode}: {(tail[-1] if tail else '')[:160]}"
    if not verify(out):
        return False, "verify-after-compile"
    return True, ""


def run_work(work: str, rebuild: bool = False) -> dict:
    tgts = locators(work)
    res = {"work": work, "passages": len(tgts), "ok": 0, "skipped": 0, "fail": []}
    if not tgts:
        res["fail"].append(("NO-LEDGER", "no passages.jsonl or no locators"))
        return res
    for t in tgts:
        out = OUTDIR / f"{work}-{t}.json"
        if out.is_file() and not rebuild and verify(out):
            res["skipped"] += 1
            continue
        ok, note = build(work, t)
        if ok:
            res["ok"] += 1
        else:
            res["fail"].append((t, note))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="")
    ap.add_argument("--served-untraced", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.work:
        works = [a.work]
    elif a.served_untraced:
        works = [r["work"] for r in (sa.row(w) for w in sa.universe())
                 if r["served"] and r["traces"] == 0]
    elif a.all:
        works = [w for w in sa.universe() if locators(w)]
    else:
        print("nothing to do: pass --work W, --served-untraced, or --all",
              file=sys.stderr)
        return 2

    if not TOOL.is_file() or not OUTDIR.is_dir():
        print(f"trika-x trace tooling not found under {TRIKA}", file=sys.stderr)
        return 2

    t0 = time.time()
    rows, batch_fail = [], 0
    for i, w in enumerate(works, 1):
        r = run_work(w, rebuild=a.rebuild)
        rows.append(r)
        if r["fail"]:
            batch_fail += 1
        print(f"[{i}/{len(works)}] {w}: ok={r['ok']} skip={r['skipped']} "
              f"fail={len(r['fail'])} ({time.time()-t0:.0f}s)", flush=True)

    summary = {"works": len(rows), "works_with_failures": batch_fail,
               "bundles_ok": sum(r["ok"] for r in rows),
               "bundles_skipped": sum(r["skipped"] for r in rows),
               "bundles_failed": sum(len(r["fail"]) for r in rows)}
    if a.json:
        print(json.dumps({"summary": summary, "rows": rows}, indent=1))
    else:
        fails = [(r["work"], t, n) for r in rows for (t, n) in r["fail"]][:30]
        print(f"DONE works={summary['works']} bundles_ok={summary['bundles_ok']} "
              f"skip={summary['bundles_skipped']} fail={summary['bundles_failed']}")
        for w, t, n in fails:
            print(f"  FAIL {w}:{t} | {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
