"""schemas — the canonical translation-stack data-object schemas (versioned).

Single import point. SCHEMA_VERSION is the contract version: validators stamp it into
every record they check; check.py refuses to run mixed versions without an explicit
migration note in STATUS. Additive changes bump minor; breaking changes bump major
and require re-validation of all data/*.json.
"""
from __future__ import annotations

SCHEMA_VERSION = "1.1.0"

LAYER_ORDER = ["t1", "l0", "argmap", "l2", "c1", "c2"]

# Every file that defines the canonical stack. check.py verifies all of these exist
# and that the validators they contain execute without error.
CANONICAL_FILES = [
    "LAYERS.md",
    "ALIGNMENT.md",
    "schemas/__init__.py",
    "schemas/base.py",
    "schemas/t1.py",
    "schemas/l0.py",
    "schemas/argmap.py",
    "schemas/l2.py",
    "schemas/c1.py",
    "tools/emit_data.py",
    "tools/validate_song.py",
    "schemas/c2.py",
    "tools/render_md.py",
    "tools/proof_record.py",
    "tools/proof-disp.json",
    "skills/crystal-ipvv/SKILL.md",
    "lore/rasa/abhinavagupta-rasa-grounding-2026-11-01.md",
    "CHAT.md",
    "DATATYPES.json",
    "skills/crystal-ipvv/EXAMPLES.md",
    "lore/ipvv-deepdive-2026-11-01.md",
]


def get_version() -> str:
    return SCHEMA_VERSION
