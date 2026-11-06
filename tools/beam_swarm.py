#!/usr/bin/env python3
"""beam_swarm — 3 cheap beam-free workers draft, assessor (me) decides.

Workers (nohup'd) pull tasks from process/beam/queue.json, draft with
beam-free, pydantic-validate the draft SHAPE, and park outputs for review.
Workers NEVER write canonical data/ and NEVER mark PASS. The assessor
reviews (beam_swarm.py review), approves into ipvv/pilot/ (or bounces with
a note the worker must address on retry).

Usage:
  python3 tools/beam_swarm.py init-queue        # seed demo batch (idempotent)
  nohup python3 tools/beam_swarm.py worker w1 > process/beam/w1.log 2>&1 &
  python3 tools/beam_swarm.py status
  python3 tools/beam_swarm.py review <task-id>
  python3 tools/beam_swarm.py approve <task-id> # pilot_pair only: pilot->ipvv/pilot/
  python3 tools/beam_swarm.py bounce <task-id> "note"
Needs $OPENCODE_GO_KEY for workers.
"""
from __future__ import annotations
import argparse, datetime, json, os, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
STATE = ROOT / 'process' / 'beam'
QFILE = STATE / 'queue.json'

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print('pydantic required', file=sys.stderr)
    raise SystemExit(2)

# ---------- schemas ----------

class Task(BaseModel):
    id: str
    kind: str  # pilot_pair | tal_brief | lore_queries | lore_distill | recon | tal_gloss | tal_cm | tal_am
    args: dict = Field(default_factory=dict)
    status: str = 'pending'  # pending|claimed|done|failed|approved|bounced
    attempts: int = 0
    max_attempts: int = 3
    worker: str = ''
    note: str = ''
    created: str = ''
    updated: str = ''


class PilotSelfCheck(BaseModel):
    has_question: bool
    has_sec2: bool
    has_sec4: bool
    premises_ge2: bool
    l2_nonempty: bool


class BriefItem(BaseModel):
    span: str  # e.g. "vv1-3"
    topic: str
    gist: str


class TalBrief(BaseModel):
    ahnika: str
    items: list[BriefItem] = Field(min_length=1)


class LoreQueries(BaseModel):
    topic: str
    queries: list[str] = Field(min_length=2, max_length=6)


class LoreBrief(BaseModel):
    topic: str
    moves: list[str] = Field(min_length=2)
    traps: list[str] = Field(min_length=1)
    approach: list[str] = Field(min_length=1)


class ReconSection(BaseModel):
    span: str  # e.g. "L100-L450"
    kind: str  # root-verse | commentary | colophon | paratext | apparatus
    note: str


class ReconReport(BaseModel):
    path: str
    bytes: int
    lines: int
    markers: dict[str, int]
    hypothesis: list[ReconSection] = Field(min_length=1)


class GlossRow(BaseModel):
    surface: str
    gloss: str
    grounds: str


class TalGloss(BaseModel):
    song: str
    verse: int
    rows: list[GlossRow] = Field(min_length=1)


class CmRow(BaseModel):
    lemma: str
    morph: str
    grounds: str


class TalCm(BaseModel):
    song: str
    verse: int
    rows: list[CmRow] = Field(min_length=1)


# ---------- queue ----------

_Q_LOCK = str(QFILE) + '.lock'

