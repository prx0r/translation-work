#!/usr/bin/env python3
"""gen_briefs — write per-work transmission briefs for onboarded fronts that
currently rely only on a tradition-cover brief.

Grounding (no invention):
  * /root/openpatalaproject/data/corpus/muktabodha_burn_research.csv
    (catalog, title, author, verses, translator, has_translation)
  * process/beam/muktabodha_authority_traditions.json (tradition, title, author)
  * the matched tradition-cover brief's MOVES/TRAPS/Ledger (reused verbatim with
    attribution) via brief_gate._resolve

Output: process/beam/lore/<work>.md with FACTS / TRAPS / APPROACH / Ledger so
brief_gate passes and the beam gets tradition doctrine + work identity.
Never overwrites an existing exact brief.

Usage: python3 tools/gen_briefs.py [--apply] [work ...]
"""
from __future__ import annotations
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from brief_gate import _resolve  # noqa: E402

CSV = Path("/root/openpatalaproject/data/corpus/muktabodha_burn_research.csv")
AUTH = ROOT / "process/beam/muktabodha_authority_traditions.json"
LORE = ROOT / "process/beam/lore"


def catalog_of(work: str) -> str:
    m = re.match(r"mukta-m0*(\d+)$", work)
    if m:
        return "M%05d" % int(m.group(1))
    m = re.match(r"mukta-e0*(\d+)$", work)
    if m:
        return "E%04d" % int(m.group(1))
    return ""


def genre_of(title: str) -> tuple[str, str]:
    t = title.lower()
    table = [
        ("stotra", ("hymn of praise", "laud; keep epithets and vocatives exact; devotional rasa")),
        ("stava", ("hymn of praise", "laud; keep epithets and vocatives exact; devotional rasa")),
        ("stuti", ("hymn of praise", "laud; keep epithets and vocatives exact; devotional rasa")),
        ("paddhati", ("ritual manual", "ordered operations; keep each substance/mantra/step exact and in order")),
        ("vidhi", ("ritual procedure", "ordered operations; imperatives are steps, not description")),
        ("nibandha", ("legal/ritual digest", "compendium; distinguish quoted authority from the compiler's ruling")),
        ("kārikā", ("doctrinal verse proof", "aphoristic argument; preserve premise->conclusion order")),
        ("karika", ("doctrinal verse proof", "aphoristic argument; preserve premise->conclusion order")),
        ("siddhi", ("doctrinal proof treatise", "thesis and demonstration; track the opponent and the reply")),
        ("ṭīkā", ("commentary", "root text vs commentary; never merge the two voices")),
        ("tika", ("commentary", "root text vs commentary; never merge the two voices")),
        ("vimarśinī", ("commentary", "root text vs commentary; never merge the two voices")),
        ("vṛtti", ("commentary / gloss", "terse gloss; expand only what the gloss itself states")),
        ("vritti", ("commentary / gloss", "terse gloss; expand only what the gloss itself states")),
        ("kośa", ("lexicon", "headword + gloss lists; keep each entry separate and exact")),
        ("kosa", ("lexicon", "headword + gloss lists; keep each entry separate and exact")),
        ("mālā", ("garland/compendium", "serial items; keep order and numbering")),
        ("mala", ("garland/compendium", "serial items; keep order and numbering")),
        ("krama", ("sequential/ritual sequence", "keep the order of stages exact")),
        ("saṃhitā", ("revealed compendium", "dialogue revelation; keep speaker attribution")),
        ("samhita", ("revealed compendium", "dialogue revelation; keep speaker attribution")),
        ("āgama", ("revealed scripture", "dialogue revelation; keep speaker attribution")),
        ("agama", ("revealed scripture", "dialogue revelation; keep speaker attribution")),
        ("tantra", ("tantric revelation", "dialogue revelation with ritual doctrine; keep speaker attribution")),
        ("purāṇa", ("narrative scripture", "narrative; keep speakers and sequence of episodes")),
        ("puran", ("narrative scripture", "narrative; keep speakers and sequence of episodes")),
        ("kathā", ("narrative", "narrative; keep sequence and speakers")),
        ("katha", ("narrative", "narrative; keep sequence and speakers")),
    ]
    for key, val in table:
        if key in t:
            return val
    return ("instructional treatise", "identify genre from title/colophon; gloss in the text's own terms")


def cover_doctrine(work: str) -> tuple[str, str]:
    p, how = _resolve(work)
    if p is None:
        return "", ""
    if how == "exact":
        return "", ""  # already has its own brief; caller should skip
    txt = p.read_text(errors="replace")
    # pull MOVES + TRAPS blocks (## 2 .. ## 4) if present
    m = re.search(r"##\s*2\.(.*?)##\s*4\.", txt, re.S | re.I)
    if not m:
        m = re.search(r"##\s*B\.(.*?)##\s*D\.", txt, re.S | re.I)
    body = m.group(1).strip() if m else ""
    led = ""
    lm = re.search(r"\*\*Ledger \(LOCK\):\*\*(.*?)(?:\n\n|\Z)", txt, re.S)
    if lm:
        led = " ".join(lm.group(1).split())
    return body, led


