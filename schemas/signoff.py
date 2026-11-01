"""schemas.signoff — human acceptance records (the peer-review bar).

GATE PASS = deterministic checks green AND a human accepted (name + date).
Machine proposes; humans dispose. A signoff covers a song at a schemas version;
any data change after the signoff date re-opens review (checked by date comparison
in validate_song, warning only — the human decides, not the machine).
"""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["song", "accepted_by", "date", "scope"]


def validate(obj: dict, path: str = "signoff") -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "notes", list, path)
    if obj.get("scope") not in ("full", "t1-l0", "l2", "c1", "spot"):
        out.append(err(path, "scope must be full|t1-l0|l2|c1|spot"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED}
