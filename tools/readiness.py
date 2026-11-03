#!/usr/bin/env python3
"""tools/readiness.py — the burn-down matrix: every work, every gate, one screen.

  python3 tools/readiness.py            # all works, sorted most-ready first
  python3 tools/readiness.py --work paramarthasara

Columns: PROOF (PASS/total) · SIGNOFF (signed/songs) · L4 (songs with data) ·
C1 (songs with commentary) · SITE (ipvv chunks: PASS/total, l4 count) ·
PUSH (pushing queries) · READY (all of: proof all-PASS + signoff all + site PASS=all).
Read-only; cross-repo reads (ipvv) are tolerated — absent ipvv shows '-'
"""
from __future__ import annotations
import argparse, glob, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IPVV = Path("/root/ipvv")

def song_of(p: Path) -> str:
    return p.name.split(".")[0]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work")
    a = ap.parse_args()

    pushing = {}
    try:
        idx = json.loads((IPVV / "site/data/pushing/INDEX.json").read_text())
        for r in idx.get("records", []):
            h = r.get("work_hint", "")
            pushing[h] = pushing.get(h, 0) + len(r.get("questions", []))
    except Exception:
        pass

    rows = []
    dirs = [ROOT / a.work] if a.work else sorted({p.parent.parent for p in ROOT.glob("*/data/*.t1.json")})
    for w in dict.fromkeys(dirs):
        if not (w / "data").exists():
            continue
        proofs = sorted((w / "proof").glob("proof-*.json")) if (w / "proof").exists() else []
        ppass = sum(1 for f in proofs if json.loads(f.read_text()).get("deterministic_gate") == "PASS")
        songs = sorted({song_of(p) for p in (w / "data").glob("*.t1.json")})
        signoffs = len(list((w / "data").glob("*.signoff.json")))
        l4 = len(list((w / "data").glob("*.l4.json")))
        c1 = len(list((w / "data").glob("*.c1.json")))
        site = l4n = "-"
        site_ok = site_all = False
        tf = IPVV / f"site/data/translations/{w.name}.json"
        if tf.exists():
            try:
                chunks = json.loads(tf.read_text())
                npass = sum(1 for c in chunks if c.get("gate") == "PASS")
                l4n = sum(1 for c in chunks if c.get("l4"))
                site, site_ok = f"{npass}/{len(chunks)}", npass == len(chunks)
                site_all = all(c.get("l4") for c in chunks)
            except Exception:
                site = "?"
        push = pushing.get(w.name, "-")
        proof_ok = bool(proofs) and ppass == len(proofs)
        sign_ok = signoffs == len(songs)
        ready = proof_ok and sign_ok and site_ok and site_all
        rows.append((w.name, f"{ppass}/{len(proofs)}", f"{signoffs}/{len(songs)}",
                     f"{l4}/{len(songs)}", f"{c1}/{len(songs)}", str(site), str(l4n),
                     str(push), "READY" if ready else ""))

    rows.sort(key=lambda r: (r[-1] == "READY", int(r[2].split("/")[0]) - int(r[2].split("/")[1]) if "/" in r[2] else 0), reverse=True)
    hdr = ("WORK", "PROOF", "SIGNOFF", "L4d", "C1", "SITE", "L4site", "PUSH", "")
    widths = [max(len(str(x)) for x in col) for col in zip(hdr, *rows)]
    def line(r): return "  ".join(str(x).ljust(w) for x, w in zip(r, widths))
    print(line(hdr)); print(line(tuple("-" * w for w in widths)))
    for r in rows:
        print(line(r))
    ready = sum(1 for r in rows if r[-1] == "READY")
    print(f"\n{ready}/{len(rows)} READY · full signoff+proof+site+l4site")
    return 0

if __name__ == "__main__":
    sys.exit(main())