def _locked():
    """Cross-process exclusive lock for read-modify-write of queue.json."""
    import contextlib, fcntl
    @contextlib.contextmanager
    def cm():
        STATE.mkdir(parents=True, exist_ok=True)
        fh = open(_Q_LOCK, 'a+')
        try:
            fcntl.flock(fh, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
            fh.close()
    return cm()

def load_q() -> list[dict]:
    for _ in range(3):
        if not QFILE.exists():
            return []
        raw = QFILE.read_text()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # tolerate a torn tail left by a crashed writer: keep first doc
            try:
                obj, _end = json.JSONDecoder().raw_decode(raw)
                return obj
            except json.JSONDecodeError:
                time.sleep(0.2)
    raise RuntimeError('queue.json unreadable — repair needed')

def save_q(tasks: list[dict]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    # unique temp per writer: os.replace is atomic, but a SHARED temp path
    # lets two writers interleave into the same file (corruption 2026-11-06)
    tmp = QFILE.with_name(f'{QFILE.name}.{os.getpid()}.{time.time_ns()}.tmp')
    with open(tmp, 'w') as f:
        f.write(json.dumps(tasks, indent=1))
    os.replace(tmp, QFILE)

STALE_CLAIM_SECS = 15 * 60  # a claim older than this is dead; steal it

def claimable(t: dict) -> bool:
    if t['attempts'] >= t['max_attempts']:
        return False
    if t['status'] == 'pending':
        return True
    if t['status'] == 'claimed':
        # dead worker left it claimed: re-drive only if no live flag
        flag = STATE / 'claims' / (t['id'] + '.json')
        try:
            return time.time() - flag.stat().st_mtime >= STALE_CLAIM_SECS
        except FileNotFoundError:
            return True
    return False

def claim(tasks: list[dict], worker: str) -> dict | None:
    tasks = load_q()  # re-read under lock below
    for t in tasks:
        if claimable(t):
            flag = STATE / 'claims' / (t['id'] + '.json')
            try:
                fd = os.open(flag, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, json.dumps({'worker': worker}).encode())
                os.close(fd)
            except FileExistsError:
                try:
                    if time.time() - flag.stat().st_mtime < STALE_CLAIM_SECS:
                        continue
                    flag.unlink()  # stale: previous worker died
                except FileNotFoundError:
                    continue
                try:
                    fd = os.open(flag, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.write(fd, json.dumps({'worker': worker}).encode())
                    os.close(fd)
                except FileExistsError:
                    continue
            t['status'] = 'claimed'
            t['worker'] = worker
            t['attempts'] += 1
            t['updated'] = datetime.datetime.now().isoformat(timespec='seconds')
            with _locked():
                cur = {x['id']: x for x in load_q()}
                if t['id'] in cur:  # merge onto freshest state
                    cur[t['id']].update({'status': 'claimed', 'worker': worker,
                                         'attempts': cur[t['id']].get('attempts', 0) + 1,
                                         'updated': t['updated']})
                    save_q(list(cur.values()))
                else:
                    save_q(tasks)
            return t
    return None

def mark(tasks: list[dict], tid: str, status: str, note: str = '') -> None:
    with _locked():
        tasks = load_q()
        _mark_unlocked(tasks, tid, status, note)

def _mark_unlocked(tasks: list[dict], tid: str, status: str, note: str = '') -> None:
    for t in tasks:
        if t['id'] == tid:
            t['status'] = status
            if note:
                t['note'] = (t.get('note', '') + ' | ' + note).strip(' |')
            t['updated'] = datetime.datetime.now().isoformat(timespec='seconds')
    save_q(tasks)
    try:
        (STATE / 'claims' / (tid + '.json')).unlink()
    except FileNotFoundError:
        pass

# ---------- task impls ----------

TAL_SYS = ('You summarize Tantraloka passages for a translation pipeline. '
           'Output ONLY JSON matching the requested schema. No commentary. '
           'Machine-proposed; a scholar reviews.')

def run_pilot_pair(t: dict) -> tuple[bool, str]:
    lbl = t['args']['label']
    env = dict(os.environ)
    p = subprocess.run([sys.executable, 'tools/beam_pilot.py', '--label', lbl],
                       cwd=ROOT, capture_output=True, text=True, env=env, timeout=900)
    if p.returncode != 0:
        return False, (p.stdout + p.stderr)[-600:]
    return True, 'selfcheck gate in beam_pilot passed'

LORE_Q_SYS = ('You prepare scholarship searches for a Sanskrit translation project. '
                'Output ONLY JSON. No commentary.')

LORE_D_SYS = ('You distill search excerpts into a transmission brief for a drafter model. '
              'Output ONLY JSON matching the schema. Never invent citations; mark gaps.')


def run_lore_queries(t: dict) -> tuple[bool, str]:
    from beam_client import beam
    topic = t['args']['topic']
    context = t['args'].get('context', '')
    user = (f'Topic: {topic}\nContext: {context}\n\n'
            'Propose 2-6 web search queries that would surface the scholarship a drafter needs: '
            'editions, translations, key secondary literature, witnesses, known cruxes. '
            'Reply ONLY JSON: {"topic": "...", "queries": ["...", ...]}')
    text = beam(LORE_Q_SYS, user, session=f'lore-q-{t["id"]}', max_tokens=1500)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object: ' + text[:300]
    try:
        q = LoreQueries.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]}'
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'queries.json').write_text(q.model_dump_json(indent=1))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(q.queries)} queries (assessor executes searches next)'


