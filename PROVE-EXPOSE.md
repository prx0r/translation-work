# PROVE-EXPOSE — making translations readable & provable to ChatGPT

*2026-11-14. The process note for the "prove + expose" lane: how a finished
translation in `translation-work/` becomes something ChatGPT can actually read
and verify through the MCP estate. Machine-proposed throughout; nothing here is
human-signed. Law: `skills/crystal-ipvv/SKILL.md` + `skills/largetext/SKILL.md`
still govern the translation layers; this lane only *publishes* them.*

---

## 1. The goal (owner 2026-11-14)

> Get the whole thing onto ChatGPT as MCP connectors/plugins.

Translation quality is the product. The **distribution** target is the MCP
estate. A translation is "done" for this lane only when a ChatGPT connector
can (a) **read** it (`scholar__passage_evidence`: hash-checked Sanskrit +
English) and (b) **trace** it (`claim` page → trace → verify pack →
openpatala id).

## 2. What "readable" actually means (the one condition)

The ChatGPT reading path is:

```
ChatGPT → mcp.svatantrya.net/mcp (federation)
        → scholar__passage_evidence(work, target)
        → svread/data/scholar/<work>.json  (the "Scholar projection")
        → source_verses[target] + originals{t1,l0,argmap,l2,c1,...}
```

**A work is served iff its projection has a non-empty `source_verses` for the
target.** If `source_verses` is empty → `"Passage unavailable or withheld"`,
regardless of how good the translation is. That is the single bottleneck, and
it is what `serve_status` measures.

Note `target` is **verse-level** (`tsa-a08-v01`), not the passage locator
(`tsa08-p01`). Passage locators drive claim pages; verse targets drive reading.

## 3. The pipeline (deterministic — NO beam)

```
canonical layers (data/<song>.<layer>.json)  +  proof PASS
   │  (produced by the beam swarm / assessor — see §6)
   ▼
source audit ── _source_audited(work): source/manifest.json (source-intake/1)
   │            OR source/record.json (svatantrya-source-record/1) whose
   │            every volume sha256 re-hashes to the on-disk bytes. Never
   │            serve bytes we did not re-hash; stale record = BLOCKED.
   ▼
tools/emit_scholar.py --work W   →  svread/data/scholar/W.json (source_verses)
   │
   ├─ trace layer (only works with a trika-x bundle):
   │    trika-x trace_bundle.py --work W --target T  → data/traces/W-T.json
   │    svread emit_traces.py   (copy + index, fail-closed verify)
   │    svread emit_verify.py   (per-file hashed packs)
   │    svread emit_claim_pages.py (claim/ + work/ + chain/ + md)
   ▼
svread emit_discovery.py          (llms/sitemap/ai-catalog/pushing)
svread scripts/release_manifest.py --write   (LAST)
```

Each step is idempotent and `--check`-able (deterministic). The publish chain
is **fail-closed**: one stale trace aborts `emit_traces` (fix the trace, don't
force it).

## 4. The MCP surface (added 2026-11-14)

Two tools on the `shastra` server (`mcp_server.py`, 34 tools total):

- **`shastra.serve_status(work="")`** — read-only scorecard. Per work: `audited`,
  `source`, `proj_src` (source_verses count = the readability condition),
  `traces`, `verify`, `claims`, `served`. `work=""` = every work with layer
  data. Backed by `tools/serve_audit.py`.
- **`shastra.make_readable(work="", all=false, publish=false)`** — the button.
  Audits source, runs `emit_scholar` for the work(s), reports served/blocked.
  `publish=true` then runs the svread publish chain. Backed by
  `tools/make_readable.py`. Unaudited works are reported **BLOCKED**, never
  served.

CLI equivalents:

```bash
python3 tools/serve_audit.py                 # full scorecard
python3 tools/serve_audit.py --work kularnavatantra --json
python3 tools/make_readable.py --work tantrasara-a13
python3 tools/make_readable.py --all --publish     # audit+project+publish
```

## 5. What this session fixed / found (2026-11-14)

1. **Trace layer was 222/951 stale** (failed `trace_bundle --verify`) because
   works were re-keyed/re-chunked after traces were made. Fail-closed
   `emit_traces` blocked all publication. Fixed: recompiled 158, re-keyed 61
   (`chunkA→chunk-a`, `sivs→span`, `para→ptv`), archived 2 removed spanda
   passages → **0 stale / 948**.
2. **8 gold works had no traces** (dehastha, gitarthasangraha,
   mahopadeshavimshatika, paramarthadvadasika, rahasyapanchadashika,
   sivasutravimarsini, malinivijayavarttika, tattvasandoha). Built + verified
   41 bundles.
3. **`emit_scholar` only accepted `source/manifest.json`**, so 20 Tantrasara
   ahnikas (which carry a valid `source/record.json` whose volume sha256
   matches the source bytes) served **zero** verses. Fixed: `_source_audited()`
   now accepts a hash-verified `record.json` too (both path conventions),
   while `SOURCE_COVERAGE_HOLDS` (ghatakarpara) stays withheld. Result:
   **Tantrasara is now readable** (739 verses).
