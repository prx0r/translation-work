# HANDOVER — 2026-11-04 (B): six golds #23–#28 banked; vbt in progress at L0 v61

*For the next agent. Read AGENTS.md → todoregistry.md → REGISTRY.json → this file.*
*This continues HANDOVER-2026-11-04.md (stava #22 + L4 method). Nothing below is
invented: every count came from a gate run this session.*

## 0. Where we stand (verified, all committed)

- **REGISTRY**: 92 works / **28 gold** / 64 pending.
- **Gold #23 saktavijnana** (30v): full pipeline, L4 sung v01–v30, C2 in place.
- **Gold #24 svabodhasiddhi** (33v, 4 songs): full pipeline, L4 v01–v33, C2.
- **Gold #25 paratrimshika** (36v): full pipeline, L4 v01–v36, C2. Recension
  notes live in `paratrimshika/lore-2026-11-04.md` (GRETIL root + Singh
  Vivaraṇa + Yogawiki; word-stages/vāk doctrine).
- **Gold #26 ptvmadhyama** (35v M00044 mūla of Lakṣmīrāma's Vivṛti): the
  legacy T1 was corrupt (vārttika mixed in, commentary interleaved); REBUILT
  edition from `SivS`-style markers minus prose. Later niḥṣyanda not touched.
- **Gold #27 spanda** (25v): FIRST NIḤṢYANDA ONLY (vv1–25 = svarūpaspanda per
  Kallata/Kṣemarāja both; later niḥṣyandas out of scope). Legacy 6-passage
  ranges (garbled `20-3`/`16-2`) superseded, documented in lore.
- **Gold #28 sivasutra** (75 sutras, 8 songs): Kaul Shastri 1925 recension
  (I.1-20 / II.1-10 / III.1-45), sutra-numbered in every layer. Vārttika
  verses excluded from edition (separate commentary, not translated).
- Each gold: `validate_song` 0 errors × N songs · `proof_record` PASS × N ·
  `roundtrip` 0 diffs · `check.py --work <x>` **CANONICAL: 0 failures** at
  completion · `qa_vs_witness` NEEDS_WITNESS (honest — no witness vendored).