def run_lore_distill(t: dict) -> tuple[bool, str]:
    from beam_client import beam
    topic = t['args']['topic']
    excerpts = t['args'].get('excerpts', '')
    if not excerpts or len(excerpts) < 200:
        return False, 'no excerpts yet — assessor pastes search results into args.excerpts, then requeue'
    user = (f'Topic: {topic}\n\nSEARCH EXCERPTS (may be thin — mark gaps, never invent):\n{excerpts[:25000]}\n\n'
            'Distill a transmission brief: what the text is (moves), traps (terms that look alike, '
            'nearby-but-different targets, print issues), approach (scope rules, honesty rules). '
            'Reply ONLY JSON: {"topic": "...", "moves": [...], "traps": [...], "approach": [...]}')
    text = beam(LORE_D_SYS, user, session=f'lore-d-{t["id"]}', max_tokens=2500)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object: ' + text[:300]
    try:
        b = LoreBrief.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]}'
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'brief.json').write_text(b.model_dump_json(indent=1))
    (outd / 'raw.txt').write_text(text)
    md = [f'# TRANSMISSION BRIEF — {b.topic}', '',
          '*Machine-distilled from search excerpts; ASSESSOR MUST REVIEW before use as packet lore.*', '']
    md += ['## Moves'] + [f'{i + 1}. {m}' for i, m in enumerate(b.moves)] + ['']
    md += ['## Traps'] + [f'- {x}' for x in b.traps] + ['']
    md += ['## Approach'] + [f'- {x}' for x in b.approach]
    (outd / 'LORE_BRIEF.md').write_text('\n'.join(md))
    return True, 'brief drafted — assessor review required before process/beam/lore/'


RECON_SYS = ('You survey a Sanskrit e-text for a translation pipeline. '
               'Output ONLY JSON matching the schema. Never invent verse counts; '
               'report what the markers show, flag ambiguity.')


def run_recon(t: dict) -> tuple[bool, str]:
    import re as _re
    from beam_client import beam
    path = t['args']['path']  # repo-relative or absolute
    p = (ROOT / path) if not path.startswith('/') else pathlib.Path(path)
    if not p.exists():
        return False, f'missing source {p}'
    raw = p.read_text()[:120000]
    lines = raw.splitlines()
    pats = {
        'dbl_pipe_num': r'\|\|\s*\d+\s*\|\|',
        'adhyaya': r'(?i)adhy[āa]ya',
        'sarga': r'(?i)sarga',
        'sloka_marker': r'//\s*[A-Za-zĀ-ž_]*\d+\s*//',
        'page_mark': r'\(p\.\s*\d+\)',
        'danda_pair': r'\|\|',
    }
    markers = {k: len(_re.findall(v, raw)) for k, v in pats.items()}
    head = '\n'.join(lines[:120])
    tail = '\n'.join(lines[-60:])
    user = (f"FILE: {path} ({p.stat().st_size} bytes, {len(lines)} lines)\n"
            f'MARKER CENSUS: {json.dumps(markers)}\n\nHEAD (120 lines):\n{head}\n\n'
            f'TAIL (60 lines):\n{tail}\n\n'
            'Hypothesize the document structure as line spans: root-verse vs commentary '
            'vs colophon vs paratext vs apparatus. '
            'Reply ONLY JSON: {"path": "...", "bytes": N, "lines": N, '
            '"markers": {...}, "hypothesis": [{"span": "Lx-Ly", "kind": "...", "note": "..."}]}')
    text = beam(RECON_SYS, user, session=f"recon-{t['id']}", max_tokens=3000)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object: ' + text[:300]
    try:
        rep = ReconReport.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]}'
    rep.path, rep.bytes, rep.lines, rep.markers = str(p), p.stat().st_size, len(lines), markers
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'recon.json').write_text(rep.model_dump_json(indent=1))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(rep.hypothesis)} sections (assessor verifies before intake)'


TAL_GLOSS_SYS = ('You gloss Sanskrit verse tokens for a translation pipeline. '
                 'Output ONLY JSON matching the schema. Glosses: lowercase English, '
                 'hyphen-joined, no parens, no quotes, max 6 parts. Grounds: morphology '
                 '+ which L1/L2 line supports it. Never invent; mark uncertainty in grounds.')


