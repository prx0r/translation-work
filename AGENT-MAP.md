# AGENT-MAP — start here if you are a new agent in this stack

*2026-11-03. One page to navigate three repos + worker + the recent work (docs, schemas,
data hygiene, qprivately). Read this, then the file it points to for your task.*

## Agent entry points

- `python3 tools/agent_contract.py describe --include-instructions` returns the ordered
  layers, versioned structural schemas, both canonical skills and their standards, pinned examples,
  and hashes. Add `--layer l0` to focus on one datatype. Structural validation and
  cross-layer/source validation are separate, and the examples are not a human signoff.
  The generated schema release is pinned at `schemas/releases/2.0.0.json`; the gate
  rejects any drift from the registry, so changing the contract requires a new release.
- `python3 tools/agent_contract.py examples --layer l4 --work paramarthasara` indexes
  the existing data files, hashes and recorded proof gates; use `--offset` / `--limit`
  for pagination. They are candidates to inspect, not certified human-reviewed exemplars.
- `python3 tools/agent_contract.py validate --layer l3 --file <json>` validates layer
  objects. Run `tools/validate_song.py` and `check.py` for the wider invariants.
- `tools/intake.py` pins a new UTF-8 source and explicit complete byte spans. Run its
  `--help` before initializing a work. It prepares the source; it does not translate it.
- `tools/scholar.py import --file <export>` imports a Scholar draft chain as validated,
  content-addressed version files and an append-only ledger. Git commit and publication
  remain separate operations. C2 is song-scoped; legacy signoff hashes remain unchanged.
- `tools/scholar_service.py` accepts authenticated Scholar submissions and creates
  isolated Git branches. It binds to localhost and needs a private token file and an
  HTTPS reverse proxy. The optional remote push publishes a branch for review, not main.
- `tools/style_profile.py` prepares a private style brief from a scholar's own edits and
  recorded L0 choices. An explicitly authorized runner can turn a brief with at least
  three distinct examples into an agent-attributed draft. The brief stays local until
  that runner is invoked. `tools/style_runner_openai.py` is an optional configurable
  OpenAI-compatible runner; the operator chooses the provider and permitted model.
- Regression checks: `python3 -m unittest discover -s tests -p test_scholar_p0.py -v`.

## The three repos (and what lives where)

| Repo | What it is | Gate before push |
|---|---|---|
| **`prx0r/translation-work`** (this repo) | Canonical pipeline: SOURCE→T1→L0→ARGMAP→L2→C1→L3→L4→C2, per-work data, emitters, scholar versioning | `python3 check.py` → `CANONICAL: 0 failures` |
| **`prx0r/ipvv`** (`/root/ipvv`) | Site + display data + worker: `site/data/*` (emitted inputs), `site/dist/*` (built), `worker/` (ipvv-api) | `python3 tools/verify_site.py` → exit 0 |
| **`prx0r/svread`** (`/root/svread`) | The reader people actually use: https://svread.pages.dev (one HTML + app.js + vendored data, no build) | `node --check app.js` + browser smoke |

Test commands (all green 2026-11-03):
```bash
python3 check.py && python3 -m pytest tests/ -q          # this repo
cd ../ipvv && python3 -m pytest tests/ -q && node --test 'tests/*.test.mjs'   # NEVER: node --test tests/ (dir mode runs the .py too → false fail)
cd ../svread && node tests/scholar-smoke.cjs
```

Live: svread reader **https://svread.pages.dev** · data backend https://ipvv-a8u.pages.dev ·
worker https://ipvv-api.tradesprior.workers.dev · deploy with `CLOUDFLARE_API_TOKEN=$(cat /root/.cf-api-token) wrangler pages deploy …`.

## Read order (30 min)

1. `README.md` + `AGENTS.md` (this repo) — the gate, the stack table, lanes.
2. `SCHOLAR.md` — **the canonical doc for recent work**: versioned scholar edits, fork chains,
   ReviewEvents/Promotions, signoffs, BOTH hash schemes (do not interchange them), rights
   (translation = FREE, scholar words = (c)), storage division table.
3. `LAYERS.md` — layer contracts incl. §"Scholar versions" and L4 (Svatantrya = canonical).
4. `process/SCHOLAR-HUB-2026-11-03.md` — that session's history + invariants.
5. For the reader UI: `svread/SPEC.md` (lanes, Audio widget, Language/Style dropdown,
   side-by-side alignment, Scholar hub) + `svread/README.md`.

## DATA HYGIENE — which tool writes which site file (ownership; do not cross)

