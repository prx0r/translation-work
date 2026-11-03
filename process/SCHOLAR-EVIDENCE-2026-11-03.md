# Scholar evidence projection recovery

`tools/emit_scholar.py --work <work>` now adds `source_verses` and `l4_craft`
to the existing generated Scholar projection. The projection is read-only and
never changes translation data or ledger authority.

`source_verses` reuses matching, PASS-gated verse displays from the ipvv site
with their existing provenance and license fields. If a legacy site file is
passage-shaped, only the audited Paramārthasāra/Kramastotra mappings or a
byte-pinned intake manifest may supply parser-reconstructed verse tokens; the
result is clearly labelled and carries the source file hash. Other missing
source displays stay missing until their mappings are audited. Consumers must
check the cited edition and must not treat display text as a new source edition.

`l4_craft` includes draft craft, rejected readings and rationale only when the
draft's complete nested L4 object exactly matches the currently projected,
proof-eligible L4. Each item records both draft-file and canonical-object hashes.
It does not grant human approval or assert scholarly correctness. Missing,
blocked or stale-proof source and L4 material remains unavailable. Existing C2
eligibility rules are unchanged.

This is only an evidence projection. No private account workspace, Qwen integration,
voice relay or publication feature is supplied by this change. The earlier local-only
Scholar suite commits were lost with their temporary workspace and are not on GitHub.
See ipvv `process/SCHOLAR-RECOVERY-2026-11-03.md` for the recovery status and
remaining account-security work. Run `python3 check.py` and
`python3 -m unittest tests.test_scholar_p0` before publishing these changes.
