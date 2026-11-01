"""schemas.l2 — plain-English verse objects (every clause traces to L0)."""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["verse_id", "song", "verse", "plain_english", "sanskrit_cite", "l0_ids"]


def validate(obj: dict, path: str = "l2", l0_ids: set | None = None,
             source_text: str | None = None) -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    if not obj.get("plain_english", "").strip():
        out.append(err(path, "empty plain_english"))
    out += check_type(obj, "l0_ids", list, path)
    if not obj.get("l0_ids"):
        out.append(err(path, "empty l0_ids (every L2 must trace to L0)"))
    # supplied: every bracketed interpolation / referent-supply, logged not hidden (ipvv l2 compat).
    if "supplied" in obj:
        out += check_type(obj, "supplied", list, path)
        for s in obj.get("supplied", []):
            if not isinstance(s, str) or not s.strip():
                out.append(err(path, "supplied entries must be non-empty strings"))
    if "fidelity" in obj and obj["fidelity"] not in ("preserved", "supplied", "not-resolved"):
        out.append(err(path, "fidelity must be preserved/supplied/not-resolved"))
    if l0_ids is not None:
        for lid in obj.get("l0_ids", []):
            if lid not in l0_ids:
                out.append(err(f"{path}", f"l0_id {lid} does not exist"))
    cite = obj.get("sanskrit_cite", "")
    if source_text is not None and cite:
        import re as _re
        flat = _re.sub(r"\s+", " ", source_text)
        for part in [p.strip() for p in cite.split("|") if p.strip()]:
            if _re.sub(r"\s+", "", part) not in _re.sub(r"\s+", "", flat):
                out.append(err(path, f"cite part not byte-exact in source: {part[:60]}"))
                break
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED}
