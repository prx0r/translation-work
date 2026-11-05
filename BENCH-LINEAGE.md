# OpenPāṭala → translations → SanskritBench → essays: first auditable path

2026-11-05. This is an **advisory, read-only prototype**, not a new publication gate.
It implements the first part of the svread `endgame/` implementation note: pin a
source candidate, record the precise translation layers and run the real pinned
SanskritBench checks, then inspect whether a published Scholar essay actually cites
the selected passage. Missing links and uncertain claims remain visible.

## Run and replay

Use sibling Git checkouts. `ipvv` must have the source file version used by
`tools/workcfg.py`; `sanskritbench` and `openpatala` must contain the pinned files.
For the first demonstrated passage these are SanskritBench commit
`cb5981b66fb7fc7a3bd8636352588bd8a4c42cad` and OpenPāṭala commit
`4147a198d4d91acca2784cca9865ef02c1d7970f`. An arbitrary later checkout is accepted
only if its actual relevant file bytes match the pins and its own Git commit. No
network access, keys, account data or LLM are needed.

```sh
python3 tools/lineage_audit.py run \
  --work paramarthasara --target param-p01-v01 \
  --bench-root ../sanskritbench --openpatala-root ../openpatala

# Optional: save a NEW receipt inside this repo. The tool refuses to overwrite.
python3 tools/lineage_audit.py run \
  --work paramarthasara --target param-p01-v01 \
  --bench-root ../sanskritbench --openpatala-root ../openpatala \
  --essay paramarthasara/scholar/essays/62e62283ac8d5aa4a927ecbdcc064eeac4a38d8291a5dcd39db976f1b794e51b.json \
  --output logs/lineage/example.json
python3 tools/lineage_audit.py verify logs/lineage/example.json \
  --bench-root ../sanskritbench --openpatala-root ../openpatala
python3 -m unittest discover -s tests -p test_lineage_audit.py -v
```

With no `--output`, JSON goes to stdout and no project file is written. To replay,
check out the source and companion commits recorded in the receipt and restore the
exact translation files and tool code. `verify` checks the receipt digest **and**
re-runs the audit against the current inputs. The receipt is not a signature: its
integrity depends on comparing its digest with an independently trusted copy.
The compact, sorted JSON hash used here matches the encoding used by Scholar's
Scheme A; it is **not** the human-authority Scheme B or a qprivately receipt.

## What is and isn't established

| Step | This prototype does | Still needed |
|---|---|---|
| Source → OpenPāṭala | Checks committed source bytes, a pinned dossier, the exact GRETIL external identifier and a reviewed candidate map. | Link Work → edition → witness; resolve the dossier's `en` language assertion for this Sanskrit source. The map is a candidate, not a witness attestation. |
| Source → passage | Hashes the source file and the output of the actual `workcfg` parser; requires the registered song's source verses. | Pin and independently audit complete byte-exact spans against the named edition. Whitespace-token reconstruction isn't such a span. |
| Layers | Hashes every existing T1/L0/argmap/L2/C1/L3/L4/C2 JSON layer and compares it to the historical proof's stored hashes. Runs the current structural/cross-layer validator and hashes its program and schemas. | The old proof does not pin every Markdown input; matching its recorded layer hashes does not rerun the proof or establish philological correctness. Human review stays separate. |
| SanskritBench | Verifies the committed pinned kernel bytes before executing its actual five checks. Saves their raw booleans/ratios as advisory diagnostics with full source/candidate digests. | Evaluate against an independently annotated, licensed Sanskrit gold set and calibrate per check. A heuristic PASS cannot prove faithful meaning, coverage or absence of fabricated claims. No gold score is claimed here. |
| Essay | Validates the public content-addressed Scholar essay and checks whether it cites the exact work, target and T1-row digest. | Resolve the cited historical projection and Git commit, trace individual essay claims to cited evidence, and separately record human/agent review. A self-attested sign-off is not a cryptographic signature. |

For the included Paramārthasāra example, the available OpenPāṭala dossier is
`PTCND_sa_abhinavagupta-paramArthasAra`. Both it and the source header name
`sa_abhinavagupta-paramArthasAra`; this is useful for a candidate work mapping,
but does not authenticate the edition. The checked-in editorial essay is a valid
published snapshot but does not cite the chosen verse, so its status is `UNLINKED`.

The current benchmark's check names are stronger than their implementation. For
example, a negated English translation can pass all five; its result ID also uses a
function object and only a candidate prefix. This adapter **does not use that ID**
and never treats the kernel's `proof` flag as an approval. It pins the kernel by full
SHA-256 and identifies the complete normalized source and candidate independently.
The receipt's `overall` remains `INCOMPLETE`; no site files, proof records, version
ledgers, publication permissions or translation data are modified.

## Follow-through

1. Build candidate maps and reviewed byte spans for actual works in OpenPāṭala;
   do not equate the similarly named Īśvarapratyabhijñāvimarśinī dossier with IPVV.
   Keep the IPVV R2 import's `BLOCKED/PROOF_NOT_RUN` gates until its own source and
   canonical layers exist.
2. Assemble a consented/licensed, independently annotated Sanskrit benchmark;
   measure false positives and negatives before any promotion or threshold policy.
3. Bind cited essays to resolvable historical source and projection commits and
   give each claim a specific citation. Expose evidence gaps to Scholar review.
4. Only after validating those links, consider a separately versioned, fail-closed
   release gate and reader integration; never make an advisory PASS publish content.
