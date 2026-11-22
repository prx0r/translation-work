#!/usr/bin/env python3
"""gen_chunk_song_map.py — derive chunk<->song maps for gate_reconcile.

gate_reconcile needs <work>/chunk-song-map.json. Only ipvv had one committed;
every other work was left without, which is why their GATE.json could not be
reconciled from proof records. This builds the map deterministically:

  * identity       — proof-<chunk>.json exists (chunk is its own song)
  * single song    — the work has exactly one proof song; map every chunk to it
  * suffix match   — the work has several songs; map a chunk to the unique
                     proof song sharing its final '-pNN' token (e.g. the
                     sivasutra 'sivs-p01' chunks back the 'span-p01' proofs)

An ambiguous chunk is left unmapped and reported; gate_reconcile preserves any
GATE entry not in the map, so an incomplete map is safe. Never guesses.

  python3 tools/gen_chunk_song_map.py --work tantraloka-a01
  python3 tools/gen_chunk_song_map.py --all
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build(workdir: Path) -> tuple[dict, list[str]]:
    gate_path = workdir / "GATE.json"
    if not gate_path.exists():
        return {}, []
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    proofs = {}
    for pr in glob.glob(str(workdir / "proof" / "proof-*.json")):
        try:
            d = json.loads(Path(pr).read_text(encoding="utf-8"))
        except ValueError:
            continue
        if d.get("song"):
            proofs[d["song"]] = Path(pr).name
    proof_files = set(proofs.values())
    songs = sorted(proofs)
    mapping, unmapped = {}, []
    for cid, entry in gate.items():
        if not isinstance(entry, dict):
            continue
        if f"proof-{cid}.json" in proof_files:
            mapping[cid] = cid
        elif len(songs) == 1:
            mapping[cid] = songs[0]
        else:
            tail = cid.split("-")[-1]
            cands = [s for s in songs if s == tail or s.endswith("-" + tail)]
            if len(cands) == 1:
                mapping[cid] = cands[0]
            else:
                unmapped.append(cid)
    return mapping, unmapped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if not a.work and not a.all:
        print("gen_chunk_song_map: pass --work or --all", file=sys.stderr)
        return 2
    if a.all:
        works = sorted(p.parent for p in (ROOT).glob("*/GATE.json"))
    else:
        works = [ROOT / a.work]
    rc = 0
    for w in works:
        mp = w / "chunk-song-map.json"
        if mp.exists():
            continue
        mapping, unmapped = build(w)
        if not mapping:
            continue
        mp.write_text(json.dumps(mapping, indent=1, sort_keys=True) + "\n",
                      encoding="utf-8")
        msg = f"{w.name}: {len(mapping)} mapped"
        if unmapped:
            msg += f", {len(unmapped)} unmapped {unmapped[:4]}"
            rc = 1
        print(msg)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
