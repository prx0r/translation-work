#!/usr/bin/env python3
"""Optional offline Vidyut candidates from one pinned source passage.

This never writes canonical data. Provide separately licensed metre data yourself.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import sys
import tempfile
from pathlib import Path

import style_profile

SUPPORTED_VERSION = '0.4.0'


def analyze(work: str, target: str, scheme: str, meters: str | None = None) -> dict:
    if work == 'ghatakarpara':
        raise ValueError('Ghaṭakarpara source alignment is withheld pending repair')
    try:
        version = importlib.metadata.version('vidyut')
        from vidyut.lipi import Scheme, transliterate
    except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
        raise ValueError('Install the optional vidyut==0.4.0 package first') from exc
    if version != SUPPORTED_VERSION:
        raise ValueError(f'Expected vidyut {SUPPORTED_VERSION}; found {version}')
    context = style_profile.source_context(work, target, 'l3')
    source = context['source_excerpt']
    src = {'iast': Scheme.Iast, 'devanagari': Scheme.Devanagari}.get(scheme)
    if src is None:
        raise ValueError('Input scheme must be iast or devanagari')
    slp = transliterate(source, src, Scheme.Slp1)
    result = {
        'format': 'svatantrya.vidyut-candidates/1', 'status': 'machine-generated-unreviewed',
        'work': work, 'target': target, 'source_sha256': context['source_sha256'],
        'source_lines': context.get('source_lines'), 'source_byte_span': context.get('source_byte_span'),
        'source_excerpt': source, 'source_scheme': scheme, 'slp1_candidate': slp,
        'generator': {'name': 'vidyut', 'version': version},
        'warning': 'Computational candidates only; verify the source span, script and every analysis independently.'
    }
    if meters:
        from vidyut.chandas import Chandas
        path = Path(meters)
        raw = path.read_bytes()
        if not raw or len(raw) > 2_000_000:
            raise ValueError('Meter file must be nonempty and no larger than 2 MB')
        # Classify the exact bytes that were fingerprinted, even if the original changes.
        with tempfile.NamedTemporaryFile() as pinned:
            pinned.write(raw)
            pinned.flush()
            match = Chandas(pinned.name).classify(slp)
        result['meter_candidate'] = {'name_slp1': match.padya,
            'syllables': [[{'text': a.text, 'weight': a.weight} for a in row] for row in match.aksharas],
            'meter_data_sha256': hashlib.sha256(raw).hexdigest(),
            'warning': 'Experimental classification; a partial or absent match is not a verified metre.'}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--scheme', choices=['iast', 'devanagari'], default='iast')
    parser.add_argument('--meters', help='Path to separately sourced, licensed Vidyut-compatible meters.tsv')
    args = parser.parse_args()
    try:
        result = analyze(args.work, args.target, args.scheme, args.meters)
    except (ValueError, OSError, KeyError) as exc:
        print(f'vidyut candidates: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
