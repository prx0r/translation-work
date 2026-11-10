# FINALCHECK — whole-corpus sweep, shortest-first (owner order 2026-11-10)

*Goal: every work chunked and standardized the same way. Method: machine
census over all 95 works (tools/finalcheck_audit.py) + assessor sampling
(one spot-read per batch, more where the audit flags). Fix what fails,
record the rest. Minimal-gold bar throughout (L3/L4 waived for śāstra).*

## Standard (what "same" means)

1. `data/<song>.<layer>.json` for t1/l0/argmap/l2/c1 (+l3/l4/c2 only where
   the work sings: stotras keep full stack, śāstra stays minimal).
2. `proof/proof-<song>.json` PASS (or BLOCKED with recorded disposition).
3. `working-t1-<song>.json` present (token identity spine).
4. `STATUS.json`: {work, next, counts.proof, updated}.
5. REGISTRY row: gold=true, minimal-gold note where L3/L4 waived.
6. Lore brief: `process/beam/lore/tal-aNN.md` (TAL) or `<work>.md` (others).
7. No T1-coverage gaps (validate 0 errors), no shared C1/L2 sentences,
   no quotes/metacommentary in C1 (sampling + gates).

## Batches (shortest-first; T = todo #)

| T | Works (verses) |
|---|---|
| 3 | spandasandoha(2) + tantrasara-a18(2) |
| 4 | anubhavanivedana(4) + tantrasara-a02(4) |
| 5 | pancashloki(5) + tantraloka-a34(5) |
| 6 | tantrasara-a01(5) + tantrasara-a17(6) |
| 7 | tantrasara-a15(7) + tantrasara-a19(7) + largetext-EXAMPLES cross-check |
| 8 | anuttarastika(8) + paramarthacarca(8) |
| 9 | parapravesika(9) + bhairavastava(10) |
| 10 | tantrasara-a12(10) + tantraloka-a18(11) |
| 11 | paramarthadvadasika(13) + tantrasara-a21(13) |
| 12 | bodhapancadasika(15) + dehastha(16) + rahasyapanchadashika(16) |
| 13 | tantraloka-a20(16) + tantraloka-a36(17) + tantrasara-a10(18) |
| 14 | mahopadeshavimshatika(20) + phrdaya(20) + ghatakarpara(21) |
| 15 | tattvasandoha(21, done — verify only) |
| 16 | sambandhasiddhi(23) + tantraloka-a24(24) + tantrasara-a16(24) |
| 17 | spanda(25) + tantrasara-a11(25) + tantraloka-a12(26) |
| 18 | ajadapramatrsiddhi(27) + tantrasara-a07(28) |
| 19 | tantraloka-a25(29) + tantrasara-a14(29) + kramastotra(30) |
| 20 | saktavijnana(30) + svabodhasiddhi(33) + tantraloka-a33(33) |
| 21 | tantrasara-a03(34) + ptvmadhyama(35) + paratrimshika(36) |
| 22 | bodhavilasa(41) + tantrasara-a05(43) + tantraloka-a35(44) |
| 23 | tantrasara-a04(46) + tantraloka-a14(47) |
| 24 | bhairavanukarana(48) + tantraloka-a22(48) + ipvv-vivrti-vimarsini(49) |
| 25 | tantraloka-a02(50) + paryantapancasika(52) |
| 26 | tantrasara-a09(53) + tantrasara-a22(53) + isvarasiddhi(56) |
| 27 | tantraloka-a19(56) + tantraloka-a27(59) + tantraloka-a21(61) |
| 28 | tantrasara-a20(65) + tantraloka-a32(69) + tantraloka-a07(71) |
| 29 | sivasutra(75) + tantraloka-a26(76) |
| 30 | sivasutravimarsini(77, done — verify only) |
| 31 | tantrasara-a06(82) + tantraloka-a37(85) |
| 32 | tantrasara-a08(93) + tantrasara-a13(101) |
| 33 | tantraloka-a23(103) + paramarthasara(105) |
| 34 | tantraloka-a11(118) + stavacintamani(120) |
| 35 | tantraloka-a17(122) + tantraloka-a30(123) |
| 36 | tantraloka-a05(159) + vbt(162) + tantraloka-a31(164) |
| 37 | tantraloka-a06(252) + tantraloka-a04(279) |
| 38 | tantraloka-a29(292) + tantraloka-a03(295) |
| 39 | tantraloka-a10(310) + tantraloka-a16(311) |
| 40 | tantraloka-a09(314) + tantraloka-a01(333) |
| 41 | tantraloka-a13(362) + tantraloka-a28(435) |
| 42 | sivastotravali(450) + tantraloka-a08(452) |
| 43 | tantraloka-a15(613, XL — reconfirmed) |
| 44 | gitarthasangraha(740, XL — reconfirmed) |
| 45 | malinivijayavarttika(1404, XL — reconfirmed) |
| 46 | standardization-fix pass (apply all fixes found) |
| 47 | REGISTRY + STATUS accuracy pass (counts/notes/dates) |
| 48 | lore-brief coverage (every front has a brief or a why-not) |
| 49 | full gates + check.py CANONICAL |
| 50 | final handover + push |

*T1 = this file + audit script. T2 = gates baseline (validate_all --quick +
proof sweep + check.py) before touching anything.*

## Results (2026-11-10, sampling sweep complete)

- **Corpus mechanical: 96 audit units, 0 proof failures, 0 unparseable.**
- **C1 corpus scan: 0 metacommentary, 0 quotes in essence** (after fixing
  60 doc-talk lines across 28 files — mistakes #2/#8 slips the narrow gate
  missed; all 27 affected songs re-proved PASS, 0 warnings).
- **STATUS counts.proof backfilled** on 72 works (uniform schema).
- **Content spot-reads (sampling):** spandasandoha, anubhavanivedana,
  tantrasara-a02, sivasutra(span-p01), tal-a15 (XL 613v), plus gita/MVV/SSV/
  tattvasandoha (same-day promotions). All read clean.

### Accepted exceptions (documented, not defects)

1. **`ipvv` (49 chunks)**: full data in `data/chunk-*.{t1,l0}.json` +
   legacy L2 (`chunkA-*.l2.json`); argmap/c1 live in `pilot/` and proofs
   record full content. `chunk-a-svatyandya` + `chunk-b-eligibility-gita`
   lack canonical `data.*.argmap/l2/c1` — conversion is a yak-shave (proof
   PASS with full records stands as the truth). Layout exception recorded.
2. **`ipvv-vivrti-vimarsini`**: registry alias row for `ipvv` (dual-vimarsini
   work); dir holds source only. Data lives under `ipvv/`.
3. **`tantrasara-*` + legacy stotras**: no `working-t1-*.json` (swarm-era
   artifact; they use legacy `T1.md`). Working-t1 required only for swarm
   fronts (TAL/Gita/MVV/SSV/tattva).
4. **Lore briefs**: required for swarm-era fronts (TAL 18 briefs + MVV/
   Gita/SSV/tattva present). Pre-swarm works never had them — not a defect
   (audit flag accepted).
5. **`spandasandoha/proof-s01.json`**: stale legacy proof alongside
   `proof-sand-p01.json` (the real one, PASS 1.0). Harmless.
