#!/usr/bin/env python3
"""Read-only OpenPāṭala → translation layers → SanskritBench → essay audit.

A receipt records observations, not a proof of meaning or an approval to publish.
See BENCH-LINEAGE.md for the pinned inputs, limitations and replay instructions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import scholar
import workcfg

FORMAT = 'svatantrya-lineage-audit/1'
BENCH_COMMIT = 'cb5981b66fb7fc7a3bd8636352588bd8a4c42cad'
BENCH_SHA = '8549018f1db7e4e1835f4007163cdd4cc5771699d335cf05c503e316b15682fa'
LAYERS = ('t1', 'l0', 'argmap', 'l2', 'c1', 'l3', 'l4', 'c2')
REQUIRED = {'t1', 'l0', 'argmap', 'l2', 'c1'}


class AuditError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def object_sha(obj) -> str:
    return digest(canonical(obj))


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if result.returncode:
        raise AuditError(f'Git cannot resolve {args[0]} in {repo}')
    return result.stdout


def committed_file(path: Path) -> dict:
    """Bind bytes to a locally available Git commit; fail on a dirty file."""
    path = path.resolve(strict=True)
    base = Path(git(path.parent, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    try:
        relative = path.relative_to(base).as_posix()
    except ValueError as exc:
        raise AuditError('source path is outside its Git repository') from exc
    commit = git(base, 'rev-parse', 'HEAD').decode().strip()
    content = path.read_bytes()
    if git(base, 'show', f'{commit}:{relative}') != content:
        raise AuditError(f'file differs from committed Git bytes: {relative}')
    return {'commit': commit, 'path': relative, 'sha256': digest(content)}


def load_benchmark(bench_root: Path):
    path = bench_root.resolve() / 'pipeline' / 'translation_proof.py'
    try:
        code = path.read_bytes()
    except OSError as exc:
        raise AuditError(f'SanskritBench kernel unavailable: {exc}') from exc
    if digest(code) != BENCH_SHA:
        raise AuditError('SanskritBench kernel does not match the pinned SHA-256')
    recorded = committed_file(path)
    # A checkout newer than the pinned commit is acceptable only when the precise
    # audited bytes are also present at the pinned commit and in the worktree.
    if git(bench_root, 'show', f'{BENCH_COMMIT}:pipeline/translation_proof.py') != code:
        raise AuditError('SanskritBench bytes do not match the pinned commit')
    namespace = {'__name__': 'pinned_sanskritbench_kernel'}
    exec(compile(code, str(path), 'exec'), namespace)
    return namespace['verify_translation'], {'repository': 'prx0r/sanskritbench',
          'pinned_commit': BENCH_COMMIT, 'kernel_sha256': BENCH_SHA,
          'checkout_commit': recorded['commit']}


def source_candidate(work: str, source_path: Path, openpatala_root: Path) -> dict:
    mapping = ROOT / 'source-maps' / f'{work}.json'
    if not mapping.exists():
        return {'status': 'UNMAPPED', 'witness': 'UNKNOWN'}
    try:
        spec = json.loads(mapping.read_bytes())
        if spec.get('format') != 'openpatala-source-candidate/1' or spec.get('work') != work:
            raise AuditError('invalid source candidate map')
        source = source_path.read_bytes()
        if digest(source) != spec['source_file_sha256'] or spec['source_header'] not in source.decode('utf-8').splitlines():
            raise AuditError('source file no longer matches the candidate map')
        base = openpatala_root.resolve(strict=True)
        dossier = (base / spec['openpatala_dossier']).resolve(strict=True)
        dossier.relative_to(base)
        raw = dossier.read_bytes()
        if digest(raw) != spec['openpatala_dossier_sha256']:
            raise AuditError('OpenPāṭala dossier does not match the pinned digest')
        data = json.loads(raw)
        expected = (spec['external_identifier_scheme'], spec['external_identifier'])
        ids = {(x.get('scheme'), x.get('identifier')) for x in data.get('external_identifiers', [])}
        if data.get('work_id') != spec['openpatala_work_id'] or expected not in ids:
            raise AuditError('OpenPāṭala work or external identifier does not match')
        recorded = committed_file(dossier)
        languages = sorted({str(x.get('literal')) for x in data.get('assertions', [])
                            if x.get('predicate') == 'LANGUAGE'})
        return {'status': 'CANDIDATE', 'witness': 'UNKNOWN', 'edition_verified': False,
                'map_sha256': digest(mapping.read_bytes()), 'dossier': recorded,
                'work_id': data['work_id'], 'external_identifier': list(expected),
                'language_assertions': languages,
                'language_conflict': bool(languages and 'sa' not in languages)}
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise AuditError(f'OpenPāṭala candidate unavailable or invalid: {exc}') from exc


def layer_snapshot(work: str, song: str, source_spans: dict, verses: list[int]) -> tuple[dict, dict]:
    data = ROOT / work / 'data'
    layers = {}
    for name in LAYERS:
        path = data / f'{song}.{name}.json'
        if path.exists():
            raw = path.read_bytes()
            value = json.loads(raw)
            layers[name] = {'file_sha256': digest(raw), 'canonical_json_sha256': object_sha(value)}
    missing = sorted(REQUIRED - layers.keys())
    proof_path = ROOT / work / 'proof' / f'proof-{song}.json'
    proof = json.loads(proof_path.read_bytes()) if proof_path.exists() else None
    historical_source = digest(' '.join(' '.join(source_spans[v]) for v in sorted(verses)).encode())[:16]
    recorded_layers = (proof or {}).get('layer_sha256', {})
    changed = sorted(k for k in set(recorded_layers) | set(layers)
                     if recorded_layers.get(k) != layers.get(k, {}).get('canonical_json_sha256'))
    if proof is None:
        state = 'MISSING'
    elif missing or changed or proof.get('source_sha') != historical_source:
        state = 'STALE_OR_INCOMPLETE'
    else:
        state = 'RECORDED_LAYER_AND_SOURCE_HASHES_MATCH'
    return layers, {'status': state, 'missing_required_layers': missing, 'changed_layers': changed,
                    'historical_source_sha16': historical_source,
                    'recorded_source_sha16': (proof or {}).get('source_sha'),
                    'recorded_gate': (proof or {}).get('deterministic_gate'),
                    'proof_file_sha256': digest(proof_path.read_bytes()) if proof else None,
                    'note': 'Only recorded JSON layer and normalized-source hashes were compared. Markdown inputs and the historical proof were not rerun.'}


def essay_link(path: Path | None, work: str, target: str, t1_sha: str) -> dict:
    if path is None:
        return {'status': 'NOT_REQUESTED'}
    base = (ROOT / work / 'scholar' / 'essays').resolve()
    try:
        path = path.resolve(strict=True)
        path.relative_to(base)
        essay = json.loads(path.read_bytes())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise AuditError(f'essay must be a public saved essay for this work: {exc}') from exc
    errors = scholar.essay_errors(essay, work, path.name)
    citations = essay.get('snapshot', {}).get('content', {}).get('citations', [])
    match = [c for c in citations if isinstance(c, dict) and c.get('work') == work and c.get('target') == target]
    status = 'INVALID' if errors else ('UNLINKED' if not match else
             'PARTIAL_T1_MATCH' if match[0].get('t1_sha256') == t1_sha else 'T1_MISMATCH')
    return {'status': status, 'path': path.relative_to(ROOT).as_posix(),
            'file_sha256': digest(path.read_bytes()), 'essay_id': essay.get('essay_id'),
            'validation_errors': errors, 'identity_state': essay.get('identity_state'),
            'source_git_commit': essay.get('source_git_commit'),
            'note': 'Self-attested sign-off is not a digital signature or peer review. A matching citation alone does not verify the cited projection or entailment.'}


def audit(work: str, target: str, bench_root: Path, openpatala_root: Path,
          essay_path: Path | None = None) -> dict:
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}', work):
        raise AuditError('invalid work')
    match = re.fullmatch(r'([a-z0-9][a-z0-9_-]*)-v(\d+)', target)
    if not match:
        raise AuditError('target must be a song verse ID, for example param-p01-v01')
    song, verse = match.group(1), int(match.group(2))
    if work not in workcfg.WORKS or song not in workcfg.WORKS[work].get('songs', {}):
        raise AuditError('work or song is not registered with canonical workcfg')
    verses = workcfg.song_verses(work, song)
    spans = workcfg.source_spans(work)
    if not spans or verse not in verses or not set(verses).issubset(spans):
        raise AuditError('source spans for this song are unavailable or incomplete')
    source_path = Path(workcfg.WORKS[work]['source'])
    source_git = committed_file(source_path)
    candidate = source_candidate(work, source_path, openpatala_root)
    data = ROOT / work / 'data'
    try:
        t1 = json.loads((data / f'{song}.t1.json').read_bytes())
        l2 = json.loads((data / f'{song}.l2.json').read_bytes())
        t1_rows = [x for x in t1 if x.get('verse_id') == target and x.get('verse') == verse]
        l2_rows = [x for x in l2 if x.get('verse_id') == target and x.get('verse') == verse]
        if len(t1_rows) != 1 or len(l2_rows) != 1 or not isinstance(l2_rows[0].get('plain_english'), str):
            raise AuditError('expected exactly one T1 and one L2 row for the target')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise AuditError(f'translation layers unavailable: {exc}') from exc
    source_text = ' '.join(spans[verse])
    if not source_text.strip() or not l2_rows[0]['plain_english'].strip():
        raise AuditError('empty source or candidate')
    layers, historic = layer_snapshot(work, song, spans, verses)
    validate = subprocess.run([sys.executable, str(ROOT / 'tools/validate_song.py'), '--work', work, '--song', song],
                              cwd=ROOT, capture_output=True, text=True)
    try:
        validation = json.loads(validate.stdout)
    except json.JSONDecodeError:
        validation = {'errors': ['validator did not return JSON'], 'counts': {}}
    structural = {'status': 'PASS' if validate.returncode == 0 and not validation.get('errors') else 'BLOCKED',
                  'errors': validation.get('errors', []), 'counts': validation.get('counts', {}),
                  'python_version': '.'.join(str(v) for v in sys.version_info[:3]),
                  'program_sha256': {
                      p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
                      for p in [ROOT / 'tools/validate_song.py', ROOT / 'tools/workcfg.py',
                                ROOT / 'tools/proof_record.py', *sorted((ROOT / 'schemas').glob('*.py'))]},
                  'signoff_file_sha256': digest((data / f'{song}.signoff.json').read_bytes())
                      if (data / f'{song}.signoff.json').exists() else None}
    verify, bench = load_benchmark(bench_root)
    raw = verify(source_text, l2_rows[0]['plain_english'])
    # Do not propagate the kernel's misleading proof flag, result ID or prose
    # descriptions of heuristic checks as established facts.
    checks = {name: {k: v for k, v in row.items() if k in ('PASS', 'ratio', 'issues', 'ungrounded')}
              for name, row in raw['checks'].items()}
    t1_sha = object_sha(t1_rows[0])
    result = {
        'format': FORMAT,
        'scope': {'work': work, 'song': song, 'target': target, 'candidate_layer': 'l2'},
        'source': {'repository_file': source_git, 'openpatala': candidate,
                   'extracted_verse_sha256': digest(source_text.encode()),
                   'extraction': 'workcfg whitespace-token reconstruction', 'byte_exact_span': 'UNKNOWN',
                   'workcfg_sha256': digest((ROOT / 'tools/workcfg.py').read_bytes())},
        'translation': {'layers': layers, 't1_row_sha256': t1_sha,
                        'l2_row_sha256': object_sha(l2_rows[0]),
                        'l2_text_sha256': digest(l2_rows[0]['plain_english'].encode()),
                        'historical_record': historic, 'structural_validation': structural},
        'benchmark': {**bench, 'usage': 'ADVISORY_HEURISTICS_ONLY',
                      'reported_gate': raw['deterministic_gate'], 'checks': checks,
                      'gold': 'NOT_EVALUATED'},
        'essay': essay_link(essay_path, work, target, t1_sha),
        'claims': {'semantic_fidelity': 'UNKNOWN', 'full_source_coverage': 'UNKNOWN',
                   'witness_authenticated': 'UNKNOWN', 'human_review': 'UNKNOWN',
                   'publication_authorized': False},
        'overall': 'INCOMPLETE',
        'auditor_sha256': digest(Path(__file__).read_bytes()),
        'hash_scheme': 'sha256 over UTF-8; JSON uses sorted keys, compact separators, ensure_ascii=false',
    }
    result['receipt_sha256'] = object_sha(result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    run = sub.add_parser('run')
    run.add_argument('--work', required=True)
    run.add_argument('--target', required=True)
    run.add_argument('--essay', type=Path)
    run.add_argument('--output', type=Path, help='new file within this repository; never overwrites')
    check = sub.add_parser('verify')
    check.add_argument('receipt', type=Path)
    for p in (run, check):
        p.add_argument('--bench-root', type=Path, required=True)
        p.add_argument('--openpatala-root', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == 'run':
            result = audit(args.work, args.target, args.bench_root, args.openpatala_root, args.essay)
            encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
            if args.output:
                path = args.output.resolve()
                path.relative_to(ROOT)
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('x', encoding='utf-8') as f:
                    f.write(encoded)
            else:
                print(encoded, end='')
        else:
            saved = json.loads(args.receipt.read_bytes())
            receipt_sha = saved.pop('receipt_sha256', None)
            if saved.get('format') != FORMAT or object_sha(saved) != receipt_sha:
                raise AuditError('receipt digest or format does not match')
            scope = saved['scope']
            essay = saved['essay'].get('path')
            fresh = audit(scope['work'], scope['target'], args.bench_root, args.openpatala_root,
                          ROOT / essay if essay else None)
            if fresh['receipt_sha256'] != receipt_sha:
                raise AuditError('current inputs or results do not match this receipt')
            print(json.dumps({'status': 'MATCH', 'receipt_sha256': receipt_sha}))
        return 0
    except (AuditError, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'lineage audit: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
