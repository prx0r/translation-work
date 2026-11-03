#!/usr/bin/env python3
"""tools/emit_scholar.py — project a work's scholar/ ledgers + layer originals to svread.

  python3 tools/emit_scholar.py --work paramarthasara

Writes `/root/svread/data/scholar/<work>.json` (+ `index.json`) for the Scholar hub.
Originals come from the canonical `data/<song>.<layer>.json` files (the same bytes
`tools/scholar.py show` prints) — the hub never re-derives them.

Read-only: never writes back into this repo.
"""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/root/translation-work")
SVREAD = Path("/root/svread")
sys.path.insert(0, str(ROOT / "tools"))
import scholar as sch  # noqa: E402  (reuse the exact loaders + hashers)

def build(work: str) -> dict:
    # layer originals for every verse/song target in the work's canonical data
    originals: dict = {layer: {} for layer in sch.LAYERS}
    songs = sorted({p.stem.split(".")[0] for p in (ROOT / work / "data").glob("*.l3.json")})
    if not songs:
        raise SystemExit(f"{work}: no data/*.l3.json")
    for layer in sch.LAYERS:
        for song in songs:
            f = ROOT / work / "data" / f"{song}.{layer}.json"
            if not f.exists():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            if layer == "c1":
                originals[layer][song] = d
                continue
            for row in d:
                tid = row.get("verse_id")
                if tid:
                    originals[layer][tid] = row

    versions = sch.load_versions(work)
    reviews = sch.jsonl_read(sch.rpath(work))
    promotions = sch.jsonl_read(sch.ppath(work))
    signoffs = []
    stack_hashes = {}
    for song in songs:
        cur, _ = sch.stack_sha(work, song)
        stack_hashes[song] = cur
        so = sch.load_signoff(work, song)
        if so:
            so = dict(so)
            so["stack_sha"] = cur
            # back the signoff with its review id (the live binding)
            rv = [r for r in reviews if r.get("review_target", {}).get("object_ref")
                  == f"original:{work}:{song}"]
            so["review_id"] = rv[-1]["review_id"] if rv else ""
            signoffs.append(so)

    return {
        "work": work,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "translation-work canonical data + scholar/ ledgers (emit_scholar.py)",
        "originals": originals,
        "versions": versions,
        "reviews": reviews,
        "promotions": promotions,
        "signoffs": signoffs,
        "stack_hashes": stack_hashes,
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="paramarthasara")
    ap.add_argument("--out", default=str(SVREAD / "data" / "scholar"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = build(a.work)
    p = out / f"{a.work}.json"
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    # index of all emitted works (small, for the hub's work list)
    idx_path = out / "index.json"
    idx = json.loads(idx_path.read_text()) if idx_path.exists() else {}
    idx[a.work] = {
        "title": a.work,
        "versions": len(doc["versions"]),
        "reviews": len(doc["reviews"]),
        "signoffs": len(doc["signoffs"]),
        "generated": doc["generated"],
    }
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")

    kb = p.stat().st_size // 1024
    print(f"emitted {p} ({kb} KB) — {len(doc['versions'])} versions, "
          f"{len(doc['reviews'])} reviews, {len(doc['signoffs'])} signoffs, "
          f"originals: " + ", ".join(
              f"{l}:{len(v)}" for l, v in doc["originals"].items() if v))
    return 0

if __name__ == "__main__":
    sys.exit(main())
