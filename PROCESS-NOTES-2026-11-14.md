# PROCESS NOTES — 2026-11-14 (how to do this work, repeatably)

*Durable operator notes from this session. Not a changelog (that's
`SESSION-NOTES-2026-11-14.md`) — this is the **procedure**: how to validate
the core, author C1, record dispositions, publish, and serve, plus the traps
that cost time. Read with `PROVE-EXPOSE.md` (pipeline), `skills/proof/SKILL.md`
(what a proof is), and `CORE-VALIDATION-2026-11-14.md` (current result).*

---

## 0. The mental model (one paragraph)

Translation is layered: **T1** (quick gloss, full coverage) → **L0**
(term audit, forks live here) → **argmap** (whole-verse argument, adjudicates
forks) → **L2** (readable English, every clause traced) → **C1** (essence:
what the passage *does*). A deterministic gate (`proof_record.py`) checks the
layers are consistent, complete, and honest; `validate_song.py` checks schemas
+ cross-layer invariants. "PASS" means the *contract* holds — never that the
Sanskrit reading is correct. Meaning is judged by the assessor, disposed by a
human. Machines never sign off.

## 1. Validate the core (the honesty check — do this first, always)

```bash
python3 tools/verify_core.py                 # all REGISTRY works
python3 tools/verify_core.py --work tantraloka-a21
shastra.verify_core                          # same, via MCP / ChatGPT
```

It **re-derives** every song's gate from current bytes (never trusts stored
`proof-*.json`) and reports `GATE-OK / REGRESSION / IMPROVED / NO-PROOF /
OUT-OF-SCOPE / VALIDATE-ERR`. A `REGRESSION` (stored PASS, recompute BLOCKED)
means the "gold" claim is false for that song — stop and fix.

**THE #1 TRAP (cost me a full wrong pass): two proof modes.**
- `shastra` mode reads `data/<song>.{t1,l0,argmap,l2,c1}.json`.
- `classic` mode reads `T1-*.md` / `L2-*.md` / `c1/C1-*.md`.
Recompute each song in **its own mode** or the comparison is meaningless.
Mode is authoritative from the proof's `lineage.t1`: a `/data/` path ⇒
shastra, a `T1-*.md` path ⇒ classic. Forcing `--shastra` on a classic work
invents phantom ALIGN/C1 blocks (I reported 11 fake regressions this way).
`verify_core` now derives mode from lineage — trust it, not ad-hoc runs.

## 2. Author C1 essence (the one real gap we fixed)

For minimal-gold śāstra works, C1 is a **per-verse condensed claim**, not
prose copied from L2. The defect pattern: `C1 essence == argmap premise ==
inference == L2` (one sentence replicated 61–85 times). The gate catches it
as `C1_L2_SHARED n`.

Procedure (proven on a07/a21/a26/a32/a37, 353 verses):
1. Read the work's L2 verse-by-verse (`data/<song>.l2.json`).
2. Write a **telegraphic claim per verse** — the meaning compressed into your
   own words (like the tantrasara golds: "World-born glory-natured wombing…"),
   NOT the L2 sentence.
3. **Keep the count identical** — L4 `essence_maps` point at per-verse indices;
   collapsing to one SUMMARY breaks ~60–80 L4 traces (`essence index out of
   range`). This is why a shortcut is not available.
4. Write `data/<song>.c1.json` `essence[]`, then:
   `proof_record --shastra --no-write` → expect PASS with no `C1_L2_SHARED`,
   and `validate_song --song S --work W` → 0 errors.

Do **not** try to derive essence from the argmap when the argmap is itself
the same L2 sentence — there is no deeper claim source; that would be
inventing scholarship. Author it from reading the verses.

## 3. Record dispositions (the honest-exception mechanism)

Sub-0.90 alignment is often genuine sandhi (T1 citation forms vs witness
joined forms). Record it — with grounds — in `tools/proof-disp.json`:

- Key is **work-qualified** `"work:song"` (bare song names collide across
  works — `mukta-m0-p01` lives in 3). `proof_record` prefers qualified keys.
- Each entry named the joint classes and "assessor-verified <date>".
- Batch-classify with `python3 tools/audit_align.py` (sandhi-only vs
  needs-eyes); only sandhi-only is dispositionable. Single-vowel swaps,
  >4-char fragments, and content insertions/deletions never auto-pass.
- Keep key hygiene with `python3 tools/repair_disp_keys.py` after adding.

**tsa-a01 v4 (ratio 0.17) is the extreme case:** pada-split T1 vs a saṃhitā
source — same order and content, near-total re-segmentation. Defensible, but
0.17 is a signal to spot-read, not to rubber-stamp.

## 4. Fix real defects (the repair playbook)

Worked examples this session:
- **Dropped repetitions** (kul-p39): T1 had 5 of 7 source tokens. Restore the
  missing tokens to T1 **and** L0 (with `history[]`), renumber `pada_index`,
  extend argmap/L2 `l0_ids`, re-proof. argmap/L2 often already read the
  repetition — the tokens are the defect.
- **Word order** (kul-p62 v1530): T1 had a token in the wrong slot vs source.
  Reorder T1+L0 (keep ids, renumber), argmap/L2 `l0_ids` sorted by id, re-proof.
  Meaning unchanged; the order was the defect.
