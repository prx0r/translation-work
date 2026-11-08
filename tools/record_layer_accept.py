#!/usr/bin/env python3
"""tools/record_layer_accept.py — append layer-accept decisions at ingest.

Every layer acceptance (machine-proposed) writes one row per layer to
<work>/scholar/decisions.jsonl so the decision trail exists where the
layers are made — not reconstructed later. Rows are MACHINE-PROPOSED with
grounds (gate result, layer bytes sha, proof sha + tool version); only a
human review + sign-off promotes them. Re-running with identical layer
bytes appends nothing (idempotent).

  python3 tools/record_layer_accept.py --work phrdaya --song phr-p01
  python3 tools/record_layer_accept.py --work phrdaya --song phr-p01 --dry-run

Row: {"format":"translation-decision/1","subject":"layer-accept:<work>:
<target>:<layer>:<stem>", ...}. Never overwrites, never deletes; append-only.
Only song-scoped files are recorded (whole-work files like ARGMAP.md are
flagged as such in scope_note); missing files mean no row, never a guess.
Importable: proof_record.py calls record() at ingest time.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import workcfg  # noqa: E402

TOOL_VERSION = "record_layer_accept v1 2026-11-08"


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def record(work: str, song: str, dry_run: bool = False):
    """Append missing layer-accept rows. Returns (n_new, n_scanned, path)."""
    target = workcfg.chunk_id_for(work, song) or song
    wdir = ROOT / work
    if not wdir.is_dir():
        raise ValueError(f"no such work: {work}")

    proof_path = wdir / "proof" / f"proof-{song}.json"
    proof = None
    if proof_path.is_file():
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
    gate = (proof or {}).get("deterministic_gate", "UNKNOWN")
    blocking = (proof or {}).get("blocking", [])

    candidates: list[tuple[str, Path, str]] = [
        ("T1", wdir / f"working-t1-{song}.json", ""),
        ("L0", wdir / f"working-l0-{song}.json", ""),
        ("L2", wdir / f"L2-{target}.md", ""),
        ("L2", wdir / f"L2-{song}.md", ""),
        ("L2", wdir / "data" / f"{target}.l2.json", ""),
        ("L2", wdir / "data" / f"{song}.l2.json", ""),
        ("C1", wdir / f"C1-{target}.md", ""),
        ("C1", wdir / f"C1-{song}.md", ""),
        ("C1", wdir / "c1" / f"C1-{target}.md", ""),
        ("C1", wdir / "data" / f"{target}.c1.json", ""),
        ("ARGMAP", wdir / "ARGMAP.md", "whole file; chunk section only"),
        ("proof", proof_path, ""),
    ]
    uniq: list[tuple[str, Path, str]] = []
    seen = set()
    for layer, p, note in candidates:
        if not p.is_file() or (layer, p.name) in seen:
            continue
        seen.add((layer, p.name))
        uniq.append((layer, p, note))

    dec_path = wdir / "scholar" / "decisions.jsonl"
    existing = []
    if dec_path.is_file():
        for line in dec_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    existing.append(json.loads(line))
                except ValueError:
                    continue
    have = {(r.get("subject"), r.get("layer_sha256"))
            for r in existing if isinstance(r, dict)}

    now = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    new_rows = []
    for layer, p, note in uniq:
        digest = sha_file(p)
        subject = f"layer-accept:{work}:{target}:{layer}:{p.stem}"
        if (subject, digest) in have:
            continue
        new_rows.append({
            "format": "translation-decision/1",
            "subject": subject,
            "work": work,
            "target": target,
            "layer": layer,
            "path": str(p.relative_to(ROOT)),
            "scope_note": note,
            "layer_sha256": digest,
            "grounds": {
                "deterministic_gate": gate,
                "blocking": blocking,
                "proof_tool": (proof or {}).get("tool"),
                "proof_sha256": (sha_file(proof_path)
                                 if proof_path.is_file() else None),
            },
            "proposed_by": "translation-work machine ingest",
            "tool": TOOL_VERSION,
            "at": now,
            "status": "machine-proposed",
            "needs": "human review + sign-off (scholar)",
        })
    if dry_run:
        return new_rows, len(uniq), dec_path
    if new_rows:
        dec_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dec_path, "a", encoding="utf-8") as f:
            for r in new_rows:
                f.write(json.dumps(r, ensure_ascii=False,
                                   sort_keys=True) + "\n")
    return new_rows, len(uniq), dec_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", required=True)
    ap.add_argument("--song", required=True,
                    help="song id (chunk-song-map resolves the chunk target)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        new_rows, scanned, dec_path = record(a.work, a.song,
                                             dry_run=a.dry_run)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if a.dry_run:
        print(f"dry-run: {len(new_rows)} new decision rows "
              f"({scanned} layers scanned)")
        for r in new_rows:
            print(f"  + {r['subject']}")
        return 0
    rel = dec_path.relative_to(ROOT) if dec_path.exists() or True else dec_path
    print(f"recorded {len(new_rows)} layer-accept decisions "
          f"({scanned} layers scanned) -> {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
