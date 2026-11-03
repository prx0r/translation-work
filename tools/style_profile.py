#!/usr/bin/env python3
"""Prepare an opt-in local style brief and render a separately attributed draft.

Examples stay local until an explicitly selected runner is invoked. A runner
reads the brief as JSON on stdin and returns {"model": "...", "content": {...}}.
The generated submission contains provenance hashes, not the private examples.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import scholar  # noqa: E402
import workcfg  # noqa: E402

STYLE_LAYERS = ("l2", "l3", "l4")
FIELDS = {"l2": "plain_english", "l3": "lines", "l4": "lines"}
PROFILE_VERSION = "scholar-style-brief/1"


def fail(message: str):
    raise ValueError(message)


def read_drafts(paths: list[str]) -> list[dict]:
    result = []
    for name in paths:
        payload = json.loads(Path(name).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            fail("private draft file must contain an object")
        rows = payload.get("versions", [payload])
        if not isinstance(rows, list):
            fail("private draft versions must be a list")
        for row in rows:
            if not isinstance(row, dict):
                fail("each private draft must be an object")
            result.append({"work": payload.get("work"), **row})
    return result


def original(work: str, layer: str, target: str):
    scholar.validate_work(work)
    return scholar.load_original(work, layer, target)[0]


def authorized_rows(author: str, private_files: list[str], include_legacy: bool) -> list[dict]:
    entries = []
    for ledger in sorted(ROOT.glob("*/scholar/versions.jsonl")):
        entries.extend(scholar.jsonl_read(ledger))
    entries.extend(read_drafts(private_files))
    parents = {row.get("version_id"): row for row in entries}
    allowed = []
    for row in sorted(entries, key=lambda item: (item.get("created_at", ""), item.get("version_id", ""))):
        if row.get("author") != author:
            continue
        if row.get("author_kind") != "human" and not (
            include_legacy and "author_kind" not in row
        ):
            continue
        parent = row.get("parent")
        if parent and (parent not in parents or parents[parent].get("author") != author):
            continue
        if row.get("version_schema") == scholar.VERSION_SCHEMA:
            if scholar.vid_of(row) != row.get("version_id") or scholar.sha(row["content"]) != row.get("content_sha256"):
                fail(f"version {row.get('version_id')} failed its content hash")
        allowed.append(row)
    return allowed


def base_for(row: dict):
    work, target, layer = row.get("work"), row.get("target"), row.get("layer")
    base = original(work, layer, target)
    if row.get("version_schema") == scholar.VERSION_SCHEMA:
        snapshot = scholar.object_path(work, row["base_sha256"])
        base = json.loads(snapshot.read_text(encoding="utf-8"))
        if scholar.sha(base) != row["base_sha256"]:
            fail(f"version {row.get('version_id')} has an invalid base snapshot")
    elif row.get("base_sha256") and scholar.sha(base) != row["base_sha256"]:
        fail(f"draft {row.get('version_id')} was made against a different base")
    return base


def collect_examples(author: str, layer: str, private_files: list[str],
                     include_legacy: bool = False) -> tuple[list[dict], list[dict]]:
    chosen, lexical = {}, {}
    for row in authorized_rows(author, private_files, include_legacy):
        if row.get("layer") not in (layer, "l0"):
            continue
        work, target = row.get("work"), row.get("target")
        if not isinstance(work, str) or not isinstance(target, str):
            continue
        base = base_for(row)
        content = row.get("content")
        if row["layer"] == "l0":
            if not isinstance(base, list) or not isinstance(content, list):
                continue
            original_tokens = {token.get("id"): token for token in base}
            for token in content:
                prior = original_tokens.get(token.get("id"), {})
                try:
                    old = prior["options"][prior["chosen_index"]]["gloss"]
                    selected = token["options"][token["chosen_index"]]
                except (KeyError, IndexError, TypeError):
                    continue
                if selected.get("gloss") and selected["gloss"] != old:
                    lexical[(work, target, token.get("id"))] = {
                        "work": work, "target": target, "token_id": token.get("id"),
                        "surface": token.get("surface"), "previous": old,
                        "chosen": selected["gloss"], "grounds": selected.get("grounds", ""),
                        "version_id": row.get("version_id"),
                    }
            continue
        if not isinstance(content, dict) or not isinstance(base, dict):
            continue
        field = FIELDS[layer]
        before = base.get(field)
        after = content.get(field)
        if not after or before == after:
            continue
        chosen[(work, target)] = {
            "work": work, "target": target, "version_id": row.get("version_id"),
            "source_excerpt": base.get("sanskrit_cite", ""),
            "source_excerpt_is_complete": False,
            "before": before, "after": after,
        }
    return ([chosen[key] for key in sorted(chosen)],
            [lexical[key] for key in sorted(lexical)])


def source_context(work: str, target: str, layer: str) -> dict:
    base = original(work, layer, target)
    t1 = original(work, "t1", target)
    cfg = workcfg.work_config(work) or {}
    source = Path(cfg.get("source", ""))
    lines = t1.get("source_lines")
    if not source.is_file():
        fail("a configured source file is required for the target")
    if cfg.get("kind") == "segments":
        matches = [item for item in cfg["segments"] if item["verse_id"] == target]
        if len(matches) != 1:
            fail("target does not resolve to one pinned source segment")
        raw = cfg["source_bytes"]
        span = matches[0]
        excerpt = raw[span["start"]:span["end"]].decode("utf-8")
    else:
        if not isinstance(lines, list) or len(lines) != 2:
            fail("source_lines are required for this target")
        raw = source.read_bytes()
        decoded = raw.decode("utf-8").splitlines()
        start, end = lines
        if not isinstance(start, int) or not isinstance(end, int) or not (1 <= start <= end <= len(decoded)):
            fail("target source_lines do not resolve in the source edition")
        excerpt = "\n".join(decoded[start - 1:end])
    context = {"work": work, "target": target, "layer": layer,
               "source_sha256": hashlib.sha256(raw).hexdigest(),
               "source_lines": lines, "source_excerpt": excerpt,
               "base_sha256": scholar.sha(base), "original": base, "t1": t1}
    if cfg.get("kind") == "segments":
        context["source_byte_span"] = [span["start"], span["end"]]
    for name in ("l0", "argmap", "l2", "l3", "l4"):
        path = ROOT / work / "data" / f"{scholar.song_of(target, name)}.{name}.json"
        if path.exists():
            context[name] = original(work, name, target)
    song = scholar.song_of(target, layer)
    if (ROOT / work / "data" / f"{song}.c1.json").exists():
        context["c1"] = original(work, "c1", song)
    return context


def prepare(author: str, work: str, target: str, layer: str,
            private_files: list[str], include_legacy: bool = False) -> dict:
    if layer not in STYLE_LAYERS:
        fail("style drafts support L2, L3, and L4")
    examples, lexical = collect_examples(author, layer, private_files, include_legacy)
    profile = {"format": PROFILE_VERSION, "author": author, "layer": layer,
               "minimum_examples": 3, "ready": len(examples) >= 3,
               "examples": examples, "lexical_choices": lexical,
               "target": source_context(work, target, layer),
               "instructions": (
                   "Draft only the requested translation field. Use the source and grounded "
                   "layers for meaning. Use the scholar's examples and recorded lexical "
                   "choices for word choice and cadence when appropriate to the context, "
                   "without adding unsupported claims. Record uncertainty in a separate review, "
                   "and attribute the output to the agent, not to the scholar."
               )}
    profile["profile_sha256"] = scholar.sha(profile)
    return profile


def write_private(path: str, value: dict) -> None:
    target = Path(path).resolve()
    if target.is_relative_to(ROOT.resolve()):
        fail("save private style briefs outside the translation-work repository")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def render(profile: dict, command: str, agent: str) -> dict:
    if not isinstance(profile, dict) or profile.get("format") != PROFILE_VERSION:
        fail("not a style brief")
    expected = profile.get("profile_sha256")
    if expected != scholar.sha({key: value for key, value in profile.items() if key != "profile_sha256"}):
        fail("style brief hash does not match its contents")
    if not profile.get("ready") or len(profile.get("examples", [])) < 3:
        fail("at least three distinct edited passages are required")
    args = shlex.split(command)
    if not args:
        fail("runner command is empty")
    completed = subprocess.run(args, input=json.dumps(profile, ensure_ascii=False),
                               text=True, capture_output=True, timeout=180, check=False)
    if completed.returncode:
        fail(f"runner failed with exit {completed.returncode}")
    response = json.loads(completed.stdout)
    if not isinstance(response, dict) or not isinstance(response.get("content"), dict):
        fail("runner must return an object containing content")
    target = profile["target"]
    field = FIELDS[target["layer"]]
    if set(response["content"]) != {field}:
        fail(f"runner content must contain only {field}")
    content = {**target["original"], **response["content"]}
    errors = scholar.layer_registry.validate(target["layer"], content)
    if errors:
        fail("runner returned invalid content: " + "; ".join(errors))
    model = response.get("model")
    if not isinstance(model, str) or not model.strip():
        fail("runner must identify its model")
    if not agent.strip():
        fail("agent identity is required")
    entry = {"version_id": "local:style-" + scholar.sha({"profile": expected,
                                                          "content": content, "agent": agent}),
             "work": target["work"], "layer": target["layer"], "target": target["target"],
             "parent": None, "base_sha256": target["base_sha256"], "author": agent,
             "author_kind": "agent", "note": "Agent draft informed by opted-in scholar edits",
             "content": content, "provenance": {"style_author": profile["author"],
                 "style_profile_sha256": expected, "model": model}}
    return {"format": "scholar-submission/v1", "work": target["work"], "versions": [entry]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("--author", required=True)
    p.add_argument("--work", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--layer", choices=STYLE_LAYERS, required=True)
    p.add_argument("--private-drafts", action="append", default=[])
    p.add_argument("--include-legacy", action="store_true")
    p.add_argument("--output")
    r = commands.add_parser("render")
    r.add_argument("--profile", required=True)
    r.add_argument("--runner", required=True, help="command receiving the private brief on stdin")
    r.add_argument("--agent", required=True)
    r.add_argument("--consent", action="store_true", help="scholar has authorized this runner")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(args.author, args.work, args.target, args.layer,
                             args.private_drafts, args.include_legacy)
            if args.output:
                write_private(args.output, result)
                print(json.dumps({"ready": result["ready"], "examples": len(result["examples"]),
                                  "profile_sha256": result["profile_sha256"]}))
            else:
                print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        else:
            if not args.consent:
                fail("the scholar must authorize the selected runner")
            profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
            print(json.dumps(render(profile, args.runner, args.agent), ensure_ascii=False, indent=2))
    except (ValueError, OSError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
