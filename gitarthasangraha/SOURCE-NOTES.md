# gitarthasangraha — source & segmentation record (2026-11-04)

*Source: Muktabodha M00244, Gītārthasaṃgraha, ed. Laksmana Raina (Lakshman Joo),
Kashmiri Pratap Steam Press 1933 · CC BY-NC 4.0 · IAST transliteration.
Fetched 2026-11-04, vendored to ipvv site/data/sanskrit/gitarthasangraha.txt
(complete through its colophon: paripūrṇo'yaṃ … gītārthasaṃgrahe … iti śivam).*

## What this text is (scholarship checked, websearch 2026-11-04)

- Abhinavagupta's Gītārthasaṃgraha = the Bhagavadgītā **in the Kashmir
  recension (K)** with his Śaiva commentary — NOT the vulgate (V).
- K has **extra verses and shifted numbering** vs V. Independent confirmations:
  - Bansat-Boudon & Törzsök, "Abhinavagupta on the Kashmirian Gītā" — first
    critical edition underway (K from 1 K Devanāgarī + 7 Śāradā MSS);
    K-vs-V differences include added verses (e.g. 1.1 sarvakṣatrasamāgame).
  - Bansat-Boudon (2016-2018), "Le Gītārthasamgraha" (ASR) — K recension from
    Abhinavagupta himself as Kashmiri.
  - Schrader (1930): K = 14 whole + 4 half stanzas beyond V; Belvalkar/Edgerton
    disputed K's priority; controversy unresolved → **translate K as our text
    stands, mark recension notes, never silently harmonize with V.**
  - Pandita (shardapaakjod.in): "fifteen additional verses"; Marjanovic: same.
  - wisdomlib critical study: K counts per chapter 47,74,48,42,29,49,30,28,35,
    42,60,20,35,27,20,24,28,78 (+6 benedictory + 4 closing saṃgraha).

## Segmentation (tools in /tmp/opencode/gita-seg2.py — one-off, reproducible)

**Unit = verse-block: Gita mūla verse (marker `|| A-V ||`) + Abhinavagupta's
commentary on it up to the next marker.** Work-level: 19 songs = intro (6
benedictory verses, `gita-a00`) + 18 adhyāyas (`gita-a01..a18`). Absolute
verse ids gita-aNN-v<abs>; abs 1..740 (6 intro + 717 verse + 17 saṃgraha
closers counted per adhyāya… totals: 740 = 6 + Σ(75,49,43,…)+18 saṃgraha).

Mechanics (byte-exact, intake-validated):
1. Join wrapped markers: line ending `||` + next line `N ||` or `||` merged.
2. `athā…'dhyāyaḥ` headers open adhyāyas; `atra saṃgrahaślokaḥ` opens the
   adhyāya's saṃgraha unit; adhyāya unit ends at colophon line.
3. Verse unit start = backward walk from marker collecting verse-like lines
   (no `||`, no final prose punctuation, blanks ≤2), floored at previous unit
   start; cap 20. Word-cues (itra/iti/…) deliberately NOT used as exclusions —
   K mūla legitimately begins `atra śūrā…` (verified line 103).
4. Ch1 markers restart (intro shares 1-x labels) → intro bounded by first header.

**Counts verified vs source: 740 units, 0 coverage gaps/overlaps, 0 empty.**
Per-adhyāya unit counts (incl. saṃgraha unit) match wisdomlib's K counts + 1
saṃgraha each: a02 75=74+1, a03 49=48+1, a11 61=60+1, a18 79=78+1 …
(the +1 anomaly in early checks was unit-count vs verse-count accounting.)

Known benign anomaly: line 1529 closer prints `|| 27 ||` after the 4-28 verse
block (edition closer-numbering lag; closers never open units).

## Translation implications (for T1 onward)

- **Mūla = the `|| A-V ||` line + collected verse-lines; commentary prose is
  part of the unit's Sanskrit and must be T1'd too** (same as tantrasara units).
- Kashmir-recension verses are REAL text: number by this edition (label kept
  in segments.json), note K-vs-V deltas in lore when they matter (never
  normalize to vulgate numbering).
- Loose ends from this session's reality-checks: ch8 had no 8-8/8-9 markers
  in an early dry-run (fixed by the join rule — markers on split lines); any
  future marker-format discovery goes here.

## Witness candidates (found 2026-11-04, second search)

- **Arvind Sharma, *Gitarthasangraha* (translated, all 18 ch) with Ingalls preface** —
  English witness for qa_vs_witness when vendored/quotable; Ingalls: "the printed
  text is so corrupt that many passages are unintelligible without emendation"
  (Sharma emended via BORI MS 422) → our Muktabodha print oddities are the
  documented corruption, handle as L0 forks, never silently smooth.
- TextGrid TEI Gītārthasaṃgraha (Ishitobi 2020) — collation candidate (header
  attribution says "Yāmuna" — verify before use).
- wisdomlib critical study: "716 ślokas (K) + 6 benedictory + 4 closing saṃgraha";
  per-chapter counts verified earlier; also the Maṅgala-verse numbering 1-6.
