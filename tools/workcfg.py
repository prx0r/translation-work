#!/usr/bin/env python3
"""tools/workcfg.py — per-work source configuration (one canonical code path, many works).

Each work names its GRETIL source file, its verse-marker dialect, and (where verses
are absolute-numbered across the work) its song->verse-range map. Tools resolve
(work, song) through here instead of hardcoding sivastotravali.

Song ids are human-readable (s01, ajad-p01). Verse numbers are ABSOLUTE within the
work source (matching the edition numbering, e.g. UtAjp_1..27).
"""
from __future__ import annotations
import re
from pathlib import Path

SITE_SA = Path("/root/ipvv/site/data/sanskrit")

WORKS = {
    "sivastotravali": {
        "source": SITE_SA / "sivastotravali-u.txt",
        "kind": "utsst",  # markers UtSst_<song>.<verse>, song-numbered
    },
    "ajadapramatrsiddhi": {
        "source": SITE_SA / "ajadapramatrsiddhi.txt",
        "kind": "utajp",  # markers // UtAjp_<N> //, absolute N=1..27
        "songs": {"ajad-p01": (1, 9), "ajad-p02": (10, 18), "ajad-p03": (19, 27)},
    },
    "sambandhasiddhi": {
        "source": SITE_SA / "sambandhasiddhi.txt",
        "kind": "sambandha",  # Muktabodha prose; 23 slokas explicit (2 mangala + 21 karikas)
        "songs": {"samb-p01": (1, 9), "samb-p02": (10, 18), "samb-p03": (19, 23)},
    },
    "isvarasiddhi": {
        "source": SITE_SA / "isvarasiddhi.txt",
        "kind": "isvara",  # Muktabodha prose-interleaved; 56 numbered slokas
        "songs": {"isva-p01": (1, 9), "isva-p02": (10, 18), "isva-p03": (19, 27),
                  "isva-p04": (28, 36), "isva-p05": (37, 45), "isva-p06": (46, 54),
                  "isva-p07": (55, 56)},
    },
}


def song_verses(work: str, song: str) -> list[int]:
    """Absolute verse numbers belonging to (work, song)."""
    cfg = WORKS[work]
    if "songs" in cfg:
        lo, hi = cfg["songs"][song]
        return list(range(lo, hi + 1))
    # song-numbered works: s01 -> 1 (verse set discovered from markers)
    return []


