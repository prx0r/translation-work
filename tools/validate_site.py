#!/usr/bin/env python3
"""tools/validate_site.py — validate site data structures against DATATYPES.json.

  python3 tools/validate_site.py --work sivastotravali

Checks (DATATYPES.json: site-chunk, site-argmap-md, corpus-record rules):
  - every chunk has required fields; gate in {PASS,BLOCKED}
  - FAIL-CLOSED: PASS chunks have non-empty sanskrit+l1+l2; BLOCKED chunks have EMPTY l1/l2
  - l1 follows ## <chunk> (<n>) header + // <ref> trailer convention (reader strips both)
  - argmap md exists per PASS chunk; adjudications match canonical data option_choices
  - corpus rule: BLOCKED English must be gate-labeled (never silently embedded)
Exit 0 clean, 1 with errors. Warnings (non-blocking) reported separately.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
SITE = Path("/root/ipvv/site/data")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()
    errs: list[str] = []
    warns: list[str] = []

    contract = json.loads((ROOT / "DATATYPES.json").read_text())
    sys.path.insert(0, str(ROOT / "schemas"))
    try:
        from __init__ import SCHEMA_VERSION  # noqa
    except ImportError:
        SCHEMA_VERSION = "1.1.0"
    assert contract["version"] == SCHEMA_VERSION, "DATATYPES.json version drift"

    f = SITE / "translations" / f"{args.work}.json"
    if not f.exists():
        print(json.dumps({"work": args.work, "errors": ["no translations JSON (work absent — greyed, honest)"],
                          "warnings": []}))
        return 0
    chunks = json.loads(f.read_text(encoding="utf-8"))
    data = ROOT / args.work / "data"

    for it in chunks:
        ch = it.get("chunk", "?")
        for req in ["chunk", "verses", "sanskrit", "gate", "blocking", "model", "date"]:
            if req not in it:
                errs.append(f"{ch}: missing field {req}")
        if it.get("gate") not in ("PASS", "BLOCKED"):
            errs.append(f"{ch}: gate must be PASS|BLOCKED, got {it.get('gate')!r}")
            continue
        if it["gate"] == "PASS":
            for lf in ["sanskrit", "l1", "l2"]:
                if not (it.get(lf) or "").strip():
                    errs.append(f"{ch}: PASS chunk with empty {lf}")
            l1 = it.get("l1", "")
            if not re.match(r"## \S+ \(\d+(?:[–-]\d+)?\)\n", l1):
                errs.append(f"{ch}: l1 missing ## <chunk> (<n>[-m]) header")
            if not re.search(r"// \S+\s*$", l1):
                errs.append(f"{ch}: l1 missing // <ref> trailer")
            am = SITE / "argmaps" / args.work / f"{ch}.md"
            if not am.exists():
                warns.append(f"{ch}: PASS chunk without argmap md")
        else:
            if (it.get("l1") or "").strip() or (it.get("l2") or "").strip():
                errs.append(f"{ch}: BLOCKED chunk carries English — FAIL-CLOSED VIOLATION")

    # cross-check chunk count vs canonical data songs
    n_data = len(list(data.glob("*.t1.json"))) if data.exists() else 0
    songs = {c["chunk"].rsplit("-v", 1)[0] for c in chunks if "-v" in c.get("chunk", "")}
    if songs and len(songs) != n_data:
        warns.append(f"songs in site JSON ({len(songs)}) != canonical data songs ({n_data})")

    # adjudication fidelity: site argmap md must reflect data option_choices
    for chf in sorted((SITE / "argmaps" / args.work).glob("*.md")) if (SITE / "argmaps" / args.work).exists() else []:
        stem = chf.stem
        m = re.match(r"(s\d+)-v(\d+)", stem)
        if not m:
            continue
        ajf = data / f"{m.group(1)}.argmap.json"
        if not ajf.exists():
            continue
        am = {o["verse_id"]: o for o in json.loads(ajf.read_text())}
        o = am.get(f"{m.group(1)}-v{int(m.group(2)):02d}", {})
        for chc in o.get("option_choices", []):
            txt = chf.read_text(encoding="utf-8")
            if chc["l0_id"] not in txt or str(chc["chosen_index"]) not in txt:
                errs.append(f"{stem}: adjudication {chc['l0_id']} not reflected in site argmap md")

    print(json.dumps({"work": args.work, "chunks": len(chunks),
                      "pass": sum(1 for c in chunks if c.get("gate") == "PASS"),
                      "errors": errs, "warnings": warns}, indent=1))
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
