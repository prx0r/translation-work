# SHASTRA-MINIMAL — the minimal build for śāstra works (IPVV, remaining Tantraloka)

*2026-11-06. Status: SPEC (machine-proposed, owner review open). Extends `LAYERS.md`,
does not replace it. Where this file conflicts with `LAYERS.md` on śāstra works,
this file wins after owner nod. Stotra works (devotional verse) stay on the full
stack — L3/L4 are their point. Śāstra works (commentary, ritual prose) build here.*

## 0. Why this exists

The full stack (`T1→L0→ARGMAP→L2→C1→L3→L4→C2`) was designed for stotra: short
devotional verses where the song (L3/L4) IS the deliverable. Applied to śāstra —
IPVV (2 MB of kārikā + vivṛti + vimarśinī across 49 chunks, ~178k tokens) or
Tantraloka a15 (613 verses of phonematic doctrine) — L3 couplets + per-verse L4
songs cost more than they transmit. The readable translation (L2) + the argument
(ARGMAP) + a sharp essence (C1) is the deliverable. Songs can follow later; they
must never block proofs.

Rule of thumb: **if the text argues, build minimal. If it sings, build full.**
Tantrasāra/TAL-XS golds already did full — they stand, no retrofit.

## 1. The minimal stack (5 layers, 3 waived)

```
SOURCE (intake-pinned, chunk spans, vol-verbatim — §4)
  → T1  contract token rows: 1 row per chunk (verse = chunk order), surfaces =
        source span tokens byte-exact, quick_gloss hyphenated, paren-free.
        quick_english = chunk prose summary. Coverage judged vs chunk span.
  → L0  per-token rows: options[] with grounds+source, fork none|live|resolved.
        Bootstrap from hand-written T1 docs where they exist (R2 v1 tarball for
        IPVV vol1); every token hand-verified, gaps hand-glossed (never faked).
        AMBIGUOUS stays parse-quality; FAILED = 0 bar unchanged.
  → ARGMAP  scope=passage, 1 row per chunk. Structured preferred
        (speaker/question/premises/inference); unstructured with reconstruction
        prose accepted for pilot prose maps. Adjudicates L0 forks on the record.
  → L2  1 row per chunk: plain exact English, ≥1 l0_id, cite = chunk-span slice
        byte-exact. Rasa where the text has it (śānta/adbhuta in maṅgalas);
        śāstra prose does not need forced rasa — honesty over decoration.
  → C1-ESSENCE  {song, essence[3–6 lines], essence_only:true, renders:{}}.
        No 7-part essay. 0 quotes, 0 metacommentary, 0 shared sentences vs L2 —
        all existing bars stay. rasa{} optional, same contract.
  → (WAIVED: L3, L4, C2 — validators already treat them as optional;
        proof never required them. No schema change needed for the waiver.)
  → Proof-SHASTRA  PASS per chunk (§3) → emit_scholar → Scholar hub.
```

What is NOT waived: T1 full-span coverage (vs chunk span, not tool report),
L0 100% PARSED-or-AMBIGUOUS with FAILED=0, fork discipline (grounds or it does
not exist), 0-shared sentences (L2 vs essence, argmaps across chunks),
byte-exact cites, `check.py` CANONICAL 0 failures.

## 2. Schema delta (additive, minor bump)

`schemas/c1.py`: allow essence-only. When `essence_only is true`, `renders`
may be `{}` and the standard-sections check is skipped; `essence` non-empty
and all prose bars (quotes/meta/shared) still enforced. `SCHEMA_VERSION`
1.3.0 → 1.4.0; `stack.json` + `DATATYPES.json` + this spec updated in the same
commit; `check.py` must pass on all songs before landing (CANONICAL protocol).

```python
# schemas/c1.py — in validate(), after REQUIRED check:
if obj.get("essence_only") is True:
    if not isinstance(obj.get("renders", {}), dict):
        out.append(err(path, "renders must be an object (may be empty when essence_only)"))
    # skip standard-sections check; prose bars below still apply
    ...proceed to rasa/derivation checks, skip §renders.standard block...
```

Full-stack songs are unaffected (no `essence_only` flag → current behavior).

## 3. Proof delta (`proof_record.py --shastra`, to be implemented)

Current `proof_record.py` is sivastotravali-shaped (UtSst markers, `[and]-`
parse, `C1-*.md`/`L2-*.md` MD paths, `The Sanskrit:` cites). It cannot run on
chunk works. `--shastra` mode:

- B1 source: `workcfg.source_spans(work)` chunk span (already the fallback
  path); verse identity = chunk order, not GRETIL markers.
- B1 L0: read `data/<song>.l0.json` (contract rows), not `T1-*.l0.jsonl`;
  bar = FAILED==0 (AMBIGUOUS allowed, counted).
- B3 concat-align: T1 surfaces vs chunk-span tokens; sub-threshold chunks need
  recorded dispositions (same `--disp` mechanism, chunk scope).
- B4/B5/B6: read `data/<song>.c1.json` essence + `data/<song>.l2.json`
  plain_english (not MD files); shared-sentences/zero-quotes/metacommentary
  bars unchanged.