def run_tal_gloss(t: dict) -> tuple[bool, str]:
    import re as _re
    from beam_client import beam
    work, song, verse = t['args']['work'], t['args']['song'], int(t['args']['verse'])
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    entry = next(e for e in wt if e['verse'] == verse)
    surfs = [x['surface'] for x in entry['tokens']]
    ctx = t.get('args', {}).get('context', '')
    ahn = t['args'].get('ahnika') or (work.split('tantraloka-a')[-1] if work.startswith('tantraloka-a') else '')
    lore = ''
    lp = STATE / 'lore' / f'tal-{ahn}.md' if ahn else None
    if lp is not None and lp.exists():
        lore = lp.read_text()[:4000]
    prev = (t.get('note') or '').split(' | ')[-1]
    user = (f'Verse {verse} ({len(surfs)} tokens, hyphen-split compounds, @ marks sandhi):\n'
            + '\n'.join(f'{i}: {s}' for i, s in enumerate(surfs))
            + f'\n\nPASSAGE PROSE (L1/L2 reads — ground every gloss here):\n{ctx[:12000]}\n\n'
            + (f'TRANSMISSION BRIEF:\n{lore}\n\n' if lore else '')
            + (f'PREVIOUS ATTEMPT NOTE: {prev}\n\n' if prev and 'attempt failed' not in prev and len(prev) > 5 else '')
            + 'Gloss EVERY token in order. Reply ONLY JSON: {"song": "...", "verse": N, '
              '"rows": [{"surface": "...(exact)", "gloss": "...", "grounds": "..."}]}')
    text = beam(TAL_GLOSS_SYS, user, session=f'tal-gloss-{song}-v{verse}-001', max_tokens=6000)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object: ' + text[:300]
    try:
        g = TalGloss.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]}'
    rs = [r.surface for r in g.rows]
    if rs != surfs:
        return False, (f'surface drift: {len(rs)} rows vs {len(surfs)} tokens; '
                       f'first mismatch e.g. {next(((a, b) for a, b in zip(rs, surfs) if a != b), ("?", "?"))}')
    LEAK = ('genitive', 'nominative', 'accusative', 'instrumental', 'dative',
            'ablative', 'locative', 'vocative', 'singular', 'plural', 'dual',
            'participle', 'passive', 'causative', 'optative', 'imperative',
            'sandhi', 'compound')
    bad = [r.gloss for r in g.rows
           if not r.gloss or '(' in r.gloss or ')' in r.gloss or '"' in r.gloss
           or r.gloss != r.gloss.lower() or len(r.gloss.split('-')) > 8
           or any(w in r.gloss.lower().split('-') for w in LEAK)
           or not (r.grounds or '').strip()]
    if bad:
        return False, f'gloss/grounds format fail e.g. {bad[:3]}'
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'gloss.json').write_text(g.model_dump_json(indent=1, ensure_ascii=False))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(g.rows)} glosses'


TAL_CM_SYS = ('You analyze Sanskrit morphology for a translation pipeline. '
              'Output ONLY JSON matching the schema. Morphology: case.number.gender '
              '(m.nom.sg), verb person.number.voice-tense/mood + root (3sg.pres.mid √gam), '
              'indeclinables as (indecl.), compounds as member+membership. Grounds cite '
              'the gloss + form. If unsure, say so in grounds (AMBIGUOUS stays honest).')


def run_tal_cm(t: dict) -> tuple[bool, str]:
    from beam_client import beam
    work, song, verse = t['args']['work'], t['args']['song'], int(t['args']['verse'])
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    entry = next(e for e in wt if e['verse'] == verse)
    pairs = [(x['surface'], x.get('quick_gloss', '')) for x in entry['tokens']]
    if any(not g for _, g in pairs):
        # gloss results may live only in runs/ until the assemble stage
        gf = ROOT / 'process' / 'beam' / 'runs' / f"{song}-gloss-v{verse:02d}" / 'gloss.json'
        try:
            got = {r['surface']: r['gloss'] for r in json.loads(gf.read_text())['rows']}
            pairs = [(s_, got.get(s_, g_)) for s_, g_ in pairs]
        except (OSError, ValueError, KeyError):
            pass
    if any(not g for _, g in pairs):
        return False, 'glosses missing — run tal_gloss first'
    user = ('Verse tokens (surface = gloss):\n'
            + '\n'.join(f'{s} = {g}' for s, g in pairs)
            + '\n\nOne CM row per token IN ORDER: [lemma_iast, morph, grounds]. '
              'Reply ONLY JSON: {"song": "...", "verse": N, "rows": [{"lemma": "...", "morph": "...", "grounds": "..."}]}')
    text = beam(TAL_CM_SYS, user, session=f'tal-cm-{song}-v{verse}-001', max_tokens=6000)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object: ' + text[:300]
    try:
        c = TalCm.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]}'
    if len(c.rows) != len(pairs):
        return False, f'row count {len(c.rows)} vs {len(pairs)} tokens'
    if any(not r.lemma or not r.morph or not (r.grounds or '').strip() for r in c.rows):
        return False, 'empty lemma/morph/grounds present'
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'cm.json').write_text(c.model_dump_json(indent=1, ensure_ascii=False))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(c.rows)} CM rows'


