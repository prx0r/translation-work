# scholar/ — versioned scholar work on this work (the git for the stack)

Three append-only JSONL files. Never edit a line; corrections are new lines (fast-forward only).

## `versions.jsonl` — one line per scholar version

```json
{"version_id": "sv:<16hex>",          // = sha256(canonical{work,layer,target,parent,author,content_sha256,created_at})[:16]
 "work": "paramarthasara",
 "layer": "l3",                        // t1 | l0 | argmap | l2 | c1 | l3 | l4
 "target": "param-p01-v01",            // verse_id (c1: the song id, e.g. param-p01)
 "parent": null,                       // null = fork of the ORIGINAL canonical layer
                                      // "sv:…" = child of that scholar version (fork-of-fork, any depth)
 "base_sha256": "<canonical original content sha256 it was cut from>",
 "author": "owner",                    // free name; identity verification is a review concern
 "created_at": "2026-11-03T00:00:00Z",
 "note": "",
 "content_sha256": "<sha256 of canonical content>",
 "content": {},                        // layer-shaped: the actual edit (e.g. {"lines": ["…"]})
 "status": "MACHINE_DRAFT"             // MACHINE_DRAFT | REVIEWED | REJECTED
}
```

- **Original** = the canonical file in `../data/` (not stored here; `base_sha256` pins it).
- **Fork** = any version whose `parent` points at another scholar's version.
- `version_id` is content-derived: same inputs ⇒ same id, duplicates impossible.

## `reviews.jsonl` — ReviewEvents (vendored `tools/human_authority/contracts_human_authority.py`)

Scholar judgment about an **exact** `(target, hash)`. Evidence, never a mutation:
`review_id · review_target{object_ref, version, hash, layer} · reviewer{…} · decision
(ACCEPT|ACCEPT_WITH_QUALIFICATION|DISPUTE|PROPOSE_ALTERNATIVE|ABSTAIN|OUT_OF_SCOPE) ·
review_scope · evidence_refs · reasoning · created_at · event_hash`.
Optional `signer` (Ed25519 pubkey hex) + `signature` over `review_id` — the schol-off,
same semantics as `qp_acom` receipts (signature rides outside the hashed body).

## `promotions.jsonl` — PromotionEvents (the only path to "reviewed")

`promotion_id · object_ref · object_version · from_status · to_status · basis[review_ids] ·
reason · promotion_hash`. `NOT_REVIEWED → INDEPENDENT_REVIEWED` requires `basis` to name
live reviews. A signoff run (`tools/scholar.py signoff`) writes: ReviewEvent → PromotionEvent
→ `../data/<song>.signoff.json` (the existing per-song signoff schema).

## Rules

1. Append, never rewrite. `python3 tools/scholar.py verify --work paramarthasara` re-derives
   every id, hash and fork link — any mismatch fails `check.py` (`scholar-valid`).
2. A signoff is bound to the stack hash of the song at sign time; any layer edit afterwards
   changes the hash ⇒ review re-opens (machinery: `schemas/signoff.py` date rule + this hash).
3. Browser drafts (svread localStorage) are unpublished until saved through
   `tools/scholar.py save` into these files, then re-emitted to `svread/data/scholar/`.
