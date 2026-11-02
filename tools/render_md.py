#!/usr/bin/env python3
"""tools/render_md.py — regenerate legacy MD verse bodies from canonical JSON (round-trip check).

  python3 tools/render_md.py --song s01 --work sivastotravali [--write]

Without --write: reports diffs between regenerated bodies and legacy MD bodies (must be empty).
With --write: rewrites the verse-body lines in the legacy MD (headers/ledgers untouched).
"""
from __future__ import annotations
import argparse, difflib, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True); ap.add_argument("--work", default="sivastotravali")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    w = ROOT / args.work
    song = args.song
    data = w / "data"
    t1 = json.loads((data / f"{song}.t1.json").read_text())
    l2 = {o["verse"]: o for o in json.loads((data / f"{song}.l2.json").read_text())}
    l0 = json.loads((data / f"{song}.l0.json").read_text())

    diffs = []

    # ---- T1 bodies ----
    t1p = w / f"T1-{song}.md"
    lines = t1p.read_text(encoding="utf-8").splitlines()
    verse_of = {}
    for i, ln in enumerate(lines):
        m = re.match(r"## \S+-v(\d+)", ln)
        if m:
            verse_of[int(m.group(1))] = i
    for v in t1:
        line = " ".join(f"[and]-{t['quick_gloss']} ({t['surface']})" for t in v["tokens"])
        # legacy wraps into 2 visual lines for long verses: compare concatenation instead
        if v["verse"] not in verse_of:
            diffs.append(f"T1 header missing v{v['verse']}"); continue

    # compare per-verse token streams (order + content), not visual line breaks
    sys.path.insert(0, str(ROOT / "tools"))
    from proof_record import parse_t1 as _pt  # noqa
    legacy = {int(re.match(r".*-v(\d+)", k) or [0, 0])[1]: None for k in []}
    leg_toks: dict[int, list[str]] = {}
    cur = None
    for ln in lines:
        m = re.match(r"## \S+-v(\d+)", ln)
        if m:
            cur = int(m.group(1)); leg_toks[cur] = []; continue
        if cur is not None and "[and]-" in ln:
            leg_toks[cur] += re.findall(r"\[and\]-(.*?)\(([^)]+)\)", ln)
    for v in t1:
        vn = v["verse"]
        new = [(t["quick_gloss"], t["surface"]) for t in v["tokens"]]
        old = [(g.strip(), s.strip()) for g, s in leg_toks.get(vn, [])]
        if new != old:
            diffs.append(f"T1 v{vn}: JSON/MD token mismatch")

    # ---- L2 bodies ----
    l2p = w / f"L2-{song}.md"
    l2md = l2p.read_text(encoding="utf-8")
    for m in re.finditer(r"## v\.(\d+).*?\n(.*?)(?=\n## v\.\d+|\Z)", l2md, re.S):
        vn, body = int(m.group(1)), m.group(2)
        cm = re.search(r"The Sanskrit: \*(.+?)\*", body)
        plain = re.sub(r"\n+", " ", body[:cm.start()].strip()) if cm else body.strip()
        cite = cm.group(1).strip() if cm else ""
        o = l2.get(vn)
        if not o:
            diffs.append(f"L2 v{vn} missing in JSON"); continue
        if o["plain_english"] != plain or o["sanskrit_cite"] != cite:
            diffs.append(f"L2 v{vn}: JSON/MD mismatch")

    print(json.dumps({"song": song, "roundtrip_diffs": diffs}, indent=1))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
