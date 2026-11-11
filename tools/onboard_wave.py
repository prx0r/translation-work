#!/usr/bin/env python3
"""onboard_wave — take N shortest not_started works -> full Pass-1 setup -> burn.

Per work: onboard (source intake + passages + STATUS), auto-brief lore from
the authority tradition, then run auto_burn for it (T1 -> gate -> seed).

Safety (structural, not advisory):
  * refuses catalogs in process/beam/work_aliases.json (dupe prevention)
  * refuses existing work dirs
  * refuses prose (0-verse) — needs the chunker
  * realm filter: skips Mantranaya/Vajrayāna

Usage:
  python3 tools/onboard_wave.py --n 12 [--dry] [--min-verses 1 --max-verses 60]
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, "/root/openpatalaproject/pipeline")

MUKTA = Path("/tmp/mukta/MUKTABODHA-LIBRARY-IAST")
OUT_OF_REALM = ("mantranaya", "vajray", "guhyasamaja", "manjusri", "sadhanamala",
                "advayavajra")

BRIEF = """# Transmission brief — {title} ({catalog})

*AUTO-BRIEF (pass-1 scaffold; pass-2 must add real web scholarship).
Tradition per Muktabodha authority: **{trads}**. {verses} verses.
Editors/scribes per catalogue: {who}.*

## 1. WHAT IT IS

{title} — a {trads} work in the Muktabodha corpus. Pass-1 target: literal
pada glosses + argument maps that stay inside the tradition's own terms.
Do NOT import later Trika technical vocabulary unless the text uses it.

## 2. MOVES TO LOOK FOR

1. **Genre first.** Identify the genre from the title/colophon
   (stotra = praise; paddhati/vidhi = ritual procedure; tantra = dialogue
   revelation; karika/siddhi = doctrinal proof). The gloss strategy
   follows the genre.
2. **Ritual sequences.** In paddhati material, imperative steps are
   ordered operations — keep the order and each substance/mantra exact.
3. **Divine speech.** In tantra/stotra, keep speaker (Śiva/Devī/narrator)
   distinct per verse.

## 3. TRAPS

1. **Flat dictionary glosses.** Technical terms in this tradition are
   load-bearing; gloss by function in situ, never by generic meaning.
2. **Mantra material.** Bīja syllables are transliterated, never
   "translated"; keep them byte-exact.
3. **Audit gap.** This brief is a scaffold: verify specialist terms on
   pass 2 before promoting beyond minimal gold.

## 4. APPROACH

Short work: chunk 25 verses/passage, T1 labeled verses (≤25/call),
coverage gate ≥0.85, seed 12-verse triples. Minimal gold = T1/L0/argmap/
L2/C1-essence (L3/L4 waived).

