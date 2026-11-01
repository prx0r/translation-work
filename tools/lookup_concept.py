#!/usr/bin/env python3
"""tools/lookup_concept.py — look up a term in the trika glossary index.

  python3 tools/lookup_concept.py spanda
  python3 tools/lookup_concept.py --search "consciousness"
  python3 tools/lookup_concept.py --create spanda  (creates concept file skeleton from glossary)

The glossary index (lore/trika_glossary_index.json) has 325 terms from
sanskrit-trikashaivism.com. This tool looks up a term and optionally creates
a concept file skeleton that the translator enriches with sources, rasa, works.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
GLOSSARY = ROOT / "lore" / "trika_glossary_index.json"
CONCEPTS = ROOT / "lore" / "concepts"


def slug(term: str) -> str:
    import unicodedata
    # Simple slug: lowercase, strip diacritics
    nfkd = unicodedata.normalize('NFKD', term.lower())
    return ''.join(c for c in nfkd if c.isalnum() or c == '-').strip('-')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("term", nargs="?")
    ap.add_argument("--search", default=None, help="search definitions for a keyword")
    ap.add_argument("--create", default=None, help="create concept file skeleton for term")
    ap.add_argument("--list", action="store_true", help="list all terms")
    args = ap.parse_args()

    glossary = json.loads(GLOSSARY.read_text(encoding='utf-8'))

    if args.list:
        for term in sorted(glossary):
            print(f"  {term}: {glossary[term]['definition'][:60]}...")
        return 0

    if args.search:
        q = args.search.lower()
        hits = [(t, info) for t, info in glossary.items()
                if q in t.lower() or q in info['definition'].lower()]
        for t, info in sorted(hits):
            print(f"  {t} ({info['devanagari']}): {info['definition'][:100]}...")
        print(f"\n  {len(hits)} hits")
        return 0

    if args.create:
        term = args.create
        # find in glossary (case-insensitive)
        match = None
        for t, info in glossary.items():
            if t.lower() == term.lower():
                match = (t, info)
                break
        if not match:
            # fuzzy
            for t, info in glossary.items():
                if term.lower() in t.lower():
                    match = (t, info)
                    break
        if not match:
            print(f"Term '{term}' not found in glossary", file=sys.stderr)
            return 1
        t, info = match
        s = slug(t)
        out_path = CONCEPTS / f"{s}.json"
        if out_path.exists():
            print(f"Concept file already exists: {out_path}")
            return 0
        concept = {
            "term": t,
            "iast": t,
            "definition": info['definition'],
            "tradition": "Trika/Kashmir Śaivism",
            "rasa": "TBD (fill during translation)",
            "sources": [{"scholar": "sanskrit-trikashaivism.com", "work": "Trika Glossary", "claim": info['definition'][:200]}],
            "works": [],
            "related": [],
            "translations": {"en": "", "note": "Fill during translation. Glossary definition above is the base."}
        }
        CONCEPTS.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(concept, indent=1, ensure_ascii=False), encoding='utf-8')
        print(f"Created concept skeleton: {out_path}")
        print(f"  Definition: {info['definition'][:100]}...")
        print(f"  Enrich with: sources, rasa, works, related terms, translations")
        return 0

    if args.term:
        term = args.term
        match = None
        for t, info in glossary.items():
            if t.lower() == term.lower():
                match = (t, info)
                break
        if not match:
            for t, info in glossary.items():
                if term.lower() in t.lower():
                    match = (t, info)
                    break
        if not match:
            print(f"Term '{term}' not found", file=sys.stderr)
            return 1
        t, info = match
        print(f"Term: {t} ({info['devanagari']})")
        print(f"Page: {info['page']}")
        print(f"Definition: {info['definition']}")
        # Check if concept file exists
        s = slug(t)
        cp = CONCEPTS / f"{s}.json"
        print(f"Concept file: {'EXISTS' if cp.exists() else 'MISSING (create with --create)'}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
