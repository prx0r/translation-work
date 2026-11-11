#!/usr/bin/env python3
"""recycle_failed — turn dead triples back into work (halving rule).

Failure classes that are RETRYABLE at a smaller window
(question rejected / premise too short / schema fail / bad row /
surface drift / no JSON) used to die at max_attempts. This recycler
splits them into halves (or 12s if already <=24) and re-queues with
attempts=0, capped so nothing loops forever.

Only tasks whose id does not already start with 'rc2-' are recycled
(one recycle generation); everything else stays failed for the assessor.

Usage: python3 tools/recycle_failed.py [--dry]
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "process/beam/queue.json"
RETRYABLE = ("question rejected", "premise too short", "schema fail",
             "bad row", "surface drift", "no JSON", "l2 too short")


def main() -> int:
    dry = "--dry" in sys.argv
    q = json.loads(QUEUE.read_text())
    have = {t["id"] for t in q}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    live = {}
    for t in q:
        if t.get("kind") == "tal_triple" and t.get("status") not in ("failed", "superseded"):
            a = t.get("args") or {}
            if a.get("verses"):
                live.setdefault((a.get("work"), a.get("song")), []).append(
                    (min(a["verses"]), max(a["verses"])))
    added, recycled, skipped = 0, 0, 0
    for t in q:
        if t.get("kind") != "tal_triple" or t.get("status") != "failed":
            continue
        if t["id"].startswith("rc2-"):
            skipped += 1
            continue
        note = (t.get("note") or "").lower()
        if not any(k in note for k in RETRYABLE):
            skipped += 1
            continue
        a = t.get("args") or {}
        vs = a.get("verses") or []
        if not vs:
            continue
        # skip if the range is already covered by live work (regenerated)
        if all(any(lo <= v <= hi for lo, hi in live.get((a["work"], a["song"]), []))
               for v in vs):
            skipped += 1
            continue
        size = 12 if len(vs) > 12 else len(vs)
        for i in range(0, len(vs), size):
            grp = vs[i:i + size]
            if any(lo <= grp[0] and grp[-1] <= hi for lo, hi in live.get((a["work"], a["song"]), [])):
                continue
            tid = f"rc2-{a['work'][:6]}-{a['song'][-4:]}-v{grp[0]:04d}"
            if tid in have:
                continue
            q.append({"id": tid, "kind": "tal_triple",
                      "args": {"work": a["work"], "song": a["song"], "verses": grp},
                      "status": "pending", "attempts": 0, "max_attempts": 4,
                      "worker": None,
                      "note": f"recycled (halved to {size}) from {t['id']}",
                      "created": now, "updated": now})
            have.add(tid)
            live.setdefault((a["work"], a["song"]), []).append((grp[0], grp[-1]))
            added += 1
        recycled += 1
    if not dry:
        QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=0))
    from collections import Counter
    print(f"recycled {recycled} failed tasks -> {added} halved tasks"
          f" | skipped {skipped} | queue: {dict(Counter(t['status'] for t in q))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
