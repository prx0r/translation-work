# human_authority — vendored from patalacheckpoints

Vendored 2026-11-03 from `/root/patalacheckpoints` (git `31c376f`):

| File | Original path |
|---|---|
| `contracts_human_authority.py` | `source-evidence/schema/contracts_human_authority.py` |
| `review_engine.py` + test | `pipeline/review_engine.py`, `pipeline/test_review_engine.py` |
| `review_bundle.py` + test | `pipeline/review_bundle.py`, `pipeline/test_review_bundle.py` |
| `patala_ml/goldchain.py` | `machinelearning/research/patala_ml/goldchain.py` |
| `patala_ml/philproof.py` | `machinelearning/research/patala_ml/philproof.py` |
| `tests/test_goldchain.py` | `machinelearning/research/tests/test_goldchain.py` |

Why: the scholar sign-off endgame. `ReviewEvent` is evidence about an EXACT version
(hash-bound), never a mutation; `ReviewProposal → Adjudication → PromotionEvent` is the only
path that changes review state; `goldchain` gives a per-dimension certificate (never one
number). Stdlib-only, no edits made to vendored code.

Verified here (2026-11-03): `test_review_engine.py` 23/23 · `test_review_bundle.py` PASS ·
`tests/test_goldchain.py` 40/40 — 63 checks green.

Usage: `python3 test_review_engine.py` from this directory. Do not edit vendored files in
place — upstream re-import + re-test instead (same rule as `tools/qp_acom/`).
