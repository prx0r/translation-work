# HANDOVER — Full briefing for the next agent (2026-11-06)

*Read this file first. It is the single entry point: what we're doing, why,
where things stand, how to work, what to avoid, and what's next. Longer-lived
canon lives in AGENTS.md / FINAL-PROCESS.md / skills/; this file is the live
state + working agreement. If anything here conflicts with AGENTS.md's verbatim
User Directive 2026-11-01, the directive wins.*

---

## 1. What we are doing

Building **crystal-quality machine-proposed, human-reviewed English translations
of Abhinavagupta's Sanskrit corpus** (Trika Shaivism), as validated data objects
— not documents. Every layer is JSON, validated by schemas, gated by `check.py`;
Markdown is kept only as rendered views for human review.

**Done:** Tantrasāra, all 22 āhnikas, GOLD (machine-proposed throughout).
52 more gold works (stotras, prakaraṇas, VBT, Gītā slice, etc.). Registry total:
101 works / 53 gold / 48 pending.

**Now:** Tantraloka recon — all 37 āhnikas. Recon means, per ahnika: verify
verse spans against GRETIL, count verses/tokens, register in `tools/workcfg.py`,
assess meter/difficulty/legacy materials/witnesses, record the queue. Transform
(gold translation) comes after, shortest-first per owner goal (a34 → … → a15).

## 2. Why (the thesis in one paragraph)

Each layer looks at the previous layers for support; nothing floats. T1 covers
the whole source first (coverage before sharpness); L0 audits every token so
forks live in exactly one place with grounds; argmap reads the whole verse
against Sanskrit+T1+L0+scholarship so adjudication is on the record; L2 renders
the plain meaning so every clause traces down; C1 names the essence (what the
verse DOES, per Abhinavagupta's rasa theory) so renders have something to point
at; L3 is the frozen transmission; L4 sets it to music with subset traces.
Machine proposes, humans dispose — `COMPLETE` always means machine-proposed
until a human signs off.

## 3. Where things stand (verified 2026-11-06)

- `python3 check.py` per work: **CANONICAL, 0 failures** across all gold works
  (22 tantrasara + 31 others + gitarthasangraha slice).
- Tantraloka parser `parse_taloka` added to `tools/workcfg.py` (+ `taloka` kind
  in `source_spans`, but **no works registered yet** — registration is todo
  #38–40, in three batch commits).
- Count table (GRETIL `[AbhT_A.V]` markers, verified programmatically):

| Ahnika | Verses | Ahnika | Verses | Ahnika | Verses |
|---|---|---|---|---|---|
| a01 | 333 | a14 | 47 | a27 | 59 |
| a02 | 50 | a15 | 613 | a28 | 435 |
| a03 | 295 | a16 | 311 | a29 | 292 |
| a04 | 279 | a17 | 122 | a30 | 123 |
| a05 | 159 | a18 | 11 | a31 | 164 |
| a06 | 252 | a19 | 56 | a32 | 68 |
| a07 | 71 | a20 | 16 | a33 | 32 |
| a08 | 452 | a21 | 61 | a34 | 4 |
| a09 | 314 | a22 | 48 | a35 | 44 |
| a10 | 310 | a23 | 103 | a36 | 16 |
| a11 | 118 | a24 | 24 | a37 | 85 |
| a12 | 26 | a25 | 29 | — | — |
| a13 | 362 | a26 | 76 | Total | 5860 |

- Known discrepancy: legacy frozen T1 header for a01 says 334 verses; parser
  finds 333 numbered verses. Do NOT "fix" — record as boundary during recon.
- Legacy dirs `tantraloka-a01/` … `tantraloka-a37/` contain batch-era files
  (T1.md, L1.md, ARGMAP.md, GATE.json BLOCKED, etc.). **Frozen. Never edit.**
  Gold files live alongside under new names (`working-*`, `data/tsa-aNN.*`,
  `T1-tsa-aNN.md`, `c1/C1-tsa-aNN.md`, `proof/`, updated `STATUS.json`).
- 50-todo recon plan is in the todo list: #1 done (parser + counts);
  #2–#38 per-ahnika recon pending; #39–#41 batch registration commits;
  #42–#50 wrap-up (registry, report, order, lore, witnesses, handover,
  check sweep, owner verdict).

## 4. How to work (the drill — no deviations)

Per work (FINAL-PROCESS.md + skills/crystal-ipvv/SKILL.md — read both fully
before touching a translation):
1. Pick ONE target. Never parallelize across works.
2. Source first: read and master it before writing anything.
3. Lore: ONE focused web search + the rasa grounding file. Verse-specific
   notes only.
4. T1: lore-primed fast pass, pada-split glosses, FULL coverage. Forks marked
   for L0, never smoothed.
5. L0: hand-written CM (`cm/l0cm-v1-N.json` = [citation, morph, grounds] per
   span token, ONE entry per span token, fused-span rule: whatever the source
   joined, you join). `build_l0.py` builds working-L0 (gloss inherited from T1).
6. T1.md + .l0.jsonl + .report (assembler scripts may assemble; content is
   hand-written by you).
7. Argmaps: hand-written, terse logical statements, verse-specific lore,
   adjudicate L0 forks on the record. `fill_argmap.py` fills traces + sha.
8. L2: plain-English read prose, rasa-carried, byte-exact cites, l0_ids,
   supplied[].
9. C1: essence (atomic, one per unit) + standard 7-part essay + rasa{} + NOTE
   file. 0 quotes, 0 metacommentary, 0 shared sentences with L2.
10. L3: handcrafted couplets/sequences, reworded vs L2, traced, no slashes,
    exact diacritics. FROZEN once loved.
11. L4: DRAFT per verse OUTSIDE data/ first: sthāyin + firing rows +
    rejected-with-killers + read-aloud + reads_against. Subset traces only.
12. Data emit → validate_song 0 errors → proof_record PASS → qa_vs_witness →
    STATUS + REGISTRY as machine-proposed → check.py CANONICAL → commit
    locally. **Push only when explicitly asked AND no other agent is active.**
13. C2 is WAIVED per owner (existing C2 stays; do not build new C2).

For recon (current phase): spans → counts → register → assess. No translation
yet. One focused lore search per hard ahnika is enough; witnesses are
comparison-only, never copied.

## 5. Skills and docs map (read in this order if new)

1. This file. 2. `AGENTS.md` (operating system + verbatim user directive).
3. `FINAL-PROCESS.md` (canonical process). 4. `skills/crystal-ipvv/SKILL.md` +
   `EXAMPLES.md` (the only authorized workflow + good/bad exhibits per layer).
5. `LAYERS.md` (layer contracts). 6. `crystal.md` (finished-work standard).
7. `mistakes.md` (failure log — every rule below comes from a real defect).
8. `skills/l4-song/SKILL.md` + `process/L4-SONG-PROCESS-2026-11-03.md` (songs).
9. `process/L3-HANDCRAFT.md` (transmission craft). 10. `AGENT-MAP.md`
    (three-repo map + data-hygiene ownership). 11. `REGISTRY.json` +
    `todoregistry.md` (queue truth). 12. Tool `--help` before any tool use.

## 6. Mistakes to avoid (all learned the hard way — most this month)

1. **Never trust your own JSON brackets.** After writing any hand JSON, parse
   it immediately. Bracket slips compound silently across batches.
2. **Fused-span rule.** One CM entry per span token, in span order. Never split
   what the source joined (`tasyāpi`, `cānudbhinnavibhāgā`, `vedyāc`,
   `sthaṇḍilāny` stay single). The 3-way assert (CM vs span vs T1) is your
   friend — run it after every batch.
3. **build_l0 overwrites working-l0.** Mint L0 forks AFTER building, then
   re-verify drift (chosen == T1 gloss). Validate after every mutation.
4. **fill_argmap rejected[] takes gloss STRINGS, not indices.** The validator
   compares against option glosses. Same for option_choices l0_ids — they must
   match the forked token's id exactly (a misindex once shipped a fork onto
   the wrong pada; the drift check caught it).
