#!/usr/bin/env python3
"""work_state — THE single source of truth for "has this work been worked?"

Rule (owner 2026-11-11): it must be IMPOSSIBLE to redo work. No derived
JSON may carry its own copy of work status. Everyone calls this.

Canonical inputs (read-only):
  <work>/STATUS.json   per-work ground truth (dir presence = started;
                       'machine-complete'/'minimal gold complete' in
                       `next` = machine-complete)
  process/beam/queue.json  task-level (per song/verse), NOT work-level —
                       never use it to decide work existence.

Usage:
  python3 tools/work_state.py --catalog M00048        # one work
  python3 tools/work_state.py --all | head            # census sweep
  from work_state import state_for_catalog            # importable
"""
from __future__ import annotations
import argparse
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CENSUS = Path("/tmp/mukta_census.json")

def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return "".join(ch for ch in s if ch.isalpha())

def _dirs() -> dict:
    """norm(dirname) -> (dirname, status_next) for every work dir."""
    out = {}
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir():
            continue
        st = d / "STATUS.json"
        nxt = ""
        if st.exists():
            try:
                nxt = (json.loads(st.read_text()).get("next") or "")
            except Exception:
                nxt = ""
        out[norm(d.name)] = (d.name, nxt)
    return out

_STATE_CACHE: dict | None = None

def states() -> dict:
    global _STATE_CACHE
    if _STATE_CACHE is None:
        _STATE_CACHE = _dirs()
    return _STATE_CACHE

_ALIASES = None

def _aliases() -> dict:
    global _ALIASES
    if _ALIASES is None:
        try:
            _ALIASES = json.loads(
                (ROOT / "process/beam/work_aliases.json").read_text())["catalogs"]
        except Exception:
            _ALIASES = {}
    return _ALIASES


def state_for_title(title: str, catalog: str = "") -> dict:
    """state for a muktabodha work. ALIAS REGISTRY FIRST (structural
    duplicate prevention): a catalog mapped there resolves to its canonical
    dir and can never be onboarded as new work."""
    a = _aliases().get(catalog)
    if a is not None:
        d = a.get("dir")
        if not d:
            return {"state": "not_started", "dir": None,
                    "alias_note": a.get("note", "")}
        nxt = states().get(norm(d), (d, ""))[1]
        low = nxt.lower()
        st = ("machine-complete" if ("machine-complete" in low
                                     or "minimal gold complete" in low)
              else "started")
        return {"state": st, "dir": d, "next": nxt[:90],
                "alias": True, "alias_note": a.get("note", "")}
    t = norm(title)
    dirs = states()
    hit = dirs.get(t)
    if not hit:
        # containment both ways, shortest dirname wins (conservative)
        cands = [v for k, v in dirs.items()
                 if len(k) > 6 and len(t) > 6 and (k in t or t in k)]
        if cands:
            hit = sorted(cands, key=lambda x: len(x[0]))[0]
    if not hit:
        return {"state": "not_started", "dir": None}
    dname, nxt = hit
    low = nxt.lower()
    if "machine-complete" in low or "minimal gold complete" in low:
        s = "machine-complete"
    elif low:
        s = "started"
    else:
        s = "started"  # dir exists, no status text
    return {"state": s, "dir": dname, "next": nxt[:90]}

def state_for_catalog(catalog: str) -> dict:
    if not CENSUS.exists():
        return {"state": "unknown", "error": "no census"}
    for r in json.load(open(CENSUS)):
        if r["catalog"] == catalog:
            return state_for_title(r["title"], catalog)
    return {"state": "unknown", "error": f"catalog {catalog} not in census"}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        for r in json.load(open(CENSUS)):
            s = state_for_title(r["title"], r["catalog"])
            print(f"{r['catalog']:8} {s['state']:17} {r['title'][:50]}")
        return 0
    if not a.catalog:
        ap.error("--catalog or --all")
    print(json.dumps(state_for_catalog(a.catalog), ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
