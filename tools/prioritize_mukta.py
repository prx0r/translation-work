#!/usr/bin/env python3
"""prioritize_mukta — rank the Muktabodha burn list.

Rule (owner): shortest untranslated first; translated-with-most last.
Translatedness T(work) = max(index English count, our machine-complete
flag counts as translated, curated famous-translation estimates).
Rank key: (T, verses). Done-by-us works sink to bottom (skip burn).

Usage: python3 tools/prioritize_mukta.py [--out process/beam/ranked_burn.json]
Reads: /tmp/mukta_census.json, process/beam/mukta_priority_queue.json,
  openpatala availability index (for the 15 title-joins).
Writes: ranked list [{burn_rank, catalog, title, verses, T, T_why}].
"""
from __future__ import annotations
import argparse, json, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Curated famous-English-translation counts (high-confidence only; estimates
# flagged ~. Re-audit against the research matrix when PR-001 lands.)
FAMOUS = {
    "M00167": (50, "~Bhagavadgita: dozens of English renderings"),
    "M00244": (50, "see M00167 (another Gita edition)"),
    "M00330": (50, "see M00167 (another Gita edition)"),
    "M00216": (10, "~Saundaryalahari: many renderings"),
    "M00334": (10, "~Hathayogapradipika: many renderings"),
    "M00067": (5, "~Spandakarika: Dyczkowski/Singh/Hughes et al."),
    "M00271": (5, "~Vijnanabhairava: Singh/Dixon et al."),
    "M00349": (4, "~Sivasutra: Singh/Dyczkowski et al. (+Vimarsini layer)"),
    "M00019": (1, "IPVV: Pandey 1954 English (Karika+Vimarsini, dated); Torella IPK+vrtti 2002 for context; NO modern full rendering"),
    "M00092": (4, "Tantraloka: Dyczkowski 2023 11v complete EN + Gnoli Italian + Lakshmanjoo ch1-4 + Singh 5v"),
    "M00093": (4, "see M00092"),
    "M00160": (1, "MV-mula: Singh/Maheshvarananda selected chs (1,2,12-19,21-23, Indica 2016) only"),
    "M00091": (1, "Svacchanda: Singh ch-VII (prana) only; otherwise untranslated"),
    "M00038": (1, "Netra: Singh ch VII-VIII only; Flood/Wernicke-Olesen full translation IN PROGRESS (unpublished)"),
    "M00271": (3, "Vijnanabhairava: Singh selected + Dixon + Pradipaka (trikashaivism)"),
    "M00163": (1, "Spandanirnaya: Pradipaka translation (trikashaivism)"),
    "M00349": (4, "SivasutraVimarsini: Dyczkowski-era + Singh + Pradipaka Vimarshini translation"),
    "M00505": (2, "Bhairavastava: ours + Pradipaka Bhairavastotram (trikashaivism)"),
    "M00031": (3, "Kularnava: Rai 1983 + Banerji complete EN (seed) + Pandit readings free"),
    "M00349": (3, "Sivasutra: Dyczkowski 1992 Aphorisms + Singh selected + ours"),
    "M00153": (1, "~Tantrasara: partial/excerpt renderings"),
    "M00013": (1, "~Brhattantrasara: excerpt renderings"),
    "M00027": (1, "Kaulajnananirnaya: Magee complete EN (seed)"),
    "M00350": (1, "~Pratyabhijnahrdaya: Singh"),
    "M00154": (1, "~Paratrimsikavivrti: partial renderings"),
    "M00089": (1, "~Stavacintamani: Hanneder-associated work"),
    "M00259": (2, "~Sivasutravimarsini: partial renderings"),
}

def norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(c)).lower()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="process/beam/ranked_burn.json")
    a = ap.parse_args()
    rows = json.load(open("/tmp/mukta_census.json"))
    try:
        q = json.load(open(ROOT / "process/beam/mukta_priority_queue.json"))
        qstat = {o["catalog"]: o["status"] for o in q}
    except Exception:
        qstat = {}
    try:
        ch = {}
        with open(ROOT / "process/beam/curated_hits.jsonl", encoding="utf-8") as f:
            for ln in f:
                try:
                    r = json.loads(ln)
                    ch[r["catalog"]] = r["hits"]
                except Exception:
                    pass
    except Exception:
        ch = {}
    try:
        idx = json.load(open("/root/openpatalaproject/data/corpus/"
                             "translation-availability.json")).get("works", {})
        ixn = {norm(w.get("title", "")): w for w in idx.values()}
    except Exception:
        ixn = {}

    try:
        sev = json.load(open(ROOT / "process/beam/seed_evidence.json"))
    except Exception:
        sev = {}
    out = []
    for r in rows:
        cat = r["catalog"]
        blob = norm(r["title"] + " " + r["file"])
        if any(k in blob for k in ("manjusrimulakalpa", "guhyasamaja",
                                   "sadhanamala", "advayavajra")):
            continue  # out of realm (buddhist; M00652 sricakrasadhanam is
            # Hindu Srividya ritual — keep it)
        st = qstat.get(cat, "queued")
        if "complete" in st:
            T, why = 10 ** 9, "machine-complete by us: skip burn"
        else:
            T, why = 0, "no known translation: unserved"
            w = ixn.get(norm(r["title"]))
            if w and (w.get("has_english") or (w.get("translations") or [])):
                T = max(T, len(w.get("translations") or []) or 1)
                why = "openpatala index: english present"
            if cat in FAMOUS:
                fT, fwhy = FAMOUS[cat]
                if fT >= T:
                    T, why = fT, "curated: " + fwhy
            if cat in ch and ch[cat]:
                # scraped index evidence (Magee PDFs, Dyczkowski pages,
                # Wallis posts): each hit is a real translation artefact
                T = T + len(ch[cat])
                why = (why + f" + {len(ch[cat])} index hits "
                       f"({', '.join(sorted(set(h['source'] for h in ch[cat])))})")
            if cat in sev:
                # bibliographySeed gold evidence (curated 2026-08-10, URLs)
                e = sev[cat]
                add = 3 * e["complete_en"] + max(0, e["n"] - e["complete_en"])
                if add > 0:
                    T = T + add
                    why = why + f" + seed:{e['status']}({add})"
        out.append({"catalog": cat, "title": r["title"], "verses": r["verses"],
                    "T": T, "T_why": why, "tw": st,
                    "prose": r["verses"] == 0})
    # 0-verse prose needs a chunker the verse pipeline lacks: rank it as its
    # own tail track, never ahead of translatable verse texts.
    out.sort(key=lambda o: (o["T"] >= 10 ** 9, o["prose"], o["T"], o["verses"]))
    for i, o in enumerate(out, 1):
        o["burn_rank"] = i
    (ROOT / a.out).write_text(json.dumps(out, ensure_ascii=False, indent=0))
    un = [o for o in out if o["T"] == 0]
    print(f"ranked {len(out)} | untranslated: {len(un)} "
          f"({sum(o['verses'] for o in un)} verses)")
    print("top 12:")
    for o in out[:12]:
        print(f"  {o['burn_rank']:3d}  {o['verses']:5d}v T={o['T']}  "
              f"{o['catalog']:8s}  {o['title'][:44]}")
    print("bottom 5:")
    for o in out[-5:]:
        print(f"  {o['burn_rank']:3d}  {o['verses']:5d}v T={o['T']}  "
              f"{o['catalog']:8s}  {o['title'][:44]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
