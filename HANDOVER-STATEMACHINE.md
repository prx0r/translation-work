# HANDOVER-STATEMACHINE — IPVV translation loop (run this, nothing else)

**You are a machine executing a fixed state machine.** Follow states in order. Every state has an
exact command, an expected output, and PASS/FAIL branches. Do not improvise. Do not "improve"
tools. Do not translate anything yourself except inside STATE 6b (hand-gloss), which is the only
place you may write words by hand.

Working directory for every command: `/root/translation-work`

---

## GLOBAL RULES (apply in every state)

1. **Never claim PASS from memory.** A chunk is PASS only when STATE 6 prints `gate: PASS`.
2. **Never edit `ipvv/data/*.json` by hand.** Data comes only from tools.
3. **Never gloss paratext** (page markers, `||`, `END OF FILE`, `(?)`, `(1.5.7)`, anything with a
   `|`). Tools drop these automatically.
4. **Gloss rules**: literal, hyphenated, **no parentheses**, uncertain = mark `AMBIGUOUS` in
   grounds. Never smooth uncertainty away.
5. **Git**: never `--force`. Always `git pull --rebase origin master` before push. Commit message
   pattern below. If rebase has conflicts you cannot resolve mechanically → ABORT (rule A6).
6. **On any ABORT**: write one line to `active/BLOCKERS.md` (`<date> <song> <state> <error>`),
   stop, report the error verbatim. Do not attempt creative repairs.

---

## STATE 0 — PREFLIGHT (once per session, before anything)

```bash
cd /root/translation-work && git pull --rebase origin master && python3 check.py
```
- **PASS**: prints `CANONICAL: 0 failures` → continue.
- **FAIL**: ABORT (rule A1). Do not continue.

```bash
ls /tmp/opencode/r2/full/translations/_stack/ipvv/l0/*.l0.jsonl /tmp/opencode/r2/v1/translations/_stack/ipvv/l0_v1/*.l0.jsonl 2>/dev/null | wc -l
```
- **PASS**: number ≥ 49 → continue. (Row tarballs must be present; all 49 resolve with either dir.)
- **FAIL**: ABORT (rule A2: row tarballs missing — owner must re-provide them under
  `/tmp/opencode/r2/{v1,full}/translations/_stack/ipvv/`).

```bash
ls tools/shastra_charfill.py tools/shastra_merge.py tools/shastra_convert_chunk.py tools/validate_song.py tools/proof_record.py
```
- **PASS**: all 5 listed → continue. **FAIL**: ABORT (rule A3: tools missing, do not recreate them).

---

## STATE 1 — PICK NEXT CHUNK

```bash
python3 - <<'EOF'
import json
st = json.load(open('ipvv/STATUS.json'))
done = set(st['counts']['shastra_pass'])
nxt = [e for e in json.load(open('ipvv/chunk-table.json')) if e['song'] not in done]
print(json.dumps(nxt[0] if nxt else None))
EOF
```
- **PASS**: prints an object like `{"chunk_id": "...", "song": "...", "verse": N, ...}`.
  Remember `SONG` and `VERSE` from this object. Go to STATE 2.
- **Prints `null`**: queue empty → jump to **FINAL REPORT** below. Done.

---

## STATE 2 — CHARFILL (assembles glosses for uncovered tokens)

```bash
python3 tools/shastra_charfill.py --song SONG --verse VERSE
```

Expected shape (real run, chunk-v2-q):
```
SONG: real=1961 covered=1940 +Gchar=0 ({'v1': 0, 'doc': 0, 'part': 0}) residual=21 v1rows=1959 mod=...
```
- **PASS**: line printed, exit 0, and `ipvv/cm/SONG.charfill.json` exists → STATE 3.
- **Exit code 2** (`FAIL: no v1/full rows found...`): ABORT (rule A2).
- **Traceback / no output**: ABORT (rule A4, paste traceback).
- `residual` > 100 is allowed here (proof will tell you in STATE 6) — do NOT stop.

---

## STATE 3 — MERGE (folds Gchar into T1+L0 data)

Get the rows path the tool found (never hand-type it):

