#!/usr/bin/env python3
"""bibliography — THE base layer for translation priority (final 2026-11-12 baseline).

Where the final bibliography lives (canonical paths, newest-first):

  openpatalaproject/data/corpus/
    muktabodha_burn_research.csv           499×19 flat catalog (has_translation, …)
    muktabodha_translation_editions.jsonl  294 keyed edition records
    muktabodha_bibliographic_links.csv     718 catalog↔URL relationships
    muktabodha_research_matrix.json        499 rows, research.translations[] (merged)
    translation-availability.json          compiled index (743 works; API surface)
    downloads/muktabodha_final_2026-11-12/ full release package (source of truth)

  openpatala/data/translation-availability.json   served copy (same bytes)

Priority rule (owner): untranslated first, shortest first within equal T;
machine-complete / in-progress sink. T comes from THIS bibliography first
(editions count / has_translation), then curated FAMOUS + local state.

Usage:
  from bibliography import load, lookup, paths, priority_rows
  python3 tools/bibliography.py paths
  python3 tools/bibliography.py get --catalog M00031
  python3 tools/bibliography.py search --title kularnava
  python3 tools/bibliography.py priority --limit 20
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# ── THE PATHS (edit here if the baseline moves) ──────────────────────────────
CORPUS = Path("/root/openpatalaproject/data/corpus")
PKG = CORPUS / "downloads/muktabodha_final_2026-11-12"
BURN = CORPUS / "muktabodha_burn_research.csv"
EDITIONS = CORPUS / "muktabodha_translation_editions.jsonl"
LINKS = CORPUS / "muktabodha_bibliographic_links.csv"
MATRIX = CORPUS / "muktabodha_research_matrix.json"
INDEX = CORPUS / "translation-availability.json"
SERVED = Path("/root/openpatala/data/translation-availability.json")
RANKED = Path("/root/translation-work/process/beam/ranked_burn.json")
AS_OF = "2026-11-12"


def paths() -> dict:
    """Where the final bibliography lives (for MCP / docs / humans)."""
    def _m(p: Path) -> dict:
        return {"path": str(p), "exists": p.exists(),
                "bytes": p.stat().st_size if p.exists() else 0}
    return {
        "as_of": AS_OF,
        "role": "base layer for translation priority",
        "burn_flat": _m(BURN),
        "editions": _m(EDITIONS),
        "links": _m(LINKS),
        "research_matrix": _m(MATRIX),
        "availability_index": _m(INDEX),
        "availability_served": _m(SERVED),
        "release_package": _m(PKG),
        "ranked_burn": _m(RANKED),
        "priority_rule": "untranslated first, shortest first within T; "
                         "machine-complete/in-progress sink; T from this bibliography first",
    }


def load() -> dict:
    """Load burn + editions + matrix into one dict keyed by catalog."""
    burn: dict[str, dict] = {}
    if BURN.exists():
        with BURN.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                burn[(r.get("catalog") or "").strip()] = r

    editions: dict[str, list[dict]] = {}
    if EDITIONS.exists():
        for line in EDITIONS.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            editions.setdefault((r.get("catalog") or "").strip(), []).append(r)

    matrix: dict[str, dict] = {}
    if MATRIX.exists():
        for r in json.loads(MATRIX.read_text(encoding="utf-8")):
            cat = (r.get("catalog") or "").strip()
            if cat and cat not in matrix:
                matrix[cat] = r

    index: dict[str, dict] = {}
    if INDEX.exists():
        index = json.loads(INDEX.read_text(encoding="utf-8")).get("works") or {}

    return {"burn": burn, "editions": editions, "matrix": matrix, "index": index}


def _norm(s: str) -> str:
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return "".join(ch for ch in s if ch.isalpha())


def lookup(catalog: str = "", title: str = "", data: dict | None = None) -> dict:
    """One work's bibliography record (flat + editions + matrix + availability)."""
    d = data or load()
    cat = (catalog or "").strip()
    if not cat and title:
        nt = _norm(title)
        for c, row in d["matrix"].items():
            if _norm(row.get("title") or "") == nt:
                cat = c
                break
        if not cat:
            for c, row in d["burn"].items():
                if _norm(row.get("title") or "") == nt:
                    cat = c
                    break
    if not cat:
        return {"error": "not found", "catalog": catalog, "title": title}

    burn = d["burn"].get(cat, {})
    eds = d.get("editions", {}).get(cat, [])
    mx = d["matrix"].get(cat, {})
    research = mx.get("research") or {}
    # availability: prefer openpatala_key slug, else catalog key
    wid = mx.get("openpatala_key") or cat
    avail = d["index"].get(wid) or d["index"].get(cat) or {}
    has_t = (burn.get("has_translation") or "").strip().upper() == "TRUE" \
        or bool(research.get("translations")) or bool(eds)
    return {
        "catalog": cat,
        "title": burn.get("title") or mx.get("title") or avail.get("title"),
        "author": burn.get("author") or mx.get("author") or avail.get("author"),
        "verses": burn.get("verses") or mx.get("verses"),
        "has_translation": has_t,
        "tw_status": burn.get("tw_status") or research.get("burn_tw_status"),
        "translations": research.get("translations") or [],
        "editions": eds,
        "edition_count": len(eds),
        "languages": sorted({(e.get("language") or "und") for e in eds})
                     or avail.get("languages") or [],
        "openpatala_key": mx.get("openpatala_key"),
        "availability": {
            "work": avail.get("work"),
            "coverage": avail.get("coverage"),
            "has_english": avail.get("has_english"),
            "missing": avail.get("missing"),
        } if avail else None,
        "evidence_notes": burn.get("evidence_notes") or research.get("burn_evidence_notes"),
        "info_url": burn.get("info_url") or (eds[0].get("info_url") if eds else ""),
        "baseline": f"muktabodha_final_{AS_OF}",
        "paths": {k: v["path"] for k, v in paths().items() if isinstance(v, dict) and "path" in v},
    }


