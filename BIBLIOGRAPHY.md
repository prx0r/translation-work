# BIBLIOGRAPHY.md — the final Muktabodha bibliography (base layer)

*Baseline: **2026-11-12** (`MUKTABODHA_FINAL_COVERAGE_AND_WATCH`). This is
the base layer for translation priority. Newest-first: when anything conflicts,
this baseline wins over older research matrices.*

## Where it lives (canonical)

| Role | Path |
|---|---|
| **Flat catalog** (499×19, `has_translation`) | `/root/openpatalaproject/data/corpus/muktabodha_burn_research.csv` |
| **Editions** (294 keyed records) | `/root/openpatalaproject/data/corpus/muktabodha_translation_editions.jsonl` |
| **Bibliographic links** (718 catalog↔URL) | `/root/openpatalaproject/data/corpus/muktabodha_bibliographic_links.csv` |
| **Research matrix** (499 rows, `research.translations[]`) | `/root/openpatalaproject/data/corpus/muktabodha_research_matrix.json` |
| **Availability index** (743 works; API surface) | `/root/openpatalaproject/data/corpus/translation-availability.json` |
| **Served copy** (openpatala API) | `/root/openpatala/data/translation-availability.json` |
| **Full release package** (source of truth) | `/root/openpatalaproject/data/corpus/downloads/muktabodha_final_2026-11-12/` |
| **Ranked burn** (priority order) | `/root/translation-work/process/beam/ranked_burn.json` |

Reader (single code path): `/root/translation-work/tools/bibliography.py`
Importer (re-runnable): `/root/openpatalaproject/pipeline/import_muktabodha_final.py`

## Priority rule (owner 2026-11-12) — the formula

Ranked in **buckets**, shortest-first within each, with a tunable verse-**line**
`short_max` (default 50) separating short from long:

| bucket | meaning |
|---|---|
| 1 | **untranslated-short** (T=0, verses ≤ short_max) — start here |
| 2 | **translated-short** (T>0, verses ≤ short_max) |
| 3 | **untranslated-long** (T=0, verses > short_max) — "the line": start longer untranslated here |
| 4 | translated-long |
| 8 | prose (needs a chunker) |
| 9 | in-progress (queue finishes it; not a *start* candidate) |
| 10 | machine-complete |

Sort key: `(bucket, verses, T)`. Tune `short_max` (`priority(short_max=…)`):
- `short_max=25` → 65 untranslated-short works / 570 verses
- **`short_max=50` → 95 works / 1,748 verses (recommended first sweep)**
- `short_max=100` → 128 works / 4,179 verses

- **T (translatedness)** comes from THIS bibliography first:
  edition count / `has_translation` (2026-11-12 baseline), then curated
  FAMOUS estimates, scraped hits, seed evidence, local `work_state`.
- Prose (0 verses) ranks in its own tail — never ahead of verse texts.
- Re-rank: `python3 tools/prioritize_mukta.py` (from `translation-work/`).

Current top of queue (untranslated, shortest): see
`python3 tools/bibliography.py priority --limit 20`.

## OpenPatala REST API (live)

Public, read-only, Postgres-backed: **`https://patala.svatantrya.net`** (46 `/v1/*`
routes + `/health`; OpenAPI at `/openapi.json`). Durable: `openpatala-api.service`
(:8802, enabled) behind `svatantrya-tunnel.service`.

Useful for translation work:
- `/v1/resolve?q=` — map a title/catalog to a canonical `PTW_…` work id (provenance binding)
- `/v1/works/{id}/translations` — existing translations for a work
- `/v1/translations`, `/v1/translation-availability` — availability index (743 works, 265 w/ English)
- `/v1/passages/{id}/translations` + `/alignments` — verse-level alignment to our layers
- `/v1/frontier/translations` — gaps (what to translate next)
- `/v1/passages`, `/v1/editions`, `/v1/witnesses`, `/v1/stats`

Local: `http://127.0.0.1:8802`. The MCP `availability`/`bibliography` tools already
serve the same availability data; the REST adds the identity graph (PTW ids, editions,
witnesses, alignments) that binds our translations to canonical records.

## MCP (base layer for translations)

Registered as `shastra` (remote: `https://mcp.svatantrya.net/mcp`). Full
query/browse surface:

| Tool | Args | Returns |
|---|---|---|
| `shastra.bibliography` | none | `paths()` — where the bibliography lives |
| | `catalog` or `title` | one work: editions, has_translation, availability join |
| | `q` | substring search (catalog/title/author) |
| `shastra.priority` | `limit`, `untranslated_only` | ranked burn rows (`burn_rank`, `T`, `T_why`, `edition_count`) |
| `shastra.schema` | — | every data structure: fields, types, values, paths |
| `shastra.stats` | — | counts: positives, editions, languages, coverage, domains |
| `shastra.works` | `has_translation`, `language`, `min/max_verses`, `limit`, `offset` | filtered work list |
| `shastra.editions` | `catalog`, `language`, `tier`, `downloadable_only` | **translation links** (translator/year/url/evidence) |
| `shastra.links` | `catalog`, `domain`, `edition_related` | 718 catalog↔URL with roles |
| `shastra.availability` | `catalog`, `work`, `language`, `coverage`, `missing` | 743-work compiled index |

```bash
# CLI equivalents
python3 tools/bibliography.py paths|stats|schema
python3 tools/bibliography.py get --catalog M00031
python3 tools/bibliography.py search kularnava
python3 tools/bibliography.py priority --limit 20
python3 tools/bibliography.py works --has-translation false --limit 20
python3 tools/bibliography.py editions --catalog M00031
python3 tools/bibliography.py links --catalog M00031
python3 tools/bibliography.py availability --coverage none --limit 20
```

Typical browse flow:
1. `stats` → orientation
2. `priority` → pick next work
3. `bibliography` with that catalog → what translations already exist
4. `editions` / `links` → exact translation URLs + evidence
5. `recon` → `swarm_seed` (or hand-draft) → layers → `promote`


## Stats (baseline 2026-11-12)

- 499 catalog rows · **213** with translation evidence · **294** keyed editions
- 286 unresolved (NOT proven untranslated)
- Availability index: **743** works · M-catalog coverage full 125 / partial 82 / none 271
- Languages (editions): en 194, hi 53, fr 15, de 14, …

## Do not

- Do not re-research from zero — this baseline is the prior art.
- Do not label unresolved works “untranslated” without exhaustive review.
- Do not serve `translation-availability.json` from `patalacheckpoints`
  (stale); always `PATALA_ROOT=/root/openpatalaproject`.
- Do not treat the package README’s older batch counts as current — the
  staged corpus files above are the post-merge truth.