```bash
V1=$(python3 -c "import json;print(json.load(open('ipvv/cm/SONG.charfill.json'))['v1_path'])")
MOD=$(python3 -c "import json;print(json.load(open('ipvv/cm/SONG.charfill.json'))['mod'])")
PYTHONPATH=ipvv/cm python3 tools/shastra_merge.py --song SONG --verse VERSE --v1 "$V1" --gtables "$MOD"
```

Expected (real run): `merged toks: 1940 | paratext skipped: 267 | still gap: 21`
- **PASS**: `merged toks` is ≥ 90% of `real` from STATE 2, no Traceback → STATE 4.
- **FAIL** (merged toks much smaller than `covered+gchar`, or Traceback): ABORT (rule A4).
  Check the printed `mod` name matches the file in `ipvv/cm/` — if it does, ABORT anyway.

---

## STATE 4 — LAYERS (argmap + L2 + C1 from T1; ALWAYS use --layers-only)

```bash
python3 tools/shastra_convert_chunk.py --song SONG --verse VERSE --v1 "$V1" --layers-only
```
- **PASS**: prints `CONVERTED SONG: PASS` → STATE 5.
- **FAIL** / Traceback / any other verdict: ABORT (rule A4).

> `--layers-only` is MANDATORY in this loop. Never run the converter without it
> (it would rebuild T1/L0 and clobber STATE 2–3 work).

---

## STATE 5 — VALIDATE (schema + cross-layer)

```bash
python3 tools/validate_song.py --song SONG --work ipvv
```
- **PASS**: prints JSON with `"errors": []` (or `0`) → STATE 6.
- **FAIL**: any error text → ABORT (rule A5). Paste the errors verbatim. Common causes are
  already-known tool bugs — do NOT patch tools yourself; report.

---

## STATE 6 — PROOF (the only PASS authority)

```bash
python3 tools/proof_record.py --song SONG --work ipvv --shastra
```
Read the printed JSON: `gate`, `blocking`, `min_ratio`.

- **`gate: PASS`** → STATE 7. (Real reference: `min_ratio: 0.965`, `blocking: []`.)
- **`C1_JSON_MISSING` / `L2_JSON_MISSING`**: STATE 4 didn't actually run → re-run STATE 4, then 5, then 6.
- **`ALIGN... ratio=0.xxx` (below 0.90)**: go to **STATE 6b — HAND-GLOSS**, then re-run
  STATE 3 → 4 → 5 → 6.
- **`DATA_OBJECTS ... errors`**: STATE 5 should have caught this → ABORT (rule A5).

---

## STATE 6b — HAND-GLOSS (only when proof says ALIGN short)

This is the ONLY place you write text yourself.

```bash
python3 -c "import json;d=json.load(open('ipvv/cm/SONG-residual.json'));print(len(d['residual']));[print(r) for r in d['residual']]"
```

Create/extend `ipvv/cm/SONG_Ghand.py` (create if missing) with entries for residual tokens:

```python
Ghand = [
 (4, 'perceiving-some-thing', 'residual hand-gloss; source token kiñcidālokyate'),
 (11, 'by-us', 'residual hand-gloss; particle ta eva asmād-ibhiḥ'),
]
```
Rules: `i` = the residual's `i`; gloss = literal, hyphenated, **no parens**; grounds = what the
token actually is; if genuinely uncertain write `('AMBIGUOUS', 'why')`-style grounds and keep the
gloss minimal. Never invent — look at the source token and the T1 doc line quoted in residual
output.

Then re-run STATE 3 with both tables:
```bash
PYTHONPATH=ipvv/cm python3 tools/shastra_merge.py --song SONG --verse VERSE --v1 "$V1" --gtables "$MOD,SONG_Ghand"
```
(note: module name = filename without `.py`, hyphens→underscores), then STATE 4 → 5 → 6.

- Loop 6b→3→4→5→6 until `gate: PASS` or you hit the **cap**:
  - **cap**: >60 residual tokens remaining, or 3 full loops without PASS → ABORT
    (rule A7: report `min_ratio`, remaining residual count, stop).

---

## STATE 7 — RECORD THE PASS

