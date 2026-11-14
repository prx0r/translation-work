#!/usr/bin/env python3
"""tools/verify_core.py — re-verify the Trika core from current bytes.

The point (owner 2026-11-14): volume is not the goal; *proving the core is
correct and the pipeline works* is. This tool does NOT trust stored
proof-*.json files. For every REGISTRY work it recomputes each song's
deterministic gate + schema/cross-layer validation from current data, then
reports where reality differs from what is claimed.

Detects, per song:
  REGRESSION   stored gate PASS but recompute BLOCKED  (claimed proof is false)
  IMPROVED     stored BLOCKED but recompute PASS       (stale record)
  GATE-OK      stored PASS == recompute PASS
  STILL-BLOCKED both BLOCKED
  NO-PROOF     data exists, no stored proof
  VALIDATE-ERR validate_song reports schema/cross-layer errors

Also reports: align min-ratio distribution, how many verses lean on a
disposition, and per-work rollups. Writes nothing (proof_record --no-write).

Usage: python3 tools/verify_core.py [--work W] [--json] [--out FILE]
Exit 0 always (a report); the numbers are the point.
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISP = "tools/proof-disp.json"

# Songs whose data exists but which are OUT OF SCOPE for the build (documented
# in REGISTRY): the later Spanda nihṣyandas (only vv1-25 are in scope) and the
# sivasutra extra sutras beyond the 75-sutra Kaul recension. They are not
# defects and carry no proof by design.
OUT_OF_SCOPE = {
    "spanda/span-p04b": "later nihṣyanda; REGISTRY scope = first nihṣyanda vv1-25",
    "spanda/span-p05": "later nihṣyanda; out of scope",
    "spanda/span-p06": "later nihṣyanda; out of scope",
    "sivasutra/span-p09": "sutras 76-77 beyond the 75-sutra Kaul Shastri recension",
}


def registry_works() -> list[str]:
    reg = json.loads((ROOT / "REGISTRY.json").read_text(encoding="utf-8"))
    return sorted({w["work"] for w in reg["works"] if w.get("work")})


def stored_gate(path: Path) -> str | None:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return d.get("deterministic_gate") or d.get("gate")


def stored_mode(path: Path) -> str:
    """Each work was proved in ONE mode: 'shastra' (data JSON) or 'classic'
    (T1-*.md / L2-*.md / c1/ MD files). Recompute in the SAME mode, or the
    comparison is meaningless. Authoritative signal is the proof's own
    lineage: a data-path t1 ⇒ shastra, an MD t1 ⇒ classic. The `mode` field
    is a fallback (older proofs predate it)."""
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "shastra"
    lin = (d.get("lineage") or {}).get("t1", "") or ""
    if "/data/" in lin:
        return "shastra"
    if lin.startswith("T1-") or lin.endswith(".md"):
        return "classic"
    return "shastra" if (d.get("mode") == "shastra") else "classic"


def recompute(work: str, song: str, mode: str) -> tuple[str, list, float]:
    cmd = [sys.executable, "tools/proof_record.py", "--song", song,
           "--work", work, "--no-write", "--disp", DISP]
    if mode == "shastra":
        cmd += ["--shastra"]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=300)
    raw = r.stdout
    i = raw.find("{")
    try:
        d = json.loads(raw[i:])
        return d.get("gate", f"RC{r.returncode}"), d.get("blocking", []), d.get("min_ratio", 0)
    except (ValueError, AttributeError):
        return f"ERR({r.returncode})", [(r.stderr or raw)[-200:]], 0


def validate(work: str, song: str) -> list:
    r = subprocess.run([sys.executable, "tools/validate_song.py", "--song", song,
                        "--work", work], cwd=str(ROOT), capture_output=True,
                       text=True, timeout=300)
    try:
        return json.loads(r.stdout).get("errors", [])
    except ValueError:
        return [f"validator rc={r.returncode}"]


def disp_count(work: str, song: str) -> int:
    try:
        all_d = json.loads((ROOT / DISP).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    d = all_d.get(f"{work}:{song}", all_d.get(song, {}))
    return len(d) if isinstance(d, dict) else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    works = [a.work] if a.work else registry_works()
    rows = []
    ratios = []
    for wi, w in enumerate(works, 1):
        songs = sorted(p.name[:-len(".t1.json")]
                       for p in (ROOT / w / "data").glob("*.t1.json"))
        for s in songs:
            pp = ROOT / w / "proof" / f"proof-{s}.json"
            sg = stored_gate(pp)
            mode = stored_mode(pp)
            fg, blocking, mr = recompute(w, s, mode)
            errs = validate(w, s)
            if f"{w}/{s}" in OUT_OF_SCOPE:
                kind = "OUT-OF-SCOPE"
            elif sg is None:
                kind = "NO-PROOF"
            elif sg == "PASS" and fg != "PASS":
                kind = "REGRESSION"
            elif sg != "PASS" and fg == "PASS":
                kind = "IMPROVED"
            elif fg == "PASS":
                kind = "GATE-OK"
            else:
                kind = "STILL-BLOCKED"
            if errs and kind == "GATE-OK":
                kind = "VALIDATE-ERR"
            ratios.append(mr)
            rows.append({"work": w, "song": s, "stored": sg, "fresh": fg,
                         "kind": kind, "blocking": blocking,
                         "min_ratio": mr, "validate_errors": errs[:3],
                         "dispositions": disp_count(w, s)})
        if wi % 10 == 0:
            print(f"  [{wi}/{len(works)}] works, {len(rows)} songs", file=sys.stderr)

    kinds = Counter(r["kind"] for r in rows)
    ratios.sort()
    def pct(q):
        return ratios[int(q * (len(ratios) - 1))] if ratios else 0
    summary = {
        "works": len(works),
        "songs": len(rows),
        "kinds": dict(kinds),
        "regressions": [f"{r['work']}/{r['song']}" for r in rows if r["kind"] == "REGRESSION"],
        "validate_errors": [f"{r['work']}/{r['song']}: {r['validate_errors']}"
                            for r in rows if r["kind"] == "VALIDATE-ERR"],
        "min_ratio": {"p0": ratios[0] if ratios else 0,
                      "p10": pct(0.10), "p50": pct(0.50), "p90": pct(0.90),
                      "max": ratios[-1] if ratios else 0},
        "verses_on_disposition": sum(r["dispositions"] for r in rows),
        "low_ratio_songs": [{"work": r["work"], "song": r["song"],
                             "ratio": r["min_ratio"], "disp": r["dispositions"]}
                            for r in rows if r["min_ratio"] < 0.95],
    }
    out = {"summary": summary, "rows": rows}
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        print(f"CORE VERIFICATION — {len(works)} works, {len(rows)} songs")
        print("  kinds:", dict(kinds))
        print("  min-ratio  p0=%.3f p10=%.3f p50=%.3f p90=%.3f max=%.3f"
              % (summary["min_ratio"]["p0"], summary["min_ratio"]["p10"],
                 summary["min_ratio"]["p50"], summary["min_ratio"]["p90"],
                 summary["min_ratio"]["max"]))
        print(f"  verses relying on a disposition: {summary['verses_on_disposition']}")
        if summary["regressions"]:
            print("  *** REGRESSIONS (claimed PASS, recompute BLOCKED) ***")
            for x in summary["regressions"]:
                print("   -", x)
        if summary["validate_errors"]:
            print("  validate errors:", summary["validate_errors"][:10])
        lr = summary["low_ratio_songs"]
        print(f"  songs with min-ratio < 0.95: {len(lr)}")
        for x in lr[:20]:
            print(f"   - {x['work']}/{x['song']} r={x['ratio']} disp={x['disp']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
