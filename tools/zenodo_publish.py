#!/usr/bin/env python3
"""zenodo_publish.py — archive a signed Scholar essay on Zenodo. Stdlib only.

Dry-run by default (builds the bundle, prints the deposition, sends
nothing). Publishing needs a token + explicit confirmation; without both,
nothing touches the network.

  zenodo_publish.py bundle --work W --essay ID [--out DIR]
  zenodo_publish.py publish --work W --essay ID [--sandbox] --confirm-live
      [--creator NAME] [--affiliation AFF] [--orcid ID] [--pub-type preprint]

Token: $ZENODO_TOKEN or /root/.zenodo-token (0600). Sandbox default URL is
the live Zenodo API; --sandbox targets sandbox.zenodo.org for tests.
Rights mapping: cc-by-4.0/cc0 -> open access; anything else -> closed
access (rights preserved, never upgraded). DOI record lands in
~/.scholar/zenodo-dois.json (local registry, never in a repo).
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TW = Path(os.environ.get("TRANSLATION_WORK_ROOT", "/root/translation-work"))
SVREAD = Path(os.environ.get("SVREAD_ROOT", "/root/svread"))
DOI_REGISTRY = Path.home() / ".scholar" / "zenodo-dois.json"
LIVE_API = "https://zenodo.org/api"
SANDBOX_API = "https://sandbox.zenodo.org/api"
OPEN_LICENSES = {"cc-by-4.0", "cc0"}


def find_essay(work: str, essay_id: str) -> dict:
    proj = json.loads((SVREAD / "data" / "scholar" / f"{work}.json").read_text(encoding="utf-8"))
    for e in proj.get("essays", []) or []:
        if e.get("essay_id") == essay_id:
            return e
    raise SystemExit(f"error: essay {essay_id} not found in {work} projection")


def git_head() -> str:
    try:
        return subprocess.run(["git", "-C", str(TW), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def build_bundle(work: str, essay: dict, outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    text = essay.get("text", "")
    md = f"# {essay.get('title', '')}\n\n_by {essay.get('author', '')}_\n\n{text}\n"
    (outdir / "essay.md").write_text(md, encoding="utf-8")
    (outdir / "essay.json").write_text(
        json.dumps(essay, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    provenance = {
        "format": "scholar-zenodo-bundle/1",
        "work": work, "essay_id": essay["essay_id"],
        "signoff": essay.get("signoff", {}).get("id", ""),
        "rights": essay.get("rights", ""),
        "identity_state": essay.get("identity_state", ""),
        "translation_work_commit": git_head(),
        "reader_url": f"https://svread.pages.dev/data/scholar/{work}.json",
        "bundled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    (outdir / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    files = {}
    for name in ("essay.md", "essay.json", "provenance.json"):
        p = outdir / name
        files[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return {"dir": str(outdir), "files": files, "provenance": provenance}


def deposition_metadata(work: str, essay: dict, args) -> dict:
    rights = essay.get("rights", "")
    open_access = rights in OPEN_LICENSES
    description = (essay.get("text", "")[:1200] +
                   f"\n\nSigned Scholar essay ({essay.get('identity_state', '')}) by "
                   f"{essay.get('author', '')}. Canonical record: translation-work "
                   f"commit {git_head()}; reader projection {work}. "
                   f"AI assistance: {essay.get('model') or 'none (human-authored)'}.")
    creators = [{"name": args.creator or essay.get("author", "Svatantrya Editorial")}]
    if args.affiliation:
        creators[0]["affiliation"] = args.affiliation
    if args.orcid:
        creators[0]["orcid"] = args.orcid
    return {"metadata": {
        "title": essay.get("title", f"Scholar essay {essay['essay_id'][:12]}"),
        "upload_type": "publication",
        "publication_type": args.pub_type,
        "description": description,
        "creators": creators,
        "license": rights if open_access else None,
        "access_right": "open" if open_access else "closed",
        "keywords": ["sanskrit", "trika-shaivism", "pratyabhijna",
                     "indian-philosophy", "translation-work"],
        "language": "eng",
        "version": "1.0.0",
        "related_identifiers": [
            {"identifier": f"https://svread.pages.dev/data/scholar/{work}.json",
             "relation": "isSupplementTo"},
            {"identifier": "https://github.com/prx0r/translation-work",
             "relation": "isDerivedFrom"}],
        "notes": ("Peer-reviewed through the Scholar workspace; signed off by the author. "
                  "Machine-readable signed record and provenance bundled as files.")}}


def api_request(base: str, token: str, method: str, path: str, payload=None, raw_path=None):
    url = base + (raw_path if raw_path is not None else path)
    body = None
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "svread-scholar-mcp/0.1"}
    if payload is not None:
        body = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode() or "{}")
        except ValueError:
            detail = {}
        raise SystemExit(f"error: Zenodo {e.code} {path}: {json.dumps(detail)[:300]}")


def token():
    if os.environ.get("ZENODO_TOKEN"):
        return os.environ["ZENODO_TOKEN"]
    p = Path("/root/.zenodo-token")
    if p.is_file():
        if p.stat().st_mode & 0o077:
            raise SystemExit("error: /root/.zenodo-token must be mode 600")
        return p.read_text(encoding="utf-8").strip()
    return ""


def cmd_bundle(args) -> int:
    essay = find_essay(args.work, args.essay)
    outdir = Path(args.out or (Path.home() / ".scholar" / "bundles" /
                               f"{args.work}-{essay['essay_id'][7:15]}"))
    bundle = build_bundle(args.work, essay, outdir)
    meta = deposition_metadata(args.work, essay, args)
    print(json.dumps({"bundle": bundle, "deposition_metadata": meta,
                      "mode": "dry-run (nothing sent)",
                      "publish_requires": "token + --confirm-live"},
                     ensure_ascii=False, indent=1))
    return 0


def cmd_publish(args) -> int:
    if not args.confirm_live:
        raise SystemExit("error: refusing to publish without --confirm-live")
    tok = token()
    if not tok:
        raise SystemExit("error: no token (ZENODO_TOKEN or /root/.zenodo-token)")
    essay = find_essay(args.work, args.essay)
    base = SANDBOX_API if args.sandbox else LIVE_API
    outdir = Path(args.out or (Path.home() / ".scholar" / "bundles" /
                               f"{args.work}-{essay['essay_id'][7:15]}"))
    bundle = build_bundle(args.work, essay, outdir)
    meta = deposition_metadata(args.work, essay, args)
    _, dep = api_request(base, tok, "POST", "/deposit/depositions", {})
    dep_id = dep["id"]
    bucket = dep["links"]["bucket"]
    for name in ("essay.md", "essay.json", "provenance.json"):
        data = (outdir / name).read_bytes()
        req = urllib.request.Request(
            f"{bucket}/{name}", data=data, method="PUT",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/octet-stream",
                     "User-Agent": "svread-scholar-mcp/0.1"})
        try:
            urllib.request.urlopen(req, timeout=300).read()
        except urllib.error.HTTPError as e:
            raise SystemExit(f"error: Zenodo upload {name}: HTTP {e.code}")
    _, dep2 = api_request(base, tok, "PUT", f"/deposit/depositions/{dep_id}", meta)
    _, pub = api_request(base, tok, "POST", f"/deposit/depositions/{dep_id}/actions/publish", {})
    record = {"essay_id": essay["essay_id"], "work": args.work,
              "doi": pub.get("doi", ""), "conceptdoi": pub.get("conceptdoi", ""),
              "deposition_id": dep_id, "sandbox": bool(args.sandbox),
              "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    reg = {}
    if DOI_REGISTRY.is_file():
        try:
            reg = json.loads(DOI_REGISTRY.read_text(encoding="utf-8"))
        except ValueError:
            reg = {}
    reg[essay["essay_id"]] = record
    DOI_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    DOI_REGISTRY.write_text(json.dumps(reg, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(record, indent=1))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="zenodo_publish.py")
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("bundle")
    b.add_argument("--work", required=True)
    b.add_argument("--essay", required=True)
    b.add_argument("--out", default=None)
    b.add_argument("--pub-type", default="preprint")
    b.add_argument("--creator", default=None)
    b.add_argument("--affiliation", default=None)
    b.add_argument("--orcid", default=None)
    q = sub.add_parser("publish")
    q.add_argument("--work", required=True)
    q.add_argument("--essay", required=True)
    q.add_argument("--out", default=None)
    q.add_argument("--sandbox", action="store_true")
    q.add_argument("--confirm-live", action="store_true")
    q.add_argument("--creator", default=None)
    q.add_argument("--affiliation", default=None)
    q.add_argument("--orcid", default=None)
    q.add_argument("--pub-type", default="preprint")
    args = p.parse_args(argv)
    if args.command == "bundle":
        return cmd_bundle(args)
    return cmd_publish(args)


if __name__ == "__main__":
    raise SystemExit(main())
