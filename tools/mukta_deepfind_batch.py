#!/usr/bin/env python3
"""mukta_deepfind_batch — run translation_deepfinder over works, threaded.

Finds WHAT translations exist per work, WHERE, and download links (via the
download layer for confirmed hits). Resumable: skips ids already in output.
Feeds tools/prioritize_mukta.py (T values) and PR-001's matrix.

Usage:
  python3 tools/mukta_deepfind_batch.py [--limit N] [--only M00067,M00019]
      [--source census|openpatala] [--workers 8] [--out deepfind.jsonl]
Sources: census (/tmp/mukta_census.json, skips buddhist) or openpatala
  (Postgres works table, skips mukta-* already covered by census batch).
Writes: process/beam/<out> (one row per work).
"""
from __future__ import annotations
import argparse, json, sys, threading, time, unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, "/root/openpatalaproject/pipeline")
sys.path.insert(0, "/root/openpatalaproject")

BUDDHIST = ("manjusrimulakalpa", "guhyasamaja", "sadhanamala", "advayavajra")

def norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(c)).lower()

def census_works():
    rows = json.load(open("/tmp/mukta_census.json"))
    return [{"id": r["catalog"], "title": r["title"], "verses": r["verses"]}
            for r in rows
            if not any(k in norm(r["title"] + " " + r["file"]) for k in BUDDHIST)]

def openpatala_works():
    import psycopg2
    c = psycopg2.connect(dbname="openpatala", user="patala",
                         password="patala", host="127.0.0.1")
    cur = c.cursor()
    cur.execute("select id, preferred_title from works "
                "where id not like 'mukta-%' order by id")
    return [{"id": i, "title": t or i, "verses": 0} for i, t in cur.fetchall()]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    ap.add_argument("--source", default="census",
                    choices=["census", "openpatala"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="deepfind.jsonl")
    a = ap.parse_args()
    from translation_deepfinder import deepfind
    pool = census_works() if a.source == "census" else openpatala_works()
    outp = ROOT / "process/beam" / a.out
    done = set()
    if outp.exists():
        for ln in open(outp, encoding="utf-8"):
            try:
                done.add(json.loads(ln)["catalog"])
            except Exception:
                pass
    only = set(x.strip() for x in a.only.split(",") if x.strip())
    todo = [w for w in pool
            if w["id"] not in done and (not only or w["id"] in only)]
    if a.limit:
        todo = todo[:a.limit]
    print(f"todo: {len(todo)} (have {len(done)})", flush=True)
    lock, fh, n = threading.Lock(), open(outp, "a", encoding="utf-8"), [0]

    def one(w):
        try:
            res = deepfind(w["id"], w["title"], net=True)
            row = {"catalog": w["id"], "title": w["title"],
                   "verses": w.get("verses", 0),
                   "confirmed": res.get("confirmed_translations", 0),
                   "translations": res.get("translations", [])[:12],
                   "sources": {k: {"status": v.get("status"),
                                   "hits": v.get("hits", 0)}
                               for k, v in res.get("sources", {}).items()}}
        except Exception as e:  # noqa: BLE001 - never let one work kill the batch
            row = {"catalog": w["id"], "title": w["title"],
                   "verses": w.get("verses", 0), "error": str(e)[:200]}
        with lock:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            n[0] += 1
            if n[0] % 25 == 0:
                print(f"{n[0]}/{len(todo)}", flush=True)
        time.sleep(0.5)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(one, todo))
    print(f"DONE {n[0]}", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
