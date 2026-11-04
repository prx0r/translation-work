# IPVV-IMPORT — flag for the translation-work lane (pick this up here)

**From:** svread/endgame lane, 2026-11-05 (autonomous import, owner-directed).
**To:** the agents working translation-work (the gold batch / HANDOVER-G owners).
**What:** every available IPVV byte pulled off R2 into this repo as a canonical
work directory (`ipvv/`), honestly unprovenanced-where-not-proven, with exact
recipes for everything that remains. **Nothing here is theater: no proof was
hand-written, no gate flipped, no layer faked.**

---

## 1. TL;DR

`ipvv/` now looks like every other work here: `passages.jsonl` (49 chunks),
`T1-*.md` (49 frozen T1 files), `T1-*.l0.report.txt` (35), `data/*.l2.json` (49),
`GATE.json` (all `BLOCKED / PROOF_NOT_RUN`), `proof/README.md` (the recipe),
`STATUS.json` (hashes + provenance), `pilot/` (109 files), `published/` (49
bundles + CL-3 themes), `artifacts/` (20 R2 process docs), `t1-detail/` (14
sub-chunk T1s). 12 MB total. The moment proofs PASS per chunk, run
`emit_scholar --work ipvv` and the Scholar hub lights up with editable
originals — same as paramarthasara.

## 2. What was pulled (complete source inventory)

| Source | What | Where now |
|---|---|---|
| R2 `sanskritree/ipvv-translations/` (229 files, 153.6 MB) | t1-vol1 (28 md), t1-golden (35 md), pilot/ (49 L2 reads + 49 argument maps + apparatus), l0/ (audit + 35 reports + **2 tarballs**), artifacts/ + process docs (README, CALIBRATION_REPORT, IPVV_STALL_LOG, IPVV_FREESTYLE_LESSONS, IPVV_PROCESS_NEXT_STEPS, IPVV_MANIFEST, CHUNK_MAP_VOL3, VOL3_MINED_TRANSLATIONS) | md → `ipvv/T1-*.md`, `ipvv/t1-detail/`, `ipvv/pilot/`, `ipvv/artifacts/`; reports → `ipvv/T1-*.l0.report.txt`; **tarballs NOT copied into git** (hashes in STATUS.json, staging at `/root/ipvv-r2-staging/l0/`) |
| R2 `patala/public/published/ipvv/` (57 files, 2.5 MB) | 49 published passage bundles (source byte-spans, l2_text, c1, argmap pointers) + CL-3 themes (clusters, adjudication, goldchain, essay-cl3, index) | `ipvv/published/` |
| R2 `uploads …/t1-batches/ipvv-*.jsonl` (2 files) | legacy T1 batch exports | staging only (reference in STATUS) |
| `/root/ipvv/works/ipvv/` (crown build) | passages.jsonl (49), work.json (counts: T1 63 · L0 102,157 · ARGMAP · L1 · L2 49 · C1 49 · published 49), WORK.md | copied into `ipvv/` with import header |
| **Source text (already local!)** | `ipvv/site/data/sanskrit/ipvv-vol1/2/3.txt` (M00020/21/22, 553/787/733 KB) + `ipk.txt` (Torella) — **sha256 recorded in STATUS.json** | untouched in the ipvv repo |

Bundle sha256s for both l0 tarballs are in `ipvv/STATUS.json` (`r2.l0_v1`,
`r2.l0_full`). Bundle chunk ids carry a `.md` suffix (`chunkA-svatyandya.md`);
canonical target = `chunk_id` **without** suffix (matches passages.jsonl and
`IDENT` regex) — normalized in all data filenames; normalize in any future tool. Passage `locator` is normalized to chunk_id (tw/lingua/Scholar convention); the crown's `M00020 chunk….md` value is preserved as `source_locator`, and `verses` carries `<vol>:<line_start>-<line_end>`.

## 3. What is NOT done (in order, with recipes)

1. **PROOFS (the gate to everything).** `proof/README.md` has the full recipe.
   Short version: per-chunk byte spans already exist inside
   `published/pt-passage-*.json` (`source.start/end/text`, `vol` = M00020/21/22)
   → run `tools/intake.py` per volume against the on-disk source files → add an
   `ipvv` entry to `tools/workcfg.py` (source, `song_verses`, `source_spans`,
   song = chunk id) → `python3 tools/proof_record.py --song <chunk> --work ipvv`.
   **Do not hand-write PASS records.** Until then emit correctly withholds all 49.
