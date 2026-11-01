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
