# SESSION NOTES — 2026-11-14

*One session, start to finish. What changed, what's proven, what's open. The
durable "where we are" is `WHERE-WE-ARE.md`; the prove lane is
`PROVE-EXPOSE.md`; the proof standard is `skills/proof/SKILL.md`. This file
is the dated log for this session only. All work is on `burn/muktabodha`
(master is ~1,082 commits behind — see the audit import note).*

## 1. Orientation + estate truth (start of session)

- Loaded the two laws (`crystal-ipvv`, `largetext`); confirmed the live loop:
  `tal-campaign` systemd → harness → 3 staggered beam workers.
- Found and fixed a **stale-brief bug** in `mcp_server._lore_path()` — burn
  fronts (`mukta-*`, `kularnava`) returned `brief: null` despite the brief
  existing. Now resolves `lore/<work>.md` first.
- Reconciled the MCP tool count (docs said 25/29/19; live was 31→now **36**).
- Snapshotted `WHERE-WE-ARE.md` (the owner was "sorta lost" on state) and
  fixed a real gate regression: `check.py` NOT CANONICAL (proof-s01/02/03
  BLOCKED) → recorded honest sandhi dispositions → CANONICAL 0 failures.

## 2. Prove + expose lane (the ChatGPT goal)

- Built the deterministic pipeline: `serve_status` / `make_readable` /
  `make_traces` / `health` MCP tools + `tools/serve_audit.py`,
  `make_readable.py`, `make_traces.py`. **Readability KPI 56 → 92/144 works**;
  107 scholar projections.
- Fixed the source-audit gate so **Tantrasara (20 ahnikas, 739 verses) is
  readable** (accepted hash-verified `record.json`, not just manifest).
- ipvv: root-caused 3 layers deep (stale locator scheme → only 5 eligible →
  print apparatus in spans); added `is_paratext` cleaning; **ipvv serves 5
  fully-built chunks**, 44 correctly withheld (argmap/C1 await authorship).
- Published the full chain: 2,621 traces (192 COMPLETE / 2,429 PARTIAL) →
  2,621 verify packs (11k+ hashed files) → 2,621 claim pages (131 work
  indexes) → discovery → release_manifest (26k assets). Determinism GREEN,
  mcp unittest green. Converged **without pausing the loop** (refresh-drift →
  immediate republish; fail-closed emit is the detector).
- Filed trika-x#20 for the other agent: the loop-vs-trace race, the
  projection_sha coupling, and 4 deconfliction options.

## 3. Prove-everything waves

- New `tools/audit_align.py` (+ `shastra.audit_align`): replays proof_record's
  exact B3 per BLOCKED song, classifies sandhi-only vs needs-human-eyes.
  Conservative by construction (no single-vowel-swap auto-pass, no >4-char
  fragments, no content insertions, iva/eva forks always human).
- **211 honest sandhi dispositions → 25 songs flipped to PASS**; the
  classifier refused real defects on sight (kul-p39's dropped repetitions,
  transcription omissions) — those went to the repair queue.
- **Caught and fixed a real integrity bug:** `proof-disp.json` was keyed by
  bare song name; names collide across works (`mukta-m0-p01` lives in 3), so a
  disposition could suppress a *different* work's verse. `repair_disp_keys.py`
  re-verified every entry in its owning work and migrated 13 keys to
  `work:song` form; `proof_record.py` prefers qualified keys. One genuine
  fork (m00034 p19 `auditā`/`uditā`) correctly held for a human.

## 4. Kularnavatantra close-out (79/83 gold, was 76)

- **kul-p39**: T1 had 5 of 7 tokens (dropped `yatra yatra … tatra tatra`);
  restored them to T1+L0, renumbered, re-proofed → PASS (0.848 → 1.0).
  The argmap/L2 already read the repetition — the tokens were the defect.
