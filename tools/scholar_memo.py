#!/usr/bin/env python3
"""scholar_memo.py — proactive research memos. Deterministic, no model.

Watches a scholar's drafts; for each new revision compiles objections,
related passages, crossover leads, variant briefs and suggested works —
every line a pointer to something already on disk, labeled by tier.

  scholar_memo.py memo --api URL --cookie C [--work W ...] [--doc ID]
                       [--all] [--post] [--out DIR] [--suggest-works]

Default run prints memos and advances state (delivered once). --post also
saves one private labelled note per memo. --doc forces a single document.
Nothing is shared, granted or published — that stays an explicit human act.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TW = Path(os.environ.get("TRANSLATION_WORK_ROOT", "/root/translation-work"))
SVREAD = Path(os.environ.get("SVREAD_ROOT", "/root/svread"))
TANTRAESSAYS = Path(os.environ.get("TANTRAESSAYS_ROOT", "/root/tantraessays"))
RESEARCH_LIB = Path(os.environ.get("RESEARCH_LIBRARY_ROOT", "/root/damn/research-library"))
LEVIN = Path(os.environ.get("LEVIN_ROOT", "/root/gcomedy/library/levin"))
IPVV = Path(os.environ.get("IPVV_ROOT", "/root/ipvv"))
DEFAULT_STATE = Path.home() / ".scholar" / "memo-state.json"
AGENT_SOURCE = "scholar-memo/1"
TERM_RE = re.compile(r"^term:\s*(.+?)\s*$")
STOPWORDS = set("the a an of to in on and or for with what how why is are be as at by from that this essay translation what which their about".split())


def api(api_base, cookie, method, path, payload=None):
    req = urllib.request.Request(
        api_base.rstrip() + path, method=method,
        headers={"Cookie": cookie, "Content-Type": "application/json",
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


def unwrap_list(payload, key):
    if isinstance(payload, dict):
        payload = payload.get(key, payload)
    return payload if isinstance(payload, list) else []


def scan_works(explicit):
    if explicit:
        return explicit
    idx = SVREAD / "data" / "scholar"
    if not idx.is_dir():
        return []
    return sorted(p.stem for p in idx.glob("*.json") if p.stem != "index")


def glossary_for(api_base, cookie, works):
    glossary = {}
    for work in works:
        _, payload = api(api_base, cookie, "GET",
                         "/api/scholar/decisions?work=" + urllib.parse.quote(work))
        for row in unwrap_list(payload, "decisions"):
            if not isinstance(row, dict):
                continue
            m = TERM_RE.match(str(row.get("subject", "")))
            if not m or not str(row.get("after_text", "") or "").strip():
                continue
            term = m.group(1)
            if term in glossary:
                continue  # newest first; latest wins
            glossary[term] = {"after": str(row.get("after_text")).strip(),
                              "reason": str(row.get("reason", "") or ""),
                              "decision_id": row.get("id", "")}
    return glossary


def song_of(target):
    return re.sub(r"-v\d+$", "", target or "")


def gate_objections(work, target):
    try:
        gates = json.loads((TW / work / "GATE.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    entry = gates.get(song_of(target), {})
    if entry.get("deterministic_gate") != "BLOCKED":
        return []
    blocking = entry.get("blocking", [])
    return [f"gate BLOCKED: {b}" for b in blocking[:3]] if blocking else ["gate BLOCKED (no listed checks)"]


def argmap_open(work, target):
    try:
        text = (TW / work / "ARGMAP.md").read_text(encoding="utf-8")
    except OSError:
        return []
    if song_of(target) not in text:
        return []
    lines = [l.strip() for l in text.splitlines()
             if "nresolved" in l.lower()
             and not re.search(r"unresolved:\s*none\.?\s*$", l, re.I)]
    return [f"argmap: {l[:200]}" for l in lines[:3]]


def pushing_open(work):
    try:
        cat = json.loads((SVREAD / "data" / "pushing-catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for r in cat.get("records", []):
        if r.get("work") == work:
            out.append(f"open enquiry: {r.get('question', '?')} ({r.get('file', '?')})")
            if len(out) >= 3:
                break
    return out


def variant_mentions(work, target):
    try:
        text = (IPVV / "site" / "data" / "variants" / f"{work}.json").read_text(encoding="utf-8")
    except OSError:
        return []
    n = text.count(target)
    return [f"{n} variant record(s) mention this target"] if n else []


def t1_hits(terms, skip_work=None, skip_target=None, cap=8):
    """Glossary terms found in other passages' T1 files. Your words, elsewhere."""
    hits = []
    if not terms or not TW.is_dir():
        return hits
    for path in sorted(TW.glob("*/T1-*.md")):
        if len(hits) >= cap:
            break
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        work = path.parent.name
        target = path.stem[3:]
        if "." in target:
            continue  # roundtrip artifacts, not verse locators
        if work == skip_work and target == skip_target:
            continue
        found = [t for t in terms if re.search(r"\b" + re.escape(t) + r"\b", text)]
        if found:
            hits.append(f"{work}:{target} (matches: {', '.join(found[:3])})")
    return hits


