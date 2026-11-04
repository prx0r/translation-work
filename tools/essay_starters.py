#!/usr/bin/env python3
"""essay_starters.py — turn the essay estate into organized starters. Stdlib, read-only.

Archives are never modified. Three passes, each writing only to --out:

  essay_starters.py index --out DIR       walk every archive, dedupe by bytes,
                                          INDEX.json + INDEX.md
  essay_starters.py glossary --out DIR    mine term (gloss) candidates, ranked,
                                          proposed-status, with file:line refs
  essay_starters.py anchor --out DIR [--index F] [--glossary F]
                                          resolve locator mentions against
                                          translation-work chunk ledgers,
                                          anchor glossary terms to T1 chunks,
                                          coverage per starter

A starter = {thesis, crux, terms, chunks, source, grade}. Cruxes feed the
memo compiler and pushing; terms feed the glossary (owner approves);
chunks come from the translation-work ledgers, never invented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

DIACRITICS = set("āīūṛḷṃṅñṭḍṇśṣḥĀĪŪṚḸṂṄÑṬḌṆŚṢḤ")
SKIP_MD = ("_", "README", "TEMPLATE", "TEMPLATE-", "INDEX", "FORMULA",
           "PROCESS_NOTES", "HANDOVER", "AGENTS", "CONTRIBUTING",
           "LECTURE_INDEX", "RENDER_CHECKLIST")
CLIP_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]*-\d+)")
GLOSS_RE = re.compile(
    r"\b([A-Za-z\u0101\u012b\u016b\u1e5b\u1e37\u1e43\u1e45\u1e47\u1e6d\u1e0d\u1e47\u015b\u1e63\u1e25"
    r"\u0100\u012a\u016a\u1e5a\u1e36\u1e42\u1e44\u1e46\u1e6c\u1e0c\u1e46\u015a\u1e62\u1e24\-]{3,40})"
    r"\s+\(([^()\n]{3,80})\)")
BANNED_GLOSS = ("see ", "see.", "cf ", "cf.", "e.g", "i.e", "etc", "viz",
                "vol ", "pp ", "ch ", "fig ", "http")
LOCATOR_RE = re.compile(r"\b([a-z]{2,}[a-z0-9]*-\d+(?:-v\d+)?)\b")


def roots():
    return {
        "tantraessays": Path(os.environ.get("TANTRAESSAYS_ROOT", "/root/tantraessays/essays")),
        "research_libs": [Path(p) for p in os.environ.get(
            "RESEARCH_LIBS",
            "/root/damn/research-library:/root/projects/research-library").split(":")],
        "expansion": Path(os.environ.get("EXPANSION_ROOT",
                                         "/root/projects/tantraloka/expansion-packs/unpacked")),
        "workshop": Path(os.environ.get("WORKSHOP_ROOT",
                                        "/root/thomas/oldessays/essaygen/workshop")),
        "basecamp": Path(os.environ.get("BASECAMP_ROOT", "/root/projects/basecamp/knowledge")),
    }


def tw_root():
    return Path(os.environ.get("TRANSLATION_WORK_ROOT", "/root/translation-work"))


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def md_record(path: Path, repo: str, kind: str) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    title = path.stem.replace("_", " ")
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    headings = [l[3:].strip() for l in text.splitlines()
                if l.startswith("## ")][:12]
    return {"id": f"{kind}:{sha_bytes(text.encode())[:12]}", "kind": kind,
            "repo": repo, "path": str(path),
            "title": title[:200], "crux": "",
            "words": len(text.split()), "headings": headings,
            "refs": sorted(set(CLIP_RE.findall(text))),
            "timestamps": text.count("-->"),
            "content_sha256": sha_bytes(text.encode())}


def iter_md(root: Path, repo: str, kind: str):
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*.md")):
        if path.name.startswith(SKIP_MD) or path.name.startswith("."):
            continue
        rec = md_record(path, repo, kind)
        if rec:
            yield rec


def cmd_index(args) -> int:
    r = roots()
    starters, seen = [], {}
    dupes = 0

    def add(rec):
        nonlocal dupes
        if rec["content_sha256"] in seen:
            dupes += 1
            return
        seen[rec["content_sha256"]] = rec["path"]
        starters.append(rec)

    for rec in iter_md(r["tantraessays"], "tantraessays", "essay-md"):
        add(rec)
    for lib in r["research_libs"]:
        for rec in iter_md(lib, "research-library", "essay-md"):
            add(rec)
    if r["expansion"].is_dir():
        for pack in sorted(r["expansion"].iterdir()):
            if not pack.is_dir():
                continue
            manifest = pack / (pack.name + "/manifest.json")
            cands = [manifest] if manifest.is_file() else []
            if not cands:
                for m in sorted(pack.rglob("manifest.json")):
                    cands.append(m)
                    break
            meta = {}
            if cands:
                try:
                    meta = json.loads(cands[0].read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    meta = {}
            for md in sorted(pack.rglob("*.md")):
                if md.name in ("README.md", "SOURCES.md") or md.name.startswith("_"):
                    continue
                rec = md_record(md, "expansion-packs", "expansion-essay")
                if not rec:
                    continue
                rec["crux"] = meta.get("title", "")
                rec["topics"] = meta.get("key_concepts", [])
                rec["pack"] = pack.name
                add(rec)
    if r["workshop"].is_dir():
        for path in sorted(r["workshop"].glob("*.json")):
            try:
                d = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(d, dict) or "body" not in d:
                continue
            kinds, words = {}, 0
            for b in d["body"] if isinstance(d["body"], list) else []:
                if isinstance(b, dict) and isinstance(b.get("text"), str):
                    kinds[b.get("kind", "?")] = kinds.get(b.get("kind", "?"), 0) + 1
                    words += len(b["text"].split())
            raw = json.dumps(d, ensure_ascii=False, sort_keys=True)
            starters.append({
                "id": f"workshop-essay:{sha_bytes(raw.encode())[:12]}",
                "kind": "workshop-essay", "repo": "oldessays",
                "path": str(path), "title": str(d.get("title", path.stem))[:200],
                "crux": "", "words": words,
                "topics": d.get("concepts", []), "body_kinds": kinds,
                "refs": [], "timestamps": 0,
                "content_sha256": sha_bytes(raw.encode())})
    bc = r["basecamp"]
    for eo in sorted((bc / "essay-objects").glob("*/eo.json")) if (bc / "essay-objects").is_dir() else []:
        try:
            d = json.loads(eo.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        q = d.get("question", {}) if isinstance(d.get("question"), dict) else {}
        raw = json.dumps(d, ensure_ascii=False, sort_keys=True)
        starters.append({
            "id": f"essay-object:{d.get('eo_id', sha_bytes(raw.encode())[:12])}",
            "kind": "essay-object", "repo": "basecamp", "path": str(eo),
            "title": str(d.get("title", eo.parent.name))[:200],
            "crux": str(q.get("tension_point", ""))[:500],
            "words": len(raw.split()), "topics": [],
            "refs": [], "timestamps": 0, "content_sha256": sha_bytes(raw.encode())})
    for cf in sorted((bc / "contentions").glob("*.json")) if (bc / "contentions").is_dir() else []:
        try:
            d = json.loads(cf.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        raw = json.dumps(d, ensure_ascii=False, sort_keys=True)
        starters.append({
            "id": f"contention:{sha_bytes(raw.encode())[:12]}",
            "kind": "contention", "repo": "basecamp", "path": str(cf),
            "title": str(d.get("title", d.get("question_id", cf.stem)))[:200],
            "crux": str(d.get("central_reading", ""))[:500],
            "words": len(raw.split()), "topics": [str(d.get("tradition", ""))],
            "claims": len(d.get("claims", []) or []),
            "refs": [], "timestamps": 0, "content_sha256": sha_bytes(raw.encode())})
    for sd in sorted((bc / "essay-seeds").glob("*.json")) if (bc / "essay-seeds").is_dir() else []:
        try:
            d = json.loads(sd.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        raw = json.dumps(d, ensure_ascii=False, sort_keys=True)
        starters.append({
            "id": f"essay-seed:{d.get('seed_id', sha_bytes(raw.encode())[:12])}",
            "kind": "essay-seed", "repo": "basecamp", "path": str(sd),
            "title": str(d.get("title", sd.stem))[:200],
            "crux": str(d.get("sharp_question", ""))[:500],
            "words": len(raw.split()), "topics": [],
            "refs": [], "timestamps": 0, "content_sha256": sha_bytes(raw.encode())})

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "INDEX.json").write_text(
        json.dumps(starters, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = ["# Essay starters index", "",
             f"{len(starters)} starters, {dupes} byte-duplicates collapsed.",
             "", "| kind | title | words | refs | path |",
             "|---|---|---|---|---|"]
    for s in sorted(starters, key=lambda x: (x["kind"], x["title"])):
        lines.append(f"| {s['kind']} | {s['title'][:70]} | {s['words']} | "
                     f"{len(s.get('refs', []))} | `{s['path']}` |")
    (outdir / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    kinds = {}
    for s in starters:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    print(f"index: {len(starters)} starters ({dupes} duplicates collapsed): " +
          ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    return 0


def has_diacritic(s: str) -> bool:
    return any(c in DIACRITICS for c in s)


def gloss_ok(term: str, gloss: str) -> bool:
    if len(term) < 3 or term.lower() in ("the", "and", "for", "with", "from"):
        return False
    if term.isupper() or "-" in term:
        return False  # apparatus labels (BRANCHES) and ref keys (in-the-sūtra)
    if any(c.isdigit() for c in term + gloss):
        return False  # syn tables, timestamps, verse numbers
    gl = gloss.strip().lower()
    if gl.startswith(BANNED_GLOSS):
        return False
    if not has_diacritic(term):
        if not (term[0].isupper() and (" " in gloss or len(gloss) > 12)):
            return False
    return True


def cmd_glossary(args) -> int:
    r = roots()
    hits = {}
    files_scanned = 0
    sources = []
    if r["tantraessays"].is_dir():
        sources.append(r["tantraessays"])
    for lib in r["research_libs"]:
        if lib.is_dir():
            sources.append(lib)
    if r["expansion"].is_dir():
        sources.append(r["expansion"])
    for root in sources:
        for path in sorted(root.rglob("*.md")):
            if path.name.startswith(SKIP_MD) or path.name.startswith("."):
                continue
            if path.name in ("README.md", "SOURCES.md"):
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, ValueError):
                continue
            files_scanned += 1
            for i, line in enumerate(lines, 1):
                for m in GLOSS_RE.finditer(line):
                    term, gloss = m.group(1).strip("-"), m.group(2).strip()
                    if not gloss_ok(term, gloss):
                        continue
                    key = (term, gloss)
                    h = hits.setdefault(key, {"files": set(), "count": 0, "refs": []})
                    h["files"].add(str(path))
                    h["count"] += 1
                    if len(h["refs"]) < 3:
                        h["refs"].append(f"{path}:{i}")
    ranked = sorted(hits.items(), key=lambda kv: (len(kv[1]["files"]), kv[1]["count"]),
                    reverse=True)[:args.top]
    proposals = [{"term": t, "rendering": g, "files": len(h["files"]),
                  "occurrences": h["count"], "refs": h["refs"],
                  "status": "proposed"} for (t, g), h in ranked]
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "glossary-proposals.json").write_text(
        json.dumps(proposals, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"glossary: {len(proposals)} proposals from {files_scanned} files "
          f"(top: {', '.join(p['term'] for p in proposals[:5])})")
    return 0


def load_locator_map():
    locmap = {}
    for p in sorted(tw_root().glob("*/passages.jsonl")):
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("locator"):
                    locmap[row["locator"]] = p.parent.name
        except OSError:
            continue
    return locmap


def load_t1():
    corpus = []
    for p in sorted(tw_root().glob("*/T1-*.md")):
        stem = p.stem[3:]
        if "." in stem:
            continue
        try:
            corpus.append((p.parent.name, stem, p.read_text(encoding="utf-8")))
        except OSError:
            continue
    return corpus


def cmd_anchor(args) -> int:
    index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    glossary = json.loads(Path(args.glossary).read_text(encoding="utf-8"))
    terms = [(g["term"], g["rendering"]) for g in glossary
             if isinstance(g, dict) and g.get("term")]
    locmap = load_locator_map()
    corpus = load_t1()
    report = []
    for s in index:
        if s.get("kind") not in ("essay-md", "expansion-essay", "workshop-essay"):
            continue
        try:
            if s["kind"] == "workshop-essay":
                d = json.loads(Path(s["path"]).read_text(encoding="utf-8"))
                text = "\n".join(b.get("text", "") for b in d.get("body", [])
                                  if isinstance(b, dict))
            else:
                text = Path(s["path"]).read_text(encoding="utf-8")
        except (OSError, ValueError):
            continue
        mentioned = sorted(set(LOCATOR_RE.findall(text)))
        resolved = [m for m in mentioned if m in locmap]
        found_terms, anchored = [], {}
        for term, _render in terms[:150]:
            if re.search(r"\b" + re.escape(term) + r"\b", text):
                found_terms.append(term)
                hits = []
                for work, target, body in corpus:
                    if re.search(r"\b" + re.escape(term) + r"\b", body):
                        hits.append(f"{work}:{target}")
                        if len(hits) >= 3:
                            break
                if hits:
                    anchored[term] = hits
        denom = len(mentioned) + len(found_terms)
        coverage = round((len(resolved) + len(anchored)) / denom, 3) if denom else None
        report.append({"id": s["id"], "title": s["title"], "path": s["path"],
                       "locators_found": len(mentioned),
                       "locators_resolved": resolved,
                       "terms_found": len(found_terms),
                       "terms_anchored": anchored, "coverage": coverage})
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "anchor-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    scored = [x for x in report if x["coverage"] is not None]
    avg = round(sum(x["coverage"] for x in scored) / len(scored), 3) if scored else None
    print(f"anchor: {len(report)} starters assessed, mean coverage {avg} "
          f"({len(scored)} with anchorable items)")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="essay_starters.py")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("index")
    a.add_argument("--out", required=True)
    b = sub.add_parser("glossary")
    b.add_argument("--out", required=True)
    b.add_argument("--top", type=int, default=200)
    c = sub.add_parser("anchor")
    c.add_argument("--out", required=True)
    c.add_argument("--index", required=True)
    c.add_argument("--glossary", required=True)
    args = p.parse_args(argv)
    if args.command == "index":
        return cmd_index(args)
    if args.command == "glossary":
        return cmd_glossary(args)
    return cmd_anchor(args)


if __name__ == "__main__":
    raise SystemExit(main())