def parse_utajp(source: Path) -> dict[int, tuple[list[str], list[int]]]:
    """Parse // UtAjp_N // mūla verses. Returns verse -> (tokens, [first_ln, marker_ln]).

    Mūla = non-empty lines between the previous marker and this one, excluding
    Vṛ: prose, # comments, and [stage-direction] labels. $ & % are pāda marks
    (deleted); wrap-hyphen continuations joined (xxx- + yyy -> xxxyyy).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    out: dict[int, tuple[list[str], list[int]]] = {}
    buf: list[tuple[int, str]] = []  # (lineno, text) since previous marker

    def flush(marker_ln: int, verse: int):
        toks: list[str] = []
        first_ln = marker_ln
        for ln, s in buf:
            t = s.strip()
            if not t or t.startswith("#") or t.startswith("Vṛ:") or t.startswith("Vr:"):
                continue
            if t.startswith("[") and t.endswith("]"):
                continue
            if re.search(r"UtAjp_\d+", t):
                continue  # marker lines handled by caller
            # strip pāda marks, keep words
            t = t.replace("$", " ").replace("&", " ").replace("%", " ")
            t = re.sub(r"//.*", "", t)
            words = t.split()
            if words and first_ln == marker_ln:
                first_ln = ln
            toks.extend(words)
        # join wrap-hyphen continuations
        joined: list[str] = []
        for wd in toks:
            if joined and joined[-1].endswith("-"):
                joined[-1] = joined[-1][:-1] + wd
            else:
                joined.append(wd)
        joined = [wd for wd in joined if wd and wd != "//"]
        out[verse] = (joined, [first_ln, marker_ln])

    for ln, line in enumerate(raw, start=1):
        m = re.search(r"// UtAjp_(\d+) //", line)
        if m:
            pre = line[:m.start()].strip()
            if pre:
                buf.append((ln, pre))
            flush(ln, int(m.group(1)))
            buf = []
        else:
            buf.append((ln, line))
    return out


def parse_sambandha(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse Muktabodha Sambandhasiddhi slokas. Returns (verses, variants).

    verses: absolute v01..v23 -> (tokens, [first_ln, marker_ln]).
    v01-v02 = opening mangala pair; v03..v23 = (tadaha) karikas 1..21.
    Verse lines = indented lines (or pada-continuations ending in |) inside the
    opening zone (from the `atha` line) and the post-(tadaha) zone. Prose is
    skipped for tokens. [kha./pu./ka. ...] readings (even multi-line) are
    stripped from tokens and returned as (lineno, text) for the apparatus note.
    """
    text = source.read_text(encoding="utf-8")
    variants = [(m.group(0)[:120], text[:m.start()].count("\n") + 1)
                for m in re.finditer(r"\[(kha|pu|ka)\..*?\]", text, re.S)]
    variants = [(ln, v) for v, ln in variants]
    raw = text.splitlines()
    lines = []
    i = 0
    while i < len(raw):
        ln = raw[i]
        if re.search(r"\|\|\s*\d+\s*$", ln) and i + 1 < len(raw) and raw[i + 1].strip() == "||":
            lines.append((i + 1, ln + " ||"))
            i += 2
            continue
        lines.append((i + 1, ln))
        i += 1
    verses: dict[int, tuple[list[str], list[int]]] = {}
    buf: list[tuple[int, str]] = []
    zone: str | None = None  # None | "opening" | "karika"
    in_bracket = False

    for ln, line in lines:
        if re.match(r"^\s*atha\s*$", line):
            zone = "opening"
            buf = []
            continue
        if "(tadāha)" in line:
            zone = "karika"
            buf = []
            continue
        if zone is None:
            continue
        # track multi-line [...] spans so their continuations are skipped
        opens = line.count("[")
        closes = line.count("]")
        marked = re.search(r"\|\|\s*(\d+)\s*\|\|\s*$", line)
        ind = line[:1] in " \t"
        iscont = bool(re.match(r"^\s*(yathā\s+)?\|\|", line))
        pada_end = line.rstrip().endswith("|") and "viracitā" not in line
        if (ind or iscont or pada_end) and not in_bracket and not marked:
            t = _clean_verse_text(line)
            if t.strip():
                buf.append((ln, t))
        if opens > closes:
            in_bracket = True
        if closes > opens:
            in_bracket = False
        if marked:
            n = int(marked.group(1))
            pre = line[:marked.start()].strip()
            if pre and not re.match(r"^\s*(yathā\s+)?\|\|", line):
                # marker shares its line with verse text (e.g. `svabhāvataḥ || 46 ||`)
                t = _clean_verse_text(pre)
                if t.strip():
                    buf.append((ln, t))
            vnum = n if zone == "opening" else n + 2
            toks: list[str] = []
            for _, t in buf:
                toks.extend(t.replace("|", " ").split())
            toks = [w for w in toks if w]
            joined: list[str] = []
            for w in toks:
                if joined and joined[-1].endswith("-"):
                    joined[-1] = joined[-1][:-1] + w
                else:
                    joined.append(w)
            first = buf[0][0] if buf else ln
            verses[vnum] = (joined, [first, ln])
            buf = []
    return verses, variants


def _clean_verse_text(s: str) -> str:
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\[[^\]]*$", " ", s)
    s = re.sub(r"\(p\.\s*\d+\)", " ", s)
    s = re.sub(r"\|\|\s*\d+\s*\|\|", " ", s).replace("||", " ")
    return s


def _verse_tokens(text_lines: list[str]) -> list[str]:
    toks: list[str] = []
    for t in text_lines:
        toks.extend(t.replace("|", " ").split())
    toks = [w for w in toks if w and not re.fullmatch(r"\.+", w)]
    joined: list[str] = []
    for w in toks:
        if joined and joined[-1].endswith("-"):
            joined[-1] = joined[-1][:-1] + w
        else:
            joined.append(w)
    return joined


