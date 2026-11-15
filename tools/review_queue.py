#!/usr/bin/env python3
"""review_queue — risk-prioritized HUMAN review queue for the Trika core.

Read-only. Ranks songs by how much a human should look at them, using
deterministic trust signals. **It never approves, never signs, never writes a
decision** — ranking is not judgment (AGENTS: machine proposes, humans dispose;
agreement is not evidence).

Signals (highest risk first):
  R0 REGRESSION        stored PASS, recompute BLOCKED (gold claim false)
  R1 MODE-HELD         stored mode != the mode it re-proves in (unresolved)
  R2 DISPOSITION       a recorded sub-0.90 exception stands in for judgment
  R3 ALIGN-LOW         stored min_ratio < 0.90 (even if dispositioned)
  R4 ALIGN-WATCH       stored min_ratio < 0.95
  R5 WARNINGS          metacommentary / C1 length / other proof warnings
  R6 BLOCKED           stored gate BLOCKED (needs repair, not review)
  R7 UNSERVED          passed mechanically but ChatGPT cannot read it yet
  R8 NO-SIGNOFF        every song is machine-proposed (baseline; ranks below)

Usage:
  python3 tools/review_queue.py                 # computes REGRESSION itself (slow)
  python3 tools/review_queue.py --core core.json # use a cached verify_core --out
  python3 tools/review_queue.py --limit 40 --json
Exit 0 always (a report, not a gate).
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISP = ROOT / "tools" / "proof-disp.json"
SVREAD = ROOT.parent / "svread" / "data" / "scholar"


def registry_works() -> list[str]:
    """Registry work names resolved through STATUS `alias_of` + deduped, so an
    alias row (ipvv-vivrti-vimarsini -> ipvv) contributes the canonical work's
    songs instead of none. Same resolution verify_core uses."""
    from workcfg import resolve_alias
    reg = json.loads((ROOT / "REGISTRY.json").read_text(encoding="utf-8"))
    out, seen = [], set()
    for w in reg["works"]:
        if not w.get("work"):
            continue
        resolved = resolve_alias(w["work"])
        if resolved not in seen:
            seen.add(resolved)
            out.append(resolved)
    return out


def load_core(path: str) -> dict:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    out = ROOT / "process" / "beam" / "verify_core.json"
    r = subprocess.run([sys.executable, "tools/verify_core.py", "--json", "--out", str(out)],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=3600)
    if out.exists():
        return json.loads(out.read_text(encoding="utf-8"))
    raise SystemExit(f"verify_core failed (rc={r.returncode}): {(r.stderr or r.stdout)[-400:]}")


def dispositions() -> dict:
    try:
        return json.loads(DISP.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def served_works() -> set[str]:
    out = set()
    if not SVREAD.is_dir():
        return out
    for f in SVREAD.glob("*.json"):
        if f.name == "index.json":
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if len(d.get("source_verses") or {}) > 0:
            out.add(d.get("work") or f.stem)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", default="", help="cached verify_core --out FILE")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    core = load_core(a.core)
    rows = core.get("rows", [])
    kind_by = {f"{r['work']}/{r['song']}": r for r in rows}
    disp = dispositions()
    served = served_works()
    works = registry_works()

    items = []
    for work in works:
        pdir = ROOT / work / "proof"
        if not pdir.is_dir():
            continue
        for f in sorted(pdir.glob("proof-*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                items.append({"work": work, "song": f.stem[6:], "risk": "R0",
                              "reason": "proof file unreadable", "score": 100})
                continue
            song = d.get("song") or f.stem[6:]
            key = f"{work}/{song}"
            fresh = kind_by.get(key, {})
            lin = (d.get("lineage") or {}).get("t1", "")
            mode = "shastra" if "/data/" in lin else "classic"
            gate = d.get("deterministic_gate")
            mr = (d.get("align") or {}).get("min_ratio", 1)
            warns = d.get("warnings") or []
            ndisp = len(disp.get(f"{work}:{song}", disp.get(song, {})) or {})
            if not isinstance(ndisp, int):
                ndisp = 0

            risk, score = None, 0
            if fresh.get("kind") == "REGRESSION":
                risk, score = "R0", 100
            elif fresh.get("kind") == "IMPROVED":
                risk, score = "R0", 99
            elif gate == "BLOCKED":
                risk, score = "R6", 40 + min(ndisp * 5, 20)
            elif ndisp:
                risk, score = "R2", 80 + ndisp
            elif mr is not None and mr < 0.90:
                risk, score = "R3", 70 + round((0.90 - mr) * 100)
            elif mr is not None and mr < 0.95:
                risk, score = "R4", 55 + round((0.95 - mr) * 100)
            elif warns:
                risk, score = "R5", 35 + len(warns) * 2
            elif work not in served:
                risk, score = "R7", 25
            else:
                risk, score = "R8", 5  # machine-proposed, no signoff (baseline)

            reason_bits = []
            if fresh.get("kind") in ("REGRESSION", "IMPROVED"):
                reason_bits.append(f"fresh={fresh.get('fresh')} stored={d.get('stored') or gate}")
                reason_bits += [str(b) for b in (fresh.get("blocking") or [])][:2]
            if gate:
                reason_bits.append(f"stored={gate}")
            if mr is not None:
                reason_bits.append(f"align={mr}")
            if ndisp:
                reason_bits.append(f"{ndisp} disposition(s)")
            if warns:
                reason_bits.append("warn: " + "; ".join(warns[:2]))
            if mode == "classic":
                reason_bits.append("classic mode")
            if work not in served:
                reason_bits.append("unserved")

            items.append({
                "risk": risk, "score": score, "work": work, "song": song,
                "mode": mode, "reason": "; ".join(reason_bits),
            })

    items.sort(key=lambda x: (-x["score"], x["work"], x["song"]))
    shown = items[: a.limit]
    counts = Counter(i["risk"] for i in items)

    if a.json:
        print(json.dumps({"total": len(items), "by_risk": dict(counts),
                          "items": shown}, indent=1, ensure_ascii=False))
        return 0

    print(f"HUMAN REVIEW QUEUE — {len(items)} songs across {len(works)} works")
    print("  (machine-proposed ranking only; nothing here is approved)")
    print("  by risk level:", dict(sorted(counts.items())))
    print()
    for i in shown:
        print(f"  {i['risk']} {i['score']:>4}  {i['work']}/{i['song']:<24} {i['reason'][:110]}")
    if len(items) > len(shown):
        print(f"  ... +{len(items) - len(shown)} more (use --limit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
