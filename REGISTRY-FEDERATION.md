# REGISTRY FEDERATION — one work ID across translation, books, video, socials

*2026-11-06. Status: SPEC (proposal for lane owners; translation-work implements only its own side). Nothing here writes other repos. Nothing here auto-publishes — influence's consequence-control law stands (drafts queue, humans confirm sends).*

## 0. The key

`openpatala_work_id` (box DB `works.id`, e.g. `tantrasara`, `tantraloka-a15`,
`ipvv`). Every factory record that touches a work carries it. Resolution:
`tools/dbread.py ids <tw-work>` (translation-work side, read-only).

Current state: svread `source-map.json` (87 works) still shows
`openpatala_work_id: "UNRESOLVED"`. Filling that in is a svread-lane edit
with owner nod — this spec assumes it done and defines what consumes it.

## 1. Asset fields (additive, fail-closed)

Per work, in the work's own registry (bookfactory `projects/<book>/thesis.json`,
videofactory `REGISTRY.json` series entries, influence job packs):

```json
"assets": {
  "books": [{"kind": "print|epub", "isbn": "978-…|TBD",
             "pack_rev": "<git sha>", "ledger_sha256": "<sha>",
             "kdp_status": "draft|preflight-pass|OWNER-SHIP"}],
  "videos": [{"series": "tantrasara", "unit": "tsa-a01",
              "sealed_mp4_sha256": "<sha>", "receipt": "<path>",
              "pack_rev": "<git sha>"}],
  "social": [{"channel": "x|ig|yt", "post_id": "…|DRAFT",
              "quote_handoff_sha": "<sha>", "status": "draft|queued-human-confirm|sold"}]
}
```

Rules (all lanes):
- Missing/UNRESOLVED/TBD = draft-only. Nothing ships, sells, or posts without resolved IDs + green gates. This is the same fail-closed shape as bookfactory's `check.py` (queued projects return nonzero) — extended to identity.
- ISBN lives ONLY on print assets, assigned at OWNER-SHIP, never invented by a worker. A beam drafter that emits an ISBN is a defect; reject the draft.
- Social `post_id` is written ONLY by the influence runtime after human confirm. Beam drafts copy + asset pointers; the post ID comes back from the runtime receipt.
- Shop/customer socials (Etsy triage, review replies, drop alerts): jobs in influence's queue, drafts from translation-work quotables (L2/C1-essence via bookfactory quote-handoff, which already exists), human confirms every send. Bodacious drafting, lawful publishing.

## 2. The loop, ported (for factory owners)

Each factory already has the hard half (gates: videofactory `check.py` + contract suite; bookfactory `check.py` stage-aware; influence `pipeline/runtime.py` + receipts). The portable half is the largetext skill §5:

```
queue (ranked: untranslated/unrendered/unposted first, shortest-first)
  -> workers draft (beam-free, $0, prose/assets only, never canonical)
  -> pydantic self-check (shape) -> assessor review batch
  -> deterministic assemble/convert -> lane gate (check.py etc.)
  -> commit+push on green, park with reasons on red
```

Adoption per lane (owner acts; this spec proposes, never imposes):
1. **videofactory**: queue = unrendered series units (tantrasara 22, shiva 78); beam drafts storyboard-adjacent prose (glossary entries, apparatus notes — never timing/cues); converter = existing builders; gate stays `check.py` + parity mode until owner cutover.
2. **bookfactory**: queue = unbuilt book entries (36+36 prayer books, ipvv lane); beam drafts entry-adjacent prose (headnotes, not verses); `factory.py inspect/quote/verify` remain the assemblers; KDP ship stays owner-only (existing fail-closed gate — the loop must never learn a ship command).
3. **influence**: queue = draft posts/replies from quotables (C1-essence/L2 via quote-handoff SHAs); beam drafts copy variants; runtime + human confirm stay the ONLY path to publish/spend/send. The loop ends at `queued-human-confirm`. Full stop.

## 3. What translation-work provides (our lane, wired)

- `tools/dbread.py` — works/passages/editions/coverage/ids (read-only).
- `tools/registry_sync.py` — DB universe × local STATUS → tiered PLAN (already drives translation).
- Quote-handoff inputs (L2/C1-essence, sha-pinned) for bookfactory/influence drafts.
- This spec + the largetext skill as the portable pattern.

## 4. Explicit non-goals

- No auto-publish, auto-spend, auto-send anywhere (influence law).
- No ISBN invention, no rights inference (bookfactory law: rights missing = draft-only).
- No video cutover (videofactory parity mode stands until owner acts).
- No writes to other repos' registries from translation-work tooling.
- No AMBIGUOUS→PARSED promotion by vote-count (mistakes.md #20 restated for assets: an unresolved ID is not a resolved one).