class TalAm(BaseModel):
    song: str
    verse: int
    question: str
    premises: list[str] = Field(min_length=1)
    inference: str
    uncertainties: list[str] = Field(default_factory=list)
    plain_english: str


TAL_AM_SYS = ('You map and translate one Sanskrit verse (Tantraloka) for a '
              'pipeline. Output ONLY JSON. premises are terse logical statements '
              'in verse order; plain_english is a readable translation, no '
              'metacommentary; uncertainties are honest gaps. No certainty labels.\n'
              'The QUESTION is the question the verse itself answers, asked in the '
              "verse's own terms — e.g. \"Who is fit to be consecrated?\", "
              "\"What does the former guru retain after transmitting?\". "
              'BANNED question forms: "What does verse N state...", "What is being told?", '
              '"What is this verse about?". Minimum 5 words.')


def run_tal_am(t: dict) -> tuple[bool, str]:
    from beam_client import beam
    work, song, verse = t['args']['work'], t['args']['song'], int(t['args']['verse'])
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    e = next(x for x in wt if x['verse'] == verse)
    pairs = [(x['surface'], x.get('quick_gloss', '')) for x in e['tokens']]
    gf = ROOT / 'process' / 'beam' / 'runs' / f"{song}-gloss-v{verse:02d}" / 'gloss.json'
    if any(not g for _, g in pairs) and gf.exists():
        try:
            got = {r['surface']: r['gloss'] for r in json.loads(gf.read_text())['rows']}
            pairs = [(s_, got.get(s_, g_)) for s_, g_ in pairs]
        except (OSError, ValueError, KeyError):
            pass
    l0 = json.loads((ROOT / work / f'working-l0-{song}.json').read_text())
    morph = {}
    for o in l0:
        if o.get('verse_id', '').endswith(f'-v{verse:02d}'):
            morph[o['surface']] = o.get('morph', '')
    ahn = work.split('tantraloka-a')[-1]
    lp = STATE / 'lore' / f'tal-{ahn}.md'
    lore = lp.read_text()[:6000] if lp.exists() else ''
    prev = (t.get('note') or '').split(' | ')[-1]
    user = ('VERSE %d\n' % verse
            + '\n'.join(f'{s} = {g}   [{morph.get(s,"")}]' for s, g in pairs)
            + ('\n\nCONTEXT (prev verse): ' + t['args'].get('prev', '') if t['args'].get('prev') else '')
            + ('\n\nLORE (what this ahnika is doing):\n' + lore if lore else '')
            + (('\n\nFIX: ' + prev) if prev and 'attempt failed' not in prev and len(prev) > 5 else '')
            + '\n\nReply ONLY JSON: {"song":"...","verse":N,"question":"...",'
              '"premises":["..."],"inference":"...","uncertainties":["..."],'
              '"plain_english":"..."}')
    text = beam(TAL_AM_SYS, user, session=f'tal-am-{song}-v{verse}-001', max_tokens=6000)
    a, b = text.find('{'), text.rfind('}')
    if a < 0:
        return False, 'no JSON: ' + text[:200]
    try:
        d = TalAm.model_validate_json(text[a:b + 1])
    except ValidationError as ex:
        return False, f'schema fail: {ex.errors()[:2]}'
    probs = []
    lq = d.question.lower().strip()
    if not d.question.endswith('?'): probs.append('question must end ?')
    if len(d.question.split()) < 5: probs.append('question too short/empty')
    if 'does verse' in lq or 'this verse' in lq or 'is being told' in lq:
        probs.append('meta-question: ask the verse\'s own question in its own terms')
    if len(d.plain_english.split()) < 4: probs.append('l2 too short')
    if any(len(x.split()) < 3 for x in d.premises): probs.append('premise too short')
    if probs: return False, '; '.join(probs)
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'am.json').write_text(d.model_dump_json(indent=1, ensure_ascii=False))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(d.premises)} premises'


