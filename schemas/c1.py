"""schemas.c1 — essence + the STANDARD render (C1: the sharpest poetic reading).

C1 is the canonical rendering: the 7-part essay, preserved. All further renders
(genz, eli5, poetic, formal, ...) live in C2 objects (schemas/c2.py), each carrying
the prompt that reproduces it. C1 texts are never duplicated into C2 or vice versa."""

from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["song", "essence", "renders"]
STANDARD_SECTIONS = ["SUMMARY", "FUNCTION", "KEY TERMS", "LOCAL CONTEXT",
                     "EXPLANATION", "BOUNDARY", "RELATED"]


def validate(obj: dict, path: str = "c1") -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "essence", list, path)
    if not obj.get("essence"):
        out.append(err(path, "empty essence (renders must render SOMETHING)"))
    renders = obj.get("renders", {})
    if not isinstance(renders, dict) or "standard" not in renders:
        out.append(err(path, "renders.standard missing (existing 7-part essay is preserved)"))
        return out
    for name in renders:
        if name != "standard":
            out.append(err(f"{path}.renders.{name}",
                           "non-standard renders live in C2 now (data/<song>.c2.json) — moved, not duplicated"))
    std = renders["standard"]
    if isinstance(std, dict):
        for sec in STANDARD_SECTIONS:
            if sec not in (std.get("sections") or {}):
                out.append(err(f"{path}.renders.standard", f"section '{sec}' missing"))
    # rasa: Abhinavagupta's frame — what the verse DOES (relish/camatkāra), not just what it
    # says. Optional; when present all three fields are required and non-empty.
    if "rasa" in obj:
        r = obj["rasa"]
        if not isinstance(r, dict):
            out.append(err(f"{path}.rasa", "must be an object"))
        else:
            for f in ["dominant", "sthayibhava", "justification"]:
                if not str(r.get(f, "")).strip():
                    out.append(err(f"{path}.rasa", f"'{f}' required when rasa is given"))
    # derivation: L200-lite. MT decisions (SUPPLIED/LEXICAL/GRAMMATICAL/STRUCTURAL_CONNECTIVE)
    # strictly separated from IA interpretive assertions. Optional for backfill; new work fills it.
    if "derivation" in obj:
        d = obj["derivation"]
        if not isinstance(d, dict):
            out.append(err(f"{path}.derivation", "must be an object"))
        else:
            for f in ["mt_decisions", "ia_assertions"]:
                if f in d and not isinstance(d[f], list):
                    out.append(err(f"{path}.derivation", f"'{f}' must be a list"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED,
            "properties": {"song": {"type": "string"},
                           "essence": {"type": "array", "items": {"type": "string"}},
                           "renders": {"type": "object"}}}
