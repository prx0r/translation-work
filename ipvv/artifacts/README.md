# IPVV — the translation pack

*Target: Abhinavagupta's Īśvarapratyabhijñāvivṛtivimarśinī (IPVV). This is the working
translation pack for the crown. See `corpus/ipvv-anchor/MANIFEST.md` for the full anchor
corpus (primary sources, the 802-paper scholarship, the term-ledger).*

## The stack

```
00_source/   the base texts
   torella_ipk.txt          Torella's ĪPK critical edition + Vṛtti + English translation
                            (the kārikās the IPVV comments on) — the gold-standard base
   (add: the IPVV Sanskrit vols M00020-22 here, chunked per-passage)
01_t1/       working translations (per passage)
02_r1/       adversarial reviews
03_t2/       opposing readings
04_r2/       adjudications
05_t3/       final resolved translations
06_c1/       commentary
```

## The base text (acquired 2026-08-10)

**Torella, *Īśvarapratyabhijñākārikā of Utpaladeva with the Author's Vṛtti* (critical ed. +
annotated English translation, corrected ed. Delhi 2002).** Text-searchable. The kārikās +
Vṛtti the IPVV comments on. PDF also in `corpus/ipvv-anchor/primary/`.

Also: **B.N. Pandit, *The Īśvara Pratyabhijñā Kārikā of Utpaladeva*** (image-scan, for
page-reference cross-check).

## The method

1. Anchor each IPVV passage on the **kārikā** (Torella's text).
2. Recover the **Vivṛti** layer via Ratié's fragments (the IPVV embeds them).
3. Use the **Dharmakīrti/apoha** papers for the Buddhist opponent.
4. Keep the **term-ledger** at Pratyabhijñā-register throughout.

## The layered edition (the derivation stack)

The T1 golden chunks are the **immutable analytical substrate**. Everything else is *derived*
(never edits the chunks). See `l0/L0_EXTRACTION_AUDIT.md` for the L0 validation and
`pilot/pilot_V3B_k1_readable_apparatus.md` for the frozen four-track pilot format.

```
SANSKRIT  (M00022 + Torella)
   ↓
L0  STRUCTURED LITERAL   = T1 chunks (immutable) + t1_extract.py → l0/*.l0.jsonl records
   ↓
L1  CONTROLLED TRANSLATION = proposition-faithful, close to Sanskrit syntax; for COMPARE / audit
   ↓
L2  READ                   = real book prose (derived from L1; never from/over the golden chunks)
   ↓
A1  APPARATUS              = material interpretive departures only (the "would a competent reader's
                             view change?" test)
   ↓
SOURCE-LAYER               = who speaks / what is commented (root/Vṛtti/Vivṛti-recon/IPVV/objection/
                             reply/quotation) — the graph that makes IPVV usable
   ↓
AUDIT_QUEUE                = open cruxes surfaced by L1→L2, incl. UNRESOLVED_QUOTATION,
                             INFERENCE_BLOCK, SOURCE_LAYER_UNCERTAIN, TECHNICAL_MEASURE_OR_REALIA
   ↓
C1  study                  = larger philosophical/philological explanation
```

**Publication views** — the same passage, four views, no duplicated scholarship:

```
READ      L2 only (book prose)
COMPARE   L1 (Sanskrit-close) + L2
LITERAL   Sanskrit + L1 hyperliteral
CRITICAL  L2 + A1 + SL + AQ + evidence + C1
```

Every L2 sentence links to the L1 span(s) → L0 records → Sanskrit, so readability never sacrifices
auditability. **L2 is a distinct prose pass, not a cosmetic polish of L1**: it dissolves `-ness`,
unpacks compounds, breaks impossible sentences, and surfaces (never invents) external-knowledge gaps.
See `CALIBRATION_REPORT.md` for the layer lock and the L2 production rules; the L2 proof is
`pilot/pilot_V3B_L2_proof.md`. **Audit depth follows risk**; the READ edition must be independently
good.

## The pipeline tools

- `translations/tools/t1_extract.py` — T1 → L0 records (raw-fragment provenance, PARSED/AMBIGUOUS/
  FAILED). Backed up to R2 (`sanskritree/ipvv-translations/`).
- Layer lock + L2 rules: `CALIBRATION_REPORT.md`.
- Pilots (L1 + A1 + SL + AQ): `pilot/pilot_V3B_k1_L1_apparatus.md`,
  `pilot/pilot_V3B_k2-7_L1_apparatus.md`.
- L2 proof (READ prose on the hard passages): `pilot/pilot_V3B_L2_proof.md`.
