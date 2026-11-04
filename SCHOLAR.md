# SCHOLAR — versioned scholar work, signed review, and how it gets live

## Account sign-off submission bridge

The optional account bridge accepts an HMAC-authenticated request from the Worker
for an explicitly approved, exact private revision. Configure an owner-only
`--bridge-secret-file` outside the repository, and the same value in the Worker
`SCHOLAR_BRIDGE_SECRET`. Put the localhost-only service behind HTTPS and set the
Worker `SCHOLAR_BRIDGE_URL` to that HTTPS origin. `--tokens-file` remains optional
for the legacy bearer flow; existing session-cookie authentication remains separate.
Rotate bridge credentials securely and never commit them.

The bridge rechecks the Scheme A snapshot hash and rights declaration, imports the
version in an isolated Git worktree, verifies the current proof and cross-layer song
validator, and records a self-attested author ReviewEvent for the exact version and
content hash. Author approval is not independent peer review and does not by itself
promote the contribution to independently reviewed. AI-assisted text stays labelled.
Signed essays become content-addressed `scholar-essay/1` objects; `verify` checks
their address, attribution, rights and exact snapshot, not factual truth.
After a reviewed merge, `python3 tools/emit_scholar.py --all` regenerates Scholar
projections for every work with canonical T1 data in the sibling svread checkout.

With `--push-remote origin`, explicit submission may expose the signed text on a
public Git branch. It does not merge that branch or publish it on the reader; without
the remote the result is only a local preparation. Live operation still needs the
Worker migration, credentials, HTTPS proxy, site/browser gates and end-to-end testing.
Never send private examples, notes or unsigned drafts to public Git.

For the gated source and L4 evidence projection, see
`process/SCHOLAR-EVIDENCE-2026-11-03.md`.

**Status:** existing hub SHIPPED · 2026-11-03 · canonical reference for `scholar/` ledgers, `tools/scholar.py`,
`tools/emit_scholar.py` and the svread Scholar hub. Session history: `process/SCHOLAR-HUB-2026-11-03.md`.
The v2 intake and submission service in this branch need a deployment before use by the live site.
Gate: `check.py` → `scholar-valid`.

The existing v1 events and IDs remain readable. New layer versions use
`scholar-version/2`, with a full content-derived ID, contributor kind, pinned
structural schema and validator hashes, and separate canonical JSON files in
`<work>/scholar/objects/`. These files become Git blobs when committed. A local
import is not itself a remote publication or a human review.

> Anyone can edit any layer of the stack. Every edit is an append-only **version** that forks off
> the original or off anyone else's version. A scholar's judgment is a hash-bound **ReviewEvent**.
> The only path to "reviewed" is a **PromotionEvent**. A sign-off binds to a stack hash. The site
> renders projections; git holds truth.

## 1. The loop

```
show original (canonical bytes, never edited)
  → save an edit ──────────────► version (parent: null  = fork of ORIGINAL
  → fork someone's version ────►              parent: sv:… = child of that version)
  → ReviewEvent  (judgment bound to exact (target, content hash); evidence, never mutation)
  → PromotionEvent (from_status → to_status, basis[] names live reviews)
  → data/<song>.signoff.json (existing per-song schema + stack hash)
  → emit_scholar.py → svread/data/scholar/<work>.json (disposable projection)
  → svread Scholar hub renders it
```

## 2. Storage division (who holds what)

| Artifact | Home | Form | Trust |
|---|---|---|---|
| versions / reviews / promotions | git `<work>/scholar/*.jsonl` | append-only JSONL | truth |
| v2 base, content, and structural schema snapshots | git `<work>/scholar/objects/<sha256>.json` | canonical UTF-8 JSON | content-addressed snapshots |
| sign-offs | git `<work>/data/<song>.signoff.json` | one JSON doc | truth |
| canonical layer originals | git `<work>/data/*.json` | per-song layer files | truth |
| hub projection | git `svread/data/scholar/<work>.json` + `index.json` | generated JSON | disposable (rebuild) |
| browser drafts | svread `localStorage` | `local:…` ids | device-local, unpublished |
| signing key | `~/.scholar/key` (mode 600) | 32-byte secret, hex | NEVER in any repo |

