#!/usr/bin/env python3
"""review_inbox — the assessor's per-verse review console (no beam calls).

Reads only process/beam/runs/* and working-t1. Lets the assessor drive quality
by hand while beam drafts in the background.

Usage:
  python3 tools/review_inbox.py coverage tantraloka-a13
  python3 tools/review_inbox.py verse tantraloka-a13 58
  python3 tools/review_inbox.py next  tantraloka-a13        # first verse missing a layer
  python3 tools/review_inbox.py newest                     # newest done drafts across fronts
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "process" / "beam" / "runs"
Q = ROOT / "process" / "beam" / "queue.json"


def song_of(work: str) -> str:
    return work.replace("tantraloka-", "tal-")


def load_wt(work: str, song: str):
    p = ROOT / work / f"working-t1-{song}.json"
    return json.loads(p.read_text()) if p.exists() else []


def has(song: str, layer: str, v: int) -> bool:
    return (RUNS / f"{song}-{layer}-v{v:02d}" / f"{layer}.json").exists()


def coverage(work: str) -> None:
    song = song_of(work)
    wt = load_wt(work, song)
    vs = [e["verse"] for e in wt]
    if not vs:
        print(f"{work}: no working-t1-{song}.json"); return
    rows = []
    for layer in ("gloss", "cm", "am"):
        have = [v for v in vs if has(song, layer, v)]
        miss = [v for v in vs if v not in have]
        rows.append((layer, len(have), len(vs), miss[:12]))
    print(f"{work}  ({song})  {len(vs)} units: {vs[0]}..{vs[-1]}")
    for layer, n, tot, miss in rows:
        print(f"  {layer:5} {n:4}/{tot}")
        if miss:
            print(f"        missing: {miss}{' …' if n and (tot-n) > len(miss) else ''}")
    # task status for this song
    if Q.exists():
        import collections
        tasks = [t for t in json.loads(Q.read_text())
                 if t.get("args", {}).get("song") == song]
        c = collections.Counter((t["kind"], t["status"]) for t in tasks)
        print("  tasks:", dict(c))


def verse(work: str, v: int) -> None:
    song = song_of(work)
    wt = load_wt(work, song)
    entry = next((e for e in wt if e["verse"] == v), None)
    if not entry:
        print(f"no verse {v}"); return
    print(f"\n=== {song} v{v} — SOURCE ({len(entry['tokens'])} tokens) ===")
    print(" ".join(t["surface"] for t in entry["tokens"]))
    for layer in ("gloss", "cm", "am"):
        f = RUNS / f"{song}-{layer}-v{v:02d}" / f"{layer}.json"
        print(f"\n--- {layer} ---")
        if not f.exists():
            print("  (missing)"); continue
        d = json.loads(f.read_text())
        if layer == "gloss":
            for r in d["rows"]:
                print(f"  {r['surface']:32} {r['gloss']:34} | {r.get('grounds','')[:60]}")
        elif layer == "cm":
            for r in d["rows"]:
                print(f"  {r['lemma']:32} {r['morph']}")
        else:
            print("  Q:", d.get("question"))
            for p in d.get("premises", []):
                print("  -", p)
            print("  inference:", d.get("inference"))
            print("  uncertainties:", d.get("uncertainties"))
            print("  L2:", d.get("plain_english"))


def next_missing(work: str) -> None:
    song = song_of(work)
    wt = load_wt(work, song)
    for e in wt:
        v = e["verse"]
        miss = [l for l in ("gloss", "cm", "am") if not has(song, l, v)]
        if miss:
            print(f"next: {work} v{v} missing {miss}")
            verse(work, v)
            return
    print(f"{work}: all verses have gloss+cm+am")


def newest() -> None:
    files = sorted(RUNS.glob("*-am-v*/am.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files[:15]:
        d = json.loads(f.read_text())
        print(f"{f.parent.name:24} {d.get('question','')[:70]}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__); return 1
    cmd = sys.argv[1]
    if cmd == "coverage":
        coverage(sys.argv[2])
    elif cmd == "verse":
        verse(sys.argv[2], int(sys.argv[3]))
    elif cmd == "next":
        next_missing(sys.argv[2])
    elif cmd == "newest":
        newest()
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
