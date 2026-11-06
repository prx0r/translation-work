# FORMAL-ALIGN — canonical alignment record for trika-x formalisation

*Verified 2026-11-06 against trika-x @ `formal-trika/{EVIDENCE.json,bridge/,tools/evidence_check.py,tools/bridge_resolve.py}` and openpatala box DB (`openpatala_box`). This file is the standing contract; re-verify with the commands below after any passages.jsonl change.*

## What trika-x expects from us (their gates, our obligations)

1. **EVIDENCE chunk locators resolve.** `evidence_check.py`: every `chunks[].locator`
   in EVIDENCE.json must exist in the corresponding work's `passages.jsonl`
   (via `work_of()` prefix map), locators unique + non-empty per file.
   Status: **8/8 resolve** (`tsa08-p01..04`, `tsa07-p01`, `param-p04`, `phr-p04`;
   `vbt` is work-level by design and passes).
2. **Ledger bytes match the pinned snapshot.** `bridge_resolve.py --check --tw <checkout>`:
   all 6 EVIDENCE works' ledgers byte-identical to `passages.snapshot.json`.
   Status: **PASS — 6 works, 45 passage IDs, BYTES_MATCH_SNAPSHOT.**
3. **Immutable identity.** BACKBONE spine requires `immutable_id` per row.
   Status: **909/909 rows carry one; globally unique (0 dupes).**
4. **Locator uniqueness is per-file** (matches the `evidence_check` gate:
   duplicates *within* a ledger fail; cross-work reuse does not).
   Known grandfathered collisions (work-disambiguated in bridge maps, never
   to be repeated in new schemes): `anu-p01..04` (anubhavanivedana ×
   anuttarastika), `par-p01..08` (paramarthacarca × parapravesika).
   Rule for new work: locator schemes MUST be globally unique
   (`chunkId`, `tsaNN-pMM`, `tal-aNN-pMM` all are).
4. **No witness invention.** Witnesses UNPINNED box-wide; `witness_candidates`
   are pointers with provenance, never pins. Our side: never ship a witness
   claim; NEEDS_WITNESS stands until owner decides otherwise.

## Locator inventory (stable — do not rename without trika-x coordination)

| track | scheme | example | rows |
|---|---|---|---|
| ipvv (49 chunks) | chunkId (`chunkA-…` vol1, `chunkV2-A-…`/`chunkV3-A-…`) | `chunkA-svatyandya` | 49 |
| tsa ahnikas (22) | `tsaNN-pMM` | `tsa08-p03` | per-ahnika |
| tal ahnikas (37) | `tal-aNN-pMM` | `tal-a15-p01` | per-ahnika |
| flat works | `<song>-pNN` | `ajad-p01`, `phr-p04` | per work |
| vbt | work-level `vbt` | `vbt` | 1 |

`work_of()` in evidence_check.py currently maps: tsa08, tsa07, param, phr,
vbt, spanda/span. **Extension contract (trika-x side):** when EVIDENCE starts
citing ipvv/tal/new-tsa locators, extend the prefix map + register the work
in `EVIDENCE["works"]` with the ledger path. Our side guarantees: the row
exists, the locator is unique, the bytes are in git, MANIFEST pins the sha.

## Verify (run these; all must pass)

```bash
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work   # snapshot bytes
python3 formal-trika/tools/evidence_check.py --root /root/translation-work          # theorems+locators+coverage
python3 tools/validate_all.py            # includes passages-ledger stage (below)
python3 tools/dbread.py coverage ipvv    # DB passages vs local songs
```

`validate_all` stage `passages-ledger`: every `*/passages.jsonl` row has a
non-empty unique locator + non-empty immutable_id; immutable_ids unique
repo-wide. Fail-closed: duplicates, missing locators, or missing ids fail
the gate before any commit.

## Known deltas (not defects)

- EVIDENCE pins 6 works / 45 passages; the repo holds 909 rows across all
  gold works. The other 864 are the formalisation queue (their gap list =
  Treeka formal-column seed), not a coverage failure.
- MANIFEST.json pins canonical bytes per work; the bridge snapshot pins the
  6 EVIDENCE ledgers. Different scopes, same rule: bytes beat claims.
- Manifest assertions count (box DB 1512 vs manifest note 1532): DB truth is
  the restored box; see DB-BACKBONE.md open questions. Does not affect
  locator resolution.
