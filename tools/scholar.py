#!/usr/bin/env python3
"""tools/scholar.py — scholar versions · forks · reviews · sign-offs (the git for the stack).

Endgame loop (process/SCHOLAR-HUB-2026-11-03.md):
  show an original layer → save an edit (a version) → another scholar forks THAT version
  (child, any depth) → ReviewEvent binds to the exact (target, hash) → PromotionEvent +
  signoff.json → emitted live to svread.

Append-only everywhere: nothing is ever rewritten. `verify` re-derives every id, hash and
fork link and fails closed. Signatures are Ed25519 over the event id (qp_acom semantics:
the signature rides OUTSIDE the hashed body; kernel never forges).

  python3 tools/scholar.py keygen
  python3 tools/scholar.py show  --work paramarthasara --layer l3 --target param-p01-v01
  python3 tools/scholar.py save  --work paramarthasara --layer l3 --target param-p01-v01 \
      --author NAME --body '{"lines":["…"]}' [--note "…"]
  python3 tools/scholar.py fork  --work … --layer … --target … --from sv:… --author NAME [--body …]
  python3 tools/scholar.py log   --work paramarthasara [--target T --layer L]
  python3 tools/scholar.py signoff --work paramarthasara --song param-p01 --by NAME \
      [--scope full] [--key ~/.scholar/key] [--note "…"]
  python3 tools/scholar.py verify --work paramarthasara
"""
from __future__ import annotations
import argparse, fcntl, hashlib, json, os, re, sys, tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools" / "human_authority"))
from contracts_human_authority import (  # noqa: E402
    ReviewEvent, ReviewerIdentity, ReviewTarget, PromotionEvent)
import ed25519  # noqa: E402
from schemas import SCHEMA_VERSION  # noqa: E402
from schemas import registry as layer_registry  # noqa: E402

LEGACY_STACK_LAYERS = ("t1", "l0", "argmap", "l2", "c1", "l3", "l4")
LAYERS = (*LEGACY_STACK_LAYERS, "c2")
VERSION_SCHEMA = "scholar-version/2"
REVIEW_SIGNATURE_V2 = "event-hash-ed25519-v2"
DEFAULT_KEY = Path.home() / ".scholar" / "key"

# ----------------------------------------------------------------- helpers

def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")

def sha(obj) -> str:
    return hashlib.sha256(canon(obj)).hexdigest()

def sha16(obj) -> str:
    return sha(obj)[:16]

