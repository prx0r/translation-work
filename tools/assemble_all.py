#!/usr/bin/env python3
"""assemble_all — unattended Pass-1 closer. Runs forever (or until done).

Dynamically discovers EVERY work with a working-t1-<song>.json (no hardcoded
front list), and for each song not yet assembled, checks that every verse has
its gloss+cm+am beam runs. When complete, runs tal_stage (assemble ->
validate -> proof, dispositions honoured) and logs the verdict. Never edits
prose; never seeds (workers do that).

Usage: nohup python3 tools/assemble_all.py --rounds 100000 --sleep 600 &
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "process" / "beam" / "runs"


def discover() -> list[tuple[str, str]]:
    out = []
    for wt in ROOT.glob("*/working-t1-*.json"):
        work = wt.parent.name
        song = wt.name[len("working-t1-"):-len(".json")]
        out.append((work, song))
    return sorted(out)


def song_ready(work: str, song: str) -> tuple[bool, str]:
    try:
        wt = json.loads((ROOT / work / f"working-t1-{song}.json").read_text())
    except Exception:
        return (False, "no working-t1")
    if not wt:
        return (False, "empty working-t1")
    missing = []
    for e in wt:
        v = e["verse"]
        for layer in ("gloss", "cm", "am"):
            if not (RUNS / f"{song}-{layer}-v{v:02d}" / f"{layer}.json").exists():
                missing.append((v, layer))
                break
    return (not missing, f"{len(wt)-len(missing)}/{len(wt)} drafted"
            + (f"; missing {missing[:5]}" if missing else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--sleep", type=int, default=600)
    ap.add_argument("--log", default="/root/assemble_all.log")
    ap.add_argument("--max-fails", type=int, default=3)
    a = ap.parse_args()
    log = open(a.log, "a")
    statep = Path("/root/assemble_all.fails.json")
    try:
        fails = json.loads(statep.read_text())
    except Exception:
        fails = {}

    def bump(work, song, ok):
        key = f"{work}/{song}"
        if ok:
            fails.pop(key, None)
        else:
            fails[key] = fails.get(key, 0) + 1
        try:
            statep.write_text(json.dumps(fails, indent=1))
        except Exception:
            pass
    for rnd in range(a.rounds):
        did = 0
        for work, song in discover():
            data = ROOT / work / "data" / f"{song}.t1.json"
            if data.exists():
                continue
            key = f"{work}/{song}"
            if fails.get(key, 0) >= a.max_fails:
                continue
            ok, msg = song_ready(work, song)
            if not ok:
                continue
            print(f"[r{rnd}] {work}/{song}: {msg} -> assemble", file=log, flush=True)
            try:
                p = subprocess.run(
                    [sys.executable, "tools/tal_stage.py", "--work", work, "--song", song],
                    cwd=ROOT, capture_output=True, text=True, timeout=1800)
                out = (p.stdout + p.stderr)[-400:]
                verdict = "PASS" if "staged, validated, proofed" in out else "BLOCKED"
            except subprocess.TimeoutExpired:
                verdict = "TIMEOUT"
            bump(work, song, verdict == "PASS")
            print(f"[r{rnd}] {work}/{song}: {verdict}"
                  + (f" (fails {fails.get(key,0)}/{a.max_fails})" if verdict != "PASS" else ""),
                  file=log, flush=True)
            did += 1
            time.sleep(2)
        if not did:
            print(f"[r{rnd}] nothing ready; sleeping {a.sleep}s", file=log, flush=True)
        time.sleep(a.sleep)
    print("DONE rounds", file=log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
