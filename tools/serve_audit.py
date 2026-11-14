#!/usr/bin/env python3
"""tools/serve_audit.py — is a work readable/provable via the ChatGPT MCP?

Read-only scorecard for the "prove + expose" pipeline. For every work with
canonical layer data (data/*.t1.json) — plus ipvv — report the six facts that
decide whether `scholar__passage_evidence` (mcp.svatantrya.net) can serve it:

  audited   a byte-pinned source audit exists (source/manifest.json, or a
            svatantrya-source-record/1 whose volume sha256 matches on-disk
            bytes — re-hashed here, never trusted)
  source    workcfg resolves a source file
  proj_src  scholar projection source_verses count (>0 == MCP can serve)
  traces    svread trace bundles for the work
  verify    svread verification packs
  claims    svread claim pages

`served` = proj_src > 0 (the actual MCP readability condition).

Usage: python3 tools/serve_audit.py [--work W] [--json]
Exit 0 always (a report, not a gate); summary line on stderr-free stdout.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVREAD = ROOT.parent / "svread"
sys.path.insert(0, str(ROOT / "tools"))
import emit_scholar  # noqa: E402  (_source_audited is the audit gate)


def _count(d: Path, pat: str) -> int:
    return sum(1 for _ in d.glob(pat)) if d.is_dir() else 0


def projection_source_verses(work: str) -> int:
    p = SVREAD / "data" / "scholar" / f"{work}.json"
    if not p.is_file():
        return -1  # no projection at all
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return -1
    return len(d.get("source_verses") or {})


def row(work: str) -> dict:
    audited = emit_scholar._source_audited(work)
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import workcfg
        cfg = workcfg.work_config(work)
        src = bool(cfg and cfg.get("source") and Path(cfg["source"]).is_file())
    except Exception:
        src = False
    ps = projection_source_verses(work)
    return {
        "work": work,
        "audited": audited,
        "source": src,
        "proj_src": ps,
        "traces": _count(SVREAD / "data" / "traces", f"{work}-*.json"),
        "verify": _count(SVREAD / "data" / "verify", f"{work}-*"),
        "claims": len([p for p in (SVREAD / "claim" / work).glob("*") if p.is_dir()])
        if (SVREAD / "claim" / work).is_dir() else 0,
        "served": ps > 0,
    }


def universe() -> list[str]:
    names = {p.parent.parent.name for p in ROOT.glob("*/data/*.t1.json")}
    if (ROOT / "ipvv" / "data").is_dir():
        names.add("ipvv")
    return sorted(names)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    works = [a.work] if a.work else universe()
    rows = [row(w) for w in works]
    served = [r for r in rows if r["served"]]
    audited = [r for r in rows if r["audited"]]
    no_proj = [r["work"] for r in rows if r["proj_src"] == -1]
    empty_proj = [r["work"] for r in rows if r["proj_src"] == 0]
    summary = {
        "works": len(rows),
        "served": len(served),
        "audited": len(audited),
        "unserved": len(rows) - len(served),
        "no_projection": len(no_proj),
        "empty_projection": len(empty_proj),
        "unserved_works": [r["work"] for r in rows if not r["served"]],
        "empty_projection_works": empty_proj,
        "no_projection_works": no_proj,
    }
    if a.json:
        print(json.dumps({"summary": summary, "rows": rows}, indent=1, ensure_ascii=False))
    else:
        print(f"served {len(served)}/{len(rows)} | audited {len(audited)} | "
              f"no-projection {len(no_proj)} | empty-projection {len(empty_proj)}")
        for r in rows:
            flag = "OK " if r["served"] else "-- "
            print(f"  {flag}{r['work']:<28} audited={int(r['audited'])} "
                  f"proj_src={r['proj_src']:<5} traces={r['traces']:<4} "
                  f"verify={r['verify']:<4} claims={r['claims']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
