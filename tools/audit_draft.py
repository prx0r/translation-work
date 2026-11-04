#!/usr/bin/env python3
"""audit_draft.py — run the reasoning-chain gate on a draft. Stdlib only.

  audit_draft.py --text-file draft.md --refs refs.json [--sources sources.json]
                 [--identity NAME] [--model NAME]

Prints the audit receipt (content hash, verifier, per-check results,
verdict). Exit 1 on FAIL, 0 on PASS — wire it before any publish step.
Refs: [{"kind":"chunk","work":...,"target":...}]; sources:
{"markers": {marker: {"text": ...}}, "external": [{ref, retrieved}]}.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "svread" / "mcp"))
import audit  # noqa: E402


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="audit_draft.py")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text-file", default=None)
    g.add_argument("--text", default=None)
    p.add_argument("--refs", default="[]")
    p.add_argument("--sources", default="{}")
    p.add_argument("--identity", default="scholar-cli/audit")
    p.add_argument("--model", default="")
    args = p.parse_args(argv)
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    try:
        refs = json.loads(args.refs)
        sources = json.loads(args.sources)
    except ValueError as e:
        print(f"error: bad JSON: {e}", file=sys.stderr)
        return 2
    try:
        receipt = audit.audit(text, refs=refs, sources=sources,
                              identity=args.identity, model=args.model)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 1 if receipt["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
