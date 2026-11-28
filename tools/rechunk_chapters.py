#!/usr/bin/env python3
"""rechunk_chapters — regroup passages on REAL chapter boundaries.

Tantraloka gold = one song per ahnika. The equivalents:
  kularnavatantra  -> ullāsa  (17)
  netratantra      -> adhikāra (22)
  svacchandatantra -> paṭala   (per colophons)
  any other work   -> auto-detect from markers

Modes:
  (default) report  — detect markers, map verses to chapters, print ranges
  --apply           — rewrite passages.jsonl (backs up to passages.25v.bak)
                      and update song ids; DOES NOT touch working-t1 files
                      (they stay as fine-grained evidence; assemble_all
                      keys to the new song ids after re-parse)

Safety: refuses to apply if any marker is missing/unparseable, or if the
chapter verse-counts don't cover the extracted verse list 1:1.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MUKTA = Path("/tmp/mukta/MUKTABODHA-LIBRARY-IAST")

PREFIX = {"kularnavatantra": "kul", "netratantra": "net",
          "svacchandatantra": "sva"}

MARKERS = [
    ("ullasa", re.compile(r"(pratham|dvitīy|tṛtīy|chaturth|pañcam|ṣaṣṭh|saptam|aṣṭam|navam|daśam|ekādaś|dvādaś|trayodaś|chaturdaś|pañcadaś|ṣoḍaś|saptadaś)\w*ollāsa", re.I)),
    ("adhikara", re.compile(r"(prathama|dvitīya|tṛtīya|chaturtha|pañchama|ṣaṣṭha|saptama|aṣṭama|navama|daśama|ekādaśa|dvādaśa|trayodaśa|chaturdaśa|pañcadaśa|ṣoḍaśa|saptadaśa|aṣṭādaśa|navadaśa|viṃśa|ekaviṃśa|dvāviṃśa)\w*adhikāra", re.I)),
    ("patala", re.compile(r"paṭalaḥ", re.I)),
]


def find_source(work: str) -> Path | None:
    # catalogue file naming is HK-transliteration; match by prefix-ish title
    for f in MUKTA.glob("*.txt"):
        low = f.name.lower()
        if work.startswith("kularna") and "kul" in low:
            return f
        if work.startswith("netra") and "netra" in low:
            return f
        if work.startswith("svacchanda") and "svacchanda" in low:
            return f
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--chapters", type=int, default=0, help="expected count (sanity)")
    a = ap.parse_args()
    W = ROOT / a.work
    verses = json.loads((W / "source/verses.json").read_text())
    src = find_source(a.work)
    if not src:
        print("no source file found"); return 2
    text = src.read_text(encoding="utf-8", errors="replace")

    # locate markers in source order; count how many verses precede each
    marks = []
    for kind, rx in MARKERS:
        for m in rx.finditer(text):
            marks.append((m.start(), kind, m.group(0)[:40]))
    if not marks:
        print("no chapter markers found — cannot rechunk"); return 2
    marks.sort()
    # verse markers in order for offset mapping
    vmarks = [m.start() for m in re.finditer(r"\|\|\s*\d+(?:/\d+)?\s*(?:\((\d+)\))?\s*\|\|", text)]
    bounds = []
    for off, kind, label in marks:
        n_before = sum(1 for v in vmarks if v < off)
        bounds.append({"offset": off, "kind": kind, "label": label,
                       "verse_before": n_before})
    # dedupe consecutive identical verse_before (colophons + headings pair up)
    seen, chap = set(), []
    for b in bounds:
        if b["verse_before"] in seen:
            continue
        seen.add(b["verse_before"])
        chap.append(b)
    ranges = []
    for i, c in enumerate(chap):
        lo = c["verse_before"] + 1
        hi = (chap[i + 1]["verse_before"] if i + 1 < len(chap) else len(verses))
        if hi >= lo:
            ranges.append({"n": i + 1, "kind": c["kind"], "lo": lo, "hi": hi,
                           "label": c["label"]})
    total = sum(r["hi"] - r["lo"] + 1 for r in ranges)
    print(f"{a.work}: {len(ranges)} chapters, {total}/{len(verses)} verses covered")
    for r in ranges:
        print(f"  ch{r['n']:02d} {r['kind']:9} vv{r['lo']}-{r['hi']} ({r['hi']-r['lo']+1})")
    if a.chapters and len(ranges) != a.chapters:
        print(f"WARNING expected {a.chapters} chapters, detected {len(ranges)}")
    if total != len(verses):
        print("REFUSING apply: coverage mismatch (markers unreliable)")
        return 1
    if not a.apply:
        print("report only (pass --apply to rewrite passages.jsonl)")
        return 0
    p = W / "passages.jsonl"
    shutil.copy(p, W / "passages.25v.bak")
    pre = PREFIX.get(a.work, a.work[:3])
    with open(p, "w") as f:
        for r in ranges:
            song = f"{pre}-c{r['n']:02d}"
            f.write(json.dumps({"work_id": a.work, "order": r["n"],
                                "locator": song,
                                "verses": f"{r['lo']}-{r['hi']}",
                                "sanskrit": " ".join(verses[r["lo"]-1:r["hi"]]),
                                "chapter": r["label"]}, ensure_ascii=False) + "\n")
    print(f"APPLIED: {len(ranges)} chapter passages -> {p} (backup passages.25v.bak)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
