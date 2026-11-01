# Concept database (built during translation, consolidated after)

*One JSON file per concept: `lore/concepts/<term-slug>.json`.
Built incrementally: each C1's KEY TERMS feeds it. Consolidated at the end of a work.
Cross-references, scholarly sources, and related terms are added as we encounter them.*

## Schema (per concept)

```json
{
  "term": "spanda",
  "iast": "spanda",
  "definition": "Śiva's autonomy-power (svasvātantryaśakti), by which he is conscious of himself. Synonymous with Śakti = I-consciousness. Not a physical vibration but a movement in the space of Consciousness.",
  "tradition": "Trika/Kashmir Śaivism",
  "rasa": "adbhuta/śānta (wonder at unmeasured greatness resolving into tranquility)",
  "sources": [
    {"scholar": "Abhinavagupta", "work": "Spandasandoha (vivṛti on Spandakārikā 1.1)", "claim": "spanda = Śiva's self-aware autonomy"},
    {"scholar": "sanskrit-trikashaivism.com", "work": "Spandakārikā translation", "claim": "Spanda is synonymous with Śakti (I-consciousness)"}
  ],
  "works": ["spandasandoha", "spandakarika", "tantraloka"],
  "related": ["svātantrya", "vimarśa", "pratyabhijñā", "śakti", "māyā"],
  "translations": {
    "en": "throb / vibration / pulsation",
    "note": "No English equivalent; 'throb' is the closest but carries physical connotations that mislead. Use 'autonomy-power' or 'self-aware throb' in technical contexts."
  }
}
```

## When to build

- **During translation**: when you write a C1 KEY TERMS section, create or update the concept file.
- **After each work**: consolidate — merge new terms, add cross-references, link to lore notes.
- **At the end**: full audit — every concept cited in C1 has a file; every file has sources.

## Rules

1. One file per concept. Slug = lowercase IAST with diacritics stripped for filename
   (spanda.json, svatantrya.json, pratyabhijna.json).
2. Definition must be sourced — cite scholar + work, not just "means X."
3. Related terms must exist as files (or be flagged as "not-yet-defined").
4. No concept file without a C1 KEY TERMS entry pointing at it (and vice versa).
5. The glossary (site/data/glossary.json) is built FROM concept files, not the other way.


## Gold reference: sanskrit-trikashaivism.com Trika Glossary

The glossary at sanskrit-trikashaivism.com is the gold reference for Trika terminology.
It is organized by Sanskrit alphabet (8 pages):
- Vowels: /en/trika-glossary-vowels/525
- Gutturals: /en/trika-glossary-gutturals/526
- Palatals: /en/trika-glossary-palatals/527
- Dentals: /en/trika-glossary-dentals/528
- Labials: /en/trika-glossary-labials/529
- Semivowels: /en/trika-glossary-semivowels/530
- Sibilants: /en/trika-glossary-sibilants-and-sonant-aspirate/531

Each entry: Devanagari | IAST | definition (with cross-references to related terms).
The definitions cross-reference other terms ("Sanskrit terms occurring in the definitions
have generally their own definition in the Glossary as well"). This IS a knowledge graph:
nodes = terms, edges = cross-references, properties = definitions.

### How to use it

1. When `build_concepts.py` reports a missing concept, check if it's in the glossary.
2. Fetch the relevant glossary page (by first letter of the term).
3. Create a concept file with the glossary definition as the base, then enrich:
   - Add scholarly sources (Abhinavagupta, Kṣemarāja, etc.)
   - Add rasa (from C1 rasa block)
   - Add works (which of our works use this term)
   - Add related terms (from glossary cross-references + our own)
   - Add translations (English equivalents + notes)
4. The concept file is the enriched node; the glossary is the raw node.
   Our graph is a superset of the glossary graph.

### Do NOT scrape all 100+ terms upfront

That's batchy. Create concept files as we encounter terms in translation. The
build_concepts.py tool tells us what's missing. Fetch from the glossary on demand.
Over time, the concept database grows to cover the terms we actually use, with
scholarly enrichment that the glossary doesn't have.


## Glossary index (scraped 2026-11-01)

`lore/trika_glossary_index.json` — 325 terms from sanskrit-trikashaivism.com, parsed from
7 HTML pages (vowels, gutturals, palatals, dentals, labials, semivowels, sibilants).
Each entry: {devanagari, iast, definition, page}.

This is the RAW graph (terms + definitions + cross-references in prose). Our concept
files are the ENRICHED graph (sources, rasa, works, related terms, translations).

### How to use the index

1. When `build_concepts.py` reports a missing concept, check the glossary index:
   `python3 tools/lookup_concept.py <term>` — shows the definition if it exists.
2. If found: `python3 tools/lookup_concept.py --create <term>` — creates a concept
   file skeleton with the glossary definition as the base. Enrich with sources, rasa,
   works, related terms.
3. If not found: the term is not in the trika glossary. Create a concept file manually
   with scholarly sources. Flag it as "not in trika glossary" in the sources.

### The graph

The glossary is a knowledge graph: nodes = terms, edges = cross-references ("Sanskrit
terms occurring in the definitions have generally their own definition in the Glossary
as well"). Our concept database is a richer version of the same graph. The trika
glossary is the "raw" graph; our concept files are the "enriched" graph.

Over time, as we translate more works, the concept database grows to cover more of
the glossary's 325 terms. But we don't pre-populate all 325 — we create concept files
as we encounter terms in translation. The glossary index is the lookup table; the
concept files are the enriched nodes.
