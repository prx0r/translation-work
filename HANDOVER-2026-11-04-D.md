# HANDOVER — 2026-11-04 (D): golds #30–33, Abhinavagupta shortest-first goal

*For the next agent. Read AGENTS.md → todoregistry.md → REGISTRY.json → HANDOVER-2026-11-04-B → HANDOVER-2026-11-04-C → this file.*
*Nothing below is invented: every count came from a gate run this session. Note: commit a464756's message says "#34" but the work is gold #33 (cosmetic only; registry/STATUS/todoregistry all say #33).*

## 0. Where we stand (verified, all committed, pushed to origin/master on request)

- **REGISTRY**: 91 works / **33 gold** / 58 pending. (92→91: paramadvayadvadashika merged as variant title — see §1.)
- **Gold #30 dehastha** (16v, 2 songs): Abhinavastotravali print, full pipeline, CANONICAL 0 failures.
- **Gold #31 paramarthadvadasika** (13v, 2 songs): Sferra/Hamburg recension; Abhinavastotravali print recorded as variant recension (v9/v10/v12/v15 etc.), never built.
- **Gold #32 rahasyapanchadashika** (16v, 2 songs): Abhinavastotravali print, full pipeline, CANONICAL 0 failures.
- **Gold #33 mahopadeshavimshatika** (20v, 2 songs): Abhinavastotravali print, full pipeline, CANONICAL 0 failures.
- Each gold: validate 0 ×N · proof PASS ×N · roundtrip 0 · qa NEEDS_WITNESS (honest, no witnesses vendored) · site ABSTENTION skeleton in /root/ipvv (uncommitted there — owner commits ipvv separately).
- Six earlier golds' qa re-run vs vendored legacy-L2 witnesses: SHIP_AS_IS (+2 WITH_NOTES, both adjudicated on record).

## 1. Owner directive 2026-11-04 (binding): all Abhinavagupta works, shortest first

- Completed Abhinavagupta stotras/prakaraṇas (gold): anubhavanivedana 4, pancashloki 5, anuttarastika 8, paramarthacarca 8, bhairavastava 10, paramarthadvadasika 13, bodhapancadasika 15, dehastha 16, rahasyapanchadashika 16, mahopadeshavimshatika 20, kramastotra 30, ptvmadhyama 35, paratrimshika 36, paryantapancasika 52, paramarthasara 105, tantrasara-a01/a02.
- **Next**: tantrasara-a18(2) → a17(6) → a19(7) → a12(10) → a21(13) → a10(18) → a16(24) → a11(25) → a07(28) → a03(34) → a05(43) → a04(46) → a09(53) → a22(53) → a20(65) → a06(82) → a08(93) → a13(101) → a14/a15 (prose, 0 verses) — verse counts from INDEX.json.
- **Then**: tantraloka-a34(4) → a18(11) → a20(16) → a36(16) → a24(24) → a12(26) → a25(29) → a33(32) → a35(44) → a14(47) → a22(48) → a02(50) → a19(56) → a27(59) → a21(61) → a32(68) → a07(71) → a26(76) → a37(85) → a23(103) → a11(118) → a17(122) → a30(123) → a05(159) → a31(164) → a06(252) → a04(279) → a29(292) → a03(295) → a10(310) → a16(311) → a09(314) → a01(333) → a13(362) → a28(435) → a08(452) → a15(613) — counts from /root/ipvv/site/data/sanskrit/tantraloka.txt GRETIL markers.
- **Explicitly OUT of this goal**: tattvasandoha (Kṣemarāja — verified via Jaideva Singh intro, Wikipedia, McNally Jackson, Vishvasa bibliography; stays no-repo general queue), parapravesika (Kṣemarāja/Nāgānanda wrinkle → Kṣemarāja per works lists), sambandhasiddhi (gold; attribution uncertain, excluded pending verification), all non-Abhinavagupta golds (Somānanda/Utpala/Vasugupta/Kallaṭa/Kṣemarāja/Bhaṭṭa Nārāyaṇa/Kālidāsa works).

## 2. Duplication audit #2 (owner decision executed: single gold)
- paramadvayadvadashika == paramarthadvadasika (colophon: "paramādvayadvādaśikā athavā paramārthadvādaśikā"; both 13v; same Ramyadeva seal). Unlike the ptv recension pair (both already gold before audit), nothing was built here — so: ONE gold from the Sferra recension (SOURCE.txt in-repo), Abhinavastotravali print kept as recorded variant. Registry entry merged (92→91). Reversible: variant readings preserved verbatim in lore + argmap uncertainties.

## 3. Working notes for the next agent
- New-work drill (proven: dehastha→mahopadeshavimshatika in one session each): websearch source (sanskritdocuments .itx preferred, Ruma Dewan) → curl .itx to <work>/cm/source.itx → parse verse blocks (strip TeX, drop parenthesized print variants WITH lore note, join wrap-hyphens, one IAST line per verse) → transliterate indic-transliteration → segments-input.json → intake.py → lore-2026-11-04.md (lore search = the acquisition search + Dyczkowski/Hareesh where available) → T1 (span-exact assert) → build_l0.py from cm/*.json (citation IAST + analyzed morph + grounds; enrich forks by hand after) → argmaps (zero-shared scan) → L2 → C1 (0 quotes/meta/shared scans) → data emit + T1/L2 MDs + jsonl/reports + C1 MDs → validate/proof/roundtrip/qa → L3 (0-shared audit) → L4 (craft_notes + audit vs own L3, mistakes.md #19) → C2 (render_c2 --print-prompt, [E#] tags) → c1.NOTE → data l3 emit → gates → STATUS → check.py → gold commit → REGISTRY/todoregistry → push when asked.
- Known byte-quirk pattern: fused spans (vaṭukamapānābhidhaṃ-style), avagraha-initial tokens ('sīti, 'tra, 'khilam, naTavan print-slip for naṭavat, double visarga tattvataḥḥ, ṃ/ṅ sandhi forms). Keep byte-true, gloss sense, flag in lore/L0 grounds.
- mistakes.md #19 enforced on all four golds (L4-vs-L3 overlap audits, all ≥0.83 except the fixed vbt case).
- ipvv writes (site/data/translations/*.json ABSTENTION skeletons) are uncommitted in /root/ipvv — owner's repo, owner's commit.

## 4. Standing owner items
- First-verse L4 voice verdicts (all recent golds) + human review of every machine-proposed stack. Nothing marked final.
- ptvmadhyama re-aim (Vivṛti) vs recension pair; paratrimshika↔ptvmadhyama cross-links already in STATUS+lore.
- Push cadence: push only when asked (Rule 1); this session pushed 29→33 + merges on explicit request.
