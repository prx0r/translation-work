"""Shared layer registry for agent tooling and Scholar submissions.

The existing validators remain authoritative.  The exported JSON schemas describe
their structural subset; song-level checks still require validate_song.py.
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

from . import LAYER_ORDER, SCHEMA_VERSION

SONG_LAYERS = frozenset({"c1", "c2"})
STRUCTURAL_SCHEMA_VERSION = "2.0.0"

TEXT = {"type": "string", "minLength": 1}
TEXTS = {"type": "array", "items": TEXT, "minItems": 1}
INDEXES = {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 1}
IDENTITY = {"verse_id": TEXT, "song": TEXT, "verse": {"type": "integer", "minimum": 1}}
PROPERTIES = {
    "t1": {**IDENTITY, "quick_english": TEXT, "source_sha": TEXT,
           "tokens": {"type": "array", "minItems": 1, "items": {
               "type": "object", "required": ["surface", "quick_gloss"],
               "properties": {"surface": TEXT, "quick_gloss": TEXT}}}},
    "l0": {"id": TEXT, "verse_id": TEXT, "pada_index": {"type": "integer", "minimum": 0},
           "surface": TEXT, "citation": TEXT, "chosen_index": {"type": "integer", "minimum": 0},
           "status": {"type": "string", "enum": ["PARSED", "AMBIGUOUS", "FAILED"]},
           "fork": {"type": "string", "enum": ["none", "live", "resolved"]},
           "options": {"type": "array", "maxItems": 5, "items": {
               "type": "object", "required": ["gloss", "rank", "source", "grounds"],
               "properties": {"gloss": TEXT, "rank": {"type": "integer", "minimum": 1},
                              "source": TEXT, "grounds": TEXT}}}},
    "argmap": {**IDENTITY, "sanskrit_sha": TEXT, "speaker": TEXT, "question": TEXT,
               "inference": TEXT, "reconstruction": TEXT, "premises": {"type": "array", "items": TEXT},
               "uncertainties": {"type": "array"}, "structured": {"type": "boolean"},
               "traces": {"type": "object", "required": ["t1_verse", "l0_ids"],
                          "properties": {"t1_verse": TEXT, "l0_ids": TEXTS}}},
    "l2": {**IDENTITY, "plain_english": TEXT, "sanskrit_cite": TEXT, "l0_ids": TEXTS,
           "supplied": {"type": "array", "items": TEXT}},
    "c1": {"song": TEXT, "essence": TEXTS, "renders": {"type": "object", "required": ["standard"]}},
    "l3": {**IDENTITY, "lines": TEXTS, "sanskrit_cite": TEXT, "l0_ids": TEXTS, "essence_maps": INDEXES},
    "l4": {**IDENTITY, "lines": TEXTS, "sanskrit_cite": TEXT, "l0_ids": TEXTS, "essence_maps": INDEXES},
    "c2": {"song": TEXT, "renders": {"type": "array", "minItems": 1, "items": {
        "type": "object", "required": ["style", "prompt", "paragraphs"],
        "properties": {"style": TEXT, "prompt": TEXT, "paragraphs": {"type": "array", "minItems": 1,
            "items": {"type": "object", "required": ["text", "maps_to"],
                      "properties": {"text": TEXT, "maps_to": INDEXES}}}}}}},
}


def module(layer: str):
    if layer not in LAYER_ORDER:
        raise ValueError(f"unknown layer: {layer}")
    return importlib.import_module(f"schemas.{layer}")


def schema(layer: str) -> dict:
    result = module(layer).to_json_schema()
    result["properties"] = {**result.get("properties", {}), **PROPERTIES[layer]}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:svatantrya:schema:{STRUCTURAL_SCHEMA_VERSION}:{layer}",
        "title": f"Svatantrya {layer.upper()} structural schema",
        "x-validator": f"schemas.{layer}.validate",
        "x-schema-version": SCHEMA_VERSION,
        "x-structural-schema-version": STRUCTURAL_SCHEMA_VERSION,
        **result,
    }


def content_schema(layer: str) -> dict:
    """The shape of one Scholar version; L0 versions contain all verse tokens."""
    item = schema(layer)
    if layer != "l0":
        return item
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:svatantrya:schema:{STRUCTURAL_SCHEMA_VERSION}:l0:verse",
        "title": "Svatantrya L0 verse token list structural schema",
        "x-validator": "schemas.l0.validate (per token)",
        "x-schema-version": SCHEMA_VERSION,
        "x-structural-schema-version": STRUCTURAL_SCHEMA_VERSION,
        "type": "array", "minItems": 1, "items": item,
    }


def snapshot() -> dict:
    return {"structural_schema_version": STRUCTURAL_SCHEMA_VERSION,
            "base_schema_version": SCHEMA_VERSION,
            "layers": {layer: content_schema(layer) for layer in LAYER_ORDER}}


def snapshot_errors() -> list[str]:
    path = Path(__file__).resolve().parent / "releases" / f"{STRUCTURAL_SCHEMA_VERSION}.json"
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"structural schema snapshot unavailable: {exc}"]
    return [] if saved == snapshot() else ["structural schema snapshot differs from the registry"]


def structural_errors(value, spec: dict, path: str) -> list[str]:
    expected = spec.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
    if expected in types and (not isinstance(value, types[expected]) or
                              (expected == "integer" and isinstance(value, bool))):
        return [f"{path}: must be {expected}"]
    errors = []
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{path}: must be one of {spec['enum']}")
    if isinstance(value, str) and len(value) < spec.get("minLength", 0):
        errors.append(f"{path}: must be non-empty")
    if isinstance(value, int) and not isinstance(value, bool) and value < spec.get("minimum", value):
        errors.append(f"{path}: below minimum {spec['minimum']}")
    if isinstance(value, dict):
        for key in spec.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        for key, rule in spec.get("properties", {}).items():
            if key in value:
                errors.extend(structural_errors(value[key], rule, f"{path}.{key}"))
    if isinstance(value, list):
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if len(value) > spec.get("maxItems", len(value)):
            errors.append(f"{path}: too many items")
        if "items" in spec:
            for index, item in enumerate(value):
                errors.extend(structural_errors(item, spec["items"], f"{path}[{index}]"))
    return errors


def validate(layer: str, content, *, path: str = "content") -> list[str]:
    """Run the existing per-object validator, returning errors for malformed input."""
    validator = module(layer).validate
    if layer == "l0":
        if not isinstance(content, list) or not content:
            return [f"{path}: L0 must be a non-empty list of token objects"]
        rows = content
    elif layer in SONG_LAYERS:
        rows = [content]
    else:
        rows = content if isinstance(content, list) else [content]
        if not rows:
            return [f"{path}: must contain at least one object"]

    errors = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{path}[{index}]: must be an object")
            continue
        errors.extend(structural_errors(row, schema(layer), f"{path}[{index}]"))
        try:
            errors.extend(validator(row, f"{path}[{index}]"))
        except (TypeError, ValueError, KeyError, AttributeError, IndexError) as exc:
            errors.append(f"{path}[{index}]: malformed {layer} object ({exc})")
    return errors
