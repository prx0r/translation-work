#!/usr/bin/env python3
"""assemble_all — unattended Pass-1 closer. Runs forever (or until done).

For each (work, song) in the works list: if every verse of the song has a
triple run, run shastra.assemble (tal_stage + validate + proof). Logs
PASS/BLOCKED/short. Never edits prose; never seeds (workers do that).

Usage: nohup python3 tools/assemble_all.py --rounds 20 &
Works: kularnavatantra (p05-p83), then svacchandatantra (p01-p56),
       netratantra (p01-p17) — extend the list as waves onboard.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "process/beam/runs"


def song_ready(work: str, song: str) -> tuple:
    try:
        wt = json.loads((ROOT / work / f"working-t1-{song}.json").read_text())
    except Exception:
        return (False, "no working-t1")
    need = {e["verse"] for e in wt}
    have = set()
    for f in RUNS.glob(f"**/*{song}*triple.json", recursive=True):
        try:
            d = json.loads(f.read_text())
            for it in d.get("items", []):
                have.add(it.get("verse"))
        except Exception:
            pass
    missing = need - have
    return (not missing, f"{len(need)-len(missing)}/{len(need)} drafted"
            + (f"; missing {sorted(missing)[:5]}" if missing else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--sleep", type=int, default=600)
    a = ap.parse_args()
    plan = [("kularnavatantra", f"kul-p{i:02d}") for i in range(5, 84)] + \
           [("svacchandatantra", f"svacchandatantra-p{i:02d}") for i in range(1, 57)] + \
           [("netratantra", f"netratantra-p{i:02d}") for i in range(1, 18)]
    log = open("/root/assemble_all.log", "a")
    for rnd in range(a.rounds):
        did = 0
        for work, song in plan:
            data = ROOT / work / "data" / f"{song}.t1.json"
            if data.exists():
                continue
            ok, msg = song_ready(work, song)
            if not ok:
                continue
            print(f"[r{rnd}] {work}/{song}: {msg} -> assemble", file=log, flush=True)
            p = subprocess.run([sys.executable, str(ROOT / "mcp_server.py"),
                                "shastra.assemble",
                                json.dumps({"work": work, "song": song})],
                               capture_output=True, text=True, timeout=1800)
            out = (p.stdout + p.stderr)[-400:]
            verdict = "PASS" if "staged, validated, proofed" in out else "BLOCKED"
            print(f"[r{rnd}] {work}/{song}: {verdict}", file=log, flush=True)
            did += 1
            time.sleep(2)
        if not did:
            print(f"[r{rnd}] nothing ready; sleeping", file=log, flush=True)
        time.sleep(a.sleep)
    print("DONE rounds", file=log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
