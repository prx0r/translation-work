# CHAT — retrieval contract for the eventual chat (and style worker)

*The site reader shows translations. Chat ANSWERS questions. Different job, stricter
contract: every claim in an answer must resolve to a gated record. This file is the
retrieval spec any chat implementation must satisfy. Worker contract in
`DATATYPES.json` (chat-answer, style-render) is normative; this file explains it.*

## What chat may retrieve (closed world)

1. **Translations**: `site/data/translations/*.json` chunks with `gate == "PASS"` ONLY.
   BLOCKED chunks are invisible to retrieval (their English does not exist for chat).
2. **Corpus**: `dist/data/corpus.jsonl` records with `en_gate in {PASS, PUBLISHED, OWNER}`.
   BLOCKED/MACHINE_DRAFT English is quarantined: retrievable for audit, never quotable
   as established. Any answer quoting quarantined English is a gate violation.
3. **Variants**: `site/data/variants/<work>.json` — for "what else could X mean?" questions.
   Answers MUST present fork status (live = undecided, resolved = adjudicated with reason).
   Never present one option as the answer when fork is live.
4. **Proofs + signoffs**: `proof/proof-sXX.json` (gate, needs, lineage), `data/*.signoff.json`
   (human acceptance). Answers about trust ("is this reviewed?") resolve here, not in prose.

## Citation format (mandatory in every answer with a claim)

`work · chunk · source file lines` — e.g. *sivastotravali s01-v21 · sivastotravali-u.txt:88*.
Line numbers come from `links.source_lines` (two-pass loader, wrap-aware). Never cite a
pada index alone (renumbers on retokenization); cite verse + file + lines, and token
surface for word questions.

## Answer rules

- Every factual claim ends in a citation a reader can verify in the reader.
- Uncertainty is stated, not smoothed: "the fork X/Y is live" beats picking one silently.
- Human-proposed-but-unreviewed content is labeled machine-proposed, always.
- User-pasted versions (localStorage) are user data: usable in-session, never bundled,
  never embedded, never presented as ours.
- Style renders (C2, stylelab): entertainment/exploration only until essence is human-reviewed (T4).

## What chat needs that does not exist yet

- [ ] Machine-readable work ledgers (term → approved gloss) for term-consistency at answer time.
      Today: T1 headers (parseable) + qa_vs_witness tables (generated). Canonical ledger file: queued.
- [ ] Per-clause L2→L0 derivation (T2) for sub-verse citations. Today: verse-level traces only.
- [ ] Enforced worker contract (retrieval filter + quote rules live in worker code, currently
      specified but not wired — owner-side TODO).
- [ ] Signoffs: no song signed yet. Unsigned = machine-proposed, everywhere, no exceptions.

## Embeddings note

`corpus.jsonl` is the embeddings input (one record per line, stable `{work}:{chunk}` ids,
gate labels for filtering). Re-embed on: new chunks, changed English, changed gates.
Embeddings never override gates — similarity is retrieval, verdicts are validators.
