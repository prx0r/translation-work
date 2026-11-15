# REPRESENTATION-UNIFICATION.md — proposal (2026-11-15)

*Status: PROPOSAL for owner decision. No files rewritten. Diagnosis first;
the risk is proof↔serve drift, not cosmetic duplication.*

## 1. The situation (measured from current bytes)

From `ipvv/proof/` + `*/proof/` lineages (2026-11-15):

| Representation | Proofs | Read side |
|---|---|---|
| `shastra` (data JSON: `data/<song>.{t1,l0,argmap,l2,c1}.json`) | **772** | proofs + `emit_scholar` |
| `classic` (Markdown: `T1-*.md`, `L2-*.md`, `c1/C1-*.md`) | **266** | proofs; NOT served |
| works carrying **both** `data/` and `T1-*.md` | **124** | ambiguous |

`verify_core` already derives mode from each proof's `lineage.t1`
(`/data/` ⇒ shastra, `T1-*.md` ⇒ classic), so the honesty check is correct
per song. The open question is **which side serving/proofs should treat as
canonical when a work has both.**

## 2. Why it matters

- `emit_scholar` / the ChatGPT MCP read the **shastra** side
  (`svread/data/scholar/<work>.json`). A classic-only gold work is proved but
  not served.
- A work with both sides can have the two diverge (different T1 text, different
  C1). `verify_core` passes per lineage, but a reader gets the data side while
  a human reviews the Markdown side — silent drift.
- Mass-converting is the wrong move: it rewrites provenance and would
  invalidate frozen L3/L4 traces.

## 3. Recommendation

**One canonical side per work, declared, not inferred.**

1. Add a single field to each work's `STATUS.json`:
   `"representation": "shastra" | "classic"` (default: infer from the work's
   existing PASS proofs — majority lineage).
2. Make `verify_core`, `validate_song`, `proof_record`, and
   `emit_scholar` **read that field first**, falling back to lineage only when
   absent. A mismatch (proof lineage ≠ declared side) becomes a named
   `REPRESENTATION_DRIFT` warning, not a silent pass.
3. Canonical assignment rule (proposed defaults):
   - **burn-era `mukta-m*`, `kularnavatantra`, `netratantra`,
     `svacchandatantra` ⇒ `shastra`** (minimal gold, L3/L4 waived, served).
   - **full-stack stotras with L3/L4 (`tantrasara-*`, `ipvv/` chunks,
     `sivastotravali`, etc.) ⇒ keep their existing side** (usually classic for
     the older hand-drafted works; do not convert).
   - **works with both but no L3/L4 ⇒ `shastra`** (serving is the goal).
4. Do **not** delete the other side. It stays as provenance; the field only
   decides which side proofs/serving trust.

## 4. Migration (cheap, reversible)

```
1. Script: infer proposed side per work from PASS proof lineages; write a
   proposal JSON (no writes to STATUS yet).
2. Owner reviews the proposal (124 both-side works are the only decisions).
3. Apply "representation" to STATUS.json; leave data untouched.
4. Wire the 4 consumers to honour it; run verify_core + serve_status; expect
   REPRESENTATION_DRIFT = 0.
```

Effort: ~1 session for the script + wiring; the owner decision is the gate.

## 5. What this is NOT

- Not a re-translation, not a mass format conversion, not a proof rewrite.
- Not a change to the trust boundary: PASS is still a structural contract.

## 6. Owner decisions needed

1. Approve `representation` as the canonical-side field?
2. Accept the default assignment in §3.3, or hand-assign the 124 both-side works?
3. Should classic-only gold works be served (by emitting shastra projections)
   or left as reviewed-but-unserved?