**Ledger (LOCK):** (pass-2 fills the work-specific terms; pass-1 uses
in-situ functional glosses and records uncertain terms in L0 grounds.)
"""


def norm(s: str) -> str:
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return "".join(ch for ch in s if ch.isalpha())


def onboard(cat: str, title: str, verses: list, trads: str, who: str) -> Path:
    from intake import validate_segments
    from harvest_to_factory import extract_verses
    src = next(MUKTA.glob(f"*{cat}-IAST.txt"), None)
    if src is None:
        raise FileNotFoundError(f"no muktabodha file for {cat}")
    w = ROOT / f"mukta-{cat}".lower()
    (w / "source").mkdir(parents=True, exist_ok=True)
    (w / "data").mkdir(exist_ok=True)
    (w / "proof").mkdir(exist_ok=True)
    # verse texts straight from the extractor (canonical for this work)
    json.dump(verses, open(w / "source/verses.json", "w"), ensure_ascii=False)
    ps = []
    for i in range(0, len(verses), 25):
        n = i // 25 + 1
        ps.append({"work_id": w.name, "order": n,
                   "locator": f"{w.name[:10]}-p{n:02d}",
                   "verses": f"{i+1}-{i+len(verses[i:i+25])}",
                   "sanskrit": " ".join(verses[i:i + 25])})
    with open(w / "passages.jsonl", "w") as f:
        for p in ps:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    # source intake (workcfg-registerable)
    text = "\n\n".join(v.strip() for v in verses) + "\n"
    raw = text.encode()
    segs, pos = [], 0
    for idx, v in enumerate(verses):
        song = ps[min(idx // 25, len(ps) - 1)]["locator"]
        b = v.strip().encode()
        start = raw.find(b, pos)
        end = start + len(b)
        pos = end
        segs.append({"song": song, "verse": idx + 1,
                     "verse_id": f"{song}-v{idx+1}",
                     "start": start, "end": end})
    (w / "source/edition.txt").write_bytes(raw)
    sj = json.dumps(segs, ensure_ascii=False)
    (w / "source/segments.json").write_text(sj, encoding="utf-8")
    man = {"format": "source-intake/1", "work": w.name,
           "source_sha256": hashlib.sha256(raw).hexdigest(),
           "segments_sha256": hashlib.sha256(sj.encode()).hexdigest(),
           "edition": f"Muktabodha {cat} (IAST, CC BY-NC 4.0)"}
    (w / "source/manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    errs = validate_segments(raw, segs)
    if errs:
        raise ValueError(f"{cat}: intake invalid: {errs[:2]}")
    json.dump({"work": w.name, "updated": "2026-11-11",
               "next": "pass-1 auto_burn (T1 -> triples -> assemble)",
               "counts": {"passages": len(ps), "verses": len(verses),
                          "proof": "QUEUED"}},
              open(w / "STATUS.json", "w"), ensure_ascii=False, indent=1)
    brief = ROOT / "process/beam/lore" / f"{w.name}.md"
    brief.parent.mkdir(parents=True, exist_ok=True)
    if not brief.exists():
        brief.write_text(BRIEF.format(title=title, catalog=cat, trads=trads,
                                      verses=len(verses), who=who or "unknown"))
    return w


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--max-verses", type=int, default=60)
    ap.add_argument("--min-verses", type=int, default=3)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    ranked = json.load(open(ROOT / "process/beam/ranked_burn.json"))
    aliases = json.load(open(ROOT / "process/beam/work_aliases.json"))["catalogs"]
    auth = json.load(open(ROOT / "process/beam/muktabodha_authority_traditions.json"))
    census = {r["catalog"]: r for r in json.load(open("/tmp/mukta_census.json"))}
    from harvest_to_factory import extract_verses
    import os as _os
    def _no_dir(cat):
        return not _os.path.isdir(ROOT / f"mukta-{cat}".lower())

    todo = [o for o in ranked
            if o["tw"] == "not_started" and _no_dir(o["catalog"])
            and a.min_verses <= o["verses"] <= a.max_verses
            and o["catalog"] not in aliases
            and not any(k in norm(census[o["catalog"]]["title"] + " "
                                  + census[o["catalog"]]["file"])
                        for k in OUT_OF_REALM)][:a.n]
    print(f"wave candidates: {len(todo)}")
    for o in todo:
        c = census[o["catalog"]]
        trads = " / ".join(t["tradition"] for t in auth.get(o["catalog"], [])) or "unclassified"
        who = ", ".join(filter(None, [c.get("author"), c.get("author")]))
        print(f"  {o['verses']:4d}v {o['catalog']} {c['title'][:44]} [{trads[:34]}]")
        if a.dry:
            continue
        try:
            src = next(MUKTA.glob(f"*{o['catalog']}-IAST.txt"))
            verses = extract_verses("MUKTABODHA", o["catalog"], src)
            w = onboard(o["catalog"], c["title"], verses, trads, who)
            print(f"    onboarded -> {w.name} ({len(verses)} verses)")
            subprocess.Popen([sys.executable, str(ROOT / "tools/auto_burn.py"),
                              "--work", w.name, "--from", "1",
                              "--to", str(len(verses) // 25 + 1)],
                             stdout=open(f"/root/autoburn-{w.name}.log", "w"),
                             stderr=subprocess.STDOUT, env=os.environ.copy())
            print("    auto_burn launched")
        except Exception as e:  # noqa: BLE001
            print(f"    FAILED: {str(e)[:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
