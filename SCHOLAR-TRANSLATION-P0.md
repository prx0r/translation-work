# Scholar Translation P0 — translate once, publish everywhere, own your words

Status: **specified + built + tested** (tool: `tools/scholar_apply.py`).
No existing system was modified: every primitive below already lived in the
worker, the UI, or the bridge. P0 wires them into one loop.

## The loop

```
take a site translation
  → edit freely (workspace autosaves; history keeps every revision)
  → justify each choice (decision: subject + before + after + reason)
  → name terms once (decision subject "term: X" = glossary entry, global)
  → agent replays your choices onto any text (scholar_apply: deterministic,
    no model, no training — every substitution cites the decision that drove it)
  → review the diff in revision history (restore anyone, teach style pairs)
  → sign off with YOUR rights (incl. all-rights-reserved = © you)
  → submit → bridge → author-attributed version in git → release → reader
```

## Why this commoditises translation (without training anything)

The expensive part of translation was never typing — it is the thousand
micro-decisions (this term renders *this* way, because…). P0 records those
decisions as data (decisions table + l0 token grounds + style pairs) and
replays them deterministically. Translate once with full justification;
every later text starts from your choices, with each applied rendering
carrying its why. The scholar's judgment compounds; the typing does not.
No model is trained, no weights change, nothing leaves the scholar's
account without their explicit per-request consent.

## Primitives (all pre-existing; P0 adds no schema)

| Need | Primitive | Where |
|---|---|---|
| Edit + keep everything | translation drafts, revision history, restore | workspace UI + `PUT /api/scholar/documents/:id` |
| Justify a choice | decision: subject/before/after/**reason**, bound to exact revision hash | `POST /api/scholar/decisions` |
| Name a term once | **convention**: decision subject `term: <X>` = global glossary entry | this file + `scholar_apply.py` |
| Learn my hand | style examples (edit pairs, opted-in), `lexicalChoices()` (l0 grounds) | worker + assist prompt |
| Draft in my voice | agent draft with style/decision/lexical context, consent + quotas | assist (model path, gated) |
| Replay my choices | `scholar_apply.py` (deterministic, no model) | this file |
| Publish as mine | sign-off with rights (`all-rights-reserved` = ©), bridge translation submit, author-attributed version, submission branch | bridge + `scholar.py import/approve-version` |
| Own git | versions carry author+rights; `scholar/submission-<hash>` branches; JSON export | translation-work `scholar/` |

## Glossary convention

A decision whose subject matches `^term:\s*(.+?)\s*$` is a glossary entry:
`after` is the scholar's rendering, `reason` is the grounds. Latest entry
per term wins. Recorded against the passage where it was decided; applies
to every text. The apply tool never invents a term — unknown words pass
through untouched and are reported.

## scholar_apply (deterministic replay)

```
scholar_apply.py glossary --api URL --cookie C [--work W]
scholar_apply.py apply --api URL --cookie C --base WORK:TARGET:LAYER [--title T]
```

- `glossary`: reads the scholar's `term:` decisions (latest per term).
- `apply`: loads the canonical base bytes (same projection bytes the worker
  loads), replays glossary (l0: token `chosen_index` replay with grounds;
  l2/l3/l4 prose: longest-first whole-word substitution), PUTs the canonical
  document id with CAS revision, then writes one decision row per applied
  term (`term: X`, before→after, reason = grounds + source decision id).
- Marks the draft `agent_source: scholar-apply/1`, `assisted: false`
  (mechanical replay, not model prose). Scholar reviews, edits, publishes.
- Refuses on: unknown terms (reported, untouched), revision conflict (409),
  missing base bytes, unresolvable layer JSON.

## Copyright

Rights are chosen at sign-off per version: `all-rights-reserved`,
`cc-by-4.0`, `cc0`. Published versions record author + rights + sign-off id
in git; the reader lists author versions. © is therefore `author +
all-rights-reserved + git-attributed version` — no extra field, no extra
table. Scholars wanting Creative Commons pick it per version, per text.

## Their own git

Every published translation version is content-addressed (`sv:` hash chain
with `parent`), attributed (`author`, `author_kind: human`), rights-tagged,
and merged through reviewable submission branches. A scholar's whole oeuvre
is queryable by author today (`versions.jsonl` + projections) and exportable
as JSON; a per-author fork remote is a future convenience, not a P0 need.

## Test plan

- `tests/test_scholar_apply.py`: glossary parsing (latest-wins, bad rows
  ignored), l2 substitution (longest-first, whole-word, unknown untouched),
  l0 token replay (grounds carried, missing option reported), draft payload
  shape, decision-row shape. All mocked API.
- Existing suites stay green: worker `node --test tests/*.test.mjs`,
  `tw/tests` pytest, svread node tests. No worker/UI/bridge file touched.
- Live proof (private, labeled): one `term:` decision + one applied draft
  under the editorial account; offline bridge publish of a translation
  version to a temp remote (pattern already covered by
  `test_scholar_account_submission.py`).