- B7 cites: L2 `sanskrit_cite` must occur byte-exact in the chunk span
  (chunk-slice cites, not verse-pair `|` cites).
- B8: `validate_song.py` unchanged (already handles workcfg spans; L3/L4
  optional; C1 essence_only per §2).
- `T1-*.md` prose docs remain as human-readable views; the JSON is canonical.

Until `--shastra` lands, shastra chunks carry no gold proof records (GATE stays
`PROOF_NOT_RUN`). Landed 2026-11-06: per-chunk **inventory receipts**
(`ipvv/proof/inventory-<song>.json`, gate=`INVENTORY`) — presence + vol-verbatim
receipts from existing artifacts, explicitly not gold PASS. Result: 49/49 have
bundle+T1+pilot-argmap+pilot-L2+L2-data+L0-rows; only gap is 14 missing vol1
L0 reports (regenerable at conversion). `proof_record.py --shastra` landed
2026-11-06 (schemas 1.4.0): reads contract data JSON, workcfg chunk spans,
chunk-slice cites, C1-essence; classic path regression-tested (s01 PASS with
disp). Pilot chunkJ first proof: BLOCKED honest (ALIGN 0.265 = 303/899,
C1+L2 missing). Do NOT hand-write PASS.

## 4. IPVV program (49 chunks, ~178k tokens)

Landed 2026-11-06 (verified, in-repo):

- `ipvv/source/edition.txt` (2,041,720 B) + `segments.json` (49) +
  `manifest.json` (`source-intake/1`, sha `db44b7ce…`) — all 49 bundle slices
  byte-verbatim in M00020/21/22 (49/49 exact-sha cross-checked vs
  `source/volumes/*.json`). `workcfg` resolves (`kind: segments`, 49 songs,
  177,954 whitespace tokens). Legacy bundle `start/end` are line coords —
  superseded by byte spans; kept per-segment as `legacy_*` + `vol` note only.
- Song ids: lowercase-normalized (`chunkA-…` → `chunk-a-…`,
  `chunkV2-A-…` → `chunk-v2-a-…`, dots → hyphens); 1:1 reversible map in
  `/tmp/opencode/chunk_song_map.json` — **copy into `ipvv/` before converting
  layer 1** (currently temp-only).
- R2 survey 2026-11-06 (new keys): R2 == repo import, nothing newer finished
  there. `l0_v1` tarball (1.6 MB, 22,064 rows, 28 files: chunks A–N + 14
  k-files) = vol1 T1-doc extractions, staged at `/tmp/opencode/r2/v1/`.
  Full tarball (145 MB) downloading → `/tmp/opencode/r2/` (V2/V3 line-level
  rows; convert, don't trust blindly). R2 creds: S3 keys rotate — do not rely
  on R2 as source of truth; repo is truth.
- Per-chunk conversion order (smallest first; pilot → pattern → batch):
  1. T1 rows: surfaces = span tokens (exact); quick_gloss from v1 rows where
     present, hand-glossed elsewhere. quick_english = chunk summary.
  2. L0 rows: 1/token, options[0] = gloss (source t1-draft), chosen 0;
     hand-verify all; mint genuine forks with grounds; AMBIGUOUS stays honest.
  3. ARGMAP: convert `pilot/*_ARGUMENT_MAP.md` → canonical JSON
     (scope=passage, traces resolve); adjudicate forks.
  4. L2: convert `data/*.l2.json` (rename song, re-trace l0_ids, chunk-slice
     cites byte-exact).
  5. C1-essence: new-write 3–6 lines (0 quotes/meta/shared vs L2).
  6. `validate_song` 0 errors → proof-shastra (§3) → STATUS machine-proposed.
- PILOT: `chunk-j-k1-11-kartapi-kalpita` (verse 10, 899 tokens, smallest).
  v1 covers 303/899 (gap report `/tmp/opencode/chunkJ_gap.json` — copy into
  `ipvv/cm/` at conversion start). ~596 tokens need hand glosses. Has T1 doc +
  pilot argmap + L2 read. L0 report missing (vol1) — generate at conversion.
- Do NOT rename/reformat existing `T1-*.md`, `pilot/`, `published/`,
  `data/*.l2.json` in place — conversion writes new canonical files beside
  them; legacy files freeze (rule 4: never import legacy into new pipelines
  silently — the recipe above is the explicit bridge).

## 5. Tantraloka-18 application

Remaining ahnikas (a01,a03–a06,a08–a11,a13,a15–a17,a23,a28–a31) build minimal
on the same contract (workcfg `taloka` spans already exist; song ids already
canonical `tal-aNN`). XL chunks (a15 613u, a08 452u, a28 435u) are the reason
this spec exists — no L3/L4 until owner asks. The 19 existing TAL golds stay
full-stack (no retrofit, no re-litigation).

## 6. Precedence + landing

After owner nod: implement §2 (schema + version bump + stack.json/DATATYPES),
implement §3 (`--shastra`), convert pilot chunk (§4), then shortest-first.
`check.py` CANONICAL 0 failures before every commit. Every gold is
MACHINE_PROPOSED until human signoff — minimal included.