```bash
python3 - <<'EOF'
import json, datetime
p = 'ipvv/STATUS.json'
st = json.load(open(p))
song = 'SONG'   # replace
if song not in st['counts']['shastra_pass']:
    st['counts']['shastra_pass'].append(song)
st['updated'] = datetime.date.today().isoformat()
# set next to the State-1 query you would run (or None if queue empty)
import json as j
done = set(st['counts']['shastra_pass'])
nxt = [e for e in j.load(open('ipvv/chunk-table.json')) if e['song'] not in done]
st['next'] = f"shastra loop: {len(nxt)} chunks remaining"
st['notes'] = f"shastra PASS {song} via state-machine loop"
json.dump(st, open(p, 'w'), indent=1, ensure_ascii=False)
print('recorded', len(st['counts']['shastra_pass']), 'PASS total')
EOF
```
- **PASS**: prints `recorded N PASS total` with N larger than before → STATE 8.

---

## STATE 8 — COMMIT & PUSH

```bash
python3 check.py
```
- **FAIL**: ABORT (rule A1). Never commit red.

```bash
git add ipvv tools && git commit -m "IPVV shastra-minimal: SONG proof PASS (N/49)" \
  && git pull --rebase origin master && git push origin master
```
- **PASS**: push accepted → STATE 1 (next chunk).
- **Push rejected**: run `git pull --rebase origin master` once more and retry. If rebase reports
  **conflicts inside `ipvv/data/`** → ABORT (rule A6: another agent touched the same chunk —
  do not force, do not resolve by guessing).
- If `git commit` says nothing to commit: another process already committed → re-run
  `python3 check.py`; if canonical, go straight to STATE 1.

---

## FINAL REPORT (queue empty)

When STATE 1 prints `null`: run `python3 check.py` once more, then report:
`DONE: N/49 chunks PASS, shastra-minimal complete` — and stop. Do not start new work.

---

## ABORT RULES (exact triggers)

| # | Trigger | Action |
|---|---------|--------|
| A1 | `check.py` not `CANONICAL: 0 failures` | stop, report |
| A2 | row tarballs missing (STATE 0 or exit 2) | stop, report |
| A3 | a listed tool file missing | stop, report |
| A4 | Traceback in any tool | stop, paste traceback |
| A5 | validate errors you cannot map to a listed known cause | stop, paste errors |
| A6 | git rebase conflict in `ipvv/data/` | stop, report |
| A7 | hand-gloss cap hit (>60 residual or 3 loops) | stop, report min_ratio |

## NEVER DO

- Never write a `gate: PASS` yourself; never run proof twice and copy an old result.
- Never edit `ipvv/data/`, `ipvv/T1-*.md`, or source files directly.
- Never run `shastra_convert_chunk.py` without `--layers-only` inside this loop.
- Never push `--force`, never `git checkout` someone else's commits away.
- Never gloss paratext, never add parentheses to glosses, never mark FAILED rows as covered.

## REFERENCE TRANSCRIPT (one complete successful cycle)

```
$ python3 tools/shastra_charfill.py --song chunk-v2-q-saptamo-k11-close --verse 31
chunk-v2-q-...: real=1961 covered=1940 +Gchar=0 (...) residual=21 v1rows=1959 mod=chunk_v2_q_..._Gchar
$ PYTHONPATH=ipvv/cm python3 tools/shastra_merge.py --song ... --gtables chunk_v2_q_..._Gchar
merged toks: 1940 | paratext skipped: 267 | still gap: 21
$ python3 tools/shastra_convert_chunk.py --song ... --layers-only
CONVERTED chunk-v2-q-saptamo-k11-close: PASS
$ python3 tools/validate_song.py --song ... --work ipvv
"errors": []
$ python3 tools/proof_record.py --song ... --work ipvv --shastra
gate: PASS | blocking: [] | min_ratio: 0.965
```

Context/contract (read only if a state needs it): `SHASTRA-MINIMAL.md` (layer contract),
`HANDOVER-2026-11-06-IPVV-GUIDE.md` (full plan), `REVIEW-IPVV-2026-11-06.md` (defects history).