def search(q: str, limit: int = 20, data: dict | None = None) -> list[dict]:
    """Substring match on catalog or title."""
    d = data or load()
    nq = _norm(q)
    out = []
    seen = set()
    for src in (d["matrix"], d["burn"]):
        for cat, row in src.items():
            if not cat or cat in seen:
                continue
            blob = _norm(f"{cat} {row.get('title') or ''} {row.get('author') or ''}")
            if nq and nq in blob:
                seen.add(cat)
                out.append(lookup(catalog=cat, data=d))
                if len(out) >= limit:
                    return out
    return out


def priority_rows(limit: int = 0, untranslated_only: bool = False,
                  data: dict | None = None) -> list[dict]:
    """Ranked burn list — bibliography-aware T, shortest-first within T.

    Prefers process/beam/ranked_burn.json when present and fresh; otherwise
    builds a lightweight rank from the bibliography + work_state.
    """
    d = data or load()
    # Prefer the full ranked file (prioritize_mukta output) if it exists
    if RANKED.exists():
        try:
            rows = json.loads(RANKED.read_text(encoding="utf-8"))
            if isinstance(rows, list) and rows:
                if untranslated_only:
                    rows = [r for r in rows if r.get("T") == 0]
                # already burn_rank ordered
                if limit:
                    rows = rows[:limit]
                for r in rows:
                    r.setdefault("baseline", f"muktabodha_final_{AS_OF}")
                    # attach live bibliography bits
                    cat = r.get("catalog") or ""
                    eds = d.get("editions", {}).get(cat, [])
                    r["edition_count"] = len(eds)
                    burn = d.get("burn", {}).get(cat, {})
                    r["has_translation"] = (burn.get("has_translation") or "").upper() == "TRUE" \
                        or bool(eds) or bool(r.get("T"))
                return rows
        except Exception:
            pass

    # Fallback: rank from bibliography alone
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from work_state import state_for_catalog
    except Exception:
        def state_for_catalog(c):  # type: ignore
            return {"state": "not_started"}

    out = []
    for cat, burn in d["burn"].items():
        if not cat:
            continue
        st = (state_for_catalog(cat) or {}).get("state", "not_started")
        eds = d.get("editions", {}).get(cat, [])
        if st == "machine-complete":
            T, why = 10 ** 9, "machine-complete by us: skip"
        elif st == "started":
            T, why = 10 ** 8, "in progress: finish first"
        elif eds or (burn.get("has_translation") or "").upper() == "TRUE":
            T = max(len(eds), 1)
            why = f"bibliography: {len(eds)} edition(s), has_translation"
        else:
            T, why = 0, "untranslated in final bibliography"
        verses = int(burn.get("verses") or 0) if str(burn.get("verses") or "").isdigit() else 0
        prose = verses == 0
        out.append({
            "catalog": cat, "title": burn.get("title") or "", "verses": verses,
            "T": T, "T_why": why, "tw": st, "prose": prose,
            "edition_count": len(eds),
            "has_translation": T > 0 and T < 10 ** 8,
            "baseline": f"muktabodha_final_{AS_OF}",
        })
    out.sort(key=lambda o: (o["T"] >= 10 ** 9, o["prose"], o["T"], o["verses"]))
    for i, o in enumerate(out, 1):
        o["burn_rank"] = i
    if untranslated_only:
        out = [o for o in out if o["T"] == 0]
    if limit:
        out = out[:limit]
    return out


