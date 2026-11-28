#!/usr/bin/env python3
"""corpus_terms — OCHS text-mining ports (term freq, tf-idf distinctiveness,
bigrams) over the Muktabodha corpus, grouped by burn school.

Ported analyses from ulyngs/ochs_text_mining (tidytext: term frequencies +
tf-idf + n-grams). Pure Python, stdlib only. Used for: school vocabulary
profiles (shared-term burn grouping), glossary seeding per school, and
parallel-passage candidate surfacing (shared rare bigrams).

Usage: python3 tools/corpus_terms.py [--top N]
Reads: /tmp/mukta_census.json + /tmp/mukta/MUKTABODHA-LIBRARY-IAST/*.txt
  + burn school assignments (process/beam/burn_sequence.json)
Writes: process/beam/school_terms.json {school: {terms, bigrams, n_texts}}
"""
from __future__ import annotations
import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return s

def toks(text: str) -> list:
    text = norm(text)
    text = re.sub(r"[|‖/0-9()\[\]{}<>*­–—‘’“”\"'.,;:!?]", " ", text)
    return [w for w in text.split() if len(w) > 2 and not w.startswith("http")]

def body_text(fp: Path) -> str:
    t = fp.read_text(encoding="utf-8", errors="replace")
    i = t.find("****", 2000)
    return t[i if i > 0 else 0:]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    seq = {o["catalog"]: o["school"]
           for o in json.load(open("/root/translation-work/process/beam/"
                                   "burn_sequence.json"))}
    rows = json.load(open("/tmp/mukta_census.json"))
    base = Path("/tmp/mukta/MUKTABODHA-LIBRARY-IAST")
    tf: dict = {}
    df: Counter = Counter()
    bg: dict = {}
    ndoc: Counter = Counter()
    for r in rows:
        sch = seq.get(r["catalog"], "misc")
        fp = base / r["file"]
        if not fp.exists():
            continue
        ws = toks(body_text(fp))
        tf.setdefault(sch, Counter()).update(ws)
        bg.setdefault(sch, Counter()).update(
            zip(ws, ws[1:]))
        for w in set(ws):
            df[(sch, w)] = df.get((sch, w), 0) + 1
        ndoc[sch] += len(ws)
        df[("__docs__", sch)] = df.get(("__docs__", sch), 0) + 1
    out = {}
    for sch, c in tf.items():
        total = sum(c.values())
        scored = []
        for w, f in c.most_common(400):
            # distinctiveness: tf in school vs presence elsewhere
            elsewhere = sum(1 for (s2, w2) in df
                            if w2 == w and not (isinstance(s2, str)
                                                and s2.startswith("__"))
                            and s2 != sch)
            idf = math.log((len(tf) + 1) / (elsewhere + 1)) + 1
            scored.append((w, f, round(f / total * 10000, 2),
                           round(f / total * 10000 * idf, 2)))
        scored.sort(key=lambda x: -x[3])
        out[sch] = {
            "tokens": ndoc[sch],
            "terms": [{"w": w, "n": f, "per10k": p, "distinct": d}
                      for w, f, p, d in scored[:a.top]],
            "bigrams": [{"w": f"{x} {y}", "n": n}
                        for (x, y), n in bg[sch].most_common(15)],
        }
    json.dump(out, open("/root/translation-work/process/beam/school_terms.json",
                         "w"), ensure_ascii=False, indent=0)
    for sch in sorted(out, key=lambda s: -out[s]["tokens"])[:10]:
        top5 = ", ".join(t["w"] for t in out[sch]["terms"][:5])
        print(f"{sch:20s} {out[sch]['tokens']:8d} toks | {top5}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
