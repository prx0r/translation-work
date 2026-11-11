#!/usr/bin/env python3
"""mukta_deepfind_batch — run translation_deepfinder over the Muktabodha census.

Finds WHAT translations exist per work, WHERE, and download links (via the
download layer for confirmed hits). Resumable: skips catalogs already in the
output JSONL. Feeds tools/prioritize_mukta.py (T values) and PR-001's matrix.

Usage: python3 tools/mukta_deepfind_batch.py [--limit N] [--only M00067,M00019]
Reads: /tmp/mukta_census.json (falls back to titles only)
Writes: process/beam/deepfind.jsonl (one row per work: catalog/title/
  confirmed count/translations[]/sources{}).
"""
from __future__ import annotations
import argparse, json, sys, time, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, "/root/openpatalaproject/pipeline")
sys.path.insert(0, "/root/openpatalaproject")

BUDDHIST = ("manjusrimulakalpa", "guhyasamaja", "sadhanamala", "advayavajra")

def norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(c)).lower()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    from translation_deepfinder import deepfind
    rows = json.load(open("/tmp/mukta_census.json"))
    outp = ROOT / "process/beam/deepfind.jsonl"
    done = set()
    if outp.exists():
        for ln in open(outp, encoding="utf-8"):
            try:
                done.add(json.loads(ln)["catalog"])
            except Exception:
                pass
    only = set(x.strip() for x in a.only.split(",") if x.strip())
    work = [r for r in rows
            if r["catalog"] not in done
            and (not only or r["catalog"] in only)
            and not any(k in norm(r["title"] + " " + r["file"]) for k in BUDDHIST)]
    if a.limit:
        work = work[:a.limit]
    print(f"todo: {len(work)} (have {len(done)})", flush=True)
    n = 0
    with open(outp, "a", encoding="utf-8") as f:
        for r in work:
            try:
                res = deepfind(r["catalog"], r["title"], net=True)
                row = {"catalog": r["catalog"], "title": r["title"],
                       "verses": r["verses"],
                       "confirmed": res.get("confirmed_translations", 0),
                       "translations": res.get("translations", [])[:12],
                       "sources": {k: {"status": v.get("status"),
                                       "hits": v.get("hits", 0)}
                                   for k, v in res.get("sources", {}).items()}}
            except Exception as e:  # noqa: BLE001 - never let one work kill the batch
                row = {"catalog": r["catalog"], "title": r["title"],
                       "verses": r["verses"], "error": str(e)[:200]}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            n += 1
            if n % 25 == 0:
                print(f"{n}/{len(work)}", flush=True)
            time.sleep(0.5)
    print(f"DONE {n}", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
