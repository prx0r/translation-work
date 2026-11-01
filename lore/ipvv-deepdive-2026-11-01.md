# Deepdive — ipvv translation files (full inspection, 2026-11-01)

*Inspected: /root/ipvv site/data/translations/*.json (26 works, 298 chunks) +
works/*/WORK.md + samples/ + R2 references. Read alongside `ALIGNMENT.md` (schema
mapping) and `TENSIONS.json` (frictions). This is the raw landscape, not a plan.*

## 1. Volume

26 translation JSONs: 298 chunks total; ~170 PASS, ~128 BLOCKED (WITHHELD).
PASS-heavy: bhairavanukarana 5/5, bodhavilasa 5/5, paryantapancasika 8/8, phrdaya 5/5,
bhairavastava 8/10, bodhapancadasika 7/15, kramastotra 11/30, tantrasara 7/51, isvarasiddhi 1/7.
BLOCKED-heavy: anuttarastika 0/8, ghatakarpara 0/3, paramarthasara 0/12, paratrimshika 0/4,
ptvmadhyama 0/4, saktavijnana 0/3, sambandhasiddhi 0/3, sivasutra 0/8, spanda 0/6,
stavacintamani 0/12, svabodhasiddhi 0/4, vbt 0/17, tantraloka-a01 0/34.

## 2. Per-chunk shape (what the site actually consumes)

Each chunk: `chunk, verses, sanskrit, gate, blocking[], model, date, status, l1, l2,
checks{SOURCE_BINDING, COVERAGE, ABSTENTION, TERM_CONSISTENCY, CITATION_GROUNDING}.
BLOCKED chunks carry empty l1/l2 (fail-closed) but full Sanskrit. Some PASS chunks
carry a `*T1 frozen 2026-10-30.*` trailer inside l2 (legacy contamination).

## 3. Why things are BLOCKED (honest root causes)

- `ABSTENTION` (candidate repeats source / no translation): the T1-in-batch records
  are raw Sanskrit with a bare `[and]-` prefix and zero English glosses (peer-review
  F2). The gate is right to block them.
- `CITATION_GROUNDING` (technical term used in candidate but not in source): the
  generic 12-term glossary (maya/illusion, shakti/power...) applied to texts where
  the IAST term is absent. This is the generic-glossary problem (T7), not a real
  defect — Trika readings get flagged by a Vedāntic glossary.
- `TERM_CONSISTENCY`: mixed renderings of the same term inside one chunk (e.g.
  Shiva and Siva). Real, fixable.
- `SOURCE_BINDING`/`COVERAGE`: length-ratio heuristics; only fire on badly broken
  records.

## 4. What is missing vs our stack (the gap)

| ipvv layer | ipvv shape (specs/) | ipvv reality | our shape (schemas/) |
|---|---|---|---|
| T1 | MD text chunk, frozen_hash, inline gloss grammar | raw Sanskrit in batches, 0 glosses | data JSON objects, source_sha, history |
| L0 | l0_schema.json: coords + raw_fragment + single gloss + status | extractor counts; 96.4% PARSED overall | options[] with grounds/sources, fork axis |
| ARGMAP | argmap.json: speaker/question/premises/inference, no traces | WORK.md prose + batch records; no committed full L200/C1 for most works | traces, option_choices, scope, structured tier |
| L2 | text + supplied[] + fidelity + derived_from_l0 | committed in batch records as l1_text/l2_text; full L200/C1 unlocatable (F3) | plain_english + cite + l0_ids + supplied/fidelity optional |
| L200 | 8-section audit, MT vs IA, derivation_map | claimed in WORK.md, unlocatable for most | partially via L0 grounds + argmap uncertainties + C1 derivation (deferred, D1) |
| C1 | body 100-450w + sections, requires l200_id | claimed, mostly unlocatable | essence + renders.standard (7-part) + derivation optional |
| GATE | deterministic 5 dims | BLOCKED on ABSTENTION/CITATION_GROUNDING | B1-B8, all machine-checkable, per-song proof JSON |

## 5. The real gold (ipvv gold_records)

`pipeline/gold_records/tantra_text_kramasadbhava_1_8.json` is the template: stages
(T1 with close_translation + reader_draft separated), flags (crux marked, never
smoothed), lexical_decisions + grammatical_notes slots, parallels, lineage
(created_by/derived_from/supersedes), policy (schema/contract versions), review_status.
Shape is right; content is thin (empty decision lists, T1 only). Our anāma record
(2 grounded options + adjudication + history + signoff-pending) is the filled version.

## 6. The 5,601 benchy exemplars

5,552 mitrasamgraha (Gītā, Vedic/General) + 373 Pratyabhijñā/Trika + 278 Śaiva
Siddhānta + 123 Krama. Flat {id, work, source, gold, tradition}. No options, no
grounds, no forks. Good for: Kendall eval on the Trika SLICE, Gītā as negative
control, background term frequencies. Bad for: fork adjudication, training our
task, doctrinal claims (Vedāntic glossary flags correct Trika readings). Rule:
slice only, never bulk, for anything load-bearing.

## 7. The gaps we should actually close (in priority order)

1. **Generic glossary (T7)**: replace the 12-term list with per-work ledgers before
   any term-consistency gate runs on Trika texts. Today our T1 headers are the
   ledger; make them machine-readable (queued).
2. **Unlocatable L200/C1 (F3)**: commit or publish location. Blocks qa_vs_witness
   on those works and blocks any claim about them.
3. **"DONE" vs 0 PASS (F1)**: rename STAGED. Labels are public claims.
4. **T1 raw-Sanskrit records (F2)**: either gloss or rename the stage.
5. **Recension notes (F4)**: one line each (sivasutra 75 vs 77, VBT 161 vs 112
   dharanas, spanda 51 vs 52-53). Counts are claims.
6. **GATE status in Notes (F5)**: so drafts are never cited as results.
7. **`needs` field (F6)**: our proof records now have it; ipvv batch records don't.
8. **Namespace collision (F7)**: works/ipvv vs works/spanda-sutra etc. — decide
   together. We own translation-work/; ipvv owns site/. No collision on our side.

## 8. What we have that ipvv doesn't (yet)

- T1 as living JSON with history[] (not frozen text with a hash)
- L0 options[] with grounds + sources (ipvv has single gloss)
- argmap traces (t1_verse, l0_ids) + option_choices with reasons
- fork axis (none|live|resolved) separate from parse quality
- C1 essence + C2 prompt renders with maps_to enforcement
- rasa notes (optional, unfilled) grounded in Abhinavagupta
- signoff + suggestion + variants + proof B8 + check.py canonical gate
- per-verse GRETIL line anchors (source_lines) for chat citations
- living-translation loop (propose/support/accept, git-diffed, qa_vs_witness)

## 9. What ipvv has that we lack (and should borrow or adapt)

- Passage-scope argmaps (our verse scope misses multi-verse dialectic — T1/T8)
- L200 8-section audit with derivation_map (our L2 traces are verse-grain; T2)
- Published receipts with immutable_ids and evidence hashes (our proof records have
  source_sha + lineage; adding immutable_id is one field)
- Witness-based QA at scale (qa_vs_witness.py exists; we've run it on 5 songs)
- Glossary build from C1 key_terms (build_glossary.py — adapt to our ledgers)
- Recite/karaoke audio alignment (out of scope for translation; site lane owns)
