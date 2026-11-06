#!/usr/bin/env python3
"""shastra_fullclose — honest 49/49 T1/L0 closure for IPVV.

For each non-PASS chunk, emits ipvv/cm/<song>_Gfull.py with:
  G = [(src_idx, gloss, grounds)] for every residual REAL token
  STATUS = {src_idx: 'PARSED'|'AMBIGUOUS'}

Rules (no faking):
- SAFE closed-class / frequent stable forms -> real English gloss, PARSED,
  grounds cite grammar + T1-doc context, machine-proposed.
- Everything else -> AMBIGUOUS placeholder gloss "<stem>-unparsed",
  grounds state no v1/doc/particle source, needs hand gloss.
- Paratext never emitted (handled by merge skip).
- Existing Gchar/Ghand glosses authoritative; fullclose only fills still-gaps.

Run: python3 tools/shastra_fullclose.py [--only song]
Then: python3 tools/shastra_batch_fill.py (picks up Gfull automatically? no,
this tool merges directly) -- this tool writes Gfull then runs shastra_merge.
"""
from __future__ import annotations
import json, re, pathlib, subprocess, sys, os

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import source_spans, data_dir

# SAFE: normalized_key -> (gloss, grounds_note). PARSED, high-confidence only.
# normalized = lowercase IAST letters only.
SAFE = {
 'evam': ('thus', 'indecl, standard'),
 'iva': ('as-if', 'indecl particle'),
 'katham': ('how', 'interrogative indecl'),
 'tathahi': ('for-thus', 'explanatory particle'),
 'tathāhi': ('for-thus', 'explanatory particle'),
 'tena': ('by-that', 'inst.sg of tad'),
 'ayam': ('this', 'nom.sg masc of idam'),
 'cet': ('if', 'conditional particle'),
 'prati': ('towards', 'preverb/prep'),
 'prakasate': ('shines', '3sg pres of pra-kāś'),
 'prakāśate': ('shines', '3sg pres of pra-kāś'),
 'kim': ('what', 'interrogative'),
 'kiṃ': ('what', 'interrogative'),
 'yo': ('who', 'nom.sg of yad'),
 'nilam': ('blue', 'acc.sg of nīla'),
 'nīlaṃ': ('blue', 'acc.sg of nīla'),
 'ye': ('who', 'nom.pl of yad'),
 'bhati': ('shines', '3sg pres of bhā'),
 'bhāti': ('shines', '3sg pres of bhā'),
 'saha': ('with', 'prep, instr sense'),
 'vimarsah': ('reflexion', 'Trika technical term vimarśa'),
 'vimarśaḥ': ('reflexion', 'Trika technical term vimarśa'),
 'tada': ('then', 'indecl'),
 'tadā': ('then', 'indecl'),
 'pramata': ('knower', 'pramātṛ technical term'),
 'pramātā': ('knower', 'pramātṛ technical term'),
 'ya': ('which', 'relative pronoun'),
 'sutre': ('in-the-sūtra', 'loc.sg of sūtra'),
 'sūtre': ('in-the-sūtra', 'loc.sg of sūtra'),
 'iha': ('here', 'indecl'),
 'tadeva': ('that-very', 'tad+eva'),
 'bhavet': ('would-be', '3sg opt of bhū'),
 'vina': ('without', 'prep + instr/acc'),
 'vinā': ('without', 'prep'),
 'san': ('being', 'pres participle of as'),
 'santah': ('being', 'nom.pl of sant'),
 'santaḥ': ('being', 'nom.pl of sant'),
 'param': ('supreme', 'para-'),
 'paraṃ': ('supreme', 'para-'),
 'nama': ('by-name', 'indecl'),
 'nāma': ('by-name', 'indecl'),
 'vastu': ('thing', 'object, reality'),
 'tatasca': ('and-thence', 'tataḥ+ca'),
 'tataśca': ('and-thence', 'tataḥ+ca'),
 'tarhi': ('then', 'indecl correlative'),
 'nahi': ('for-not', 'na+hi'),
 'nahi': ('for-not', 'na+hi'),
 'kramena': ('in-order', 'inst.sg of krama'),
 'krameṇa': ('in-order', 'inst.sg of krama'),
 'aham': ('I', 'nom.sg of asmad'),
 'ahaṃ': ('I', 'nom.sg of asmad'),
 'kale': ('in-time', 'loc.sg of kāla'),
 'kāle': ('in-time', 'loc.sg of kāla'),
 'prakarena': ('in-the-way', 'inst.sg of prakāra'),
 'prakāreṇa': ('in-the-way', 'inst.sg of prakāra'),
 'tacca': ('and-that', 'tad+ca'),
 'tasmin': ('in-that', 'loc.sg of tad'),
 'anyatha': ('otherwise', 'indecl'),
 'anyathā': ('otherwise', 'indecl'),
 'uktam': ('said', 'past participle of vac'),
 'uktaṃ': ('said', 'past participle of vac'),
 'ko': ('who', 'nom.sg of kim'),
 'yena': ('by-which', 'inst.sg of yad'),
 'sambandhah': ('relation', 'saṃbandha technical term'),
 'saṃbandhaḥ': ('relation', 'saṃbandha technical term'),
 'eka': ('one', 'numeral'),
 'sarvatra': ('everywhere', 'indecl'),
 'yadyapi': ('although', 'yadi+api'),
 'tadaha': ('then-says', 'tadā+āha formula'),
 'tadāha': ('then-says', 'tadā+āha formula'),
 'atmani': ('in-the-self', 'loc.sg of ātman'),
 'ātmani': ('in-the-self', 'loc.sg of ātman'),
 'rupena': ('by-form', 'inst.sg of rūpa'),
 'rūpeṇa': ('by-form', 'inst.sg of rūpa'),
 'ahamiti': ('I-thus', 'aham+iti quotative'),
 'bhavatiti': ('becomes-thus', 'bhavati+iti'),
 'visvam': ('universe', 'viśva-'),
 'viśvaṃ': ('universe', 'viśva-'),
 'mama': ('of-me', 'gen.sg of asmad'),
 'tathaiva': ('just-thus', 'tathā+eva'),
 'tathaiva': ('just-thus', 'tathā+eva'),
 'bhava': ('become', '2sg imperative of bhū'),
 'bhāvā': ('states', 'nom.pl of bhāva'),
 'kevalam': ('mere', 'indecl adjective'),
 'kevalaṃ': ('mere', 'indecl adjective'),
 'vrttau': ('in-the-commentary', 'loc.sg of vṛtti'),
 'vṛttau': ('in-the-commentary', 'loc.sg of vṛtti'),
 'tathapi': ('even-so', 'tathā+api'),
 'tathāpi': ('even-so', 'tathā+api'),
 'jnanasya': ('of-knowledge', 'gen.sg of jñāna'),
 'jñānasya': ('of-knowledge', 'gen.sg of jñāna'),
 'kimcit': ('something', 'kim+cit indefinite'),
 'kiṃcit': ('something', 'kim+cit indefinite'),
 'atmana': ('by-the-self', 'inst.sg of ātman'),
 'ātmanā': ('by-the-self', 'inst.sg of ātman'),
 'tesam': ('of-them', 'gen.pl of tad'),
 'teṣāṃ': ('of-them', 'gen.pl of tad'),
 'visayah': ('object', 'viṣaya-'),
 'viṣayaḥ': ('object', 'viṣaya-'),
 'kila': ('indeed', 'indecl evidential'),
 'yavat': ('as-far-as', 'yāvat correlative'),
 'yāvat': ('as-far-as', 'yāvat correlative'),
 'sphurati': ('flashes', '3sg pres of sphur'),
 'anena': ('by-this', 'inst.sg of idam'),
 'yata': ('from-which', 'yataḥ'),
 'yataḥ': ('from-which', 'indecl ablative sense'),
 'purvam': ('before', 'pūrvam indecl/acc'),
 'pūrvaṃ': ('before', 'pūrvam'),
 'svatmani': ('in-own-self', 'sva+ātmani'),
 'svātmani': ('in-own-self', 'sva+ātmani'),
 'sarvatha': ('in-every-way', 'sarvathā'),
 'sarvathā': ('in-every-way', 'sarvathā'),
 'arthe': ('in-the-matter', 'loc.sg of artha'),
 'nirbhasate': ('appears', '3sg of nir-bhās'),
 'nirbhāsate': ('appears', '3sg of nir-bhās'),
 'tatraiva': ('right-there', 'tatra+eva'),
 'brahma': ('brahman', 'neuter absolute'),
 'svayam': ('oneself', 'indecl reflexive'),
 'svayaṃ': ('oneself', 'indecl reflexive'),
 'pasyati': ('sees', '3sg pres of dṛś'),
 'paśyati': ('sees', '3sg pres of dṛś'),
 'svatma': ('own-self', 'sva+ātman'),
 'svātmā': ('own-self', 'sva+ātman'),
 'atmanah': ('of-the-self', 'gen.sg of ātman'),
 'ātmanah': ('of-the-self', 'gen.sg of ātman'),
 'ātmanaḥ': ('of-the-self', 'gen.sg of ātman'),
 'sabdena': ('by-word', 'inst.sg of śabda'),
 'śabdena': ('by-word', 'inst.sg of śabda'),
 'madhye': ('in-the-middle', 'indecl loc sense'),
 'etadeva': ('this-very', 'etad+eva'),
 'prakasa': ('manifestation', 'prakāśa technical term'),
 'prakāśa': ('manifestation', 'prakāśa technical term'),
 'sabd ah': ('word', 'śabda-'),
 'śabdaḥ': ('word', 'śabda-'),
 'sarvasya': ('of-all', 'gen.sg of sarva'),
 'tadapi': ('that-too', 'tad+api'),
 'yada': ('when', 'yadā'),
 'yadā': ('when', 'yadā'),
 'uktam': ('said', 'ukta-'),
 'tau': ('those-two', 'nom.du of tad'),
 'samyak': ('rightly', 'indecl'),
 'tathaca': ('and-so', 'tathā+ca'),
 'tathāca': ('and-so', 'tathā+ca'),
 'asau': ('that-one', 'adas pronoun'),
 'sve': ('in-own', 'loc of sva'),
 'astu': ('let-it-be', '3sg imperative of as'),
 'mayi': ('in-me', 'loc.sg of asmad'),
 'siddhih': ('accomplishment', 'siddhi-'),
 'siddhiḥ': ('accomplishment', 'siddhi-'),
 'hetuh': ('cause', 'hetu-'),
 'hetuḥ': ('cause', 'hetu-'),
 'punah': ('again', 'punar indecl'),
 'punaḥ': ('again', 'punar indecl'),
 'atrapi': ('even-here', 'atra+api'),
 'atrāpi': ('even-here', 'atra+api'),
 'atmaiva': ('self-itself', 'ātmā+eva'),
 'ātmā': ('self', 'ātman-'),
 'atma': ('self', 'ātman-'),
 'ātmā': ('self', 'ātman-'),
 'loke': ('in-the-world', 'loc.sg of loka'),
 'rupam': ('form', 'rūpa-'),
 'rūpam': ('form', 'rūpa-'),
 'rūpaṃ': ('form', 'rūpa-'),
 'athava': ('or-else', 'athavā'),
 'athavā': ('or-else', 'athavā'),
 'ittham': ('thus', 'ittham indecl'),
 'itthaṃ': ('thus', 'ittham'),
 'sarvam': ('all', 'acc.sg of sarva'),
 'sarvaṃ': ('all', 'acc.sg of sarva'),
 'siddhah': ('accomplished', 'siddha-'),
 'siddhaḥ': ('accomplished', 'siddha-'),
 'dharma': ('dharma', 'dharma-'),
 'kriya': ('action', 'kriyā-'),
 'kriyā': ('action', 'kriyā-'),
 'naiva': ('not-at-all', 'na+eva'),
 'sat': ('being', 'sat pres participle'),
 'yatha': ('as', 'yathā'),
 'yathā': ('as', 'yathā'),
 'taya': ('by-her', 'inst.sg fem of tad'),
 'tayā': ('by-her', 'inst.sg fem of tad'),
 'vrttih': ('functioning', 'vṛtti-'),
 'vṛttiḥ': ('functioning', 'vṛtti-'),
 'kriyate': ('is-done', '3sg pass of kṛ'),
 'siddham': ('established', 'siddha-'),
 'siddhaṃ': ('established', 'siddha-'),
 'sutram': ('sūtra', 'sūtra-'),
 'sūtraṃ': ('sūtra', 'sūtra-'),
 'idanim': ('now', 'idānīm'),
 'idānīm': ('now', 'idānīm'),
 'ghata': ('pot', 'ghaṭa stock example'),
 'ghaṭa': ('pot', 'ghaṭa stock example'),
 'prathamata': ('firstly', 'prathamataḥ'),
 'prabhrti': ('beginning-with', 'prabhṛti'),
 'prabhṛti': ('beginning-with', 'prabhṛti'),
 'jada': ('inert', 'jaḍa-'),
 'jaḍa': ('inert', 'jaḍa-'),
 'ekasya': ('of-one', 'gen.sg of eka'),
 'sthane': ('in-place', 'sthāna-'),
 'sthāne': ('in-place', 'sthāna-'),
 'mahesvara': ('great-lord', 'maheśvara-'),
 'maheśvara': ('great-lord', 'maheśvara-'),
 'tata': ('thence', 'tataḥ'),
 'tataḥ': ('thence', 'tataḥ'),
 'atah': ('hence', 'ataḥ'),
 'ataḥ': ('hence', 'ataḥ'),
 'tavat': ('so-long', 'tāvat'),
 'tāvat': ('so-long', 'tāvat'),
 'api': ('too', 'indecl'),
 'eva': ('indeed', 'indecl'),
 'ca': ('and', 'indecl'),
 'va': ('or', 'indecl'),
 'vā': ('or', 'indecl'),
 'na': ('not', 'indecl'),
 'tu': ('but', 'indecl'),
 'hi': ('for', 'indecl'),
 'iti': ('thus', 'quotative'),
 'tat': ('that', 'tad-'),
 'tad': ('that', 'tad-'),
 'etat': ('this', 'etad-'),
 'etad': ('this', 'etad-'),
 'idam': ('this', 'idam-'),
 'idam': ('this', 'idam-'),
 'tatra': ('there', 'indecl'),
 'yatra': ('where', 'indecl'),
 'sarva': ('all', 'sarva-'),
 'yatha': ('as', 'yathā'),
 'tatha': ('thus', 'tathā'),
 'sati': ('being', 'loc.abs of as'),
 'asti': ('is', '3sg of as'),
 'syat': ('would-be', 'opt of as'),
 'syāt': ('would-be', 'opt of as'),
 'bhavati': ('becomes', '3sg of bhū'),
 'aha': ('says', 'āha'),
 'āha': ('says', 'āha'),
 'yah': ('who', 'yad-'),
 'yaḥ': ('who', 'yad-'),
 'yat': ('which', 'yad-'),
 'yad': ('which', 'yad-'),
 'tasya': ('of-that', 'gen.sg of tad'),
 'asya': ('of-this', 'gen.sg of idam'),
 'eṣa': ('this', 'etad-'),
 'kva': ('where', 'interrogative'),
 'kadacit': ('sometimes', 'kadācit'),
 'kadācit': ('sometimes', 'kadācit'),
 'nunam': ('surely', 'nūnam'),
 'nūnaṃ': ('surely', 'nūnam'),
 'vai': ('indeed', 'indecl'),
 'nanu': ('surely', 'objection particle'),
 'nanu': ('surely', 'objection particle'),
 'atha': ('now', 'mangala opener'),
 'tatha': ('thus', 'tathā'),
 'evam': ('thus', 'evam'),
 'khalu': ('indeed', 'khalu'),
 'siva': ('śiva', 'śiva-'),
 'śivaḥ': ('śiva', 'śiva-'),
 'sakti': ('power', 'śakti-'),
 'śakti': ('power', 'śakti-'),
 'jnanam': ('knowledge', 'jñāna-'),
 'jñānaṃ': ('knowledge', 'jñāna-'),
 'jñāna': ('knowledge', 'jñāna-'),
 'kriya': ('action', 'kriyā-'),
 'maya': ('consisting-of', 'maya- suffix'),
 'mayā': ('by-me', 'inst.sg of asmad'),
 'tvam': ('you', 'tvam-'),
 'tvāṃ': ('you', 'tvam acc'),
 'mam': ('me', 'acc/gen of asmad'),
 'mama': ('of-me', 'gen of asmad'),
 'te': ('they', 'tad nom.pl / 2sg dat'),
 'tam': ('him', 'acc.sg of tad'),
 'taṃ': ('him', 'acc.sg of tad'),
 'tameva': ('him-very', 'tam+eva'),
 'tveva': ('you-very', 'tvam+eva'),
}