- **Owner decisions outstanding (all six + stava #22): first-verse L4 voice
  verdict** per work (each L4 v01 DRAFT says so), plus human review of every
  machine-proposed stack. Nothing marked final.

## 1. vbt — IN PROGRESS, exact state

**Scope decision**: full tantra **162 verses** (NOT 112 — that is the count of
dhāraṇās inside; the queue's "~112v" conflates them). 17 songs: vbt-p01..p16 =
10v each (v1–160), vbt-p17 = closing pair (v161–162). Structure per Singh
outline: vv1–7 Devī doubts, v7b–v21 Bhairava answers, vv22–23 the beg, vv24–135
dhāraṇās, vv136+ fruits + colophon (kaṇṭhe lagnā). Legacy vbt batch files
(161v claim, 17 passages) are superseded; do not trust them.

**Done and committed** (`git log --oneline -- vbt/`):
1. `vbt/source/` intake — 162v byte-pinned, 17 songs, uvāca tags excluded
   (documented in `vbt/lore-2026-11-04.md`; lore also has Singh/Roche/uk-yoga
   structure, lehana-bowdlerizing note, rasa pointers).
2. **T1 162/162 span-exact** — `vbt/working-t1-vbt-p01..p17.json`, byte quirks
   kept (chinddhi, chaktyā, chivaḥ, ma.ṅdalaiḥ, bhittis, =B9haṃ, hoccāraṃ,
   laṣyam, bhavajij…), each flagged in `forks_noted`.
3. **L0 v1–60** — `vbt/working-l0-vbt-p01..p06.json`, **598 records, 0 schema
   errors, 0 drift** (gloss inherited from T1 by construction).

**Immediate next step — L0 v61–162 (102 verses, ~1000 records).**
The working pattern is proven; reuse it:
- Builder: `/tmp/opencode/build_l0abcd.py` (v1–40) and
  `/tmp/opencode/build_l0_p05p06.py` (v41–60). Copy one, edit the CM path +
  verse range + song map.
- CM data format: JSON `{verse: [[citation(IAST lemma), morph, grounds],…]}`
  — ONE entry per span token, order == `workcfg.source_spans` order (filter
  `set(tok)!={'|'}`). Builder asserts `len(cms)==len(span)` and
  `len(T1.tokens)==len(span)`; gloss comes from T1, never re-typed.
- **Draft CM exists for v61–70** at `/tmp/opencode/cm_v61_70.json` — BUT its
  citations are degraded ASCII (smri/bhu/bhava without diacritics, some
  half-written). **Fix to proper IAST (smṛ, bhū, bhāva…) before running**, and
  audit morph strings. `cm_v61_80.json` is a truncated fragment — ignore.
- For v71–162 dump T1 first (`[surface, quick_gloss]` per verse), then write
  CM in **≤10-verse chunks** (bigger writes got truncated twice this session —
  verify `json.load` parses before running the builder).
- After each batch: `schemas/l0.py` validate + T1 drift check + commit.

**Then the rest of the stack** (same as every gold): argmaps → L2 → C1 →
data emit → L3 → L4 → C2 → `render_c2`/`proof`/`qa` → `check.py --work vbt` →
registry/todoregistry/STATUS + c1.NOTE files. Current gate state is expectedly
red: `check.py --work vbt` = `FAIL data-present`, `FAIL qa-present` only.

## 2. Session failure log (new entries — add to mistakes.md discipline)

1. **Large JSON writes truncate.** Three CM files corrupted (one `Expecting
   ',' delimiter`, one silently truncated mid-array). Rule: write ≤10 verses
   per file; `json.load`-verify immediately; never trust a write you didn't
   parse.
2. **CM entries must be length-audited against spans** — off-by-one from fused
   spans (yāvasthā etc.) and stale scaffold entries (`kā ?`, `x`) are the
   recurring bugs; the builder assert catches them, keep it.
3. **`ca` dropped from T1 v31** once (L0 drifted) — normalized both layers
   from span bytes; span is the only truth.
4. **grep/`(?=)` drift checks** — print `(repr(a),repr(b))` on mismatch before
   "fixing"; twice the wrong side was patched (an anusvāra, a visarga).
5. **L3≡L2 identical-line** fails `validate_song` — rewrite, don't patch:
   occurred on 37 sūtra lines (they are short); distinct phrasing, 0 shared
   re-verified after.
6. **Essence count mismatch** (C1 6 vs L3 mapping v7) — validate with the
   ACTUAL per-song essence length read from the C1 file, not a stale dict.
7. **Registry pending arithmetic**: pending = total − gold (28+64=92), never
   hand-increment one side.

## 3. Owner standing orders (still binding)

- Sanskrit-first trust gradient; L4 first-verse voice verdict BEFORE treating
  any new gold's L4 as voice; no invented refrains; dosed adbhuta; paper-thin
  finale; one work at a time; every layer machine-proposed, human reviews.
- tantrasara-a03–a22 / tantraloka excluded per owner — queue after vbt:
  no-repo intakes (see todoregistry §5).

## 4. Entry points (30-second orientation)

- Process: `FINAL-PROCESS.md` §how-to-transform · Skill: `skills/crystal-ipvv/SKILL.md`
- Gate: `python3 check.py --work <x>` (must print CANONICAL before registry edit)
- Per-song: `tools/validate_song.py` · `tools/proof_record.py --song X --work Y`
  · `tools/render_md.py` (roundtrip) · `tools/qa_vs_witness.py --work Y`
- Spans: `tools/workcfg.py::source_spans(work)` (ints via manifest, no workcfg
  edit needed for segmented intakes)
- Best gold specimens for style: `paratrimshika/` (short sūtra-adjacent) and
  `sivasutra/` (single-line L3/L4 form — the form for aphoristic works).
- The 50-todo list: `todoregistry.md` (queue §2 now 6/7 DONE + vbt marked
  IN PROGRESS with pointer here).