| File | Producer | Notes |
|---|---|---|
| `ipvv/site/data/translations/<w>.json` (emit-shaped: l1/l2/l3/l4, links) | `translation-work/tools/emit_site_general.py` | new intakes use pinned spans; Paramārthasāra and Kramastotra use audited source lines; other older works need a source audit; **refuses ingest-shaped files** (guard) |
| `ipvv/site/data/translations/tantrasara-a01.json` | same emitter (single-passage fallback) | locator `tsa01-p01` vs song `tsa-a01` handled |
| `ipvv/site/data/translations/sivastotravali.json` | `translation-work/tools/emit_site.py` | its own emitter (workcfg spans, immutable ids from passages) |
| `ipvv/site/data/translations/<ingest w>.json` (en_variants/ahnika/checks: ajadapramatrsiddhi, isvarasiddhi, sambandhasiddhi, tantrasara, vbt, tantraloka-aXX …) | `ipvv/tools/ingest_batch.py` from R2 `batch-t1/` | **never run emit_site_general on these** — it refuses (2026-11-03 lesson: a blanket re-emit reshaped 4 of them; 3 restored from git, tantrasara-a01 re-emitted + traced) |
| provenance fields (`source_file/source_license/source_origin`, `immutable_id`) | `ipvv/tools/trace_translations.py` (+ pass-through in emitters) | content-match + work-root + edition fallbacks; **re-run after any re-emit**; 3 SanskritDocuments works carry provenance-only licenses (no invented SPDX) |
| `ipvv/site/data/argmaps/**` | emitters, **preserve-on-write** (hand-written views never clobbered; `--force` to re-emit) | gates: `## ` header + ≥15w (terse structured renders legal) |
| `ipvv/site/data/c1/**` | emitters | gates: `.NOTE.md` = note (≥10w) · `**SUMMARY.**`/`*Rasa:` render = 15–450w · else essay 100–450w |
| `ipvv/site/data/r2audio-index.json` | `ipvv/tools/audio_r2_index.py` | mp3s live in R2 (`svread-audio`), never git; verify checks local OR index |
| `svread/data/*.json` | copy of `ipvv/site/dist/data/layers/<w>.json` (re-vendor after rebuild) | reader fetches ipvv live first, vendored = fallback |
| `svread/data/scholar/*` | `translation-work/tools/emit_scholar.py` | disposable projection of `scholar/` ledgers |
| `svread/data/styles.json` | hand-maintained | C2 style registry for the Style dropdown |

**The release train:** fix upstream → emit (preserves!) → trace (if provenance changed) →
`python3 site/build.py` (FULL: receipts run AFTER arguments) → `verify_site.py` exit 0 →
deploy ipvv → re-vendor svread data → `node --check` + browser smoke → deploy svread → push all.

## SCHEMAS + QPRIVATELY (the audit machinery)

- **Schemas**: `translation-work/schemas/*.py` (t1/l0/argmap/l2/c1/l200/l3/l4/signoff/suggestion)
  driven by `stack.json` (v1.3.0). ipvv display contract: `ipvv/specs/schema/site-item.json`.
- **qp kernel**: `ipvv/tools/qp_acom/` (vendored prx0r/qprivately, `acom/0.1`) —
  `transition()` receipts with **merkle evidence roots**, content-derived ids, Ed25519
  `sign_receipt` (signatures still unwired), `store.py`/`versions.py` present but dormant.
- **Project gates**: `ipvv/tools/qp_gates.py` (6 gates, program hashes pinned in verify —
  new logic = new gate id, never edit in place).
- **Receipts**: `ipvv/site/dist/data/receipts.jsonl` (2280): every chunk + argument packet;
  `verify_site §6b` recomputes every id from canonical bytes (tamper = commit blocked) and
  pins gate program hashes (registry rot = blocked).
- **Human authority** (scholar review): `translation-work/tools/human_authority/` —
  vendored patalacheckpoints `ReviewEvent/Adjudication/PromotionEvent` + `review_engine`
  (23/23) + `goldchain/philproof` (40/40) + `ed25519`. Reviewed by `scholar-valid` step in
  `check.py` (recomputes every version id/hash/fork link; stale signoff = WARN not FAIL).
- **Hash rules**: `SCHOLAR.md §3` — Scheme A (compact canon, versions/ids) vs Scheme B
  (default-separator contract_sha, ReviewEvent/Promotion hashes). Interchanging them is the
  one way to fail `scholar-valid` on untampered data.

## Recent work index (2026-11-03, in order)

1. Scholar versioning endgame: `SCHOLAR.md` + `tools/scholar.py` + `paramarthasara/scholar/`
   ledgers + first signed signoff + `scholar-valid` gate.
2. `tools/human_authority/` vendored (63/63 checks) + `ed25519`.
3. L4 (Svatantrya) shipped end-to-end: emit→layers→svread default column; `license: FREE`
   on every translation chunk; Work ID = source edition; rights block (FREE vs (c)).
4. Data hygiene: provenance trace (1143/1143), receipts-after-arguments (parity), C1/argmap
   gates re-scoped to real artifacts, mp3s vs R2 index, per-verse Sanskrit, emitter ownership
   guards, hand-argmap preservation.
5. svread: side-by-side row alignment (105/105), "English translation" rename, Language/Style
   dropdown (styles = C2), Scholar hub (`?view=scholar`), Audio widget + read sanskrit/english
   via `POST /api/read` (fish `s2.1-pro-free` $0; voices: Sanskrit `4e873c37…` / Granny
   `614f8afd…`), stored verse-by-verse in R2 `read/<work>/<verse>_<lang>.mp3`.

## Rules that don't bend

1. T1 frozen; BLOCKED = no English anywhere; fail-closed display.
2. Append-only everywhere it's a ledger (scholar/, receipts, argmap views) — corrections are
   new lines. Never `--force` push; `git pull --rebase` first.
3. Keys never in git: `~/.scholar/key`, `/root/.fish-env`, `.r2-env`, CF token.
4. Free tiers only: fish header `model: s2.1-pro-free`, CF workers free models.
5. Verify before push in BOTH repos; deploy only after exit 0; curl markers after every deploy.