5. **Argmap option_choices need matching fork state.** Adjudicated →
   set L0 fork to `resolved`. Undecided stays `live` with uncertainties noted.
   Never smooth; never invent grounds.
6. **L2 must be genuinely re-written read prose**, not T1 with punctuation
   changes. (A copied L2 file was once caught by inspection: T1-identical.)
   Some overlap on short injunctions is honest; wholesale identity is failure.
7. **L4 overlap audit after EVERY batch** (content-word overlap L4 vs own L3;
   anything < 0.30 is re-sung from the true L3, never defended). Memory-composed
   L4 with copied traces is the failure mode — the validator cannot catch it.
8. **C1 states the MATTERS, never the document.** Ban list is a floor: run the
   broad scan ("the poem/passage/text/song/work", "this passage", "reader
   knows", "first/middle/final passage"). "The passage moves in N steps" in
   display text is metacommentary even if a gate doesn't flag it.
9. **No scripts as authors.** Scripts may assemble/verify/probe (spans,
   validation, overlap audit, file assembly). Glosses, lines, arguments,
   essences are written by hand with the verse in front of you. Never batch
   across works.
10. **Verify spans first, always.** `source_spans()` is ground truth. When your
    labels disagree with it, your labels are wrong (happened twice: stale
    printouts misread). Re-derive from spans, don't patch around them.
11. **workcfg.py is shared infrastructure.** Additive entries only. After any
    edit: import-check + full check sweep before committing. Never restructure
    existing parsers.
12. **Legacy files are frozen.** Batch-era T1.md/L1.md/ARGMAP.md/GATE.json etc.
    stay untouched; gold files use new names. `check.py` fails on banned paths.
13. **Notebooks of record:** STATUS.json + REGISTRY.json + todoregistry.md must
    move together in the gold commit. REGISTRY header counts must equal the
    body (it went stale twice).
14. **COMMIT LOCALLY, push only when asked.** If another agent is active in the
    repo (check `git log origin/master` and ask the owner), do NOT push, do NOT
    rebase through their work, do NOT touch their files. Local commits are
    cheap and safe.

## 7. Good behavior (what excellence looks like here)

- Verify, don't assume: run the gate after every layer, not just at the end.
- Counts first: every batch asserts lengths immediately (spans vs CM vs T1).
- Read the whole stack (SOURCE→T1→L0→argmap→L2→C1) before writing the next
  layer; L3/L4 start by re-reading everything, Sanskrit first.
- Craft notes written WHILE composing, with named rejected alternatives and
  the exact reason each lost (layer, row, or read-aloud fact). A choice with
  no named rival is a preference, not a decision.
- Read finished work aloud; the ear catches what gates miss (caught real
  defects: wrong counts, garbled lines, inversions).
- Record uncertainty in place (obscure forms, open antecedents, anomalous
  prints) — a flagged gap beats a smoothed guess.
- Small, sharp, finished beats big, batchy, approximate. One work at a time.
- Leave the repo cleaner: scratch in-repo per work (`cm/`, `working-*`);
  `/tmp` only for dumps; clean up when done.

## 8. Tooling quick reference

- `tools/workcfg.py` — registry + `source_spans()` (canonical spans) +
  `parse_*` per text (`parse_abhts` Tantrasara, `parse_taloka` Tantraloka).
- `tools/build_l0.py` (CM+T1 → working-L0), `tools/fill_argmap.py`
  (traces+sha+gates), `tools/validate_song.py`, `tools/render_md.py`,
  `tools/proof_record.py` (+`proof-disp.json`), `tools/qa_vs_witness.py`
  (NEEDS_WITNESS when no witness vendored), `tools/render_c2.py` (dormant),
  `tools/propose.py` + `tools/scholar.py` (living translation/review).
- Gate: `python3 check.py --work <work>` → `CANONICAL: 0 failures`.
- Site skeletons live in the ipvv repo (`site/data/translations/<work>.json`,
  ABSTENTION/BLOCKED until human review; owner commits ipvv).

## 9. What's next (the 50-todo plan, in todolist)

- #2–#38: per-ahnika recon (counts ✓ already from parser; still needed per
  ahnika: meter scan, difficulty rating, legacy-file assessment, witness
  check). Suggested batching: A (a01–12), B (a13–25), C (a26–37).
