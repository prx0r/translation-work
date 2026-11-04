#!/usr/bin/env python3
"""tools/render_c2.py — prompt-driven C2 renders: prompt out, render in, validated.

The cool thing, made concrete: a new reading is just a prompt. Flow:
  1. BUILD the grounded prompt:  python3 tools/render_c2.py --song s01 --style genz --print-prompt
     (starter styles: eli5, genz. Anything else: --style <name> --prompt "..." | --prompt-file F)
  2. RUN it anywhere (model, user, agent). Model tags each paragraph with essence
     indices like [E0] [E2]. Tag protocol is in the prompt itself.
  3. INGEST the output:   python3 tools/render_c2.py --song s01 --style genz --text-file out.txt
     Parses tags -> maps_to, validates (schemas/c2.py), merges into data/<song>.c2.json.
     Fail-closed: untagged/out-of-range paragraphs -> .draft file + error, never canonical.
  4. --run tries hermes -z directly; on failure it writes the prompt file and stops
     cleanly (never fabricates a render).

Essence comes from data/<song>.c1.json. Context is frozen layers only (L2 + C1 SUMMARY).
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STARTERS = {
    "eli5": ("Explain the argument of this song as if to a bright 10-year-old.",
             "Short words. Concrete images. No jargon, no Sanskrit terms, no meta-commentary."),
    "genz": ("Render the argument of this song in a Gen-Z voice: direct, a little feral, "
             "zero cringe, no slang overload.",
             "Keep every doctrinal claim intact — voice changes, content does not. "
             "No new doctrines, no comparisons, no meta-commentary, no quoted terms."),
}


def build_prompt(work: str, song: str, style: str, user_prompt: str) -> tuple[str, list[str]]:
    w = ROOT / work
    c1 = json.loads((w / "data" / f"{song}.c1.json").read_text(encoding="utf-8"))
    l2 = json.loads((w / "data" / f"{song}.l2.json").read_text(encoding="utf-8"))
    essence = c1["essence"]
    ess_txt = "\n".join(f"[E{i}] {e}" for i, e in enumerate(essence))
    l2_txt = "\n".join(f"(v{o['verse']}) {o['plain_english']} // {o['sanskrit_cite']}" for o in l2)
    summary = (c1.get("renders", {}).get("standard", {}).get("sections", {}).get("SUMMARY", ""))
    return (f"{user_prompt}\n\nUse ONLY the claims in the ESSENCE list below. Output one paragraph "
            f"per idea, separated by blank lines. End EACH paragraph with its essence tags like "
            f"[E0] or [E0] [E2] (every paragraph needs at least one tag, tags only from the list).\n\n"
            f"ESSENCE:\n{ess_txt}\n\nL2 (plain-English grounding, do not contradict):\n{l2_txt}\n\n"
            f"C1 SUMMARY (register reference):\n{summary}\n", essence)


def parse_render(text: str, n_essence: int) -> tuple[list[dict], list[str]]:
    paras, problems = [], []
    for raw in re.split(r"\n\s*\n", text.strip()):
        p = raw.strip()
        if not p:
            continue
        tags = sorted({int(x) for x in re.findall(r"\[E(\d+)\]", p)})
        body = re.sub(r"\s*\[E\d+\]", "", p).strip()
        bad = [t for t in tags if not (0 <= t < n_essence)]
        if bad:
            problems.append(f"out-of-range tags {bad} in: {body[:70]}")
        if not tags:
            problems.append(f"untagged paragraph (rejected): {body[:70]}")
            continue
        if not body:
            problems.append("empty paragraph after tag strip")
            continue
        paras.append({"text": body, "maps_to": tags})
    if not paras:
        problems.append("no valid paragraphs parsed")
    return paras, problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True)
    ap.add_argument("--style", required=True, help="eli5 | genz | custom name")
    ap.add_argument("--prompt", default=None)
    ap.add_argument("--prompt-file", default=None)
    ap.add_argument("--print-prompt", action="store_true")
    ap.add_argument("--text-file", default=None, help="model output to ingest")
    ap.add_argument("--run", action="store_true", help="try hermes -z directly")
    ap.add_argument("--model", default="crystal-v1")
    ap.add_argument("--work", default="sivastotravali")
    ap.add_argument("--date", default="2026-11-01")
    args = ap.parse_args()

    if args.style in STARTERS and not (args.prompt or args.prompt_file):
        head, tail = STARTERS[args.style]
        user_prompt = f"{head} {tail}"
    elif args.prompt:
        user_prompt = args.prompt
    elif args.prompt_file:
        user_prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        print("custom style needs --prompt or --prompt-file", file=sys.stderr)
        return 2

    prompt, essence = build_prompt(args.work, args.song, args.style, user_prompt)
    w = ROOT / args.work

    if args.print_prompt and not args.text_file and not args.run:
        print(prompt)
        return 0

    if args.run and not args.text_file:
        try:
            r = subprocess.run(["hermes", "-z", prompt, "-m", "mimo-v2.5",
                                "--provider", "opencode-go"],
                               capture_output=True, text=True, timeout=600)
            out = (r.stdout or "").strip()
            if not out:
                raise RuntimeError(f"empty model output (stderr: {r.stderr[:200]})")
        except Exception as e:
            pf = w / f"c2-{args.song}-{args.style}.prompt.md"
            pf.write_text(prompt, encoding="utf-8")
            print(f"model call failed ({e}); prompt saved to {pf} — run it anywhere, "
                  f"then ingest with --text-file", file=sys.stderr)
            return 3
    elif args.text_file:
        out = Path(args.text_file).read_text(encoding="utf-8")
    else:
        print("nothing to ingest: use --text-file or --run", file=sys.stderr)
        return 2

    paras, problems = parse_render(out, len(essence))
    if problems:
        dp = w / f"c2-{args.song}-{args.style}.draft.md"
        dp.write_text(out, encoding="utf-8")
        print(json.dumps({"song": args.song, "style": args.style, "accepted": False,
                          "problems": problems, "draft": str(dp)}, indent=1))
        return 1

    sys.path.insert(0, str(ROOT / "schemas"))
    import c2 as c2s  # noqa: E402
    c2p = w / "data" / f"{args.song}.c2.json"
    c2 = json.loads(c2p.read_text()) if c2p.exists() else {"song": args.song, "renders": []}
    c2["renders"] = [r for r in c2.get("renders", []) if r.get("style") != args.style]
    c2["renders"].append({"style": args.style, "prompt": user_prompt, "model": args.model,
                           "date": args.date, "status": "machine-proposed",
                           "paragraphs": paras})
    errs = c2s.validate(c2, "c2", len(essence))
    if errs:
        dp = w / f"c2-{args.song}-{args.style}.draft.md"
        dp.write_text(out, encoding="utf-8")
        print(json.dumps({"song": args.song, "style": args.style, "accepted": False,
                          "problems": errs, "draft": str(dp)}, indent=1))
        return 1
    c2p.write_text(json.dumps(c2, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"song": args.song, "style": args.style, "accepted": True,
                      "paragraphs": len(paras)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
