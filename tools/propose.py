#!/usr/bin/env python3
"""tools/propose.py — the living-translation loop: propose -> support -> accept/reject.

  python3 tools/propose.py --song s01 --kind new-option --target l0:s01-v21-p011 \\
      --body '{"gloss":"of-no-repute","source":"grammar","grounds":"a-naman as social privative; cf. R. on v15"}' \\
      --by "reader@example" --grounds-seen
  (grounds live in --body JSON for option kinds; --grounds-seen confirms you read the fork.)

  python3 tools/propose.py --song s01 --support <sug-id> --by NAME [--note ...]
  python3 tools/propose.py --song s01 --accept <sug-id> --by MAINTAINER --reason "..."
  python3 tools/propose.py --song s01 --reject <sug-id> --by MAINTAINER --reason "..."
  python3 tools/propose.py --song s01 --list [--status open]

Accept writes history, never silently:
  new-option    -> appends L0 option (chosen unchanged unless --choose)
  choose-option -> flips L0 chosen_index + writes history + requires argmap
                   option_choices entry (use --reason; tool appends it)
  gloss-edit    -> revises T1 quick_gloss + L0 chosen (both, with history + revised flag)
  morph-fix     -> sets L0 morph (clears morph_unknown), history entry
  l2-edit       -> replaces L2 plain_english (traces kept; validator re-checks cites)
  essence-note  -> appends to C1 uncertainties/notes? rejected for now (see below)

Files: data/<song>.suggest.json (array). Validation via schemas/suggestion.py.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
sys.path.insert(0, str(ROOT / "schemas"))
import suggestion as sug  # noqa: E402


def load(sugg_path: Path) -> list:
    return json.loads(sugg_path.read_text()) if sugg_path.exists() else []


def save(sugg_path: Path, items: list):
    sugg_path.write_text(json.dumps(items, indent=1, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True)
    ap.add_argument("--kind", default=None)
    ap.add_argument("--target", default=None, help="l0:<id> | t1:<verse_id> | l2:<verse_id> | ...")
    ap.add_argument("--body", default=None, help="JSON string or plain text proposal")
    ap.add_argument("--by", default=None)
    ap.add_argument("--note", default="")
    ap.add_argument("--reason", default="")
    ap.add_argument("--support", default=None, metavar="SUG_ID")
    ap.add_argument("--accept", default=None, metavar="SUG_ID")
    ap.add_argument("--reject", default=None, metavar="SUG_ID")
    ap.add_argument("--choose", action="store_true", help="new-option also becomes chosen")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", default=None)
    args = ap.parse_args()

    w = ROOT / "sivastotravali"
    data = w / "data"
    sp = data / f"{args.song}.suggest.json"
    items = load(sp)

    if args.list:
        for o in items:
            if args.status and o.get("status") != args.status:
                continue
            print(f"{o['id']} [{o['status']}] {o['kind']} {o['target_kind']}:{o['target_id']} "
                  f"by {o['by']} supports={len(o.get('supports', []))}")
            print(f"   {o['body'][:160]}")
        return 0

    if args.support:
        o = next((x for x in items if x["id"] == args.support), None)
        if not o:
            print(f"no such suggestion: {args.support}", file=sys.stderr); return 2
        if o["status"] != "open":
            print(f"suggestion is {o['status']}, not open", file=sys.stderr); return 2
        o.setdefault("supports", []).append({"by": args.by, "date": "2026-11-01",
                                              "note": args.note} if args.note else
                                             {"by": args.by, "date": "2026-11-01"})
        save(sp, items); print(f"supported {o['id']} ({len(o['supports'])} supports)")
        return 0

    if args.reject:
        o = next((x for x in items if x["id"] == args.reject), None)
        if not o:
            print(f"no such suggestion: {args.reject}", file=sys.stderr); return 2
        if not args.reason:
            print("--reason required (closed PRs explain why)", file=sys.stderr); return 2
        o["status"] = "rejected"; o["reason"] = args.reason
        errs = sug.validate(o, "suggestion")
        if errs:
            print(json.dumps(errs, indent=1)); return 1
        save(sp, items); print(f"rejected {o['id']}")
        return 0

    if args.accept:
        return do_accept(args, w, data, sp, items)

    # create
    if not (args.kind and args.target and args.body and args.by):
        print("--kind --target --body --by required to propose", file=sys.stderr); return 2
    tkind, _, tid = args.target.partition(":")
    try:
        body = json.loads(args.body) if args.body.strip().startswith("{") else {"text": args.body}
    except Exception:
        body = {"text": args.body}
    nid = f"{args.song}-sug{len(items)+1:03d}"
    o = {"id": nid, "song": args.song, "target_kind": tkind, "target_id": tid,
         "kind": args.kind, "body": body, "grounds": body.get("grounds", args.reason or ""),
         "by": args.by, "date": "2026-11-01", "status": "open", "supports": []}
    errs = sug.validate(o, "suggestion")
    if errs:
        print(json.dumps(errs, indent=1)); return 1
    items.append(o); save(sp, items)
    print(f"proposed {nid} (open; needs supports + maintainer accept)")
    return 0


def do_accept(args, w, data, sp, items) -> int:
    o = next((x for x in items if x["id"] == args.accept), None)
    if not o:
        print(f"no such suggestion: {args.accept}", file=sys.stderr); return 2
    if o["status"] != "open":
        print(f"suggestion is {o['status']}, not open", file=sys.stderr); return 2
    if not args.by or not args.reason:
        print("--by (maintainer) and --reason required to accept", file=sys.stderr); return 2
    song = o["song"]
    hist = {"gloss": "", "reason": f"accept {o['id']} by {args.by}: {args.reason}", "date": "2026-11-01"}

    if o["kind"] == "new-option" and o["target_kind"] == "l0":
        p = data / f"{song}.l0.json"
        l0 = json.loads(p.read_text())
        t = next((x for x in l0 if x["id"] == o["target_id"]), None)
        if not t:
            print("target l0 not found", file=sys.stderr); return 2
        b = o["body"] if isinstance(o["body"], dict) else {"gloss": str(o["body"])}
        opt = {"gloss": b.get("gloss", ""), "rank": len(t.get("options", [])) + 1,
               "source": b.get("source", "witness"), "grounds": b.get("grounds", o.get("grounds", ""))}
        if not opt["gloss"] or not opt["grounds"]:
            print("new-option needs body.gloss + grounds", file=sys.stderr); return 2
        t["options"].append(opt)
        if len(t["options"]) > 1 and not t.get("fork") or t.get("fork") == "none":
            t["fork"] = "live"
        if args.choose:
            t["chosen_index"] = len(t["options"]) - 1
            t["revised"] = True; t["revise_reason"] = hist["reason"]
            t.setdefault("history", []).append({**hist, "gloss": opt["gloss"]})
        t.setdefault("history", []).append({**hist, "gloss": f"+option: {opt['gloss']}"})
        json.dump(l0, open(p, "w"), indent=1, ensure_ascii=False)
        o["merged_as"] = f"l0 {t['id']} option+{len(t['options'])}"
    elif o["kind"] == "morph-fix" and o["target_kind"] == "l0":
        p = data / f"{song}.l0.json"
        l0 = json.loads(p.read_text())
        t = next((x for x in l0 if x["id"] == o["target_id"]), None)
        if not t:
            print("target l0 not found", file=sys.stderr); return 2
        b = o["body"] if isinstance(o["body"], dict) else {}
        t["morph"] = b.get("morph", ""); t["morph_unknown"] = False
        t.setdefault("history", []).append({**hist, "gloss": t.get("citation", "")})
        json.dump(l0, open(p, "w"), indent=1, ensure_ascii=False)
        o["merged_as"] = f"l0 {t['id']} morph"
    elif o["kind"] == "choose-option" and o["target_kind"] == "l0":
        p = data / f"{song}.l0.json"
        l0 = json.loads(p.read_text())
        t = next((x for x in l0 if x["id"] == o["target_id"]), None)
        if not t:
            print("target l0 not found", file=sys.stderr); return 2
        b = o["body"] if isinstance(o["body"], dict) else {}
        idx = int(b.get("index", -1))
        if not (0 <= idx < len(t.get("options", []))):
            print("choose-option needs body.index in range", file=sys.stderr); return 2
        # write argmap adjudication (the decision lives on the record)
        ap = data / f"{song}.argmap.json"
        am = json.loads(ap.read_text())
        a = next((x for x in am if x["verse_id"] == t["verse_id"]), None)
        if a is None:
            print("verse argmap not found", file=sys.stderr); return 2
        rej = [x["gloss"] for i, x in enumerate(t["options"]) if i != idx]
        a.setdefault("option_choices", [])
        a["option_choices"] = [c for c in a["option_choices"] if c.get("l0_id") != t["id"]]
        a["option_choices"].append({"l0_id": t["id"], "chosen_index": idx,
                                    "rejected": rej, "reason": args.reason})
        if t.get("fork") == "live":
            t["fork"] = "resolved"
        t["chosen_index"] = idx
        t["revised"] = True; t["revise_reason"] = hist["reason"]
        t.setdefault("history", []).append({**hist, "gloss": t["options"][idx]["gloss"]})
        json.dump(l0, open(p, "w"), indent=1, ensure_ascii=False)
        json.dump(am, open(ap, "w"), indent=1, ensure_ascii=False)
        o["merged_as"] = f"l0 {t['id']} chosen={idx} + argmap option_choices"
    elif o["kind"] == "l2-edit" and o["target_kind"] == "l2":
        p = data / f"{song}.l2.json"
        l2 = json.loads(p.read_text())
        v = next((x for x in l2 if x["verse_id"] == o["target_id"]), None)
        if not v:
            print("target l2 not found", file=sys.stderr); return 2
        b = o["body"] if isinstance(o["body"], dict) else {}
        if not b.get("plain_english"):
            print("l2-edit needs body.plain_english", file=sys.stderr); return 2
        v["plain_english"] = b["plain_english"]
        json.dump(l2, open(p, "w"), indent=1, ensure_ascii=False)
        o["merged_as"] = f"l2 {v['verse_id']} plain_english"
    else:
        print(f"accept for kind {o['kind']} on {o['target_kind']} not yet implemented "
              f"(gloss-edit/essence-note: maintainer edits JSON directly with history)",
              file=sys.stderr)
        return 2
    o["status"] = "accepted"
    errs = sug.validate(o, "suggestion")
    if errs:
        print(json.dumps(errs, indent=1)); return 1
    save(sp, items)
    print(f"accepted {o['id']} -> {o['merged_as']} (re-validate the song next)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