def schema() -> dict:
    """All data structures + field docs so any agent can query without reading files."""
    return {
        "as_of": AS_OF,
        "role": "base layer for translation priority — query via shastra MCP",
        "files": {
            "burn_flat": {
                "path": str(BURN), "format": "csv", "rows": 499, "columns": [
                    {"name": "catalog", "type": "string", "desc": "Mnnnnn catalog id (may be blank for unkeyed)"},
                    {"name": "title", "type": "string"},
                    {"name": "author", "type": "string"},
                    {"name": "verses", "type": "int", "desc": "0 = prose (needs chunker)"},
                    {"name": "tier", "type": "string"},
                    {"name": "tw_status", "type": "string", "desc": "queued|started|machine-complete|…"},
                    {"name": "known_T", "type": "string"},
                    {"name": "T_why", "type": "string"},
                    {"name": "has_translation", "type": "bool", "desc": "TRUE = some translation evidence (NOT proven complete)"},
                    {"name": "translator", "type": "string"},
                    {"name": "year", "type": "string"},
                    {"name": "scope_full_partial_chapters", "type": "string"},
                    {"name": "access_tier", "type": "string", "desc": "BUY|PRINT|BORROW|DIRECT|FREE|…"},
                    {"name": "download_url", "type": "url"},
                    {"name": "publisher", "type": "string"},
                    {"name": "info_url", "type": "url"},
                    {"name": "evidence_notes", "type": "string"},
                    {"name": "researcher", "type": "string"},
                    {"name": "verified_at", "type": "date"},
                ],
            },
            "editions": {
                "path": str(EDITIONS), "format": "jsonl", "rows": 294, "record": {
                    "catalog": "Mnnnnn", "title": "str", "translator": "str",
                    "year": "str", "language": "en|hi|fr|de|…",
                    "scope": "full|partial|chapter text", "complete": "bool (derived)",
                    "publisher": "str", "access_tier": "BUY|PRINT|FREE|DIRECT|…",
                    "access_mode": "PRINT|ONLINE_PDF|…",
                    "download_url": "url (may be empty)", "info_url": "url",
                    "corroboration_url": "url", "evidence": "str",
                    "confidence": "high|medium|low",
                    "publication_status": "published|…",
                    "verification_status": "BIBLIOGRAPHICALLY_VERIFIED|…",
                    "source_type": "catalogue|book|scholarly_journal_primary|…",
                    "researcher": "str", "verified_at": "date",
                },
            },
            "links": {
                "path": str(LINKS), "format": "csv", "rows": 718, "columns": [
                    {"name": "catalog"}, {"name": "url"}, {"name": "domain"},
                    {"name": "source_roles", "desc": "CANONICAL_INFO_URL | EDITION_INFO_URL | …"},
                    {"name": "origin_files"}, {"name": "edition_related", "desc": "YES|NO"},
                    {"name": "unresolved_audit_related", "desc": "YES|NO"},
                    {"name": "evidence_notes"},
                ],
            },
            "research_matrix": {
                "path": str(MATRIX), "format": "json", "rows": 499,
                "record_fields": [
                    "catalog", "title", "author", "verses", "file",
                    "openpatala_key", "openpatala_coverage",
                    "tradition_guess", "traditions_authority", "research",
                ],
                "research_fields": [
                    "translations", "researcher", "verified_at", "rights",
                    "edition_print", "public_edition_url", "secondary_literature",
                    "dating_text", "provenance_ms", "ochs_db_hit",
                    "burn_has_translation", "burn_tw_status", "burn_evidence_notes",
                    "source_baseline",
                ],
                "research_translation_shape": "= editions record + _src (see editions), plus complete:bool",
            },
            "availability_index": {
                "path": str(INDEX), "format": "json", "count": 743,
                "record_fields": [
                    "work", "title", "author", "catalog_no", "traditions",
                    "has_english", "languages", "coverage", "missing",
                    "translations", "copyright_hint", "english_urls",
                    "factory", "live_checked", "live_note", "source",
                    "baseline", "tw_status",
                ],
                "translation_fields": [
                    "language", "translator", "coverage", "complete", "type",
                    "tier", "url", "found_live", "source", "year", "publisher",
                    "evidence", "verification_status",
                ],
                "coverage_values": ["full", "partial", "none"],
                "factory_fields": ["t1", "l2", "c1", "next_action"],
            },
            "served_copy": {"path": str(SERVED), "note": "same bytes as availability_index; openpatala API reads this"},
            "ranked_burn": {"path": str(RANKED), "format": "json", "rows": 492,
                            "record": ["burn_rank", "catalog", "title", "verses",
                                       "T", "T_why", "tw", "prose", "edition_count",
                                       "has_translation", "baseline"]},
            "release_package": {"path": str(PKG), "note": "full 2026-11-12 release (source of truth for staged files)"},
        },
        "priority_rule": paths()["priority_rule"],
        "mcp_tools": ["shastra.bibliography", "shastra.priority",
                      "shastra.editions", "shastra.links",
                      "shastra.availability", "shastra.schema", "shastra.stats"],
        "datatypes_pipeline": "/root/translation-work/DATATYPES.json (translation layers T1→C2)",
        "caveat": "has_translation/missing=false is bibliographic evidence, NOT proof of a complete rights-cleared translation. 286 unresolved ≠ untranslated.",
    }


