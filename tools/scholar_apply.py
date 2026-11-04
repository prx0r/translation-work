#!/usr/bin/env python3
"""scholar_apply.py — replay a scholar's own choices onto any text. Stdlib only.

Deterministic, no model, no training. The scholar translates once with
justification (workspace decisions, subject "term: X"); this tool replays
those renderings elsewhere and records every substitution as its own
decision row, so the "why" travels with the words.

  scholar_apply.py glossary --api URL --cookie C [--work W]
  scholar_apply.py apply --api URL --cookie C --base WORK:TARGET:LAYER

`glossary` prints the scholar's term entries (latest per term).
`apply` PUTs the canonical translation document id with CAS revision, then
POSTs one decision row per applied term. Exit 1 with stderr on refusal
(unknown base, revision conflict, unparseable layer) — never partial.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TERM_RE = re.compile(r"^term:\s*(.+?)\s*$")
AGENT_SOURCE = "scholar-apply/1"

# Projection bytes live next to this repo; the worker loads these same files.
SVREAD = Path(__file__).resolve().parent.parent.parent / "svread"


def api(api_base: str, cookie: str, method: str, path: str, payload=None):
    req = urllib.request.Request(
        api_base.rstrip("/") + path, method=method,
        headers={"Cookie": cookie, "Content-Type": "application/json",
                 # Identified UA: box egress is challenged (CF 1010) otherwise.
                 "User-Agent": "svread-scholar-mcp/0.1"})
    try:
        with urllib.request.urlopen(req,
                                    data=json.dumps(payload).encode() if payload is not None else None,
                                    timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as ex:
        try:
            detail = json.loads(ex.read().decode() or "{}")
        except ValueError:
            detail = {}
        raise SystemExit(f"error: API {ex.code} {path}: "
                         f"{detail.get('error', 'request failed')}")


def fetch_glossary(api_base: str, cookie: str, work: str | None = None) -> dict:
    path = "/api/scholar/decisions" + (f"?work={urllib.parse.quote(work)}" if work else "")
    _, payload = api(api_base, cookie, "GET", path)
    rows = payload.get("decisions", payload) if isinstance(payload, dict) else payload
    glossary = {}
    for row in rows if isinstance(rows, list) else []:
        m = TERM_RE.match(str(row.get("subject", "")))
        if not m:
            continue
        term = m.group(1)
        after = str(row.get("after_text", "") or "").strip()
        if not term or not after:
            continue  # malformed glossary rows are ignored, never applied
        if term in glossary:
            continue  # API returns newest first; latest entry wins
        glossary[term] = {"after": after,
                          "reason": str(row.get("reason", "") or ""),
                          "decision_id": row.get("id", ""),
                          "work": row.get("work", ""),
                          "target": row.get("target", "")}
    return glossary


def load_base(work: str, target: str, layer: str):
    proj_path = SVREAD / "data" / "scholar" / f"{work}.json"
    try:
        proj = json.loads(proj_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise SystemExit(f"error: no Scholar projection for work: {work}")
    originals = proj.get("originals", {}).get(layer, {})
    if target not in originals:
        raise SystemExit(f"error: no {layer} base for {work}:{target}")
    base_hash = (proj.get("original_hashes", {}).get(layer, {}) or {}).get(target, "")
    if not re.fullmatch(r"[0-9a-f]{64}", base_hash or ""):
        raise SystemExit(f"error: base hash missing for {work}:{target} ({layer})")
    return originals[target], base_hash


def substitute_prose(text: str, glossary: dict) -> tuple[str, list]:
    """Longest-first whole-word substitution. Returns (new_text, applied)."""
    applied = []
    for term in sorted(glossary, key=len, reverse=True):
        after = glossary[term]["after"]
        pattern = re.compile(r"\b" + re.escape(term) + r"\b")
        text, n = pattern.subn(after, text)
        if n:
            applied.append({"term": term, "after": after, "count": n,
                            **{k: glossary[term][k] for k in ("reason", "decision_id", "work", "target")}})
    return text, applied


def replay_l0(tokens, glossary: dict) -> tuple[list, list, list]:
    """Set each token's chosen_index to the scholar's recorded gloss.

    Matches glossary terms against token surfaces; options carrying other
    glosses are left alone and reported. Returns (tokens, applied, skipped).
    """
    if not isinstance(tokens, list):
        raise SystemExit("error: l0 base is not a token list")
    applied, skipped = [], []
    for tok in tokens:
        if not isinstance(tok, dict):
            continue
        surface = str(tok.get("surface", "") or "")
        options = tok.get("options") or []
        entry = glossary.get(surface)
        if not entry:
            continue
        hit = next((i for i, o in enumerate(options)
                    if isinstance(o, dict) and o.get("gloss") == entry["after"]), None)
        if hit is None:
            skipped.append({"term": surface, "wanted": entry["after"],
                            "reason": "no token option carries that gloss"})
            continue
        if tok.get("chosen_index") != hit:
            tok["chosen_index"] = hit
            applied.append({"term": surface, "after": entry["after"], "count": 1,
                            "reason": entry["reason"], "decision_id": entry["decision_id"],
                            "work": entry["work"], "target": entry["target"]})
    return tokens, applied, skipped


def cmd_glossary(args) -> int:
    glossary = fetch_glossary(args.api, args.cookie, args.work)
    print(json.dumps(glossary, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


def cmd_apply(args) -> int:
    try:
        work, target, layer = args.base.split(":")
    except ValueError:
        raise SystemExit("error: --base must be WORK:TARGET:LAYER")
    if layer not in ("l0", "l2", "l3", "l4"):
        raise SystemExit("error: apply supports l0/l2/l3/l4 text layers")
    glossary = fetch_glossary(args.api, args.cookie)
    if not glossary:
        raise SystemExit("error: no term: decisions found — record at least one glossary entry first")
    base_value, base_hash = load_base(work, target, layer)
    doc_id = f"translation:{layer}:{target}"
    _, payload = api(args.api, args.cookie, "GET",
                     f"/api/scholar/documents?work={urllib.parse.quote(work)}")
    docs = payload.get("documents", payload) if isinstance(payload, dict) else payload
    current = next((d for d in (docs if isinstance(docs, list) else [])
                    if d.get("id") == doc_id), None)
    revision = int(current.get("revision", 0)) if current else 0
    render_field = None
    if layer == "l0":
        new_tokens, applied, skipped = replay_l0(
            json.loads(json.dumps(base_value)), glossary)
        new_text = json.dumps(new_tokens, ensure_ascii=False)
    else:
        render_field = None
        if isinstance(base_value, str):
            work_text = base_value
        elif isinstance(base_value, dict):
            # Layer records carry one renderable string; replay touches only it.
            for key in ("plain_english", "text"):
                if isinstance(base_value.get(key), str):
                    render_field, work_text = key, base_value[key]
                    break
            else:
                raise SystemExit(f"error: {layer} base for {work}:{target} "
                                 f"has no renderable text field")
        else:
            raise SystemExit(f"error: {layer} base for {work}:{target} is not text")
        new_text, applied = substitute_prose(work_text, glossary)
        skipped = []
    if not applied:
        print(json.dumps({"draft_id": None, "applied": [], "skipped": skipped,
                          "note": "glossary matched nothing; draft untouched"}))
        return 0
    _, saved = api(args.api, args.cookie, "PUT", f"/api/scholar/documents/{doc_id}", {
        "expected_revision": revision, "kind": "translation", "work": work,
        "target": target, "layer": layer, "title": args.title or "",
        "content": {"text": new_text, "base_sha256": base_hash, "parent": None,
                    "assisted": False, "agent_source": AGENT_SOURCE}})
    new_revision = int(saved["document"]["revision"])
    decision_ids = []
    for a in applied:
        _, d = api(args.api, args.cookie, "POST", "/api/scholar/decisions", {
            "document_id": doc_id, "revision": new_revision,
            "subject": f"term: {a['term']}",
            "before": a["term"], "after": a["after"],
            "reason": (f"Replayed by {AGENT_SOURCE} from decision "
                       f"{a['decision_id'] or '(recorded)'}"
                       + (f" — grounds: {a['reason']}" if a.get("reason") else ""))[:4000]})
        decision_ids.append(d["id"])
    print(json.dumps({"draft_id": doc_id, "revision": new_revision,
                      "render_field": render_field if layer != "l0" else None,
                      "applied": applied, "skipped": skipped,
                      "decision_ids": decision_ids,
                      "agent_source": AGENT_SOURCE}, ensure_ascii=False, indent=1))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="scholar_apply.py")
    parser.add_argument("--api", required=True)
    parser.add_argument("--cookie", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    g = sub.add_parser("glossary")
    g.add_argument("--work", default=None)
    a = sub.add_parser("apply")
    a.add_argument("--base", required=True)
    a.add_argument("--title", default="")
    args = parser.parse_args(argv)
    if args.command == "glossary":
        return cmd_glossary(args)
    return cmd_apply(args)


if __name__ == "__main__":
    raise SystemExit(main())
