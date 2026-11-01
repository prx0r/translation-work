# AGENTS.md — Translation-Work Control Plane (IPVV)

*Working Sanskrit translations in `/root/translation-work`. When in doubt, check here first. Independent of `/root/AGENTS.md` (Drop project) — do not mix the two tracks.*

---

## Identity

I am a Sanskrit translation agent working one text at a time toward crystal quality. I do not batch. I do not mark work complete — the human reviews; I only propose. My job: take the next target from the queue and return it stunning, or return it honestly incomplete.

---

## The Skill (the law)

Next-agent focus, no exceptions:
`/root/translation-work/skills/crystal-ipvv/SKILL.md`

One work at a time: source → lore (one focused search) → T1 (full-verse) → L0 (100% parsed, coverage verified vs source) → per-passage argmaps (real reconstruction, distinct lore) → L2 read prose → C1 argument condensation → mechanical gates → registry as machine-proposed, never final.

## Absolute Bars (from `mistakes.md`, learned the hard way)

- No quoted English gloss-words in C1 ever.
- No metacommentary *about the text* in C1 ever.
- C1 shares zero sentences with L2; argmaps share zero sentences with each other.
- Uncertainties marked, never smoothed. Nothing invented.
- Parse rate never certifies coverage: verify T1 against the source edition, verse by verse.

## File Reference

| File | Purpose |
|------|---------|
| `skills/crystal-ipvv/SKILL.md` | The mandatory process skill |
| `crystal.md` | The standard, with exhibits of crystal vs non-crystal |
| `mistakes.md` | Failure log — binding rules learned the hard way |
| `targets.md` | The work queue — one at a time, in order |
| `REGISTRY.json` | Completion registry (machine-proposed only, never final) |
| `INDEX.json` | Work index |
| `THEMES.md` | Cross-work themes |

## Reference Works (built this session — the templates to copy)

| Work | Why it is the template |
|------|------------------------|
| `pancashloki/` | Built fresh end-to-end: full-verse T1, 137/137 L0, distinct argmaps, separated C1 |
| `bhairavastava/` | Repaired end-to-end (was half-verse T1, duplicate C1): T1 114/114, rewritten C1 pair |
| `anuttarastika/` | Sharpened end-to-end: real per-verse argmaps, distinct C1 pair |

## Per-Work Shape (`<work>/`)

`T1.md` (frozen hyperliteral gloss) → `T1.l0.jsonl` + `T1.l0.report.txt` (via `/root/ipvv/tools/t1_extract.py`) → `passages.jsonl` → `argmaps/*.md` + `argmaps/argmap.json` → `L1.md` → `L2.md` → `L2.v2.md` (+ Sanskrit) → `c1/C1.md` → `c1/C1.v2.md` → `L200.md` → `STATUS.json`.

No batch artifacts required for manual single-work builds (no `batch.jsonl`, no GATE r2 keys). Note their absence honestly in STATUS.

## The One Rule

> **Small, sharp, finished beats big, batchy, and approximate. If in doubt, shrink the scope, never the standard.**

## User Directive 2026-11-01 — Layer Redefinition (verbatim, binding)

*The following is the user's message saved verbatim. It redefines the stack. Where it conflicts
with older sections above (e.g. "Per-Work Shape"), this directive plus `LAYERS.md` win.*

i think we need like really rigid schemas for l0 and l2 and c1 honestly it should work like this.. t1 is the standard quick translation the ai does over the whole text. l0 is the literal gloss it basically is the options the word could mean like exact precise sanskrit. argmap then looks at sanskrit, t1 and l0 and whole verses in order to translate the verse as sharply as possibly (now understanding the philosophical argument information gained from these 3) from this we can now collapse into our l2 which is plain english translation of the line. then C1 is basically the best rendering capturing the essense of the verse. c1 can also be a gen z reading for example or a poetic reading these can just be different ai skill renders over the top and you can perhaps even prompt the ai to be like give me a suuper basic eli5 or even mathematical or other ones.. i think its worth right now defining / redifiniing these files, their relationship and then formalising teh schmeas again as data objects not md files
