#!/usr/bin/env python3
"""openpatala_translations — write translation-evidence rows in the
bibliographySeed.ts shape (language/translator/coverage/complete/type/url).

The translations table is relational (translator_ids[], external_ids jsonb);
this writer maps the seed's flat shape onto it. Idempotent (ON CONFLICT
DO NOTHING on stable ids). Seed records without work rows get minimal
rows (provider seed, verified false) so the FK holds.

Usage:
  python3 tools/openpatala_translations.py --backfill-seed   # 34 records
  python3 tools/openpatala_translations.py --add --work ID --lang en \
      --translator NAME --coverage complete --complete 1 --type scholarly \
      --url https://...
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone

DSN = "dbname=openpatala user=patala password=patala host=127.0.0.1"

def slug(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unknown"

def db():
    import psycopg2
    return psycopg2.connect(DSN)

def ensure_work(cur, work_id: str, title: str, traditions: list):
    cur.execute("select 1 from works where id=%s", (work_id,))
    if cur.fetchone():
        return False
    cur.execute(
        "insert into works(id, preferred_title, work_type, external_ids)"
        " values(%s,%s,'TEXT',%s) on conflict do nothing",
        (work_id, title,
         json.dumps({"seed_traditions": traditions,
                     "provider": "bibliographySeed", "verified": False})))
    return True

def ensure_person(cur, name: str) -> str:
    pid = "person-" + slug(name)
    cur.execute("insert into people(id, preferred_name) values(%s,%s)"
                " on conflict do nothing", (pid, name))
    return pid

def add_translation(cur, work_id: str, lang: str, translator: str,
                    coverage: str, complete: bool, ttype: str,
                    url: str | None, provenance: str) -> str:
    pid = ensure_person(cur, translator)
    cur.execute("select count(*) from translations where work_id=%s",
                (work_id,))
    n = cur.fetchone()[0]
    tid = f"{work_id}:tr:{n + 1}"
    ext = [{"coverage": coverage, "complete": complete, "type": ttype}]
    if url:
        ext[0]["url"] = url
    cur.execute(
        "insert into translations(id, work_id, target_language,"
        " translator_ids, completeness, external_ids, provenance_refs,"
        " created_at) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        " on conflict do nothing",
        (tid, work_id, lang, [pid],
         "complete" if complete else "partial",
         json.dumps(ext), [provenance],
         datetime.now(timezone.utc)))
    return tid

def backfill_seed() -> tuple[int, int]:
    import re as _re
    src = open("/root/openpatalaproject/data/atlas/bibliographySeed.ts",
               encoding="utf-8", errors="replace").read()
    src = _re.sub(r"^import.*$", "", src, flags=_re.M)
    src = src.replace("export const seed", "const seed").replace(
        "const seed: BibliographyRecord[]", "const seed")
    open("/tmp/seed_full.mjs", "w").write(
        src + "\nconsole.log(JSON.stringify(seed));\n")
    import subprocess
    raw = subprocess.run(["node", "/tmp/seed_full.mjs"], capture_output=True,
                         text=True, timeout=60).stdout
    seed = json.loads(raw)
    conn, nw, nt = db(), 0, 0
    cur = conn.cursor()
    for r in seed:
        wid = r["id"]
        if ensure_work(cur, wid, r.get("work") or wid,
                       r.get("traditions") or []):
            nw += 1
        for t in r.get("translations") or []:
            add_translation(cur, wid, t.get("language") or "en",
                            t.get("translator") or "unknown",
                            t.get("coverage") or "", bool(t.get("complete")),
                            t.get("type") or "", t.get("url"),
                            "bibliographySeed.ts:status_checked_2026-08-10")
            nt += 1
    conn.commit()
    return nw, nt

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill-seed", action="store_true")
    ap.add_argument("--work", default="")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--translator", default="")
    ap.add_argument("--coverage", default="")
    ap.add_argument("--complete", type=int, default=0)
    ap.add_argument("--type", default="")
    ap.add_argument("--url", default="")
    a = ap.parse_args()
    if a.backfill_seed:
        nw, nt = backfill_seed()
        print(f"works created: {nw}, translation rows: {nt}")
        return 0
    conn = db()
    cur = conn.cursor()
    tid = add_translation(cur, a.work, a.lang, a.translator or "unknown",
                          a.coverage, bool(a.complete), a.type,
                          a.url or None, "manual:openpatala_translations")
    conn.commit()
    print(tid)
    return 0

if __name__ == "__main__":
    sys.exit(main())
