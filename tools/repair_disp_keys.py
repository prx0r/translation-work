#!/usr/bin/env python3
"""tools/repair_disp_keys.py — one-time migration: work-qualify colliding
proof-disp.json keys, with independent re-verification.

Background: proof-disp.json was keyed by bare song name, but song names like
mukta-m0-p01 / par-p08 exist in multiple works. A disposition verified on
work A's verse N could suppress a genuinely different verse N in work B.

This script, for EVERY disposition entry, recomputes the verdict directly
from the owning work's data (independent of current proof state, so already-
fixed songs are handled correctly):
  - sandhi-only again  -> rewritten under the "work:song" key
  - needs-eyes now     -> FLAGGED for human review, never copied
  - unique song names  -> kept as bare keys (back-compat), re-verified too;
                          dropped with a flag if they no longer verify

proof_record.py accepts "work:song" keys first, bare song keys as fallback.

Usage: python3 tools/repair_disp_keys.py [--apply]
Without --apply: dry run listing every decision.
"""
from __future__ import annotations
import argparse
import difflib
import glob
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import audit_align as AA  # noqa: E402

DISP_PATH = ROOT / "tools" / "proof-disp.json"


def owners() -> dict[str, list[str]]:
    o: dict[str, list[str]] = defaultdict(list)
    for f in sorted(ROOT.glob("*/data/*.t1.json")):
        o[f.name[:-len(".t1.json")]].append(f.parent.parent.name)
    return o


def classify_verse(work: str, song: str, verse: int):
    """Independent verdict for one verse (ignores proof state)."""
    try:
        src, t1 = AA.load_pair(work, song)
    except Exception as e:  # noqa: BLE001
        return ("load-error", str(e)[:120])
    a = "".join(t1.get(verse, []))
    b = "".join(AA._clean(src.get(verse, [])))
    if not a:
        return ("no-t1", "")
    r = difflib.SequenceMatcher(None, AA.P.deparen(a),
                                AA.P.deparen(b)).ratio()
    if r >= 0.90:
        return ("stale-pass", f"ratio={r:.3f}, no disposition needed")
    return AA.classify(AA.P.deparen(a), AA.P.deparen(b)) + (r,)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    disp = json.loads(DISP_PATH.read_text(encoding="utf-8"))
    own = owners()
    decisions = []  # (key, work, verse, action, detail)
    newd: dict = {}
    for song in sorted(disp):
        for v, note in disp[song].items():
            if not isinstance(note, str):
                continue
            verse = int(v)
            ws = sorted(own.get(song, []))
            if len(ws) <= 1:
                w = ws[0] if ws else None
                if w is None:
                    decisions.append((song, "?", v, "ORPHAN-KEY",
                                      "no work has this song; dropping"))
                    continue
                verdict = classify_verse(w, song, verse)
                if verdict[0] == "sandhi-only":
                    newd.setdefault(song, {})[str(verse)] = (
                        note if "2026-11-14" not in note else note)
                    # refresh note to current classifier wording
                    newd[song][str(verse)] = verdict[1]
                    decisions.append((song, w, v, "keep",
                                      verdict[1][:70]))
                elif verdict[0] == "stale-pass":
                    decisions.append((song, w, v, "drop-stale",
                                      verdict[1]))
                else:
                    decisions.append((song, w, v, "FLAG-NEEDS-EYES",
                                      f"{verdict[0]} :: {verdict[1][:100] if len(verdict)>1 else ''}"))
            else:
                for w in ws:
                    verdict = classify_verse(w, song, verse)
                    if verdict[0] == "sandhi-only":
                        newd.setdefault(f"{w}:{song}", {})[str(verse)] = verdict[1]
                        decisions.append((f"{w}:{song}", w, v, "move",
                                          verdict[1][:70]))
                    elif verdict[0] == "stale-pass":
                        decisions.append((f"{w}:{song}", w, v, "drop-stale",
                                          verdict[1]))
                    else:
                        decisions.append((f"{w}:{song}", w, v, "FLAG-NEEDS-EYES",
                                          f"{verdict[0]} :: {verdict[1][:100] if len(verdict)>1 else ''}"))
    from collections import Counter
    print("decisions:", dict(Counter(d[3] for d in decisions)))
    for key, w, v, what, det in decisions:
        if what in ("FLAG-NEEDS-EYES", "ORPHAN-KEY", "drop-stale"):
            print(f"  {what:22s} {key} v{v} {det[:110]}")
    if not a.apply:
        print("(dry run — pass --apply to rewrite proof-disp.json)")
        return 0
    DISP_PATH.write_text(json.dumps(newd, ensure_ascii=False, indent=1) + "\n")
    print(f"rewrote {DISP_PATH} ({len(newd)} keys)")
    # re-proof every touched song
    pairs = set()
    for key, w, v, what, det in decisions:
        if what in ("keep", "move"):
            s = key.split(":", 1)[-1]
            pairs.add((w, s))
    passed, still = [], []
    for (w, s) in sorted(pairs):
        r = subprocess.run([sys.executable, "tools/proof_record.py",
                            "--song", s, "--work", w, "--shastra",
                            "--disp", "tools/proof-disp.json"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=300)
        try:
            g = json.loads(r.stdout[r.stdout.index("{"):])["gate"]
        except (ValueError, KeyError):
            g = f"rc={r.returncode}"
        (passed if g == "PASS" else still).append(f"{w}:{s}={g}")
    print(f"reproof PASS: {len(passed)} | still blocked: {len(still)}")
    for s in still:
        print(f"  STILL {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
