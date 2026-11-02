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
    import l3 as l3s  # noqa: E402
except ImportError:
    l3s = None
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
    song = args.song
    data = w / "data"
    errs: list[str] = []

    t1 = json.loads((data / f"{song}.t1.json").read_text())
    l0 = json.loads((data / f"{song}.l0.json").read_text())
    am = json.loads((data / f"{song}.argmap.json").read_text())
    l2 = json.loads((data / f"{song}.l2.json").read_text())
    c1 = json.loads((data / f"{song}.c1.json").read_text())

    from workcfg import WORKS as _WORKS, song_verses as _song_verses, source_spans as _source_spans
    _all = _source_spans(args.work)
    if _all is not None:
        _want = set(_song_verses(args.work, song))
        src = {v: toks for v, toks in _all.items() if v in _want}
    else:
        n = int(song[1:])
        _src_path = _WORKS.get(args.work, {}).get(
            "source", Path("/root/ipvv/site/data/sanskrit/sivastotravali-u.txt"))
        src = load_gretil_song(_src_path, n)
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
    l3path = data / f"{song}.l3.json"
    l3 = json.loads(l3path.read_text()) if l3path.exists() else None
    if l3 is not None and l3s is not None:
        l2_by_verse = {o["verse"]: o.get("plain_english", "") for o in l2}
        for o in l3:
            errs += l3s.validate(o, f"l3[{o.get('verse_id')}]", l0_ids)
            # register check: L3 must differ from L2 (a copy is a failed L3)
            import re as _re
            lines = o.get("lines", [])
            fe = "\n".join(x for x in lines if isinstance(x, str)) if isinstance(lines, list) else str(o.get("final_english", ""))
            pe = str(l2_by_verse.get(o.get("verse"), ""))
            if fe.strip() and fe.strip() == pe.strip():
                errs.append(f"l3[{o.get('verse_id')}]: identical to L2 (rewrite, don't copy)")
            else:
                def _sents(t):
                    return {s.strip() for s in _re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) >= 30}
                shared = _sents(fe) & _sents(pe)
                if shared:
                    errs.append(f"l3[{o.get('verse_id')}]: shares sentence(s) with L2: {sorted(shared)[:1]}")
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
    if l3 is not None and {o["verse"] for o in l3} != src_verses:
        errs.append(f"coverage l3: {sorted(o['verse'] for o in l3)} != source {sorted(src_verses)}")
    l0_verses = set()
    _vid2verse = {o["verse_id"]: o.get("verse") for o in t1}
    for o in l0:
        vid = o["verse_id"]
        if "-v" in vid:
            try:
                l0_verses.add(int(vid.split("-v")[1]))
                continue
            except ValueError:
                pass
        if vid in _vid2verse and _vid2verse[vid] is not None:
            l0_verses.add(_vid2verse[vid])
        else:
            errs.append(f"coverage l0: unmappable verse_id {vid!r}")
    if l0_verses != src_verses:
        errs.append(f"coverage l0 verses {sorted(l0_verses)} != source {sorted(src_verses)}")

    print(json.dumps({"song": song, "errors": errs,
                      "counts": {"t1": len(t1), "l0": len(l0), "argmap": len(am),
                                 "l2": len(l2), "l3": len(l3) if l3 else 0,
                                 "essence": len(c1.get("essence", [])),
                                 "renders": list(c1.get("renders", {})),
                       "c2_renders": [r.get("style") for r in (c2 or {}).get("renders", [])]
                                  if c2 else [],
                       "signoff": bool(signoff)}}, indent=1))
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
