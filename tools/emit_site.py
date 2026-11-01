#!/usr/bin/env python3
"""tools/emit_site.py — emit the reader's data structures from canonical JSON.

  python3 tools/emit_site.py --work sivastotravali

Writes (site lane inputs — logged in process/CLAIMS.md for site-lane review):
  /root/ipvv/site/data/translations/<work>.json   (chunks the reader renders)
  /root/ipvv/site/data/argmaps/<work>/<chunk>.md  (critical-view argument maps)

One chunk per verse. gate comes from proof/proof-sXX.json — BLOCKED (or unproven)
verses are emitted with gate BLOCKED and NO English (fail-closed: the reader
withholds English for non-PASS chunks; missing songs are simply absent).
Renders beyond standard are local-only until essence is human-reviewed (T4).
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
SITE = Path("/root/ipvv/site/data")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()
    w = ROOT / args.work
    data = w / "data"
    proofdir = w / "proof"

    with open("/dev/null", "w") as _d:
        pass
    sys.path.insert(0, str(ROOT / "tools"))
    from proof_record import load_gretil_song  # noqa: E402

    gretil = Path("/root/ipvv/site/data/sanskrit/sivastotravali-u.txt")
    chunks = []
    argdir = SITE / "argmaps" / args.work
    argdir.mkdir(parents=True, exist_ok=True)
    songs = 0
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        n = int(song[1:])
        t1 = json.loads(t1f.read_text())
        l2 = {o["verse"]: o for o in json.loads((data / f"{song}.l2.json").read_text())}
        am = {o["verse"]: o for o in json.loads((data / f"{song}.argmap.json").read_text())}
        prec = proofdir / f"proof-{song}.json"
        proof = json.loads(prec.read_text()) if prec.exists() else {"deterministic_gate": "BLOCKED",
                                                                   "blocking": ["no proof record"],
                                                                   "date": "2026-11-01"}
        gate = "PASS" if proof.get("deterministic_gate") == "PASS" else "BLOCKED"
        needs = proof.get("needs", ["human-review"])
        so = data / f"{song}.signoff.json"
        sign = json.loads(so.read_text()) if so.exists() else None
        src = load_gretil_song(gretil, n)
        for v in t1:
            vn = v["verse"]
            vid = f"{song}-v{vn:02d}"
            satext = " ".join(t for t in src.get(vn, []) if t not in ("&",))
            l2o = l2.get(vn, {})
            if gate == "PASS":
                close = " ".join(t["quick_gloss"] for t in v["tokens"])
                l1 = f"## {vid} ({vn})\n{close} // UtSst_{n}.{vn}"
                l2t = (l2o.get("plain_english", "") or "").strip()
            else:
                l1, l2t = "", ""
            ch = {"chunk": vid, "verses": str(vn), "sanskrit": satext,
                  "gate": gate, "blocking": proof.get("blocking", []),
                  "needs": proof.get("needs", ["human-review"]),
                  "model": "crystal-v1", "date": proof.get("date", "2026-11-01"),
                  "l1": l1, "l2": l2t,
                  "links": {"source_file": "site/data/sanskrit/sivastotravali-u.txt",
                            "edition": "GRETIL sa_utpaladeva-zivastotrAvali.txt (Bailly ed.)"}}
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
    # variants file: every token with its options, so the site can show alternative
    # morphology/glosses per word. OUR glosses only — witness text never hosted.
    var = []
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        n = int(song[1:])
        prec = proofdir / f"proof-{song}.json"
        pgate = json.loads(prec.read_text()).get("deterministic_gate") if prec.exists() else "BLOCKED"
        l0 = json.loads((data / f"{song}.l0.json").read_text())
        for o in l0:
            var.append({"chunk": f"{song}-v{int(o['verse_id'].split('-v')[1]):02d}",
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
