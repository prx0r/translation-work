#!/usr/bin/env python3
"""tools/mitra_grounds.py — frequency-ranked translation grounds for L0.

Read-only lookup over lore/mitra-trika-subset.jsonl (219 Trika-relevant
headwords distilled from MITRA-lexicon sa-en-by-sa, CC BY-SA 4.0; see
lore/mitra-trika-subset.PROVENANCE.json). Returns ranked senses with
attestation counts + example sentence pairs — the `grounds + source`
shape L0 options require. Unknown headwords return [] (never invented;
full lexicon lives upstream at lexicon.dharmamitra.org).

Usage: python3 tools/mitra_grounds.py <headword> [--top N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBSET = ROOT / "lore" / "mitra-trika-subset.jsonl"
LICENSE = "CC BY-SA 4.0 (MITRA-lexicon sa-en-by-sa slice)"


def _index() -> dict:
    out = {}
    try:
        with SUBSET.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                sa = d.get("sa")
                if isinstance(sa, str):
                    out[sa.casefold()] = d
    except OSError:
        pass
    return out


def grounds(headword: str, top: int = 8) -> list[dict]:
    """Ranked senses for one headword. [] when unknown — never invented."""
    if not isinstance(headword, str) or not headword.strip():
        return []
    d = _index().get(headword.strip().casefold())
    if not d:
        return []
    return [{"en": s.get("en"), "count": s.get("count"),
             "attestations": s.get("ex", [])}
            for s in (d.get("senses") or [])[:max(top, 0)]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("headword")
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args()
    print(json.dumps({"headword": a.headword, "license": LICENSE,
                      "grounds": grounds(a.headword, a.top)},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
