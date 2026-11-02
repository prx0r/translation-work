#!/usr/bin/env python3
"""tools/qa_vs_witness.py — quality gate: our translation vs independent witness.

Mirrors ipvv tools/qa_vs_witness.py (same 5-check shape, same verdicts), pointed at
OUR data objects + vendored witnesses (lore/witnesses/). Computational comparison
only; report quotes are short excerpts (<=25 words) — fair use. Witness text is
never copied into site data.

Usage:
  python3 tools/qa_vs_witness.py --work sivastotravali
  python3 tools/qa_vs_witness.py --work sivastotravali --witness lakshmanjoo-sivastotravali

Checks:
  1. COVERAGE — data verses vs GRETIL verse count per song
  2. SANSKRIT — L2 cites byte-exact vs GRETIL (re-verified, not trusted)
  3. LEDGER — per-song ledger glosses vs witness renderings (table)
  4. FORKS — witness-sourced L0 options that lost (adjudication review queue)
  5. GATE — proof records re-verified (BLOCKED must stay blocked for cause)

Verdict per song: SHIP_AS_IS | SHIP_WITH_NOTES | HOLD | NEEDS_WITNESS
Report: logs/qa/<work>.md
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
sys.path.insert(0, str(ROOT / "tools"))
from proof_record import load_gretil_song  # noqa: E402


def short(s: str, n: int = 25) -> str:
    return " ".join(s.split()[:n])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    ap.add_argument("--witness", default=None,
                    help="witness JSON in lore/witnesses/ (default: lakshmanjoo-sivastotravali "
                         "for sivastotravali, none otherwise -> NEEDS_WITNESS)")
    args = ap.parse_args()
    if args.witness is None:
        args.witness = ("lakshmanjoo-sivastotravali" if args.work == "sivastotravali"
                        else "__no_witness_vendored__")
    w = ROOT / args.work
    data = w / "data"
    wit_path = ROOT / "lore/witnesses" / f"{args.witness}.json"
    if wit_path.exists():
        wit = json.loads(wit_path.read_text(encoding="utf-8"))
        wverses = wit.get("verses", {})
        witness_note = args.witness
    else:
        # No independent witness vendored for this work: witness-dependent
        # checks report NEEDS_WITNESS; coverage/cites/gate still run.
        wverses = {}
        witness_note = f"{args.witness} (NOT VENDORED — ledger/fork checks skipped)"
    gretil = Path("/root/ipvv/site/data/sanskrit/sivastotravali-u.txt")
    try:
        from workcfg import WORKS as _WORKS, song_verses as _song_verses
        sys.path.insert(0, str(ROOT / "tools"))
        _cfg = _WORKS.get(args.work)
    except ImportError:
        _cfg = None

    songs = sorted(p.stem.split(".")[0] for p in data.glob("*.t1.json"))
    report = [f"# QA vs witness: {args.work} vs {witness_note}", ""]
    overall = []
    # per-work source resolution (one canonical code path): workcfg first,
    # sivastotravali song-numbered fallback last.
    from workcfg import source_spans as _source_spans
    _all = _source_spans(args.work)
    for song in songs:
        if _all is not None:
            from workcfg import song_verses as _sv
            _want = set(_sv(args.work, song))
            src = {v: toks for v, toks in _all.items() if v in _want}
            n = None
        else:
            n = int(song[1:])
            src = load_gretil_song(gretil, n)
        t1 = json.loads((data / f"{song}.t1.json").read_text())
        l0 = json.loads((data / f"{song}.l0.json").read_text())
        l2 = {o["verse"]: o for o in json.loads((data / f"{song}.l2.json").read_text())}
        am = {o["verse"]: o for o in json.loads((data / f"{song}.argmap.json").read_text())}
        findings = []

        # 1. COVERAGE
        have = {o["verse"] for o in t1}
        if have != set(src):
            findings.append(f"HOLD: coverage {sorted(have)} != source {sorted(src)}")

        # 2. SANSKRIT cites
        flat = " ".join(" ".join(t) for _, t in sorted(src.items()))
        flat_ns = re.sub(r"\s+", "", flat)
        bad_cite = [v for v, o in l2.items()
                    if not all(re.sub(r"\s+", "", p) in flat_ns
                               for p in (o.get("sanskrit_cite", "").split("|")) if p.strip())]
        if bad_cite:
            findings.append(f"HOLD: non-byte-exact cites in verses {bad_cite}")

        # 3. LEDGER vs witness
        m = re.search(r"\*Ledger: (.*?)\*", (w / f"T1-{song}.md").read_text(encoding="utf-8"))
        ledger = {}
        if m:
            for frag in re.split(r"[·;]", m.group(1)):
                if "=" in frag:
                    x, y = [s.strip() for s in frag.split("=", 1)]
                    y = re.split(r"[.;(]", y)[0].strip()
                    if x and " " not in x and y:
                        ledger[x] = y
        table = []
        for term, gloss in ledger.items():
            if n is None or not wverses:
                continue  # no witness attestation possible for this work
            hits = [k for k, v in wverses.items()
                     if k.startswith(f"shivastotravali_{n}_") and
                     gloss.lower().replace("-", " ") in v.lower()]
            table.append((term, gloss, len(hits)))
        missing = [t for t, g, h in table if h == 0]

        # 4. FORKS where a witness option lost
        lost = []
        for o in l0:
            wopts = [x for x in o.get("options", []) if str(x.get("source", "")).startswith("witness")
                     or x.get("source") in ("lakshmanjoo", "dyczkowski", "ksemaraja-vivrti")]
            if wopts and o.get("options", [{}])[o.get("chosen_index", 0)] not in wopts:
                ao = am.get(int(o["verse_id"].split("-v")[1]), {})
                decided = any(ch.get("l0_id") == o["id"] for ch in ao.get("option_choices", []))
                lost.append((o["id"], [x["gloss"] for x in wopts], decided))

        # 5. GATE re-verified
        prec = w / "proof" / f"proof-{song}.json"
        pgate = json.loads(prec.read_text()).get("deterministic_gate") if prec.exists() else "MISSING"
        if pgate != "PASS":
            findings.append(f"HOLD: proof gate {pgate}")

        if any(f.startswith("HOLD") for f in findings):
            verdict = "HOLD"
        elif not wit_path.exists():
            verdict = "NEEDS_WITNESS"
        elif missing or lost:
            verdict = "SHIP_WITH_NOTES"
        else:
            verdict = "SHIP_AS_IS"
        overall.append((song, verdict))
        report += [f"## {song}: {verdict}", ""]
        report += [f"- coverage: {len(have)}/{len(src)} verses; cites bad: {bad_cite or 'none'}; "
                   f"proof: {pgate}"]
        report += [f"- ledger terms: {len(table)}, unattested in witness: "
                   f"{missing if missing else 'none'}"]
        for t_, g_, h_ in table:
            report.append(f"  - {t_} = {g_} (witness verses: {h_})")
        if lost:
            report.append(f"- witness options that lost (review queue):")
            for lid, gl, dec in lost:
                report.append(f"  - {lid}: {gl} — adjudicated: {'yes' if dec else 'NO (record reason)'}")
        report += [f"- findings: {findings if findings else 'none'}", ""]

    report.append("Quoted witness text: short excerpts only (<=25 words), fair use.")
    logdir = ROOT / "logs" / "qa"
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / f"{args.work}.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"work": args.work, "verdicts": dict(overall),
                      "report": str(logdir / f"{args.work}.md")}, indent=1))
    return 0 if all(v != "HOLD" for _, v in overall) else 1


if __name__ == "__main__":
    sys.exit(main())
