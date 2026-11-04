# Essay Starters P0 — organize the estate, mine the glossary, anchor to chunks

Status: **built + tested** (`tools/essay_starters.py`). Read-only over every
archive; writes only to `--out`. No existing file touched.

## What it does

```
index     walk tantraessays / research-library (both mirrors, deduped) /
          expansion-packs / workshop JSONs / basecamp objects+contentions+seeds
          → INDEX.json + INDEX.md (starter = thesis + crux + terms + chunks +
          source + grade)
glossary  mine `term (gloss)` candidates, ranked by file spread, proposed-only,
          every candidate with file:line refs
anchor    resolve locator mentions against translation-work chunk ledgers,
          anchor glossary terms to T1 chunks, coverage per starter
```

## Pristine rules (enforced, not wished)

- Miner proposes, owner disposes: every glossary candidate is `proposed`
  until recorded as a `term:` decision (the scholar glossary remains the
  only accepted source — see SCHOLAR-TRANSLATION-P0.md).
- Terms need a diacritic or a capitalized head; banned gloss leads
  (`see/cf/e.g./etc`) are dropped; alternates are kept, top rendering wins.
- Chunks are never invented: locators resolve against `passages.jsonl` or
  the mention stays external (clip IDs live in their own system).
- Duplicates collapse by content hash, first path kept, count reported —
  the damn/projects mirrors stop double-counting.
- Basecamp structured objects (essay-objects, contentions, seeds) enter
  with their cruxes intact: question, tension_point, central_reading.

## Feeds

- Starters with cruxes → memo compiler essay ideas + pushing catalog.
- Glossary proposals → owner approval → `term:` decisions → `scholar_apply`.
- Anchor coverage → which essays are canon-solid, which float; unanchored
  starters are reframe-or-research candidates, never published as grounded.
- Shared starters are the commons (fork with attribution); drafts stay
  private; published work is signed with its reasoning chain.