def crossover_leads(keywords, cap=5):
    """House-archive leads: file refs only, never claims. Unverified by definition."""
    leads = []

    def add(ref, why):
        if len(leads) < cap and all(r[0] != ref for r in leads):
            leads.append((ref, why))

    if TANTRAESSAYS.is_dir():
        try:
            meta = json.loads((TANTRAESSAYS / "metadata.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            meta = {}
        for lec in meta.get("lectures", []) if isinstance(meta, dict) else []:
            hay = " ".join(lec.get("topics", []) + [lec.get("summary", "")]).lower()
            hit = [k for k in keywords if k.lower() in hay]
            if hit:
                add(f"tantraessays:{lec.get('file', lec.get('id', '?'))}",
                    f"lecture topics touch {', '.join(hit[:3])}")
    if RESEARCH_LIB.is_dir():
        for path in sorted(RESEARCH_LIB.rglob("*.md")):
            if len(leads) >= cap:
                break
            name = path.stem.lower().replace("_", " ").replace("-", " ")
            hit = [k for k in keywords if k.lower() in name]
            if hit:
                add(f"research-library:{path.relative_to(RESEARCH_LIB)}",
                    f"filename touches {', '.join(hit[:2])}")
    if LEVIN.is_dir():
        for path in sorted(LEVIN.glob("*.pdf")):
            if len(leads) >= cap:
                break
            name = path.stem.lower().replace("_", " ")
            if any(k.lower() in name for k in keywords):
                add(f"levin:{path.name}", "filename match")
    return [f"{ref} — {why} (lead, unverified)" for ref, why in leads]


def title_keywords(title, glossary_terms):
    words = [w.strip(".,;:!?\"'()").lower() for w in (title or "").split()]
    keys = [w for w in words if len(w) > 4 and w not in STOPWORDS]
    seen, out = set(), []
    for w in keys + [t.lower() for t in glossary_terms]:
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out[:8]


def suggested_works(glossary_terms, cap=5):
    """Tw works with no Scholar projection, ranked by glossary-term T1 hits."""
    scored = []
    for workdir in sorted(TW.iterdir()):
        if not workdir.is_dir() or not (workdir / "STATUS.json").is_file():
            continue
        if (SVREAD / "data" / "scholar" / f"{workdir.name}.json").is_file():
            continue
        hits = t1_hits(glossary_terms, cap=3) if glossary_terms else []
        _ = hits
        n = 0
        for path in sorted(workdir.glob("T1-*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if any(re.search(r"\b" + re.escape(t) + r"\b", text) for t in glossary_terms):
                n += 1
                if n >= 3:
                    break
        if n:
            scored.append((n, workdir.name))
    scored.sort(reverse=True)
    return [f"{w} ({n} T1 passages touch your glossary)" for n, w in scored[:cap]]


def memo_translation(doc, glossary):
    work, target = doc["work"], doc.get("target", "")
    lines = [f"# Copilot memo · translation {work}:{target} (rev {doc['revision']})", ""]
    objections = gate_objections(work, target) + argmap_open(work, target) + \
        pushing_open(work) + variant_mentions(work, target)
    lines.append("## Objections (the canon's own open questions)")
    lines += [f"- {o}" for o in objections] or ["- none found on disk"]
    lines.append("")
    related = t1_hits(list(glossary), skip_work=work, skip_target=target)
    lines.append("## Related passages (your words, elsewhere)")
    lines += [f"- {r}" for r in related] or ["- none found (record term: decisions to personalize)"]
    lines.append("")
    leads = crossover_leads(list(glossary))
    lines.append("## Crossover leads (house archives, unverified)")
    lines += [f"- {l}" for l in leads] or ["- none found"]
    lines.append("")
    return "\n".join(lines)


def memo_essay(doc, glossary, content):
    work, title = doc["work"], doc.get("title", "")
    text = content.get("text", "") if isinstance(content, dict) else ""
    cites = content.get("citations", []) if isinstance(content, dict) else []
    lines = [f"# Copilot memo · essay '{title or doc['id']}' ({work}, rev {doc['revision']})", ""]
    keys = title_keywords(title, list(glossary))
    leads = crossover_leads(keys)
    lines.append("## Variant briefs (skeletons — you write the prose)")
    if leads:
        lines.append(f"- crossover angle: take the top lead below and ask what it would say to your thesis")
    objections = pushing_open(work) + argmap_open(work, doc.get("target", ""))
    if objections:
        lines.append(f"- counter angle: {objections[0]}")
    lines.append(f"- tighten angle: {len(cites)}/10 pinned citations used; "
                 + ("room to pin more load-bearing claims" if len(cites) < 10 else "at the citation cap — prune or split"))
    lines.append("")
    lines.append("## Crossover leads (house archives, unverified)")
    lines += [f"- {l}" for l in leads] or ["- none found"]
    lines.append("")
    lines.append("## Note")
    lines.append(f"- draft is {len(text)} chars; citations point at "
                 + (", ".join(c.get("target", "?") for c in cites[:5]) if cites else "nothing pinned yet"))
    lines.append("")
    return "\n".join(lines)


def load_state(path):
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def cmd_memo(args) -> int:
    works = scan_works(args.work)
    glossary = glossary_for(args.api, args.cookie, works)
    state = {} if args.no_state else load_state(args.state or DEFAULT_STATE)
    memos = []
    ordered_docs = []
    for work in works:
        _, payload = api(args.api, args.cookie, "GET",
                         "/api/scholar/documents?work=" + urllib.parse.quote(work))
        for d in unwrap_list(payload, "documents"):
            if not isinstance(d, dict) or d.get("kind") not in ("translation", "essay"):
                continue
            ordered_docs.append(d)
    if args.doc:
        ordered_docs = [d for d in ordered_docs if d.get("id") == args.doc]
        if not ordered_docs:
            raise SystemExit(f"error: no such draft: {args.doc}")
    for doc in ordered_docs:
        doc_id = doc["id"]
        if not args.all and not args.doc and state.get(doc_id, 0) >= int(doc.get("revision", 0)):
            continue
        content = {}
        try:
            content = json.loads(doc.get("content_json", "") or "{}")
        except ValueError:
            pass
        if doc["kind"] == "translation":
            text = memo_translation(doc, glossary)
        else:
            text = memo_essay(doc, glossary, content)
        memos.append((doc, text))
        state[doc_id] = int(doc.get("revision", 0))
    if args.suggest_works:
        sug = suggested_works(list(glossary))
        block = "# Suggested works (no projection yet — translate next, in your voice)\n\n" + \
            ("\n".join(f"- {s}" for s in sug) if sug else "- none found (record term: decisions first)") + "\n"
        print(block)
    if not memos:
        print("nothing new: all drafts at their memoed revisions")
        if not args.no_state:
            Path(args.state or DEFAULT_STATE).parent.mkdir(parents=True, exist_ok=True)
            Path(args.state or DEFAULT_STATE).write_text(json.dumps(state, indent=1, sort_keys=True))
        return 0
    for doc, text in memos:
        print(text)
        print("---")
        if args.out:
            outdir = Path(args.out)
            outdir.mkdir(parents=True, exist_ok=True)
            slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", doc["id"]).strip("-")
            (outdir / f"memo-{slug}-r{doc['revision']}.md").write_text(text + "\n", encoding="utf-8")
        if args.post:
            note_id = "memo-" + re.sub(r"[^A-Za-z0-9_.:-]+", "-", doc["id"]).strip("-") + f"-r{doc['revision']}"
            _, saved = api(args.api, args.cookie, "PUT", f"/api/scholar/documents/{note_id}", {
                "expected_revision": 0, "kind": "note", "work": doc["work"],
                "target": doc.get("target", ""), "layer": doc.get("layer", ""),
                "title": f"Copilot memo · {doc['id']} r{doc['revision']}",
                "content": {"text": text, "base_sha256": "", "parent": None,
                            "assisted": False, "agent_source": AGENT_SOURCE}})
            print(f"posted private note {saved['document']['id']}")
    if not args.no_state:
        spath = Path(args.state or DEFAULT_STATE)
        spath.parent.mkdir(parents=True, exist_ok=True)
        spath.write_text(json.dumps(state, indent=1, sort_keys=True))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="scholar_memo.py")
    p.add_argument("--api", required=True)
    p.add_argument("--cookie", required=True)
    p.add_argument("--work", action="append", default=None)
    p.add_argument("--doc", default=None)
    p.add_argument("--all", action="store_true")
    p.add_argument("--post", action="store_true")
    p.add_argument("--out", default=None)
    p.add_argument("--suggest-works", action="store_true")
    p.add_argument("--state", default=None)
    p.add_argument("--no-state", action="store_true")
    args = p.parse_args(argv)
    return cmd_memo(args)


if __name__ == "__main__":
    raise SystemExit(main())
