#!/usr/bin/env python3
"""tools/audit_align.py — classify ALIGN_NODISP blocks: sandhi-only vs real defect.

For every BLOCKED song (or --work/--song), recompute the exact B3 comparison
proof_record makes (T1 surfaces vs cleaned source spans, deparen, ratio), then
diff the joined strings and classify every non-equal opcode:

  sandhi-only (propose disposition): every opcode fragment is a known joint —
    -aḥ/-o, -aḥa/o', aa/ā, i/y, u/v, t/d(/c/n), n/ṇ, s/ś, m/ṃ, ai/aī/e,
    avagraha '/∅, hiatus-a deletion, whitespace/token-split only —
    AND every fragment is ≤4 chars (longer = real content difference).

  NEEDS-EYES (human backlog): anything else — wrong words, order changes,
    dropped/added tokens, long replacements. Never auto-dispositioned.

Output (default): JSON report {song: {verse: {verdict, ratio, note|diff}}}.
With --apply: merge SANDHI-ONLY notes into tools/proof-disp.json
(same indent=1 format), then re-run proof_record to confirm PASS.
Re-run is per-song; a song that stays BLOCKED keeps its disposition rows
(they are honest records either way) and is reported, never forced.

Usage:
  python3 tools/audit_align.py [--work W] [--song S] [--apply] [--json]
"""
from __future__ import annotations
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import proof_record as P  # noqa: E402  (reuse the exact B3 loaders/cleaners)
from shastra_merge import is_paratext as _para  # noqa: E402

DISP_PATH = ROOT / "tools" / "proof-disp.json"

# (t1-fragment, src-fragment) pairs that are pure sandhi joints. Fragments
# longer than 4 chars on either side are NEVER sandhi (see classifier).
SANDHI_PAIRS = {
    ("aḥ", "o"), ("o", "aḥ"), ("aḥa", "o'"), ("o'", "aḥa"),
    ("aa", "ā"), ("ā", "aa"), ("i", "y"), ("y", "i"),
    ("u", "v"), ("v", "u"), ("t", "d"), ("d", "t"),
    ("t", "c"), ("c", "t"), ("t", "n"), ("n", "t"),
    ("n", "ṇ"), ("ṇ", "n"), ("s", "ś"), ("ś", "s"),
    ("m", "ṃ"), ("ṃ", "m"),
    ("aī", "e"), ("e", "aī"), ("aḥ", "r"), ("r", "aḥ"),
    ("ḥ", "s"), ("s", "ḥ"), ("ḥ", "r"), ("r", "ḥ"),
    ("aa", "a"), ("a", "aa"),
    ("uu", "ū"), ("ū", "uu"), ("ii", "ī"), ("ī", "ii"),
    ("m", "ñ"), ("ñ", "m"), ("tś", "cch"), ("cch", "tś"),
    # ā+i→e and ā+e→ai (vṛddhi) joints. The 2-char āi/āe side makes these
    # distinctive: a lone e/i swap is kept as needs-eyes (fork risk, e.g.
    # iva/eva). Bare ai/e is NOT a pair (too broad — would launder real
    # spelling differences).
    ("āi", "e"), ("e", "āi"), ("āe", "ai"), ("ai", "āe"),
}


def _eva_window_ok(a_full: str, b_full: str, i1: int, i2: int, j1: int, j2: int,
                   a_frag: str, b_frag: str, tag: str) -> tuple[bool, str] | None:
    """The ca+eva convention: T1 writes citation forms (ca, eva) where the
    witness joins them (caiva, via a+e→ai). In spaceless joined strings this
    surfaces as e~i inside an [aā]eva/[aā]iva window. Accept ONLY inside that
    window — a bare e/i swap elsewhere stays needs-eyes (iva/eva is a genuine
    fork: 'like' vs 'indeed'). Returns None when the rule does not apply."""
    if tag != "replace":
        return None
    if sorted([a_frag, b_frag]) != ["e", "i"]:
        return None
    a_win = a_full[max(0, i1 - 3):i2 + 1]
    b_win = b_full[max(0, j1 - 3):j2 + 1]
    pair = sorted([a_win, b_win])
    if pair == ["aeva", "aiva"] or pair == ["āeva", "āiva"]:
        return True, "ca+eva convention"
    return None


def _clean(toks: list[str]) -> list[str]:
    out = []
    for t in toks:
        s = t.replace("|", "").replace("‖", "")
        if not s.strip():
            continue
        if _para is not None and _para(s):
            continue
        out.append(s)
    return out


