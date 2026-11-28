#!/usr/bin/env python3
"""De-overlap beam T1 token runs (count-preserving).

Defect: drafters sometimes emit a whole compound AND its tail as separate rows
(e.g. 'ājñāsiddhirbhavettasya' / 'bhavettasya' / 'tasya'). Concatenation then
repeats source material and the align gate drops below 0.90.

Fix: left-to-right, when token[i-1].surface ENDS WITH token[i].surface (a
proper suffix, exact string), strip that suffix off token[i-1]. Token count is
unchanged, so L0 index invariants (L0.chosen == T1.quick_gloss by index) hold.

Usage: python3 tools/dedup_t1.py <work> [song ...]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fix_tokens(tokens):
    changed = []
    for i in range(1, len(tokens)):
        a = tokens[i - 1].get("surface", "")
        b = tokens[i].get("surface", "")
        if not a or not b or a == b:
            continue
        if a.endswith(b) and len(a) > len(b):
            new = a[: -len(b)]
            if new:
                tokens[i - 1]["surface"] = new
                changed.append((a, new, b))
    return changed


def main():
    work = sys.argv[1]
    songs = sys.argv[2:] or sorted(
        p.name[: -len(".t1.json")] for p in (ROOT / work / "data").glob("*.t1.json")
    )
    total = 0
    for song in songs:
        path = ROOT / work / "data" / f"{song}.t1.json"
        data = json.loads(path.read_text())
        song_changed = 0
        for o in data:
            ch = fix_tokens(o["tokens"])
            if ch:
                song_changed += 1
                o.setdefault("history", []).append(
                    {"gloss": o.get("quick_english", ""),
                     "reason": ("de-overlapped token run: stripped redundant suffix repeats "
                                "from compound surfaces (count-preserving, T1-only); "
                                f"{len(ch)} token(s); align gate repair 2026-11-13"),
                     "date": "2026-11-13"}
                )
        if song_changed:
            path.write_text(json.dumps(data, indent=1, ensure_ascii=False))
            print(f"{song}: {song_changed} verses fixed")
            total += song_changed
    print(f"TOTAL verses fixed: {total}")


if __name__ == "__main__":
    main()
