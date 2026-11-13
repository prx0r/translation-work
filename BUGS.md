> **STATUS 2026-11-11:** steps/commands live in MUKTABODHA-RUNBOOK.md. This file supplies detail/reasoning only; runbook wins on procedure.

# BUGS — root causes and permanent fixes (2026-11-11)

*Every entry = symptom → root cause → fix → the rule that prevents it.
These are binding for all agents; PROCESS.md carries the rules.*

## 1. Duplicate translation work (VB burned twice)
**Symptom:** `vijnanabhairava` onboarded and 50 verses drafted while `vbt`
already held the finished 162-verse/136-data-file work.
**Root:** status by dirname/title similarity — abbreviations (`vbt`) never
match long titles.
**Fix:** `process/beam/work_aliases.json` (catalog → canonical dir) consulted
FIRST by `tools/work_state.py`; `onboard_wave.py` refuses aliased catalogs.
**Rule:** *No work status may live outside `work_state.py`; no derived JSON
carries a status copy. Aliases win over titles.*

## 2. Duplicate triple tasks in the queue
**Symptom:** 21 overlapping verse ranges per song (`-retry1` twins,
recursive-split parents).
**Root:** seeding had no range awareness.
**Fix:** `tools/queue_guard.py` (MCP `shastra.queue_guard`) + the seeder
refuses any group overlapping a live task.
**Rule:** *Every seeding path must pass the overlap guard.*

## 3. Data/t1 emitted in working shape → 90+ cross-layer errors
**Symptom:** `l0.chosen != T1.quick_gloss None`.
**Root:** `tal_stage` wrote working-t1 verbatim; the schema wants
`sanskrit/iast/gloss/status`, while downstream tools read `surface` /
`quick_gloss`.
**Fix:** emit all aliases (`sanskrit`, `surface`, `iast`, `gloss`,
`quick_gloss`) in one token record; merge `+` sandhi splits into one token
per source word.
**Rule:** *Emitter = union of every consumer's key contract. Never emit a
working format as a schema format.*

## 4. L2 citation byte-exact failures
**Symptom:** `L2_CITE_FAIL` on `tasya+śravaṇamātreṇa…`.
**Root:** citations built from token joins (carry `+`, `|` differences).
**Fix:** citation = canonical source verse text, pipe-normalised
(`' '.join(text.replace('|',' ').split())`).
**Rule:** *Citations come from the source, never from token streams.*

## 5. `sanskrit_sha` mismatch (25 errors, 4 wrong guesses)
**Symptom:** `argmap[...]: sanskrit_sha mismatch`.
**Root:** convention is **song-scoped**:
`sha(' '.join(' '.join(spans[v]) for v in song_verses))`. I assumed
per-verse, then whole-work.
**Fix:** `tal_stage._src_sha` computes the song-scoped digest once.
**Rule:** *Read the validator's own computation before mirroring a digest.*

## 6. Verse-id padding mismatch
**Symptom:** `kul-p01-v9` (working) vs `kul-p01-v09` (build_l0).
**Fix:** ids are unpadded everywhere; format only for display.
**Rule:** *One id format, set by the earliest producer.*

## 7. T1 coverage gate refusals (0.81–0.82)
**Root:** drafting drifts on long compound verses.
**Fix (in place):** gate refuses to seed; retry with labeled verses.
**Status:** known-open for the ~20 affected passages.

## 8. Single-source-of-truth violation (audit/ranking copies)
**Symptom:** ranker offered finished works as candidates.
**Root:** three derived JSONs carried `status`/`tw` copies I had written.
**Fix:** copies deleted; ranker imports `work_state` live.
**Rule:** *Derived data may reference status, never copy it.*

## 9. Openpatala rows/ids (ingest edge cases)
**Symptom:** `mukta-` empty id (blank catalogue number in filename);
site_url written onto parent anthology rows.
**Fix:** renamed `mukta-unknown-saundaryalahari` w/ children retargeted;
site_url canonical only where `work_id == slug`.
**Rule:** *FK children move first; URL ownership = one work per slug.*

## 10. MCP/tal_stage proof ignored recorded dispositions (2026-11-13)
**Symptom:** songs with verified sandhi-only dispositions (tools/proof-disp.json)
stayed BLOCKED, and cloud promotions could not clear them.
**Root:** `mcp_server.validate/promote` and `tools/tal_stage.py` called
`proof_record.py --shastra` without `--disp`.
**Fix:** both paths now pass `--disp tools/proof-disp.json` when present
(`_proof_cmd` in mcp_server; inline disp in tal_stage). Kularnava 42→60 gold.
**Rule:** *one proof invocation; dispositions always honoured.*