4. **Scale run:** emitted projections for every audited work that lacked one →
   served works went **56 → 91 of 144** (vs. the ~58 that were projected
   before). `mukta-m00027` (605v), `kularnavatantra`, etc. now served.

Pre-existing, honest gaps: `ipvv` projection has empty `source_verses`
(alias/legacy layout — separate fix); 14 works emitted empty projections
because no *proof-complete* song was eligible yet (correct conservative
behaviour); 78 works remain `UNMAPPED` to canonical openpatala IDs
(dossier-acquisition frontier — ID match only, never invented).

## 6. How to do this at scale — and where beams fit

**Beams do NOT help this lane.** Beams draft *layers* (T1→L0→argmap→L2→C1).
The expose lane is a **deterministic join + emit**, so it needs no model and
should never call one. The correct split:

```
BEAM / assessor  →  produce layers + proof PASS      (the long pole, per work)
EXPOSE (this)    →  audit → project → trace → verify → claim → manifest
                    (a fan-out of cheap deterministic jobs)
```

At scale, the expose step is a post-promotion hook:

1. **Trigger:** when a song/ahnika passes `proof_record` (or `promote`), enqueue
   an **expose job** for the work. `make_readable --work W` is that job.
2. **Fan-out:** run expose jobs in parallel, bounded (CPU/IO), no model calls.
   `make_readable --all` is the batch form; it is safe to re-run (idempotent).
3. **Trace step:** only for works with a trika-x bundle. New gold works need a
   bundle first: `trace_bundle.py --work W --target T` per passage (41 built
   this session). A `make_traces` driver (todo) would batch this exactly like
   `make_readable`.
4. **Publish once:** after the batch, run the svread chain once
   (`emit_traces → verify → claim → discovery → release_manifest`), not per
   work — the emitters are global and fail-closed.
5. **Gate:** `serve_status` is the dashboard. "Served / total" is the KPI;
   `blocked-unaudited` and `empty(no eligible songs)` are the two backlogs.

**The scaling bottleneck is NOT compute.** It is (a) source audits
(`record.json`/manifest per work) and (b) trace locator hygiene. Both are
deterministic; neither is beam work. Beams should keep drafting the corpus;
the expose lane keeps it read.

### Recommended cadence

```
loop:  beam drafts → proof PASS → (hook) make_readable --work W
batch: weekly  make_readable --all --publish
daily: serve_status | head -1   (served / total KPI)
```

## 7. Hard rules (inherited)
Hard rules (inherited)

- **BLOCKED ≠ PASS.** A work with an unverified source or an ineligible song
  is BLOCKED, reported as such, never force-emitted.
- **Three stamps stay separate:** bytes (sha256, re-hashed on every emit),
  mechanics (`proof_record` PASS + trace verify), meaning (human sign-off —
  pending everywhere). `served` is a *bytes+links* fact, not a truth claim.
- **Never invent a mapping.** UNMAPPED works stay UNMAPPED until a shared
  external ID justifies CANDIDATE.
- **No auto-publish of meaning.** `make_readable` publishes machine-proposed
  projections; it never signs off or marks reviewed.
## 8. Session log — 2026-11-14, second pass (trace fan-out + ipvv)
Session log — 2026-11-14, second pass (trace fan-out + ipvv)

- **`tools/make_traces.py` + `shastra.make_traces`** (34 tools total): batch
  `trace_bundle` per passage — one work, `--served-untraced`, or `--all`.
  Idempotent, fail-closed per bundle; verified bundles feed `make_readable
  --publish` into the claim layer.
- **Scale result:** 1672 bundles built for 35 served-but-traceless works
  (kularnavatantra, 34 mukta burn works), 0 failures. Published through the
  svread chain (2640+ traces → verify packs → claim pages); `scholar__passage_evidence`
  confirmed serving the new works.
- **ipvv readable (5/49 chunks).** Root causes, verified: (a) projection was
  stale (old `chunkA-*` scheme; current data is hyphenated `chunk-a-*` with
  symlinked layers); (b) 44 chunks have only t1/l0 (+ orphan old-scheme L2s) —
  argmap/C1 await authorship, correctly withheld; (c) workcfg spans carry print
  apparatus, so reconstruction now drops `is_paratext` tokens (estate doctrine,
  same as proof alignment). Served text verified clean (0 pipes/page-marks).
- **Coordination rule (binding):** stay out of `formal-trika/data/traces`
  while another agent works there. Trace verify drifts when the translation
  loop adds layers mid-publish (observed twice on mukta-m00125); the fail-closed
  publish is the detector, not the problem. Coordination issue: trika-x#20.
  Publish only from a refresh-then-publish pass, or during a loop pause.