def stats() -> dict:
    """Aggregate counts for quick orientation."""
    d = load()
    burn = d["burn"]
    eds = d["editions"]
    n_pos = sum(1 for b in burn.values()
                if (b.get("has_translation") or "").strip().upper() == "TRUE")
    n_ed = sum(len(v) for v in eds.values())
    langs: dict[str, int] = {}
    for cat, rows in eds.items():
        for e in rows:
            langs[e.get("language") or "und"] = langs.get(e.get("language") or "und", 0) + 1
    idx = d["index"]
    mworks = [(k, v) for k, v in idx.items()
              if (v.get("catalog_no") or "").startswith("M") or k.startswith("M")]
    cov: dict[str, int] = {}
    for _, v in mworks:
        cov[v.get("coverage") or "none"] = cov.get(v.get("coverage") or "none", 0) + 1
    # links
    n_links = 0
    domains: dict[str, int] = {}
    if LINKS.exists():
        with LINKS.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                n_links += 1
                domains[row.get("domain") or ""] = domains.get(row.get("domain") or "", 0) + 1
    ranked = []
    if RANKED.exists():
        try:
            ranked = json.loads(RANKED.read_text(encoding="utf-8"))
        except Exception:
            ranked = []
    return {
        "as_of": AS_OF,
        "catalog_rows": len(burn),
        "has_translation_TRUE": n_pos,
        "unresolved": len(burn) - n_pos,
        "keyed_editions": n_ed,
        "edition_catalogs": len(eds),
        "languages": dict(sorted(langs.items(), key=lambda x: -x[1])),
        "availability_works": idx.get("count") or len(idx),
        "m_catalog_works": len(mworks),
        "m_coverage": cov,
        "bibliographic_links": n_links,
        "top_domains": dict(sorted(domains.items(), key=lambda x: -x[1])[:10]),
        "ranked_rows": len(ranked),
        "ranked_untranslated": sum(1 for r in ranked if r.get("T") == 0),
        "ranked_top5": [{k: r.get(k) for k in
                         ("burn_rank", "catalog", "title", "verses", "T_why")}
                        for r in ranked[:5]],
        "paths": {k: v["path"] for k, v in paths().items()
                  if isinstance(v, dict) and "path" in v},
    }


