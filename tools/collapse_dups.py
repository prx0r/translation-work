#!/usr/bin/env python3
"""collapse_dups — remove ADJACENT IDENTICAL token repeats from a verse.

Some beam drafts emit the same surface several times in a row
(e.g. [A, A, A, B] for source [A, B]); dedup_t1 only handles suffix overlaps.
This collapses consecutive identical surfaces to one and keeps every layer
consistent:

  * T1 tokens: drop repeats (keep first)
  * L0: drop the entries at dropped positions, renumber pada_index (ids kept)
  * argmap.traces.l0_ids + l2.l0_ids: remove the dropped ids (they no longer exist)
  * working-t1: same collapse so re-staging cannot reintroduce the defect

Only runs where the L0 entry count equals the T1 token count (index-aligned);
otherwise it SKIPS and reports, never guesses.

Usage: python3 tools/collapse_dups.py <work> [song ...]
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def keep_indices(surfaces: list[str]) -> list[int]:
    """Keep the first of each run of identical adjacent surfaces."""
    return [i for i, s in enumerate(surfaces) if i == 0 or s != surfaces[i - 1]]


def collapse_tokens(tokens: list[dict]) -> tuple[list[dict], set[int]]:
    surfaces = [t.get("surface", "") for t in tokens]
    keep = keep_indices(surfaces)
    dropped = set(range(len(tokens))) - set(keep)
    return [tokens[i] for i in keep], dropped


def process(work: str, song: str) -> int:
    W = ROOT / work
    t1p = W / "data" / f"{song}.t1.json"
    l0p = W / "data" / f"{song}.l0.json"
    amp = W / "data" / f"{song}.argmap.json"
    l2p = W / "data" / f"{song}.l2.json"
    if not t1p.exists():
        return 0
    t1 = json.loads(t1p.read_text())
    l0 = json.loads(l0p.read_text()) if l0p.exists() else []
    am = json.loads(amp.read_text()) if amp.exists() else []
    l2 = json.loads(l2p.read_text()) if l2p.exists() else []

    l0_by_v: dict[str, list] = {}
    for o in l0:
        l0_by_v.setdefault(o["verse_id"], []).append(o)
    am_by_v = {o["verse_id"]: o for o in am}
    l2_by_v = {o["verse_id"]: o for o in l2}

    fixed = 0
    for e in t1:
        surf = [t.get("surface", "") for t in e["tokens"]]
        keep = keep_indices(surf)
        if len(keep) == len(surf):
            continue
        vid = e["verse_id"]
        le = l0_by_v.get(vid, [])
        if len(le) != len(surf):
            print(f"  SKIP {song} v{e['verse']}: L0 {len(le)} != T1 {len(surf)} (not index-aligned)")
            continue
        le_sorted = sorted(le, key=lambda o: o.get("pada_index", 0))
        dropped_pos = sorted(set(range(len(surf))) - set(keep))
        dropped_ids = {le_sorted[p]["id"] for p in dropped_pos}
        # T1
        e["tokens"] = [e["tokens"][i] for i in keep]
        # L0: keep + renumber pada_index
        for new_i, pos in enumerate(keep):
            le_sorted[pos]["pada_index"] = new_i
        kept_l0 = [le_sorted[p] for p in keep]
        l0_by_v[vid] = kept_l0
        # argmap / l2 id pruning
        a = am_by_v.get(vid)
        if a and isinstance(a.get("traces"), dict):
            a["traces"]["l0_ids"] = [x for x in a["traces"].get("l0_ids", []) if x not in dropped_ids]
        w2 = l2_by_v.get(vid)
        if w2:
            w2["l0_ids"] = [x for x in w2.get("l0_ids", []) if x not in dropped_ids]
        fixed += 1
        print(f"  {song} v{e['verse']}: {len(surf)} -> {len(keep)} tokens (dropped {sorted(dropped_pos)})")

    if not fixed:
        return 0
    new_l0 = [o for v in sorted(l0_by_v, key=lambda x: (l0_by_v[x][0].get("verse_id") if l0_by_v[x] else "", x)) for o in l0_by_v[v]]
    # preserve original verse order by first appearance in t1
    order = [e["verse_id"] for e in t1]
    new_l0 = [o for vid in order for o in l0_by_v.get(vid, [])]
    t1p.write_text(json.dumps(t1, indent=1, ensure_ascii=False))
    if l0p.exists():
        l0p.write_text(json.dumps(new_l0, indent=1, ensure_ascii=False))
    if amp.exists():
        amp.write_text(json.dumps(am, indent=1, ensure_ascii=False))
    if l2p.exists():
        l2p.write_text(json.dumps(l2, indent=1, ensure_ascii=False))
    # working-t1 (same collapse)
    wtp = W / f"working-t1-{song}.json"
    if wtp.exists():
        wt = json.loads(wtp.read_text())
        for e in wt:
            e["tokens"], _ = collapse_tokens(e.get("tokens", []))
        wtp.write_text(json.dumps(wt, indent=1, ensure_ascii=False))
    return fixed


def main() -> int:
    work = sys.argv[1]
    songs = sys.argv[2:] or sorted(
        p.name[: -len(".t1.json")] for p in (ROOT / work / "data").glob("*.t1.json"))
    total = 0
    for s in songs:
        n = process(work, s)
        if n:
            print(f"{s}: {n} verses collapsed")
            total += n
    print(f"TOTAL verses collapsed: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
