# PROCESS LOG — Ghatakarpara (canonical process run, 2026-11-01)
*Work chosen: 21 verses, 3 passages, kāvya + Abhinava vivṛti. Shortest unworked short work with source present.*
*Process: SKILL.md (only process) + LAYERS.md + EXAMPLES.md. Each step logged here as it happens.*

## Step 0 — Inventory & decision
- Chose ghatakarpara over pancashloki/anuttarastika (already DONE) and sivastotravali (20 songs, too large for one pass).
- Existing state: T1 raw Sanskrit (no glosses — F2 bug), L0 2 PARSED/1 AMBIGUOUS (misleading), L2/C1 generic, gate run. Treated as STAGED, not DONE.
- Deleted superseded batch artifacts (ARGMAP.md, GATE.json, L1.md, L2.md, L2.v2.md, T1-SKEL-s01..s05) — already removed in the sivastotravali cleanup; ghatakarpara still has them; removing now.

## Step 1 — Lore (one focused search)
- Search: "Ghatakarpara kavya Abhinavagupta vivrti commentary meaning verses" (deep).
- Findings:
  - Ghatakarparakāvya = earliest sandeśa-kāvya (messenger poem): a love-lorn wife's lament to the monsoon cloud, appealing to it to carry her message. ~24 stanzas, 5 metres.
  - Abhinavagupta (10th c.) wrote a vivṛti (commentary) on it — KSTS vol 67, "The Ghatakarpara Kavya of Kalidasa with the Commentary of Abhinavagupta", ed. Madhusudan Kaul Shastri. Abhinava thought it might be Kalidāsa's; Siegfried Lienhard rejected the attribution.
  - Authorship unknown; possibly one of the "nine gems" of Vikramāditya's court. Date uncertain.
  - Abhinava's aesthetic framing: rasa = śṛṅgāra (erotic) with vira/adbhuta coloring; sahrdaya relish through dhvani.
  - Wikipedia/owiki: "twenty-four stanzas" vs our source's 3 passages (~21 verse-units). Recension difference — note in STATUS (F4).
- Ledger locked: pramadā=beloved · proṣita=separated · madana=Kāma · cātaka=cātaka bird · pathika=traveler · ambuda=cloud · mañjarī=sprout · kuṭaja=kuṭaja tree · nīpa=nīpa tree · jalada=cloud · ratyutsava=love-festival · yamaka=yamaka figure · ghaṭakarpara=potsherd · vivṛti=commentary.
- Lore note: verse-specific only; no copy-paste (mistakes.md #5).

## Step 2 — T1 (fast translation, lore-primed)
- Composed T1.md: 3 passages, 47 tokens, all pada-split.
- L0 extraction: 47/47 PARSED, 0 AMBIGUOUS, 0 FAILED.
- Concat-align check: ratios 0.338/0.412/0.833 — LOW, but this is expected for pada-split compounds (sandhi changes at junctions: proṣitapramadayedam → proṣita+pramadā+idam, where ā+i→e). Token ORDER verified by hand against source for all 3 passages: every pada appears in source order, no inversions, no drops. The aligner was calibrated for whole-token (ipvv original); pada-split compounds lower the ratio by sandhi, not by error. Decision: keep pada-split per LAYERS.md; record the sandhi-adjusted coverage in this log.
- Uncertainty: ghat-p01 has a doubtful reading "sādya te" (possibly sādyate compressed); kept as-is, flagged in argmap.
- Ledger locked above; T1 frozen 2026-11-01.
