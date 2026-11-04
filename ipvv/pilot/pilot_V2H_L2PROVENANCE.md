# IPVV — V2-H: L2→L0 provenance (paragraph-level)

*2026-08-11. **Prototype** of the L2→L0 traceability layer (Option 2.2). Each L2 paragraph-block of
`pilot_V2H_L2_read.md` is anchored to (a) the T1 chunk lines, (b) the L0 record-id range, and (c) the
raw source lines (M00021). The chunk line == the L0 `line_id`. Finer sentence/span alignment is added
only where a decision is disputed, an apparatus entry exists, the QA scaler flags it, or a scholar asks
to inspect it — not for ordinary prose.*

**Keying:** `V2-H` = chunk `chunkV2-H-pancamo-vimarsa-k11-13.md`; L0 file
`l0/chunkV2-H-pancamo-vimarsa-k11-13.l0.jsonl` (3162 records, chunk lines 9–172); source M00021.

---

## L2 paragraph-block anchors

| L2 ¶ (opening words) | T1 chunk lines | L0 records | source (M00021) |
|---|---|---|---|
| "Here, in the deepest part… the manifestation (prakāśa) is not passive" | 49–52 | L49:T501 → L52:T831 | 5200–5215 |
| "Consider the very first surge… the paśyantī, the middle-self" | 52 (mid) | L52:T509 → L52:T831 | 5200–5203 |
| "The proof that this is so is drawn from the swiftest of our acts" | 54–57 | L54:T832 → L57:T1016 | 5203–5216 |
| "And this is the will — the first surge, the first tuṭi" (the Śivadṛṣṭi 1.8) | 57 (end)–59 | L57:T1017 → L59:T1018 | 5225–5244 |
| "So the reflexive-awareness is not a thing… it is the parā-vāk" | 59+ | L59:T1019+ | 5245+ |

*Note:* the L2 read is a continuous piece; the block boundaries above are approximate, keyed to the
main argumental turns. Where the scaler flags a specific sentence, refine to sentence-level here.

---

## How to verify a claim

1. Take an L2 sentence, find its paragraph-block above.
2. Open the L0 file, jump to the record range.
3. The records give the Sanskrit lemma + literal gloss for the source the sentence rests on.
4. Cross-check the raw source lines in M00021.

This makes the readable edition auditable without embedding provenance in every sentence of the prose.

---

## Prototype findings (for the QA scaler)

While mapping, note these as **fixtures** (things a scaler should be able to detect generically):

- **Term-policy drift risk:** the L2 says "the light's own grasp of itself" for vimarśa; the ledger is
  "reflexive-awareness." The prose uses a gloss-image, not the locked term — acceptable in READ prose,
  but a scaler should know this is a *prose-rendering* of a ledger term, not a new decision. (This is
  exactly the "prose is allowed to paraphrase, but must not silently re-decide the term" rule.)
- **Speaker:** the whole block is Abhinava's voice; the Śivadṛṣṭi 1.8 verse is quoted — a scaler
  should confirm the quote boundary is marked (it is, in the chunk).

---

## Next (when scaling)

- Generate these provenance tables for every L2 file (Vol 1 A–N, V2-A…S, V3-A…P).
- Keep them in `l0/` or a new `provenance/` dir, one file per chunk, named `<chunk>.l2provenance.md`.
- The QA scaler reads these tables to (a) verify every L2 block has a non-empty L0 range, (b) flag
  blocks with suspiciously large ranges (possible lost-proposition / compression), (c) drive the
  fine-alignment only where flagged.
