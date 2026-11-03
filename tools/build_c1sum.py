#!/usr/bin/env python3
"""tools/build_c1sum.py — compile the chat intro: a concise mini-essay of the
whole work, from argmaps (the text's opening question) + C1 (one essence
sentence per song, in order).

  python3 tools/build_c1sum.py            # all works -> svread/data/c1sum.json
  python3 tools/build_c1sum.py --work paramarthasara

The output is data, not prose-by-hand: same inputs -> same intro (SCHOLAR.md
§"emit"). Length: clamped at ~900 chars on a sentence boundary — reads as a
mini-essay in a chat bubble, not a paragraph wall.
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVREAD = Path("/root/svread/data")

def first_sentence(text) -> str:
    if isinstance(text, (list, tuple)):
        text = " ".join(str(x) for x in text)
    t = re.sub(r"\s+", " ", str(text or "").replace("*", "")).strip()
    if not t:
        return ""
    m = re.search(r"(?<=[.!?])\s", t)
    # no "…" here — lines get JOINED mid-essay; the final clamp owns the ellipsis
    s = t[:m.start() + 1] if m and m.start() > 40 else (t if len(t) <= 140 else t[:140].rstrip())
    return s.strip()

def clamp(s: str, n: int = 900) -> str:
    if len(s) <= n:
        return s
    cut = s[:n]
    dot = cut.rfind(". ")
    return (cut[:dot + 1] if dot > 300 else cut.rstrip() + "…")

def build(work: str) -> str:
    wdir = ROOT / work
    # songs in verse order (t1 files sorted = song order)
    songs = sorted(p.stem.split(".")[0] for p in (wdir / "data").glob("*.t1.json"))
    # 1. the opening question — first argmap row of the first song
    q = ""
    for song in songs:
        am = wdir / "data" / f"{song}.argmap.json"
        if am.exists():
            rows = json.loads(am.read_text(encoding="utf-8"))
            if rows and rows[0].get("question"):
                q = rows[0]["question"].strip()
                break
    # 2. one essence sentence per song, in order — the narrative spine
    parts = []
    for song in songs:
        cf = wdir / "data" / f"{song}.c1.json"
        if not cf.exists():
            continue
        c1 = json.loads(cf.read_text(encoding="utf-8"))
        s = first_sentence(c1.get("essence") or "")
        if s:
            parts.append(s)
    if not parts:
        return ""
    body = " ".join(parts)
    essay = (f"“{q}” — the question the text opens on. {body}" if q else body)
    return clamp(essay)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    SVREAD.mkdir(parents=True, exist_ok=True)
    out = {}
    dest = SVREAD / "c1sum.json"
    if dest.exists():
        out = json.loads(dest.read_text(encoding="utf-8"))
    works = [a.work] if a.work else sorted(p.parents[1].name for p in ROOT.glob("*/data/*.c1.json"))
    made = 0
    for w in works:
        if a.work is None and not (ROOT / w / "data").exists():
            continue
        try:
            essay = build(w)
        except Exception as e:
            print(f"{w}: ERROR {e}")
            continue
        if essay:
            out[w] = essay
            made += 1
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"c1sum: {made} works -> {dest} ({dest.stat().st_size // 1024} KB)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