def run_tal_brief(t: dict) -> tuple[bool, str]:
    import re as _re
    from beam_client import beam
    ahn = t['args']['ahnika']  # e.g. a18
    wdir = ROOT / f'tantraloka-{ahn}'
    # Real GRETIL verse text via workcfg (primary); legacy L2 as secondary.
    import workcfg as _w
    try:
        verses_all = _w.song_verses(f'tantraloka-{ahn}', f'tal-{ahn}')
        spans_all = _w.source_spans(f'tantraloka-{ahn}')
    except KeyError:
        return False, f'unknown ahnika {ahn} in workcfg'
    lo, hi = int(t['args'].get('lo', verses_all[0])), int(t['args'].get('hi', verses_all[-1]))
    verses = [v for v in verses_all if lo <= v <= hi]
    lines = [f"v{v}: {' '.join(spans_all[v])}" for v in verses if v in spans_all]
    src = '\n'.join(lines)[:45000]
    want = set(verses)
    tag = f'{ahn}-vv{lo}-{hi}'
    l2 = ''
    for cand in (wdir / f'L2-tal-{ahn}.md', wdir / 'L2.md'):
        if cand.exists() and cand.stat().st_size > 2000:
            l2 = cand.read_text()[:15000]
            break
    prev = (t.get('note') or '').split(' | ')[-1]
    user = (f'AHNIKA {ahn} — WINDOW vv{lo}-{hi} (final verse of window: v{hi}). VERSE TEXT (vN: tokens):\n{src}\n\n'
            + (f'TRANSMISSION BRIEF (scholarly orientation — follow it):\n{(STATE / "lore" / f"tal-{ahn}.md").read_text()[:8000]}\n\n' if (STATE / 'lore' / f'tal-{ahn}.md').exists() else '')
            + (f'LEGACY ENGLISH READ (excerpt):\n{l2[:15000]}\n\n' if l2 else '')
            + (f'PREVIOUS ATTEMPT NOTE (fix this): {prev}\n\n' if prev and 'attempt failed' not in prev and len(prev) > 5 else '')
            + f'Partition THIS WINDOW ONLY (vv{lo}-{hi}) into passage spans of 1-8 verses each. '
              'Follow TOPIC shifts: a new span starts where the subject changes. '
              'Span format is EXACTLY vvA-B — e.g. vv61-64, or vv7-7 for a single verse. Never write bare numbers. '
              'NEVER emit uniform blocks — if spans look mechanical, repartition by topic. '
              'The last span MUST end at v{hi}. Cover every verse in the window, no gaps, no overlaps. '
              'For each: topic (<=8 words) and gist (1-2 sentences: what is argued). '
              'Reply ONLY with JSON: {"ahnika": "<id>", "items": [{"span":..., "topic":..., "gist":...}]}')
    text = beam(TAL_SYS, user, session=f'tal-brief-{tag}-001', max_tokens=8000)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object in reply: ' + text[:300]
    try:
        brief = TalBrief.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]} | raw: {text[start:start + 300]}'
    # coverage + variety gates (span prefixes normalized: vA-B -> vvA-B)
    covered: set[int] = set()
    lens: list[int] = []
    normed = 0
    for it in brief.items:
        s = it.span.strip()
        m = _re.fullmatch(r'vv(\d+)-(\d+)', s)
        if not m:
            m2 = _re.fullmatch(r'v(\d+)-v?(\d+)', s)
            if m2:
                it.span = f'vv{m2.group(1)}-{m2.group(2)}'
                m, normed = m2, normed + 1
            else:
                m3 = _re.fullmatch(r'v{0,2}(\d+)', s)
                if m3:  # bare verse number = single-verse span
                    it.span = f'vv{m3.group(1)}-{m3.group(1)}'
                    m, normed = m3, normed + 1
        if not m:
            return False, f'bad span format {it.span!r}; use vvA-B'
        a, b = int(m.group(1)), int(m.group(2))
        covered.update(range(a, b + 1))
        lens.append(b - a + 1)
    if want:
        missing = sorted(set(want) - covered)
        if len(covered & want) < 0.9 * len(want):
            return False, (f'coverage {len(covered & want)}/{len(want)} '
                           f'missing e.g. {missing[:8]}; partition EVERY verse 1-8 per span')
    if len(lens) > 5:
        from collections import Counter as _C
        top, cnt = _C(lens).most_common(1)[0]
        if cnt / len(lens) > 0.8:
            return False, (f'mechanical spans ({cnt}/{len(lens)} are length {top}); '
                           'repartition by TOPIC shifts, vary span lengths')
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'brief.json').write_text(brief.model_dump_json(indent=1))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(brief.items)} spans'

