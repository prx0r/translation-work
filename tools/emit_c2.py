#!/usr/bin/env python3
"""tools/emit_c2.py — ship approved C2 renders to the site in the canonical shape.

  python3 tools/emit_c2.py                    # every REGISTRY-gold work with C2
  python3 tools/emit_c2.py --work kramastotra

Source of truth: data/<song>.c2.json (DATATYPES c2-render: {song, renders[{style,
prompt, paragraphs[{text,maps_to}], model, date}]}), validated by schemas/c2.py
via check.py. Output: ipvv/site/data/c2/<work>.<style>.json:

  {work, style, kind:"c2-song-renders", label, provenance:{source, registry, approval},
   items:[{chunk:<song>, gate, prompt, model, date, paragraphs, text}]}

Fail-closed: only REGISTRY `status:"gold"` works; only songs whose proof says PASS
(the DATATYPES gate: renders are withheld exactly where the stack is withheld);
`text` = paragraphs joined for one-line readers. The REGISTRY note (which carries
the owner's "standing approval" record) travels in provenance — no approval is
invented here.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = Path("/root/ipvv/site/data/c2")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work")
    a = ap.parse_args()
    reg = json.loads((ROOT / "REGISTRY.json").read_text(encoding="utf-8"))
    entries = reg.get("works", []) if isinstance(reg, dict) else []
    by_name = {w.get("work"): w for w in entries if isinstance(w, dict)}

    todo = [a.work] if a.work else [w for w, e in by_name.items()
            if e.get("status") == "gold" and e.get("c2_songs")]
    SITE.mkdir(parents=True, exist_ok=True)
    made, skipped = [], []
    for work in todo:
        entry = by_name.get(work, {})
        files = sorted((ROOT / work / "data").glob("*.c2.json"))
        if not files:
            skipped.append(f"{work}(no c2)")
            continue
        # per-song content + proof gates
        by_style: dict[str, list] = {}
        for f in files:
            song = json.loads(f.read_text(encoding="utf-8")).get("song") or f.name.split(".c2")[0]
            pf = ROOT / work / "proof" / f"proof-{song}.json"
            gate = "BLOCKED"
            if pf.exists():
                gate = json.loads(pf.read_text(encoding="utf-8")).get("deterministic_gate", "BLOCKED")
            for r in json.loads(f.read_text(encoding="utf-8")).get("renders", []):
                style = str(r.get("style") or "").strip()
                paras = r.get("paragraphs") or []
                if not style or not paras or not r.get("prompt"):
                    continue
                if gate != "PASS":
                    continue                     # fail-closed: withheld where the stack is
                by_style.setdefault(style, []).append({
                    "chunk": song, "gate": gate,
                    "prompt": r["prompt"], "model": r.get("model", ""),
                    "date": r.get("date", ""),
                    "paragraphs": paras,
                    "text": "\n\n".join(p.get("text", "") for p in paras if p.get("text")),
                })
        if not by_style:
            skipped.append(f"{work}(nothing shippable)")
            continue
        for style, items in by_style.items():
            out = {"work": work, "style": style, "kind": "c2-song-renders",
                   "label": "prompt-reproducible render over the canonical stack — NOT canonical translation",
                   "provenance": {
                       "source": f"translation-work {work}/data/*.c2.json (DATATYPES c2-render, schemas/c2.py)",
                       "registry": f"REGISTRY status={entry.get('status','?')} c2_songs={entry.get('c2_songs','?')}",
                       "approval": (lambda n: (n[n.index("standing approval"):] if "standing approval" in n else n[-240:]).strip())(entry.get("note", "")),
                       "generated": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
                   "items": items}
            p = SITE / f"{work}.{style}.json"
            p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            made.append(f"{work}.{style}({len(items)})")
    print(f"emit_c2: {len(made)} files -> {SITE}")
    for m in made:
        print(" ", m)
    if skipped:
        print("skipped:", ", ".join(skipped))
    return 0

if __name__ == "__main__":
    sys.exit(main())
