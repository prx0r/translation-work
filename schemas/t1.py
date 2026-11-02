"""schemas.t1 — T1 quick-translation objects (one per verse)."""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["verse_id", "song", "verse", "quick_english", "tokens", "source_sha"]
TOKEN_REQUIRED = ["surface", "quick_gloss"]


def validate_token(t: dict, path: str) -> list[str]:
    out = check_required(t, TOKEN_REQUIRED, path)
    out += check_type(t, "surface", str, path)
    out += check_type(t, "quick_gloss", str, path)
    if not t.get("surface"):
        out.append(err(path, "empty surface"))
    if not t.get("quick_gloss"):
        out.append(err(path, "empty quick_gloss"))
    # MD-safety: [and]-gloss (surface) lines are parsed by regex downstream
    # (proof_record.parse_t1, render_md); parens inside either field corrupt
    # the parse (phrdaya v01 precedent). Keep glosses paren-free.
    for f in ("surface", "quick_gloss"):
        if any(c in str(t.get(f, "")) for c in "()"):
            out.append(err(path, f"{f} contains parens (breaks [and]-MD parsing)"))
    return out


def validate(obj: dict, path: str = "t1") -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "tokens", list, path)
    for i, t in enumerate(obj.get("tokens", [])):
        if not isinstance(t, dict):
            out.append(err(f"{path}.tokens[{i}]", "must be an object")); continue
        out += validate_token(t, f"{path}.tokens[{i}]")
    if not obj.get("quick_english", "").strip():
        out.append(err(path, "empty quick_english (T1 must face every pada)"))
    sl = obj.get("source_lines")
    if sl is not None:
        if not (isinstance(sl, list) and len(sl) == 2 and all(isinstance(x, int) for x in sl)
                and sl[0] >= 1 and sl[0] <= sl[1]):
            out.append(err(path, "source_lines must be [start, end] 1-based GRETIL lines"))
    # history[]: every change to a shipped gloss is recorded, never silently edited.
    # The base is living, but its past is immutable: each entry {gloss, reason, date}.
    for h in obj.get("history", []):
        if not isinstance(h, dict) or not h.get("gloss") or not h.get("reason") or not h.get("date"):
            out.append(err(path, "history[] entries need {gloss, reason, date}"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED,
            "properties": {"verse_id": {"type": "string"}, "song": {"type": "string"},
                           "verse": {"type": "integer"}, "quick_english": {"type": "string"},
                           "source_sha": {"type": "string"},
                           "tokens": {"type": "array", "items": {"type": "object",
                                        "required": TOKEN_REQUIRED}}}}
