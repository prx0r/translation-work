"""schemas.l0 — L0 literal-gloss objects (one per token). The options list is the point."""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["id", "verse_id", "pada_index", "surface", "citation", "options",
            "chosen_index", "status"]
OPTION_REQUIRED = ["gloss", "rank"]
# OPTION_SOURCES: controlled vocabulary for where an alternative reading comes from.
# A fork without a source is an invention. New witnesses append here, never free-text elsewhere.
OPTION_SOURCES = ("t1-draft", "grammar", "lakshmanjoo", "dyczkowski", "ksemaraja-vivrti",
                  "bailly", "sandhi-variant", "compound-split", "witness")
STATUSES = ("PARSED", "AMBIGUOUS", "FAILED")
# status = PARSE QUALITY (ipvv meaning: AMBIGUOUS = recoverable but not clean).
# fork = SEMANTIC STATE (T5): none | live (undecided) | resolved (argmap adjudicated).
# The two axes are independent: a clean record can carry a live fork.
FORKS = ("none", "live", "resolved")
MAX_OPTIONS = 5


def validate(obj: dict, path: str = "l0") -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "options", list, path)
    opts = obj.get("options", [])
    if len(opts) > MAX_OPTIONS:
        out.append(err(path, f"{len(opts)} options > max {MAX_OPTIONS} (genuine forks only)"))
    for i, o in enumerate(opts):
        p = f"{path}.options[{i}]"
        if not isinstance(o, dict):
            out.append(err(p, "must be an object")); continue
        out += check_required(o, OPTION_REQUIRED, p)
        if not o.get("gloss"):
            out.append(err(p, "empty gloss"))
        if "source" in o and o["source"] not in OPTION_SOURCES and not str(o["source"]).startswith("witness-"):
            out.append(err(p, f"source {o['source']!r} not in controlled vocabulary (see OPTION_SOURCES)"))
        if "grounds" in o and not str(o["grounds"]).strip():
            out.append(err(p, "grounds present but empty (state the grammatical/witness basis)"))
    ci = obj.get("chosen_index")
    if isinstance(ci, int) and opts and not (0 <= ci < len(opts)):
        out.append(err(path, f"chosen_index {ci} out of range ({len(opts)} options)"))
    st = obj.get("status")
    if st not in STATUSES:
        out.append(err(path, f"status must be one of {STATUSES}"))
    if st == "FAILED" and opts:
        out.append(err(path, "FAILED must carry no usable options"))
    if st == "PARSED" and not opts:
        out.append(err(path, "PARSED requires >=1 option"))
    fk = obj.get("fork", "none" if len(opts) <= 1 else None)
    if fk not in FORKS:
        if fk is None:
            out.append(err(path, f"{len(opts)} options require explicit fork: live (undecided) or resolved (adjudicated)"))
        else:
            out.append(err(path, f"fork must be one of {FORKS}"))
    elif fk in ("live", "resolved") and len(opts) < 2:
        out.append(err(path, f"fork:{fk} requires >=2 options"))
    if fk in ("live", "resolved"):
        # Forked tokens are where scholarship lives: morphology must be stated, not unknown.
        # Convention: case.number.gender (m.nom.sg), verb person.number.voice-tense/mood + root
        # (3sg.pres.mid √gam), indeclinables as (indecl.), compounds as member+membership.
        if not str(obj.get("morph", "")).strip() or obj.get("morph_unknown"):
            out.append(err(path, "fork:live|resolved requires analyzed morph "
                                 "(case/number/gender or tense/mood/voice+root) — no unknown morphology on forks"))
    for h in obj.get("history", []):
        if not isinstance(h, dict) or not h.get("gloss") or not h.get("reason") or not h.get("date"):
            out.append(err(path, "history[] entries need {gloss, reason, date}"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED,
            "properties": {"id": {"type": "string"}, "verse_id": {"type": "string"},
                           "pada_index": {"type": "integer"}, "surface": {"type": "string"},
                           "citation": {"type": "string"}, "morph": {"type": "string"},
                           "morph_unknown": {"type": "boolean"},
                           "options": {"type": "array", "maxItems": MAX_OPTIONS,
                                       "items": {"type": "object", "required": OPTION_REQUIRED}},
                           "chosen_index": {"type": "integer"}, "status": {"type": "string"},
                           "revised": {"type": "boolean"}, "revise_reason": {"type": "string"}}}
