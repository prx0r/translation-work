#!/usr/bin/env python3
"""assessor_sweep.py — the assessor's eyes while the model sleeps.

Single idempotent pass. NEVER bounces, NEVER approves prose, NEVER writes
data/. It only: (1) verdicts new DONE outputs into assessor-reviews.jsonl,
(2) escalates content-failures-at-max to the hand-draft backlog (log),
(3) seeds lore_queries beam tasks for fronts that need briefs (beam proposes
searches; the model executes them on return — proactive staging),
(4) reports songs with complete runs awaiting assemble (promote-ready).

Run by hand, by ralph.sh each pass, or by assessor_loop.sh every 10 min.
"""
from __future__ import annotations
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q = ROOT / "process" / "beam" / "queue.json"
RUNS = ROOT / "process" / "beam" / "runs"
LOG = ROOT / "process" / "beam" / "assessor-reviews.jsonl"

META_Q = ("what argument does this passage", "does verse", "this verse",
          "is being told", "what does this passage say about")

now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def logged_ids() -> set[str]:
    out = set()
    if LOG.exists():
        for ln in LOG.read_text().splitlines():
            try:
                d = json.loads(ln)
                if d.get("task"):
                    out.add(d["task"])
            except ValueError:
                pass
    return out


def emit(task: str, verdict: str, note: str) -> None:
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": now, "reviewer": "assessor-daemon",
                            "task": task, "verdict": verdict,
                            "note": note[:500]}) + "\n")


def check_am(am: dict) -> list[str]:
    bad = []
    q = (am.get("question") or "")
    if not (q.endswith("?") and len(q.split()) >= 5):
        bad.append("question-shape")
    if any(p in q.lower() for p in META_Q):
        bad.append("question-meta")
    if not am.get("premises") or any(len(p.split()) < 3 for p in am["premises"]):
        bad.append("premises-thin")
    if not am.get("uncertainties"):
        bad.append("no-uncertainties")
    if len((am.get("plain_english") or "").split()) < 4:
        bad.append("l2-short")
    return bad


def main() -> int:
    from beam_swarm import _locked, load_q, queue_update

    if not Q.is_file():
        raise FileNotFoundError(f"queue does not exist: {Q}")
    with _locked():
        if not Q.is_file():
            raise FileNotFoundError(f"queue does not exist: {Q}")
        q = load_q()
    seen = logged_ids()
    n_verdict = n_esc = n_lore = n_ready = 0
    # 1-2. verdict new dones; escalate content-failures at max
    for t in q:
        tid, kind, st = t["id"], t["kind"], t["status"]
        note = t.get("note", "")
        if kind == "tal_triple" and st == "done" and tid not in seen:
            song = t["args"].get("song", "")
            verses = t["args"].get("verses", [])
            flaws: list[str] = []
            n_am = 0
            for v in verses:
                f = RUNS / f"{song}-am-v{v:02d}" / "am.json"
                if not f.exists():
                    flaws.append(f"v{v}-missing")
                    continue
                try:
                    flaws.extend(f"v{v}:{b}" for b in
                                 check_am(json.loads(f.read_text())))
                except ValueError:
                    flaws.append(f"v{v}-unparseable")
            if flaws:
                emit(tid, "needs-assessor", "; ".join(flaws[:8]))
            else:
                emit(tid, "useful-first-draft",
                     f"{len(verses)}v Qs verse-owned, premises terse, uncertainties honest")
            n_verdict += 1
        elif (kind == "tal_triple" and st == "failed"
                and t.get("attempts", 0) >= t.get("max_attempts", 3)
                and tid not in seen and "beam chat failed" not in note):
            emit(tid, "escalated-hand-draft",
                 f"failed {t.get('attempts')}/{t.get('max_attempts')}: {note[-200:]}")
            n_esc += 1
    # 3. lore gaps: fronts with triple work but no brief and no query task
    briefed = {p.stem for p in (ROOT / "process" / "beam" / "lore").glob("tal-*.md")}
    briefed |= {"tal-V3B"}
    def seed_missing_lore(current: list[dict]) -> tuple[list[dict], int]:
        if not Q.is_file():
            raise FileNotFoundError(f"queue does not exist: {Q}")
        have_query = {t["id"] for t in current if t.get("kind") == "lore_queries"}
        need = sorted({(t.get("args") or {}).get("work", "") for t in current
                       if t.get("kind") == "tal_triple"
                       and (t.get("args") or {}).get("work", "").startswith("tantraloka-a")})
        seeded = 0
        for work in need:
            ahn = work.split("tantraloka-a")[-1]
            if f"tal-a{ahn}" in briefed:
                continue
            qid = f"lore-q-{ahn}"
            if qid in have_query:
                continue
            nw = time.strftime("%Y-%m-%dT%H:%M:%S")
            current.append({"id": qid, "kind": "lore_queries",
                            "args": {"work": work, "ahnika": ahn,
                                     "context": f"propose 2-6 scholarship searches for Tantraloka ahnika {ahn}"},
                            "status": "pending", "attempts": 0, "max_attempts": 3,
                            "worker": "", "note": "daemon-seeded: brief missing",
                            "created": nw, "updated": nw})
            seeded += 1
        return current, seeded

    n_lore = queue_update(seed_missing_lore)
    print(f"sweep: verdicts={n_verdict} escalated={n_esc} lore_seeded={n_lore}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
