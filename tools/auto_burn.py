#!/usr/bin/env python3
"""auto_burn — batch Pass-1 drafting at scale (T1 -> gate -> seed 12v triples).

Runs detached; safe to leave for hours. Skips anything already done
(working-t1 exists / queue has the triple). Free beam only (dual-key).

Usage:
  python3 tools/auto_burn.py --work kularnavatantra --from 6 --to 83
  python3 tools/auto_burn.py --work vijnanabhairava --from 2 --to 6
  python3 tools/auto_burn.py --work svacchandatantra --from 1 --to 56

Per passage: one beam call (labeled verses, <=25v) -> parse to
working-t1-<song>.json -> coverage gate (difflib>=0.85/verse; regen once
on failure with the same labeled input) -> append 12v tal_triple seeds.
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


def load_queue() -> list:
    return json.loads((ROOT / "process/beam/queue.json").read_text())


def save_queue(q: list) -> None:
    (ROOT / "process/beam/queue.json").write_text(
        json.dumps(q, ensure_ascii=False, indent=0))


def seed(q: list, work: str, song: str, verses: list, note: str) -> int:
    have = {t.get("id") for t in q}
    # STRUCTURAL duplicate guard: never seed a range overlapping live work
    taken = []
    for t in q:
        if t.get("kind") != "tal_triple" or t.get("status") in ("failed", "superseded"):
            continue
        a = t.get("args") or {}
        if a.get("work") == work and a.get("song") == song and a.get("verses"):
            taken.append((min(a["verses"]), max(a["verses"])))
    n = 0
    for i in range(0, len(verses), 24):
        grp = verses[i:i + 24]
        if any(grp[0] <= hi and lo <= grp[-1] for lo, hi in taken):
            continue  # overlap: already being/been done
        tid = f"{work[:7]}-triple-{song}-v{grp[0]:03d}"
        if tid in have:
            continue
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        q.append({"id": tid, "kind": "tal_triple",
                  "args": {"work": work, "song": song, "verses": grp},
                  "status": "pending", "attempts": 0, "max_attempts": 4,
                  "worker": None, "note": note, "created": now, "updated": now})
        n += 1
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
    passages = [json.loads(l) for l in open(ROOT / work / "passages.jsonl")]
    passages = [p for p in passages if lo <= int(re.search(r"p(\d+)", p["locator"]).group(1)) <= hi]
    vs = json.loads((ROOT / work / "source/verses.json").read_text())
    q = load_queue()
    for p in passages:
        song = p["locator"]
        t1 = ROOT / work / f"working-t1-{song}.json"
        m = re.match(r"(\d+)-(\d+)$", p["verses"])
        num = [int(x) for x in m.groups()] if m else None
        target = list(range(num[0], num[1] + 1)) if num else []
        if t1.exists():
            ok, bad = coverage(work, song, target)
            if ok:
                n = seed(q, work, song, target, f"auto_burn {song} (T1 pre-existing)")
                if n:
                    save_queue(q)
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
                n = seed(q, work, song, target, f"auto_burn {song} T1 gated")
                save_queue(q)
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
