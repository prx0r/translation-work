"""schemas.l3 — final canonical translation objects (the single translation to read).

L3 is line-by-line evocative verse: it renders what the verse says (never
about the verse), carrying rasa in diction. Every line must trace to L0 ids
and to C1 essence indices; no clause may float. New doctrine, if any, fails.
Boundary items from C1 NOTEs stay open (neutral gloss + note), never smoothed.
"""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["verse_id", "song", "verse", "lines", "sanskrit_cite", "l0_ids", "essence_maps"]


def validate(obj: dict, path: str = "l3", l0_ids: set | None = None,
             n_essence: int | None = None) -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    lines = obj.get("lines", [])
    out += check_type(obj, "lines", list, path)
    if not lines or not all(isinstance(x, str) and x.strip() for x in lines):
        out.append(err(path, "lines must be non-empty strings, one per verse line"))
    out += check_type(obj, "l0_ids", list, path)
    if not obj.get("l0_ids"):
        out.append(err(path, "empty l0_ids (every L3 must trace to L0)"))
    out += check_type(obj, "essence_maps", list, path)
    if not obj.get("essence_maps"):
        out.append(err(path, "empty essence_maps (every L3 must map to C1 essence)"))
    for i in obj.get("essence_maps", []):
        if not isinstance(i, int) or i < 0:
            out.append(err(path, f"essence_maps must be non-negative ints, got {i!r}"))
        elif n_essence is not None and i >= n_essence:
            out.append(err(path, f"essence index {i} out of range (0..{n_essence - 1})"))
    if "supplied" in obj:
        out += check_type(obj, "supplied", list, path)
    if "notes" in obj:
        out += check_type(obj, "notes", list, path)
    if "fidelity" in obj and obj["fidelity"] not in ("preserved", "supplied", "not-resolved"):
        out.append(err(path, "fidelity must be preserved/supplied/not-resolved"))
    if l0_ids is not None:
        for lid in obj.get("l0_ids", []):
            if lid not in l0_ids:
                out.append(err(f"{path}", f"l0_id {lid} does not exist"))
    cite = obj.get("sanskrit_cite", "")
    if not cite.strip():
        out.append(err(path, "empty sanskrit_cite"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED}
