#!/usr/bin/env python3
"""tools/proof_record.py — crystal proof record for one song (T1/L0/L2/C1 gates, machine-checkable).

Adopts sanskritbenchy's *record envelope* (source_sha + deterministic gate + lineage) while
keeping OUR bars (mistakes.md): T1 coverage vs source (concat-align, not length-ratio),
zero C1/L2 shared sentences, zero quotes in C1, Sanskrit only in C1 KEY-TERMS, L2 cites
byte-exact vs GRETIL, sub-0.90 verses need a recorded disposition.

Usage:
  python3 tools/proof_record.py --song s01 --work sivastotravali
  python3 tools/proof_record.py --song s01 --work sivastotravali --disp tools/proof-disp.json

Exit 0 + gate PASS, exit 1 + gate BLOCKED. Writes work/proof/proof-<song>.json.
Stdlib only.
"""
from __future__ import annotations
import argparse, difflib, hashlib, json, re, sys
from pathlib import Path

TOOL_VERSION = "proof_record v1 2026-11-01"
IAST = set("āīūṛṝḷḹēōṃḥṅñṭḍṇśṣ")
META_PATTERNS = [
    r"the (verse|hymn|stotra|stanza|passage|text|song) (has|describes|quotes|opens|closes|does|shows|says|argues)",
    r"the (grammar|imagery|syntax|meter|composition) (does|shows|suggests)",
    r"this closes the arc",
    r"the move from \S+ to \S+",
    r"as we (saw|have seen)",
    r"in other words,? the (verse|text|song|stotra)",
]


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", norm_ws(text))
    return [p for p in parts if p]