def worker_loop(name: str) -> int:
    from beam_client import chat  # noqa: F401  (fail fast if key missing)
    import beam_client as _b
    _b._key()
    while True:
        tasks = load_q()
        t = claim(tasks, name)
        if not t:
            print(f'[{name}] queue empty, exiting')
            return 0
        print(f'[{name}] claimed {t["id"]} ({t["kind"]}) try {t["attempts"]}', flush=True)
        try:
            if t['kind'] == 'pilot_pair':
                ok, msg = run_pilot_pair(t)
            elif t['kind'] == 'tal_brief':
                ok, msg = run_tal_brief(t)
            elif t['kind'] == 'lore_queries':
                ok, msg = run_lore_queries(t)
            elif t['kind'] == 'lore_distill':
                ok, msg = run_lore_distill(t)
            elif t['kind'] == 'recon':
                ok, msg = run_recon(t)
            elif t['kind'] == 'tal_gloss':
                ok, msg = run_tal_gloss(t)
            elif t['kind'] == 'tal_cm':
                ok, msg = run_tal_cm(t)
            elif t['kind'] == 'tal_am':
                ok, msg = run_tal_am(t)
            else:
                ok, msg = False, f'unknown kind {t["kind"]}'
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f'{type(e).__name__}: {str(e)[:300]}'
        tasks = load_q()
        if ok:
            mark(tasks, t['id'], 'done', msg)
            print(f'[{name}] done {t["id"]}: {msg}', flush=True)
        else:
            left = t['attempts'] < t['max_attempts']
            mark(tasks, t['id'], 'pending' if left else 'failed', f'attempt failed: {msg}')
            print(f'[{name}] fail {t["id"]}: {msg[:200]}', flush=True)
        time.sleep(2)

# ---------- CLI ----------

def cmd_init_queue() -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / 'claims').mkdir(exist_ok=True)
    (STATE / 'runs').mkdir(exist_ok=True)
    tasks = load_q()
    have = {t['id'] for t in tasks}
    now = datetime.datetime.now().isoformat(timespec='seconds')
    seed = [
        {'id': 'v3b-pilot', 'kind': 'pilot_pair', 'args': {'label': 'V3B'}},
        {'id': 'tal-a18-brief', 'kind': 'tal_brief', 'args': {'ahnika': 'a18'}},
        {'id': 'tal-a12-brief', 'kind': 'tal_brief', 'args': {'ahnika': 'a12'}},
    ]
    for s in seed:
        if s['id'] not in have:
            tasks.append(Task(id=s['id'], kind=s['kind'], args=s['args'],
                              created=now, updated=now).model_dump())
    save_q(tasks)
    print(f'queue: {len(tasks)} tasks')

def cmd_status() -> None:
    for t in load_q():
        print(f"{t['id']:16} {t['kind']:11} {t['status']:9} try={t['attempts']} worker={t.get('worker','')} :: {(t.get('note') or '')[:80]}")

def cmd_review(tid: str) -> None:
    t = next((x for x in load_q() if x['id'] == tid), None)
    if not t:
        print('unknown task'); return
    print(json.dumps(t, indent=1)[:800])
    if t['kind'] == 'pilot_pair':
        d = ROOT / 'ipvv' / 'cm' / 'beam' / t['args']['label']
        for f in ['selfcheck.json']:
            p = d / f
            if p.exists():
                print(f'--- {f} ---'); print(p.read_text()[:600])
        am = d / f"pilot_{t['args']['label']}_ARGUMENT_MAP.md"
        if am.exists():
            print(f'--- argmap head ({am.stat().st_size}B) ---')
            print(am.read_text()[:2500])
    elif t['kind'] in ('lore_queries', 'lore_distill'):
        for f in ['queries.json', 'brief.json', 'LORE_BRIEF.md']:
            p = STATE / 'runs' / tid / f
            if p.exists():
                print(f'--- {f} ---'); print(p.read_text()[:2500])
    elif t['kind'] == 'recon':
        for f in ['recon.json']:
            p = STATE / 'runs' / tid / f
            if p.exists():
                print(f'--- {f} ---'); print(p.read_text()[:3000])
    else:
        r = STATE / 'runs' / tid / 'brief.json'
        if r.exists():
            print(r.read_text()[:3000])

