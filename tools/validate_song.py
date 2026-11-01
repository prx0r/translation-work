#!/usr/bin/env python3
"""tools/validate_song.py — validate a song's canonical JSON data objects (all 6 invariants).

  python3 tools/validate_song.py --song s01 --work sivastotravali

Checks schemas/t1+l0+argmap+l2+c1 plus cross-layer invariants:
  1. L0.chosen == T1.quick_gloss (unless revised+reason)
  2. coverage: T1+L0+argmap+L2 span exactly the GRETIL verse set
Returns 0 valid / 1 errors. Stdlib only.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "schemas"))
from proof_record import load_gretil_song  # noqa: E402
import t1 as t1s, l0 as l0s, argmap as ams, l2 as l2s, c1 as c1s, c2 as c2s  # noqa: E402
try:
    import signoff as signoff_s  # noqa: E402
except ImportError:
    signoff_s = None


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True); ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()
    w = ROOT / args.work
    song, n = args.song, int(args.song[1:])
    data = w / "data"
    errs: list[str] = []

    t1 = json.loads((data / f"{song}.t1.json").read_text())
    l0 = json.loads((data / f"{song}.l0.json").read_text())
    am = json.loads((data / f"{song}.argmap.json").read_text())
    l2 = json.loads((data / f"{song}.l2.json").read_text())
    c1 = json.loads((data / f"{song}.c1.json").read_text())

    src = load_gretil_song(Path("/root/ipvv/site/data/sanskrit/sivastotravali-u.txt"), n)
    src_sha = sha(" ".join(" ".join(t) for v, t in sorted(src.items())))
    src_verses = set(src)
    src_flat = " ".join(" ".join(t) for v, t in sorted(src.items()))

    t1_verses = {o["verse_id"] for o in t1}
    l0_ids = {o["id"] for o in l0}
    l0_by_id = {o["id"]: o for o in l0}
    for o in t1:
        errs += t1s.validate(o, f"t1[{o.get('verse_id')}]")
    for o in l0:
        errs += l0s.validate(o, f"l0[{o.get('id')}]")
    for o in am:
        errs += ams.validate(o, f"argmap[{o.get('verse_id')}]", l0_ids, t1_verses, src_sha, l0_by_id)
    for o in l2:
        errs += l2s.validate(o, f"l2[{o.get('verse_id')}]", l0_ids, src_flat)
    errs += c1s.validate(c1, "c1")
    c2path = data / f"{song}.c2.json"
    c2 = json.loads(c2path.read_text()) if c2path.exists() else None
    if c2 is not None:
        errs += c2s.validate(c2, "c2", len(c1.get("essence", [])))
    spost = data / f"{song}.signoff.json"
    signoff = None
    if spost.exists():
        if signoff_s is None:
            errs.append("signoff present but schemas/signoff.py unavailable")
        else:
            signoff = json.loads(spost.read_text())
            errs += signoff_s.validate(signoff, "signoff")

    # invariant 1: L0.chosen == T1.quick_gloss unless revised
    tq = {(o["verse_id"], i): g for o in t1 for i, g in
          enumerate([t.get("quick_gloss", "") for t in o.get("tokens", [])])}
    per_verse_counter: dict[str, int] = {}
    for o in l0:
        v = o["verse_id"]
        per_verse_counter[v] = per_verse_counter.get(v, 0)
        i = per_verse_counter[v]; per_verse_counter[v] += 1
        if o.get("status") != "PARSED" or not o.get("options"):
            continue
        chosen = o["options"][o.get("chosen_index", 0)].get("gloss", "")
        if not o.get("revised") and chosen != (tq.get((v, i)) or ""):
            errs.append(f"l0[{o['id']}]: chosen {chosen!r} != T1.quick_gloss {tq.get((v, i))!r} (mark revised+reason)")

    # invariant 6: coverage == GRETIL verse set
    for name, have in [("t1", {o["verse"] for o in t1}), ("argmap", {o["verse"] for o in am}),
                       ("l2", {o["verse"] for o in l2})]:
        if have != src_verses:
            errs.append(f"coverage {name}: {sorted(have)} != source {sorted(src_verses)}")
    l0_verses = {int(o["verse_id"].split("-v")[1]) for o in l0}
    if l0_verses != src_verses:
        errs.append(f"coverage l0 verses {sorted(l0_verses)} != source {sorted(src_verses)}")

    print(json.dumps({"song": song, "errors": errs,
                      "counts": {"t1": len(t1), "l0": len(l0), "argmap": len(am),
                                 "l2": len(l2), "essence": len(c1.get("essence", [])),
                                 "renders": list(c1.get("renders", {})),
                      "c2_renders": [r.get("style") for r in (c2 or {}).get("renders", [])]
                                 if c2 else [],
                      "signoff": bool(signoff)}}, indent=1))
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
