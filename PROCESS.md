# PROCESS — the translation pipeline (canonical, 2026-11-11)

*Owner directive: reach FULL gold in passes. Never block pass 1 on pass 3.*
*DONE = machine-translated. Free beam only. Beam never writes data/.*

## Pass model

| Pass | Scope | Gate to advance |
|---|---|---|
| **1 MINIMAL (default)** | onboard → T1 → 12v triples → assemble → validate | `validate_song` PASS, `next` = "minimal gold complete; L3/L4 waived" |
| **2 REVIEW + CORE** | read output; web-search → knowledge core (IPVV-style) or lore brief | core file in `lore/` + STATUS updated |
| **3 FULL GOLD** | C1 depth, L3, L4, C2 renders | full layer set + human spot-check |

## Pass 1 mechanics (exact steps, all runnable by an agent)

1. **Source intake** (once per work): `source/edition.txt` (verses joined by
   `\n\n`), `source/segments.json` (`{song, verse, verse_id, start, end}`
   byte offsets, songs = 25-verse passages), `source/manifest.json`
   (`format: source-intake/1`, sha256 of both). Validate with
   `tools/intake.py::validate_segments`. This auto-registers the work in
   `workcfg.source_spans` — required by build_l0/tal_stage.
2. **Lore brief** (required before seeding): `process/beam/lore/<work>.md`
   (WHAT IT IS / MOVES / TRAPS / APPROACH + ledger). Unbriefed seeds
   degenerate. Optional pass-2 upgrade: full knowledge core.
3. **T1** — labeled verses only, max 25/call: pre-split verses with fixed
   numbers, ask for `[gloss](surface +split)` per pada. Then
   `tools/spanda_t1_parse.py --work <w> --song <s>` → `working-t1-<song>.json`
   + **coverage gate** difflib ≥ 0.85 per verse; below gate = redo with
   labeled input (never ship).
4. **Seed** `tal_triple` tasks, **≤12 verses per group** (25v groups bounce
   review: "premise too short"). Append to `process/beam/queue.json`.
5. **Drain** — workers (`tools/beam_swarm.py worker wN`, max 3) on
   `beam-free`/`iceman`, dual-account rotation; 429 → other account →
   park model 30 min only if both.
6. **Assemble** — `build_l0.py --work <w> --cm <cm-dict>` (CM rows →
   working-l0) then `tal_stage.py` assemble → `data/*.json` + validate_song
   + proof_record. Fix `working-l0-<song>.json` gaps by converting
   `runs/<song>-cm-vNN/cm.json` rows to the `{verse:[[lemma,morph,grounds]]}`
   shape.
7. **Close** — `STATUS.json`: `next` = "minimal gold complete; L3/L4 waived;
   human review pending", counts from validate. `work_state.py` then
   resolves it as machine-complete (the ONLY status source).

## Hard rules

- **Single status source**: `tools/work_state.py` (dir + STATUS.json).
  Never copy status into derived JSON (that caused redoing finished work).
- **Coverage gate** on every T1 batch; labeled verses only; never renumber.
- **12-verse seeds**; halve any failing group; triple-split merger is fixed
  (unique child ids + merged parent).
- **Realm**: Hindu/Śaiva/Śākta/Trika/Krama/Kaula/Siddhānta; Buddhist
  (Mantranaya) excluded from burn, kept in catalogue.
- **Traditions**: authority = Muktabodha browse pages
  (`muktabodha-traditions-verbatim.md` / `_authority_traditions.json`),
  never keyword guesses where authority speaks.
- No pushes by agents; owner merges PR #18.

## Evidence / discovery layer

- `deepfind*.jsonl` — OpenLibrary/archive/Wisdomlib hits (T counts).
- `curated_hits.jsonl` — Magee/Dyczkowski/Wallis/Pradīpaka indexes.
- `seed_evidence.json` — bibliographySeed verified pairs (URLs).
- `ranked_burn.json` — burn order (T asc, verses asc, prose tail).
- Manual research: `burn_research.csv` + `RESEARCH-BRIEF.md` (print/Hindi/
  thesis layers) — merge on `catalog`.

## Root rules learned the hard way (see BUGS.md for each)

1. Status lives ONLY in `work_state.py`; aliases (work_aliases.json) beat
   title matching; derived JSON references status, never copies it.
2. Every seeding path passes `queue_guard` (id uniqueness + range overlap).
3. Emit data objects as the UNION of consumer key contracts
   (`sanskrit/surface/iast/gloss/quick_gloss`); merge `+` splits to source
   words.
4. Citations come from the source text, never from token streams.
5. Digests mirror the validator's own computation — read it first
   (sanskrit_sha is SONG-scoped).
6. One id format (unpadded) from earliest producer.
7. FK children move before parents; one owner per site slug.
