#!/usr/bin/env python3
"""finalcheck_audit — machine census over all works (read-only, fast).

Per work reports: data songs found, per-layer row counts, proof gates,
STATUS/REGISTRY presence, lore brief, working-t1 presence, anomalies.
Skips full validate_song (gates cover that); checks structure + records.
Usage: python3 tools/finalcheck_audit.py [--work NAME]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYERS = ("t1", "l0", "argmap", "l2", "c1", "l3", "l4")


def audit_work(work: str) -> dict:
    out = {"work": work, "issues": [], "songs": {}}
    wdir = ROOT / work
    if not wdir.is_dir():
        return {"work": work, "issues": ["NO-DIR"], "songs": {}}
    dd = wdir / "data"
    songs: dict[str, dict] = {}
    if dd.is_dir():
        for f in sorted(dd.glob("*.json")):
            parts = f.stem.split(".")
            if len(parts) == 2 and parts[1] in LAYERS:
                songs.setdefault(parts[0], {})[parts[1]] = f
    for song, files in sorted(songs.items()):
        sc: dict = {"layers": {}}
        for layer, f in files.items():
            try:
                d = json.loads(f.read_text())
                sc["layers"][layer] = len(d) if isinstance(d, list) else 1
            except ValueError:
                sc["layers"][layer] = "UNPARSEABLE"
                out["issues"].append(f"{song}.{layer} unparseable JSON")
        # proof
        proof = None
        for cand in (wdir / "proof" / f"proof-{song}.json",):
            if cand.exists():
                try:
                    p = json.loads(cand.read_text())
                    proof = p.get("gate", p.get("deterministic_gate", "?"))
                    if proof not in ("PASS",):
                        out["issues"].append(f"{song} proof gate={proof}")
                except ValueError:
                    proof = "UNPARSEABLE"
                    out["issues"].append(f"{song} proof unparseable")
        if proof is None:
            out["issues"].append(f"{song} MISSING proof file")
        sc["proof"] = proof
        # minimal-gold completeness
        for need in ("t1", "l0", "argmap", "l2", "c1"):
            if need not in files:
                out["issues"].append(f"{song} MISSING data.{need}")
        out["songs"][song] = sc
    if not songs:
        out["issues"].append("NO data/*.json songs")
    # STATUS
    sp = wdir / "STATUS.json"
    if sp.exists():
        try:
            st = json.loads(sp.read_text())
            for k in ("work", "next", "counts", "updated"):
                if k not in st:
                    out["issues"].append(f"STATUS missing key {k}")
            if not isinstance(st.get("counts", {}), dict) or "proof" not in st.get("counts", {}):
                out["issues"].append("STATUS counts.proof missing")
        except ValueError:
            out["issues"].append("STATUS unparseable")
    else:
        out["issues"].append("NO STATUS.json")
    # REGISTRY
    try:
        reg = json.loads((ROOT / "REGISTRY.json").read_text())
        row = next((w for w in reg["works"] if w["work"] == work), None)
        if row is None:
            out["issues"].append("NOT IN REGISTRY")
        elif not row.get("gold"):
            out["issues"].append(f"registry not-gold ({row.get('status')})")
    except ValueError:
        out["issues"].append("REGISTRY unreadable")
    # lore
    lore = list((ROOT / "process" / "beam" / "lore").glob(f"{work}.md"))
    tal = work.startswith("tantraloka-a")
    tbrief = (ROOT / "process" / "beam" / "lore" / f"tal-{work.split('tantraloka-a')[-1]}.md") if tal else None
    if not lore and not (tbrief and tbrief.exists()):
        out["issues"].append("NO lore brief (work-level or tal-)")
    # working-t1
    if not list(wdir.glob("working-t1-*.json")):
        out["issues"].append("NO working-t1 files")
    return out


def main() -> int:
    only = sys.argv[sys.argv.index("--work") + 1] if "--work" in sys.argv else None
    reg = json.loads((ROOT / "REGISTRY.json").read_text())
    names = [w["work"] for w in reg["works"] if (only is None or w["work"] == only)]
    # also audit dirs not in registry
    have = {w["work"] for w in reg["works"]}
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and (d / "data").is_dir() and d.name not in have and not d.name.startswith((".", "process", "tools", "skills", "lore", "test")):
            names.append(d.name)
    fails = warns = 0
    for name in names:
        try:
            r = audit_work(name)
        except Exception as e:  # noqa: BLE001 — audit must not die on one work
            print(f"{name}: AUDIT-ERROR {e}")
            fails += 1
            continue
        n = len(r["songs"])
        if not r["issues"]:
            print(f"OK   {name} ({n} songs)")
        else:
            warns += 1
            print(f"FLAG {name} ({n} songs): " + " | ".join(r["issues"][:6]))
    print(f"\nworks={len(names)} clean/_flagged: {len(names)-warns}/{warns} (audit-errors={fails})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
