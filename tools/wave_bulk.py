#!/usr/bin/env python3
"""wave_bulk — onboard N eligible works, then burn them sequentially.

Eligibility (all must hold):
  * ranked_burn status == not_started
  * catalog not in work_aliases (structural dupe guard)
  * no existing work dir
  * brief_gate PASS (researched brief: FACTS + TRAPS + LEDGER)
  * extraction ratio sane (verses >= 3 and chars/verse <= 400)

Usage: python3 tools/wave_bulk.py --n 100 [--dry]
Onboards (source intake + passages + STATUS) then runs auto_burn for each
in ONE background process (no 100 processes).
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, "/root/openpatalaproject/pipeline")
MUKTA = Path("/tmp/mukta/MUKTABODHA-LIBRARY-IAST")
OUT_OF_REALM = ("mantranaya", "vajray", "guhyasamaja", "manjusri",
                "sadhanamala", "advayavajra")


def norm(s: str) -> str:
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return "".join(ch for ch in s if ch.isalpha())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    from brief_gate import check as bg
    from harvest_to_factory import extract_verses
    from intake import validate_segments
    ranked = json.loads((ROOT / "process/beam/ranked_burn.json").read_text())
    aliases = json.loads((ROOT / "process/beam/work_aliases.json").read_text())["catalogs"]
    census = {r["catalog"]: r for r in json.loads(Path("/tmp/mukta_census.json").read_text())}
    picked, skipped = [], {"no_brief": 0, "too_short": 0, "extract_fail": 0,
                           "aliased": 0, "exists": 0, "realm": 0, "no_file": 0}
    for o in ranked:
        if len(picked) >= a.n:
            break
        cat = o["catalog"]
        c = census.get(cat)
        if not c:
            continue
        wname = f"mukta-{cat}".lower()
        if o["tw"] != "not_started":
            continue
        if cat in aliases:
            skipped["aliased"] += 1; continue
        if (ROOT / wname).is_dir():
            skipped["exists"] += 1; continue
        blob = norm(c["title"] + " " + c["file"])
        if any(k in blob for k in OUT_OF_REALM):
            skipped["realm"] += 1; continue
        ok, why = bg(wname)
        if not ok:
            skipped["no_brief"] += 1; continue
        src = next(MUKTA.glob(f"*{cat}-IAST.txt"), None)
        if src is None:
            skipped["no_file"] += 1; continue
        try:
            verses = extract_verses("MUKTABODHA", cat, src)
        except Exception:
            skipped["extract_fail"] += 1; continue
        if len(verses) < 3:
            skipped["too_short"] += 1; continue
        chars = len(src.read_text(encoding="utf-8", errors="replace"))
        if chars / max(1, len(verses)) > 400:
            skipped["extract_fail"] += 1; continue
        picked.append((cat, c, verses, wname))
    print("picked:", len(picked), "| skipped:", skipped, flush=True)
    if a.dry:
        for cat, c, v, w in picked[:20]:
            print(f"  {len(v):5d}v {cat} {c['title'][:44]}")
        return 0
    import hashlib
    on = 0
    for cat, c, verses, wname in picked:
        W = ROOT / wname
        (W / "source").mkdir(parents=True, exist_ok=True)
        (W / "data").mkdir(exist_ok=True); (W / "proof").mkdir(exist_ok=True)
        json.dump(verses, open(W / "source/verses.json", "w"), ensure_ascii=False)
        ps = []
        for i in range(0, len(verses), 25):
            n = i // 25 + 1
            ps.append({"work_id": wname, "order": n,
                       "locator": f"{wname[:8]}-p{n:02d}",
                       "verses": f"{i+1}-{i+len(verses[i:i+25])}",
                       "sanskrit": " ".join(verses[i:i + 25])})
        with open(W / "passages.jsonl", "w") as f:
            for p in ps:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        text = "\n\n".join(v.strip() for v in verses) + "\n"
        raw = text.encode(); segs = []; pos = 0
        for idx, v in enumerate(verses):
            song = ps[min(idx // 25, len(ps) - 1)]["locator"]
            b = v.strip().encode(); s = raw.find(b, pos); e = s + len(b); pos = e
            segs.append({"song": song, "verse": idx + 1,
                         "verse_id": f"{song}-v{idx+1}", "start": s, "end": e})
        (W / "source/edition.txt").write_bytes(raw)
        sj = json.dumps(segs, ensure_ascii=False)
        (W / "source/segments.json").write_text(sj)
        json.dump({"format": "source-intake/1", "work": wname,
                   "source_sha256": hashlib.sha256(raw).hexdigest(),
                   "segments_sha256": hashlib.sha256(sj.encode()).hexdigest(),
                   "edition": f"Muktabodha {cat} (IAST, CC BY-NC 4.0)"},
                  open(W / "source/manifest.json", "w"), ensure_ascii=False, indent=1)
        if validate_segments(raw, segs):
            print("intake invalid, skipping", cat); continue
        json.dump({"work": wname, "updated": "2026-11-11",
                   "next": "pass-1 auto_burn (bulk wave)",
                   "counts": {"passages": len(ps), "verses": len(verses),
                              "proof": "QUEUED"}},
                  open(W / "STATUS.json", "w"), indent=1)
        on += 1
    print("onboarded:", on, flush=True)
    # burn them all in ONE background process
    subprocess.Popen(["/bin/bash", "-lc",
                      "for d in " + " ".join(w for *_ , w in picked) +
                      "; do [ -f $d/STATUS.json ] || continue; "
                      "python3 tools/auto_burn.py --work $d --from 1 --to 999; done"],
                     cwd=ROOT, stdout=open("/root/autoburn-wave3.log", "w"),
                     stderr=subprocess.STDOUT, start_new_session=True)
    print("burn loop launched -> /root/autoburn-wave3.log")
    return 0


if __name__ == "__main__":
    sys.exit(main())