- **kul-p11**: hand-drafted v275 (the only missing verse) — and caught the
  legacy working gloss reading *plurals* where the byte-pinned source reads
  singular feminine. Assembled 25/25, PASS.
- **kul-p62**: hand-drafted v1550; fixed a real word-order defect in v1530
  (`nikṛntaye` was 4th, source has it last); 3 hand-verified dispositions.
  Assembled 25/25, PASS.
- **p64**: 4 enriched-packet retests seeded. **p49/p69/p77**: already fully
  covered by pending worker tasks (no action; drain then assemble).
- STATUS → 79 gold, 0 blocked; gates green; pushed and verified on origin.

## 5. Trust surface + docs

- `skills/proof/SKILL.md` — **what a proof actually is**: the ordered checks
  (verse census, B1 L0 parse, B3 concat-align, B4–B6 C1/L2, B7 byte-exact
  cites, B8 schema+cross-layer), the disposition rules, a verify-it-yourself
  recipe, and the *exact* trust boundary (PASS = structural contract, never
  scholarly correctness). Wired to `shastra.skill("proof")`; verified live on
  the public endpoint.
- `CHATGPT-TEST.md` — acceptance pack: 10 read-only tests with ground-truth
  values, a copy-paste report template, and an interpretation guide. Encodes
  two real findings rather than filing them as bugs: the public federation
  serves stale scholar data, and the video MCP is intentionally 401-gated.
- `PROVE-EXPOSE.md` — the at-scale plan (beams draft layers; expose is
  deterministic joins) and the steady-state publish cadence.

## 6. Third-party audit imported (read `AUDIT-IMPORT-2026-11-14.md`)

- An external audit (`translation-work-audit-2026-11-14.zip`, from R2) is
  technically **accurate** on every checkable claim — but it audited
  `master` (`c2c1672`), which is **1,082 commits behind** the live
  `burn/muktabodha`. It never saw the burn-era or session work.
- Valid and **already addressed**: "proof ≠ correctness" (now the core of
  `skills/proof`); "aggregate PASS ambiguous" (documented; structural-gate
  framing adopted).
- Valid and **fixed this session**: `source_sha` was a truncated 64-bit
  normalized digest. Proof records now also carry
  `source_sha256_raw` (exact source-file bytes, with path) and
  `source_digest_normalized_sha256` (full). Additive; not mass-regenerated
  this pass to avoid a publish cycle.
- Valid and **backlog**: formal theorems are all Frontier / self-assessed /
  no scholar statement-mapping review (trika-x lane, not this lane);
  openpatala evidence bundle is a 2026-08-17 snapshot; want a machine-readable
  cross-repo `federation-lock.json`.
- Mistaken about scope, not about facts: it assumed GitHub `master` is
  current. Recommend the audit re-run against `burn/muktabodha`.

## 7. Numbers (end of session)

- Proofs: **632 PASS** / ~180 BLOCKED (down from 586/185 at session start,
  before wave 1 landed), across 786 songs.
- Kularnavatantra: **79/83 gold** (was 76); p49/p69/p64/p77 draining.
- Readability: **92/144 works served**; 107 scholar projections.
- MCP: **36 tools** live (added `health`, `serve_status`, `make_readable`,
  `make_traces`, `audit_align`); `skill("proof")` live.
- Gates: `validate_all --quick` 0 failures; `check.py` CANONICAL;
  svread publish determinism GREEN; mcp unittest green.

## 8. What's next (unchanged from the roadmap)

1. Drain kularnava p49/p69/p64-retest/p77 → assemble+proof (10 min each on
   completion) → 83/83.
2. Prove wave 2: T1-repair backlog (~400 verses), DATA_OBJECTS/C1_L2 triage,
   netra/svacchanda re-intake (23 songs), the m00034 p19 fork.
3. Serve everything: onboard the 37 no-projection works as data lands.
4. Owner lane: merge PRs #15/#48/#21; L4 voice verdicts; video MCP Access;
   re-run the external audit against `burn/muktabodha`.
