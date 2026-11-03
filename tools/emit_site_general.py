#!/usr/bin/env python3
"""tools/emit_site_general.py — publish non-sivastotravali canonical works to ipvv."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
SITE = Path("/root/ipvv/site/data")


def checks_from_proof(p) -> dict:
    """Batch-style checks dict ([bool, note] pairs) derived from a proof record.
    Receipts gate on this (qp checks-pass); the proof facts already exist — this
    only names them. Batch-supplied checks win when present (ingest shape)."""
    if not isinstance(p, dict):
        return {}
    if p.get("checks"):
        return p["checks"]
    l0 = p.get("l0") or {}
    al = p.get("align") or {}
    cites = p.get("l2_cites") or {}
    dob = p.get("data_objects") or {}
    return {
        "GATE": [p.get("deterministic_gate") == "PASS", str(p.get("deterministic_gate"))],
        "L0_PARSED": [l0.get("failed", 1) == 0,
                      f"{l0.get('parsed', 0)} parsed, {l0.get('failed', 0)} failed"],
        "ALIGNMENT": [float(al.get("min_ratio", 0)) >= 0.9 and not al.get("sub090"),
                      f"min_ratio={al.get('min_ratio', '?')}"],
        "L2_CITES": [cites.get("checked", 0) > 0 and not cites.get("failures"),
                     f"{cites.get('checked', 0)} cites, {len(cites.get('failures') or [])} failures"],
        "C1_NO_QUOTES": [p.get("c1_quotes", 1) == 0, f"{p.get('c1_quotes', '?')} quotes"],
        "C1_NO_SHARED": [not p.get("c1_l2_shared"),
                         f"{len(p.get('c1_l2_shared') or [])} shared-with-L2"],
        "C1_NO_METACOMMENTARY": [not p.get("c1_metacommentary"),
                                 f"{len(p.get('c1_metacommentary') or [])} metacomments"],
        "DATA_OBJECTS": [not dob.get("errors"), f"{len(dob.get('errors') or [])} errors"],
    }


def clean_site_text(s: str) -> str:
    """Site display text: strip trailing translator fidelity footer
    (*Fidelity: ... Added: ... Not-resolved: ...) — provenance that lives
    in translation-work data + proof records, not in the reading lane."""
    return re.sub(r"\s*\*Fidelity:.*$", "", s or "", flags=re.S).strip()


def clean_site_sanskrit(s: str) -> str:
    """Drop trailing source-sigil tails (e.g. '|| AgAna_5'), bare verse-number
    brackets ('[1]'), '+' sandhi-join markers, TeX apparatus ('\\var{...}',
    '\\em', '(?)') that some source rows carry — the locator/edition fields
    hold provenance."""
    s = re.sub(r"\\[A-Za-z]+(\{[^{}]*\})?", "", s or "")
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\(\?\)", "", s)
    s = re.sub(r"\|\|\s*[A-Za-z][A-Za-z0-9_'\-]*\s*$", "", s).strip()
    s = re.sub(r"\s*\[\d+\]", "", s)
    return s.replace("+", "").strip()


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
    ap.add_argument("--work", required=True)
    ap.add_argument("--force", action="store_true",
                    help="overwrite site-lane l1/l2 hand fixes (default: preserve them)")
    args = ap.parse_args()
    w = ROOT / args.work
    data = w / "data"
    proofdir = w / "proof"
    passages = load_passages(args.work)
    # site-lane hand fixes (translations JSON edited after emit) are preserved
    # unless --force: regenerating T1/L2 must never silently wipe review.
    prior = {}
    site_out = SITE / "translations" / f"{args.work}.json"
    if site_out.exists() and not args.force:
        try:
            for c in json.loads(site_out.read_text()):
                prior[c.get("chunk")] = c
        except Exception:
            prior = {}

    # FAIL-SAFE: some works' site data is owned by ipvv's ingest_batch producer
    # (song-grained chunks with en_variants/checks/styles). Rewriting those with
    # this emitter destroys their fields and granularity — refuse loudly.
    if prior and any(("en_variants" in c or "ahnika" in c) for c in prior.values()):
        print(f"REFUSING {args.work}: site data is ingest-shaped (en_variants/ahnika) — "
              "produced by ipvv tools/ingest_batch.py, not this emitter")
        return 2
    chunks = []
    argdir = SITE / "argmaps" / args.work
    argdir.mkdir(parents=True, exist_ok=True)
    c1dir = SITE / "c1" / args.work
    c1dir.mkdir(parents=True, exist_ok=True)
    songs = 0
    for t1f in sorted(data.glob("*.t1.json")):
        song = t1f.stem.split(".")[0]
        t1 = json.loads(t1f.read_text())
        l2_path = data / f"{song}.l2.json"
        am_path = data / f"{song}.argmap.json"
        c1_path = data / f"{song}.c1.json"
        l2 = {o["verse"]: o for o in json.loads(l2_path.read_text())} if l2_path.exists() else {}
        am = {o["verse"]: o for o in json.loads(am_path.read_text())} if am_path.exists() else {}
        l3_path = data / f"{song}.l3.json"
        l3 = {o["verse"]: o for o in json.loads(l3_path.read_text())} if l3_path.exists() else {}
        l4_path = data / f"{song}.l4.json"
        l4 = {o["verse"]: o for o in json.loads(l4_path.read_text())} if l4_path.exists() else {}
        prec = proofdir / f"proof-{song}.json"
        if not prec.exists():
            # fallback: by index among sorted proof files — ONLY when counts
            # match 1:1 (else indices misalign and a verse inherits another
            # verse's proof: anu-p02 would PASS on anu-p05's record).
            # Otherwise fail closed: no proof record -> BLOCKED below.
            t1files = sorted(data.glob("*.t1.json"))
            cands = sorted(proofdir.glob("proof-*.json"))
            if len(cands) == len(t1files):
                idx = t1files.index(t1f)
                if idx < len(cands):
                    prec = cands[idx]
        proof = json.loads(prec.read_text()) if prec.exists() else {"deterministic_gate": "BLOCKED",
                                                                   "blocking": ["no proof record"],
                                                                   "date": "2026-11-01"}
        gate = "PASS" if proof.get("deterministic_gate") == "PASS" else "BLOCKED"
        needs = proof.get("needs", ["human-review"])
        so = data / f"{song}.signoff.json"
        sign = json.loads(so.read_text()) if so.exists() else None
        psg = passages.get(song, {})
        if not psg and len(passages) == 1:
            # single-passage work (e.g. tantrasara-a01: locator tsa01-p01 vs
            # song tsa-a01) — one row covers every verse of the one song
            psg = next(iter(passages.values()))
        src_text = clean_site_sanskrit(psg.get("sanskrit", ""))  # passage-level (song) — kept for passage-grained chunks
        for v in t1:
            vn = v["verse"]
            vid = v["verse_id"]
            l2o = l2.get(vn, {})
            l3o = l3.get(vn, {})
            l4o = l4.get(vn, {})
            t1o = next((o for o in t1 if o["verse"] == vn), {})
            if gate == "PASS":
                close = " / ".join(t["quick_gloss"] for t in v["tokens"])
                l1 = f"## {vid} ({vn})\n{close} // {psg.get('locator', song)}"
                if len(t1) == 1 and len(l2) > 1:
                    # passage-grained song: one T1 record spans the passage but
                    # L2 is per verse — join all verses so the chunk's English
                    # covers its Sanskrit (ghatakarpara, spandasandoha)
                    try:
                        order = sorted(l2, key=lambda x: int(str(x)))
                    except (ValueError, TypeError):
                        order = sorted(l2, key=str)
                    l2t = clean_site_text("\n\n".join(
                        (l2[k].get("plain_english") or "").strip() for k in order))
                else:
                    l2t = clean_site_text((l2o.get("plain_english") or "").strip())
            else:
                l1, l2t = "", ""
            # preserve site-lane hand fixes (translation review applied after emit)
            prev = prior.get(vid, {})
            if prev and (prev.get("l1", "") != l1 or prev.get("l2", "") != l2t):
                print(f"  keep site-lane l1/l2 for {vid} (hand-fixed; --force to overwrite)")
                l1, l2t = prev.get("l1", ""), prev.get("l2", "")
            # verse-grained songs: each chunk shows ITS OWN verse, not the whole
            # song (sanskrit_cite is the verse's verbatim source; song-level text
            # only when one T1 record spans the passage)
            verse_sa = src_text
            if len(t1) > 1:
                cite = (l3o.get("sanskrit_cite") or l2o.get("sanskrit_cite") or "").strip()
                if cite:
                    verse_sa = clean_site_sanskrit(cite)
            ch = {"chunk": vid, "verses": str(vn), "sanskrit": verse_sa,
                  "checks": checks_from_proof(proof),
                  "gate": gate, "blocking": proof.get("blocking", []),
                  "needs": needs,
                  "model": "crystal-v1", "date": proof.get("date", "2026-11-01"),
                  "l1": l1, "l2": l2t,
                  "source_file": t1o.get("source_file", "passages.jsonl"),
                  "links": {"source_file": t1o.get("source_file", "passages.jsonl"),
                            "edition": psg.get("source_edition", "canonical"),
                            "source_lines": t1o.get("source_lines")}}
            if sign:
                ch["accepted_by"] = sign.get("accepted_by")
                ch["accepted_date"] = sign.get("date")
                ch["accept_scope"] = sign.get("scope")
            if psg.get("immutable_id"):
                ch["immutable_id"] = psg["immutable_id"]
            for pf in ("source_file", "source_license", "source_origin"):
                if prev.get(pf) and not ch.get(pf):
                    ch[pf] = prev[pf]
            ch["license"] = "FREE"   # OUR English translation: free use (scholar words are (c))
            if gate == "PASS" and l3o.get("lines"):
                ch["l3"] = "\n".join(x.strip() for x in l3o["lines"] if x.strip())
            # L4 = the canonical svatantrya translation (song layer, subset of L3)
            if gate == "PASS" and l4o.get("lines"):
                ch["l4"] = "\n".join(x.strip() for x in l4o["lines"] if x.strip())
            # source_license: deliberately NOT defaulted — needs per-edition
            # legal decision (GRETIL/Muktabodha/KSTS differ). verify_site will
            # keep flagging it until the owner sets it. See CHAT.md gap log.
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
                                     f"over {', '.join(oc.get('rejected', []))} — {oc['reason']}")
                amd = argdir / f"{vid}.md"
                if not args.force and amd.exists():
                    pass          # keep the site-lane argmap view (hand-written; --force to re-emit)
                else:
                    amd.write_text("\n".join(lines) + "\n", encoding="utf-8")
        # C1: pristine display (SUMMARY + rasa) + scholar NOTE alongside.
        # ONE copy per song, attached to the song's first verse (single-verse
        # songs unchanged: vid == song). Data never duplicates the essay;
        # svread's c1 lane fans it out to the song's other verses.
        first_vid = t1[0].get("verse_id") or vid
        if c1_path.exists():
            c1 = json.loads(c1_path.read_text())
            std = ((c1.get("renders") or {}).get("standard") or {}).get("sections") or {}
            summ = (std.get("SUMMARY") or "").strip()
            rasa = c1.get("rasa") or {}
            clines = [f"## {first_vid} — C1", ""]
            if summ:
                clines += [f"**SUMMARY.** {summ}", ""]
            if rasa.get("dominant"):
                clines += [f"*Rasa: {rasa.get('dominant','')}"
                           + (f" — {rasa.get('justification','')}" if rasa.get("justification") else "")
                           + "*", ""]
            if len(clines) > 2:
                (c1dir / f"{first_vid}.md").write_text("\n".join(clines), encoding="utf-8")
            notef = data / f"{song}.c1.NOTE.md"
            if notef.exists():
                (c1dir / f"{first_vid}.NOTE.md").write_text(notef.read_text(encoding="utf-8"),
                                                     encoding="utf-8")
        songs += 1
    out = SITE / "translations" / f"{args.work}.json"
    out.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    npass = sum(1 for c in chunks if c["gate"] == "PASS")
    print(f"{args.work}: {len(chunks)} chunks ({npass} PASS), {songs} songs -> {out}")
    print(f"argmaps -> {argdir}/ ({len(list(argdir.glob('*.md')))} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
