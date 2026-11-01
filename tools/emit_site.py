#!/usr/bin/env python3
"""tools/emit_site.py — emit ipvv reader data from canonical JSON (work-agnostic).

  python3 tools/emit_site.py --work <work>

Writes:
  /root/ipvv/site/data/translations/<work>.json
  /root/ipvv/site/data/argmaps/<work>/<chunk>.md
  /root/ipvv/site/data/variants/<work>.json
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
SITE = Path("/root/ipvv/site/data")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def load_passages(work: str) -> dict:
    out = {}
    p = ROOT / work / "passages.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            o = json.loads(line)
            out[o["locator"]] = o
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()
    w = ROOT / args.work
    data = w / "data"
    proofdir = w / "proof"
    passages = load_passages(args.work)

    chunks = []
    argdir = SITE / "argmaps" / args.work
    argdir.mkdir(parents=True, exist_ok=True)
    songs = 0
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        t1 = json.loads(t1f.read_text())
        l2_path = data / f"{song}.l2.json"
        am_path = data / f"{song}.argmap.json"
        l2 = {o["verse"]: o for o in json.loads(l2_path.read_text())} if l2_path.exists() else {}
        am = {o["verse"]: o for o in json.loads(am_path.read_text())} if am_path.exists() else {}
        prec = proofdir / f"proof-{song}.json"
        proof = json.loads(prec.read_text()) if prec.exists() else {"deterministic_gate": "BLOCKED",
                                                                   "blocking": ["no proof record"],
                                                                   "date": "2026-11-01"}
        gate = "PASS" if proof.get("deterministic_gate") == "PASS" else "BLOCKED"
        needs = proof.get("needs", ["human-review"])
        so = data / f"{song}.signoff.json"
        sign = json.loads(so.read_text()) if so.exists() else None
        psg = passages.get(song, {})
        src_text = psg.get("sanskrit", "")
        for v in t1:
            vn = v["verse"]
            vid = v["verse_id"]
            l2o = l2.get(vn, {})
            t1o = next((o for o in t1 if o["verse"] == vn), {})
            if gate == "PASS":
                close = " / ".join(t["quick_gloss"] for t in v["tokens"])
                l1 = f"## {vid} ({vn})\n{close}"
                l2t = (l2o.get("plain_english", "") or "").strip()
            else:
                l1, l2t = "", ""
            ch = {"chunk": vid, "verses": str(vn), "sanskrit": src_text if not isinstance(src_text, str) else src_text,
                  "gate": gate, "blocking": proof.get("blocking", []),
                  "needs": needs,
                  "model": "crystal-v1", "date": proof.get("date", "2026-11-01"),
                  "l1": l1, "l2": l2t,
                  "links": {"source_file": t1o.get("source_file", f"passages.jsonl"),
                            "edition": psg.get("source_edition", "canonical"),
                            "source_lines": t1o.get("source_lines")}}
            if sign:
                ch["accepted_by"] = sign.get("accepted_by")
                ch["accepted_date"] = sign.get("date")
                ch["accept_scope"] = sign.get("scope")
            chunks.append(ch)
            ao = am.get(vn, {})
            if gate == "PASS" and ao:
                lines = [f"## {vid} — argument map", "",
                         ao.get("reconstruction", "") or
                         " ".join(ao.get("premises", []))]
                if ao.get("uncertainties"):
                    lines += ["", "### Open"] + [f"- {u}" for u in ao["uncertainties"]]
                if ao.get("option_choices"):
                    lines += ["", "### Gloss adjudications"]
                    for oc in ao["option_choices"]:
                        lines.append(f"- {oc['l0_id']}: chose option {oc['chosen_index']} "
                                     f"over {', '.join(oc.get('rejected', []))} — {oc['reason']}")
                (argdir / f"{vid}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        songs += 1
    out = SITE / "translations" / f"{args.work}.json"
    out.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    npass = sum(1 for c in chunks if c["gate"] == "PASS")
    print(f"{args.work}: {len(chunks)} chunks ({npass} PASS), {songs} songs -> {out}")
    print(f"argmaps -> {argdir}/ ({len(list(argdir.glob('*.md')))} files)")
    # variants
    var = []
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        prec = proofdir / f"proof-{song}.json"
        pgate = json.loads(prec.read_text()).get("deterministic_gate") if prec.exists() else "BLOCKED"
        l0 = json.loads((data / f"{song}.l0.json").read_text())
        for o in l0:
            var.append({"chunk": o["verse_id"],
                        "l0_id": o["id"], "surface": o.get("surface", ""),
                        "citation": o.get("citation", ""), "morph": o.get("morph", ""),
                        "fork": o.get("fork", "none"), "status": o.get("status", ""),
                        "gate": pgate,
                        "chosen": (o.get("options", [{}])[o.get("chosen_index", 0)].get("gloss", "")
                                   if o.get("options") else ""),
                        "options": [{"gloss": x.get("gloss", ""), "rank": x.get("rank", 0),
                                     "source": x.get("source", ""), "grounds": x.get("grounds", "")}
                                    for x in o.get("options", [])]})
    vdir = SITE / "variants"
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / f"{args.work}.json").write_text(json.dumps(var, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    print(f"variants -> {vdir / (args.work + '.json')} ({len(var)} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