Rule (same as CG's ledger division): **git never stores trust it cannot recompute, projections are
rebuildable, keys never travel.** Delete `svread/data/scholar/` entirely → `emit_scholar.py`
recreates it byte-for-byte from the ledgers.

## 3. Hashing — two exact schemes (do not interchange them)

**Scheme A — `canon` / `sha`** (versions, stack hashes, all ids in `scholar.py`):

```python
canon(obj) = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                        ensure_ascii=False).encode("utf-8")
sha(obj)   = sha256(canon(obj)).hexdigest()          # 64 hex
```

**Scheme B — `contract_sha`** (ReviewEvent / PromotionEvent hashes — exact match to
`tools/human_authority/contracts_human_authority.py`, which uses **default** separators):

```python
contract_sha(obj) = sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()
```

Getting these backwards is the one way to make `scholar-valid` fail on untampered data.

### Derived identifiers

| Id | Formula | Exactness |
|---|---|---|
| legacy `version_id` | `"sv:" + sha({work, layer, target, parent, author, content_sha256, created_at})[:16]` | historical scheme, unchanged |
| v2 `version_id` | `"sv:" + sha(version fields except version_id)` | full SHA-256 including identity, content, schema and provenance |
| `content_sha256` / `base_sha256` | `sha(content)` / `sha(original layer content)` | 64 hex, full |
| `review_id` | `"pt:review:REV-" + sha16({work, song, by, hash, at})[:12]` | 12 hex |
| `promotion_id` | `"pt:promotion:PRO-" + sha16({…, basis, at})[:12]` | 12 hex |
| `event_hash` | `contract_sha(body − event_hash)` | computed by `ReviewEvent.emit()` **before** signer/signature exist |
| `promotion_hash` | `contract_sha(body − promotion_hash)` | same |
| `stack_sha(song)` | `sha({layer: sha(layer_json) for each existing data/<song>.<layer>.json})` | the sign-off target |
| local draft id | `"local:" + crypto.randomUUID()` where available; local hash fallback | device-local, NOT verifiable outside the browser |

### Signature semantics

- Existing signatures without `signature_version` sign the review ID only. They remain
  verifiable and receive a warning; they do not bind the complete review statement.
- New `event-hash-ed25519-v2` signatures cover the domain-separated complete `event_hash`.
  The hash covers the review body, including its target, decision and reasoning.
- `signer`, `signature`, and `signature_version` sit outside the event hash. A key proves
  key possession; reviewer identity remains self-attested until independently verified.
- Display address: `sha256(pubkey)[:16]`.

## 4. `versions.jsonl` — one line per scholar version

| Field | Type | Rule |
|---|---|---|
| `version_id` | `sv:16hex` (v1) or `sv:64hex` (v2) | = `vid_of(line)`; recomputed by verify |
| `work` | slug | must match the ledger's directory |
| `layer` | `t1\|l0\|argmap\|l2\|c1\|l3\|l4\|c2` | the stack layer being edited |
| `target` | `param-p01-v01` (c1/c2: the song id) | must resolve to a canonical row |
| `parent` | `null` \| `sv:…` \| `local:…` | `null` = fork of the ORIGINAL; otherwise child of that version — forks of forks to any depth |
| `base_sha256` | 64 hex | `sha(original content)` — pins which original the fork descends from |
| `author` / `author_kind` | string / `human\|agent` | v2 attribution; a self-attested name is not identity verification |
| `created_at` | ISO Z | part of the v1 and v2 version-id input |
| `note` | string | why |
| `content_sha256` | 64 hex | `sha(content)`; recomputed by verify |
| `content` | object or array | the complete layer-shaped edit (L0 is a list of tokens) |
| `status` | `MACHINE_DRAFT` or `HUMAN_DRAFT` for v2 | review status is derived from separate events |

Worked example (real lines, in order — the session's fork test):

```
sv:ac094e65ee9be6aa  owner           parent=null            (fork of ORIGINAL)
└ sv:27579b10525aa57d  second-scholar parent=sv:ac094e…     (child of owner's)
  └ sv:e8043a98ddb79e50  owner         parent=sv:27579b…     (grandchild)
```

## 5. `reviews.jsonl` — ReviewEvents (vendored `tools/human_authority/`)

Flat dict = `ReviewEvent.emit()` body **plus** optional `signer` / `signature`:

| Field | Rule |
|---|---|
| `review_id` | `pt:review:REV-12hex`, unique per ledger |
| `review_target` | `{object_ref, version, hash, layer}` — `object_ref` is `original:<work>:<song>` or an `sv:…`; `hash` = the **exact** content hash judged |
| `reviewer` | `{person_ref, display_name, identity_state, domains, …}` |
| `decision` | `ACCEPT \| ACCEPT_WITH_QUALIFICATION \| DISPUTE \| PROPOSE_ALTERNATIVE \| ABSTAIN \| OUT_OF_SCOPE` |
| `review_scope` | `LOCAL_PASSAGE \| LOCAL_SECTION \| SAME_WORK \| SYSTEMATIC` |
| `reasoning` | why |
| `event_hash` | `contract_sha` over everything except `event_hash`, `signer`, `signature` |
| `signer`/`signature` | optional Ed25519 pair (§3) |

**A ReviewEvent never mutates its target.** It is evidence about one exact hash; if the target's
content changes, the old review simply no longer matches (§9).

## 6. `promotions.jsonl` — PromotionEvents (the only path to reviewed)

| Field | Rule |
|---|---|
| `promotion_id` | `pt:promotion:PRO-12hex` |
| `object_ref` / `object_version` | what was promoted + the hash it was promoted at |
| `from_status` → `to_status` | e.g. `NOT_REVIEWED → INDEPENDENT_REVIEWED` |
| `basis` | **must name live `review_id`s** — verify fails on any dangling basis |
| `promotion_hash` | `contract_sha` over body minus itself |

## 7. Sign-off — one command, three records

```bash
python3 tools/scholar.py signoff --work paramarthasara --song param-p01 --by owner \
    --scope full [--key ~/.scholar/key] [--note "…"]
```

Writes, in order (any schema failure aborts before writing the signoff):

1. **ReviewEvent** over `stack_sha(song)` — object_ref `original:paramarthasara:param-p01`,
   decision ACCEPT, signed if a key exists.
2. **PromotionEvent** — `NOT_REVIEWED → REVIEWED`, `basis=[review_id]`.
3. **`data/<song>.signoff.json`** — `{song, accepted_by, date, scope, notes}` validated by
   `schemas/signoff.py` (the same file `validate_song` and the site read).

Real first sign-off (2026-11-03): stack `721f8a8bfe2c24bce0b751dcc8a7687f0f4a5a94a5ecf131358eae3c07fc5264`,
review `pt:review:REV-136905f1872e` (Ed25519 ✓, signer `8641ac2a…93f8`, address `165f9614d7587181`),
promotion `pt:promotion:PRO-01617d6e1b3e`.

## 8. Commands (all verified against this repo)

```bash
python3 tools/scholar.py keygen                    # ~/.scholar/key, mode 600 — NEVER commit
python3 tools/scholar.py show  --work paramarthasara --layer l3 --target param-p01-v01
python3 tools/scholar.py show  --work … --version sv:ac094e65ee9be6aa
python3 tools/scholar.py save  --work … --layer l3 --target param-p01-v01 \
    --author NAME --body '{"lines":["…"]}' [--parent sv:…] [--note "…"]
python3 tools/scholar.py fork  --work … --layer l3 --target param-p01-v01 \
    --from sv:ac094e65ee9be6aa --author NAME [--body …]   # no --body = carry content, edit next
python3 tools/scholar.py log   --work paramarthasara [--target … --layer …]
python3 tools/scholar.py signoff --work … --song … --by … [--scope full|t1-l0|l2|c1|spot]
python3 tools/scholar.py promote --work … --object … --version … --basis rv1,rv2
python3 tools/scholar.py verify --work paramarthasara      # exit 0/1
python3 tools/scholar.py import --file /path/to/scholar-export.json
python3 tools/emit_scholar.py --work paramarthasara         # projection → svread
```

`save` refuses hollow content (`content is empty — refusing a hollow version`). `fork` refuses a
cross-target fork (a fork stays on the layer+target it descends from).

## 9. `verify` — what is checked (fail-closed)

Called by `check.py` as step **`scholar-valid`** for every work with a `scholar/` directory:

1. every version has all 12 fields, right work, right layer;
2. `version_id` **recomputes** from its own fields (duplicate ids impossible);
3. v1 `content_sha256` and `base_sha256` recompute against the legacy original; v2
   content, original snapshot and structural-schema objects recompute independently;
4. every `parent` resolves (second pass, order-independent);
5. every ReviewEvent `event_hash` recomputes; `review_id` unique; target resolves; review hash
   equals the target's content hash;
6. every signature verifies against its `signer` (signature without signer = fail);
7. every PromotionEvent `promotion_hash` recomputes; every `basis` names an acceptance
   for the same object and content hash;
8. every `signoff.json` passes `schemas/signoff.py` **and** is backed by a ReviewEvent;
9. **staleness (WARN, not fail):** signoff's stored review hash ≠ current `stack_sha` ⇒
   `signoff … stack changed since signoff (review re-opened)` — honest signal, human decides.

Tamper test (proven): one byte flipped inside a review's `reasoning` ⇒ exit 1
(`event_hash does not recompute`). Restore ⇒ exit 0.

## 10. Emit → svread (projection contract)

```bash
python3 tools/emit_scholar.py --work paramarthasara
# → /root/svread/data/scholar/paramarthasara.json + index.json
```

Emitted top-level keys: `work · generated · source · originals · versions · reviews ·
promotions · signoffs · stack_hashes`.

- `originals.<layer>` — canonical content for every target (`l3[param-p01-v01]` is the full row;
  `c1` is song-scoped). Sourced from `data/<song>.<layer>.json`, the same bytes `show` prints —
  the hub never re-derives them.
- `signoffs[]` — each signoff plus its `stack_sha` and `review_id`.
- `index.json` — per-work counts, for the hub's works list.
- Re-run after every ledger change; the file is disposable.

## 11. svread hub contract (`?work=X&view=scholar`)

Same functions and classes as the reader (`$`/`esc`/`get`/`W`/`dl`/`norm`; `.col`/`.verbar`/
`.version-select`/`.text`/`.varbox textarea`+`.savebtn`/`.widget`/`.wtable`/`.vref-list`/`.c2row`/
`.urn`/`.milestone`/`.cmp-note`). Reader path untouched: without `?view=scholar`, `main()` runs
exactly as before.

| Concern | Exact rule |
|---|---|
| data | `data/scholar/<WORK>.json`; missing file ⇒ works list from `index.json` |
| layer/target state | `localStorage['svv-schol-<WORK>'] = {layer, target}` |
| drafts | `localStorage['svv-scholar-<WORK>']` = array of draft versions (`local:` ids, `parent` = base chosen) |
| author | `localStorage['svv-scholar-author']` |
| edit modes | `field` layers (t1 `quick_english`, l2 `plain_english`, l3/l4 `lines[]`) edit one field of the original row; `json` layers (l0, argmap, c1, c2) edit the full object or L0 token list — content stays layer-shaped |
| base | Original **or** any published `sv:…` **or** any of your `local:…` drafts ⇒ save produces a child of it (fork-of-fork, any depth) |
| publish | **Export JSON** downloads a parent-first submission → `tools/scholar.py import --file` → commit the ledger and objects → re-emit. An optional authenticated service can submit from the browser into a separate Git branch for review. |
| gate | drafts are never served to anyone else; only ledger lines are |

## 12. Invariants (binding)

1. Ledgers append, never rewrite. No rebase of history, no edits in place — corrections are new lines.
2. The signing key never enters a repo, a chat, or an emitted file.
3. A ReviewEvent never mutates its target; only a PromotionEvent changes status, and it names its `basis`.
4. A sign-off is bound to a stack hash. Stack moves ⇒ review re-opens (warn in verify; re-sign, never hand-edit).
5. `MACHINE_DRAFT` until a human sign-off; `check.py` green (`scholar-valid`) before any commit.
6. Projections (`svread/data/scholar/`) are rebuilt, never hand-edited.
7. Scheme A vs Scheme B hashes are never interchanged (§3).
8. Browser drafts are device-local and unpublished until exported into the ledger.

## 13. Rights (owner directive, 2026-11-03)

- **Our English translation** (L1–L4 + commentary) = **FREE** — every emitted site chunk carries
  `"license": "FREE"`; the reader's Attributions states it.
- **Scholar words** (versions, reviews, sign-offs, browser drafts) = **(c) their authors, all
  rights reserved.** Carried in the emitted `rights` block (`emit_scholar.py`), shown in the
  Scholar hub. FREE never covers the scholars' edits.

## 14. Honest limits (as shipped)

- **Identity:** `signer` proves key possession, not who holds the key. `SELF_ATTESTED` vs
  `VERIFIED` = signed vs unsigned, nothing more. Admin-verified identities are future work.
- **Stale signoffs warn, they do not fail** the gate (deliberate: the machine signals, the human decides).
- **Browser submission requires the optional service** (§16). The offline alternative is
  Export JSON → `scholar.py import` → commit and re-emit.
- **`local:` ids are not content-derived** (wall-clock salt) — they are fork parents inside one
  browser only; publication re-issues them as `sv:…` ids.

## 15. Private scholar style

`tools/style_profile.py prepare` collects the named scholar's own L2, L3, or L4 edits
and any explicit L0 choices. It accepts private browser-export files with
`--private-drafts`; they are never added to the shared ledger by preparing a brief.
For a target passage, the brief includes the source lines, available canonical layers,
and at most one example per edited passage. Three distinct passages are required before
rendering. Legacy versions without a contributor kind are excluded unless explicitly
requested with `--include-legacy`.

`style_profile.py render --profile <private-file> --runner '<command>' --agent <id>
--consent` sends the private brief to the explicitly chosen command on stdin. The
command returns JSON with `model` and `content`, where content contains only the
requested `lines` or `plain_english` field. The result is a Scholar submission whose
author is the agent. It carries the scholar's name and brief hash as provenance, not
the private examples. Importing a submission does not commit or publish it. The optional
`tools/style_runner_openai.py` runner uses an explicitly configured compatible endpoint,
model, and optional key from `STYLE_API_URL`, `STYLE_MODEL`, and `STYLE_API_KEY`. The
operator must select an authorized provider and free-tier model. A generated result is
an agent draft and still requires source and cross-layer review.

## 16. Authenticated browser submissions

`tools/scholar_service.py` maps bearer-token hashes in an operator-managed private file
to contributor names. It validates submissions with `scholar.py import` in a fresh Git
worktree and writes a separate `scholar/submission-…` branch. A successful submission
does not merge or deploy the branch. The service uses the committed repository revision,
never the caller's author field, and retries return the same branch. The optional
`--push-remote origin` pushes that branch without force.

The token file must be outside this repository, readable only by its owner, and shaped
as `{"users":[{"author":"Scholar name","token_sha256":"<SHA-256 hex>"}]}`.
Use long, randomly generated tokens and share each token privately with its scholar.
The service binds to `127.0.0.1` and requires an HTTPS reverse proxy for remote access.
Start it with `python3 tools/scholar_service.py --tokens-file <private-path> --origin
https://svread.pages.dev`, optionally with `--push-remote origin`. The server, reverse
proxy, Git remote credentials, token distribution, branch review, and site deployment
still need operator configuration. The browser sends the token to the configured server
and does not store it. This token system associates an account with a configured name;
it is not independent verification of a scholar's identity.

### Signed essay passage references

An essay snapshot may include a `citations` array (up to ten distinct
`{work,target,t1_sha256,projection_sha256}` objects). It is part of the exact
snapshot covered by author sign-off. The account bridge validates each cited
work and passage against a committed Git tree, checks its proof gate and T1
hash, and records `source_git_commit` in the resulting essay object. When a
source manifest exists, the bridge also checks the proof's current layer hashes.
Ghaṭakarpara references remain withheld pending source alignment repair.

The projection hash is a client-reported reference, not authenticated by this
bridge. A passing deterministic proof is not a human philological review. The
bridge does not determine whether a passage supports an essay's argument or
verify external scholarly citations. Earlier essays without this optional field
continue to be accepted. Do not place private notebook notes in public citations.

### Known source-coverage hold

The Scholar emitter withholds every Ghaṭakarpara song and all derived layers,
versions, reviews, essays and source evidence until its incomplete source
alignment and dependent data are repaired and reviewed upstream. Its previous
PASS proofs did not detect missing first lines. The projection records the hold;
removing it requires a source audit and fresh validation, not merely a hash.