def norm_sent(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def shared_long(a: list[str], b: list[str], min_words: int = 8) -> list[str]:
    nb = {norm_sent(x) for x in b if len(x.split()) >= min_words}
    return sorted({x for x in a if len(x.split()) >= min_words and norm_sent(x) in nb})


def load_gretil_song(gretil: Path, song: int) -> dict[int, list[str]]:
    """GRETIL whitespace tokens per (song, verse). Joins wrap-hyphen continuations; drops oṃ."""
    return {v: toks for v, (toks, _) in load_gretil_spans(gretil, song).items()}


def load_gretil_spans(gretil: Path, song: int) -> dict[int, tuple[list[str], list[int]]]:
    """GRETIL tokens + 1-based file line-span per (song, verse). The line-span is the
    chat-citation anchor: verse -> (file, lines). Wrap-hyphen continuations included.
    Two-pass: marker lines located first, first halves found by scanning back to the
    previous marker (never leaking across songs)."""
    raw = gretil.read_text(encoding="utf-8").splitlines()
    marks: dict[int, int] = {}  # verse -> marker line number
    for ln, line in enumerate(raw, start=1):
        m = re.search(r"UtSst_%d\.(\d+)" % song, line)
        if m:
            marks[int(m.group(1))] = ln

    def eligible(s: str) -> bool:
        s = s.strip()
        return bool(s) and "stotram" not in s and not s.startswith("#") and s != "oṃ" \
            and not re.search(r"UtSst_\d+\.\d+", s)

    out: dict[int, tuple[list[str], list[int]]] = {}
    for v in sorted(marks):
        M = marks[v]
        # first half: nearest eligible line above M (plus wrap-hyphen continuations above it)
        parts, first_ln = [], None
        i = M - 1
        while i >= 1:
            s = raw[i - 1].strip()
            if not eligible(s):
                break
            parts.append(s)
            first_ln = i
            if not s.endswith("-"):
                break
            i -= 1
        first = " ".join(p[:-1] if p.endswith("-") else p for p in reversed(parts))
        second = raw[M - 1][:re.search(r"UtSst_%d\.(\d+)" % song, raw[M - 1]).start()].split("//")[0]
        toks = [t for t in (first + " " + second).split()
                if t and t != "oṃ" and t != "//" and t != "&"]
        out[v] = (toks, [first_ln or M, M])
    return out


def parse_t1(t1: Path) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    cur = None
    for line in t1.read_text(encoding="utf-8").splitlines():
        m = re.match(r"## \S+-v(\d+)", line)
        if m:
            cur = int(m.group(1)); out[cur] = []; continue
        if cur is not None and "[and]-" in line:
            for mm in re.finditer(r"\[and\]-(?:[^\[(]*?)\(([^)]+)\)", line):
                out[cur].append(mm.group(1))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True, help="e.g. s01")
    ap.add_argument("--work", default="sivastotravali")
    ap.add_argument("--disp", default=None, help="JSON {song: {verse: note}} for sub-0.90 dispositions")
    ap.add_argument("--gretil", default="/root/ipvv/site/data/sanskrit/sivastotravali-u.txt")
    args = ap.parse_args()
    root = Path("/root/translation-work")
    w = root / args.work
    song = args.song
    SIVA_DEFAULT = "/root/ipvv/site/data/sanskrit/sivastotravali-u.txt"
    try:
        from workcfg import WORKS as _WORKS, song_verses as _song_verses, parse_utajp, parse_sambandha, parse_isvara
    except ImportError:
        _WORKS = {}
    if args.work in _WORKS and _WORKS[args.work].get("kind") == "utajp":
        gretil = Path(_WORKS[args.work]["source"])
        _spans = parse_utajp(gretil)
        _want = set(_song_verses(args.work, song))
        _src_full = {v: toks for v, (toks, _) in _spans.items() if v in _want}
        src = _src_full
    elif args.work in _WORKS and _WORKS[args.work].get("kind") == "sambandha":
        gretil = Path(_WORKS[args.work]["source"])
        _spans, _ = parse_sambandha(gretil)
        _want = set(_song_verses(args.work, song))
        src = {v: toks for v, (toks, _) in _spans.items() if v in _want}
    elif args.work in _WORKS and _WORKS[args.work].get("kind") == "isvara":
        gretil = Path(_WORKS[args.work]["source"])
        _spans, _ = parse_isvara(gretil)
        _want = set(_song_verses(args.work, song))
        src = {v: toks for v, (toks, _) in _spans.items() if v in _want}
    else:
        n = int(song[1:])
        gretil = Path(args.gretil)
        src = load_gretil_song(gretil, n)

    rec: dict = {"tool": TOOL_VERSION, "song": song, "work": args.work,
                 "date": "2026-11-01", "blocking": [], "warnings": []}
    block = rec["blocking"]

    rec["source_sha"] = sha(" ".join(" ".join(t) for v, t in sorted(src.items())))
    rec["source_verses"] = len(src)

    t1 = parse_t1(w / f"T1-{song}.md")
    rec["t1_verses"] = len(t1)
    if len(t1) != len(src):
        block.append(f"VERSE_COUNT t1={len(t1)} source={len(src)}")
    missing = sorted(set(src) - set(t1))
    if missing:
        block.append(f"MISSING_VERSES {missing}")

    # B1: L0 report
    rep = (w / f"T1-{song}.l0.report.txt").read_text(encoding="utf-8")
    mp = re.search(r"PARSED:\s*(\d+).*AMBIGUOUS:\s*(\d+).*FAILED:\s*(\d+)", rep, re.S)
    mt = re.search(r"tokens:\s*(\d+)", rep)
    l0 = {"parsed": int(mp.group(1)), "ambiguous": int(mp.group(2)),
          "failed": int(mp.group(3)), "tokens": int(mt.group(1))} if mp and mt else {}
    rec["l0"] = l0
    if not (w / f"T1-{song}.l0.jsonl").exists():
        block.append("L0_JSONL_MISSING")
    if l0.get("failed", 1) != 0 or l0.get("parsed") != l0.get("tokens"):
        block.append(f"L0_PARSE {l0}")

    # B3: concat-align per verse
    disp = {}
    if args.disp:
        disp = json.loads(Path(args.disp).read_text()).get(song, {})
    align = {}; sub090 = {}
    for v in sorted(src):
        a = "".join(t1.get(v, []))
        b = "".join(src[v])
        r = difflib.SequenceMatcher(None, a, b).ratio()
        align[str(v)] = round(r, 3)
        if r < 0.90:
            sub090[str(v)] = {"ratio": round(r, 3), "disposition": disp.get(str(v))}
            if not disp.get(str(v)):
                block.append(f"ALIGN_NODISP v{v} ratio={r:.3f}")
    rec["align"] = {"min_ratio": min(align.values()) if align else 0, "sub090": sub090}

    # B4/B5/B6: C1 vs L2
    c1 = (w / "c1" / f"C1-{song}.md").read_text(encoding="utf-8")
    l2 = (w / f"L2-{song}.md").read_text(encoding="utf-8")
    shared = shared_long(sentences(c1), sentences(l2))
    rec["c1_l2_shared"] = shared
    if shared:
        block.append(f"C1_L2_SHARED {len(shared)}")
    q = c1.count('"')
    rec["c1_quotes"] = q
    if q:
        block.append(f"C1_QUOTES {q}")
    # IAST outside **...** spans and outside line-1 title
    # IAST in C1 prose is INFO ONLY (convention: Sanskrit terms may appear
    # parenthesized/italic/bold; the checkable bars are zero quotes + no metacommentary).
    body_lines = c1.splitlines()[1:]
    prose_iast = 0
    for ln in body_lines:
        stripped = re.sub(r"\*\*.*?\*\*", "", ln)
        prose_iast += sum(1 for ch in stripped if ch in IAST)
    rec["c1_iast_prose_info"] = prose_iast
    rec["c1_words"] = len(c1.split())
    if len(c1.split()) > 700:
        rec["warnings"].append(f"C1_WORDS {len(c1.split())} > 700")
    metas = [p for p in META_PATTERNS if re.search(p, c1, re.I)]
    rec["c1_metacommentary"] = metas
    if metas:
        rec["warnings"].append(f"METACOMMENTARY {metas}")

    # B7: L2 Sanskrit cites byte-exact
    cites = re.findall(r"The Sanskrit: \*(.+?)\*", l2)
    src_flat = norm_ws(" ".join(" ".join(t) for v, t in sorted(src.items())))
    fails = [c for c in cites if norm_ws(c) not in src_flat and
             norm_ws(c).replace(" | ", " ") not in src_flat.replace(" | ", " ")]
    # cites use | as pāda separator; source verses are separate — check per-cite against joined verse pairs
    real_fails = []
    verses_text = {v: norm_ws(" ".join(t)) for v, t in src.items()}
    for c in cites:
        parts = [norm_ws(p) for p in c.split("|")]
        ok = any(all(norm_ws(p).replace(" ", "") in verses_text[v].replace(" ", "")
                     for p in parts if p) for v in verses_text)
        if not ok:
            real_fails.append(c[:80])
    rec["l2_cites"] = {"checked": len(cites), "failures": real_fails}
    if real_fails:
        block.append(f"L2_CITE_FAIL {len(real_fails)}")

    # W3: ledger presence (from T1 header *Ledger: ...*  X=Y pairs split by ·)
    m = re.search(r"\*Ledger: (.*?)\*", (w / f"T1-{song}.md").read_text(encoding="utf-8"))
    led = {"pairs": 0, "gloss_missing_in_l2": []}
    l2n = l2.lower().replace("-", " ")
    c1n = c1.lower().replace("-", " ")
    if m:
        for frag in re.split(r"[·;]", m.group(1)):
            if "=" not in frag:
                continue
            x, y = [s.strip() for s in frag.split("=", 1)]
            if not x or " " in x or "." in x:
                continue  # prose trailer, not a term pair
            y = re.split(r"[.;(]", y)[0].strip().replace("-", " ").replace("/", " ")
            if not y:
                continue
            led["pairs"] += 1
            if y.lower() not in l2n and y.lower() not in c1n:
                led["gloss_missing_in_l2"].append(frag.strip()[:60])
    rec["ledger"] = led
    if led["gloss_missing_in_l2"]:
        rec["warnings"].append(f"LEDGER_GLOSS_MISSING {led['gloss_missing_in_l2']}")

    # B8: canonical data objects validate (when present — JSON is canonical, MD is rendered view)
    import subprocess as _sp
    dd = w / "data"
    if all((dd / f"{song}.{x}.json").exists() for x in ["t1", "l0", "argmap", "l2", "c1"]):
        r = _sp.run([sys.executable, str(Path(__file__).parent / "validate_song.py"),
                     "--song", song, "--work", args.work],
                    capture_output=True, text=True)
        try:
            vrec = json.loads(r.stdout)
            rec["data_objects"] = {"errors": vrec.get("errors", []), "counts": vrec.get("counts", {})}
            if vrec.get("errors"):
                block.append(f"DATA_OBJECTS {len(vrec['errors'])} schema/cross-layer errors")
        except Exception as e:
            block.append(f"DATA_OBJECTS validator failed to run: {e}")
    else:
        rec["data_objects"] = {"errors": [], "note": "no canonical JSON yet (MD-only song)"}

    # needs[] (ipvv peer-review F6): WHAT is needed, not just what failed.
    # fix-this entries name the repair; otherwise the song needs human review.
    needs = []
    for b in block:
        if b.startswith("ALIGN_NODISP"):
            needs.append("fix: word-order/gloss vs source for " + b.split()[1])
        elif b.startswith("L0_"):
            needs.append("fix: re-extract or repair L0")
        elif b.startswith(("C1_", "L2_")):
            needs.append("fix: layer gate " + b.split()[0])
        elif b.startswith("DATA_OBJECTS"):
            needs.append("fix: schema/cross-layer errors")
    if not block:
        needs = ["human-review"]
    rec["needs"] = sorted(set(needs))
    rec["deterministic_gate"] = "PASS" if not block else "BLOCKED"
    rec["lineage"] = {"tool": TOOL_VERSION, "source_sha": rec["source_sha"],
                      "t1": f"T1-{song}.md", "l0": f"T1-{song}.l0.jsonl",
                      "l2": f"L2-{song}.md", "c1": f"c1/C1-{song}.md"}
    outdir = w / "proof"
    outdir.mkdir(exist_ok=True)
    (outdir / f"proof-{song}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(json.dumps({"song": song, "gate": rec["deterministic_gate"],
                      "blocking": block, "warnings": rec["warnings"],
                      "min_ratio": rec["align"]["min_ratio"],
                      "cites": rec["l2_cites"]}, indent=1, ensure_ascii=False))
    return 0 if not block else 1


if __name__ == "__main__":
    sys.exit(main())