def cmd_approve(tid: str) -> None:
    tasks = load_q()
    t = next((x for x in tasks if x['id'] == tid), None)
    if not t or t['status'] != 'done':
        print('approve needs status=done'); return
    if t['kind'] == 'pilot_pair':
        lbl = t['args']['label']
        d = ROOT / 'ipvv' / 'cm' / 'beam' / lbl
        for f in [f'pilot_{lbl}_ARGUMENT_MAP.md', f'pilot_{lbl}_L2_read.md']:
            (ROOT / 'ipvv' / 'pilot' / f).write_text((d / f).read_text())
        print(f'placed pilot_{lbl}_* into ipvv/pilot/ — next: converter + validate + proof')
    mark(tasks, tid, 'approved', 'assessor approved')

def cmd_auto_review() -> None:
    """Assessor-batch for autonomy: re-verify DONE window briefs from disk and
    approve the ones that pass — EXCEPT a deterministic sample HELD for
    spot-read (every 5th by task-id hash + all full-ahnika briefs). Sampling
    is the only content check in this path; without it this is blind approval
    (mistakes.md #24). pilot_pair drafts are NEVER auto-approved (prose
    judgment required). Everything stays machine-proposed."""
    import hashlib as _h
    import re as _re
    from collections import Counter as _C
    tasks = load_q()
    n_app, n_skip = 0, []
    for t in tasks:
        if not (t['status'] == 'done' and t['kind'] == 'tal_brief'):
            continue
        if int(_h.sha256(t['id'].encode()).hexdigest(), 16) % 5 == 4:
            n_skip.append((t['id'], 'sampled for assessor spot-read (1-in-5)'))
            continue
        m = _re.fullmatch(r'tal-(a\d+)-w(\d+)-(\d+)', t['id'])
        if not m:
            n_skip.append((t['id'], 'full-ahnika brief: needs assessor read'))
            continue
        try:
            d = json.load(open(ROOT / 'process' / 'beam' / 'runs' / t['id'] / 'brief.json'))
            items = d['items']
            want = set(range(int(m.group(2)), int(m.group(3)) + 1))
            cov: set[int] = set()
            lens = []
            ok = True
            for it in items:
                mm = _re.fullmatch(r'vv(\d+)-(\d+)', it['span'].strip())
                if not mm:
                    ok = False
                    break
                a, b = int(mm.group(1)), int(mm.group(2))
                cov.update(range(a, b + 1))
                lens.append(b - a + 1)
            mech = len(lens) > 5 and max(_C(lens).values()) / len(lens) > 0.8
            if ok and len(cov & want) >= 0.9 * len(want) and not mech:
                mark(tasks, t['id'], 'approved',
                     (t.get('note', '') + ' | auto: gates re-verified, sampled spot-read pending').strip(' |'))
                n_app += 1
            else:
                n_skip.append((t['id'], 're-verify failed: needs assessor read'))
        except Exception as e:  # noqa: BLE001
            n_skip.append((t['id'], f'read error: {e}'))
    print(f'auto-review: approved={n_app} held={len(n_skip)}')
    for tid, why in n_skip[:20]:
        print(f'  HOLD {tid}: {why}')


def cmd_bounce(tid: str, note: str) -> None:
    tasks = load_q()
    mark(tasks, tid, 'pending', 'bounce: ' + note)
    print(f'{tid} bounced with note for worker retry')

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='c', required=True)
    sub.add_parser('init-queue')
    w = sub.add_parser('worker'); w.add_argument('name')
    sub.add_parser('status')
    r = sub.add_parser('review'); r.add_argument('id')
    a = sub.add_parser('approve'); a.add_argument('id')
    b = sub.add_parser('bounce'); b.add_argument('id'); b.add_argument('note')
    sub.add_parser('auto-review')
    args = ap.parse_args()
    if args.c == 'init-queue':
        cmd_init_queue()
    elif args.c == 'worker':
        return worker_loop(args.name)
    elif args.c == 'status':
        cmd_status()
    elif args.c == 'review':
        cmd_review(args.id)
    elif args.c == 'approve':
        cmd_approve(args.id)
    elif args.c == 'bounce':
        cmd_bounce(args.id, args.note)
    elif args.c == 'auto-review':
        cmd_auto_review()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