def _frag_ok(a: str, b: str, tag: str) -> tuple[bool, str]:
    """One difflib opcode -> (is_sandhi, class-name)."""
    # '+' is the T1 compound-split marker (never Sanskrit, never in source):
    # strip it before classifying; a fragment that is ONLY marker is sandhi.
    a0, b0 = a.replace("+", ""), b.replace("+", "")
    if not a0 and not b0 and (a or b):
        return True, "compound-marker"
    a, b = a0, b0
    if tag == "equal":
        return True, ""
    if len(a) > 4 or len(b) > 4:
        return False, f"long-{tag}:{a!r}~{b!r}"
    if tag == "delete":
        if re.fullmatch(r"[aā' ]+", a):
            return True, "hiatus/avagraha-drop" if a.strip(" ") else "spacing"
        return False, f"delete:{a!r}"
    if tag == "insert":
        if re.fullmatch(r"[' ]+", b):
            return True, "avagraha/spacing"
        return False, f"insert:{b!r}"
    if tag == "replace":
        if (a, b) in SANDHI_PAIRS:
            return True, f"{a}>{b}"
        # whitespace-only reshuffle inside the fragment
        if re.sub(r"\s+", "", a) == re.sub(r"\s+", "", b):
            return True, "respacing"
        return False, f"replace:{a!r}~{b!r}"
    return False, f"unknown:{tag}"


def classify(a: str, b: str) -> tuple[str, str]:
    """Joined-string diff -> ('sandhi-only', note) or ('needs-eyes', diff)."""
    sm = difflib.SequenceMatcher(None, a, b)
    classes = []
    bad = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        af, bf = a[i1:i2], b[j1:j2]
        if tag == "replace":
            eva = _eva_window_ok(a, b, i1, i2, j1, j2, af, bf, tag)
            if eva is not None:
                ok, name = eva
                (classes if ok else bad).append(name)
                continue
        ok, name = _frag_ok(af, bf, tag)
        (classes if ok else bad).append(name)
    if bad:
        return "needs-eyes", " | ".join(bad[:8])
    seen = sorted(set(classes))
    return "sandhi-only", "sandhi-only: " + ", ".join(seen[:10])


def load_pair(work: str, song: str):
    """Replicate proof_record's src + t1 dicts for (work, song)."""
    import workcfg
    w = ROOT / work
    try:
        all_spans = workcfg.source_spans(work)
    except Exception:
        all_spans = None
    if all_spans is not None:
        cfg = workcfg.work_config(work)
        want = set(workcfg.song_verses(work, song))
        src = {v: toks for v, toks in all_spans.items() if v in want}
    else:
        n = int(song[1:])
        from pathlib import Path as _P
        gretil = _P(workcfg.WORKS[work]["source"]) if work in workcfg.WORKS else None
        src = P.load_gretil_song(gretil, n) if gretil else {}
    t1objs = json.loads((w / "data" / f"{song}.t1.json").read_text(encoding="utf-8"))
    vmap: dict[int, int] = {}
    wtp = w / f"working-t1-{song}.json"
    if wtp.exists():
        try:
            wto = json.loads(wtp.read_text(encoding="utf-8"))
            if wto and all("span" in e for e in wto):
                vmap = {int(e["verse"]): int(e["span"]) for e in wto}
        except (ValueError, KeyError):
            pass
    t1 = {}
    for o in t1objs:
        t1[vmap.get(o.get("verse", 0), o.get("verse", 0))] = [
            t.get("surface", "") for t in o.get("tokens", [])]
    return src, t1


