"""schemas.base — shared validation helpers (stdlib only)."""
from __future__ import annotations


def err(path: str, msg: str) -> str:
    return f"{path}: {msg}"


def check_required(obj: dict, required: list[str], path: str) -> list[str]:
    out = []
    for f in required:
        if f not in obj:
            out.append(err(path, f"missing required field '{f}'"))
    return out


def check_type(obj: dict, field: str, types, path: str) -> list[str]:
    if field in obj and not isinstance(obj[field], types):
        return [err(path, f"'{field}' must be {types}, got {type(obj[field]).__name__}")]
    return []
