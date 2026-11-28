# SOURCE-INTAKE.md — extending the corpus beyond Muktabodha (2026-11-15)

*The burn can only translate what has a Sanskrit source. The Muktabodha set is
499 e-texts; the openpatala availability index knows 743 works. This file
tracks the gap and how an external text joins the burn.*

## The gap (measured)

| Bucket | Count |
|---|---|
| Availability index works | 743 |
| With a Muktabodha catalog / e-text (burnable) | ~495 |
| No-catalog rows, **matchable** to a local source | 30 (already in the burn set / aliases) |
| **No source on box (need acquisition)** | **218** |

The 218 include the big Kula canon the Trika commentaries lean on:
`jayadrathayamala`, `brahmayamala`, `siddhayogesvarimata`, `kularatnamala`,
`kaulajnananirnaya`, `kiranatantra`, `parakhyatantra`, `ajitagama`,
`matangaparmesvaragama`, `pauskaragama`, `sarvajnanottara`,
`sardhatrisatikalottara`, `trisirobhairava`, `nisvasaguhyasutra`, …

## How an external work joins the burn (the contract)

No registry edit needed. `tools/workcfg.work_config()` resolves any dir with a
`source/manifest.json` (format `source-intake/1`) that validates via
`tools/intake.py`:

```
<slug>/source/edition.txt     UTF-8 Sanskrit (IAST), verse text
<slug>/source/segments.json   [{song, verse, verse_id, start, end}] tiling edition.txt
<slug>/source/verses.json     [verse strings] (for coverage + stage_parse)
<slug>/source/manifest.json   format/source_sha256/segments_sha256/edition/license
<slug>/STATUS.json            so burn_wave includes it
<slug>/passages.jsonl         ~25-verse groupings
```

Then: `python3 tools/intake.py --work <slug> --source edition.txt --segments seg.json …`
(or `intake.initialize()`), and the burn picks it up (see `burn_wave.sh`, which
also iterates `ext-*`). Constraints (`intake.validate_segments`): segments must
tile the whole file, unique positive verse numbers, `verse_id == <song>-v<N>`.

## Work #1 — Jayadrathayamala (JYĀ)

- **Source found & acquired:** archive.org item, *Jayadratha Yamalam Part 1
  (Pāṭala 51, 5467 ślokas)*, ed. M. Sampath Kumar under M. Dyczkowski,
  **license: CC0 1.0 (public domain)**. Saved: `process/intake/jya-p1-ocr.txt`
  (Devanagari) + `jya-p1-iast.txt` (IAST, via `indic_transliteration`).
- **Scope:** this is Part 1 (one ṣaṭka region, ~5,467 ślokas) of a ~24,000-verse,
  4-ṣaṭka text. The rest is not in this item.
- **Blocker — OCR quality:** ~49% of lines are clean IAST; the rest are OCR
  noise (`kataṃvyaṃ`←`kartavyaṃ`, `nivāṃsyaṃte`, stray `OO` / `Sampath_eBooks`).
  **Mass-seeding garbled OCR would produce junk translations** — it violates the
  same quality bar we just fixed for the burn. So it is **not seeded yet.**

### To unblock JYĀ (choose one)
1. **Clean the OCR** (recommended): a Devanagari-aware correction pass
   (dictionary/lemma-constrained) + a human spot-check, then intake + pilot.
2. **Find a cleaner digital edition.** The archive item is the Sampath/Dyczkowski
   transcript; a cleaner IAST source (or the IFP critical edition, if licensed
   for use) would remove most noise. Check the HF `kashmir-shaivism-corpus`
   "Jayadratha Yamalam" extract, GRETIL/SARIT, and the IFP edition.
3. **Accept a noisy draft** (not recommended): intake as-is, burn, and label
   every verse `OCR_UNVERIFIED`; the assessor must re-read against the PDF.

## Standing rule
Source first; then **pilot one passage** and inspect T1/L0 before scaling a new
external work. Volume is never a reason to burn known-garbled text.

## Next actions (autonomous queue)
1. Add OCR-cleaning pass for JYĀ (Devanagari→IAST already done; correction next).
2. Batch-check the other 218 for public-domain e-texts (GRETIL/SARIT/archive.org);
   record per-work `source_url` + license in this file.
3. Intake + pilot the first external work once a clean text exists.
