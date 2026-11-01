"""schemas.suggestion — living-translation proposals (suggest + supports -> merge).

Anyone can propose an alternative; nothing enters canonical data without an
accept that writes history. Mirrors SARIT's fork/PR flow at JSON granularity and
Ambuda's status ladder (unproofed -> proofed) at object granularity:
  open       = proposed, awaiting review/supports (cf. Ambuda "Needs work")
  accepted   = merged into canonical data (history[] entry written, never silent)
  rejected   = declined with reason (kept for the record, like a closed PR)
  superseded = replaced by a newer suggestion
Supports are attestations {by, date, note} — weight follows reviewer trust;
the maintainer merges, exactly like a PR. No auth infra: honesty over machinery.
"""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["id", "song", "target_kind", "target_id", "kind", "body", "grounds",
            "by", "date", "status"]
TARGET_KINDS = ("l0", "t1", "argmap", "l2", "c1", "c2", "essence")
SUGGEST_KINDS = ("new-option", "choose-option", "gloss-edit", "l2-edit",
                 "essence-note", "witness", "morph-fix")
STATUSES = ("open", "accepted", "rejected", "superseded")


def validate(obj: dict, path: str = "suggestion") -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    if obj.get("target_kind") not in TARGET_KINDS:
        out.append(err(path, f"target_kind must be one of {TARGET_KINDS}"))
    if obj.get("kind") not in SUGGEST_KINDS:
        out.append(err(path, f"kind must be one of {SUGGEST_KINDS}"))
    if obj.get("status") not in STATUSES:
        out.append(err(path, f"status must be one of {STATUSES}"))
    if not str(obj.get("body", "")).strip():
        out.append(err(path, "empty body (say exactly what changes)"))
    if not str(obj.get("grounds", "")).strip():
        out.append(err(path, "empty grounds (grammar/witness/reason — proposals without grounds are votes, not scholarship)"))
    for i, s in enumerate(obj.get("supports", [])):
        p = f"{path}.supports[{i}]"
        if not isinstance(s, dict) or not s.get("by") or not s.get("date"):
            out.append(err(p, "supports need {by, date[, note]}"))
    if obj.get("status") == "accepted" and not obj.get("merged_as"):
        out.append(err(path, "accepted requires merged_as (history entry id / commit the merge wrote)"))
    if obj.get("status") == "rejected" and not str(obj.get("reason", "")).strip():
        out.append(err(path, "rejected requires reason (closed PRs explain why)"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED}
