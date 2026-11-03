# TODOREGISTRY — current state + todos for the next agent

*Created 2026-11-04. This file and REGISTRY.json are the two entry points:
REGISTRY.json = per-work truth (notes, counts, status); this file = the live
queue. Read both, plus AGENTS.md (control plane) and targets.md (queue
detail). When todos change, edit THIS file in the same commit — never leave
it behind.*

## State snapshot (verified 2026-11-04, everything committed and pushed)

- **21 gold works / 163 songs.** On every gold work: T1/L0/argmap/L2/C1/L3 ✓,
  L4 song ✓, C2 renders (eli5 + genz, [E#]-tagged) ✓, proofs refreshed with
  `layer_sha256` covering L3/L4/C2.
- **Gate: `python3 check.py --work <name>` → CANONICAL, 0 failures on all 21**
  (the gate defaults to `--work sivastotravali`; loop over all works when
  auditing).
- **REGISTRY.json**: 92 works, 21 gold, 71 pending (tantrasara legacy dupes
  removed; stale BLOCKED notes rewritten).
- **Active transform: stavacintamani** (Tier 2) — T1 p01–p03 glossed
  (30/119 verses, 305 tokens, span-exact vs `working-versemap.json`;
  15 forks flagged; v30 resolved via Kṣemarāja Vṛtti M00089). v1 maṅgala
  gap logged (corpus = vv2–120; fetch + byte-verify before final T1).
- Working files for the transform: `stavacintamani/working-versemap.json`
  (119v Sanskrit spans, GRETIL-verified), `working-t1-stav-p01.json`,
  `working-t1-stav-p02-p03.json`, `lore-2026-11-04.md` (scholars banked).

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
- [ ] 15. C1 p07–p12 (matters-not-document, rasa block, 0 quotes/meta)
- [ ] 16. L3 p01–p06 (draft, DRAFT-file, verdict, freeze)
- [ ] 17. L3 p07–p12 (draft, DRAFT-file, verdict, freeze)
- [ ] 18. Stava data JSON + full gate + proof + REGISTRY + commit
- [ ] 19. Stava L4 voice verdict + L4 + C2 + push  → **GOLD #22**
- [ ] 20. Tantraloka recon batches (a01–a12, a13–a25, a26–a37)
- [ ] 21. Spanda + Sivasutra + VBT recon + source pins
- [ ] 22. Short/broken works assessment batch (paramadvaya-, mahopadesha-,
      rahasya-, dehastha, tattvasandoha, saktavijnana, svabodhasiddhi,
      paratrimshika, paramarthadvadasika, ptvmadhyama)
- [ ] 23. No-repo source acquisition (5 works: locate + pin)
- [ ] 24. Owner decisions + targets.md reorder + REGISTRY/HANDOVER refresh
- [ ] 25. C2 voice check (sample 2 works) + proof signoff triage

## Open owner decisions (cannot self-resolve; ask before building on them)

1. **stava v1 inclusion** — maṅgala verse absent from corpus; needs Muktabodha
   M00089 fetch + byte-verify, or formal deferral recorded in STATUS.
2. **anu-* verse_id collision** — anuttarastika and anubhavanivedana both use
   `anu-pNN` (files are work-scoped; corpus uniqueness undecided).
3. **anu L3/C1 essence-width mismatch** — L3 essence_maps exceed C1 essence
   range (pre-existing; L4 mirrors L3 subset-valid; upstream repair = edit L3,
   which needs freeze-owner eyes).
4. **tantrasara-a01/a02 legacy dirs** — superseded by gold data dirs; archive
   or keep (rule 4: legacy never imported).

## How to continue a T1 batch (stava p04→p12)

1. Pull exact token lists: `working-versemap.json` spans → `.split()`.
2. Draft per verse: `quick_english` + per-token `quick_gloss`
   (pada-split, hyphenated compounds, source-exact surfaces incl. avagraha
   `'pi`/`'py` — surfaces must byte-match the span).
3. Flag every genuine fork / obscure form in `forks_noted` (L0 adjudicates;
   use Kṣemarāja Vṛtti via Muktabodha M00089, Marjanovic 2011, one focused
   search max per skill).
4. **Pre-flight BEFORE generating**: compare all verses' surfaces vs spans
   (difflib), fix every mismatch in one pass — never one-at-a-time.
5. Append to `working-t1-stav-p0X...json` (same schema as p01/p02-p03 files),
   commit, push. Then L0 etc. per crystal-ipvv/SKILL.md.

## Authoritative docs (do not duplicate elsewhere)

- Process: `skills/crystal-ipvv/SKILL.md` (+ EXAMPLES.md) — L4:
  `skills/l4-song/SKILL.md`, `process/L4-SONG-PROCESS-2026-11-03.md`,
  `lore/l4-english-songcraft-2026-11-03.md`, `lore/bank/songcraft-bank.json`.
- Gate: `python3 check.py --work <name>` (exit 0 = canonical).
- DRAFT law: drafts live outside `data/` until verdict; L3 frozen once
  loved; L4 = L3 set to music (subset traces, no doctrine); every L4 verse
  carries craft_notes + rejected-options-with-killers + reads_against.
- Historical handovers (dated, superseded but kept): HANDOVER-2026-11-03.md
  (L4 craft guidance — still authoritative for voice).