def list_works(has_translation: bool | None = None, language: str = "",
               min_verses: int = 0, max_verses: int = 0,
               limit: int = 50, offset: int = 0,
               data: dict | None = None) -> dict:
    """Browse works with filters — the list endpoint for agents."""
    d = data or load()
    rows = []
    for cat, b in d["burn"].items():
        if not cat:
            continue
        eds = d.get("editions", {}).get(cat, [])
        has_t = (b.get("has_translation") or "").strip().upper() == "TRUE" or bool(eds)
        if has_translation is not None and has_t != has_translation:
            continue
        if language:
            langs = {(e.get("language") or "") for e in eds}
            if language not in langs:
                continue
        try:
            verses = int(b.get("verses") or 0)
        except Exception:
            verses = 0
        if min_verses and verses < min_verses:
            continue
        if max_verses and verses > max_verses:
            continue
        rows.append({
            "catalog": cat,
            "title": b.get("title") or "",
            "author": b.get("author") or "",
            "verses": verses,
            "has_translation": has_t,
            "edition_count": len(eds),
            "languages": sorted({(e.get("language") or "und") for e in eds}),
            "tw_status": b.get("tw_status") or "",
            "info_url": b.get("info_url") or (eds[0].get("info_url") if eds else ""),
            "download_url": b.get("download_url") or next(
                (e.get("download_url") for e in eds if e.get("download_url")), ""),
        })
    # untranslated shortest-first; translated by edition count desc
    rows.sort(key=lambda r: (r["has_translation"], r["verses"] if not r["has_translation"] else -r["edition_count"],
                             r["catalog"]))
    total = len(rows)
    page = rows[offset:offset + limit] if limit else rows[offset:]
    return {"total": total, "offset": offset, "limit": limit, "count": len(page),
            "rows": page, "baseline": f"muktabodha_final_{AS_OF}"}


def list_editions(catalog: str = "", language: str = "", tier: str = "",
                  downloadable_only: bool = False,
                  limit: int = 50, offset: int = 0,
                  data: dict | None = None) -> dict:
    """Browse edition records (the translation links live here)."""
    d = data or load()
    rows = []
    for cat, eds in d.get("editions", {}).items():
        if catalog and cat != catalog:
            continue
        for e in eds:
            if language and (e.get("language") or "") != language:
                continue
            if tier and tier.upper() not in (e.get("access_tier") or "").upper():
                continue
            if downloadable_only and not (e.get("download_url") or ""):
                continue
            rows.append({
                "catalog": cat,
                "title": e.get("title") or "",
                "translator": e.get("translator") or "",
                "year": e.get("year") or "",
                "language": e.get("language") or "",
                "scope": e.get("scope") or "",
                "publisher": e.get("publisher") or "",
                "access_tier": e.get("access_tier") or "",
                "info_url": e.get("info_url") or "",
                "download_url": e.get("download_url") or "",
                "corroboration_url": e.get("corroboration_url") or "",
                "confidence": e.get("confidence") or "",
                "verification_status": e.get("verification_status") or "",
                "evidence": (e.get("evidence") or "")[:300],
                "verified_at": e.get("verified_at") or "",
            })
    rows.sort(key=lambda r: (r["catalog"], r.get("year") or ""))
    total = len(rows)
    page = rows[offset:offset + limit] if limit else rows[offset:]
    return {"total": total, "offset": offset, "limit": limit, "count": len(page),
            "rows": page, "baseline": f"muktabodha_final_{AS_OF}"}


def list_links(catalog: str = "", domain: str = "", edition_related: bool | None = None,
               limit: int = 50, offset: int = 0) -> dict:
    """Browse bibliographic URL links (discovery, not all are translations)."""
    if not LINKS.exists():
        return {"total": 0, "rows": [], "error": "links file missing"}
    rows = []
    with LINKS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if catalog and (r.get("catalog") or "") != catalog:
                continue
            if domain and domain not in (r.get("domain") or ""):
                continue
            er = (r.get("edition_related") or "").upper() == "YES"
            if edition_related is not None and er != edition_related:
                continue
            rows.append({
                "catalog": r.get("catalog") or "",
                "url": r.get("url") or "",
                "domain": r.get("domain") or "",
                "source_roles": r.get("source_roles") or "",
                "edition_related": er,
                "unresolved_audit_related": (r.get("unresolved_audit_related") or "").upper() == "YES",
                "origin_files": r.get("origin_files") or "",
                "evidence_notes": (r.get("evidence_notes") or "")[:300],
            })
    total = len(rows)
    page = rows[offset:offset + limit] if limit else rows[offset:]
    return {"total": total, "offset": offset, "limit": limit, "count": len(page),
            "rows": page, "baseline": f"muktabodha_final_{AS_OF}"}


