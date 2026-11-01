#!/usr/bin/env python3
"""tools/build_concepts.py — build concept database from C1 KEY TERMS + lore.

  python3 tools/build_concepts.py [--work ghatakarpara]

Reads C1 KEY TERMS from data/<work>.c1.json, checks each against lore/concepts/.
Reports: defined, missing (no concept file), orphan (concept file with no C1 ref).
Does NOT auto-create concept files (scholarly definitions require human input).
Exit 0 if all C1 key terms have concept files; 1 if gaps found.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")


def slug(term: str) -> str:
    return term.lower().replace(" ", "-").replace("ā", "a").replace("ī", "i").replace("ū", "u").replace("ṛ", "r").replace("ṃ", "m").replace("ḥ", "h").replace("ś", "s").replace("ṣ", "s").replace("ṭ", "t").replace("ḍ", "d").replace("ṇ", "n").replace("ṅ", "n").replace("ñ", "n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="ghatakarpara")
    args = ap.parse_args()
    w = ROOT / args.work
    data = w / "data"
    concepts_dir = ROOT / "lore" / "concepts"
    defined = {p.stem for p in concepts_dir.glob("*.json") if p.name != "README.md"}

    # Collect key terms from C1 files
    c1_terms = set()
    for cf in sorted(data.glob("*.c1.json")):
        c1 = json.loads(cf.read_text())
        std = (c1.get("renders", {}).get("standard", {}) or {})
        kt = std.get("sections", {}).get("KEY TERMS", "") or std.get("key_terms", "")
        if isinstance(kt, str):
            for line in kt.splitlines():
                line = line.strip().lstrip("*-• ").strip()
                if not line:
                    continue
                # "term — gloss" or "term: gloss"
                m = re.split(r"\s+[—–-]\s*|\s*:\s*", line, maxsplit=1)
                term = m[0].strip().lower().strip("*").strip()
                # remove bold markers
                term = re.sub(r"\*+", "", term).strip()
                if (term and len(term) >= 2 and len(term.split()) == 1
                        and not any(c in term for c in ".,;:!?()[]{}0123456789")
                        and not term.startswith("boundary") and not term.startswith("explanation")
                        and not term.startswith("local") and not term.startswith("related")):
                    c1_terms.add(term)

    missing = sorted(t for t in c1_terms if slug(t) not in defined)
    orphan = sorted(s for s in defined if s not in {slug(t) for t in c1_terms} and s != "README")

    print(json.dumps({
        "work": args.work,
        "c1_key_terms": sorted(c1_terms),
        "defined_concepts": sorted(defined),
        "missing (no concept file)": missing,
        "orphans (concept file, no C1 ref in this work)": orphan,
        "coverage": f"{len(c1_terms) - len(missing)}/{len(c1_terms)}",
    }, indent=1, ensure_ascii=False))

    # Also check all works' C1 key terms against concept files
    all_terms = set()
    for cf in (ROOT).glob("*/data/*.c1.json"):
        c1 = json.loads(cf.read_text())
        std = (c1.get("renders", {}).get("standard", {}) or {})
        kt = std.get("sections", {}).get("KEY TERMS", "") or std.get("key_terms", "")
        if isinstance(kt, str):
            for line in kt.splitlines():
                line = line.strip().lstrip("*-• ").strip()
                if not line:
                    continue
                m = re.split(r"\s+[—–-]\s*|\s*:\s*", line, maxsplit=1)
                term = re.sub(r"\*+", "", m[0].strip()).strip().lower()
                if (term and len(term) >= 2 and len(term.split()) == 1
                        and not any(c in term for c in ".,;:!?()[]{}0123456789")
                        and not term.startswith("boundary") and not term.startswith("explanation")
                        and not term.startswith("local") and not term.startswith("related")):
                    all_terms.add(term)

    all_missing = sorted(t for t in all_terms if slug(t) not in defined)
    print(f"\n=== ACROSS ALL WORKS ===")
    print(f"Total unique C1 key terms: {len(all_terms)}")
    print(f"Defined concepts: {len(defined)}")
    print(f"Missing concept files: {len(all_missing)}")
    if all_missing:
        print("  " + ", ".join(all_missing[:30]))
        if len(all_missing) > 30:
            print(f"  ... and {len(all_missing)-30} more")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
