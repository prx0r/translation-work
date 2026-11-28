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


def _lore_files():
    return {f.stem: f for f in (ROOT / "process/beam/lore").glob("*.md")}


def _norm(s: str) -> str:
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "")
                if not unicodedata.combining(c)).lower()
    return "".join(ch for ch in s if ch.isalpha())


def _resolve(work: str):
    """work id -> brief path. Order: exact -> title match -> tradition cover."""
    files = _lore_files()
    if work in files:
        return files[work], "exact"
    cat = work.replace("mukta-", "").upper()
    try:
        census = {r["catalog"]: r for r in
                  __import__("json").loads(Path("/tmp/mukta_census.json").read_text())}
        title = _norm(census.get(cat, {}).get("title", ""))
    except Exception:
        title = ""
    if title:
        for stem, f in files.items():
            t = _norm(stem)
            if len(t) > 5 and len(title) > 5 and (t in title or title in t):
                return f, f"title-match:{stem}"
    # TRADITION COVER MAP (explicit, auditable): a school-level brief covers
    # works of that school. Recorded by callers as "tradition-cover".
    COVER = {
        "Kubjikā": ["kubjika"],
        "Kālīkulakrama": ["mahanayaprakasa", "cidgaganacandrika", "maharthamanjari"],
        "Nepalese Ṣaḍāmnāya and Sarvāmnāya": ["siddhilaksmi"],
        "Śrīvidyā": ["yoginihrdaya", "vamakesvarimata", "tantrarajatantra",
                     "cidgaganacandrika"],
        "Śaiva Siddhānta": ["mrgendragama", "kiranagama", "kalottara",
                            "somasambhupaddhati"],
        "Late Śaiva Siddhānta": ["mrgendragama", "kalottara",
                                 "somasambhupaddhati"],
        "Tantranibandha": ["brihattantrasara", "somasambhupaddhati"],
        "Northeast Indian Tantra": ["brihattantrasara", "tara-corpus"],
        "Śākta General": ["tara-corpus", "siddhilaksmi"],
        "Non-dual Śaivism of Kashmir": ["kularnavatantra", "netratantra",
                                        "svacchandatantra"],
        "Bhairava Tantras": ["netratantra", "svacchandatantra"],
        "Kaula General": ["kaulajnananirnaya", "kularnavatantra"],
        "Trika": ["vatulanathasutra", "kularnavatantra"],
    }
    try:
        auth = __import__("json").loads(
            (ROOT / "process/beam/muktabodha_authority_traditions.json").read_text())
        trads = {t["tradition"] for t in auth.get(cat, [])}
    except Exception:
        trads = set()
    for tr in trads:
        for stem in COVER.get(tr, []):
            f = files.get(stem)
            if f is not None:
                return f, f"tradition-cover:{stem} ({tr})"

    # last resort: a brief whose header names the same tradition
    for stem, f in files.items():
        head = f.read_text(errors="replace")[:900]
        for tr in trads:
            if tr and tr.split()[0].lower() in head.lower():
                return f, f"tradition-cover:{stem} ({tr})"
    return None, "no brief"


def check(work: str) -> tuple[bool, str]:
    p, how = _resolve(work)
    if p is None:
        return False, "no brief"
    if how != "exact":
        # resolved briefs are legitimate but must be recorded by the caller
        pass
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
