# HANDOVER — 2026-11-04 (E): L4 beauty pass ordered; tantrasara paused

*For the next agent. Read in this order, no skipping: AGENTS.md → skills/crystal-ipvv/SKILL.md (+ EXAMPLES.md) → skills/l4-song/SKILL.md → process/L3-HANDCRAFT.md → process/L4-SONG-PROCESS-2026-11-03.md → lore/rasa/abhinavagupta-rasa-grounding + lore/rasa/english-transmission-2026-11-03.md → lore/l4-english-songcraft-2026-11-03.md + lore/bank/songcraft-bank.json (query per verse, never copy style) → mistakes.md (esp. #10 batch, #11 depth, #15 one-at-a-time, #17 L4-sings-never-L3, #18 producers-own-files, #19 alignment audit) → FINAL-PROCESS.md → LAYERS.md → todoregistry.md → REGISTRY.json → HANDOVER-2026-11-04-B → -C → -D → this file. Nothing below is invented: counts came from gate runs and file reads this session.*

## 0. Where we stand (verified; all committed except a12 WIP scratch below)

- **REGISTRY**: 91 works / **36 gold** / 55 pending. All 36 check.py CANONICAL in one full sweep this session (0 failures each).
- Golds #30–#36 this session: dehastha (16v) → paramarthadvadasika (13v, Sferra recension; Abhinavastotravali print recorded as variant) → rahasyapanchadashika (16v) → mahopadeshavimshatika (20v) → tantrasara-a18 (2 prose units, abhiṣeka) → tantrasara-a17 (6 prose units, liṅgoddhāra) → tantrasara-a19 (7 prose units, post-mortem/śrāddha).
- Earlier: paramadvayadvadashika MERGED as variant title of paramarthadvadasika (colophon "athavā"; single gold; registry 92→91).
- Uncommitted in repo: `tantrasara-a12/cm/` (source.itx, segments-input.json, working T1+L0+argmap? NO — only cm scratch + lore) + `tantrasara-a12/lore-2026-11-04.md`. a12 intake staged, translation NOT started — on purpose (see §1).
- Uncommitted in /root/ipvv (owner's repo, owner's commit): site/data/translations/*.json ABSTENTION skeletons incl. new ones through a19.
- a17/a19 STATUS + REGISTRY notes now say gold #35/#36 correctly (an earlier commit message mislabeled a19 as #35; cosmetic, in history).

## 1. Owner directive 2026-11-04 (binding — supersedes tantrasara-first ordering for now)

**PAUSE the tantrasara campaign after a19. NEXT: the L4 beauty pass — make sure all the shorter gold works have beautiful L4 and are fully finished — before resuming tantrasara-a12 onward.**
- "Beautiful" = every L4 line survives a read-aloud test (scans, sings, end-weighted doctrine words land), no invented refrains/vocatives/rhymes, no new doctrine (subset rule enforced), first-verse voice verdict requested from owner (never treat machine voice as house voice).
- "Fully finished" = the per-work Definition of Done in §4, including STATUS current, c1.NOTE present, qa re-run, proof current, no stale artifacts, data==DRAFTs verified, check.py green.
- **C2 WAIVED going forward** (owner 2026-11-04, verbatim: "u can leave genz and eli5"). Do NOT build C2 (eli5/genz) for new passes. Existing C2 files stay. Do not delete them. This is reversible by owner order only.

## 2. What the L4 audit found (2026-11-04, this session — the reason for this directive)

- **New standard (craft_notes + reads_against per verse, machine-proposed, data==DRAFTs verified byte-equal):** vbt 162/162, stavacintamani 120/120, sivasutra 75/75, saktavijnana 30/30, svabodhasiddhi 33/33, spanda 25/25, paratrimshika 36/36, ptvmadhyama 35/35, dehastha 16/16, mahopadeshavimshatika 20/20, paramarthadvadasika 13/13, rahasyapanchadashika 16/16, tantrasara-a17/a18/a19 (6/2/7), anubhavanivedana 4/4, spandasandoha 2/2, paramarthasara 16 DRAFTs (MIXED granularity — see below), anuttarastika 8 DRAFTs but only 3 with craft_notes.
- **Old style (L4 lines exist, NO craft_notes, NO reads_against — beauty unverified):** ajadapramatrsiddhi, bhairavanukarana, bhairavastava, bodhapancadasika, bodhavilasa, ghatakarpara (21/22 craft, 1 reads_against — nearly there), isvarasiddhi, kramastotra, pancashloki, paramarthacarca, parapravesika, paryantapancasika, phrdaya, sambandhasiddhi, sivastotravali (per-song DRAFTs).
- **Granularity anomalies to normalize during the pass:** paramarthasara mixes per-verse (p01 v01–v04), a range file (v05–v10), and per-song (p02) DRAFTs → normalize to per-verse everywhere. ghatakarpara has 22 DRAFTs for 21 verses (one stray per-song p03 DRAFT): verify which matches data, remove the other. sivastotravali is per-song only (20 DRAFTs / 450 verses): verify-only in this pass; full per-verse craft is a later campaign — ask owner before starting it.
- **Missing entirely:** tantrasara-a02 has ZERO L4 DRAFTs (but data/tsa-a02.l4.json exists and gates pass — provenance gap: build per-verse DRAFTs with craft_notes from the data, do not re-derive lines). tantrasara-a01 has ONE per-song DRAFT with no craft — convert to per-verse DRAFTs + craft. Both lack c1.NOTE files (only golds without NOTEs) — write them.
- tantrasara-a12: cm/ + lore staged, uncommitted, nothing built — PAUSED, do not touch until beauty pass is done.

## 3. Beauty-pass queue (shortest first; one work at a time — mistakes.md #10/#15)

**Track A — full craft treatment (old-style L4, per-verse unless noted):**
1. tantrasara-a02 (4v) — BUILD per-verse DRAFTs + craft + reads_against; write c1.NOTE.md; refresh STATUS (stale 2026-10-30 batch note).
2. pancashloki (5v) — craft per-verse.
3. tantrasara-a01 (5v) — convert the 1 per-song DRAFT to per-verse + craft; write c1.NOTE; refresh STATUS (stale).
4. paramarthacarca (8v) — craft per-verse.
5. anuttarastika (8v) — complete the 5 missing craft_notes + reads_against.
6. bhairavastava (10v) — craft per-verse.
7. bodhapancadasika (15v) — craft per-verse.
8. phrdaya (20v, 5 songs) — craft per-song (keep existing granularity).
9. ghatakarpara (21v) — craft per-verse; resolve the stray 22nd DRAFT (verify against data, delete the other).
10. sambandhasiddhi (23v, 3 per-song) — craft per-song. (Attribution uncertain — translate the Sanskrit as-is; do not litigate authorship here.)
11. ajadapramatrsiddhi (27v; verify granularity first — 3 DRAFTs suggests per-song) — craft at existing granularity.
12. kramastotra (30v, per-verse) — craft.
13. bodhavilasa (41v, 5 per-song) — craft per-song.
14. bhairavanukarana (48v, 5 per-song) — craft per-song.
15. paryantapancasika (52v, 8 per-song) — craft per-song.
16. parapravesika (prose, 9 passages) — craft per-passage.
17. isvarasiddhi (56v, 7 per-song) — craft per-song.
**Track B — read-aloud verification only (new-style already; rewrite a verse only if it fails the read-aloud test, with full craft_notes for the rewrite):**
anubhavanivedana, spandasandoha, dehastha, rahasyapanchadashika, mahopadeshavimshatika, paramarthadvadasika, saktavijnana, svabodhasiddhi, spanda, sivasutra, ptvmadhyama, paratrimshika, vbt, stavacintamani, tantrasara-a17/a18/a19.
**Deferred (owner call needed):** paramarthasara (normalize mixed granularity to per-verse + craft all — big job); sivastotravali (per-verse craft for 450 verses — big job).

## 4. Definition of done per work (beauty pass; C2 explicitly excluded)

1. Every L4 unit has craft_notes (sthāyin one phrase; firing transmission-table rows; close-shape; read-aloud audit; rejected alternatives with the exact layer/row/read-aloud killer — a choice with no named rival is a preference, not a decision) + reads_against (argmap question→inference verbatim; C1 essence text; C1 rasa) + status machine-proposed + needs human-review.
2. data/<song>.l4.json == DRAFTs exactly (verify by script, as done 2026-11-04 for 14 works).
3. validate_song 0 errors; alignment audit vs own L3 ≥0.30 every verse (mistakes.md #19); no shared 8-grams L3/L2 (re-check after any L3 touch); no slashes; exact diacritics (Śiva/Māyā/Śambhu).
4. No invented refrains, vocables carrying doctrine, or rhymes needing new slants (rules 17 + l4-song SKILL non-negotiables). Refrains verbatim-repeated or not at all.
5. First-verse DRAFT flagged for owner voice verdict (do NOT treat any machine voice as house voice).
6. STATUS.json current (counts incl. l0_parsed/ambiguous/failed, next, needs human-review); c1.NOTE present; proof re-run PASS; roundtrip 0; qa re-run (NEEDS_WITNESS expected unless witness vendored); check.py CANONICAL 0 failures; commit.
7. C2: DO NOT BUILD (waived). Existing C2 files stay untouched.

## 5. Standing items (unchanged unless noted)

- First-verse L4 voice verdicts for ALL golds + human review of every machine-proposed stack. Nothing marked final, ever, by the machine.
- ipvv site/data/translations/*.json ABSTENTION skeletons: write them (required for check.py site-data), never commit ipvv (owner's repo, owner's commit).
- Push cadence: push translation-work only when the owner explicitly says so. This session pushed 29→36 + merges on explicit request.
- ptvmadhyama re-aim (Vivṛti) vs recension pair: still owner-open; cross-links already in STATUS+lore both sides.
- Witnesses: vendored legacy-L2 witnesses converted for the six recent stotra golds (SHIP_AS_IS + 2 WITH_NOTES adjudicated). No new witnesses needed for the beauty pass (reads existing C1/L2, creates no new claims).
- New-work drill (for AFTER the beauty pass, when tantrasara resumes at a12): intake.py → cm/ provenance → T1 span-exact assert → build_l0.py (canonical builder; hand-enrich forks/AMBIGUOUS after, never retype glosses) → argmaps (zero shared sentences) → L2 → C1 (0 quotes/meta/shared) → data emit + T1/L2 MDs + jsonl/reports + C1 MDs → validate/proof/roundtrip/qa → L3 handcraft (L3-HANDCRAFT.md, frozen once loved) → L4 (this handover's drill) → NO C2 (waived) → c1.NOTE → data l3 emit → gates → STATUS → check.py → gold commit → REGISTRY/todoregistry arithmetic (total = gold + pending, always) → push only when asked.
