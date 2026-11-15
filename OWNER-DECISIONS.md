# OWNER-DECISIONS.md — things only the human can decide (as of 2026-11-15)

*Machine proposes; humans dispose. Each item below is a judgment call the tooling
deliberately refuses to make. Ordered by how much it blocks. Nothing here has
been actioned — the code/docs are ready, the call is yours.*

---

## D1 — Ghatakarpara content repair (the 3 `verify_core` REGRESSIONs) — BLOCKING

**State:** `parse_ghata` was reading only the `// Ghk_N //` marker line, dropping
the **first pāda of all 21 verses** from source spans. Parser fixed. Now
`source_spans` covers both pādas, so `verify_core` reports the 3 songs
`PASS → BLOCKED` (align 0.60–0.65): the T1 still has only the second pāda.

- `check.py` + `validate_all` still read the *stored* PASS → **gates stay green**.
  Only the honesty check flags it. Ghatakarpara is **already unserved**
  (`SOURCE_COVERAGE_HOLDS`), so no serving regresses.
- **Your call:** authorize the hand repair — author ~147 first-pāda tokens into
  T1 + L0, rebuild the argmap `sanskrit_sha`, re-trace L2/argmap `l0_ids`
  (adding tokens at the front renumbers every id), re-proof. One work at a time,
  hand-crafted (AGENTS rule 7). Estimated: a proper multi-hour work unit.
  Or: keep it held/unserved indefinitely.

**I did not fabricate the repair** — glossing 147 kāvya tokens without review
would risk exactly the "guess presented as fact" failure.

---

## D2 — `sivastotravali/{s10,s12}`: which T1 convention is canonical?

**State:** both are blocked at 0.838 / 0.886 in **shastra** mode but read
0.994 / 0.997 in **classic** mode. Root cause: source carries
`...sutkaṇṭhito(?)` / `...pūrair(?)`. Two conventions coexist:

| convention | who does it | effect |
|---|---|---|
| **strip** the `(?)`, keep the word | s10/s12's T1 | matches source *after* stripping |
| **drop** the whole token | `is_paratext` + some T1s (e.g. `malinivijayavarttika`) | matches source only if source also drops it |

I tried making `_clean_span` strip instead of drop — it **fixed s10/s12 but
broke `malinivijayavarttika/mv-k07`** (whose T1 had dropped the whole token).
Reverted, because the T1 data itself is inconsistent.

**Your call:** pick one convention, then normalize the 15 affected source tokens
across 7 files and the T1s that follow the other rule. Evidence: 15 total
`(?` occurrences repo-wide — small, bounded.

---

## D3 — Representation: confirm **shastra is canonical**

**Done this session:** 243/245 classic proofs re-proved `shastra`
(`mode` + `lineage` rewritten from data JSON, content untouched; every
recorded `layer_sha256` already matched current `data/*.json` — verified, 0
drift before rewriting). Only D2's two songs are held.

**Your call:** confirm shastra-canonical for the whole core so the classic MD
side becomes a frozen reference (never a proof source again).

---

## D4 — autojunk fix: 11 burn BLOCKED songs now recompute to PASS

`proof_record` B3 used `difflib` autojunk (default `True`), which drops
frequent tokens as boilerplate — wrong for source-vs-translation. Fixed
(mono-tone safe: can only raise a ratio). Measured across all 302 BLOCKED songs
with the fix: **only 11 flip** to PASS (291 stay BLOCKED), so no mass
promotion. Those 11 are burn-era, outside the Trika REGISTRY:

`netratantra/net-p03`, `svacchandatantra/{sva-p01,p02,p11}`,
`mukta-m00005-p10`, `mukta-m00006-p10`, `mukta-m00013-p08`,
`mukta-m00290-p01`, `mukta-m00562-p01`, `mukta-m00642-p01`, `mukta-m00644-p01`.

**Your call:** authorize a re-proof pass over exactly these 11 (stored BLOCKED →
PASS, then emit). I did **not** write them — flipping a gate for works with a
documented re-intake warning (`netra`/`svacchanda`, BUGS #12) is your call.

---

## D5 — MCP auth before wider sharing

`https://shastra.svatantrya.net/mcp` serves **39 tools with no auth**, and
several are write-class (`promote`, `assemble`, `onboard`, `burn`,
`recycle`, `queue_guard --fix`). Logic-gated, not access-gated. Full proposal
(`MCP-AUTH.md`): Cloudflare Access / Service Token in front of the tunnel —
**no code change, ~10 min**. Recommended before any public connector sharing.

---

## D5b — ChatGPT visibility: the public federation is stale AND cannot be repointed yet

**This is the largest gap between "132 works served locally" and a user actually
reading Tantraloka in ChatGPT.** `scholar__passage_evidence` on
`https://mcp.svatantrya.net` returns `Passage unavailable or withheld` for
works that serve fine on-box.

Two separate facts, both verified 2026-11-15:

| | |
|---|---|
| local projection index | **146 works** (`/root/svread/data/scholar/index.json`) |
| public bundle | **55 works**, no Tantraloka, `passage_evidence` fails |
| local federation bridge | **cannot start** — `mcp_bridge.py` → `model_validate_json` `AttributeError` (`typing.Union`, mcp SDK × Python 3.14) → 0 tools enumerated |

**So a "just repoint the tunnel" fix would make it worse.** Required order:
1. Fix the bridge runtime (older Python venv, or a patched/`mcp`-pinned SDK).
   *trika-x lane — I did not edit another lane's repo.*
2. Green the local check: `passage_evidence('tantraloka-a01','tal-a01-v01')`
   and `('paramarthasara','param-p01-v01')` must return real Sanskrit from :8940.
3. Then repoint: GET the remote ingress first (do **not** base it on the local
   `config.yml`, which is a stale fallback), change only `mcp.svatantrya.net`,
   PUT per `MCP-ESTATE.md` §6. The other 4 hostnames ride on that same tunnel.

Until then: **ChatGPT cannot read Tantraloka.** The `shastra` endpoint
(39 tools, healthy) is monitoring/ops, not the reading path.

---

## D6 — standing owner lane (unchanged)

- Merge PRs **#15** (trika-x), **#48** (svread), **#21** (stale snapshot).
- L4 first-verse **voice verdicts** (vbt, tsa-aNN, tantrasara, ghatakarpara…).
- Video MCP Access gate; re-run the external audit against `burn/muktabodha`
  (the prior one audited `master`, ~1,000 commits stale).
- Human review of all 95 works — none have a signoff; `needs:["human-review"]`
  is on every PASS record. Ranked for you by `tools/review_queue.py`.

---

## How to act

```bash
python3 tools/review_queue.py --limit 40      # ranked, human-order, never auto-approved
python3 tools/verify_core.py                  # the truth check (expect the 3 D1 signals)
python3 tools/serve_audit.py | head -1        # served KPI
```
