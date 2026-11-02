# CANONICAL — what "the stack" is, and how to prove it

*2026-11-01 · schemas v1.0.0. This file is the canonical declaration. If any other doc
describes the stack differently, this file wins (after the verbatim User Directive 2026-11-01
in `AGENTS.md`, which wins over everything).*

## The stack (one line)

`SOURCE → T1 → L0 → ARGMAP → L2 → C1(essence+renders) → L3(final translation)`, defined in `LAYERS.md`,
enforced by `schemas/*.py`, executed by `tools/*.py`, verified by `check.py`. L3 is the
canonical final translation: one polished rendering per verse, faithful to L2's meaning,
voiced by the verse's rasa, tracing to L0. Added 2026-11-02 (user directive: L3 NOW).

## What is canonical

1. **Data, not MD.** `sivastotravali/data/*.json` is the artifact. MD files are rendered
   views (`render_md.py` proves they agree). Frozen legacy T1 MDs are historical — read-only.
2. **Schemas are versioned.** `schemas/__init__.py:SCHEMA_VERSION` (currently `1.0.0`).
   Additive changes bump minor; breaking changes bump major + re-validate every data file +
   note in STATUS. Never silently widen a validator to make failing data pass.
3. **JSON is living, not frozen.** Unlike ipvv T1 chunks (frozen_hash), data JSON is hand-enriched
   (options, grounds, choices, renders). Therefore: no hash gates on data files — **content
   validation is the gate** (`validate_song.py` + `proof_record.py` B8). Provenance for each
   song lives in `proof/proof-sXX.json` (source_sha, tool + schema versions, gate, dispositions).
4. **Decisions live in objects, not prose.** A fork adjudicated anywhere except
   `argmap.option_choices[]` with a reason does not exist. A render that cannot point at
   `essence[]` via `maps_to` is rejected. A term used without an L0 trace is ungrounded.

## Precedence (highest first)

1. `AGENTS.md` / User Directive 2026-11-01 (verbatim user words)
2. This file (`CANONICAL.md`)
3. `LAYERS.md` (layer contracts + invariants)
4. `ALIGNMENT.md` (relation to ipvv specs + sanskritbenchy)
5. `schemas/*.py` (machine-enforced subset of the above)
6. `skills/crystal-ipvv/SKILL.md` (process), `mistakes.md` (failure log), `targets.md` (queue)
7. `DATATYPES.json` (every datatype in the Sanskrit-to-site pipeline + worker contracts + global rules)
8. `TENSIONS.json` (known frictions, with status)

Schemas enforce a *subset*: anything the validator cannot check (taste, sharpness, honesty of a
grounds note) is enforced by human review. `COMPLETE` always means machine-proposed, never final.

## Verify (one command)

```bash
cd /root/translation-work && python3 check.py
```

Exit 0 = canonical: schemas execute, every data song validates, every proof record PASSes,
every MD round-trips, no stale doctrine strings, directive present. Anything else exits 1
with the failing step named. Run before any commit, after any schema/tool/data change.

## Change protocol

1. Small, additive first (optional fields, new OPTION_SOURCES, new render styles).
2. Bump `SCHEMA_VERSION`, update this file + `LAYERS.md` if contracts changed.
3. `python3 check.py` must pass on all songs before the change lands.
4. Log the change in `sivastotravali/STATUS.json` under `data_objects_*`.
