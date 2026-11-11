#!/usr/bin/env python3
"""spanda_t1_parse — T1-span-*.md ([gloss](surface) pada lines) -> working-t1 JSON.

Usage: python3 tools/spanda_t1_parse.py --song span-p04b
Reads <work>/T1-<song>.md, writes <work>/working-t1-<song>.json
[{verse_id, song, verse (KSTS int from header), quick_english:'',
quick_english_source:'t1parse', tokens:[{surface, quick_gloss}]}]
plus a coverage report vs passages.jsonl Sanskrit (every surface must occur).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="spanda")
    ap.add_argument("--song", required=True)
    a = ap.parse_args()
    w = ROOT / a.work
    text = (w / f"T1-{a.song}.md").read_text(encoding="utf-8")
    secs = re.findall(r"##\s+(\S+)-v(\d+)\s*\n(.*?)(?=\n##\s|\Z)", text, re.S)
    if not secs:
        print(f"no verse blocks in T1-{a.song}.md");
        return 1
    passages = [json.loads(l) for l in open(w / "passages.jsonl", encoding="utf-8")]
    src = next((p["sanskrit"] for p in passages if p["locator"] == a.song), "")
    src_nospace = re.sub(r"\s+", "", src)
    out, missing = [], []
    for header, vnum, body in secs:
        toks = re.findall(r"\[([^\]]*)\]\(([^)]+)\)", body)
        rows = [{"surface": s, "quick_gloss": g} for g, s in toks]
        for r in rows:
            if re.sub(r"\s+", "", r["surface"]).replace("+", "") not in src_nospace:
                missing.append((vnum, r["surface"]))
        out.append({"verse_id": f"{a.song}-v{vnum}", "song": a.song,
                    "verse": int(vnum), "quick_english": "",
                    "quick_english_source": "t1parse", "tokens": rows})
    (w / f"working-t1-{a.song}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    ntok = sum(len(e["tokens"]) for e in out)
    print(f"{a.song}: {len(out)} verses, {ntok} tokens -> working-t1-{a.song}.json")
    if missing:
        print(f"WARNING {len(missing)} surfaces not in passage Sanskrit:")
        for v, s in missing[:10]:
            print(f"  v{v}: {s}")
        return 2
    print("coverage: all surfaces occur in passage Sanskrit")
    return 0

if __name__ == "__main__":
    sys.exit(main())