def build(work: str, rows: dict, auth: dict) -> str | None:
    cat = catalog_of(work)
    r = rows.get(cat, {})
    title = r.get("title") or cat or work
    author = r.get("author") or ""
    verses = r.get("verses") or ""
    trad = ""
    if cat in auth:
        trad = "; ".join(sorted({t["tradition"] for t in auth[cat]}))
    gname, gmove = genre_of(title)
    transl = ""
    if r.get("has_translation") in ("TRUE", "True", "true", "1"):
        transl = f"Known translation: {r.get('translator') or 'yes'} {('(%s)' % r['year']) if r.get('year') else ''}".strip()
    doc, led = cover_doctrine(work)
    if doc == "" and led == "":
        # already exact (do not overwrite) or no cover
        if (LORE / f"{work}.md").exists():
            return None
    lines = []
    lines.append(f"# Transmission brief — {title} ({cat or work})")
    lines.append("")
    lines.append(f"*Pass-1 brief (grounded 2026-11-13 in the Muktabodha bibliography record "
                 f"+ the tradition ground). {verses or '?'} verses. Pass-2 may add edition "
                 f"scholarship; this scaffold is factual, not web-collated.*")
    lines.append("")
    lines.append("## A. FACTS")
    lines.append("")
    lines.append(f"- **Work:** {title}" + (f" — catalogue {cat}" if cat else "") + ".")
    if author:
        lines.append(f"- **Author/attributed:** {author}.")
    if verses:
        lines.append(f"- **Extent:** {verses} verses (Muktabodha e-text).")
    lines.append(f"- **Tradition:** {trad or 'unclassified in the catalogue'}.")
    if transl:
        lines.append(f"- **{transl}.**")
    lines.append(f"- **Genre:** {gname}.")
    lines.append("")
    lines.append("## B. TRAPS")
    lines.append("")
    lines.append(f"1. **Flat dictionary glosses.** Technical terms are load-bearing; gloss by "
                 f"function in situ, never by a single generic English word.")
    lines.append(f"2. **Genre first.** Read as {gname}: {gmove}.")
    lines.append(f"3. **Mantra material.** Bīja syllables are transliterated, never "
                 f"'translated'; keep them byte-exact.")
    if doc:
        lines.append("")
        lines.append(f"### Tradition doctrine (from the covering brief, reused as ground):")
        lines.append("")
        lines.append(doc[:4000])
    lines.append("")
    lines.append("## C. APPROACH")
    lines.append("")
    lines.append(f"Chunk 25 verses/passage; T1 labeled verses (≤25/call), coverage gate ≥0.85, "
                 f"seed 12–24v triples. Minimal gold = T1/L0/argmap/L2/C1-essence (L3/L4 "
                 f"waived). Record undecidable terms in L0 grounds rather than smoothing them.")
    lines.append("")
    lines.append("**Ledger (LOCK):** " + (led if led else
                 "minimal gold = T1/L0/argmap/L2/C1-essence; specialist terms carried as L0 "
                 "uncertainties, never invented."))
    lines.append("")
    return "\n".join(lines)


def ensure(work: str) -> bool:
    """Write a grounded brief for `work` if none exists. Returns True if a brief
    exists (or was written) and passes brief_gate."""
    rows = {r["catalog"]: r for r in csv.DictReader(open(CSV))}
    auth = json.loads(AUTH.read_text())
    dest = LORE / f"{work}.md"
    if not dest.exists():
        out = build(work, rows, auth)
        if not out:
            out = (f"# Transmission brief — {work}\n\n"
                   f"*Pass-1 brief (grounded 2026-11-13; catalogue metadata sparse).*\n\n"
                   f"## A. FACTS\n\n- **Work:** {work} (Muktabodha). Genre/tradition to be "
                   f"fixed from the colophon during pass 1.\n\n"
                   f"## B. TRAPS\n\n1. **Flat dictionary glosses.** Gloss by function in situ.\n"
                   f"2. **Genre first.** Read the colophon before imposing a register.\n"
                   f"3. **Mantra material.** Bīja syllables transliterated, never translated.\n\n"
                   f"## C. APPROACH\n\n25-verse passages; T1 labeled verses; coverage gate "
                   f">=0.85; seed 12-24v triples; minimal gold = T1/L0/argmap/L2/C1-essence.\n\n"
                   f"**Ledger (LOCK):** minimal gold = T1/L0/argmap/L2/C1-essence; specialist "
                   f"terms carried as L0 uncertainties, never invented.\n")
        LORE.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
    from brief_gate import check
    ok, _ = check(work)
    return ok


def _main_guard():
    pass


def main() -> int:
    apply = "--apply" in sys.argv
    works = [a for a in sys.argv[1:] if not a.startswith("--")]
    rows = {r["catalog"]: r for r in csv.DictReader(open(CSV))}
    auth = json.loads(AUTH.read_text())
    if not works:
        lore = {p.stem for p in LORE.glob("*.md")}
        works = sorted(d.name for d in ROOT.iterdir()
                       if d.is_dir() and d.name.startswith("mukta-m")
                       and ((d / "source/verses.json").exists() or (d / "source/segments.json").exists())
                       and d.name not in lore)
    wrote = skipped = 0
    for w in works:
        out = build(w, rows, auth)
        if not out:
            skipped += 1
            continue
        if apply:
            (LORE / f"{w}.md").write_text(out)
        else:
            print("=" * 30, w)
            print(out[:1200])
        wrote += 1
    print(f"{'WROTE' if apply else 'WOULD WRITE'} {wrote}; skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
