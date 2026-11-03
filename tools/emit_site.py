#!/usr/bin/env python3
"""tools/emit_site.py — emit ipvv reader data (sivastotravali-specific, original)."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT.parent / "ipvv/site/data"


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    ap.add_argument("--songs", default="",
                    help="comma list to emit a subset, e.g. s01,s02 (songs whose T1 is genuinely glossed)")
    args = ap.parse_args()
    want = {s.strip() for s in args.songs.split(",") if s.strip()} or None
    w = ROOT / args.work
    data = w / "data"
    proofdir = w / "proof"

    sys.path.insert(0, str(ROOT / "tools"))
    from proof_record import load_gretil_song  # noqa: E402
    from emit_site_general import clean_site_sanskrit, checks_from_proof  # noqa: E402
    try:
        from workcfg import WORKS as _WORKS, song_verses as _song_verses, source_spans as _source_spans
    except ImportError:
        _WORKS = {}

    gretil = ROOT.parent / "ipvv/site/data/sanskrit/sivastotravali-u.txt"
    # prior site output: provenance stamped by trace_translations survives re-emits
    prior = {}
    site_out = SITE / "translations" / f"{args.work}.json"
    if site_out.exists():
        try:
            prior = {c.get("chunk"): c for c in json.loads(site_out.read_text())}
        except Exception:
            prior = {}
    # immutable_id: upstream passage cuts (stotra ranges -> passage id)
    imm_of = {}
    try:
        for line in (w / "passages.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            pr = json.loads(line)
            rng = str(pr.get("verses", ""))
            nums = [int(x) for x in __import__("re").findall(r"\d+", rng)]
            if len(nums) == 1:
                nums = [nums[0], nums[0]]
            for st in range(nums[0], nums[1] + 1):
                imm_of[f"s{st:02d}"] = pr["immutable_id"]
    except Exception:
        imm_of = {}
    chunks = []
    argdir = SITE / "argmaps" / args.work
    argdir.mkdir(parents=True, exist_ok=True)
    songs = 0
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        if want is not None and song not in want:
            continue
        t1 = json.loads(t1f.read_text())
        # workcfg-aware source resolution (non-sivastotravali works use
        # registered spans; sivastotravali keeps its legacy loader verbatim)
        cfg = _WORKS.get(args.work, {}) if _WORKS else {}
        if cfg.get("songs"):
            _all = _source_spans(args.work) or {}
            _want = set(_song_verses(args.work, song))
            src = {v: toks for v, toks in _all.items() if v in _want}
            src_file = str(Path(cfg["source"]))
            ipvv_root = str(ROOT.parent / "ipvv") + "/"
            if src_file.startswith(ipvv_root + "site/data/"):
                src_file = src_file[len(ipvv_root):]
            edition = {"tantrasara-a01": "GRETIL KSTS 17 (Nirnaya Sagara 1918)"}.get(
                args.work, f"GRETIL {Path(cfg['source']).name}")
            ref_of = lambda vn: f"{src_file}:{vn}"  # noqa: E731
            n = None
        else:
            n = int(song[1:])
            src = load_gretil_song(gretil, n)
            src_file = "site/data/sanskrit/sivastotravali-u.txt"
            edition = "GRETIL sa_utpaladeva-zivastotrAvali.txt (Bailly ed.)"
            ref_of = lambda vn: f"UtSst_{n}.{vn}"  # noqa: E731
        l2 = {o["verse"]: o for o in json.loads((data / f"{song}.l2.json").read_text())}
        am = {o["verse"]: o for o in json.loads((data / f"{song}.argmap.json").read_text())}
        l3_path = data / f"{song}.l3.json"
        l3 = {o["verse"]: o for o in json.loads(l3_path.read_text())} if l3_path.exists() else {}
        l4_path = data / f"{song}.l4.json"
        l4 = {o["verse"]: o for o in json.loads(l4_path.read_text())} if l4_path.exists() else {}
        prec = proofdir / f"proof-{song}.json"
        proof = json.loads(prec.read_text()) if prec.exists() else {"deterministic_gate": "BLOCKED",
                                                                   "blocking": ["no proof record"],
                                                                   "date": "2026-11-01"}
        gate = "PASS" if proof.get("deterministic_gate") == "PASS" else "BLOCKED"
        needs = proof.get("needs", ["human-review"])
        so = data / f"{song}.signoff.json"
        sign = json.loads(so.read_text()) if so.exists() else None
        for v in t1:
            vn = v["verse"]
            vid = v.get("verse_id") or f"{song}-v{vn:02d}"
            satext = clean_site_sanskrit(" ".join(t for t in src.get(vn, []) if t not in ("&",)))
            l2o = l2.get(vn, {})
            l3o = l3.get(vn, {})
            l4o = l4.get(vn, {})
            t1o = next((o for o in t1 if o["verse"] == vn), {})
            if gate == "PASS":
                close = " / ".join(t["quick_gloss"] for t in v["tokens"])
                l1 = f"## {vid} ({vn})\n{close} // {ref_of(vn)}"
                l2t = (l2o.get("plain_english", "") or "").strip()
            else:
                l1, l2t = "", ""
            ch = {"chunk": vid, "verses": str(vn), "sanskrit": satext,
                  "checks": checks_from_proof(proof),
                  "gate": gate, "blocking": proof.get("blocking", []),
                  "needs": needs,
                  "model": "crystal-v1", "date": proof.get("date", "2026-11-01"),
                  "l1": l1, "l2": l2t, "license": "FREE",
                  "links": {"source_file": t1o.get("source_file", src_file),
                            "edition": edition,
                            "source_lines": t1o.get("source_lines")}}
            if sign:
                ch["accepted_by"] = sign.get("accepted_by")
                ch["accepted_date"] = sign.get("date")
                ch["accept_scope"] = sign.get("scope")
            if imm_of.get(song):
                ch["immutable_id"] = imm_of[song]
            pv = prior.get(vid, {})
            for pf in ("source_file", "source_license", "source_origin"):
                if pv.get(pf) and not ch.get(pf):
                    ch[pf] = pv[pf]
            if gate == "PASS" and l3o.get("lines"):
                ch["l3"] = "\n".join(x.strip() for x in l3o["lines"] if x.strip())
            if gate == "PASS" and l4o.get("lines"):
                ch["l4"] = "\n".join(x.strip() for x in l4o["lines"] if x.strip())
            chunks.append(ch)
            ao = am.get(vn, {})
            if gate == "PASS" and ao:
                lines = [f"## {vid} — argument map", ""]
                if ao.get("speaker"):
                    lines += [f"**Speaker.** {ao['speaker']}", ""]
                if ao.get("question"):
                    lines += [f"**Question.** {ao['question']}", ""]
                if ao.get("reconstruction"):
                    lines += [f"**Reconstruction.** {ao['reconstruction']}", ""]
                if ao.get("premises"):
                    lines += ["**Premises.**"] + [f"- {p}" for p in ao["premises"]] + [""]
                if ao.get("inference"):
                    lines += [f"**Inference.** {ao['inference']}", ""]
                if ao.get("uncertainties"):
                    lines += ["", "### Open"] + [f"- {u}" for u in ao["uncertainties"]]
                if ao.get("option_choices"):
                    lines += ["", "### Gloss adjudications"]
                    for oc in ao["option_choices"]:
                        lines.append(f"- {oc['l0_id']}: chose option {oc['chosen_index']} "
                                       f"over {', '.join(str(r) for r in oc.get('rejected', []))} — {oc['reason']}")
                amd = argdir / f"{vid}.md"
                if amd.exists():
                    pass      # keep site-lane argmap view (hand-crafted per-verse notes; never clobber)
                else:
                    amd.write_text("\n".join(lines) + "\n", encoding="utf-8")
        songs += 1
    out = SITE / "translations" / f"{args.work}.json"
    out.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    npass = sum(1 for c in chunks if c["gate"] == "PASS")
    print(f"{args.work}: {len(chunks)} chunks ({npass} PASS), {songs} songs -> {out}")
    print(f"argmaps -> {argdir}/ ({len(list(argdir.glob('*.md')))} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
