#!/usr/bin/env python3
"""beam_review.py — SMART beam reviewer for DUMB beam drafts.

Role split (largetext SKILL): DUMB drafts prose+coverage; SMART checks it.
This is the SMART seat, staffed by beam-free itself — but with HARD limits
that keep it honest (mistakes #20/#24):

  - NEVER approves prose (no pilot_pair / tal_triple / tal_am approvals).
    Approvals stay with auto-review (window briefs, shape-only) + human assessor.
  - May BOUNCE a task, and only with an actionable mechanical note
    (span format, missing verses, flabby question, paraphrase-not-argument,
    bad row naming the surface). Vague notes are rejected.
  - Everything else (soundness, forks, witnesses, PASS) → logged verdict
    for the human assessor; queue untouched.
  - Unparseable reviewer output → escalate, never retry-loop.

Usage:
  python3 tools/beam_review.py --task <id> [--apply]   # single task
  python3 tools/beam_review.py --sweep [--max N] [--apply]  # newest unreviewed dones
Without --apply: dry run (log verdict only).
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT / "tools"))
from beam_swarm import load_q, queue_update  # noqa: E402

RUNS = ROOT / "process" / "beam" / "runs"
LOG = ROOT / "process" / "beam" / "assessor-reviews.jsonl"

META_PHRASES = ["what argument does this passage", "does verse", "this verse",
                "is being told", "what does this passage say"]

SYS = ("You are the SMART checker in a Sanskrit translation swarm. A DUMB "
 "drafter wrote verse-level drafts; you check SHAPE and HONESTY, never meaning "
 "beyond the checklist. You have NO authority to approve. Your verdicts: "
 "'looks-good' (log only), 'needs-fix' (with an ACTIONABLE bounce_note naming "
 "the exact defect and fix), or 'escalate' (genuinely stuck or needs a human). "
 "Bounce notes must name: span format, missing verses, flabby question "
 "(rewrite it), paraphrase-not-argument, or bad row WITH the surface. "
 "Vague notes are rejected. Reply ONLY strict JSON: "
 '{"verdict": "looks-good|needs-fix|escalate", "notes": ["..."], '
 '"bounce_note": "<actionable or empty>"}')


def drafts_for(t: dict) -> dict:
    out: dict = {}
    args = t.get("args", {})
    song = args.get("song", "")
    verses = args.get("verses") or ([args["verse"]] if "verse" in args else [])
    for v in verses:
        for sub in ("gloss", "cm", "am"):
            f = RUNS / f"{song}-{sub}-v{v:02d}" / f"{sub}.json"
            if f.exists():
                try:
                    out[f"v{v:02d}/{sub}"] = json.loads(f.read_text())
                except ValueError:
                    out[f"v{v:02d}/{sub}"] = {"_unparseable": True}
    if not out and t["kind"] == "tal_brief":
        for f in list(RUNS.glob(f"{t['id']}/brief.json")) + list(RUNS.glob(f"{t['id']}*/brief.json")):
            try:
                out[f.parent.name + "/brief"] = json.loads(f.read_text())
            except ValueError:
                pass
    return out


def reviewed_ids() -> set[str]:
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


def check_shapes(t: dict, drafts: dict) -> list[str]:
    """Deterministic pre-check (no model). Returns defect list."""
    bad = []
    for k, d in drafts.items():
        if not k.endswith("/am"):
            continue
        q = d.get("question", "")
        if not (q.endswith("?") and len(q.split()) >= 5):
            bad.append(f"{k}: bad question shape")
        if any(p in q.lower() for p in META_PHRASES):
            bad.append(f"{k}: meta question (about the text, not the matter)")
        if not d.get("premises") or any(len(p.split()) < 3 for p in d["premises"]):
            bad.append(f"{k}: thin premises")
        if not d.get("uncertainties"):
            bad.append(f"{k}: no uncertainties logged")
        if len((d.get("plain_english") or "").split()) < 4:
            bad.append(f"{k}: l2 too short")
    return bad


def _log(task: str, verdict: str, note: str) -> None:
    import time
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "reviewer": "beam-smart", "task": task,
                            "verdict": verdict, "note": note[:500]}) + "\n")


def _apply_bounce(task_id: str, bounce: str) -> str:
    """Requeue one still-DONE task under the worker's shared queue lock."""
    def update(q: list[dict]) -> tuple[list[dict], str]:
        task = next((x for x in q if x.get("id") == task_id), None)
        if task is None:
            return q, "missing"
        # A state change during review wins; do not reset a claimed or otherwise
        # updated task based on an old review snapshot.
        if task.get("status") != "done":
            return q, "changed"
        if task.get("attempts", 0) >= task.get("max_attempts", 3):
            return q, "at-max"
        task["status"] = "pending"
        task["note"] = (task.get("note", "") + " | smart-bounce: " + bounce)[:400]
        task["worker"] = ""
        import datetime
        task["updated"] = datetime.datetime.now().isoformat(timespec="seconds")
        return q, "bounced"

    return queue_update(update)


