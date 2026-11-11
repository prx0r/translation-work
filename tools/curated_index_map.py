#!/usr/bin/env python3
"""curated_index_map — one-time scrape of curated translation indexes.

The live site-searches miss these hosts (no WP search / JS walls), but
their INDEX pages are static and list translations directly:
  shivashakti.com/texts (+/netra) — Magee translation PDFs (direct links)
  mahanaya.org/en/scriptures/    — Dyczkowski scripture translations
Output: process/beam/curated_hits.jsonl {catalog, title, hits[]}.
Rerun rarely (indexes change slowly); polite single fetch each.
"""
from __future__ import annotations
import html as _h
import json
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "patala-translation-deepfinder/0.1 (mailto:dev@patala.local)"

def fetch(url: str, timeout: int = 30) -> str:
    r = subprocess.run(["curl", "-s", "-L", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout or ""

def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    s = "".join(ch for ch in s if ch.isalpha())
    for a, b in (("vijaana", "vijnana"), ("swami", "svami"),
                 ("shiva", "siva"), ("shaiva", "saiva")):
        s = s.replace(a, b)
    return s

def anchors(page: str, base: str) -> list:
    out = []
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
        href = _h.unescape(m.group(1))
        text = _h.unescape(re.sub("<[^>]+>", "", m.group(2))).strip()
        if not text or len(text) < 4:
            continue
        if href.startswith("mailto:") or "#" in href:
            continue
        full = href if href.startswith("http") else base.rstrip("/") + \
            (href if href.startswith("/") else "/" + href)
        out.append((text, full))
    return out

def main() -> int:
    idx = []  # (source, text, url)
    for page in ("https://shivashakti.com/texts",
                 "https://shivashakti.com/netra",
                 "https://shivashakti.com/bibby"):
        sh = fetch(page)
        for text, url in anchors(sh, "https://shivashakti.com"):
            if url.endswith((".pdf", ".ps", ".htm", ".html")) or \
               "/texts" in url or "/netra" in url or "/bib" in url:
                idx.append(("shivashakti", text, url))
    print(f"shivashakti anchors: {len(idx)}", flush=True)
    mh = fetch("https://mahanaya.org/en/scriptures/")
    n0 = len(idx)
    for m in re.finditer(
            r'<a[^>]*href="(/en/scriptures/[a-z0-9-]+/)"[^>]*>([^<]+)</a>', mh):
        idx.append(("mahanaya", _h.unescape(m.group(2)).strip(),
                    "https://mahanaya.org" + m.group(1)))
    print(f"mahanaya entries: {len(idx) - n0}", flush=True)
    # hareesh.org sitemap: Wallis verse-by-verse translations (esp. VB Tantra112)
    sm = fetch("https://hareesh.org/sitemap.xml")
    n1 = len(idx)
    for m in re.finditer(r"<loc>([^<]+)</loc>", sm):
        u = m.group(1)
        slug = u.rsplit("/", 1)[-1].replace("-", " ")
        if len(slug) > 12:
            idx.append(("hareesh", slug[:90], u))
    print(f"hareesh urls: {len(idx) - n1}", flush=True)

    rows = json.load(open("/tmp/mukta_census.json"))
    n_hit, n_rows = 0, 0
    with open(ROOT / "process/beam/curated_hits.jsonl", "w",
              encoding="utf-8") as f:
        for r in rows:
            t = norm(r["title"])
            hits = []
            for src, text, url in idx:
                n_ = norm(text)
                if len(t) > 7 and len(n_) > 7 and (t in n_ or n_ in t):
                    hits.append({"source": src, "page": text[:90], "url": url})
            # dedup urls
            seen, uniq = set(), []
            for h in hits:
                if h["url"] not in seen:
                    seen.add(h["url"])
                    uniq.append(h)
            if uniq:
                n_hit += 1
                n_rows += len(uniq)
                f.write(json.dumps({"catalog": r["catalog"], "title": r["title"],
                                    "verses": r["verses"], "hits": uniq},
                                   ensure_ascii=False) + "\n")
    print(f"works with curated hits: {n_hit}, total hits: {n_rows}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
