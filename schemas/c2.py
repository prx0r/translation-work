"""schemas.c2 — prompt-reproducible renders (genz, eli5, poetic, formal, ...).

A C2 render is what you get at the end: a NAME + a PROMPT over the frozen layers.
Each render stores its prompt (reproducibility), model/date (provenance), and
maps_to (every paragraph points at essence — same rule as before, new home).
"""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["song", "renders"]
RENDER_REQUIRED = ["style", "prompt", "paragraphs"]


def validate(obj: dict, path: str = "c2", essence_n: int | None = None) -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "renders", list, path)
    if not obj.get("renders"):
        out.append(err(path, "empty renders (a C2 file with no renders is pointless)"))
    for r in obj.get("renders", []):
        p = f"{path}.renders[{r.get('style', '?')}]"
        if not isinstance(r, dict):
            out.append(err(p, "must be an object")); continue
        out += check_required(r, RENDER_REQUIRED, p)
        if not str(r.get("prompt", "")).strip():
            out.append(err(p, "empty prompt (a C2 render without its prompt is not reproducible)"))
        paras = r.get("paragraphs", [])
        if not paras:
            out.append(err(p, "empty paragraphs"))
        for i, para in enumerate(paras):
            q = f"{p}[{i}]"
            if not isinstance(para, dict) or not str(para.get("text", "")).strip():
                out.append(err(q, "empty text")); continue
            maps = para.get("maps_to", [])
            if not maps:
                out.append(err(q, "no maps_to (every render paragraph must point at essence)"))
            if essence_n is not None:
                for e in maps:
                    if not isinstance(e, int) or not (0 <= e < essence_n):
                        out.append(err(q, f"maps_to {e} out of essence range (0..{essence_n-1})"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED,
            "properties": {"song": {"type": "string"},
                           "renders": {"type": "array", "items": {"type": "object",
                                        "required": RENDER_REQUIRED}}}}
