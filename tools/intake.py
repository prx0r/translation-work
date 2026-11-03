#!/usr/bin/env python3
"""Initialize a new work from a pinned UTF-8 source and explicit byte spans.

Each segment has song, verse, verse_id, start, and end. Offsets are zero-based
UTF-8 byte offsets, with end exclusive. Every non-whitespace byte must be covered.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def validate_segments(raw: bytes, segments) -> list[str]:
    errors = []
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return ["source must be UTF-8"]
    if not isinstance(segments, list) or not segments:
        return ["segments must be a non-empty list"]
    previous, verse_ids, verse_numbers = 0, set(), set()
    for index, segment in enumerate(segments):
        label = f"segment {index + 1}"
        if not isinstance(segment, dict):
            errors.append(f"{label} must be an object")
            continue
        start, end = segment.get("start"), segment.get("end")
        verse, song, verse_id = segment.get("verse"), segment.get("song"), segment.get("verse_id")
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
            errors.append(f"{label} needs integer start and end offsets")
            continue
        if not (previous <= start < end <= len(raw)):
            errors.append(f"{label} offsets overlap, are unordered, or are out of range")
            continue
        try:
            gap, text = raw[previous:start].decode("utf-8"), raw[start:end].decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{label} offsets must end at UTF-8 character boundaries")
            continue
        if gap.strip():
            errors.append(f"{label} leaves non-whitespace source text uncovered")
        if not text.strip():
            errors.append(f"{label} is empty")
        if not isinstance(verse, int) or isinstance(verse, bool) or verse < 1 or verse in verse_numbers:
            errors.append(f"{label} needs a unique positive verse number")
        else:
            verse_numbers.add(verse)
        if not isinstance(song, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", song):
            errors.append(f"{label} has an invalid song ID")
        elif not isinstance(verse_id, str) or not re.fullmatch(re.escape(song) + r"-v\d+", verse_id):
            errors.append(f"{label} verse_id must be <song>-v<number>")
        elif int(verse_id.rsplit("-v", 1)[1]) != verse or verse_id in verse_ids:
            errors.append(f"{label} verse_id must match its unique verse number")
        else:
            verse_ids.add(verse_id)
        previous = end
    try:
        if raw[previous:].decode("utf-8").strip():
            errors.append("source has uncovered text after the final segment")
    except UnicodeDecodeError:
        errors.append("final segment ends inside a UTF-8 character")
    return errors


def initialize(root: Path, work: str, raw: bytes, segments, edition: str,
               source_license: str, source_url: str = "") -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", work or ""):
        raise ValueError("work must be a lowercase slug")
    if not edition.strip() or not source_license.strip():
        raise ValueError("edition and source-license statements are required")
    errors = validate_segments(raw, segments)
    if errors:
        raise ValueError("; ".join(errors))
    destination = root / work
    if destination.exists():
        raise ValueError(f"work already exists: {work}")
    temp = Path(tempfile.mkdtemp(prefix=".intake-", dir=root))
    try:
        source_dir = temp / "source"
        source_dir.mkdir()
        (temp / "data").mkdir()
        (temp / "proof").mkdir()
        (source_dir / "edition.txt").write_bytes(raw)
        segment_bytes = json.dumps(segments, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8")
        (source_dir / "segments.json").write_bytes(segment_bytes)
        manifest = {"format": "source-intake/1", "work": work, "edition": edition,
                    "source_license": source_license, "source_url": source_url,
                    "source_sha256": hashlib.sha256(raw).hexdigest(),
                    "segments_sha256": hashlib.sha256(segment_bytes).hexdigest(),
                    "status": "SOURCE_PREPARED"}
        (source_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        os.rename(temp, destination)
    finally:
        if temp.exists():
            shutil.rmtree(temp)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--segments", required=True)
    parser.add_argument("--edition", required=True)
    parser.add_argument("--source-license", required=True)
    parser.add_argument("--source-url", default="")
    args = parser.parse_args()
    try:
        raw = Path(args.source).read_bytes()
        segments = json.loads(Path(args.segments).read_text(encoding="utf-8"))
        path = initialize(ROOT, args.work, raw, segments, args.edition,
                          args.source_license, args.source_url)
        print(json.dumps({"work": args.work, "source_sha256": hashlib.sha256(raw).hexdigest(),
                          "segments": len(segments), "directory": str(path),
                          "next": "Follow skills/crystal-ipvv/SKILL.md, beginning with T1"}))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
