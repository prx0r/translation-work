# Scholar Copilot P0 — proactive, internal, deterministic

Status: **specified + built + tested** (`tools/scholar_memo.py`).
No model, no training, no new schema, no existing file touched. The copilot
reads; the scholar decides. Everything it says is a pointer to something
already on disk, labeled by tier.

## The loop

```
scholar saves a version (translation or essay draft)
  → memo compiler notices the new revision (state file, per account)
  → compiles: objections · related passages · crossover leads ·
              variant briefs (essays) · suggested works
  → prints + files locally; --post saves ONE private labelled note
  → scholar reads next session, follows or ignores
```

Default run changes nothing server-side. `--post` writes exactly one
private `note` per new revision, `agent_source: scholar-memo/1`,
`assisted: false`. State advances on generation, so a memo is delivered
once.

## What a memo contains (and where each line comes from)

| Section | Source | Honest label |
|---|---|---|
| Objections | `ARGMAP.md` unresolved lines, `GATE.json` BLOCKED checks, pushing-catalog records for the work, variant mentions | "the canon's own open questions" |
| Related passages | glossary terms (`term:` decisions) grepped across `T1-*.md` files, capped | "your words, elsewhere" |
| Crossover leads | tantraessays lecture topics, research-library filenames, Levin PDF names | "house archive leads, unverified — file refs only" |
| Variant briefs (essays) | top crossover + top objection + citation coverage (n/10 pinned) | skeletons, scholar writes prose |
| Suggested works | tw works with no Scholar projection, ranked by glossary-term hits in their T1 | "what to translate next, in your voice" |

Nothing is generated prose about the doctrine. Templates are filled with
retrieved refs. A lead is a pointer, never a claim.

## The archives, tiered (how the stockpiles plug in)

- **Tier 0 canon**: projections (hash-pinned, quotable). The only tier the
  memo quotes.
- **Tier 1 scholar's own**: decisions, style pairs, lexical choices. Private,
  consent-gated, the memo's personalization source.
- **Tier 2 granted peers**: published essays with AI-use grants. Memex says
  *exists*; content only via the granted paths.
- **Tier 3 house archives**: platinum/expansion essays, tantraessays
  transcripts + grades, research-library, Levin PDFs, basecamp ROs.
  Discovery only — file refs with grades where known. Reveal pipeline:
  private lead → scholar verifies against Tier 0 → cited in draft →
  published under chosen rights. The "waiting to be revealed" essays enter
  through this gate, never around it.
- **Tier 4 external** (science papers, web): URL + retrieval hash + date on
  first touch; never cited as canon. Websearch primitive is future work;
  local PDFs (Levin shelf) are Tier 3 file refs today.

## Private collection vs shared svatantra

Default is private: drafts, notes, memos never leave the account. Sharing
is always an explicit act with a rights choice — publish (sign-off rights:
`all-rights-reserved` = © you, `cc-by-4.0`, `cc0`), grant AI-use per exact
version, or nothing. The memo compiler never shares, never grants, never
publishes. Suggested works land in the private collection as drafts first;
the shared open-source svatantra grows one signed version at a time.

## Test plan

`tests/test_scholar_memo.py`: glossary load, gate/argmap extraction,
T1-hit ranking, crossover manifest matching, memo assembly, state advance,
post payload shape, nothing-new exit, refusal paths. Mocked API + fixture
trees. Live: read-only memo for the editorial account; one labelled posted
note proving the loop.
