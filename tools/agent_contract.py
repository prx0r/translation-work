#!/usr/bin/env python3
"""Describe and validate the canonical translation layers for agents.

    python3 tools/agent_contract.py describe [--layer l0]
    python3 tools/agent_contract.py examples --layer l4 [--work paramarthasara]
    python3 tools/agent_contract.py validate --layer l3 --file passage.json

The exported structural schemas do not replace the Python validators or the
cross-layer and source checks in validate_song.py and check.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from schemas import LAYER_ORDER, SCHEMA_VERSION  # noqa: E402
from schemas import registry  # noqa: E402

CONTRACT_VERSION = "svatantrya-agent-contract/1"
EXAMPLES = {
    "t1": ("sivastotravali/data/s01.t1.json", "s01-v01"),
    "l0": ("sivastotravali/data/s06.l0.json", "s06-v01"),
    "argmap": ("sivastotravali/data/s01.argmap.json", "s01-v21"),
    "l2": ("sivastotravali/data/s01.l2.json", "s01-v01"),
    "c1": ("sivastotravali/data/s01.c1.json", "s01"),
    "l3": ("sivastotravali/data/s01.l3.json", "s01-v01"),
    "l4": ("paramarthasara/data/param-p01.l4.json", "param-p01-v01"),
    "c2": ("sivastotravali/data/s01.c2.json", "s01"),
}
DEPENDENCIES = {
    "t1": ["source"],
    "l0": ["source", "t1"],
    "argmap": ["source", "t1", "l0"],
    "l2": ["source", "t1", "l0", "argmap"],
    "c1": ["source", "t1", "l0", "argmap", "l2"],
    "l3": ["source", "t1", "l0", "argmap", "l2", "c1"],
    "l4": ["l3", "c1"],
    "c2": ["c1", "l3"],
}


def content_hash(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def example(layer: str) -> dict:
    name, identifier = EXAMPLES[layer]
    path = ROOT / name
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        matches = [row for row in data if row.get("id") == identifier
                   or row.get("verse_id") == identifier]
        if layer == "l0" and matches:
            data = matches
        elif len(matches) != 1:
            raise ValueError(f"{name}: expected one example for {identifier}")
        else:
            data = matches[0]
    elif data.get("song") != identifier:
        raise ValueError(f"{name}: expected song {identifier}")
    return {"file": name, "file_sha256": file_hash(path), "target": identifier,
            "content_sha256": content_hash(data), "content": data,
            "note": "Illustrates the data shape; review status is not implied."}


def describe(selected: str | None = None, include_instructions: bool = False) -> dict:
    errors = registry.snapshot_errors()
    if errors:
        raise ValueError("; ".join(errors))
    skill_files = ["skills/crystal-ipvv/SKILL.md", "skills/crystal-ipvv/EXAMPLES.md",
                   "skills/l4-song/SKILL.md", "process/L4-SONG-PROCESS-2026-11-03.md",
                   "lore/rasa/abhinavagupta-rasa-grounding-2026-11-01.md",
                   "lore/rasa/english-transmission-2026-11-03.md",
                   "lore/bank/songcraft-bank.json", "LAYERS.md", "crystal.md", "mistakes.md"]
    layers = [selected] if selected else LAYER_ORDER
    process_files = [{"path": name, "sha256": file_hash(ROOT / name)} for name in skill_files]
    if include_instructions:
        for item in process_files:
            item["content"] = (ROOT / item["path"]).read_text(encoding="utf-8")
    return {
        "contract_version": CONTRACT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "structural_schema_version": registry.STRUCTURAL_SCHEMA_VERSION,
        "structural_schema_snapshot_sha256": file_hash(
            ROOT / "schemas/releases" / f"{registry.STRUCTURAL_SCHEMA_VERSION}.json"),
        "order": ["source", *LAYER_ORDER],
        "policy": {
            "scope": "one work at a time",
            "status": "machine-proposed until human review",
            "l4": "first verse needs owner verdict before the rest",
            "validation": "Python validators plus validate_song.py and check.py",
            "json_schema": "structural contract; Python and cross-layer checks also apply",
        },
        "process_files": process_files,
        "layers": [{
            "id": layer,
            "depends_on": DEPENDENCIES[layer],
            "scope": "song" if layer in registry.SONG_LAYERS else "verse",
            "validator": f"schemas/{layer}.py",
            "validator_sha256": file_hash(ROOT / "schemas" / f"{layer}.py"),
            "schema": registry.content_schema(layer),
            "example": example(layer),
        } for layer in layers],
    }


def examples_catalog(layer: str, work: str | None = None, offset: int = 0,
                     limit: int = 100) -> dict:
    """Index existing canonical data as candidates, not as a quality certification."""
    if offset < 0 or not 1 <= limit <= 1000:
        raise ValueError("offset must be non-negative and limit must be 1..1000")
    paths = sorted(path for path in ROOT.glob(f"*/data/*.{layer}.json")
                   if work is None or path.parent.parent.name == work)
    records = []
    for path in paths[offset:offset + limit]:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else [data]
        targets = sorted({row.get("verse_id") or row.get("song") for row in rows
                          if isinstance(row, dict) and (row.get("verse_id") or row.get("song"))})
        song = path.name[:-(len(layer) + 6)]  # remove .<layer>.json
        proof = path.parent.parent / "proof" / f"proof-{song}.json"
        gate = json.loads(proof.read_text(encoding="utf-8")).get("deterministic_gate") if proof.exists() else None
        records.append({"work": path.parent.parent.name, "song": song,
                        "file": str(path.relative_to(ROOT)), "sha256": file_hash(path),
                        "record_count": len(rows), "target_count": len(targets),
                        "targets_sample": targets[:5], "recorded_proof_gate": gate})
    return {"contract_version": CONTRACT_VERSION, "layer": layer, "work": work,
            "offset": offset, "limit": limit, "total_files": len(paths),
            "note": "Existing layer data are candidates; a proof gate is not human review or a quality certification.",
            "files": records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    description = commands.add_parser("describe")
    description.add_argument("--layer", choices=LAYER_ORDER)
    description.add_argument("--include-instructions", action="store_true",
                             help="include the canonical process, examples, and standards")
    catalog = commands.add_parser("examples", help="index existing candidate layer files")
    catalog.add_argument("--layer", choices=LAYER_ORDER, required=True)
    catalog.add_argument("--work")
    catalog.add_argument("--offset", type=int, default=0)
    catalog.add_argument("--limit", type=int, default=100)
    validation = commands.add_parser("validate")
    validation.add_argument("--layer", choices=LAYER_ORDER, required=True)
    validation.add_argument("--file", required=True)
    args = parser.parse_args()
    if args.command == "describe":
        result = describe(args.layer, args.include_instructions)
        result["contract_sha256"] = content_hash(result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    if args.command == "examples":
        try:
            result = examples_catalog(args.layer, args.work, args.offset, args.limit)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    try:
        content = json.loads(Path(args.file).read_text(encoding="utf-8"))
        errors = registry.validate(args.layer, content)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors = [str(exc)]
    result = {"contract_version": CONTRACT_VERSION, "schema_version": SCHEMA_VERSION,
              "structural_schema_version": registry.STRUCTURAL_SCHEMA_VERSION,
              "layer": args.layer, "scope": "individual layer objects",
              "errors": errors}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