- **Extra/inserted tokens** (par-p06 digits): do NOT blind-delete — it may be
  a T1 artefact OR the source parser dropping material. That's source-vs-T1
  adjudication, not a mechanical edit. Hold for a human.
- Every manual T1/L0 change: add a `history[]` entry `{gloss, reason, date}`.

## 5. Audit-import protocol (external reviews)

An external audit is only as current as the branch it read. Before trusting
one: `git rev-parse HEAD` vs the audit's stated commit. `master` here is
~1,000 commits behind `burn/muktabodha`; audits against `master` miss
everything live. Fact-check each claim against the live tree before acting;
record valid / already-addressed / wrong in an `AUDIT-IMPORT-*.md`.

## 6. Publish + serve (the ChatGPT path)

```bash
# 1. proof-side layer (trika-x traces): recompile changed works
python3 tools/make_traces.py --work W        # or --served-untraced
# 2. served projections (translation-work → svread)
python3 tools/make_readable.py --work W      # or --all --publish
# 3. svread publish chain (fail-closed; release_manifest LAST)
cd /root/svread
python3 tools/emit_traces.py && python3 tools/emit_verify.py && \
python3 tools/emit_claim_pages.py && python3 tools/emit_discovery.py && \
python3 scripts/release_manifest.py --write
```

Serving reads `svread/data/scholar/<work>.json` (`source_verses` non-empty =
readable via `scholar__passage_evidence`). Emit is **fail-closed**: any stale
trace aborts the whole publish — fix the trace, don't force. Expect drift
during publish (the loop keeps drafting); converging takes 1–2 refresh passes
and **does not require pausing the loop**.

## 7. MCP surface (what ChatGPT calls)

36–37 tools on `shastra` (see `MCP.md`). The ones for this work:
- `verify_core` — re-verify the core (the honesty check).
- `serve_status` / `make_readable` — readability KPI + the expose button.
- `make_traces` — trace fan-out.
- `health` — one-call loop+quality+progress dashboard.
- `audit_align` — classify sub-0.90 alignments.
- `skill("proof")` — the proof standard, served to ChatGPT.
- `validate`, `gates`, `status`, `recon`, `lore`, `swarm_*`, `promote`.

## 8. Scope discipline (what NOT to do)

- **The product is the Trika core (95 works), not all 492 Muktabodha works.**
  The burn runs in the background; correctness of the core is the priority.
- **4 songs are out of scope by design:** `spanda/span-p04b/05/06` (later
  niḥṣyandas; only vv1–25 are in scope) and `sivasutra/span-p09` (sutras
  76–77 beyond the 75-sutta Kaul recension). Their data exists but they carry
  no proof on purpose. `verify_core` reports them `OUT-OF-SCOPE`, not defects.
- **Never** fabricate Sanskrit to make a gate green; never mass-promote by
  vote; never let a script author prose; never mark PASS from meaning.

## 9. Definition of done (repeated, because it's the point)

Song done = `proof_record` PASS **+** `validate_song` 0 errors **+**
`verify_core` GATE-OK. Work gold = all songs so. And always: *machine-
proposed, needs human review* — the human is the only one who says "correct".

## 10. Fast reference (this session's tools added)

| Tool | Purpose |
|---|---|
| `tools/verify_core.py` | re-derive core proofs; REGRESSION detector; mode-aware |
| `tools/audit_align.py` | classify ALIGN_NODISP: sandhi-only vs needs-eyes |
| `tools/repair_disp_keys.py` | work-qualify disposition keys safely |
| `proof_record.py --no-write` | compute a verdict without writing state |
| `tools/serve_audit.py` / `make_readable.py` / `make_traces.py` | expose pipeline |
| `CORE-VALIDATION-2026-11-14.md` | this session's findings + result |

## 11. Overnight operation (keys, 429, unattended)

**Two Go accounts, both used.** `OPENCODE_GO_KEY` and `OPENCODE_GO_KEY_BAK`
are both $0-tier; `tools/beam_client.py` spreads calls across **both** by a
session-hash rotation (~2× free-tier headroom). Both are in the oracle vault;
the harness exports both each pass (`tools/harness.sh`).

**On 429 (the failover ladder):**
1. Fail over to the *other* key immediately (still $0).
2. If that key also 429s, park that *model* 30 min in the shared
   `process/beam/model_health.json` — every worker honours it, so no hammering.
3. If every model is down, the harness writes `PAUSED`: workers drain, no
   fresh claims; it clears automatically on recovery.

**See it live:** `shastra.quota` (MCP) or `python3 tools/quota_status.py` —
keys loaded (masked), models parked + time left, worker slots, PAUSED, disk.
`shastra.supervise` shows the systemd unit; `shastra.health` is the daily view.

**Overnight safety:** systemd `tal-campaign` is boot-enabled + `Restart=always`;
harness enforces `w1..w5`; disk guard pauses at <2 GB free (auto-clears);
loop commits+pushed to GitHub on green (off-box backup). Disk is the long-term
limit — prune `process/beam/runs` + `git gc` before multi-day runs.

**Start/verify via MCP:**
```
shastra.supervise {"start_missing": true}   # ensure the unit is up
shastra.quota {}                            # 2 keys, parked models, 5 workers
shastra.swarm_status {}                     # queue depth
```
