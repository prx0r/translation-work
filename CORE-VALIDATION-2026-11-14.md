# CORE VALIDATION — 2026-11-14 (corrected)

*Owner priority: volume is not the goal; **proving the Trika core is actually
correct and the pipeline works** is. This re-derives every core proof from
current bytes instead of trusting stored `proof-*.json`. Tool:
`tools/verify_core.py` (`shastra.verify_core`).
Reproduce: `python3 tools/verify_core.py`.*

## Result

- **95 REGISTRY works / 322 songs**
- **318 GATE-OK** — stored PASS reproduces exactly from current bytes.
- **4 NO-PROOF** — `sivasutra/span-p09`, `spanda/span-p04b/05/06` (loop
  in-flight; `tw-assemble` owns them; not defects).
- **0 REGRESSIONS** — no song claims PASS that doesn't recompute.
- Align: p10 = 0.912, p50 = 1.000, p90 = 1.000. **43 verses** rely on a
  recorded, grounded disposition. 63 songs dip below 0.95 somewhere (normal
  sandhi territory) but still pass.

**Bottom line: the core is genuinely proved under its canonical mode.** The
REGISTRY's "95/95 gold" is structurally true for these songs.

## Correction to the first pass (important, and honest)

The first run of this verifier reported **11 regressions / 8 C1 defects / 3
T1 defects**. That was **my tool's bug, not the corpus's**: `verify_core`
forced `--shastra` on *every* work, but **266 of the 818 core proofs are
"classic" mode** (they read `T1-*.md` / `L2-*.md` / `c1/C1-*.md`, not
`data/*.json`). Recomputing a classic proof through the shastra path is
meaningless and produced phantom ALIGN/C1 blocks. Fixed: the verifier now
picks each proof's mode from its own `lineage` (data-path ⇒ shastra, MD ⇒
classic). After the fix: **0 regressions.**

The 3 "T1 defects" (par-p06, s10, s12) were classic-mode works — they PASS in
their real mode and were never broken. Retracted.

## What is actually true (and matters)

**The corpus has two parallel representations per work, and two proof modes.**

| mode | count | reads | canonical for |
|---|---|---|---|
| shastra | 552 songs | `data/<song>.{t1,l0,argmap,l2,c1}.json` | Tantraloka/Tantrasara/IPVV/minimal |
| classic | 266 songs | `T1-*.md`, `L2-*.md`, `c1/C1-*.md` | stotras & pre-conversion works |

Proof correctness is fine — each song is proved in one consistent mode. The
**risk is drift between the two representations**, because *serving* reads the
`data/*.json` side (`emit_scholar`), while *proof* for classic works reads the
MD side.

Concrete instance found: for 5 Tantraloka works (**a07, a21, a26, a32, a37**)
the `data/*.json` C1 `essence` is the **L2 line copied verbatim** (e.g. tal-a21:
61 essence entries, each = the L2 sentence; the proof recorded
`c1_l2_shared: []` on 2026-11-01 and was never re-run). The **classic MD C1
(`c1/C1-tal-a21.md`) is a proper authored essay** — so the *proof* is legit,
but the *served essence* for these 5 is degenerate (it just repeats L2).

**Resolved (2026-11-14).** All five were authored per-verse: the L2-copy
essence (61/71/76/69/85 lines) was replaced with condensed telegraphic claims
grounded in the verses, essence counts kept identical so L4 `essence_maps`
still resolve. Result: each of a07/a21/a26/a32/a37 now **shastra proof PASS,
validate_song 0 errors, C1_L2_SHARED gone**. (These works are not *served* —
they have no source projection — so this repaired the data/proof layer, not
the reading layer.)

## Durable fixes landed (proof layer)

- `proof_record.py --no-write`: recompute a verdict without touching committed
  state (what makes an honest verification pass possible).
- **Full-strength source identity** (audit F3): `source_sha256_raw` (+ file)
  and `source_digest_normalized_sha256` alongside the legacy 64-bit
  `source_sha`.
- **L2 cite check is now letter-level**, not space-exact: a cite that
  re-segments a source compound used to false-fail (3 songs). Occurrence over
  the source's letters is the correct test; wrong words still fail.
- `tools/verify_core.py` + `shastra.verify_core`: the honesty check, now
  mode-aware.

Minor C1 improvements kept (data essence reworded away from L2 copy, proofs
re-verified PASS): anuttarastika `anu-p04`, `anu-p08`, tantraloka-a27. (These
were safe: their essence count is unchanged, so L4 traces still resolve.)

## Backlog (ordered, honest)

1. ~~Per-verse C1 essence for a07/a21/a26/a32/a37~~ — **DONE 2026-11-14** (authored, PASS).
2. **Representation unification**: choose ONE canonical representation per work
   (MD or data-JSON), re-prove, and serve from the proved side — so proof and
   serving can never diverge. (Design decision; owner + aware of L4 coupling.)
3. 4 in-flight songs — let `tw-assemble` finish; verify after.
4. Republish traces after any data change so the served claim layer is current.

## Reproduce / trust

```
python3 tools/verify_core.py            # full core
python3 tools/verify_core.py --work W   # one work
shastra.verify_core                     # same, via MCP (ChatGPT)
```
It writes nothing; it recomputes in each proof's own mode and compares. If it
ever reports a REGRESSION, the "gold" claim is false for that song — that is
the signal this whole exercise exists to catch.
