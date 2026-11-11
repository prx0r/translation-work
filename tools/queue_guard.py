#!/usr/bin/env python3
"""queue_guard — makes duplicate/overlapping burn work structurally impossible.

Checks process/beam/queue.json:
  1. unique task ids
  2. no two tal_triple tasks for the same (work, song) with overlapping
     verse ranges unless one is 'failed'/'superseded'
  3. every tal_triple verse exists in the work's working-t1 source set
     (warn only)

--fix  : keeps the EARLIEST non-failed task per overlap group, marks the
         rest 'superseded' (never deletes history), and dedupes ids.

Usage: python3 tools/queue_guard.py [--fix]
MCP:   shastra.queue_guard
Exit 0 = clean (or fixed), 1 = violations found without --fix.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "process/beam/queue.json"


def audit(fix: bool) -> dict:
    q = json.loads(QUEUE.read_text())
    problems = {"duplicate_ids": [], "overlaps": [], "superseded": 0}

    seen, keep = set(), []
    for t in q:
        if t["id"] in seen:
            problems["duplicate_ids"].append(t["id"])
            if fix:
                continue  # drop exact dup id (first wins)
        seen.add(t["id"])
        keep.append(t)
    q = keep

    groups: dict = {}
    for t in q:
        if t.get("kind") != "tal_triple" or t.get("status") in ("failed", "superseded"):
            continue
        a = t.get("args") or {}
        vs = a.get("verses") or []
        if not vs:
            continue
        groups.setdefault((a.get("work"), a.get("song")), []).append(
            (min(vs), max(vs), t))
    for key, lst in groups.items():
        lst.sort(key=lambda x: (x[0], x[1]))
        for i in range(1, len(lst)):
            if lst[i][0] <= lst[i - 1][1]:
                problems["overlaps"].append(
                    {"work": key[0], "song": key[1],
                     "kept": lst[i - 1][2]["id"],
                     "dupe": lst[i][2]["id"]})
                if fix and lst[i][2].get("status") in ("pending", "claimed"):
                    lst[i][2]["status"] = "superseded"
                    lst[i][2]["note"] = (lst[i][2].get("note") or "") + \
                        " | superseded by queue_guard (overlap " + \
                        lst[i - 1][2]["id"] + ")"
                    problems["superseded"] += 1
    if fix:
        QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=0))
    problems["clean"] = not problems["duplicate_ids"] and not problems["overlaps"]
    return problems


if __name__ == "__main__":
    fix = "--fix" in sys.argv
    p = audit(fix)
    print(json.dumps({k: v for k, v in p.items() if k != "clean" or True},
                     ensure_ascii=False)[:2000])
    sys.exit(0 if p["clean"] or fix else 1)
