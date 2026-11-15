#!/usr/bin/env python3
"""burn_status — the BURN dashboard (T1+L0 factory).

Read-only. Reports the canonical burn definition and its live state:
  done      gloss (T1) and cm (L0) run counts on disk
  pending   queued tal_gloss / tal_cm (the burn's only work)
  stray     any pending tal_triple / tal_am (should be 0 in burn mode)
  legacy_am argmap runs left from the old triple era (not growing)
  workers   live beam workers
Exit 0 always; `ok` is false if stray triple/am work is pending.
"""
from __future__ import annotations
import glob
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _alive() -> int:
    r = subprocess.run(["pgrep", "-fc", "beam_swarm.py worker"],
                       capture_output=True, text=True)
    try:
        return int(r.stdout.strip() or 0)
    except ValueError:
        return 0


def _paused() -> bool:
    return (ROOT / "process" / "beam" / "PAUSED").exists()


def main() -> int:
    q = json.loads((ROOT / "process" / "beam" / "queue.json").read_text())
    pend = Counter(t.get("kind") for t in q if t.get("status") in ("pending", "claimed"))
    byst = Counter((t.get("kind"), t.get("status")) for t in q)
    runs = ROOT / "process" / "beam" / "runs"
    gloss = len(glob.glob(str(runs / "*-gloss-v*" / "gloss.json")))
    cm = len(glob.glob(str(runs / "*-cm-v*" / "cm.json")))
    am = len(glob.glob(str(runs / "*-am-v*" / "am.json")))

    works_active = {Path(p).parent for p in glob.glob(str(ROOT / "*" / "working-t1-*.json"))}
    total_verses = 0
    for w in works_active:
        for f in w.glob("working-t1-*.json"):
            try:
                total_verses += len(json.loads(f.read_text()))
            except (OSError, ValueError):
                pass

    stray = {
        "tal_triple": pend.get("tal_triple", 0),
        "tal_am": pend.get("tal_am", 0),
    }
    out = {
        "mode": "BURN = T1 (gloss) + L0 (cm) at scale; argmap/L2/C1 are assessor-lane (brief post-hoc)",
        "done": {"gloss": gloss, "cm": cm, "legacy_am": am},
        "pending": {k: v for k, v in sorted(pend.items())},
        "stray_non_burn_pending": stray,
        "ok": stray["tal_triple"] == 0 and stray["tal_am"] == 0,
        "works_active": len(works_active),
        "total_verses_indexed": total_verses,
        "workers_alive": _alive(),
        "paused": _paused(),
        "queue_by_kind_status": {f"{k[0]}:{k[1]}": v for k, v in sorted(byst.items(), key=str)},
    }
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
