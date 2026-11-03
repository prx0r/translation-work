# TODOREGISTRY — current state + todos for the next agent

*Created 2026-11-04. This file and REGISTRY.json are the two entry points:
REGISTRY.json = per-work truth (notes, counts, status); this file = the live
queue + the canonical checklist. Read both, plus AGENTS.md, skills/crystal-ipvv/
SKILL.md + EXAMPLES.md + FINAL-PROCESS.md + crystal.md + mistakes.md (all read
and re-verified 2026-11-04 — see CANONICAL CHECKLIST below). When todos change,
edit THIS file in the same commit — never leave it behind.*

## State snapshot (verified 2026-11-04, all committed and pushed)

- **21 gold works / 163 songs**, each with T1/L0/argmap/L2/C1/L3 + L4 song +
  C2 (eli5+genz, [E#]-tagged) + refreshed proofs (layer_sha256 over L3/L4/C2).
- **Gate green everywhere**: `python3 check.py --work <name>` CANONICAL on all
  21 (defaults to sivastotravali — loop it when auditing).
- **REGISTRY.json**: 92 works / 21 gold / 71 pending (dupes + stale notes fixed).
- **Active**: stavacintamani transform — T1 p01–p03 canonical (30/119v,
  305 tokens, span-exact vs `working-versemap.json`, 15 forks flagged;
  v30 resolved via Kṣemarāja Vṛtti/M00089; v1 maṅgala gap logged).
- Stale docs swept today: AGENTS.md counts, targets.md gold table (21 rows) +
  tier sections, HANDOVER-2026-11-03 banner, stava STATUS.

## Queue order (immediate → deferred)

1. **stavacintamani** — finish it (todos 2–19) → **gold #22**. Mid-flight.
2. **Small standalone legacy works, smallest first** — each = full transform
   (FINAL-PROCESS §how-to-transform, 14 steps) → L3 handcraft → L4 → C2:
   1. saktavijnana (~30v, 3 passages)
   2. svabodhasiddhi (~32v, 4 passages)
   3. paratrimshika (~35v, 4 passages)
   4. ptvmadhyama (35v — **T1 corrupt, rebuild T1 first**)
   5. spanda (~24v — passage verse-ranges garbled `20-3`,`16-2`; fix first)
   6. sivasutra (~80 sutras, 8 passages, 1.x-3.x numbering)
   7. vbt (~112v, 17 passages)
3. **tantrasara-a03–a22** (20) — same pattern, proven twice (a01/a02 gold).
4. **tantraloka-a01–a37** (37) — the big campaign.
5. **No-repo source acquisition (5)**: use `tools/intake.py --work X
   --source S --segments seg.json --edition E --source-license L` (byte-span
   pinned segments: song/verse/verse_id/start/end; every non-ws byte covered).
   Candidates: dehastha, mahopadeshavimshatika, paramadvayadvadashika,
   rahasyapanchadashika, tattvasandoha. Plus **paramarthadvadasika** —
   registry says legacy but dir has NO files; resolve or reclassify.

## Todos (25)

- [x] 1. T1 p02–p03 glosses (20v, 214 tokens span-exact, 15 forks) + committed  ← DONE
- [ ] 2. **T1 p04–p05 glosses (19v) + committed**  ← CURRENT
- [ ] 3. T1 p06–p07 glosses (20v) + committed
- [ ] 4. T1 p08–p09 glosses (19v) + committed
- [ ] 5. T1 p10–p11 glosses (20v) + committed
- [ ] 6. T1 p12 glosses (10v) + v1 maṅgala resolution (fetch/verify or formal defer)
- [ ] 7. L0 p01–p04 (morph + options, forks grounded) + validated
- [ ] 8. L0 p05–p08 (morph + options, forks grounded) + validated
- [ ] 9. L0 p09–p12 (morph + options, forks grounded) + validated
- [ ] 10. Argmaps p01–p06 (verse-specific lore, fork adjudication)
- [ ] 11. Argmaps p07–p12 (verse-specific lore, fork adjudication)
- [ ] 12. L2 p01–p06 (rasa-carried, traced, cited)
- [ ] 13. L2 p07–p12 (rasa-carried, traced, cited)
- [ ] 14. C1 p01–p06 (matters-not-document, rasa block, 0 quotes/meta)
      — NOTE: stava's legacy C1.md is a named non-crystal exhibit (gloss
      dumped as C1, crystal.md); REWRITE, never carry it forward.
- [ ] 15. C1 p07–p12 (matters-not-document, rasa block, 0 quotes/meta)
- [ ] 16. L3 p01–p06 per `process/L3-HANDCRAFT.md` (8-step pass, DRAFT-file,
      verdict, freeze)
- [ ] 17. L3 p07–p12 (same)
- [ ] 18. Stava data JSON + full gate + proof + REGISTRY + commit
- [ ] 19. Stava L4 voice verdict + L4 + C2 + push  → **GOLD #22**
- [ ] 20. Tantraloka recon batches (a01–a12, a13–a25, a26–a37)
- [ ] 21. Spanda + Sivasutra + VBT recon + source pins
- [ ] 22. Short/broken works assessment batch (the 10 named above)
- [ ] 23. No-repo source acquisition (5 works, via intake.py)
- [ ] 24. Owner decisions + targets.md reorder + REGISTRY/HANDOVER refresh
- [ ] 25. C2 voice check (sample 2 works) + proof signoff triage

## Open owner decisions (cannot self-resolve; ask before building on them)

1. **stava v1 maṅgala** — absent from corpus (vv2–120); fetch M00089 +
   byte-verify, or record formal deferral in STATUS.
2. **anu-* verse_id collision** — anuttarastika vs anubhavanivedana both
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
