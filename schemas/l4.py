"""schemas.l4 — song-layer objects (L3 set to music).

L4 takes the L3 exact transmission and makes it sing: prosody, rhythm,
rhyme, refrain, cadence — small edits and rearrangements so the verse
parses as song when read aloud or chanted. Music, never doctrine:

- Every L4 line traces to L0 ids and C1 essence indices ALREADY present
  in the corresponding L3 (validate_song.py enforces subset, not just
  existence). A rhyme word that needs a new slant fails: re-ground it
  in L3 first, or drop it.
- L4 requires L3. No L3, no L4.
- Readability is strict from birth: no `/` anywhere in L4 lines, and
  proper names keep exact Sanskrit diacritics (Śiva, Māyā, Śambhu).
- L4 may share sentences with L3 — it is a setting of L3, not a new
  layer of meaning. (The L2/L3 no-share rule does NOT apply L3→L4.)
- Machine-proposed until signed. First verse of a work's L4 needs
  owner verdict before the rest (mistakes.md rule 15: one at a time).
"""
from __future__ import annotations
import re
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["verse_id", "song", "verse", "lines", "sanskrit_cite", "l0_ids", "essence_maps"]

# ASCII stand-ins that rule 14 forbids in transmission lines.
ASCII_FORMS = re.compile(r"\b(Siva|Maya|Sambhu)(s|'s)?\b")


def validate(obj: dict, path: str = "l4", l0_ids: set | None = None,
             n_essence: int | None = None) -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    lines = obj.get("lines", [])
    out += check_type(obj, "lines", list, path)
    if not lines or not all(isinstance(x, str) and x.strip() for x in lines):
        out.append(err(path, "lines must be non-empty strings, one per song line"))
    for ln in lines if isinstance(lines, list) else []:
        if isinstance(ln, str):
            if "/" in ln:
                out.append(err(path, f"slash in L4 line (rule 14, no / anywhere): {ln[:60]!r}"))
            m = ASCII_FORMS.search(ln)
            if m:
                out.append(err(path, f"ASCII {m.group(1)!r} in L4 line — use exact diacritics "
                                     f"(Śiva, Māyā, Śambhu): {ln[:60]!r}"))
    out += check_type(obj, "l0_ids", list, path)
    if not obj.get("l0_ids"):
        out.append(err(path, "empty l0_ids (every L4 must trace to L0)"))
    out += check_type(obj, "essence_maps", list, path)
    if not obj.get("essence_maps"):
        out.append(err(path, "empty essence_maps (every L4 must map to C1 essence)"))
    for i in obj.get("essence_maps", []):
        if not isinstance(i, int) or i < 0:
            out.append(err(path, f"essence_maps must be non-negative ints, got {i!r}"))
        elif n_essence is not None and i >= n_essence:
            out.append(err(path, f"essence index {i} out of range (0..{n_essence - 1})"))
    if "form" in obj:
        out += check_type(obj, "form", str, path)
        if isinstance(obj.get("form"), str) and not obj["form"].strip():
            out.append(err(path, "form, if present, must be non-empty"))
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
