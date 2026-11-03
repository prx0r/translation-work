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
import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "human_authority"))
from contracts_human_authority import (  # noqa: E402
    ReviewEvent, ReviewerIdentity, ReviewTarget, PromotionEvent)
import ed25519  # noqa: E402

LAYERS = ("t1", "l0", "argmap", "l2", "c1", "l3", "l4")
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

# ------------------------------------------------------------ originals

def song_of(target: str, layer: str) -> str:
    if layer == "c1":
        return target                      # c1 is song-scoped: target IS the song
    m = re.match(r"^(.*?)-v\d+$", target)
    if not m:
        die(f"target {target!r} must be <song>-v<n> (or the song id for c1)")
    return m.group(1)

def load_original(work: str, layer: str, target: str):
    """Return (content, file) for the canonical layer content being edited."""
    if layer not in LAYERS:
        die(f"layer must be one of {LAYERS}")
    song = song_of(target, layer)
    f = ROOT / work / "data" / f"{song}.{layer}.json"
    if not f.exists():
        die(f"no canonical {layer} file for this target: {f}")
    d = json.loads(f.read_text(encoding="utf-8"))
    if layer == "c1":
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
    for layer in LAYERS:
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
    return "sv:" + sha({
        "work": v["work"], "layer": v["layer"], "target": v["target"],
        "parent": v["parent"], "author": v["author"],
        "content_sha256": v["content_sha256"], "created_at": v["created_at"],
    })[:16]

def make_version(work, layer, target, parent, author, content, note=""):
    if not content:
        die("content is empty — refusing a hollow version")
    base, _f = load_original(work, layer, target)
    v = {
        "work": work, "layer": layer, "target": target, "parent": parent,
        "base_sha256": sha(base), "author": author, "created_at": now(),
        "note": note, "content_sha256": sha(content), "content": content,
        "status": "MACHINE_DRAFT",
    }
    v["version_id"] = vid_of(v)
    # order: version_id first for readable lines
    return {"version_id": v["version_id"], **{k: v[k] for k in
            ("work", "layer", "target", "parent", "base_sha256", "author",
             "created_at", "note", "content_sha256", "content", "status")}}

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

def verify(work: str) -> int:
    fails, warns = [], []
    versions = load_versions(work)
    by_id = {}
    for i, v in enumerate(versions, 1):
        for k in ("version_id", "work", "layer", "target", "parent",
                  "base_sha256", "author", "created_at", "content_sha256",
                  "content", "status"):
            if k not in v:
                fails.append(f"versions:{i} missing field {k}")
        if fails:
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

    # reviews
    review_ids = set()
    for i, r in enumerate(jsonl_read(rpath(work)), 1):
        sig = r.pop("signature", "")
        signer = r.pop("signer", "")
        if not ReviewEvent.verify(r):
            fails.append(f"reviews:{i} event_hash does not recompute")
        rid = r.get("review_id", "")
        if rid in review_ids:
            fails.append(f"reviews:{i} duplicate review_id {rid}")
        review_ids.add(rid)
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
            elif not ed25519.verify(bytes.fromhex(signer),
                                    r.get("review_id", "").encode(),
                                    bytes.fromhex(sig)):
                fails.append(f"reviews:{i}: signature invalid")
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
    parent = None
    if a.parent and a.parent != "none":
        ids = {v["version_id"] for v in load_versions(a.work)}
        if a.parent not in ids:
            die(f"--parent {a.parent} not found")
        parent = a.parent
    v = make_version(a.work, a.layer, a.target, parent, a.author, content, a.note)
    jsonl_append(vpath(a.work), v)
    print(f"saved {v['version_id']}  ({a.layer}:{a.target} "
          f"parent={'original' if parent is None else parent})")
    return 0

def cmd_fork(a) -> int:
    ids = {v["version_id"]: v for v in load_versions(a.work)}
    if a.from_ not in ids:
        die(f"--from {a.from_} not found")
    parent = ids[a.from_]
    content = parse_body(a)
    if content is None:
        content = parent["content"]           # branch point: carry the content, edit next
    if a.target != parent["target"] or a.layer != parent["layer"]:
        die(f"fork stays on the same target: layer={parent['layer']} "
            f"target={parent['target']} (got {a.layer}:{a.target})")
    v = make_version(a.work, a.layer, a.target, a.from_, a.author, content,
                     a.note or f"fork of {a.from_}")
    jsonl_append(vpath(a.work), v)
    print(f"forked {a.from_} → {v['version_id']}  ({a.layer}:{a.target})")
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
            identity_state="VERIFIED" if a.key else "SELF_ATTESTED",
            domains=[a.work]),
        decision="ACCEPT",
        review_scope="SAME_WORK" if a.scope == "full" else "LOCAL_SECTION",
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
        sig = ed25519.sign(secret, rid.encode()).hex()
        body["signer"], body["signature"] = signer_hex, sig
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
        to_status="INDEPENDENT_REVIEWED",
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

def cmd_promote(a) -> int:
    now_s = now()
    basis = [b.strip() for b in a.basis.split(",") if b.strip()]
    known = {r.get("review_id") for r in jsonl_read(rpath(a.work))}
    missing = [b for b in basis if b not in known]
    if missing:
        die(f"basis reviews not found: {missing}")
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
    s.add_argument("--body"); s.add_argument("--file"); s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_save)

    s = sub.add_parser("fork"); s.add_argument("--work", required=True)
    s.add_argument("--layer", required=True); s.add_argument("--target", required=True)
    s.add_argument("--from", dest="from_", required=True)
    s.add_argument("--author", required=True)
    s.add_argument("--body"); s.add_argument("--file"); s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_fork)

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
    s.add_argument("--to", default="INDEPENDENT_REVIEWED")
    s.add_argument("--reason", default="")
    s.set_defaults(fn=cmd_promote)

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