def norm(s: str) -> str:
    s = s.strip().strip(',;:!?।॥|]').strip()
    s = s.strip().strip('"\'“”‘’').strip()
    return re.sub(r'[^a-zāīūṛṝḷḹēōṃḥṅñṭḍṇśṣ]', '', s.lower())

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None)
    ap.add_argument('--work', default='ipvv')
    a = ap.parse_args()
    table = json.load(open(ROOT / a.work / 'chunk-table.json'))
    status_all = json.load(open(ROOT / a.work / 'STATUS.json'))
    done = set(status_all['counts'].get('shastra_pass', []))
    mp = json.load(open(ROOT / a.work / 'chunk-song-map.json'))
    total_new_p = total_new_a = 0
    per_chunk = []
    for e in table:
        song = e['song']
        if a.only and song != a.only:
            continue
        if song in done:
            per_chunk.append((song, 'skip-pass', 0, 0))
            continue
        verse = e['verse']
        chunk_id = next(c for c, s in mp.items() if s == song)
        src = source_spans(a.work)[verse]
        # current covered
        tp = data_dir(a.work, song) / f'{song}.t1.json'
        t1 = json.loads(tp.read_text())
        covered_surf = [t['surface'] for t in t1[0]['tokens']]
        # re-derive covered idx
        covered = set()
        ptr = 0
        for s in covered_surf:
            try:
                ptr = src.index(s, ptr)
            except ValueError:
                continue
            covered.add(ptr)
            ptr += 1
        # residuals = real non-paratext idx not covered
        from shastra_merge import is_paratext
        G = []
        ST = {}
        n_p = n_a = 0
        for i, tok in enumerate(src):
            if is_paratext(tok) or i in covered:
                continue
            k = norm(tok)
            hit = SAFE.get(tok) or SAFE.get(tok.strip(',;:')) or SAFE.get(k)
            if hit:
                gl, gr = hit
                G.append((i, gl, f'standard Sanskrit closed-class/stable (grammar); machine-proposed, needs human review [{gr}]'))
                ST[i] = 'PARSED'
                n_p += 1
            else:
                stem = k if k else 'x'
                if len(stem) > 40:
                    stem = stem[:40]
                G.append((i, f'{stem}-unparsed',
                          f'residual: no v1/doc/particle source; AMBIGUOUS placeholder, needs hand gloss (machine-proposed)'))
                ST[i] = 'AMBIGUOUS'
                n_a += 1
        mod = song.replace('-', '_') + '_Gfull'
        out = ROOT / a.work / 'cm' / f'{mod}.py'
        lines = ['G = [']
        for i, g, gr in sorted(G):
            lines.append(f' ({i}, {g!r}, {gr!r}),')
        lines.append(']')
        lines.append('STATUS = {')
        for i in sorted(ST):
            lines.append(f' {i}: {ST[i]!r},')
        lines.append('}')
        out.write_text('\n'.join(lines) + '\n')
        # merge with existing gtables + Gfull
        import glob as _g
        have = []
        # collect existing mods that exist as files
        base = song.replace('-', '_')
        for cand, gname in [(f'{base}_Gchar', 'Gchar'), (f'{base}_Ghand', 'Ghand')]:
            if (ROOT / a.work / 'cm' / f'{cand}.py').exists():
                have.append(cand)
        # also G tables chunkX_Gn already folded into data; covered set protects them.
        # find charfill stats for v1 path
        cf = json.loads((ROOT / a.work / 'cm' / f'{song}.charfill.json').read_text())
        gtables = ','.join(have + [mod]) if have else mod
        env = dict(os.environ, PYTHONPATH=str(ROOT / a.work / 'cm'))
        # need Gchar module importable: charfill mod name is <song>_Gchar with dashes->underscores? charfill writes mod=song.replace('-','_')+'_Gchar'
        p = subprocess.run([sys.executable, 'tools/shastra_merge.py', '--song', song,
                            '--verse', str(verse), '--v1', cf.get('v1_path') or '/dev/null',
                            '--gtables', gtables], cwd=ROOT, capture_output=True, text=True, env=env)
        if p.returncode != 0:
            print(f'MERGE-FAIL {song}: {(p.stdout+p.stderr)[-800:]}')
            per_chunk.append((song, 'merge-fail', n_p, n_a))
            continue
        print(f'OK {song}: +PARSED {n_p} +AMBIG {n_a} :: {p.stdout.strip().splitlines()[0] if p.stdout.strip() else ""}')
        total_new_p += n_p
        total_new_a += n_a
        per_chunk.append((song, 'ok', n_p, n_a))
    print(f'\nFULLCLOSE DONE: +PARSED={total_new_p} +AMBIG={total_new_a}')
    (ROOT / a.work / 'cm' / 'fullclose-report.json').write_text(json.dumps(
        {'per_chunk': per_chunk, 'parsed': total_new_p, 'ambig': total_new_a}, indent=1))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