- #39–#41: register each batch in workcfg (kind=t aloka, songs tsa-aNN) +
  commit per batch (local commits; push only when asked & repo clear).
- #42: REGISTRY + todoregistry refresh. #43: recon report (sizes, meter map,
  difficulty ranking, witness inventory). #44: transform order per owner goal
  (shortest-first a34→…→a15 — verify against count table; note a34 has 4
  verses, a18 has 11, a20/a36 have 16). #45: lore for top-5 hardest.
  #46: witness inventory. #47: handover update. #48: full check sweep.
  #49: owner verdict package (recon review + transform order approval).
- Known open owner items (do not self-resolve): paramarthasara normalization +
  sivastotravali conversion nods; stava/sivastotravali register verdict;
  Gita a01→a18 continuation + 5 LIVE fork collations; mystics Kashmiri-gloss
  stage design; human review of all machine-proposed stacks.

## 10. Session log (2026-11-05/06, this agent)

- Reviewed /translation-work (health: green), flow + skills review.
- Tantrasara a22 (#49, 53u/652tok, 8 forks), a20 (#50, 65u/889tok, 2 forks),
  a06 (#51, 82u/981tok, 2 forks), a08 (#52, 93u/1120tok, 4 forks, 7 L4 re-sung),
  a13 (#53, 101u/1063tok, 4 forks, 4 L4 re-sung) — full stack each, all
  check.py CANONICAL, all committed locally; 4 site ABSTENTION skeletons
  committed in ipvv (locally).
- Overlap audit clean across GOLD #42–53; full sweep green (22 tantrasara +
  all other gold works).
- Pushed translation-work once when explicitly asked (6b2cd84 on top of the
  other agent's d0762b9); ipvv pushed similarly with workdir restoration.
- Owner approved all 5 first-verse L4 voices (standing). Recorded in STATUS.
- Started Tantraloka recon: parser + counts done. Registration + per-ahnika
  recon pending (see todolist).

*End of handover. Next agent: read §5 docs as needed, then continue at the
first pending todo. When in doubt: verify against spans, keep the gate green,
commit locally, push only when asked.*
