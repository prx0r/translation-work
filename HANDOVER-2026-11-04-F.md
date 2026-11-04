# HANDOVER — 2026-11-04 (F): beauty pass complete; method cracked

*Read after HANDOVER-E. This file records what worked, so the next agent (or
future us) repeats it exactly.*

## 1. What got done (all committed, all CANONICAL at commit time)

Track A (16 works → per-verse new-schema DRAFTs, machine-proposed):
pancashloki 5v (owner-approved lines) · tsa-a02 4v (built from data + NOTE) ·
tsa-a01 5v (v05 restored hiding+powers; NOTE) · paramarthacarca 8v ·
anuttarastika 8v · bhairavastava 10v · bodhapancadasika 15v · phrdaya 20v ·
ghatakarpara 21v (stray retired) · sambandhasiddhi 23v · ajadapramatrsiddhi 27v ·
kramastotra 30v · bodhavilasa 40v (v14 edition gap, not a defect) ·
bhairavanukarana 48v · paryantapancasika 52v · parapravesika 9 passages ·
isvarasiddhi 56v (v30 present — an early "gap" was my own slice artifact;
verify before claiming gaps).
Track B verify-only (17 works, STATUS-noted, no re-craft): anubhavanivedana,
spandasandoha, dehastha, rpa, mpa, pdv, saktavijnana, svabodhasiddhi, spanda,
sivasutra, ptv pair, vbt (162v spot-checked), stava (register flagged, untouched),
a17/a18/a19.
Assessments recorded: paramarthasara (~100v mixed → normalize, 1–2 sessions);
sivastotravali (450v per-song → ~450 per-verse files, 3–4 sessions; settle
register question first).

## 2. The cracked method (per work, in order)

1. `ls L4-*.DRAFT.json` → identify schema (song-level `{song,song_craft,verses[]}`
   vs per-verse `{craft_notes,form,l4,reads_against,status}` vs list-file).
2. Verify `draft==data` (+ `==L3` where claimed) with one python assert loop
   before touching anything. Never assume.
3. Pull C1 essence + rasa dominant + argmap Q/INF per song from `data/`.
4. Compose per-verse `craft_notes` = sthāyin (+vyabhicāri where C1 gives it) +
   Sanskrit-first re-parse + Abhinavagupta frame + firing rows + bank device
   names + close-shape + rupture-point + rejected-with-killers + read-aloud
   scan. `reads_against` = argmap "Q → INF" verbatim + C1 essence text(s) +
   rasa dominant string. `status` = machine-proposed.
5. Lines: default UNCHANGED (L3 already musical from handcraft era). Only
   genuine finds change lines (a01-v05 restored hiding+powers; pancashloki
   owner-approved re-lineation). Overlap audit every verse (≥0.30; ours ran
   0.78–1.00).
6. Retire superseded files with EXACT names via `git rm` (never shell globs —
   `L4-pary-p0*` matched new per-verse files too and aborted a commit; §4).
7. Gates per song: validate 0 errors, proof re-run, qa re-run, check.py work.
8. STATUS refresh (notes append, next pointer, updated date) + commit.
   Proof BLOCKED on ALIGN_NODISP with data untouched = pre-existing legacy-T1
   artifact: record honestly, check.py is the gate. A stale 11-01 PASS proof
   (tsa-a01) was overwritten by an honest BLOCKED — correct call; never
   manufacture --disp dispositions without T1-layer reverification.

## 3. Standing owner items (unchanged)

First-verse L4 voice verdicts (all golds) · human review of every
machine-proposed stack · stava/sivastotravali register verdict (archaic vs
contemporary — do NOT start line work before it) · paramarthasara +
sivastotravali scheduling nods · C2 WAIVED going forward (existing C2 stays) ·
push only when asked.

## 4. Failure log additions (mistakes.md candidates)

- Glob-rm pitfall: `git rm <prefix>*` matches newly-written files sharing the
  prefix; always rm by exact filename (paryantapancasika commit split in two).
- Slice artifact: `verses[3:]` inspection hid v30 and fabricated a "gap" —
  assert presence against data/ instead of eyeballing slices (isvarasiddhi).
- Argmap fields aren't always strings: v23-style `question` can be a list —
  coerce with join, never assume (isvarasiddhi script traceback).
- Stale PASS proofs: proof_record.py gained the ALIGN check after 11-01; a
  committed PASS can go BLOCKED on re-run with zero data changes (tsa-a01).
  Re-running proofs is honesty work, not regression.
