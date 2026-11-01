#!/usr/bin/env python3
"""tools/emit_data.py — backfill canonical JSON data objects from legacy MD (+ l0.jsonl). ONE-WAY.

  python3 tools/emit_data.py --song s01 --work sivastotravali

Writes data/<song>.t1.json, .l0.json, .argmap.json, .l2.json, .c1.json.
Mechanical derivations are marked (draft_mechanical / essence_source / trace_level).
After this runs once, JSON is canonical; MD is re-rendered by render_md.py, never hand-edited.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
sys.path.insert(0, str(ROOT / "tools"))
from proof_record import load_gretil_song  # noqa: E402


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def parse_t1(md: str) -> list[dict]:
    verses, cur = [], None
    for line in md.splitlines():
        m = re.match(r"## \S+-v(\d+)", line)
        if m:
            cur = {"verse": int(m.group(1)), "tokens": []}; verses.append(cur); continue
        if cur is not None and "[and]-" in line:
            for mm in re.finditer(r"\[and\]-(.*?)\(([^)]+)\)", line):
                cur["tokens"].append({"gloss": mm.group(1).strip(), "iast": mm.group(2).strip()})
    return verses


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True); ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()
    w = ROOT / args.work
    song, n = args.song, int(args.song[1:])
    gretil = Path("/root/ipvv/site/data/sanskrit/sivastotravali-u.txt")
    src = load_gretil_song(gretil, n)
    src_sha = sha(" ".join(" ".join(t) for v, t in sorted(src.items())))
    data = w / "data"; data.mkdir(exist_ok=True)

    # ---- T1 ----
    t1verses = parse_t1((w / f"T1-{song}.md").read_text(encoding="utf-8"))
    assert len(t1verses) == len(src), f"T1 verses {len(t1verses)} != source {len(src)}"
    t1objs = []
    for v in t1verses:
        vid = f"{song}-v{v['verse']:02d}"
        draft = " / ".join(t["gloss"] for t in v["tokens"])
        t1objs.append({"verse_id": vid, "song": song, "verse": v["verse"],
                       "quick_english": draft, "quick_english_source": "mechanical-join-v1",
                       "tokens": [{"surface": t["iast"], "quick_gloss": t["gloss"]} for t in v["tokens"]],
                       "source_sha": src_sha})
    (data / f"{song}.t1.json").write_text(json.dumps(t1objs, indent=1, ensure_ascii=False))

    # ---- L0 (from extractor jsonl, order-matched to T1 tokens) ----
    raw = [json.loads(l) for l in (w / f"T1-{song}.l0.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    flat_t1 = [(v["verse"], t) for v in t1verses for t in v["tokens"]]
    assert len(raw) == len(flat_t1), f"l0 {len(raw)} != T1 tokens {len(flat_t1)}"
    l0objs = []
    per_verse: dict[int, int] = {}
    for i, ((vnum, t), r) in enumerate(zip(flat_t1, raw)):
        if r.get("status") == "PARSED" and not (r.get("literal_gloss") or "").strip():
            print(f"WARN token {i} PARSED but empty gloss", file=sys.stderr)
        pi = per_verse.get(vnum, 0); per_verse[vnum] = pi + 1
        l0objs.append({"id": f"{song}-v{vnum:02d}-p{pi:03d}", "legacy_id": r.get("legacy_id", r.get("id")),
                       "verse_id": f"{song}-v{vnum:02d}", "pada_index": pi,
                       "surface": t["iast"], "legacy_raw": r.get("raw_fragment", ""),
                       "citation": r.get("lemma_iast", "") or t["iast"],
                       "morph": "", "morph_unknown": True,
                       "options": [{"gloss": (r.get("literal_gloss") or t["gloss"]).strip(),
                                    "note": "backfilled from T1 gloss; options pending",
                                    "rank": 1}] if (r.get("literal_gloss") or t["gloss"]).strip() else [],
                       "chosen_index": 0, "status": r.get("status", "FAILED")})
    (data / f"{song}.l0.json").write_text(json.dumps(l0objs, indent=1, ensure_ascii=False))

    # ---- ARGMAP ----
    amd = (w / "argmaps" / f"sivst-{song}.md").read_text(encoding="utf-8")
    entries: dict[int, str] = {}
    for m in re.finditer(r"\*\*(\d+)\.(\d+)\*\* — (.*?)(?=\n\*\*\d+\.\d+\*\* — |\n## |\Z)", amd, re.S):
        entries[int(m.group(2))] = m.group(3).strip()
    unres: dict[int, list[str]] = {}
    m4 = re.search(r"## 4\. Unresolved.*?(?=\n## |\Z)", amd, re.S)
    if m4:
        for b in re.finditer(r"(?:^|\n)\d+\.\s+(.*?)(?=(?:\n\d+\.\s+)|\Z)", m4.group(0), re.S):
            txt = b.group(1).strip()
            for vm in set(re.findall(r"v\.(\d+)", txt)):
                unres.setdefault(int(vm), []).append(txt)
    argobjs = []
    for v in sorted(src):
        vid = f"{song}-v{v:02d}"
        argobjs.append({"verse_id": vid, "song": song, "verse": v,
                        "structured": False,
                        "premises": [entries[v]] if v in entries else [],
                        "reconstruction": entries.get(v, ""),
                        "uncertainties": unres.get(v, []),
                        "traces": {"t1_verse": vid,
                                   "l0_ids": [o["id"] for o in l0objs if o["verse_id"] == vid],
                                   "traces_backfilled": True},
                        "sanskrit_sha": src_sha})
    (data / f"{song}.argmap.json").write_text(json.dumps(argobjs, indent=1, ensure_ascii=False))

    # ---- L2 ----
    l2md = (w / f"L2-{song}.md").read_text(encoding="utf-8")
    l2objs = []
    for m in re.finditer(r"## v\.(\d+).*?\n(.*?)(?=\n## v\.\d+|\Z)", l2md, re.S):
        vnum, body = int(m.group(1)), m.group(2)
        cm = re.search(r"The Sanskrit: \*(.+?)\*", body)
        plain = body[:cm.start()].strip() if cm else body.strip()
        l2objs.append({"verse_id": f"{song}-v{vnum:02d}", "song": song, "verse": vnum,
                       "plain_english": re.sub(r"\n+", " ", plain),
                       "sanskrit_cite": cm.group(1).strip() if cm else "",
                       "l0_ids": [o["id"] for o in l0objs if o["verse_id"] == f"{song}-v{vnum:02d}"],
                       "trace_level": "verse"})
    (data / f"{song}.l2.json").write_text(json.dumps(l2objs, indent=1, ensure_ascii=False))

    # ---- C1 ----
    c1md = (w / "c1" / f"C1-{song}.md").read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    for m in re.finditer(r"## ([A-Z][A-Z /]+)\n(.*?)(?=\n## [A-Z]|\Z)", c1md, re.S):
        key = m.group(1).strip().split("/")[0].strip()
        sections[key] = m.group(2).strip()
    summ = sections.get("SUMMARY", "")
    essence = [s.strip() for s in re.split(r"(?<=[.!?])\s+", summ) if s.strip()]
    c1obj = {"song": song, "essence": essence, "essence_source": "mechanical-from-summary-v1",
             "renders": {"standard": {"style": "standard", "sections": sections}}}
    (data / f"{song}.c1.json").write_text(json.dumps(c1obj, indent=1, ensure_ascii=False))

    print(f"{song}: t1={len(t1objs)} l0={len(l0objs)} argmap={len(argobjs)} "
          f"l2={len(l2objs)} c1-essence={len(essence)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
