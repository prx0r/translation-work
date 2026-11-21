#!/usr/bin/env python3
"""auto_burn — the BURN: T1 + L0 factory at scale (T1 draft -> gate -> seed
tal_gloss/tal_cm). This is the continuous bulk lane, NOT the full pipeline.

Definition (canonical): **burn = T1 (contract gloss rows) + L0 (per-token
morphology/grounds), at scale, by free beam models.** It stops there on
purpose. Argmap, L2 and C1 need the post-hoc web-searched brief and an
assessor; they are never produced by the burn (see BEAM-FLOW.md). A brief is
therefore NOT required to run the burn — it is written AFTER, from the output.

Runs detached; safe to leave for hours. Skips anything already done
(working-t1 exists / gloss+cm already present / task in queue). Free beam only.
Never seeds triples.

Usage:
  python3 tools/auto_burn.py --work kularnavatantra --from 6 --to 83
  python3 tools/auto_burn.py --work svacchandatantra --from 1 --to 56

Per passage: one beam call (labeled verses, <=25v) -> parse to
working-t1-<song>.json -> coverage gate (difflib>=0.85/verse; regen once
on failure) -> seed per-verse tal_gloss (then tal_cm once gloss lands).
"""
from __future__ import annotations
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from beam_client import chat  # noqa: E402

PROMPT = """Draft T1 pada-glosses for {label}. Gloss EACH labeled verse separately — never merge, never renumber.
{verses}

FORMAT (exact), per verse:
## {song}-v<N>   (N = the VERSE number given)
[gloss](surface) [gloss](surface) ...   (4+ padas per verse, split compounds with +, byte-exact surfaces; mantras kept as-is)
Lowercase-hyphenated glosses. No commentary. Reply ONLY the {n} blocks."""


def sha(b: str) -> str:
    import hashlib
    return hashlib.sha256(b.encode()).hexdigest()[:12]


def seed_locked(work: str, song: str, verses: list, note: str) -> int:
    """Seed under the SHARED queue lock (beam_swarm.queue_update) so a long
    beam call never clobbers concurrent worker claims/completions with a stale
    snapshot (2026-11-13 race fix)."""
    from beam_swarm import queue_update
    box = {'n': 0}
    def _do(tasks):
        box['n'] = seed(tasks, work, song, verses, note)
        return tasks, f'seeded {box["n"]}'
    queue_update(_do)
    return box['n']


def load_queue() -> list:
    return json.loads((ROOT / "process/beam/queue.json").read_text())


def save_queue(q: list) -> None:
    (ROOT / "process/beam/queue.json").write_text(
        json.dumps(q, ensure_ascii=False, indent=0))


def seed(q: list, work: str, song: str, verses: list, note: str) -> int:
    """T1+L0 BURN: seed tal_gloss (T1) + tal_cm (L0) ONLY.

    Never triples. Argmap/L2/C1 need the post-hoc brief and are an assessor
    act (see BEAM-FLOW.md). Seeds gloss first; a verse's cm is seeded only
    once its gloss exists, so the worker never hits 'glosses missing'.
    """
    # NEVER seed a song that already exists as assembled gold in this repo.
    if (ROOT / work / "data" / f"{song}.t1.json").exists():
        print(f"{song}: already assembled — refusing to seed")
        return 0
    have = {t.get("id") for t in q}
    runs = ROOT / "process" / "beam" / "runs"
    ahn = work.split("tantraloka-a")[-1]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    n = 0
    for v in verses:
        gid = f"{song}-gloss-v{v:02d}"
        if not (runs / gid / "gloss.json").exists():
            if gid not in have:
                q.append({"id": gid, "kind": "tal_gloss",
                          "args": {"work": work, "song": song, "verse": v,
                                   "ahnika": ahn, "context": ""},
                          "status": "pending", "attempts": 0, "max_attempts": 3,
                          "worker": None, "note": note, "created": now, "updated": now})
                have.add(gid); n += 1
            continue  # T1 first; cm is seeded next wave once gloss exists
        cid = f"{song}-cm-v{v:02d}"
        if not (runs / cid / "cm.json").exists() and cid not in have:
            q.append({"id": cid, "kind": "tal_cm",
                      "args": {"work": work, "song": song, "verse": v},
                      "status": "pending", "attempts": 0, "max_attempts": 3,
                      "worker": None, "note": note, "created": now, "updated": now})
            have.add(cid); n += 1
    return n