def review_task(t: dict, apply: bool) -> dict:
    from beam_client import beam
    drafts = drafts_for(t)
    if not drafts:
        r = {"task": t["id"], "verdict": "escalate", "note": "no drafts found"}
        _log(**r)
        return r
    shape_bad = check_shapes(t, drafts)
    sample = {k: v for i, (k, v) in enumerate(drafts.items()) if i < 12}
    user = ("TASK " + t["id"] + " (" + t["kind"] + "). Drafts (sample):\n"
            + json.dumps(sample, ensure_ascii=False)[:7000]
            + "\nDeterministic shape check found: " + (", ".join(shape_bad) or "nothing")
            + ". Do your checklist pass and reply with the verdict JSON.")
    try:
        from beam_client import chat
        import json as _j
        raw = chat([{"role": "system", "content": SYS},
                    {"role": "user", "content": user}],
                   session=f"beam-review-{t['id']}", max_tokens=1500,
                   tries=1, timeout=120)
        text = raw
    except Exception as e:  # noqa: BLE001
        r = {"task": t["id"], "verdict": "escalate",
             "note": f"reviewer call failed: {str(e)[:150]}"}
        _log(**r)
        return r
    a, b = text.find("{"), text.rfind("}")
    try:
        v = json.loads(text[a:b + 1])
        verdict = v.get("verdict", "escalate")
        notes = v.get("notes", [])
        bounce = (v.get("bounce_note") or "").strip()
    except (ValueError, AttributeError):
        r = {"task": t["id"], "verdict": "escalate",
             "note": "reviewer output unparseable"}
        _log(**r)
        return r
    if verdict not in ("looks-good", "needs-fix", "escalate"):
        verdict = "escalate"
    result = {"task": t["id"], "verdict": verdict,
              "note": ("; ".join(notes)[:400]
                       + (f" | bounce: {bounce[:200]}" if bounce else ""))}
    if apply and verdict == "needs-fix" and bounce and len(bounce) >= 10:
        outcome = _apply_bounce(t["id"], bounce)
        if outcome == "bounced":
            result["note"] += " [bounced]"
        elif outcome == "at-max":
            result["note"] += " [at max: left for hand-draft]"
        elif outcome == "changed":
            result["note"] += " [task state changed; left untouched]"
    _log(**result)
    return result


def main() -> int:
    import os
    if not os.environ.get("OPENCODE_GO_KEY"):
        try:
            import subprocess
            r = subprocess.run(["agent-vault", "vault", "credential", "get",
                                "OPENCODE_GO_KEY", "--vault", "oracle"],
                               capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and r.stdout.strip():
                os.environ["OPENCODE_GO_KEY"] = r.stdout.strip()
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--max", type=int, default=3)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    q = load_q()
    if a.task:
        t = next((x for x in q if x["id"] == a.task), None)
        if not t:
            print(json.dumps({"error": f"unknown task {a.task}"}))
            return 1
        print(json.dumps(review_task(t, a.apply), indent=1)[:2000])
        return 0
    seen = reviewed_ids()
    cands = [t for t in q if t.get("status") == "done"
             and t.get("kind") in ("tal_triple", "tal_brief", "tal_am", "tal_gloss", "tal_cm")
             and t["id"] not in seen]
    cands.sort(key=lambda t: t.get("updated", ""), reverse=True)
    out = [review_task(t, a.apply) for t in cands[:a.max]]
    print(json.dumps({"reviewed": len(out),
                      "verdicts": [r["verdict"] for r in out]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
