# Search + Audit + Signature P0 — find anything, prove everything, sign it

Status: **specified + built + tested**. New files only:
`tools/build_search_index.py`, `svread/mcp/audit.py`,
`tools/audit_draft.py`, MCP `search_texts`/`text_themes`/`audit_draft`
(additive tools), plus tests.

Pulled in (adapted, not installed): UNU's role split (specialist per
criterion + editor synthesis + multi-model disagreement surfacing),
LucaAmerio's non-negotiables (no unwritten DOIs, verbatim quote + location,
resolution refused on low confidence), TADDLE's defect taxonomy as a
self-gate on our own drafts, Manubot as the publish-leg reference,
ProReviewer's log-cited judgments (our snapshot hashes already do this).

## Search ("quickly pulling references, categorising texts")

- One index over all canon passages (T1 + quotable layers), pushing
  probes, published essays, glossary terms, theme adjudications.
  Records carry kind/work/ref/gate/license — namespaces, so chat can
  scope per-work with a filter, never a prompt.
- Gate labels enforced at index time (BLOCKED English never embedded)
  and at retrieval (default: PASS/PUBLISHED/OWNER only).
- Embeddings: CF Workers AI bge-m3 (free tier), `question:`/`passage:`
  task prefixes, argmap-question context prepended (Anthropic contextual
  retrieval, already proven in `ipvv/tools/build_embeddings.py`).
- Index lives outside repos (`~/.scholar/search-index/`, `--out`
  overridable): build artifact, not canon. Rebuild on new chunks,
  changed English, changed gates.
- MCP `search_texts`: semantic query → cosine → gate/license-filtered
  refs with source lines. MCP `text_themes`: themes evidence for a
  work/ref (labels, core claims, certificates).

## Audit (reasoning chain gate)

`audit_draft(text, refs, sources)` — every claim traceable or refused:
- dangling marker (citation with no supplied source) → FAIL (invented citation)
- quoted string absent verbatim from a cited source → FAIL
- chunk ref unresolvable or hash-mismatched → FAIL
- external ref (URL/DOI-like) well-formed AND supplied with retrieval note,
  else refused (low-confidence refused)
- paragraph with no citation → warning (uncited, not failed)
- withheld-work chunk → FAIL (unlicensed use)

Output is a receipt: content hash, verifier identity, per-check
pass/fail, verdict, timestamp. TADDLE runs on our own drafts before any
human sees them: defect taxonomy in, fixed-or-blocked out.

## Signature (electronic product → owner id)

No new schema. The tie is three links that already exist, now stated as law:
sign-off binds account + snapshot hash (`SELF_ATTESTED`) → bridge binds
submission to git identity + rights → audit receipt binds content hash to
verifier + verdict. An essay is a signed position: who (account), what
(hash), under which rights, checked by whom (receipt).

## Test plan

- Index builder on fixture tree (gate filtering, license tags, contextual
  prefix, resume/idempotence).
- MCP search/themes against a fixture mini-index (env override), gate
  exclusion enforced.
- Audit core: verbatim-quote pass/fail, dangling marker, hash mismatch,
  external-ref refusal, receipt shape.
- Pilot embed on one work, then full build; retrieval spot-checked.
