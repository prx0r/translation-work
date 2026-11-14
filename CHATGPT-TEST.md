# CHATGPT acceptance test — is the estate real and readable?

*Owner-facing test pack. Purpose: let ChatGPT (or any agent with the public
connectors) verify independently that the translation + proof estate is live,
correct, and readable — and return a report we can check against ground truth.
No vibes: every check below has an expected value.*

**What ChatGPT tests is the LIVE box deployment** (`/root/*` checkouts as
currently running), not PR branches. Code under review: trika-x #15, svread
#48, translation-work #21. If the live test passes but a PR is unmerged, the
gap is review, not reality.

---

## 0. Connector setup (do this once in ChatGPT)

Settings → Connectors → Add custom connector → paste each URL:

| # | URL | Expect | Auth |
|---|---|---|---|
| 1 | `https://shastra.svatantrya.net/mcp` | **36 tools** (`shastra__*`) | none — open |
| 2 | `https://book.svatantrya.net/mcp` | **22 tools** (`bookfactory__*`) | none — open |
| 3 | `https://video.svatantrya.net/mcp` | **HTTP 401** (`www-authenticate: Bearer …oauth-protected-resource`) | Cloudflare Access — EXPECT the 401; that *is* the correct current behavior (see §5) |
| 4 | `https://mcp.svatantrya.net/mcp` | federation gateway incl. `scholar__passage_evidence`, `openpatala__*` | none — open |
| 5 | `https://patala.svatantrya.net/health` | HTTP 200 (REST, not MCP) | none — open |

Ground-truth snapshot (2026-11-14 ~09:45 UTC; queue counts drift as the beam
loop runs — see tolerances in §2):

- `shastra.health().progress.queue` ≈ `{done: 9258, pending: 6833, claimed: 3, failed: 1057}` (done/pending move; claimed stays small)
- `shastra.health().gates` contains `VALIDATE_ALL: 0 failures`
- `shastra.health().review` ≈ `{done_triples: 3446, reviewed: 3445}` (reviewed ≈ done; gap < 50 is healthy)
- `shastra.priority(limit=3)` first row: `M00504 amṛteśatantra, 1 verse, untranslated`
- `shastra.validate({work:"kularnavatantra", song:"kul-p01"})` → `errors: []`
- `shastra.serve_status()` first line: `served 92/144` (served only ever grows; unserved shrinks)

## 1. Read tests (in order — paste each call as-is)

T1. `shastra.health()` → whole-estate snapshot. Check: `progress.queue` present, `gates` contains `VALIDATE_ALL: 0 failures`, `review.reviewed` within 50 of `review.done_triples`.
T2. `shastra.serve_status()` → readability KPI. Check: a line like `served 92/144 | audited 107 | …`. Record the numbers.
T3. `shastra.validate({"work":"kularnavatantra","song":"kul-p01"})` → Check: `errors` is `[]`.
T4. `shastra.priority({"limit":3})` → Check: first row is `M00504`.
T5. `shastra.status({"work":"kularnavatantra"})` → Check: returns registry/STATUS info, `lore_brief` path present.
T6. `shastra.skill({"name":"crystal-ipvv"})` → Check: returns the translation law (SKILL text), non-empty.
T7. Federation: `scholar__passage_evidence({"work":"tantrasara-a08","target":"tsa-a08-v01"})` → Check: returns `source.text` starting with `yad idaṃ vibhavātmakaṃ`, plus a `layers` object. **Known issue as of 2026-11-14: the public `mcp.svatantrya.net` returns `ToolError: Passage unavailable or withheld` for this exact call while the on-box federation serves it correctly** — the public deployment is serving stale scholar data. If you still see the ToolError, report `T7: FAIL (stale public deployment)` — that IS the finding, not a test error. If it returns the source text, report `T7: PASS (federation redeployed)`.
T8. Federation: `openpatala__search` (or `openpatala__resolve`) for `kularnavatantra` → Check: returns a work id, not an error.
T9. `https://patala.svatantrya.net/v1/stats` (plain GET) → Check: HTTP 200 with works/editions counts.
T10. `https://video.svatantrya.net/mcp` initialize → Check: HTTP **401** with `www-authenticate: Bearer`. (A 200 here would mean the Access policy changed — report it as a *change*, not a failure.)

**Do NOT call write tools** (`make_readable`, `make_traces`, `assemble`, `promote`, `swarm_decide`, `swarm_seed`, `burn`, `onboard`, book/video `decide/new_book/stage/*`) unless explicitly authorized in the session. Read-only testing only.

## 2. Report template (ChatGPT: fill this in, nothing else)

```
## MCP acceptance report — <date UTC>
Connector setup (which of the 5 URLs worked, tool counts seen):
T1 health: [PASS/FAIL] queue=<done/pending/claimed/failed> gates_green=<yes/no> reviewed=<x/y>
T2 serve KPI: [PASS/FAIL] served=<n/144> audited=<n>
T3 validate kul-p01: [PASS/FAIL] errors=<…>
T4 priority top: [PASS/FAIL] first=<catalog …>
T5 status kularnavatantra: [PASS/FAIL] notes=<…>
T6 skill: [PASS/FAIL] bytes=<…>
T7 passage_evidence tsa-a08-v01: [PASS/FAIL] source_starts_with=<first 40 chars> layers=<keys…>
T8 openpatala search: [PASS/FAIL] work_id=<…>
T9 patala stats: [PASS/FAIL] http=<…> works=<…>
T10 video 401: [PASS=got-401 / CHANGED=got-200 / FAIL=other]
Discrepancies vs ground truth (§0), if any (quote both values):
Uncertain/unclear (anything you could not decide — say so, do not guess):
Verdict: [LEGIT / LEGIT-WITH-NOTES / NOT-LEGIT]
```

## 3. How to return it

Paste the filled template back into this chat. If anything failed, also paste
the raw tool output for that step (truncated to 30 lines). Do not open PRs,
do not write files, do not retry more than once per step (a second identical
failure IS the result — flakiness is data).

## 4. Interpretation guide (for us, not ChatGPT)

| Signal | Meaning |
|---|---|
| All T1–T9 PASS, T10 = 401 | Estate live, correct, readable. Ship/pass review. |
| Counts drift (queue done/pending moved) | Normal — beam loop runs 24/7. Only worry if `claimed` grows or workers = 0. |
| `served` lower than ground truth | Re-emit needed (`make_readable --all --publish`); check loop didn't rewrite projections. |
| Gates ≠ 0 failures, or validate shows errors | Real regression — stop, read the gate output, fix before anything else. |
| T7 fails (no source text) | Scholar projection missing/stale for that work; check `serve_status` for it. |
| T10 returns 200 | Access policy changed — decide if intentional (owner call), else re-apply. |
| "Unclear" entries in report | Treat as FAIL until clarified; ambiguity is not a pass. |
| Any write tool ran unasked | Flag immediately; review what changed. |

## 5. Standing knowns (do NOT file as failures)

- Video MCP 401 is the intended Access gate (owner decision pending), not an outage.
- Public `mcp.svatantrya.net` serves a **stale deployment** (51 tools, old scholar data; the tunnel uses remotely-managed config, so the local `config.yml` does not control it). `T7 unavailable` = redeploy/repoint needed (infra, owner lane) — the on-box federation is green.
- 37 works have no projection yet (unaudited/early burn) and 15 emit empty ones (no proof-complete songs yet / deliberate holds like ghatakarpara) — `served 92/144` already accounts for this.
- Claim/trace counts grow as the loop drafts; only sudden drops matter.