def query_availability(catalog: str = "", work: str = "", language: str = "",
                       coverage: str = "", missing: bool | None = None,
                       limit: int = 50, offset: int = 0) -> dict:
    """Query the compiled translation-availability index (API surface shape)."""
    if not INDEX.exists():
        return {"total": 0, "rows": [], "error": "index missing"}
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    works = idx.get("works") or {}
    rows = []
    for wid, v in works.items():
        cat = v.get("catalog_no") or ""
        if catalog and cat != catalog and wid != catalog:
            continue
        if work and wid != work and (v.get("title") or "").lower() != work.lower():
            continue
        if language and language not in (v.get("languages") or []):
            continue
        if coverage and (v.get("coverage") or "") != coverage:
            continue
        if missing is not None and bool(v.get("missing")) != missing:
            continue
        rows.append({
            "work": wid,
            "catalog_no": cat,
            "title": v.get("title") or "",
            "has_english": v.get("has_english"),
            "coverage": v.get("coverage"),
            "missing": v.get("missing"),
            "languages": v.get("languages") or [],
            "translations": v.get("translations") or [],
            "english_urls": v.get("english_urls") or [],
            "copyright_hint": v.get("copyright_hint") or "",
            "tw_status": v.get("tw_status") or "",
            "baseline": v.get("baseline") or idx.get("meta", {}).get("baseline"),
        })
    total = len(rows)
    page = rows[offset:offset + limit] if limit else rows[offset:]
    return {"total": total, "offset": offset, "limit": limit, "count": len(page),
            "index_count": idx.get("count"), "rows": page,
            "meta": {k: idx.get("meta", {}).get(k) for k in
                     ("compiled_at", "baseline", "note", "works")}}


def main() -> int:
    ap = argparse.ArgumentParser(description="Final Muktabodha bibliography base layer")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("paths")
    sub.add_parser("stats")
    sub.add_parser("schema")

    g = sub.add_parser("get")
    g.add_argument("--catalog", default="")
    g.add_argument("--title", default="")

    s = sub.add_parser("search")
    s.add_argument("q")
    s.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("priority")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--untranslated-only", action="store_true")

    w = sub.add_parser("works")
    w.add_argument("--has-translation", choices=["true", "false"], default=None)
    w.add_argument("--language", default="")
    w.add_argument("--min-verses", type=int, default=0)
    w.add_argument("--max-verses", type=int, default=0)
    w.add_argument("--limit", type=int, default=50)
    w.add_argument("--offset", type=int, default=0)

    ed = sub.add_parser("editions")
    ed.add_argument("--catalog", default="")
    ed.add_argument("--language", default="")
    ed.add_argument("--tier", default="")
    ed.add_argument("--downloadable-only", action="store_true")
    ed.add_argument("--limit", type=int, default=50)
    ed.add_argument("--offset", type=int, default=0)

    ln = sub.add_parser("links")
    ln.add_argument("--catalog", default="")
    ln.add_argument("--domain", default="")
    ln.add_argument("--edition-related", choices=["true", "false"], default=None)
    ln.add_argument("--limit", type=int, default=50)
    ln.add_argument("--offset", type=int, default=0)

    av = sub.add_parser("availability")
    av.add_argument("--catalog", default="")
    av.add_argument("--work", default="")
    av.add_argument("--language", default="")
    av.add_argument("--coverage", default="")
    av.add_argument("--missing", choices=["true", "false"], default=None)
    av.add_argument("--limit", type=int, default=50)
    av.add_argument("--offset", type=int, default=0)

    a = ap.parse_args()

    def _b(v):
        return None if v is None else (v == "true")

    def out(obj):
        print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
        return 0

    if a.cmd == "paths" or a.cmd is None:
        return out(paths())
    if a.cmd == "stats":
        return out(stats())
    if a.cmd == "schema":
        return out(schema())
    if a.cmd == "get":
        return out(lookup(a.catalog, a.title))
    if a.cmd == "search":
        return out(search(a.q, a.limit))
    if a.cmd == "priority":
        rows = priority_rows(a.limit, a.untranslated_only)
        return out({"count": len(rows), "rows": rows})
    if a.cmd == "works":
        return out(list_works(has_translation=_b(a.has_translation),
                              language=a.language, min_verses=a.min_verses,
                              max_verses=a.max_verses, limit=a.limit, offset=a.offset))
    if a.cmd == "editions":
        return out(list_editions(catalog=a.catalog, language=a.language,
                                 tier=a.tier, downloadable_only=a.downloadable_only,
                                 limit=a.limit, offset=a.offset))
    if a.cmd == "links":
        return out(list_links(catalog=a.catalog, domain=a.domain,
                              edition_related=_b(a.edition_related),
                              limit=a.limit, offset=a.offset))
    if a.cmd == "availability":
        return out(query_availability(catalog=a.catalog, work=a.work,
                                      language=a.language, coverage=a.coverage,
                                      missing=_b(a.missing),
                                      limit=a.limit, offset=a.offset))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
