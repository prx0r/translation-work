"""schemas.argmap — verse-argument objects (the sharp translation's reasoning)."""
from __future__ import annotations
try:
    from .base import err, check_required, check_type
except ImportError:
    from base import err, check_required, check_type

REQUIRED = ["verse_id", "song", "verse", "traces", "sanskrit_sha"]
TRACES_REQUIRED = ["t1_verse", "l0_ids"]


def validate(obj: dict, path: str = "argmap", l0_ids: set | None = None,
             t1_verses: set | None = None, source_sha: str | None = None,
             l0_by_id: dict | None = None) -> list[str]:
    out = check_required(obj, REQUIRED, path)
    if not isinstance(obj, dict):
        return [err(path, "must be an object")]
    out += check_type(obj, "premises", list, path)
    out += check_type(obj, "uncertainties", list, path)
    structured = obj.get("structured", True)
    if structured:
        for f in ["speaker", "question", "inference"]:
            if f not in obj:
                out.append(err(path, f"structured argmap missing '{f}'"))
        if not obj.get("premises"):
            out.append(err(path, "empty premises (reconstruct the argument, not the sentence)"))
        if not obj.get("inference", "").strip():
            out.append(err(path, "empty inference"))
    else:
        if not obj.get("reconstruction", "").strip():
            out.append(err(path, "unstructured argmap requires reconstruction prose"))
    tr = obj.get("traces", {})
    if isinstance(tr, dict):
        out += check_required(tr, TRACES_REQUIRED, f"{path}.traces")
        if obj.get("scope", "verse") not in ("verse", "passage"):
            out.append(err(path, "scope must be verse|passage (default verse)"))
        if t1_verses is not None and tr.get("t1_verse") not in t1_verses:
            out.append(err(f"{path}.traces", f"t1_verse {tr.get('t1_verse')} not in T1 set"))
        if l0_ids is not None:
            for lid in tr.get("l0_ids", []):
                if lid not in l0_ids:
                    out.append(err(f"{path}.traces", f"l0_id {lid} does not exist"))
    else:
        out.append(err(f"{path}.traces", "must be an object"))
    if source_sha is not None and obj.get("sanskrit_sha") != source_sha:
        out.append(err(path, "sanskrit_sha mismatch (argmap built against a different source slice)"))
    # option_choices: the "other gloss fits better" record. When argmap adjudicates
    # between L0 options, the decision + reason live here — never silently in prose.
    for i, ch in enumerate(obj.get("option_choices", [])):
        p = f"{path}.option_choices[{i}]"
        if not isinstance(ch, dict):
            out.append(err(p, "must be an object")); continue
        out += check_required(ch, ["l0_id", "chosen_index", "reason"], p)
        if l0_ids is not None and ch.get("l0_id") not in (l0_ids or set()):
            out.append(err(p, f"l0_id {ch.get('l0_id')} does not exist"))
        if l0_by_id is not None and ch.get("l0_id") in l0_by_id:
            lo = l0_by_id[ch["l0_id"]]
            if ch.get("chosen_index") != lo.get("chosen_index"):
                out.append(err(p, f"chosen_index {ch.get('chosen_index')} != "
                                  f"L0 chosen_index {lo.get('chosen_index')} (argmap decision IS the L0 choice)"))
            for r in ch.get("rejected", []):
                if not any(r == o.get("gloss") for o in lo.get("options", [])):
                    out.append(err(p, f"rejected {r!r} is not an L0 option for {ch['l0_id']}"))
        if not str(ch.get("reason", "")).strip():
            out.append(err(p, "empty reason (why this gloss fits better)"))
    # resolved forks in traces must be adjudicated here (T5: a resolved fork with no
    # option_choices entry is an undocumented decision)
    if l0_by_id is not None and isinstance(tr, dict):
        decided = {ch.get("l0_id") for ch in obj.get("option_choices", []) if isinstance(ch, dict)}
        for lid in tr.get("l0_ids", []):
            lo = l0_by_id.get(lid, {})
            if lo.get("fork") == "resolved" and lid not in decided:
                out.append(err(f"{path}.traces", f"{lid} fork:resolved but no option_choices entry"))
    return out


def to_json_schema() -> dict:
    return {"type": "object", "required": REQUIRED,
            "properties": {"verse_id": {"type": "string"}, "traces": {"type": "object",
                            "required": TRACES_REQUIRED}}}