def parse_isvara(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse Muktabodha Isvarasiddhi slokas (prose-interleaved tadaha verses).

    Verse N = pada lines (ending in single |) collected backward from its
    || N || marker (max 3) + the marker line's pre-text + pada lines collected
    forward (max 3, stopping at `iti ||`, blanks, page refs, or non-pada lines).
    Numbering runs 1..56 continuously. Standalone dot-fillers are dropped
    (lacunae); attached dots kept byte-exact. [kha./pu. readings harvested.
    """
    text = source.read_text(encoding="utf-8")
    variants = [(text[:m.start()].count("\n") + 1, m.group(0)[:120])
                for m in re.finditer(r"\[[^\]]*p[āa][ṭt]h[āa][^\]]*\]", text, re.S)]
    raw = text.splitlines()
    lines = []
    i = 0
    while i < len(raw):
        ln = raw[i]
        if re.search(r"\|\|\s*\d+\s*$", ln) and i + 1 < len(raw) and raw[i + 1].strip() == "||":
            lines.append((i + 1, ln + " ||"))
            i += 2
            continue
        lines.append((i + 1, ln))
        i += 1

    # Explicit verse-line map supplements (bare IND verse lines without pada
    # daṇḍa, and forward-attached cd halves). Every entry hand-verified
    # against pāda-sense during T1; see the work's NOTE for discussion.
    # Hemistichs (v01, v31, v43, v44, v53) have no entry: cd lost in print.
    EXTRA_LINES: dict[int, list[int]] = {
        10: [192],
        46: [671], 54: [692, 693, 697], 55: [699, 700, 701], 56: [703, 704, 705, 706, 707, 708, 709],
    }
    FORWARD_ATTACH: dict[int, list[int]] = {
        24: [415], 25: [435], 26: [440], 27: [468], 30: [542], 42: [661], 43: [666],
    }
    EXCLUDE_LINES = {160, 161, 162, 330}  # Ślokavārttika + Bṛhadāraṇyaka quotes

    def is_pada(s: str) -> bool:
        t = s.strip()
        if not t:
            return False
        if re.fullmatch(r"[\s.]+", t):
            return False  # dot-filler lacuna lines
        if t.startswith("(p.") or re.match(r"^_+$", t):
            return False
        if "tadāha" in t:
            return False
        if re.search(r"\btrocyate\b", t):
            return False  # atrocyate/tatrocyate prose-transition formula
        if re.search(r"\([a-zāīūṛḷēōṃḥṅñṭḍṇśṣ]+\. [0-9a-zāīūṛḷēōṃḥṅñṭḍṇśṣ|]+\|[0-9]", t):
            return False  # scripture citations, e.g. (bṛ. ā. 4|5|15)
        if re.search(r"\|\|\s*\d+\s*\|\|", t):
            return False  # verse markers handled by caller
        if t in ("iti ||", "iti"):
            return False
        if re.search(r"[.,;:\-]$", t):
            return False  # prose punctuation; verse lines end | or bare
        if t.rstrip().endswith("|") and not t.rstrip().endswith("||"):
            return True
        return False

    def skippable(s: str) -> bool:
        t = s.strip()
        return (not t) or t.startswith("(p.") or re.match(r"^[_#]+$", t) \
            or t == "oṃ" \
            or re.fullmatch(r"[\s.]+", t) is not None

    def opening_junk(s: str) -> bool:
        t = s.strip()
        # title/author/om lines only: exact short matches, never substrings
        # (a substring test once ate dhūmātsiddhiḥ — a real verse line)
        return t == "oṃ" or t in ("atha", "īśvarasiddhiḥ") or "viracitā" in t

    verses: dict[int, tuple[list[str], list[int]]] = {}
    consumed: set[int] = set()  # line numbers already assigned to a verse
    idx_of = {ln: k for k, (ln, _) in enumerate(lines)}
    marks = [(k, ln, int(m.group(1))) for k, (ln, line) in enumerate(lines)
             for m in [re.search(r"\|\|\s*(\d+)\s*\|\|", line)] if m]
    marks = [(k, ln, n) for k, ln, n in marks if 1 <= n <= 56]
    by_ln = {ln: (k, n) for k, ln, n in marks}
    in_bracket = False
    for k, ln, n in marks:
        line = lines[k][1]
        if n in verses:
            continue
        buf: list[tuple[int, str]] = []
        in_bracket = False
        j = k - 1
        while j >= 0 and len(buf) < 5:
            ln2, pl = lines[j]
            if ln2 in EXTRA_LINES.get(n, []):
                j -= 1
                continue  # taken explicitly below; transparent to the walk
            if ln2 in EXCLUDE_LINES:
                j -= 1
                continue
            if ln2 in consumed:
                break
            t2 = pl.strip()
            bi = t2.find("[")
            if bi >= 0 and "]" not in t2[bi:]:
                # multi-line apparatus opens: keep head text, skip the rest
                head = t2[:bi]
                if head.strip() and pl[:1] in " \t" and is_pada(head):
                    buf.append((ln2, _clean_verse_text(head)))
                    consumed.add(ln2)
                in_bracket = True
                j -= 1
                continue
            if in_bracket:
                if "]" in t2:
                    in_bracket = False
                j -= 1
                continue
            if opening_junk(pl):
                j -= 1
                continue
            if skippable(pl):
                j -= 1
                continue
            if not (pl[:1] in " \t" and is_pada(pl)):
                break
            buf.append((ln2, _clean_verse_text(pl)))
            consumed.add(ln2)
            j -= 1
        buf.reverse()
        pre = _clean_verse_text(line[:line.find("||")])
        if pre.strip():
            buf.append((ln, pre))
        for eln in EXTRA_LINES.get(n, []):
            em = next(((kk, ll) for kk, (ll, _) in enumerate(lines) if ll == eln), None)
            if em is not None:
                _, etxt = lines[em[0]]
                buf.append((eln, _clean_verse_text(etxt)))
                consumed.add(eln)
        for fln in FORWARD_ATTACH.get(n, []):
            buf.append((fln, _clean_verse_text(
                next(t for ll, t in lines if ll == fln))))
            consumed.add(fln)
        buf.sort(key=lambda x: x[0])
        toks = _verse_tokens([t for _, t in buf])
        first = buf[0][0] if buf else ln
        last = buf[-1][0] if buf else ln
        verses[n] = (toks, [first, last])
    return verses, variants
