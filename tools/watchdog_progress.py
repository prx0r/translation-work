#!/usr/bin/env python3
"""watchdog_progress — one JSON line of system health + progress (hourly).

Appended to process/beam/watchdog-progress.jsonl by tw-watchdog.timer and
exposed to ChatGPT as the MCP tool `shastra.progress`.
"""
from __future__ import annotations
import glob, json, shutil, subprocess, sys, time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    q = json.loads((ROOT / "process/beam/queue.json").read_text())
    c = Counter(t["status"] for t in q)
    triples = [t for t in q if t.get("kind") == "tal_triple"]
    fails = Counter()
    for t in triples:
        if t["status"] == "failed":
            n = (t.get("note") or "").lower()
            for k in ("question rejected", "premise too short", "schema fail",
                      "bad row", "surface drift", "no json", "l2 too short"):
                if k in n:
                    fails[k] += 1
                    break
    workers = int(subprocess.run(["bash", "-lc",
                                  "pgrep -fc 'beam_swarm.py worker' || true"],
                                 capture_output=True, text=True).stdout.strip() or 0)
    assembled = {w: len(glob.glob(f"{w}/data/*.t1.json"))
                 for w in ("kularnavatantra", "svacchandatantra", "netratantra",
                           "mukta-m00027", "mukta-m00099")}
    last_call = ""
    try:
        rows = (ROOT / "process/beam/model_usage.jsonl").read_text().strip().splitlines()
        last_call = json.loads(rows[-1])["ts"] if rows else ""
    except Exception:
        pass
    free = shutil.disk_usage("/")
    load = open("/proc/loadavg").read().split()[0]
    mem = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":")[0], ln.split()[1]
        if k in ("MemTotal", "MemAvailable"):
            mem[k] = int(v) // 1024
    rec = {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "queue": {"done": c["done"], "pending": c["pending"],
                     "claimed": c["claimed"], "failed": c["failed"]},
           "failure_classes_top5": dict(fails.most_common(5)),
           "workers_alive": workers, "last_beam_call": last_call,
           "assembled_songs": assembled,
           "uncovered": None,
           "host": {"load1": float(load), "mem_avail_mb": mem.get("MemAvailable"),
                    "disk_free_gb": round(free.free / 1e9, 1)},
           "flags": []}
    if workers == 0 and c["pending"] > 0:
        rec["flags"].append("NO_WORKERS_WITH_PENDING_QUEUE")
    if not last_call:
        rec["flags"].append("NO_BEAM_CALLS_RECORDED")
    if rec["host"]["disk_free_gb"] < 2:
        rec["flags"].append("LOW_DISK")
    if mem.get("MemAvailable", 9999) < 400:
        rec["flags"].append("LOW_MEM")
    print(json.dumps(rec, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
