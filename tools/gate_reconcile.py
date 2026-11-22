#!/usr/bin/env python3
"""tools/gate_reconcile.py — re-derive per-chunk GATE.json entries from proof records.

A GATE chunk entry goes stale the moment its proof record exists: the old
entry says "proof/ not generated yet" while proof/proof-<song>.json already
says PASS. This tool closes that gap deterministically. It never invents a
gate: for every chunk it re-hashes the exact layer bytes the proof record
pins (canonical JSON, same as proof_record.py) and resolves the chunk id
through chunk-song-map.json. A chunk becomes PASS only if its proof record
is complete (deterministic_gate + blocking + warnings + tool), says PASS
with empty blocking, and every pinned layer byte-matches today.

  python3 tools/gate_reconcile.py --work ipvv --check   # report drift only
  python3 tools/gate_reconcile.py --work ipvv --write   # rewrite GATE.json

Exit 0 = written/matching. Exit 1 = drift under --check. Exit 2 = unreadable inputs.
Stdlib only. Refuses to run without chunk-song-map.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PROOF_KEYS = ("deterministic_gate", "blocking", "warnings", "tool")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon_sha(value) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                ensure_ascii=False).encode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()

    workdir = ROOT / a.work
    gate_path = workdir / "GATE.json"
    map_path = workdir / "chunk-song-map.json"
    try:
        gate = json.loads(gate_path.read_text(encoding="utf-8"))
        cmap = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"gate_reconcile: unreadable input: {e}", file=sys.stderr)
        return 2
    if not isinstance(cmap, dict) or not cmap:
        print("gate_reconcile: chunk-song-map.json missing or empty; "
              "refusing to guess chunk<->song", file=sys.stderr)
        return 2

    new_gate: dict = {}
    for chunk_id, song in cmap.items():
        problems: list[str] = []
        pf = workdir / "proof" / f"proof-{song}.json"
        try:
            pj = json.loads(pf.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pj = None
        if pj is None:
            problems.append("PROOF_MISSING")
        else:
            missing = [k for k in REQUIRED_PROOF_KEYS if k not in pj]
            if missing:
                problems.append("PROOF_FIELDS_INCOMPLETE:" + ",".join(missing))
            elif pj.get("deterministic_gate") != "PASS" or pj.get("blocking"):
                problems.append("PROOF_NOT_PASS")
            else:
                pinned = pj.get("layer_sha256") or {}
                if not isinstance(pinned, dict) or not pinned:
                    problems.append("PROOF_LAYERS_UNPINNED")
                else:
                    lineage = pj.get("lineage") or {}
                    for layer, want in pinned.items():
                        cands = [
                            workdir / "data" / f"{song}.{layer}.json",
                            workdir / chunk_id / "data" / f"{song}.{layer}.json",
                        ]
                        if isinstance(lineage.get(layer), str):
                            cands.append(workdir / lineage[layer])
                            cands.append(ROOT / lineage[layer])
                        val = None
                        for p in cands:
                            if not p.is_file():
                                continue
                            try:
                                val = json.loads(p.read_text(encoding="utf-8"))
                                break
                            except ValueError:
                                continue
                        if val is None:
                            problems.append(f"LAYER_MISSING:{layer}")
                            continue
                        if canon_sha(val) != want:
                            problems.append(f"LAYER_DRIFT:{layer}")
        if problems:
            new_gate[chunk_id] = {
                "deterministic_gate": "BLOCKED",
                "blocking": sorted(set(problems)),
                "checks": {"PROOF_RECORD": [False, "; ".join(sorted(set(problems)))]},
            }
        else:
            new_gate[chunk_id] = {
                "deterministic_gate": "PASS",
                "blocking": [],
                "checks": {"PROOF_RECORD": [True,
                    f"proof-{song}.json {pj['tool']}, layers re-hashed "
                    f"{len(pj['layer_sha256'])}/{len(pj['layer_sha256'])}"]},
            }
    # preserve any non-chunk top-level keys untouched (none today, but closed world)
    for k, v in gate.items():
        if k not in new_gate:
            new_gate[k] = v
    text = json.dumps(new_gate, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    current = gate_path.read_text(encoding="utf-8")
    if a.check:
        if current != text:
            old_pass = sum(1 for v in gate.values() if isinstance(v, dict) and v.get("deterministic_gate") == "PASS")
            new_pass = sum(1 for v in new_gate.values() if isinstance(v, dict) and v.get("deterministic_gate") == "PASS")
            print(f"gate_reconcile --check: DRIFT ({old_pass} PASS -> {new_pass} PASS)")
            return 1
        print(f"gate_reconcile --check: GREEN ({len(new_gate)} chunks reconciled)")
        return 0
    gate_path.write_text(text, encoding="utf-8")
    n_pass = sum(1 for v in new_gate.values() if isinstance(v, dict) and v.get("deterministic_gate") == "PASS")
    print(f"gate_reconcile: wrote {gate_path} ({n_pass}/{len(new_gate)} PASS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
