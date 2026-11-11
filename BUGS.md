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