## 11. Beam T1 duplicate/overlapping surfaces (2026-11-13)
**Symptom:** T1 token runs repeated a compound and its tail
(`ājñāsiddhirbhavettasya` / `bhavettasya` / `tasya`), and working-t1 carried
duplicate verse entries; align ratio dropped to 0.4–0.8 and DATA_OBJECTS failed.
**Root:** legacy-hint draft rows + chunk overlap, faithfully merged.
**Fix:** `tools/dedup_t1.py` (count-preserving suffix de-overlap) +
`tools/collapse_dups.py` (adjacent IDENTICAL repeats, L0 renumber + l0_id
pruning, count-changing but layer-consistent) + working-t1 duplicate-verse
dedupe. Kularnava + kjn restored to PASS; all false "sandhi" dispositions
for duplicated verses removed and regenerated from the true post-fix ratios.
**Rule:** *de-overlap at merge; one verse entry per working-t1.*

## 12. Svacchanda/Netra T1 carries non-source tokens (OPEN)
**Symptom:** T1 surfaces include gloss words and paren variants
(`p08 v176` appends `parikalpanā anuṣaṅga`; `sva-p37` repeats one word ×4;
`net-p17` has `sphī(sthī` truncated). L2_CITE_FAIL + ALIGN_NODISP.
**Root:** intake/drafting added explanatory tokens to the surface stream and
split paren-variant words mid-token. Not dispositable — the concatenation does
not equal source.
**Status:** OPEN — both fronts stay BLOCKED pending a proper T1 re-intake
(strip non-source tokens, resolve paren variants, one entry per verse).
`tools/dedup_t1.py` cannot fix addition or identical-token repetition.

## 13. Onboarding could never start (chicken-and-egg) (2026-11-13)
**Symptom:** `onboard_wave.py` called `brief_gate.check` BEFORE writing the
brief, so every brand-new catalog raised "write a researched brief first" and
no new work could enter the autonomous pipeline.
**Fix:** `gen_briefs.ensure(work)` now writes a grounded brief (bibliography +
tradition doctrine) before the gate check; `onboard_wave` calls it. Verified by
onboarding 8 tiny untranslated works end-to-end (T1 → seed). `gen_briefs.py`
also backfilled 102 per-work briefs for all `mukta-m*` fronts.
**Rule:** *supply the brief first, then gate — never gate a work that has no
brief yet.*

## 14. T1 kept paratext tokens that CM dropped (assemble crash) (2026-11-13)
**Symptom:** `build_l0` asserted `CM n != T1 n` and crashed the whole song on
verses with editorial tokens (`karata(?`) or variant parentheses (`tasmi(n`).
**Root:** `tal_stage.stage_assemble` filtered `is_paratext` from CM rows but not
from the T1 token stream; the T1 schema also forbids parens in surfaces.
**Fix:** stage_assemble now (a) drops `is_paratext` tokens from T1 with the SAME
predicate used for CM, and (b) deparens residual variant surfaces (and the
matching CM lemma) so surface equality holds. kjn-p16 assembled PASS.
**Rule:** *T1 and CM are filtered by one predicate; never diverge the two streams.*

## 15. assemble_all retried permanently-blocked songs forever (2026-11-13)
**Symptom:** sva-p50 / kjn-p16 re-attempted every round with no data written.
**Fix:** attempt counter in `/root/assemble_all.fails.json`, skip after
`--max-fails` (default 3); cleared on success. Plus tal_stage now runs
dedup_t1 + collapse_dups before validate/proof so assembled songs are clean.

### Repair plan for #12 (svacchandatantra / netratantra) — not yet executed
These fronts are not dispositionable: T1 concat ≠ source. Repair = controlled
re-intake per affected song: (1) align T1 tokens to `workcfg.source_spans`
with `tools/align_check.align`; (2) drop tokens that do not map (gloss-words
like `parikalpanā`, `anuṣaṅga`) and deparen truncated variants; (3) collapse
identical repeats (`collapse_dups`); (4) rebuild L0 from CM, remap argmap/L2
`l0_ids`; (5) re-proof. Until then they stay BLOCKED and `assemble_all` skips
after the retry cap. Cheap alternative: re-`auto_burn` the song from source
(fresh T1) once a stricter draft prompt is in place.

## 16. Queue clobbering by un-locked writers (2026-11-13)
**Symptom:** retired/superseded tasks reappeared as pending; the SAME task was
claimed by two workers; throughput was near zero (stale snapshots overwriting
worker claims).
**Root:** `auto_burn.save_queue` (tw-wave), `recycle_failed.py`, and
`registry_sync --seed` all did `json.load` → mutate → `json.dump` on
`queue.json` WITHOUT the shared lock used by `beam_swarm.queue_update`. A long
beam call in auto_burn then wrote a stale whole-queue snapshot over concurrent
worker edits.
**Fix:** all three now mutate through `beam_swarm.queue_update` (file-locked,
fresh read, immediate write). `auto_burn.seed_locked()` re-reads at seed time.
**Rule:** *one writer discipline for queue.json — always queue_update.*