def coverage(work: str, song: str, verses: list) -> tuple:
    vs = json.loads((ROOT / work / "source/verses.json").read_text())
    wt = json.loads((ROOT / work / f"working-t1-{song}.json").read_text())
    bad = []
    for e in wt:
        vtext = re.sub(r"\s+", "", vs[e["verse"] - 1])
        joined = re.sub(r"\s+", "", "".join(t["surface"] for t in e["tokens"])).replace("+", "")
        r = difflib.SequenceMatcher(None, joined, vtext, autojunk=False).ratio()
        if r < 0.85:
            bad.append((e["verse"], round(r, 2)))
    return (not bad, bad)


def run_work(work: str, lo: int, hi: int) -> None:
    # BURN MODE: T1+L0 only. No brief_gate — the brief is written POST-HOC from
    # the machine output and is needed only for argmap/L2/C1 (assessor lane).
    passages = [json.loads(l) for l in open(ROOT / work / "passages.jsonl")]
    passages = [p for p in passages if lo <= int(re.search(r"p(\d+)", p["locator"]).group(1)) <= hi]
    vs = json.loads((ROOT / work / "source/verses.json").read_text())
    for p in passages:
        song = p["locator"]
        t1 = ROOT / work / f"working-t1-{song}.json"
        m = re.match(r"(\d+)-(\d+)$", p["verses"])
        num = [int(x) for x in m.groups()] if m else None
        target = list(range(num[0], num[1] + 1)) if num else []
        if t1.exists():
            ok, bad = coverage(work, song, target)
            if ok:
                n = seed_locked(work, song, target, f"auto_burn {song} (T1 pre-existing)")
                if n:
                    print(f"{song}: seeded {n} (T1 existed)", flush=True)
                continue
        blocks = [f"VERSE {v}: {vs[v-1]}" for v in target]
        prompt = PROMPT.format(label=f"{work} {song}", verses="\n".join(blocks),
                               song=song, n=len(blocks))
        for attempt in (1, 2):
            try:
                out = chat([{"role": "user", "content": prompt}],
                           session=f"auto-burn-{song}-a{attempt}",
                           max_tokens=32000, timeout=900)
            except Exception as e:  # noqa: BLE001
                print(f"{song}: beam error {str(e)[:120]}", flush=True)
                time.sleep(30)
                continue
            if out.count(f"## {song}-v") < len(target) * 0.9:
                print(f"{song}: short output ({out.count(chr(35)*2+' '+song+'-v')}/{len(target)}), retry", flush=True)
                continue
            head = (f"# {work} {song}\n*Source: Muktabodha (IAST, CC BY-NC 4.0). "
                    f"Machine-proposed (auto_burn).*\n\n")
            (ROOT / work / f"T1-{song}.md").write_text(head + out)
            r = subprocess.run([sys.executable, str(ROOT / "tools/spanda_t1_parse.py"),
                                "--work", work, "--song", song],
                               capture_output=True, text=True)
            ok, bad = coverage(work, song, target)
            print(f"{song}: T1 {r.stdout.strip().splitlines()[0] if r.stdout else '?'} "
                  f"cov_ok={ok} bad={bad[:3]}", flush=True)
            if ok:
                n = seed_locked(work, song, target, f"auto_burn {song} T1 gated")
                print(f"{song}: seeded {n}", flush=True)
            break
        time.sleep(2)
    print(f"DONE {work} p{lo:02d}-p{hi:02d}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--from", dest="lo", type=int, required=True)
    ap.add_argument("--to", dest="hi", type=int, required=True)
    a = ap.parse_args()
    run_work(a.work, a.lo, a.hi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