def contract_sha(obj) -> str:
    """Exact hashing of contracts_human_authority (default json separators)."""
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def review_signature_message(event: dict) -> bytes:
    return b"svatantrya-review-v2\0" + bytes.fromhex(event["event_hash"])

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def die(msg: str) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def jread(p: Path):
    if not p.exists():
        die(f"missing {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def jsonl_read(p: Path) -> list:
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            die(f"{p}:{i}: bad JSON ({e})")
    return out

def jsonl_append(p: Path, obj: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def vpath(work): return ROOT / work / "scholar" / "versions.jsonl"
def rpath(work): return ROOT / work / "scholar" / "reviews.jsonl"
def ppath(work): return ROOT / work / "scholar" / "promotions.jsonl"


def validate_work(work: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", work or ""):
        die("work must be a lowercase work slug")
    if not (ROOT / work / "data").is_dir():
        die(f"no canonical data directory for {work}")


@contextmanager
def version_lock(work: str):
    validate_work(work)
    directory = vpath(work).parent
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".versions.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def object_path(work: str, digest: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{64}", digest or ""):
        die("invalid object digest")
    return ROOT / work / "scholar" / "objects" / f"{digest}.json"


def store_object(work: str, content) -> str:
    digest = sha(content)
    path = object_path(work, digest)
    data = canon(content)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            die(f"object {digest} does not match its content")
        return digest
    fd, temp = tempfile.mkstemp(prefix=".object-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return digest


def append_versions(work: str, versions: list[dict], objects: dict) -> None:
    """Atomically append a complete batch while the caller holds version_lock."""
    if not versions:
        return
    path = vpath(work)
    prior = path.read_bytes() if path.exists() else b""
    if prior and not prior.endswith(b"\n"):
        die("version ledger has an incomplete last line")
    for digest, content in objects.items():
        if store_object(work, content) != digest:
            die("object changed during submission")
    extra = b"".join(json.dumps(v, ensure_ascii=False).encode("utf-8") + b"\n"
                     for v in versions)
    fd, temp = tempfile.mkstemp(prefix=".versions-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(prior + extra)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

# ------------------------------------------------------------ originals

def song_of(target: str, layer: str) -> str:
    if layer in layer_registry.SONG_LAYERS:
        return target                      # C1 and C2 are song-scoped
    m = re.match(r"^(.*?)-v\d+$", target)
    if m:
        return m.group(1)
    # Some older one-passage songs use the song ID as the verse ID. The
    # canonical loader still requires the target to exist in that song file.
    if isinstance(target,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',target):
        return target
    die(f"invalid target {target!r}")

def load_original(work: str, layer: str, target: str):
    """Return (content, file) for the canonical layer content being edited."""
    if layer not in LAYERS:
        die(f"layer must be one of {LAYERS}")
    song = song_of(target, layer)
    f = ROOT / work / "data" / f"{song}.{layer}.json"
    if not f.exists():
        die(f"no canonical {layer} file for this target: {f}")
    d = json.loads(f.read_text(encoding="utf-8"))
    if layer in layer_registry.SONG_LAYERS:
        if target != d.get("song", target):
            die(f"{f} is song {d.get('song')!r}, target says {target!r}")
        return d, f
    rows = [r for r in d if r.get("verse_id") == target]
    if not rows:
        die(f"no {layer} row for {target} in {f}")
    if layer == "l0":
        return rows, f                      # token rows for the verse
    if len(rows) != 1:
        die(f"expected exactly 1 {layer} row for {target}, found {len(rows)}")
    return rows[0], f

def stack_sha(work: str, song: str) -> tuple[str, dict]:
    """Content hash of the song's whole canonical stack (the signoff target)."""
    stack = {}
    # Existing signoffs use this exact historical set and hash scheme.
    for layer in LEGACY_STACK_LAYERS:
        f = ROOT / work / "data" / f"{song}.{layer}.json"
        if f.exists():
            stack[layer] = sha(json.loads(f.read_text(encoding="utf-8")))
    if not stack:
        die(f"no canonical layer files for {song}")
    return sha(stack), stack

# ------------------------------------------------------------ versions

def load_versions(work: str) -> list:
    return jsonl_read(vpath(work))

def vid_of(v: dict) -> str:
    if v.get("version_schema") == VERSION_SCHEMA:
        return "sv:" + sha({k: value for k, value in v.items() if k != "version_id"})
    return "sv:" + sha({
        "work": v["work"], "layer": v["layer"], "target": v["target"],
        "parent": v["parent"], "author": v["author"],
        "content_sha256": v["content_sha256"], "created_at": v["created_at"],
    })[:16]

def make_version(work, layer, target, parent, author, content, note="",
                 author_kind="human", versions=None, created_at=None,
                 submission_id=None, submission_hash=None, expected_base=None,
                 objects=None, provenance=None):
    if not content:
        die("content is empty — refusing a hollow version")
    snapshot_errors = layer_registry.snapshot_errors()
    if snapshot_errors:
        die("; ".join(snapshot_errors))
    if author_kind not in ("human", "agent"):
        die("author kind must be human or agent")
    if not isinstance(author, str) or not author.strip():
        die("author is required")
    if not isinstance(target, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", target):
        die("invalid target")
    originals, _f = load_original(work, layer, target)
    base = originals
    parent_version = None
    if parent:
        parent_version = {v["version_id"]: v for v in (versions or [])}.get(parent)
        if not parent_version:
            die(f"parent {parent} not found")
        if parent_version["layer"] != layer or parent_version["target"] != target:
            die("parent must have the same layer and target")
        if parent_version.get("version_schema") == VERSION_SCHEMA:
            base_digest = parent_version["base_sha256"]
            if objects is not None and base_digest in objects:
                base = objects[base_digest]
            else:
                base_file = object_path(work, base_digest)
                if not base_file.exists():
                    die("parent's original snapshot is missing")
                base = json.loads(base_file.read_text(encoding="utf-8"))
    if expected_base and sha(base) != expected_base:
        die("base has changed since this draft was created")
    editing_base = parent_version["content"] if parent_version else base
    if isinstance(base, dict) and isinstance(editing_base, dict):
        # Legacy versions may contain only the edited fields.
        editing_base = {**base, **editing_base}
    if isinstance(editing_base, dict) and isinstance(content, dict):
        if set(content) == {"text"}:
            field = {"t1": "quick_english", "l2": "plain_english",
                     "l3": "lines", "l4": "lines"}.get(layer)
            if field:
                content = {field: content["text"].splitlines() if field == "lines"
                           else content["text"]}
        content = {**editing_base, **content}
    errors = layer_registry.validate(layer, content)
    if layer == "l0" and isinstance(content, list):
        ids = [row.get("id") for row in content if isinstance(row, dict)]
        if len(ids) != len(set(ids)) or any(not item for item in ids):
            errors.append("L0 token IDs must be present and unique")
        if any(row.get("verse_id") != target for row in content if isinstance(row, dict)):
            errors.append("L0 tokens must belong to the target verse")
    elif isinstance(content, dict):
        if layer in layer_registry.SONG_LAYERS:
            if content.get("song") != target:
                errors.append("song must match target")
        else:
            if content.get("verse_id") != target or content.get("song") != song_of(target, layer):
                errors.append("verse_id and song must match target")
            if isinstance(base, dict) and content.get("verse") != base.get("verse"):
                errors.append("verse number must match the original")
    if errors:
        die("invalid layer content: " + "; ".join(errors))
    base_digest = sha(base)
    content_digest = sha(content)
    structural_schema = layer_registry.content_schema(layer)
    structural_schema_digest = sha(structural_schema)
    if objects is not None:
        objects[base_digest] = base
        objects[content_digest] = content
        objects[structural_schema_digest] = structural_schema
    validator_files = {}
    for name in (f"{layer}.py", "registry.py", "base.py", "__init__.py"):
        path = ROOT / "schemas" / name
        # Tests and offline consumers may use a separate data root.
        if not path.exists():
            path = Path(__file__).resolve().parent.parent / "schemas" / name
        validator_files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    v = {
        "version_schema": VERSION_SCHEMA, "schema_version": SCHEMA_VERSION,
        "structural_schema_version": layer_registry.STRUCTURAL_SCHEMA_VERSION,
        "structural_schema_sha256": structural_schema_digest,
        "validator_files_sha256": validator_files,
        "work": work, "layer": layer, "target": target, "parent": parent,
        "base_sha256": base_digest, "author": author.strip(),
        "author_kind": author_kind, "created_at": created_at or now(),
        "note": note, "content_sha256": content_digest, "content": content,
        "status": "MACHINE_DRAFT" if author_kind == "agent" else "HUMAN_DRAFT",
        "validation_scope": "layer",
    }
    if submission_id:
        v["submission_id"] = submission_id
        v["submission_hash"] = submission_hash
    if provenance:
        if not isinstance(provenance, dict) or any(
            key not in ("style_author", "style_profile_sha256", "model") or
            not isinstance(value, str) or not value.strip()
            for key, value in provenance.items()
        ):
            die("invalid version provenance")
        digest = provenance.get("style_profile_sha256")
        if digest and not re.fullmatch(r"[0-9a-f]{64}", digest):
            die("invalid style profile digest")
        v["provenance"] = provenance
    v["version_id"] = vid_of(v)
    return {"version_id": v.pop("version_id"), **v}

def parse_body(args) -> dict:
    if getattr(args, "body", None):
        try:
            return json.loads(args.body)
        except json.JSONDecodeError:
            return {"text": args.body}          # plain text edit
    if getattr(args, "file", None):
        p = Path(args.file)
        if not p.exists():
            die(f"--file not found: {p}")
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"text": p.read_text(encoding="utf-8")}
    return None

# ------------------------------------------------------------ signoff targets

def load_signoff(work, song):
    p = ROOT / work / "data" / f"{song}.signoff.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

# ------------------------------------------------------------ verify

def essay_errors(essay: dict, work: str, filename: str) -> list[str]:
    if not isinstance(essay,dict):return [f'{filename}: essay must be an object']
    digest=sha({key:value for key,value in essay.items() if key!='essay_id'})
    errors=[]
    if essay.get('format')!='scholar-essay/1' or essay.get('work')!=work:
        errors.append(f'{filename}: invalid format or work')
    if essay.get('essay_id')!='essay:'+digest or filename!=digest+'.json':
        errors.append(f'{filename}: content address does not match')
    snap,approval=essay.get('snapshot'),essay.get('signoff')
    if not isinstance(snap,dict) or not isinstance(approval,dict) or approval.get('snapshot_sha256')!=sha(snap):
        errors.append(f'{filename}: sign-off does not match snapshot')
    else:
        content=snap.get('content')
        if (not isinstance(content,dict) or snap.get('kind')!='essay' or snap.get('work')!=work or
            essay.get('target')!=snap.get('target') or essay.get('title')!=snap.get('title') or
            essay.get('text')!=content.get('text') or essay.get('rights')!=approval.get('rights') or
            essay.get('assisted')!=bool(content.get('assisted')) or
            essay.get('model')!=str(content.get('model',''))[:120]):
            errors.append(f'{filename}: essay differs from signed snapshot')
        citations=content.get('citations',[]) if isinstance(content,dict) else []
        if not isinstance(citations,list) or len(citations)>10:
            errors.append(f'{filename}: invalid citations')
        else:
            seen=set()
            for ref in citations:
                if (not isinstance(ref,dict) or set(ref)!={'work','target','t1_sha256','projection_sha256'} or
                    not isinstance(ref.get('work'),str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}',ref['work']) or
                    not isinstance(ref.get('target'),str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,159}',ref['target']) or
                    any(not isinstance(ref.get(k),str) or not re.fullmatch(r'[a-f0-9]{64}',ref[k]) for k in ('t1_sha256','projection_sha256'))):
                    errors.append(f'{filename}: invalid citation')
                    continue
                if (ref['work'],ref['target']) in seen:errors.append(f'{filename}: duplicate citation')
                seen.add((ref['work'],ref['target']))
            if citations and (not isinstance(essay.get('source_git_commit'),str) or not re.fullmatch(r'[a-f0-9]{40,64}',essay['source_git_commit'])):
                errors.append(f'{filename}: missing cited source Git commit')
        if (not isinstance(essay.get('title'),str) or not essay['title'].strip() or
            not isinstance(essay.get('text'),str) or not essay['text'].strip() or
            essay.get('rights') not in ('all-rights-reserved','cc-by-4.0','cc0') or
            not isinstance(approval.get('id'),str) or not approval['id'].startswith('signoff:')):
            errors.append(f'{filename}: invalid title, text, rights or sign-off')
    if (not isinstance(essay.get('author'),str) or not essay['author'].strip() or
        not isinstance(essay.get('author_id'),str) or not essay['author_id'].strip() or
        essay.get('identity_state')!='SELF_ATTESTED'):
        errors.append(f'{filename}: invalid author attribution')
    return errors

def verify(work: str) -> int:
    fails, warns = [], []
    for file in sorted((ROOT/work/'scholar/essays').glob('*.json')):
        try:fails.extend(essay_errors(json.loads(file.read_text(encoding='utf-8')),work,file.name))
        except (OSError,ValueError,TypeError):fails.append(f'{file.name}: invalid essay JSON')
    versions = load_versions(work)
    by_id = {}
    for i, v in enumerate(versions, 1):
        missing = []
        for k in ("version_id", "work", "layer", "target", "parent",
                  "base_sha256", "author", "created_at", "content_sha256",
                  "content", "status"):
            if k not in v:
                missing.append(f"versions:{i} missing field {k}")
        if missing:
            fails.extend(missing)
            continue
        if v["work"] != work:
            fails.append(f"versions:{i} work {v['work']} != {work}")
        if v["layer"] not in LAYERS:
            fails.append(f"versions:{i} bad layer {v['layer']}")
        if v["version_id"] in by_id:
            fails.append(f"versions:{i} duplicate id {v['version_id']}")
        by_id[v["version_id"]] = v
        if sha(v["content"]) != v["content_sha256"]:
            fails.append(f"{v['version_id']}: content hash mismatch")
        if vid_of(v) != v["version_id"]:
            fails.append(f"{v['version_id']}: id does not recompute")
        if v.get("version_schema") == VERSION_SCHEMA:
            missing_v2 = [field for field in ("structural_schema_sha256", "structural_schema_version",
                                             "validator_files_sha256", "author_kind") if field not in v]
            if missing_v2:
                fails.append(f"{v['version_id']}: missing v2 fields {', '.join(missing_v2)}")
                continue
            for field in ("base_sha256", "content_sha256", "structural_schema_sha256"):
                try:
                    path = object_path(work, v[field])
                    if not path.exists() or path.read_bytes() != canon(json.loads(path.read_text(encoding="utf-8"))):
                        fails.append(f"{v['version_id']}: {field} object missing or noncanonical")
                    elif sha(json.loads(path.read_text(encoding="utf-8"))) != v[field]:
                        fails.append(f"{v['version_id']}: {field} object hash mismatch")
                except (SystemExit, OSError, ValueError, json.JSONDecodeError):
                    fails.append(f"{v['version_id']}: invalid {field} object")
            current_hashes = {}
            for name in (f"{v['layer']}.py", "registry.py", "base.py", "__init__.py"):
                path = ROOT / "schemas" / name
                if not path.exists():
                    path = Path(__file__).resolve().parent.parent / "schemas" / name
                if path.exists():
                    current_hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
            if v.get("author_kind") not in ("human", "agent"):
                fails.append(f"{v['version_id']}: invalid author kind")
            elif v.get("status") != ("MACHINE_DRAFT" if v["author_kind"] == "agent" else "HUMAN_DRAFT"):
                fails.append(f"{v['version_id']}: draft status does not match author kind")
            try:
                schema_path = object_path(work, v.get("structural_schema_sha256", ""))
                saved_schema = json.loads(schema_path.read_text(encoding="utf-8"))
                fails.extend(f"{v['version_id']}: {error}" for error in
                             layer_registry.structural_errors(v["content"], saved_schema, "content"))
                if current_hashes == v.get("validator_files_sha256"):
                    fails.extend(f"{v['version_id']}: {error}" for error in
                                 layer_registry.validate(v["layer"], v["content"]))
                else:
                    warns.append(f"{v['version_id']}: validator changed; historical semantic validation not rerun")
            except (SystemExit, OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                fails.append(f"{v['version_id']}: saved schema could not be checked ({exc})")
        else:
            try:
                base, _ = load_original(work, v["layer"], v["target"])
                if sha(base) != v["base_sha256"]:
                    fails.append(f"{v['version_id']}: base_sha256 no longer matches the "
                                 "canonical original (original was edited — re-cut required)")
            except SystemExit:
                fails.append(f"{v['version_id']}: target/layer unresolvable")
        if v["parent"] is not None and v["parent"] not in by_id and \
           v["parent"] not in {x.get("version_id") for x in versions}:
            fails.append(f"{v['version_id']}: parent {v['parent']} does not exist")
    # parents must exist (second pass: order-independent)
    ids = set(by_id)
    for v in versions:
        if v.get("parent") and v["parent"] not in ids:
            fails.append(f"{v.get('version_id')}: dangling parent {v['parent']}")
        elif v.get("parent") and v.get("version_schema") == VERSION_SCHEMA:
            parent = by_id[v["parent"]]
            if any(parent.get(k) != v.get(k) for k in ("work", "layer", "target", "base_sha256")):
                fails.append(f"{v.get('version_id')}: parent has a different target or base")

    # reviews
    review_ids = set()
    review_records = {}
    for i, r in enumerate(jsonl_read(rpath(work)), 1):
        sig = r.pop("signature", "")
        signer = r.pop("signer", "")
        signature_version = r.pop("signature_version", "")
        if signer and not sig:
            fails.append(f"reviews:{i}: signer without signature")
        if not ReviewEvent.verify(r):
            fails.append(f"reviews:{i} event_hash does not recompute")
        rid = r.get("review_id", "")
        if rid in review_ids:
            fails.append(f"reviews:{i} duplicate review_id {rid}")
        review_ids.add(rid)
        review_records[rid] = r
        tgt = r.get("review_target", {})
        h = tgt.get("hash", "")
        oref = tgt.get("object_ref", "")
        if oref.startswith("sv:"):
            if oref not in ids:
                fails.append(f"reviews:{i}: target {oref} not a known version")
            elif by_id[oref]["content_sha256"] != h:
                fails.append(f"reviews:{i}: review hash != target content hash")
        if sig:
            if not signer:
                fails.append(f"reviews:{i}: signature without signer")
            else:
                try:
                    if signature_version == REVIEW_SIGNATURE_V2:
                        message = review_signature_message(r)
                    elif not signature_version:
                        message = r.get("review_id", "").encode()
                        warns.append(f"reviews:{i}: legacy signature covers review ID only")
                    else:
                        raise ValueError("unknown signature version")
                    if not ed25519.verify(bytes.fromhex(signer), message, bytes.fromhex(sig)):
                        fails.append(f"reviews:{i}: signature invalid")
                except (ValueError, KeyError):
                    fails.append(f"reviews:{i}: invalid signature format")
        r["signer"], r["signature"] = signer, sig   # keep file shape (read-only reinsert)

    # promotions
    for i, p in enumerate(jsonl_read(ppath(work)), 1):
        h = p.pop("promotion_hash", "")
        want = contract_sha(p)
        if h != want:
            fails.append(f"promotions:{i} promotion_hash does not recompute")
        p["promotion_hash"] = h
        for b in p.get("basis", []):
            if b not in review_ids:
                fails.append(f"promotions:{i}: basis review {b} not found")
                continue
            review = review_records[b]
            target = review.get("review_target", {})
            if target.get("object_ref") != p.get("object_ref") or target.get("hash") != p.get("object_version"):
                fails.append(f"promotions:{i}: basis review {b} targets different content")
            if review.get("decision") not in ("ACCEPT", "ACCEPT_WITH_QUALIFICATION"):
                fails.append(f"promotions:{i}: basis review {b} is not an acceptance")

    # signoffs (existing schema + staleness signal)
    sys.path.insert(0, str(ROOT / "schemas"))
    try:
        import signoff as signoff_s
    except Exception:
        signoff_s = None
    for so in sorted((ROOT / work / "data").glob("*.signoff.json")):
        d = json.loads(so.read_text(encoding="utf-8"))
        if signoff_s:
            errs = signoff_s.validate(d, so.name)
            fails += errs
        song = d.get("song", "")
        cur, _ = stack_sha(work, song)
        matching = [r for r in jsonl_read(rpath(work))
                    if r.get("review_target", {}).get("object_ref")
                    == f"original:{work}:{song}"]
        if not matching:
            fails.append(f"{so.name}: no ReviewEvent backs this signoff")
        else:
            last = matching[-1]
            if last.get("review_target", {}).get("hash") != cur:
                warns.append(f"{so.name}: stack changed since signoff "
                             "(review re-opened — honest staleness)")

    for w in warns:
        print(f"WARN {w}")
    print(f"scholar verify: {len(versions)} versions · "
          f"{len(review_ids)} reviews · signoffs checked — "
          f"{len(fails)} failures")
    for f in fails:
        print(f"FAIL {f}")
    return 1 if fails else 0

# ------------------------------------------------------------ commands

def cmd_show(a) -> int:
    if a.version:
        vs = {v["version_id"]: v for v in load_versions(a.work)}
        if a.version not in vs:
            die(f"no version {a.version}")
        content = vs[a.version]["content"]
        print(json.dumps(content, indent=1, ensure_ascii=False))
        print(f"# version_id={a.version} author={vs[a.version]['author']} "
              f"parent={vs[a.version]['parent']}", file=sys.stderr)
    else:
        content, f = load_original(a.work, a.layer, a.target)
        print(json.dumps(content, indent=1, ensure_ascii=False))
        print(f"# ORIGINAL {f}", file=sys.stderr)
    return 0

def cmd_save(a) -> int:
    content = parse_body(a)
    if content is None:
        die("give --body '<json>' or --file <path>")
    parent = a.parent if a.parent and a.parent != "none" else None
    with version_lock(a.work):
        versions = load_versions(a.work)
        objects = {}
        v = make_version(a.work, a.layer, a.target, parent, a.author, content,
                         a.note, author_kind=a.author_kind, versions=versions,
                         objects=objects)
        if any(row["version_id"] == v["version_id"] for row in versions):
            die("this version already exists")
        append_versions(a.work, [v], objects)
    print(f"saved {v['version_id']}  ({a.layer}:{a.target} "
          f"parent={'original' if parent is None else parent})")
    return 0

def cmd_fork(a) -> int:
    with version_lock(a.work):
        versions = load_versions(a.work)
        ids = {v["version_id"]: v for v in versions}
        if a.from_ not in ids:
            die(f"--from {a.from_} not found")
        parent = ids[a.from_]
        content = parse_body(a)
        if content is None:
            content = parent["content"]
        objects = {}
        v = make_version(a.work, a.layer, a.target, a.from_, a.author, content,
                         a.note or f"fork of {a.from_}", author_kind=a.author_kind,
                         versions=versions, objects=objects)
        if any(row["version_id"] == v["version_id"] for row in versions):
            die("this version already exists")
        append_versions(a.work, [v], objects)
    print(f"forked {a.from_} → {v['version_id']}  ({a.layer}:{a.target})")
    return 0


def cmd_import(a) -> int:
    payload = jread(Path(a.file))
    if not isinstance(payload, dict):
        die("submission must be a JSON object")
    work = payload.get("work")
    entries = payload.get("versions")
    if entries is None:
        entries = [payload]
    if not isinstance(entries, list) or not entries:
        die("submission must contain at least one version")
    if len(entries) > 100:
        die("submission may contain at most 100 versions")
    with version_lock(work):
        versions = load_versions(work)
        known = {v["version_id"]: v for v in versions}
        submitted = {v.get("submission_id"): v for v in versions if v.get("submission_id")}
        staged, objects, mapping = [], {}, {}
        for entry in entries:
            if not isinstance(entry, dict):
                die("each version must be an object")
            if entry.get("work", work) != work:
                die("all versions in a submission must belong to the same work")
            local_id = entry.get("version_id") or ("local:import-" + sha(entry))
            if not isinstance(local_id, str) or not local_id.startswith("local:"):
                die("each submitted version needs a local: identifier")
            if local_id in mapping:
                die(f"duplicate local identifier {local_id}")
            submission_id = sha({"work": work, "local_id": local_id})
            submission_hash = sha(entry)
            if submission_id in submitted:
                prior = submitted[submission_id]
                if prior.get("submission_hash") != submission_hash:
                    die(f"{local_id} was already imported with different content")
                mapping[local_id] = prior["version_id"]
                continue
            parent = entry.get("parent")
            if parent is not None and not isinstance(parent, str):
                die("parent must be a version ID or null")
            if parent and parent.startswith("local:"):
                if parent not in mapping:
                    die(f"local parent {parent} must appear earlier in the submission")
                parent = mapping[parent]
            if parent and parent not in known:
                die(f"parent {parent} not found")
            v = make_version(work, entry.get("layer"), entry.get("target"), parent,
                             entry.get("author"), entry.get("content"), entry.get("note", ""),
                             author_kind=entry.get("author_kind", "human"),
                             versions=versions + staged, submission_id=submission_id,
                             submission_hash=submission_hash,
                             expected_base=entry.get("base_sha256") or None,
                             objects=objects, provenance=entry.get("provenance"))
            if v["version_id"] in known:
                die("submission generated a duplicate version ID")
            staged.append(v)
            known[v["version_id"]] = v
            mapping[local_id] = v["version_id"]
        append_versions(work, staged, objects)
    print(json.dumps({"work": work, "imported": len(staged), "versions": mapping},
                     ensure_ascii=False, sort_keys=True, indent=2))
    return 0

def cmd_log(a) -> int:
    vs = load_versions(a.work)
    if a.target:
        vs = [v for v in vs if v["target"] == a.target and
              (not a.layer or v["layer"] == a.layer)]
    if not vs:
        print("no scholar versions yet")
        return 0
    groups = {}
    for v in vs:
        groups.setdefault((v["layer"], v["target"]), []).append(v)
    for (layer, target), rows in sorted(groups.items()):
        print(f"\n{layer}:{target}")
        kids = {}
        roots = []
        for v in rows:
            if v["parent"] in {r["version_id"] for r in rows}:
                kids.setdefault(v["parent"], []).append(v)
            else:
                roots.append(v)               # parent None (original) or outside filter
        def show(v, depth):
            print("  " * depth +
                  f"├ {v['version_id']}  {v['author']}  {v['created_at']}  "
                  f"{v['status']}  sha={v['content_sha256'][:12]}"
                  + (f"\n{'  '*(depth+1)}note: {v['note']}" if v.get("note") else ""))
            for k in kids.get(v["version_id"], []):
                show(k, depth + 1)
        for v in roots:
            if v["parent"] is None:
                print(f"  ├ {v['version_id']}  {v['author']}  {v['created_at']}  "
                      f"{v['status']}  sha={v['content_sha256'][:12]}  (fork of ORIGINAL)"
                      + (f"\n     note: {v['note']}" if v.get("note") else ""))
                for k in kids.get(v["version_id"], []):
                    show(k, 1)
        # chains whose parent is outside the filter
        for v in rows:
            if v["parent"] and v["parent"] not in {r["version_id"] for r in rows} \
               and v["parent"] in {x["version_id"] for x in load_versions(a.work)}:
                show(v, 1)
    return 0

def cmd_signoff(a) -> int:
    cur, stack = stack_sha(a.work, a.song)
    now_s = now()
    # 1. ReviewEvent over the song's canonical stack (exact hash)
    rid = "pt:review:REV-" + sha16({
        "work": a.work, "song": a.song, "by": a.by, "hash": cur, "at": now_s})[:12]
    ev = ReviewEvent(
        review_id=rid,
        review_target=ReviewTarget(
            object_ref=f"original:{a.work}:{a.song}", version="canonical",
            hash=cur, layer="stack"),
        reviewer=ReviewerIdentity(
            display_name=a.by, person_ref=a.by,
            identity_state="SELF_ATTESTED",
            domains=[a.work]),
        decision="ACCEPT",
        review_scope="LOCAL_SECTION",
        reasoning=a.note or f"stack signoff scope={a.scope}",
        created_at=now_s,
    )
    body = ev.emit()
    signer_hex, sig = "", ""
    key = Path(a.key).expanduser() if a.key else DEFAULT_KEY
    if key.exists():
        secret = bytes.fromhex(key.read_text().strip())
        pk = ed25519.pubkey(secret)
        signer_hex = pk.hex()
        sig = ed25519.sign(secret, review_signature_message(body)).hex()
        body["signer"], body["signature"] = signer_hex, sig
        body["signature_version"] = REVIEW_SIGNATURE_V2
    elif a.key:
        die(f"--key not found: {key}")
    else:
        print(f"NOTE: no key at {key} — review left unsigned "
              "(run `scholar.py keygen` to sign)")
    jsonl_append(rpath(a.work), body)

    # 2. PromotionEvent — the only path to reviewed (basis names the review)
    pid = "pt:promotion:PRO-" + sha16({
        "work": a.work, "song": a.song, "basis": rid, "at": now_s})[:12]
    pev = PromotionEvent(
        promotion_id=pid,
        object_ref=f"original:{a.work}:{a.song}",
        object_version=cur,
        from_status="NOT_REVIEWED",
        to_status="REVIEWED",
        basis=[rid],
        reason=f"signoff scope={a.scope} by {a.by}",
    ).emit()
    jsonl_append(ppath(a.work), pev)

    # 3. the existing per-song signoff schema (validate first, fail-closed)
    signoff = {"song": a.song, "accepted_by": a.by, "date": now_s[:10],
               "scope": a.scope,
               "notes": [a.note or "stack signoff via tools/scholar.py"]}
    sys.path.insert(0, str(ROOT / "schemas"))
    import signoff as signoff_s
    errs = signoff_s.validate(signoff, "signoff")
    if errs:
        die("signoff schema invalid: " + "; ".join(errs))
    sp = ROOT / a.work / "data" / f"{a.song}.signoff.json"
    sp.write_text(json.dumps(signoff, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"SIGNED OFF {a.work}:{a.song} scope={a.scope} by {a.by}")
    print(f"  stack_sha  {cur}")
    print(f"  review     {rid}" + ("  (Ed25519 ✓)" if sig else ""))
    print(f"  promotion  {pid}")
    print(f"  signoff    {sp.relative_to(ROOT)}")
    return 0

def cmd_approve_version(a) -> int:
    """Record an account author's approval, without claiming independent review."""
    versions = {v['version_id']:v for v in load_versions(a.work)}
    version = versions.get(a.version)
    if not version or version.get('author') != a.by or version.get('author_kind') != 'human':
        die('version or author does not match')
    if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',a.account_id):
        die('invalid account id')
    if not re.fullmatch(r'[0-9a-f]{64}',a.snapshot_sha256):
        die('invalid signed snapshot hash')
    if not re.fullmatch(r'signoff:[A-Za-z0-9-]{1,100}',a.signoff_id):
        die('invalid signoff id')
    stamp = now()
    rid = 'pt:review:REV-'+sha16({'version':a.version,'account':a.account_id,
                                  'signoff':a.signoff_id,'at':stamp})[:12]
    event = ReviewEvent(review_id=rid,
        review_target=ReviewTarget(object_ref=a.version,version='scholar-version/2',
                                   hash=version['content_sha256'],layer=version['layer']),
        reviewer=ReviewerIdentity(display_name=a.by,person_ref='account:'+a.account_id,
                                  identity_state='SELF_ATTESTED',domains=[a.work]),
        decision='ACCEPT',review_scope='LOCAL_SECTION',conflict_of_interest='AUTHOR',
        reasoning=f'Author account approval; rights={a.rights}; signoff={a.signoff_id}; snapshot={a.snapshot_sha256}',
        created_at=stamp).emit()
    with version_lock(a.work):
        jsonl_append(rpath(a.work),event)
    print(json.dumps({'review_id':rid,'version':a.version},sort_keys=True))
    return 0


def cmd_promote(a) -> int:
    now_s = now()
    basis = [b.strip() for b in a.basis.split(",") if b.strip()]
    known = {r.get("review_id"): r for r in jsonl_read(rpath(a.work))}
    missing = [b for b in basis if b not in known]
    if missing:
        die(f"basis reviews not found: {missing}")
    if not basis:
        die("at least one review is required")
    if a.to == "INDEPENDENT_REVIEWED":
        die("independent review requires an identity and independence policy")
    for review_id in basis:
        review = known[review_id]
        body = dict(review)
        signature = body.pop("signature", "")
        signer = body.pop("signer", "")
        signature_version = body.pop("signature_version", "")
        if signer and not signature:
            die(f"review {review_id} has a signer without a signature")
        if not ReviewEvent.verify(body):
            die(f"review {review_id} has an invalid event hash")
        if signature:
            try:
                if signature_version == REVIEW_SIGNATURE_V2:
                    message = review_signature_message(body)
                elif not signature_version:
                    message = review_id.encode()
                else:
                    raise ValueError("unknown signature version")
                if not signer or not ed25519.verify(bytes.fromhex(signer), message,
                                                    bytes.fromhex(signature)):
                    die(f"review {review_id} has an invalid signature")
            except ValueError:
                die(f"review {review_id} has an invalid signature format")
        target = review.get("review_target", {})
        if target.get("object_ref") != a.object or target.get("hash") != a.version:
            die(f"review {review_id} targets different content")
        if review.get("decision") not in ("ACCEPT", "ACCEPT_WITH_QUALIFICATION"):
            die(f"review {review_id} is not an acceptance")
    pid = "pt:promotion:PRO-" + sha16({
        "work": a.work, "object": a.object, "basis": basis, "at": now_s})[:12]
    pev = PromotionEvent(
        promotion_id=pid, object_ref=a.object, object_version=a.version,
        from_status=a.from_status, to_status=a.to, basis=basis,
        reason=a.reason).emit()
    jsonl_append(ppath(a.work), pev)
    print(f"promoted {a.object} {a.from_status} → {a.to}  ({pid})")
    return 0

def cmd_keygen(a) -> int:
    out = Path(a.out).expanduser()
    if out.exists() and not a.force:
        die(f"{out} exists — refusing to overwrite (use --force)")
    secret = os.urandom(32)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(secret.hex() + "\n")
    os.chmod(out, 0o600)
    pk = ed25519.pubkey(secret)
    print(f"key written {out} (mode 600, NEVER commit)")
    print(f"pubkey  {pk.hex()}")
    print(f"address {hashlib.sha256(pk).hexdigest()[:16]}")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(prog="scholar.py", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("show"); s.add_argument("--work", required=True)
    s.add_argument("--layer"); s.add_argument("--target")
    s.add_argument("--version")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("save"); s.add_argument("--work", required=True)
    s.add_argument("--layer", required=True); s.add_argument("--target", required=True)
    s.add_argument("--author", required=True); s.add_argument("--parent", default=None)
    s.add_argument("--author-kind", choices=["human", "agent"], default="human")
    s.add_argument("--body"); s.add_argument("--file"); s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_save)

    s = sub.add_parser("fork"); s.add_argument("--work", required=True)
    s.add_argument("--layer", required=True); s.add_argument("--target", required=True)
    s.add_argument("--from", dest="from_", required=True)
    s.add_argument("--author", required=True)
    s.add_argument("--author-kind", choices=["human", "agent"], default="human")
    s.add_argument("--body"); s.add_argument("--file"); s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_fork)

    s = sub.add_parser("import", help="import a Scholar browser submission")
    s.add_argument("--file", required=True)
    s.set_defaults(fn=cmd_import)

    s = sub.add_parser("log"); s.add_argument("--work", required=True)
    s.add_argument("--layer"); s.add_argument("--target")
    s.set_defaults(fn=cmd_log)

    s = sub.add_parser("signoff"); s.add_argument("--work", required=True)
    s.add_argument("--song", required=True); s.add_argument("--by", required=True)
    s.add_argument("--scope", default="full",
                   choices=["full", "t1-l0", "l2", "c1", "spot"])
    s.add_argument("--key", default=None); s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_signoff)

    s = sub.add_parser("promote"); s.add_argument("--work", required=True)
    s.add_argument("--object", required=True); s.add_argument("--version", required=True)
    s.add_argument("--basis", required=True)
    s.add_argument("--from-status", dest="from_status", default="NOT_REVIEWED")
    s.add_argument("--to", default="REVIEWED")
    s.add_argument("--reason", default="")
    s.set_defaults(fn=cmd_promote)

    s = sub.add_parser('approve-version', help='record self-attested author approval of an exact version')
    s.add_argument('--work',required=True);s.add_argument('--version',required=True);s.add_argument('--by',required=True)
    s.add_argument('--account-id',required=True);s.add_argument('--signoff-id',required=True)
    s.add_argument('--snapshot-sha256',required=True)
    s.add_argument('--rights',required=True,choices=['all-rights-reserved','cc-by-4.0','cc0'])
    s.set_defaults(fn=cmd_approve_version)

    s = sub.add_parser("verify"); s.add_argument("--work", required=True)
    s.set_defaults(fn=lambda a: verify(a.work))

    s = sub.add_parser("keygen"); s.add_argument("--out", default=str(DEFAULT_KEY))
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_keygen)

    a = ap.parse_args()
    if a.cmd in ("show",) and not (a.version or (a.layer and a.target)):
        die("show needs --layer + --target (or --version)")
    return a.fn(a)

if __name__ == "__main__":
    sys.exit(main())
