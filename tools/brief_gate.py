#!/usr/bin/env python3
"""brief_gate — no researched brief, no burn.

A lore file passes only if it contains:
  * a FACTS section  ('## A.' or '## A ' or 'FACTS')
  * a TRAPS section  ('## D.' or 'TRAPS' or '## C.' with traps wording)
  * a Ledger line    ('Ledger (LOCK)' or 'Ledger:')
Scaffold/template briefs fail (they carry 'AUTO-BRIEF' or 'placeholder').
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(work: str) -> tuple[bool, str]:
    p = ROOT / "process/beam/lore" / f"{work}.md"
    if not p.exists():
        return False, "no brief"
    t = p.read_text(errors="replace")
    low = t.lower()
    if "auto-brief" in low or "placeholder" in low:
        return False, "scaffold/placeholder brief"
    facts = "## a." in low or "facts" in low
    traps = "## d." in low or "traps" in low
    led = "ledger (lock)" in low or "ledger:" in low
    if not (facts and traps and led):
        missing = [n for n, ok in (("FACTS", facts), ("TRAPS", traps),
                                   ("LEDGER", led)) if not ok]
        return False, "missing " + ",".join(missing)
    return True, "ok"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: brief_gate.py <work>"); sys.exit(2)
    ok, why = check(sys.argv[1])
    print(("PASS " if ok else "REFUSE ") + sys.argv[1] + ": " + why)
    sys.exit(0 if ok else 1)
