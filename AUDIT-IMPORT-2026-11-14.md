# AUDIT IMPORT — 2026-11-14 (external audit vs live state)

**Source:** `s3://ayoutube/translation-work-audit-2026-11-14.zip` (6.6 KB;
`README.md` + `sources.json`). Imported 2026-11-14 ~10:05 UTC. External
read-only audit; made no repo changes and opened no PR.

**Method it used:** GitHub read APIs, **no checkout**. It audited the default
branches as it saw them. This is the single most important context: **it did
not see the live tree.**

## 0. Scope mismatch (read this first)

| Repo | Audit saw (default) | Live HEAD here | Gap |
|---|---|---|---|
| translation-work | `master` @ `c2c1672` | `burn/muktabodha` @ `9ce12b1` | **+1,082 commits** |
| trika-x | `main` @ `50f06c7` | `bridge/trace-refresh` @ `5ae1af4` | +5 ahead of main |
| openpatala | `master` @ `85a0dbd` | branch @ `0bd247a` | +1 |

Everything the audit says about `proof_record.py`, Bodha, `formalization.json`,
and the evidence bundle was true **of `master`**, which is the pre-burn state.
It never saw: the Tantrasara/ipvv exposure work, the 2,621-trace publish,
`audit_align`, the disposition key-hygiene fix, the kularnavatantra close-out,
`skills/proof/SKILL.md`, or the 36-tool MCP surface. **Recommendation to the
auditor: re-run pinned to `burn/muktabodha`.**

Its findings are nevertheless largely still valid on the live tree — verified
below. Accurate, but under-scoped.

## 1. Finding-by-finding adjudication

### F1 — "Proof has several meanings; don't read PASS as translation-correct." ✅ VALID, already addressed this session
Verified: `proof_record.py` is a deterministic structural gate (align/parse/
schema/citations/heuristics), not a correctness proof. **This is now the
explicit content of `skills/proof/SKILL.md`** ("PASS certifies the contract,
not scholarly correctness") and is servable to ChatGPT via
`shastra.skill("proof")`. Status vocabulary the audit proposes
(`structural_gate_pass`, `source_pinned`, …) is a good P0; our doc states the
scope but does not yet emit a machine status enum. **Backlog (small): add the
enum to proof records.**

### F2 — "Bodha STATUS says proof PASS but GATE.json marks 8/15 BLOCKED." ✅ VALID, real ambiguity
Verified on live tree: `bodhapancadasika/STATUS.json` `counts.proof = "PASS"`
(all 15 per-verse `proof_record` gates PASS), while `GATE.json` has entries
BLOCKED on `CITATION_GROUNDING` (a *different*, stricter, legacy gate —
technical terms must appear verbatim in that verse's source). Two gate systems,
one unlabelled aggregate. Not fraudulent, but genuinely ambiguous.
**Backlog: label the aggregate by gate; make the badge impossible unless all
publication-required gates pass.** The audit's "add a test that the aggregate
is derived from current per-gate receipts" is the right fix.

### F3 — "`source_sha` is only the first 16 hex chars (64 bits) of SHA-256 over
normalized tokens, not raw bytes." ✅ VALID — **FIXED this session**
Verified: `def sha(s): return hashlib.sha256(...).hexdigest()[:16]`.
Both weaknesses noted (truncated; normalized text not raw bytes).
**Fix applied (additive, backward compatible):** proof records now emit
- `source_sha` — unchanged 64-bit normalized digest (existing consumers safe;
  it is exactly the first 16 chars of the full digest),
- `source_digest_normalized_sha256` — full SHA-256 of normalized token text,
- `source_sha256_raw` + `source_sha256_raw_file` — exact raw source-file bytes
  and path.
Demonstrated on `bodhapancadasika/proof/proof-bod-p01.json`
(`source_sha256_raw = 924003d3…`). Not mass-regenerated this pass (would
trigger a trace/verify publish cycle); future re-proofs carry the fields.
**Backlog: one full re-proof sweep to populate all records.**

### F4 — "Lean proves the modeled proposition, not that the Sanskrit entails it;
139 theorems, 0 Core, all Frontier, self-assessed, no scholar review." ✅ VALID (trika-x lane)
Verified exactly: `formalization.json` → `{theorems:139, core:0, frontier:139,
sorry_count:0}`, `review.status = "self-assessed", "No scholar review yet"`.
This is a **formal-trika lane** concern, not translation-work. Our
`skills/proof` wording already refuses to conflate them. **Backlog (trika-x):
per-theorem statement + assumptions + evidence tier + separate
statement-mapping review gate.** Not this lane's to fix; recorded.

### F5 — "OpenPāṭala evidence bundle is stale (2026-08-17, commit pinned)." ✅ VALID
`openpatala/data/evidence/evidence-bundle.json` timestamp `2026-08-17T12:42Z`,
commit field unpinned in what we checked. `check.py` proves presence, not
currentness. **Backlog (openpatala lane): regenerate as a CI artifact from a
disposable DB; `check.py --status` should report STALE ≠ success.**

### F6 — "Want a machine-readable cross-repo release lock (`federation-lock.json`)." ✅ VALID, good idea
Agreed with the audit. Pinning repo commits + artifact hashes + tool/schema
versions in one file, checked by each consumer, prevents a live site silently
combining current translation data with a stale formal receipt. **Backlog
(cross-lane P2).**

## 2. Where the audit is wrong, or right-but-stale

- **"No repository checkout was available"** → it audited `master`. Its
  executive summary ("promising pipeline, proof labels must not be read as
  correctness") is *more* true of `master` than of the live tree, which has
  1,082 commits of hardening the audit never saw.
- Its Bodha example is still accurate, but the `GATE.json` it cites is the
  legacy citation-grounding gate; the audit correctly suspected "two gate
  implementations" — confirmed.
- No error found in its technical claims. Its SOTA framing (Lean kernel vs
  statement meaning; autoformalization bottleneck) is sound and worth heeding.

## 3. Actions this import triggered

- [x] Add full-strength source identity to proof records (F3) — done, additive,
      demonstrated on bod-p01.
- [x] Keep "proof ≠ correctness" as a servable doc (F1) — already in
      `skills/proof`, now cross-referenced here.
- [ ] P0: status enum + remove ambiguous aggregate PASS (F1/F2) — next.
- [ ] P1: full re-proof sweep to populate `source_sha256_raw` everywhere (F3).
- [ ] P1 (trika-x): Formal-trika statement/review gates (F4).
- [ ] P2 (openpatala): current-evidence-bundle CI artifact + STALE status (F5).
- [ ] P2: `federation-lock.json` consumed by all three repos (F6).
- [ ] Ask the auditor to re-run against `burn/muktabodha`.

## 4. Verdict

**Trustworthy audit, wrong snapshot.** Every checkable claim held on the live
tree; the one that mattered for hashing is now fixed; the rest is a
well-prioritised backlog split across lanes. Treat `master` as a stale
public face — the live work is on `burn/muktabodha`, and that should probably
be reconciled (merge master ← burn, or make burn the default) so external
audits and consumers see reality.
