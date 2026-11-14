#!/usr/bin/env python3
"""tools/quota_status.py — beam quota / key-rotation / 429 state, one report.

What this answers: are BOTH Go keys loaded, which models are parked after a
429 and for how long, which worker slots are alive, and whether the loop is
PAUSED. Read-only; never prints secret material (keys are masked).

The beam client (tools/beam_client.py) holds the policy this reports:
  * two zero-price accounts — $OPENCODE_GO_KEY and $OPENCODE_GO_KEY_BAK
    (vault: oracle, fallback .env). Calls are spread across BOTH by a
    session-hash rotation, so ~2x the free-tier headroom.
  * on HTTP 429 we fail over to the OTHER key before ever parking a model;
    a model that still 429s is parked COOLDOWN_SECS (30 min) in the shared
    process/beam/model_health.json, so all workers agree — no hammering.
  * harness health-gates too: if every model is down it writes PAUSED
    (workers drain, no fresh claims) and clears it on recovery.

Usage: python3 tools/quota_status.py [--json]
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _mask(k: str) -> str:
    return (k[:6] + "…" + k[-4:]) if k and len(k) > 12 else ("<set>" if k else "<missing>")


def keys() -> list[str]:
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import beam_client
        return beam_client._keys()
    except Exception:
        ks = [os.environ.get("OPENCODE_GO_KEY", "")]
        ks.append(os.environ.get("OPENCODE_GO_KEY_BAK", ""))
        return [k for k in ks if k]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    ks = keys()
    health_p = ROOT / "process" / "beam" / "model_health.json"
    parked = {}
    if health_p.is_file():
        try:
            h = json.loads(health_p.read_text())
            now = time.time()
            for model, until in (h or {}).items():
                try:
                    left = max(0, int(float(until) - now))
                except (TypeError, ValueError):
                    left = None
                parked[model] = {"until_epoch": until, "seconds_left": left}
        except (OSError, ValueError):
            pass

    # last 429s seen in the usage log (recent window)
    last429 = {}
    usage = ROOT / "process" / "beam" / "model_usage.jsonl"
    if usage.is_file():
        try:
            lines = usage.read_text(encoding="utf-8").splitlines()[-400:]
            for ln in lines:
                try:
                    r = json.loads(ln)
                except ValueError:
                    continue
                if r.get("status") == 429 or r.get("code") == 429:
                    last429[r.get("model", "?")] = r.get("ts")
        except OSError:
            pass

    ps = subprocess.run(["pgrep", "-af", "beam_swarm.py worker"],
                        capture_output=True, text=True).stdout
    workers = sorted({ln.split("worker ")[-1] for ln in ps.splitlines()
                      if "worker " in ln})
    paused = (ROOT / "process" / "beam" / "PAUSED").is_file()
    try:
        free_gb = round(os.statvfs(str(ROOT)).f_bavail *
                        os.statvfs(str(ROOT)).f_frsize / 1e9, 1)
    except OSError:
        free_gb = None

    out = {
        "keys_loaded": len(ks),
        "keys": [_mask(k) for k in ks],
        "rotation": "session-hash across both keys; 429 -> failover to other key, then park model 30m",
        "models_parked": parked,
        "recent_429": last429,
        "workers_alive": len(workers),
        "workers": workers,
        "paused": paused,
        "disk_free_gb": free_gb,
        "note": ("Both keys = ~2x free-tier headroom. A 429 fails over to the "
                 "other key; only if both 429 does the model park 30m and the "
                 "harness set PAUSED until the tier recovers."),
    }
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        print(f"keys loaded: {out['keys_loaded']} ({', '.join(out['keys'])})")
        print(f"workers alive: {out['workers_alive']} {workers}")
        print(f"paused: {paused} | disk_free_gb: {free_gb}")
        print(f"models parked: {parked or 'none'}")
        print(f"recent 429: {last429 or 'none'}")
        print("policy:", out["rotation"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
