# CORE VALIDATION — 2026-11-14

*The owner's priority: volume is not the goal; **proving the Trika core is
actually correct and the pipeline works** is. This is the result of
re-deriving every core proof from current bytes instead of trusting the
stored `proof-*.json` files. Tool: `tools/verify_core.py`
(`shastra.verify_core`). Reproduce: `python3 tools/verify_core.py`.*

## Method

For all **95 REGISTRY works / 322 songs**, `verify_core` recomputes each
song's deterministic gate (`proof_record --no-write`) and schema/cross-layer
validation (`validate_song`) from current data, then compares to the stored
claim. It writes nothing. It also reports the align min-ratio distribution
and how many verses lean on a recorded disposition.

## Headline

- **307 / 322 songs: GATE-OK** — stored PASS reproduces from current bytes.
- **4 NO-PROOF** — `sivasutra/span-p09`, `spanda/span-p04b/05/06` (loop
  in-flight; tw-assemble owns them — not defects).
- **11 REGRESSIONS** — stored `PASS` but recompute `BLOCKED`. **The core is
  not as proved as its REGISTRY claims.** These fall in 3 classes:
  - **8 × C1_L2_SHARED** — the C1 "essence" is the L2 line verbatim.
  - **3 × real T1 tokenization defects** — T1 carries tokens the source does
    not (or the source tokenization disagrees).

(The 3 `L2_CITE_FAIL` regressions found in the first pass were a false
positive in the gate itself — a cite that re-segments a source compound. Fixed
in `proof_record.py`: occurrence is now letter-level, not space-exact. Those
3 now PASS honestly.)

Align distribution across the core: p10 = 0.907, p50 = 1.000, p90 = 1.000
(most songs align near-perfectly; 66 songs dip below 0.95 somewhere — normal
sandhi/variant territory, only 3 rise to a real block). **43 verses** across
the core rely on a recorded disposition.

## The 8 C1 defects (real; need authorship)

For these Tantraloka/Tantrasara-minimal works the whole stack above T1 is one
copied sentence: `C1 essence == argmap premise == argmap inference == L2`.
There is no independent claim source. Example (tal-a21 v3): all four layers
read "Facing-towards of the disciple consists in becoming the seat of his
grace; …". The proof recorded `c1_l2_shared: []` on 2026-11-01 and was never
re-run — the stale record hid it.

| work | song | shared sentences |
|---|---|---|
| tantraloka-a07 | tal-a07 | 71 |
| tantraloka-a21 | tal-a21 | 65 |
| tantraloka-a26 | tal-a26 | 76 |
| tantraloka-a32 | tal-a32 | 67 |
| tantraloka-a37 | tal-a37 | 85 |

**Why not auto-fixed:** a genuine essence must be supported by the Sanskrit.
The argmap for these works is itself derived from the same L2 sentence, so
there is no deeper claim source to condense from. Writing an "essence" out of
that would invent scholarship — forbidden (a guess presented as fact is worse
than a gap). These need a C1 author who reads the verses. Until then they are
**structurally proved but C1-incomplete** and must not be advertised as full
gold.

Reference for what a passing minimal essence looks like: `tantrasara-a08`
(93 telegraphic claims — condensed, not prose copied from L2) and
`kularnavatantra/kul-p01` (5 sharp claims).

## The 3 T1 defects (real; need source adjudication)

| work/song | verse | defect |
|---|---|---|
| parapravesika/par-p06 | v6 | T1 inserts editorial enumeration digits `1 śiva 2 śakti … 36` and a stray leading `iti` that are not in the source; source prints the bare tattva list |
| sivastotravali/s10 | v15 | T1 has an extra token `tyantatarasutkaṇṭhito'` the source span does not contain |
| sivastotravali/s12 | v3 | T1 has an extra token `padārthadyānsṛṣṭisravadamṛtapūrair` the source span does not contain |

**Why not auto-fixed:** removing a token could be right (T1 artefact) or wrong
(the source parser dropped material). That is a source-vs-T1 adjudication, not
a mechanical delete. Held for assessor.

## What this changes about "95/95 gold"

- 304 songs reproduce cleanly and are honestly proved (structural gate).
- **5 works are C1-incomplete** (essence duplicates L2) — the `C1` layer does
  not do its job. They are gold on T1/L0/argmap/L2/align but not on C1.
- **3 songs carry a T1 defect** masked by a stale PASS.

Recommendation: REGISTRY should not say plain "gold" for these 8 songs until
the C1 authorship / T1 adjudication lands. `verify_core` now makes this
visible on every run and to ChatGPT (`shastra.verify_core`).

## Durable fixes landed this session

- `proof_record.py`: `--no-write` (verify without touching state);
  `source_sha256_raw` + `source_digest_normalized_sha256` alongside the legacy
  digest; L2 cite check now letter-level (kills the 3 false CITE_FAILs).
- `tools/verify_core.py` + `shastra.verify_core`: the honesty check.

## Backlog (ordered)

1. **C1 authorship** for a07/a21/a26/a32/a37 (read verses, write real
   passage essences; ~5 sessions). Until then flagged, not claimed.
2. **T1 adjudication** for par-p06 v6, s10 v15, s12 v3 against source bytes.
3. Re-proof + `verify_core` after each fix; re-run until REGRESSION = 0.
4. Then republish traces (proofs changed) so the served claim layer is current.