def audit_song(work: str, song: str) -> dict:
    pf = ROOT / work / "proof" / f"proof-{song}.json"
    if not pf.is_file():
        return {"song": song, "status": "no-proof-file", "verses": {}}
    proof = json.loads(pf.read_text(encoding="utf-8"))
    blocks = [b for b in proof.get("blocking", []) if b.startswith("ALIGN_NODISP")]
    other = [b for b in proof.get("blocking", []) if not b.startswith("ALIGN_NODISP")]
    out: dict = {"song": song, "status": "BLOCKED" if proof.get("blocking") else "PASS",
                 "other_blocks": other, "verses": {}}
    if not blocks:
        return out
    try:
        src, t1 = load_pair(work, song)
    except Exception as e:
        out["status"] = f"load-error: {e}"[:120]
        return out
    for b in blocks:
        m = re.match(r"ALIGN_NODISP v(\d+) ratio=([\d.]+)", b)
        if not m:
            continue
        v = int(m.group(1))
        a = "".join(t1.get(v, []))
        b_ = "".join(_clean(src.get(v, [])))
        r = difflib.SequenceMatcher(None, P.deparen(a), P.deparen(b_)).ratio()
        if r >= 0.90:
            out["verses"][str(v)] = {"verdict": "stale-pass",
                                     "ratio": round(r, 3),
                                     "note": "re-proof clears it"}
            continue
        verdict, note = classify(P.deparen(a), P.deparen(b_))
        out["verses"][str(v)] = {"verdict": verdict, "ratio": round(r, 3),
                                 "note": note if verdict == "sandhi-only" else "",
                                 "diff": "" if verdict == "sandhi-only" else note,
                                 "t1": " ".join(t1.get(v, []))[:160],
                                 "src": " ".join(_clean(src.get(v, [])))[:160]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="")
    ap.add_argument("--song", default="")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.song and not a.work:
        print("pass --work with --song", file=sys.stderr)
        return 2
    if a.work and a.song:
        songs = [(a.work, a.song)]
    elif a.work:
        songs = [(a.work, p.name[:-len(".t1.json")])
                 for p in sorted((ROOT / a.work / "data").glob("*.t1.json"))]
    else:
        songs = []
        for dd in sorted(ROOT.glob("*/data/*.t1.json")):
            w = dd.parent.parent.name
            songs.append((w, dd.name[:-len(".t1.json")]))

    rows = [audit_song(w, s) for (w, s) in songs]
    n_sandhi = sum(1 for r in rows for v in r.get("verses", {}).values()
                   if v.get("verdict") == "sandhi-only")
    n_eyes = sum(1 for r in rows for v in r.get("verses", {}).values()
                 if v.get("verdict") == "needs-eyes")
    n_other = sum(1 for r in rows if r.get("other_blocks"))
    summary = {"songs": len(rows), "sandhi_only_verses": n_sandhi,
               "needs_eyes_verses": n_eyes,
               "songs_with_other_blocks": n_other}
    if a.apply:
        disp = json.loads(DISP_PATH.read_text(encoding="utf-8"))
        added = 0
        for r in rows:
            so = None
            for w, s in songs:
                if s == r["song"] and (not a.work or w == a.work):
                    so = (w, s)
                    break
            for v, vr in r.get("verses", {}).items():
                if vr.get("verdict") != "sandhi-only":
                    continue
                # find work for this song
                w = next((ww for ww, ss in songs if ss == r["song"]), None)
                if not w:
                    continue
                disp.setdefault(r["song"], {})
                if str(v) not in disp[r["song"]]:
                    disp[r["song"]][str(v)] = vr["note"] + f" (order verified {__import__('datetime').date.today().isoformat()})"
                    added += 1
        DISP_PATH.write_text(json.dumps(disp, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
        summary["dispositions_added"] = added
        # re-proof every touched song to confirm
        repassed, still = 0, []
        touched = sorted({r["song"] for r in rows
                          if any(v.get("verdict") == "sandhi-only"
                                 for v in r.get("verses", {}).values())})
        song_work = {s: w for (w, s) in songs}
        for s in touched:
            w = song_work[s]
            r = subprocess.run([sys.executable, "tools/proof_record.py",
                                "--song", s, "--work", w, "--shastra",
                                "--disp", "tools/proof-disp.json"],
                               cwd=str(ROOT), capture_output=True, text=True, timeout=300)
            try:
                g = json.loads(r.stdout[r.stdout.index("{"):])["gate"]
            except (ValueError, KeyError):
                g = f"rc={r.returncode}"
            if g == "PASS":
                repassed += 1
            else:
                still.append(s)
        summary["reproof_pass"] = repassed
        summary["reproof_still_blocked"] = still
    if a.json:
        print(json.dumps({"summary": summary, "songs": rows}, indent=1, ensure_ascii=False))
    else:
        print(f"songs={summary['songs']} sandhi-only={n_sandhi} "
              f"needs-eyes={n_eyes} other-blocks={n_other}")
        if a.apply:
            print(f"dispositions added: {summary.get('dispositions_added')} | "
                  f"reproof PASS: {summary.get('reproof_pass')} | "
                  f"still blocked: {summary.get('reproof_still_blocked')}")
        for r in rows:
            for v, vr in r.get("verses", {}).items():
                if vr.get("verdict") != "sandhi-only":
                    continue
                print(f"  {r['song']} v{v} r={vr['ratio']} :: {vr['note'][:110]}")
        eyes = [(r["song"], v) for r in rows for v, vr in r.get("verses", {}).items()
                if vr.get("verdict") == "needs-eyes"]
        if eyes:
            print(f"NEEDS-EYES ({len(eyes)}): " +
                  ", ".join(f"{s}v{v}" for s, v in eyes[:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
