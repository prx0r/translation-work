# Stall QA (ported from patalacheckpoints IPVV stall log)

*Every point where the L2 READ stops you becomes a fixture; fixtures
feed a scaler that searches the corpus for the same failure mode.*

## Stall entry template

| # | location (chunk + ¶ + line, anchors when available) | what confused / bothered me | type | severity |
|---|---|---|---|---|

## Type tags

- **prose** — English clunky / broken / machine-translational
- **argument** — logic doesn't follow
  - `MISSING_PREMISE` — conclusion needs an unstated premise
  - `HIDDEN_REDUCTIO` — reductio with invisible absurd-branch
  - `UNSTATED_PARTITION` — exhaustive division assumed, not argued
  - `LOGIC_INVERSION` — direction/polarity flipped or swapped
  - `REFERENT_DEPENDENCY` — step needs unstated doctrine/context
- **coverage** — source span untranslated or silently dropped
- **numbering** — verse/passage labels don't match source order
- **recension** — reading follows the wrong edition without note

## The scaler loop

1. Record stalls with type tags during any read.
2. Quarterly (or per 10 stalls): grep the corpus for the same pattern
   (e.g. every `UNSTATED_PARTITION` → audit all argmaps for partitions).
3. Fixes land as prompt rules (`tools/T1-PROMPT-RULES.md`) or reviewer
   checks, never as one-off patches.