2. **L0 contract conversion.** R2 tarballs are crown-build *line-level* rows
   (`{id, chunk_id, line_id, source_text, literal_gloss, …}`), not the contract
   token rows (`{id, verse_id, pada_index, surface, citation, options, chosen_index}`).
   Both tarballs are staged (not in git — 150 MB; hashes in STATUS). Convert
   into `data/<chunk>.l0.json` + root `T1-<chunk>.l0.jsonl`, and regenerate the
   **14 missing vol1 reports** (we have 35/49). `L0_EXTRACTION_AUDIT.md` in
   `artifacts/` is the crown build's own audit of this layer.
3. **T1 row conversion.** The 49 frozen T1 markdown files (prose-gloss reading
   docs, "max-effort T1") are not contract token rows. Same job the F2 audit
   flagged for other works: either convert honestly or rename the stage.
   `t1-detail/` holds the 14 sub-chunk k-files (k1.1–k11) — finer granularity
   than the 49 passages; keep them as material unless you re-chunk.
4. **source_verses / reader evidence.** The site file `site/data/translations/
   ipvv.json` does **not** exist (your own WORK.md "READ site" item). Until it
   or a workcfg display path exists, `emit_scholar` produces empty
   `source_verses` even post-proof — MCP `passage_evidence` needs both
   `source_verses[target]` and `originals.t1[target]`. Plan: intake manifest +
   workcfg spans also feed the display path (see emit `displayed_sources`).
5. **c1 + argmap as canonical data.** Bundles have c1 49/49 (site shape
   `{body, terms, see_also, verse_commentary}` — different from the canonical
   `{song, essence, essence_source, renders, rasa}` contract) and argmap
   pointers 10/49 → files in `pilot/`. Both need conversion decisions (their
   lane); we did NOT transcribe them into `data/` (would be shape theater).
   `site/data/argmaps/` has **no ipvv dir** — pilot argument maps are the only
   argmap material.
6. **L2 provenance label.** `data/*.l2.json` rows are mechanical transcriptions
   of each bundle's `l2_text` (the pilot L2 reads, 49/49, status `OK` in the
   patala published set). Label them at proof time the way you label staged
   English; the crown build counts pilot L2 as its L2 layer (work.json L2: 49).

## 4. Everything else available for this work (the surrounding estate)

- **sanskritbench**: 49 IPVV gold exemplars already in the bench
  (`sanskrit_gold.py` IPVV set) + proof gate + COMET/chrF meta-eval — link
  ipvv proofs to bench runs when they exist (master sequence step 2).
- **Pushing (cruxes):** 14 IPVV records in the svread pushing catalog
  (`ipvv/*` sessions: felt-to-ground, buddhist-co-opting, MEMORY, grace,
  internal-arc, method-opponents…) + `research-library/recognition/pushing-ipvv/`
  + `ipvv/site/data/pushing/ipvv/`. ARGMAP + pushing = the argument layer.
- **Essays:** the 22 IPVV essays (site + R2 archive) cite this text.
- **Themes:** CL-3 clusters/adjudication/goldchain/essay-cl3 in `published/`.
- **openpatala registration:** `ipvv` is absent from its translation-availability
  (it knows tantrasara/paramarthasara/tantraloka only) — register it when
  bridging (master sequence step 1).
- **Endgame docs:** `svread/ENDGAME-BUILD-PLAN.md` §0 master sequence — step 3
  is "IPVV + TĀ fully translated and sanskritbenched", i.e. this work's
  end-state; `svread/RESOURCES.md` for the full map.

## 5. Recommended order for you (matches your HANDOVER-G pattern)

1. intake source spans (three volumes, 49 segments) + workcfg entry.
2. L0 contract conversion + vol1 reports (prove one chunk end-to-end first).
3. `proof_record --work ipvv` per chunk → PASS records accumulate.
4. `emit_scholar --work ipvv` → projection + index → hub shows originals;
   Scholar translation drafts/L3/L4 edits become possible (base hashes from
   originals).
5. Then L3/L4 additions like any other work (`data/<chunk>.l3.json` +
   proof + emit) — the structure for it is already here.
6. c1/argmap canonical conversions + site `translations/ipvv.json` display.
