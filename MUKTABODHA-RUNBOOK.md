# MUKTABODHA RUNBOOK — from here to "all 499 minimal done"

*The single operating doc. Supersedes NEXT-PLAN.md, PROCESS.md's step lists,
and the handoff notes. If a command isn't here, it either doesn't exist or
shouldn't be used. Last update 2026-11-11 (post-largetext re-read).*

## 0. The goal and the definition of done

**Goal:** every in-realm Muktabodha work at **minimal gold** (pass 1):
T1 + L0 + argmap + L2 + C1-essence, `validate_song` 0 errors,
`proof_record` PASS, STATUS says "minimal gold complete; L3/L4 waived".

**DO NOT** aim for full gold yet. Pass 2 (knowledge core) and pass 3 (L3/L4/
C2) come later per work.

## 1. Where truth lives (never invent a second copy)

| Concern | Source of truth |
|---|---|
| Work status | `tools/work_state.py` (dirs + STATUS.json, **alias registry first**) |
| Canonical dir for a catalog | `process/beam/work_aliases.json` |
| Burn order | `process/beam/ranked_burn.json` (T asc, verses asc, prose tail) |
| Queue | `process/beam/queue.json` (+ `tools/queue_guard.py` before seeding) |
| Translation evidence | `process/beam/{deepfind,curated_hits,seed_evidence,batch6}`, DB `translations` |
| Traditions | `process/beam/muktabodha_authority_traditions.json` (verbatim source doc alongside) |
| Lore (per work) | `process/beam/lore/<work>.md` (brief) + `lore/<work>-knowledge-core.md` (scholarship) |
| Original texts | `/tmp/mukta/MUKTABODHA-LIBRARY-IAST/` (re-download from muktalib7 if gone) |

## 2. The loop (largetext procedure — this is the only sanctioned path)

1. **Onboard** (once/work): `tools/onboard_wave.py --n N --min-verses 3`
   → source intake (edition/segments/manifest), passages, STATUS,
   auto-brief, auto_burn launch. Refuses aliased catalogs.
2. **Brief**: process/beam/lore/<work>.md (WHAT IT IS / MOVES / TRAPS /
   APPROACH / LEDGER). Pass-2 upgrade: knowledge core from web scholarship.
   **Both are auto-injected into every beam packet.**
3. **T1**: labeled verses ≤25/call → `tools/spanda_t1_parse.py --work --song`
   → coverage gate difflib ≥0.85 (below = retry with labeled input).
4. **Seed**: 12-verse `tal_triple` groups (never >60; skill window rule).
5. **Drain**: 3 workers via `tools/beam_swarm.py worker wN` (or the button
   below). Dual-account key rotation; 429 → other account → park 30 min.
6. **Assemble**: `shastra.assemble` (MCP) or `tools/assemble_all.py`
   (sweeps completed songs). Runs build_l0 → tal_stage → validate → proof.
7. **Close**: STATUS.json "minimal gold complete", then `work_state` sees it.

## 3. THE BUTTONS (don't hand-run anything else)

```bash
bash tools/continue.sh once                # one supervised pass
setsid nohup bash tools/continue.sh > process/beam/continue.log 2>&1 < /dev/null &
setsid nohup bash tools/ralph.sh 240 180 > process/beam/ralph.log 2>&1 < /dev/null &
shastra_supervise                          # state of the loop (MCP)
```
ralph = autonomous supervisor: keeps workers, auto-reviews window briefs,
converts approved pilots, **gates every commit on check.py, pushes on green,
holds on red**. If ralph says `validate_all FAILED — holding`, that is the
assessor's cue, not a bug.

## 4. Known failure classes → fix (all verified)

| Class | Fix |
|---|---|
| question rejected (generic) | prompt contract ≥8 words, names the claim (done in TAL_TRIPLE_SYS) |
| surface drift | `norm_surface` strips `+`/spaces (done) |
| premise too short | halve group; 12v is the proven size |
| coverage 0.81–0.82 | retry that passage with labeled verses; never ship |
| 429 on both models | wait; check `model_health.json`; both accounts rotate |
| triple split overwrite | fixed: unique child ids + merged parent |
| duplicate seeds | `queue_guard` + seeder overlap check |

## 5. Assembly invariants (hard-won — see BUGS.md)

- `data/t1` tokens carry `sanskrit/surface/iast/gloss/quick_gloss` (union).
- Sandhi `+` merges to ONE source word.
- Citations = source verse text (never token joins).
- `sanskrit_sha` = **song-scoped** digest (validate_song line 64).
- Verse ids unpadded everywhere.
- `build_l0` needs `working-l0` (from CM runs) and song-scoped spans.

## 6. Chunking like Tantrasāra (the answer)

Tantrasāra gold = songs per āhnika with **chapter.verse** ranges from a
numbered source. Our tantra e-texts carry no usable chapter markers
(verified) → regex rechunk is a dead end. **Do:** take a numbered source
(GRETIL `SvaT_x.y` works for Svacchanda) or a curated chapter table
(Avalon's 17 ullāsas; OCHS 22 adhikāras), verify Σverses == count, then
rewrite passages to `chNN` songs with in-chapter sub-passages. Until then
the 25v grid is honest. **Open question with evidence: our Svacchanda
witness (1,385 v) is ~1/3 of GRETIL's (3,677) — check abridgement before
translating more of it.**

## 7. What remains until 499 minimal (the actual backlog)

1. **Queue drain**: 225 pending triples → assemble_all closes songs → PASS.
2. **Coverage retries**: ~20 passages at 0.81–0.82 (labeled-verse redo).
3. **Wave onboarding**: 430 not_started works, shortest-first, in batches of
   10–15 (`onboard_wave.py`); gate: min 3 verses (1-verse files = markup
   problem, not tiny texts).
4. **Prose track**: 90 zero-verse works need a chunker (separate; verse
   pipeline cannot eat them).
5. **Chapter tables** for the three big tantras (§6).
6. **Evidence merge**: batch6 rows already in DB (451 translations); new
   external research → same merge path.
7. **Dating**: scholarly assertions for researched works; PANDiT floruits
   still pending (adapter exists, needs live fetch).

## 8. Monitoring (one line each)

```bash
python3 tools/work_state.py --all | head           # work statuses
shastra.swarm_status                               # queue + workers
tail -f process/beam/ralph.log                     # loop + gate holds
tail -f /root/assemble_all.log                     # assembly sweep
python3 tools/queue_guard.py                       # duplicate check
```

## 9. Non-negotiables

- DONE = machine-translated; human review never blocks; no agent pushes.
- Free models only. Key from vault/`.env` (never in git).
- One work status source. Aliases before titles. Guard before seeding.
- Beam proposes; the assessor owns PASS. largetext boundary (§0 of skill).
