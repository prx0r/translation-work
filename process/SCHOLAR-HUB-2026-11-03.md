# SCHOLAR HUB — the endgame: git-versioned research objects, scholar sign-off, live

*2026-11-03. The session that found the whole review vision already on disk, vendored the
human-authority machinery, and built the Scholar hub. Read with `tools/human_authority/PROVENANCE.md`.*

## 1. The endgame (owner's words, kept verbatim)

> "each of these files as their own git objects … we can store versions of them … the endgame is
> ai agents can push versions and we can have scholars reviewing and then basically the scholar
> signs it off and it gets live"

Concretely:

```
git blob  = the object        (each data/*.json is content-addressed by git)
git commit = the version      (append-only, fast-forward-only, no force-push)
agent push = scholar.py save  (MACHINE_DRAFT / author-attributed version)
scholar review = ReviewEvent bound to an EXACT version (hash), never a mutation
sign-off = PromotionEvent (NOT_REVIEWED → INDEPENDENT_REVIEWED) + signoff.json
live = check.py CANONICAL + signoff present → emit_site → svread publishes
fork = a version whose parent is another scholar's version (child, like git)
```

## 2. The research-object (RO) vision already on disk

- **586 `ro.json` files** across the box (`damn/research-library/research-objects/` + `content-sources/`).
  Spec fields: `ro_id` · `schema_version` · **`current_version` (semver)** · `status`
  (stub→draft→…) · `sources[]` with **`first_added_in` / `last_reviewed_in` version stamps** ·
  `body[]` with `source_ids` provenance · **`versions[]` changelog** (`{version, date, type,
  summary, sources_added/removed, passage_count, test_pass_rate, skill_id}`).
- **`truthagent.md`** = the epistemic contract: claim statuses T/L/R/V/D/H/C/E/U/X; unit of
  research = one inferential transition; every RO carries source passage → verdict → next
  unresolved transition.
- **RO-Crate 1.1** packaging already prototyped in
  `/root/patalacheckpoints/source-evidence/pilot-out/ro-crate-metadata.json`
  (FaBiO + PROV-O + Web Annotation).
- Catalog: `damn/research-library/research-objects/README.md` ("the structured evidence base").

## 3. Deep-dive: patalacheckpoints (what we imported)

The scholar sign-off layer was already built and tested there:

| Module | What it does | Tests |
|---|---|---|
| `source-evidence/schema/contracts_human_authority.py` | the 4 human objects: **ReviewEvent** (evidence about an EXACT version, `event_hash`, never a mutation) · ReviewProposal · Adjudication · PromotionEvent (the mechanical status transition, `basis[]`) | (dataclasses) |
| `pipeline/review_engine.py` | append-only `ReviewLedger`, immutable `ObjectVersion`, typed `DependencyEdge` (GROUNDS/USES_AS_PREMISE/USES_AS_WARRANT/ORGANIZES), deterministic reducer → **ImpactReport** (what a correction stales). Doctrine: ACCEPT ≠ truth · REVISE ≠ overwrite | 23/23 |
| `pipeline/review_bundle.py` | compiled review context (scholar workbench input) | PASS |
| `patala_ml/goldchain.py` + `philproof.py` | per-dimension certificate (SOURCE_INTEGRITY/MORPH/LEXICAL/INTERPRETATION/INFERENCE/ESSAY_CLAIM — **never one number**), philological + derivational proof kept separate | 40/40 |

**Vendored verbatim into `tools/human_authority/`** (no edits; see its PROVENANCE.md) —
63/63 checks green in this repo.

Also read from patalacheckpoints:
- **Layer 08 (Human Authority)**: review attached to EXACT version → proposal → adjudication →
  new version (supersedes) → downstream staleness via dependency engine. Status: real, UI pending.
- **openpatala** (storage doctrine, locked): `Postgres = entity truth · R2 = bytes ·
  event log = history truth`; typed IDs (PTR… = ReviewEvent); "OpenAlex for Sanskrit".
- **whole_chain_proof.py**: one passage across SOURCE→…→SYNTHESIS with honest present/missing gaps.

## 4. Other evidence gathered

- **ipvv qprivately** (already in `ipvv/tools/qp_acom`): `transition()` receipts with merkle
  `evidence_root`, content-derived ids, pinned gate program hashes, Ed25519 `sign_receipt()` +
  `grants` (signing present, unused until now — this session wires it for scholar signatures).
- **sanskritree R2** (523 objects): `ipvv-translations/{pilot,l0,t1-golden,t1-vol1}` + 30
  `batch-t1/*.jsonl` raw drafts (incl. paramarthasara).
- **Existing review loop in this repo**: `schemas/signoff.py`
  (`{song, accepted_by, date, scope}`; data change after signoff date re-opens review) +
  `tools/propose.py` (propose → support → accept/reject, history written never silent).
  Zero signoffs existed before this session — paramarthasara is the first.

## 5. The build (this session's 10 steps)

1. This document.
2. **Pristine data structures** — `paramarthasara/scholar/`:
   - `versions.jsonl` — append-only. One line per scholar version:
     `{version_id, work, layer, target, parent, author, author_ref, created_at,
     content_sha256, content, status}`. `parent: null` = fork of the ORIGINAL;
     `parent: <version_id>` = child of that scholar's version (fork-of-fork, any depth).
   - `reviews.jsonl` — append-only ReviewEvents (from contracts_human_authority), hash-bound
     to `(target=version_id, hash=content_sha256)`.
   - `promotions.jsonl` — append-only PromotionEvents (`basis[]` = review ids).
   - `README.md` — the schema, kept beside the data.
3. **`tools/scholar.py`** CLI — `show · save · fork · log · signoff · promote · verify`.
   Every append recomputes hashes; `verify` re-derives every hash + fork link (fail-closed).
4. **Owner sign-off test** — first ReviewEvent + PromotionEvent + `signoff.json` on paramarthasara,
   Ed25519-signed (key outside the repo, mode 600).
5. **Gate** — `check.py` gains `scholar-valid` (hashes recompute, forks resolve, ids unique).
6. **`tools/emit_scholar.py`** — projects `scholar/` → `svread/data/scholar/<work>.json`.
7. **svread Scholar hub** — nav tab "Scholar" + `?view=scholar`, rendered by app.js with the
   EXACT existing functions (`$`/`esc`/`get`/`W`/`cleanEN`) and existing styles.css classes
   (`.widget`, `.wtable`, `.cmp-note`, `.col`, `.verbar`): layer browser per verse, version fork
   tree, edit + save (localStorage draft with parent = chosen base version), fork-of-fork.
8. Local gates: `node --check`, static smoke, `check.py` + `scholar verify`.
9. Deploy: `wrangler pages deploy .` + curl marker check (house rule: verify live after deploy).
10. Commit + push both repos.

## 6. Invariants (do not bend)

- **ReviewEvent never mutates its target.** Only PromotionEvent changes review status,
  and it names its `basis`.
- **Versions append, never overwrite.** Fork = new line with `parent`; no history rewrite
  (fast-forward only, same as OWNERS.md).
- **A signoff covers an exact content hash.** Edit after signoff ⇒ the signoff no longer
  matches that hash ⇒ review re-opens (existing `signoff.py` date rule + new hash rule).
- **MACHINE_DRAFT until a human signoff.** Browser drafts live in localStorage (`svv-…`)
  and are unpublished until saved through `scholar.py` into git.
- **Same styling/functions on the site.** The Scholar view is app.js code using the reader's
  own helpers and classes — no parallel design system.
