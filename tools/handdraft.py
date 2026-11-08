#!/usr/bin/env python3
"""handdraft — assessor hand-draft writer for runs/{gloss,cm,am}.json.

Usage (one verse):
  python3 tools/handdraft.py --work tantraloka-a28 --song tal-a28 --verse 36 \
    --gloss 'surface=gloss|grounds;...' \
    --cm 'lemma:morph:grounds;...' \
    --q '...' --premises 'p1 | p2 | p3' --inference '...' \
    --unc 'u1 | u2' --l2 '...'

Semicolons separate rows, | separates fields. Single quotes protect content.
Validates shapes (all rows non-empty, Q ends with ?, premises>=3 words)
but never judges meaning — that's the assessor's job.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "process" / "beam" / "runs"


def parse_rows(spec: str, keys: tuple) -> list:
    rows = []
    for chunk in spec.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = [p.strip() for p in chunk.split("|")]
        if len(parts) != len(keys):
            raise SystemExit(f"row needs {len(keys)} |-fields, got {len(parts)}: {chunk[:60]}")
        if any(not p for p in parts):
            raise SystemExit(f"empty field in row: {chunk[:60]}")
        rows.append(dict(zip(keys, parts)))
    if not rows:
        raise SystemExit("no rows parsed")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--song", required=True)
    ap.add_argument("--verse", required=True, type=int)
    ap.add_argument("--gloss", required=True)
    ap.add_argument("--cm", required=True)
    ap.add_argument("--q", required=True)
    ap.add_argument("--premises", required=True)
    ap.add_argument("--inference", required=True)
    ap.add_argument("--unc", required=True)
    ap.add_argument("--l2", required=True)
    a = ap.parse_args()

    wt = json.loads((ROOT / a.work / f"working-t1-{a.song}.json").read_text())
    entry = next(e for e in wt if e["verse"] == a.verse)
    surfs = [t["surface"] for t in entry["tokens"]]

    grows = parse_rows(a.gloss, ("surface", "gloss", "grounds"))
    if [r["surface"] for r in grows] != surfs:
        raise SystemExit(f"surface mismatch vs working-t1 for {a.song} v{a.verse}")
    crows = parse_rows(a.cm, ("lemma", "morph", "grounds"))
    if [r["lemma"] for r in crows] != surfs:
        raise SystemExit(f"lemma mismatch vs working-t1 for {a.song} v{a.verse}")

    prems = [p.strip() for p in a.premises.split("|") if p.strip()]
    if not a.q.strip().endswith("?"):
        raise SystemExit("question must end with ?")
    if any(len(p.split()) < 3 for p in prems):
        raise SystemExit("each premise needs >=3 words")
    if len(a.l2.split()) < 4:
        raise SystemExit("L2 needs >=4 words")
    unc = [u.strip() for u in a.unc.split("|") if u.strip()]
    if not unc:
        raise SystemExit("need >=1 uncertainty")

    (RUNS / f"{a.song}-gloss-v{a.verse:02d}").mkdir(parents=True, exist_ok=True)
    json.dump({"song": a.song, "verse": a.verse, "rows": grows},
              open(RUNS / f"{a.song}-gloss-v{a.verse:02d}" / "gloss.json", "w"),
              indent=1, ensure_ascii=False)
    (RUNS / f"{a.song}-cm-v{a.verse:02d}").mkdir(parents=True, exist_ok=True)
    json.dump({"song": a.song, "verse": a.verse, "rows": crows},
              open(RUNS / f"{a.song}-cm-v{a.verse:02d}" / "cm.json", "w"), indent=1, ensure_ascii=False)
    (RUNS / f"{a.song}-am-v{a.verse:02d}").mkdir(parents=True, exist_ok=True)
    json.dump({"song": a.song, "verse": a.verse, "question": a.q.strip(),
               "premises": prems, "inference": a.inference.strip(),
               "uncertainties": unc, "plain_english": a.l2.strip()},
              open(RUNS / f"{a.song}-am-v{a.verse:02d}" / "am.json", "w"), indent=1, ensure_ascii=False)
    print(f"wrote {a.song} v{a.verse}: {len(grows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
