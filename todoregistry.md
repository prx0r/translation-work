# TODOREGISTRY — current state + todos for the next agent

*Created 2026-11-04. This file and REGISTRY.json are the two entry points:
REGISTRY.json = per-work truth (notes, counts, status); this file = the live
queue + the canonical checklist. Read both, plus AGENTS.md, skills/crystal-ipvv/
SKILL.md + EXAMPLES.md + FINAL-PROCESS.md + crystal.md + mistakes.md (all read
and re-verified 2026-11-04 — see CANONICAL CHECKLIST below). When todos change,
edit THIS file in the same commit — never leave it behind.*

## State snapshot (verified 2026-11-04, all committed)

- **30 gold works**, each with T1/L0/argmap/L2/C1/L3 + L4 song +
  C2 (eli5+genz, [E#]-tagged) + refreshed proofs (layer_sha256 over L3/L4/C2).
- **Gate green on all 30 golds at completion**: `python3 check.py --work <name>` CANONICAL on all
  30 (defaults to sivastotravali — loop it when auditing).
- **REGISTRY.json**: 92 works / 30 gold / 62 pending.
- **DONE 2026-11-04**: stavacintamani GOLD #22 COMPLETE — T1 120v span-exact
  (incl. v1 maṅgala proposal stav-p00) + L0 1338 tok 100% PARSED (M00089
  collation: all AMBIGUOUS resolved incl. v37 māmi shine-forth) + argmaps 120v
  (verse-specific lore, all forks adjudicated, 0 shared) + L2 rasa-carried
  traced cited + C1 essence + SUMMARY + rasa (0 quotes/meta/shared) + L3
  handcrafted couplets read aloud + L4 120/120 sung verse-by-verse with
  craft_notes + rejected-with-killers (all 120 DRAFTs on file, data==DRAFTs,
  all differ from L3; owner verdicts applied: pity→compassion,
  laud-gem/gravid→wish-jewel/fortune-house, waking→awakening; trust gradient:
  Sanskrit first, nearer layers win) + C1 NOTEs + C2 eli5+genz tagged+merged.
  All validated + proofs PASS x13 + check.py CANONICAL 0 failures.
  Open: v1 source decision (fetch M00089 print + byte-verify, or formal
  deferral; prepend p00 vs extend p01), first-verse L4 voice verdict (owner),
  human review (machine-proposed throughout).
- **Next**: 7 small standalone legacy works (queue §2 below, smallest first).

## Queue order (immediate → deferred)

1. **stavacintamani — DONE → gold #22** (all 25 todos below complete;
   L4 sung meticulously v01–v120; C2 in place, owner may still defer/redo it).
2. **Small standalone legacy works, smallest first** — each = full transform
   (FINAL-PROCESS §how-to-transform, 14 steps) → L3 handcraft → L4 → C2:
   1. saktavijnana (~30v, 3 passages) — DONE → gold #23 (full pipeline, L4 sung v01–v30, C2 in place; first-verse voice verdict outstanding)
   2. svabodhasiddhi (~32v, 4 passages) — DONE → gold #24 (full pipeline, L4 sung v01–v33, C2 in place; first-verse voice verdict outstanding)
   3. paratrimshika (~35v, 4 passages) — DONE → gold #25 (full pipeline, L4 sung v01–v36, C2 in place; first-verse voice verdict outstanding)
   4. ptvmadhyama (35v) — DONE → gold #26 (M00044 mula recension rebuilt from markers; full pipeline; first-verse voice verdict outstanding)
   5. spanda — DONE → gold #27 (first nihsyanda vv1-25 only; legacy garbled ranges superseded; later nihsyandas out of scope)
   6. sivasutra (~80 sutras, 8 passages, 1.x-3.x numbering) — DONE → gold #28 (75 sutras Kaul Shastri recension; full pipeline; first-verse verdict outstanding)
    7. vbt — DONE → gold #29 (2026-11-04): T1/L0/argmap/L2/C1/L3 162/162 + L4 162/162 DRAFTs (craft_notes+rejected-killers+reads_against) + data t1/l0/argmap/l2/c1/l3/l4 x17 + C2 eli5+genz full coverage + c1.NOTE x17; validate 0 x17, proof PASS x17, roundtrip 0 x17, check.py CANONICAL 0 failures, qa NEEDS_WITNESS. Discipline events: L3-data emit omission found by gate (28 failures, fixed); p13-p14 L4 memory-composed at 0 L3-overlap, caught by audit, RE-SUNG from true L3 (mistakes.md #19). OPEN: first-verse L4 voice verdict (owner); human review (machine-proposed).
3. **tantrasara-a03–a22** (20) — same pattern, proven twice (a01/a02 gold).
4. **tantraloka-a01–a37** (37) — the big campaign.
5. **No-repo source acquisition (6)**: use `tools/intake.py --work X
    --source S --segments seg.json --edition E --source-license L` (byte-span
    pinned segments: song/verse/verse_id/start/end; every non-ws byte covered).
    Candidates — DONE: dehastha → gold #30 (Abhinavastotravali print, 16v/2 songs, full pipeline, CANONICAL 0 failures).
    Remaining: mahopadeshavimshatika, paramadvayadvadashika,
    rahasyapanchadashika, tattvasandoha. Plus **paramarthadvadasika** —
    anomaly RESOLVED 2026-11-04: SOURCE.txt holds full 13v (nothing to transform;
    reclassified no-repo, needs intake + full pipeline).

## Todos (25)

- [x] 1. T1 p02–p03 glosses (20v, 214 tokens span-exact, 15 forks) + committed  ← DONE
- [x] 2. T1 p04–p05 glosses (19v, 237 tokens span-exact, forks noted) + committed
- [x] 3. T1 p06–p07 glosses (20v, 208 tokens span-exact) + committed
- [x] 4. T1 p08–p09 glosses (20v, 243 tokens span-exact) + committed
- [x] 5. T1 p10–p12 glosses (30v, 338 tokens) + v1 maṅgala proposal stav-p00 (GRETIL BhStC_1; M00089 collation open) + committed
- [x] 6. T1 120v span-exact vs GRETIL, byte-span intake pinned (source/edition.txt + segments.json), workcfg green + committed
- [x] 7. L0 p01–p05 (542 tok, morph + grounded forks, 100% PARSED) + validated + committed
- [x] 8. L0 p06–p12 + p00 (796 tok, M00089 collation: 7 AMBIGUOUS→PARSED, v37 māmi revised shine-forth) + validated + committed
- [x] 9. L0 COMPLETE 1338/1338 100% PARSED, chosen==T1 (1 revised w/ reason) + committed
- [x] 10. Argmaps p01–p06 (49v, verse-specific lore, all forks adjudicated, 0 shared) + committed
- [x] 11. Argmaps p07–p12 + p00 (71v incl. v47 8-pada double-47 kept whole, v69 ājñā-variant recorded not smoothed) + committed
- [x] 12. L2 p01–p06 (rasa-carried read prose, traced, cited byte-exact) + committed
- [x] 13. L2 p07–p12 + p00 (rewritten hand-composed, 0 shared with T1) + committed
- [x] 14. C1 p00–p12 (essence + 7-part SUMMARY + rasa{}; 0 quotes, 0 metacommentary, 0 shared with L2; C1 NOTEs written) + committed
- [x] 15. (folded into 14: all 13 songs + NOTEs in same pass)
- [x] 16. L3 p00–p12 (120 handcrafted couplets, read aloud, traced, essence-mapped, 0 shared with L2) + committed
- [x] 17. (folded into 16: all 13 songs in same pass)
- [x] 18. Stava data JSON (13 songs) + validate_song 0 errors x13 + proof PASS x13 + intake + check.py CANONICAL 0 failures + qa NEEDS_WITNESS + committed
- [x] 19. Stava L4 120/120 sung verse-by-verse (craft_notes + rejected-with-killers + reads_against per verse, all DRAFTs on file, data==DRAFTs, all differ from L3) + C2 eli5+genz tagged+merged (translator-hand, owner may redo) + proof PASS + committed → **GOLD #22**
  — OPEN: v1 source decision + first-verse L4 voice verdict (owner) + human review (machine-proposed throughout). C2 voice check deferred per owner (C2 can be added/redone later).
- [ ] 20. Tantraloka recon batches (a01–a12, a13–a25, a26–a37)
- [ ] 21. Spanda + Sivasutra + VBT recon + source pins
- [ ] 22. Short/broken works assessment batch (the 10 named above)
- [ ] 23. No-repo source acquisition (5 works, via intake.py)
- [ ] 24. Owner decisions + targets.md reorder + REGISTRY/HANDOVER refresh
- [ ] 25. C2 voice check (sample 2 works) + proof signoff triage

## Open owner decisions (cannot self-resolve; ask before building on them)

1. **stava v1 maṅgala** — proposed as stav-p00 (GRETIL BhStC_1 span-exact;
   M00089 Vṛtti partially collated: paśyantī/dṛśyamānayā as Vāk principles,
   full print byte-verify open). Owner decides: fetch M00089 print +
   byte-verify, or formal deferral; keep prepended stav-p00 vs extend stav-p01.
2. **stava L4 voice verdict** — 120 verses sung in one hand (dash-hold,
   colon landing, end-weighted close, plain singable diction, no stated rasa,
   no invented vocatives/refrains/rhymes). Owner: approve voice as house
   voice, adjust with direction, or kill verses with direction.
3. **anu-* verse_id collision** — anuttarastika vs anubhavanivedana both
   `anu-pNN` (work-scoped files; corpus uniqueness undecided).
3. **anu L3/C1 essence-width** — L3 essence_maps exceed C1 essence range
   (L4 mirrors L3, subset-valid; upstream fix = edit frozen L3 = owner).
4. **tantrasara-a01/a02 legacy dirs** — superseded by gold data dirs;
   archive or keep (rule 4: never import legacy).

## CANONICAL CHECKLIST (re-verified against all skill files 2026-11-04)

**Hierarchy**: AGENTS.md User Directive → FINAL-PROCESS.md → skills/crystal-ipvv/
SKILL.md + EXAMPLES.md + LAYERS.md → crystal.md + mistakes.md → targets.md.
One work at a time; machine proposes, humans dispose; gate is a proxy, rule is law.

**Per-work drill** (SKILL.md §drill, 11 steps): pick 1 target → source pinned
& read → ONE focused lore search + rasa file → T1 (coverage first; forks marked,
never smoothed) → L0 (100% PARSED *and* verse-count vs edition; forks with
analyzed morph + grounded sources) → argmaps (terse logic; verse-specific lore;
option_choices adjudicates every fork; zero shared sentences across passages) →
L2 (plain, rasa-carried, byte-exact cite, clause→L0, supplied[]) → C1 (7-part
essay in NOTE; essence = matters only; 0 quotes, 0 metacommentary, 0 shared with
L2) → L3 per **process/L3-HANDCRAFT.md** (SA aloud → line shape → spine per line
→ kill small defects → L0-coverage → BOUNDARY honored in notes → variants marked
not-resolved → validate + read aloud; DRAFT-file; **frozen once loved**) → L4 per
**skills/l4-song/SKILL.md + process/L4-SONG-PROCESS** (Sanskrit first; sthāyin;
firing rows; subset traces; craft_notes + rejected-options-with-killers +
reads_against per verse; first-verse verdict) → C2 via `render_c2.py
--print-prompt` (never hand-roll the prompt; tags [E#] mandatory; untagged →
.draft) → gates loop → STATUS/REGISTRY `machine-proposed, needs human review`.

**Per-layer validators**: schemas/{t1,l0,argmap,l2,c1,l3,l4,c2}.py via
`tools/validate_song.py --song X --work W`; `tools/proof_record.py` writes
proof-<song>.json (PASS/BLOCKED + layer_sha256); `check.py --work W` must end
CANONICAL 0 failures before every commit.

**The 18 mistakes rules** (mistakes.md — checked before any COMPLETE): no C1
quotes; no C1 metacommentary (matters not document; broad scan > narrow regex);
L2≠C1 sentences; T1 full-coverage vs source not tool; no copy-paste lore;
mark uncertainty never invent; one work at a time; gate≠rule; **no scripts/bulk
as AUTHORS** (content hand-composed; scripts may only assemble/verify/probe —
glosses, lines, arguments are written by hand with the verse in front of you);
depth over speed; C1 pristine (notes in NOTE file); display-only types; L3 no
slashes + rhythm is law (rule 16); read whole stack before touching a layer,
never rewrite living voice unasked (15); L4 sings/L3 means + first-verse verdict
(17); producers own files — refuse overwriting ingest-shaped output (18).

**T1 data-lane format (gold-verified)**: tokens = source-natural (compounds
whole as source spaces them; surfaces byte-exact incl. avagraha `'pi`/`'py`),
quick_gloss = hyphenated, compound-ordered English (pada order). Every working
file must **pre-flight span-check** all verses before committing (lesson from
2026-11-04 loop: generate only after a difflib surfaces-vs-spans sweep passes).

**After translation**: concept pass (build_concepts/lookup_concept) —
post-translation, never a prerequisite (FINAL-PROCESS §concept timing).

## Authoritative docs (do not duplicate elsewhere)

- Process: `skills/crystal-ipvv/SKILL.md` (+ EXAMPLES.md), `FINAL-PROCESS.md`,
  `crystal.md`, `mistakes.md`, `LAYERS.md`, `process/L3-HANDCRAFT.md`.
- L4: `skills/l4-song/SKILL.md`, `process/L4-SONG-PROCESS-2026-11-03.md`,
  `lore/l4-english-songcraft-2026-11-03.md`, `lore/bank/songcraft-bank.json`.
- Tools: intake.py (new source byte-spans), agent_contract.py (machine
  handoff), render_c2.py, validate_song.py, proof_record.py, check.py.
- Historical (dated, kept): HANDOVER-2026-11-03.md (L4 craft voice — still
  authoritative for singing).
