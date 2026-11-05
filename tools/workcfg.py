#!/usr/bin/env python3
"""tools/workcfg.py — per-work source configuration (one canonical code path, many works).

Each work names its GRETIL source file, its verse-marker dialect, and (where verses
are absolute-numbered across the work) its song->verse-range map. Tools resolve
(work, song) through here instead of hardcoding sivastotravali.

Song ids are human-readable (s01, ajad-p01). Verse numbers are ABSOLUTE within the
work source (matching the edition numbering, e.g. UtAjp_1..27).
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_SA = ROOT.parent / "ipvv" / "site" / "data" / "sanskrit"

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
    "parapravesika": {
        "source": SITE_SA / "parapravesika.txt",
        "kind": "parapravesika",  # Muktabodha M00048 prose prakarana; 9 passages
        "songs": {"par-p01": (1, 1), "par-p02": (2, 2), "par-p03": (3, 3),
                  "par-p04": (4, 4), "par-p05": (5, 5), "par-p06": (6, 6),
                  "par-p07": (7, 7), "par-p08": (8, 8), "par-p09": (9, 9)},
    },
    "bodhapancadasika": {
        "source": SITE_SA / "abhinavagupta-bodhapaJcadasika.txt",
        "kind": "bodhapanca",  # GRETIL (Faliero); 15 numbered verses + unnumbered colophon
        "songs": {f"bod-p{i:02d}": (i, i) for i in range(1, 16)},
    },
    "phrdaya": {
        "source": SITE_SA / "phrdaya.txt",
        "kind": "phrdaya",  # GRETIL (Faliero); 20 mula sutras (vṛtti excluded, mula-only scope)
        "songs": {"phr-p01": (1, 4), "phr-p02": (5, 8), "phr-p03": (9, 12),
                  "phr-p04": (13, 16), "phr-p05": (17, 20)},
    },
    "kramastotra": {
        "source": SITE_SA / "kramastotra.txt",
        "kind": "krama",  # GRETIL (Faliero); 29 stotras (AgKs) + authorial dating verse
        "songs": {f"kram-p{i:02d}": (i, i) for i in range(1, 31)},
    },
    "bodhavilasa": {
        "source": SITE_SA / "ksemaraja-bodhavilasa.txt",
        "kind": "bodhavilasa",  # GRETIL (Pensa ed.); 42 verses + colophon
        # Print numbering jumps 13->15 (no v14 in edition); p02 lists verses explicitly.
        "songs": {"bodh-p01": (1, 10), "bodh-p02": [11, 12, 13, 15, 16, 17, 18, 19, 20],
                  "bodh-p03": (21, 30), "bodh-p04": (31, 40), "bodh-p05": (41, 42)},
    },
    "bhairavanukarana": {
        "source": SITE_SA / "ksemaraja-bhairavanukarana.txt",
        "kind": "bhairavanukarana",  # GRETIL (Cuneo; Gnoli 1958 ed.); 48 verses + invocation
        "songs": {"bhair-p01": (1, 10), "bhair-p02": (11, 20), "bhair-p03": (21, 30),
                  "bhair-p04": (31, 40), "bhair-p05": (41, 48)},
    },
    "paryantapancasika": {
        "source": SITE_SA / "paryantapancasika.txt",
        "kind": "paryanta",  # GRETIL (Faliero); 52 verses (`|| N ||`); no 43 marker (unmarked text)
        "songs": {"pary-p01": (1, 7), "pary-p02": (8, 14), "pary-p03": (15, 20),
                  "pary-p04": (21, 27), "pary-p05": (28, 33), "pary-p06": (34, 39),
                  "pary-p07": (40, 46), "pary-p08": (47, 52)},
    },
    "paramarthasara": {
        "source": SITE_SA / "paramarthasara.txt",
        "kind": "paramartha",  # GRETIL KSTS 7; 105 verses (`|| N ||`), 12 passages (p01 = 1-10)
        "songs": {"param-p01": (1, 10), "param-p02": (11, 19), "param-p03": (20, 28),
                  "param-p04": (29, 37), "param-p05": (38, 46), "param-p06": (47, 55),
                  "param-p07": (56, 64), "param-p08": (65, 73), "param-p09": (74, 82),
                  "param-p10": (83, 91), "param-p11": (92, 100), "param-p12": (101, 105)},
    },
    # Legacy hand-built works (2026-11-01): canonical Sanskrit lives in the
    # work's own frozen T1.md (per-song chains); t1md kind parses those.
    "pancashloki": {
        "source": ROOT / "pancashloki/T1.md",
        "kind": "t1md",
        "songs": {f"pan-p{i:02d}": (i, i) for i in range(1, 6)},
    },
    "anuttarastika": {
        "source": ROOT / "anuttarastika/T1.md",
        "kind": "t1md",
        "songs": {f"anu-p{i:02d}": (i, i) for i in range(1, 9)},
    },
    "bhairavastava": {
        "source": ROOT / "bhairavastava/T1.md",
        "kind": "t1md",
        "songs": {f"bh-p{i:02d}": (i, i) for i in range(1, 11)},
    },
    "anubhavanivedana": {
        "source": ROOT / "anubhavanivedana/T1.md",
        "kind": "t1md",
        "songs": {f"anu-p{i:02d}": (i, i) for i in range(1, 5)},
    },
    "paramarthacarca": {
        "source": ROOT / "paramarthacarca/T1.md",
        "kind": "t1md",
        "songs": {f"par-p{i:02d}": (i, i) for i in range(1, 9)},
    },
    "ghatakarpara": {
        "source": SITE_SA / "ghatakarpara.txt",
        "kind": "ghata",  # GRETIL (Parlier ed.); 21 single-line verses (`// Ghk_N //`), vivrti prose skipped
        "songs": {"ghat-p01": (1, 9), "ghat-p02": (10, 18), "ghat-p03": (19, 21)},
    },
    "spandasandoha": {
        "source": ROOT / "spandasandoha/T1.md",
        "kind": "spanda",  # own frozen T1.md; 13 tokens split 9/4 at rasayati (l2 verse division)
        "songs": {"sand-p01": (1, 2)},
    },
    "tantrasara-a01": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # GRETIL KSTS 17 (Nirnaya Sagara 1918); ahnika 1 = 3 mangala + 2 prose units
        "ahnika": 1,
        "songs": {"tsa-a01": (1, 5)},
    },
    "tantrasara-a02": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 2 = anupāya: 4 units (promise, recognition, four impossibilities, identity)
        "ahnika": 2,
        "songs": {"tsa-a02": (1, 4)},
    },
    "tantrasara-a18": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 18 = abhiṣeka: 2 prose units (18.1 consecration rule; 18.2 delegation + vidyāvrata + testing)
        "ahnika": 18,
        "songs": {"tsa-a18": (1, 2)},
    },
    "tantrasara-a19": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 19 = post-mortem/śrāddha initiation: 7 units (19.1 admission; 19.2 corpse-rite; 19.3 joining+burning; 19.4 offering; 19.5 daily; 19.6 knower exempt; 19.7 image-abandonment seal)
        "ahnika": 19,
        "songs": {"tsa-a19": (1, 7)},
    },
    "tantrasara-a17": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 17: 6 units
        "ahnika": 17,
        "songs": {"tsa-a17": (1, 6)},
    },
    "tantrasara-a19": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 19: 7 units
        "ahnika": 19,
        "songs": {"tsa-a19": (1, 7)},
    },
    "tantrasara-a21": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 21: 13 units
        "ahnika": 21,
        "songs": {"tsa-a21": (1, 13)},
    },
    "tantrasara-a10": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 10: 18 units
        "ahnika": 10,
        "songs": {"tsa-a10": (1, 18)},
    },
    "tantrasara-a16": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 16: 24 units
        "ahnika": 16,
        "songs": {"tsa-a16": (1, 24)},
    },
    "tantrasara-a11": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 11: 25 units
        "ahnika": 11,
        "songs": {"tsa-a11": (1, 25)},
    },
    "tantrasara-a07": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 7: 28 units
        "ahnika": 7,
        "songs": {"tsa-a07": (1, 28)},
    },
    "tantrasara-a14": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 14: 29 units
        "ahnika": 14,
        "songs": {"tsa-a14": (1, 29)},
    },
    "tantrasara-a05": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 5
        "ahnika": 5,
        "songs": {"tsa-a05": (1, 43)},
    },
    "tantrasara-a04": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 4
        "ahnika": 4,
        "songs": {"tsa-a04": (1, 46)},
    },
    "tantrasara-a09": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 9
        "ahnika": 9,
        "songs": {"tsa-a09": (1, 53)},
    },
    "tantrasara-a22": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 22: 53 units, verse-number gap (no u46, runs to 54)
        "ahnika": 22,
        "songs": {"tsa-a22": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54]},
    },
    "tantrasara-a20": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 20: 65 units
        "ahnika": 20,
        "songs": {"tsa-a20": (1, 65)},
    },
    "tantrasara-a06": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 6: 82 units
        "ahnika": 6,
        "songs": {"tsa-a06": (1, 82)},
    },
    "tantrasara-a08": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 8: 93 units
        "ahnika": 8,
        "songs": {"tsa-a08": (1, 93)},
    },
    "tantrasara-a13": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 13: 101 units
        "ahnika": 13,
        "songs": {"tsa-a13": (1, 101)},
    },
    "tantrasara-a03": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 3: 34 units
        "ahnika": 3,
        "songs": {"tsa-a03": (1, 34)},
    },
    "tantrasara-a15": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 15: 7 units
        "ahnika": 15,
        "songs": {"tsa-a15": (1, 7)},
    },
    "tantrasara-a12": {
        "source": SITE_SA / "tantrasara.txt",
        "kind": "abhts",  # ahnika 12: 10 units
        "ahnika": 12,
        "songs": {"tsa-a12": (1, 10)},
    },
}


def work_config(work: str) -> dict | None:
    """Resolve existing registrations or a pinned source-intake manifest."""
    if work in WORKS and WORKS[work].get("kind") != "segments":
        return WORKS[work]
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", work or ""):
        return None
    folder = ROOT / work / "source"
    manifest_path = folder / "manifest.json"
    if not manifest_path.exists():
        return None
    from intake import validate_segments
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = folder / "edition.txt"
    segment_path = folder / "segments.json"
    raw, segment_bytes = source_path.read_bytes(), segment_path.read_bytes()
    if (manifest.get("format") != "source-intake/1" or manifest.get("work") != work or
        hashlib.sha256(raw).hexdigest() != manifest.get("source_sha256") or
        hashlib.sha256(segment_bytes).hexdigest() != manifest.get("segments_sha256")):
        raise ValueError(f"{work}: source intake hashes or identity do not match")
    segments = json.loads(segment_bytes)
    errors = validate_segments(raw, segments)
    if errors:
        raise ValueError(f"{work}: invalid source segments: {'; '.join(errors)}")
    songs = {}
    for item in segments:
        songs.setdefault(item["song"], []).append(item["verse"])
    cfg = {"source": source_path, "kind": "segments", "songs": songs,
           "segments": segments, "source_bytes": raw}
    WORKS[work] = cfg
    return cfg


def song_verses(work: str, song: str) -> list[int]:
    """Absolute verse numbers belonging to (work, song)."""
    cfg = work_config(work)
    if cfg is None:
        raise KeyError(f"unknown work {work}")
    if "songs" in cfg:
        rng = cfg["songs"][song]
        if isinstance(rng, list):
            return list(rng)
        lo, hi = rng
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


def parse_parapravesika(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse Muktabodha M00048 Parapravesika prose into 9 passages.

    Returns passage 1..9 -> (tokens, [first_ln, last_ln]). Splits hand-set from
    the edition layout (mula + bracketed vrtti kept in text order; KSTS page
    marks `(p. N)`, verse `||` markers, `[`/`]` brackets, and lone `-` list
    dashes stripped; wrap-hyphen continuations joined). Editorial verses +
    scribe line (l.287+) excluded. Boundaries: p01 25-35; p02 37-50;
    p03 51-78+79head; p04 79tail-110; p05 111-140; p06 141tail-157;
    p07 158-209head; p08 209tail-251; p09 253-285 (colophon incl.).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    lines = {i + 1: ln for i, ln in enumerate(raw)}

    def head(ln: int, marker: str) -> str:
        t = lines[ln]
        i = t.find(marker)
        assert i >= 0, f"marker {marker!r} missing on line {ln}"
        return t[:i]

    def tail(ln: int, marker: str) -> str:
        t = lines[ln]
        i = t.find(marker)
        assert i >= 0, f"marker {marker!r} missing on line {ln}"
        return t[i:]

    segs: dict[int, list[str]] = {
        1: [lines[n] for n in range(25, 36)],
        2: [lines[n] for n in range(37, 51)],
        3: [lines[n] for n in range(51, 79)] + [head(79, "ata eva")],
        4: [tail(79, "ata eva")] + [lines[n] for n in range(80, 111)],
        5: [lines[n] for n in range(111, 141)],
        6: [tail(141, "evaṃ ca")] + [lines[n] for n in range(142, 158)],
        7: [lines[n] for n in range(158, 209)] + [head(209, "atra kalānāma")],
        8: [tail(209, "atra kalānāma")] + [lines[n] for n in range(210, 252)],
        9: [lines[n] for n in range(253, 286)],
    }
    out: dict[int, tuple[list[str], list[int]]] = {}
    bounds = {1: (25, 35), 2: (37, 50), 3: (51, 79), 4: (79, 110), 5: (111, 140),
              6: (141, 157), 7: (158, 209), 8: (209, 251), 9: (253, 285)}
    for n, texts in segs.items():
        joined = " ".join(texts)
        joined = re.sub(r"\(p\.\s+\d+\)", " ", joined)  # KSTS page marks (may span lines pre-join)
        toks: list[str] = []
        for wd in re.sub(r"\|\|", " ", joined.replace("[", " ").replace("]", " ")).split():
                if wd == "-" or wd == "|":
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        toks = [w for w in toks if w not in ("-", "|", "||")]
        out[n] = (toks, [bounds[n][0], bounds[n][1]])
    return out, []


def parse_bodhapanca(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Bodhapañcadaśikā (15 numbered verses, AgBpd_N markers).

    Returns verse 1..15 -> (tokens, [first_ln, marker_ln]). Each verse = the
    marker line's pre-text + up to 2 preceding pada lines (ending in |).
    The unnumbered colophon (sukumāramatīn...) is excluded (paratext scope).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    for i, ln in enumerate(raw):
        m = re.search(r"\|\|\s*\[AgBpd_(\d+)\]", ln)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 15 or n in verses:
            continue
        buf: list[str] = []
        j = i - 1
        while j >= 0 and len(buf) < 2:
            t = raw[j].strip()
            if not t or t.startswith("#"):
                j -= 1
                continue
            if re.search(r"\[AgBpd_\d+\]", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = ln[:m.start()]
        if pre.strip():
            buf.append(pre)
        toks: list[str] = []
        for t in buf:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|",):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        verses[n] = ([w for w in toks if w not in ("|",)], [i - len(buf) + 1, i + 1])
    return verses, []


def parse_phrdaya(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Pratyabhijnahrdaya mula (20 sutras, `|| N ||` markers).

    Returns sutra 1..20 -> (tokens, [first_ln, marker_ln]). Each sutra is
    usually one line; preceding pada-continuations (ending in |) attach (max 1).
    Commentary [N] citations (single-pipe form) never match: only the
    double-pipe `|| N ||` mula form is collected. Scope is mula-only;
    Ksemaraja's vrtti and the mangala are excluded (recorded in the work NOTE).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    for i, ln in enumerate(raw):
        m = re.search(r"\|\|\s*(\d+)\s*\|\|\s*$", ln)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 20 or n in verses:
            continue
        buf: list[str] = []
        if i - 1 >= 0:
            t = raw[i - 1].strip()
            if t and not t.startswith("#") and not re.search(r"\|\|\s*\d+\s*\|\|", t) \
                    and t.rstrip().endswith("|"):
                buf.append(t)
        pre = ln[:m.start()]
        if pre.strip():
            buf.append(pre)
        toks: list[str] = []
        for t in buf:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|",):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        verses[n] = ([w for w in toks if w not in ("|",)], [i - len(buf) + 1, i + 1])
    return verses, []


def parse_krama(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Kramastotra (29 stotras + authorial dating verse).

    Returns verse 1..30 -> (tokens, [first_ln, marker_ln]). Verses 1..29 end
    with `|| [AgKs_N]`; each takes the marker line's pre-text + up to 3
    preceding pada lines (ending in |). Verse 30 is the unmarked dating verse
    (ṣaṭṣaṣṭi...); the third-person colophon is excluded (paratext scope).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    lines = {i + 1: ln for i, ln in enumerate(raw)}

    def toks_of(texts: list[str]) -> list[str]:
        toks: list[str] = []
        for t in texts:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|",):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        return [w for w in toks if w not in ("|",)]

    verses: dict[int, tuple[list[str], list[int]]] = {}
    for ln, line in lines.items():
        m = re.search(r"\|\|\s*\[AgKs_(\d+)\]\s*$", line)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 29 or n in verses:
            continue
        buf: list[str] = []
        j = ln - 1
        while j >= 1 and len(buf) < 3:
            t = lines[j].strip()
            if not t or t.startswith("#"):
                j -= 1
                continue
            if re.search(r"\[AgKs_\d+\]", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = line[:m.start()]
        if pre.strip():
            buf.append(pre)
        verses[n] = (toks_of(buf), [buf and ln - len(buf), ln])
    # dating verse: ṣaṭṣaṣṭi couplet just before the colophon
    dln = next((ln for ln, t in lines.items() if "ṣaṭṣaṣṭinām" in t), None)
    if dln is not None:
        buf = [lines[dln], lines[dln + 1]]
        verses[30] = (toks_of(buf), [dln, dln + 1])
    return verses, []


def parse_bodhavilasa(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Bodhavilasa (42 verses, `// N //` markers, Pensa ed.).

    Returns verse 1..42 -> (tokens, [first_ln, marker_ln]). Each verse takes
    the marker line's pre-text + up to 3 preceding pada lines (ending in |).
    The colophon (rājñaḥ kṣemābhidhānasya...) is excluded (paratext scope).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    for i, ln in enumerate(raw):
        m = re.search(r"//\s*(\d+)\s*//\s*$", ln)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 42 or n in verses:
            continue
        buf: list[str] = []
        j = i - 1
        while j >= 0 and len(buf) < 3:
            t = raw[j].strip()
            if not t or t.startswith("#"):
                j -= 1
                continue
            if re.search(r"//\s*\d+\s*//", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = ln[:m.start()]
        if pre.strip():
            buf.append(pre)
        toks: list[str] = []
        for t in buf:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|", "/"):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        verses[n] = ([w for w in toks if w not in ("|", "/")], [i - len(buf) + 1, i + 1])
    # v12 printed as two marked couplets (4 padas, // 12 // twice): merge.
    # The walk above keeps the FIRST hit; collect the second explicitly.
    hits = [i + 1 for i, line in enumerate(raw) if re.search(r"//\s*12\s*//\s*$", line)]
    if len(hits) == 2:
        l2 = hits[1]
        m2 = re.search(r"//\s*12\s*//\s*$", raw[l2 - 1])
        extra = [raw[l2 - 2], raw[l2 - 1][:m2.start()] if m2 else raw[l2 - 1]]
        etoks: list[str] = []
        for t in extra:
            for wd in re.sub(r"\|\|", " ", t).split():
                if wd not in ("|", "/"):
                    etoks.append(wd)
        old_toks, (a, b) = verses[12]
        verses[12] = (old_toks + etoks, [a, l2])
    # v01 takes the standalone mangala line too (T1 glosses it; other works include mangalas)
    if 1 in verses:
        toks, (a, b) = verses[1]
        verses[1] = (["oṃ", "namo", "netrāya"] + toks, [7, b])
    return verses, []


def parse_bhairavanukarana(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Bhairavanukaranastotra (48 verses, `|| [KsBhAS_N]` markers).

    Returns verse 1..48 -> (tokens, [first_ln, marker_ln]). Each verse takes
    the marker line's pre-text + up to 3 preceding pada lines (ending in |).
    The invocation (oṃ namaś cidbhairavāya) opens verse 1 (T1 glosses it).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    for i, ln in enumerate(raw):
        m = re.search(r"\|\|\s*\[KsBhAS_(\d+)\]\s*$", ln)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 48 or n in verses:
            continue
        buf: list[str] = []
        j = i - 1
        while j >= 0 and len(buf) < 3:
            t = raw[j].strip()
            if not t or t.startswith("#"):
                j -= 1
                continue
            if re.search(r"\[KsBhAS_\d+\]", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = ln[:m.start()]
        if pre.strip():
            buf.append(pre)
        toks: list[str] = []
        for t in buf:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|", "/"):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        verses[n] = ([w for w in toks if w not in ("|", "/")], [i - len(buf) + 1, i + 1])
    return verses, []


def parse_paryanta(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Paryantapancasika (52 verses).

    Returns verse 1..52 -> (tokens, [first_ln, marker_ln]). Verses end with
    `|| N ||` — except v43, whose print marks only `|| 43` (single pipes).
    Each verse takes the marker line's pre-text + up to 3 preceding pada
    lines (ending in |). Invocation + colophon excluded (paratext scope).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}

    def collect(mark_idx: int, n: int) -> None:
        buf: list[str] = []
        j = mark_idx - 1
        while j >= 0 and len(buf) < 3:
            t = raw[j].strip()
            if not t:
                break  # blank lines delimit verses (keeps invocations out)
            if t.startswith("#"):
                j -= 1
                continue
            if re.search(r"\|\|\s*\d+\s*\|\|", t) or re.search(r"\|\|\s*43\s*$", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = raw[mark_idx][:re.search(r"\|\|", raw[mark_idx]).start()]
        if pre.strip():
            buf.append(pre)
        toks: list[str] = []
        for t in buf:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|", "/"):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        verses[n] = ([w for w in toks if w not in ("|", "/")],
                     [mark_idx - len(buf) + 1, mark_idx + 1])

    for i, ln in enumerate(raw):
        m = re.search(r"\|\|\s*(\d+)\s*\|\|\s*$", ln)
        if m and 1 <= int(m.group(1)) <= 52 and int(m.group(1)) not in verses:
            collect(i, int(m.group(1)))
    for i, ln in enumerate(raw):
        if re.search(r"\|\|\s*43\s*$", ln) and 43 not in verses:
            # single-pipe v43 marker: pre-text is the full line head
            pre = ln[:ln.find("||")]
            toks = [w for w in re.sub(r"\|\|", " ", pre).split() if w not in ("|", "/")]
            prev = [raw[i - 1]] if raw[i - 1].strip() else []
            ptoks: list[str] = []
            for t in prev + [pre]:
                for wd in re.sub(r"\|\|", " ", t).split():
                    if wd not in ("|", "/"):
                        ptoks.append(wd)
            verses[43] = (ptoks, [i, i + 1])
    return verses, []


def parse_t1md(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse a legacy work's own frozen T1.md (per-song `[and]-` chains).

    Returns verse -> (surfaces, [header_ln, end_ln]). Verse numbers come from
    the `## <song> (N)` section headers. `[is]` markers are skipped, matching
    the original data builds.
    """
    lines = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    cur: int | None = None
    start = 0
    buf: list[str] = []

    def flush(end: int) -> None:
        if cur is None:
            return
        blob = "\n".join(buf).replace("[is]", "")
        blob = re.sub(r"(?<!\[and\])-\n", "", blob)  # join word-split hyphens; keep [and]- markers split across lines
        blob = blob.replace("\n", " ")
        toks: list[str] = []
        for g, s in re.findall(r"\[and\]-(.*?)\(([^)]+)\)", blob, re.S):
            if "(" in s or ")" in s:
                continue
            g = re.sub(r"\([^)]*\)", "", g).strip()  # keep surface, drop parenthetical gloss
            toks.append(re.sub(r"\s+", " ", s).strip())
        if toks and cur not in verses:
            verses[cur] = (toks, [start, end])

    for i, ln in enumerate(lines):
        m = re.match(r"## (\S+)(?:\s+\((\d+)(?:[-–]\d+)?\))?", ln)
        if m and m.group(2):
            flush(i)
            cur = int(m.group(2))
            start = i + 1
            buf = []
            continue
        if cur is not None and ln.strip() and not ln.startswith("*"):
            buf.append(ln)
    flush(len(lines))
    return verses, []


def parse_ghata(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Ghatakarpara verses (21 single-line `// Ghk_N //` verses).

    Returns verse 1..21 -> (tokens, [ln, ln]). Vivrti prose (GhkV_) skipped.
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    verses: dict[int, tuple[list[str], list[int]]] = {}
    for i, ln in enumerate(raw):
        m = re.search(r"//\s*Ghk_(\d+)\s*//\s*$", ln)
        if not m or re.search(r"GhkV_", ln):
            continue
        n = int(m.group(1))
        if not 1 <= n <= 21 or n in verses:
            continue
        pre = ln[:m.start()]
        toks = [w for w in re.sub(r"\|\|", " ", pre).split() if w not in ("|", "/")]
        verses[n] = (toks, [i + 1, i + 1])
    return verses, []


def parse_spanda(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse Spandasandoha frozen T1.md (13 tokens; verses split 9/4 at rasayati).

    The split follows the work's own l2 verse division (v1 ends rasayati).
    """
    spans, _ = parse_t1md(source)
    toks, lines = spans[1]
    cut = toks.index("rasayati") + 1 if "rasayati" in toks else 9
    return {1: (toks[:cut], lines), 2: (toks[cut:], lines)}, []


def parse_paramartha(source: Path) -> tuple[dict[int, tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Paramarthasara (105 verses, `|| N ||` markers, KSTS 7).

    Returns verse 1..105 -> (tokens, [first_ln, marker_ln]). Each verse takes
    the marker line's pre-text + up to 3 preceding pada lines (ending in |).
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    lines = {i + 1: ln for i, ln in enumerate(raw)}
    verses: dict[int, tuple[list[str], list[int]]] = {}

    def toks_of(texts: list[str]) -> list[str]:
        toks: list[str] = []
        for t in texts:
            t = re.sub(r"\|\|", " ", t)
            for wd in t.split():
                if wd in ("|", "/"):
                    continue
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        return [w for w in toks if w not in ("|", "/")]

    for ln, line in lines.items():
        m = re.search(r"\|\|\s*(\d+)\s*\|\|\s*$", line)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= 105 or n in verses:
            continue
        buf: list[str] = []
        j = ln - 1
        while j >= 1 and len(buf) < 3:
            t = lines[j].strip()
            if not t or t.startswith("#"):
                j -= 1
                continue
            if re.search(r"\|\|\s*\d+\s*\|\|", t):
                break
            buf.append(t)
            if not t.rstrip().endswith("|"):
                break
            j -= 1
        buf.reverse()
        pre = line[:m.start()]
        if pre.strip():
            buf.append(pre)
        verses[n] = (toks_of(buf), [ln - len(buf), ln])
    return verses, []


def parse_abhts(source: Path) -> tuple[dict[tuple[int, int], tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Tantrasara (`// AbhTs_A.N //` markers, prose + verse mixed).

    Returns (ahnika, num) -> (tokens, [first_ln, marker_ln]). Each unit takes
    all non-empty lines since the previous marker (or file start), excluding
    ### provenance lines and `Tantrasāra, ... āhnikam` headers. Pāda marks
    (|, /) stripped; wrap-hyphen continuations joined.
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    units: dict[tuple[int, int], tuple[list[str], list[int]]] = {}
    buf: list[tuple[int, str]] = []

    def toks_of(texts: list[str]) -> list[str]:
        toks: list[str] = []
        for t in texts:
            t = re.sub(r"//.*", "", t)
            t = t.replace("|", " ").replace("/", " ")
            for wd in t.split():
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        return [w for w in toks if w]

    def flush(marker_ln: int, key: tuple[int, int]):
        texts = [s for _, s in buf]
        first_ln = buf[0][0] if buf else marker_ln
        units[key] = (toks_of(texts), [first_ln, marker_ln])

    for ln, line in enumerate(raw, start=1):
        t = line.strip()
        if not t or t.startswith("###"):
            continue
        if re.match(r"^Tantrasāra,.*āhnikam$", t):
            continue
        m = re.search(r"//\s*AbhTs_(\d+)\.(\d+)\s*(?://)?\s*$", t)
        if m:
            pre = t[:m.start()].strip()
            if pre:
                buf.append((ln, pre))
            flush(ln, (int(m.group(1)), int(m.group(2))))
            buf = []
        else:
            buf.append((ln, t))
    return units, []


def parse_taloka(source: Path) -> tuple[dict[tuple[int, int], tuple[list[str], list[int]]], list[tuple[int, str]]]:
    """Parse GRETIL Tantraloka (`[AbhT_A.V]` verse markers, śloka text).

    Returns (ahnika, num) -> (tokens, [first_ln, marker_ln]). Ahnika tracked
    via `::CN ...āhnikam` headers (C6/C7 split across two lines). Each verse
    takes all non-empty lines since the previous marker. Pāda marks (|, /)
    and `//` comments stripped; wrap-hyphen continuations joined.
    """
    raw = source.read_text(encoding="utf-8").splitlines()
    units: dict[tuple[int, int], tuple[list[str], list[int]]] = {}
    buf: list[tuple[int, str]] = []
    ahnika = 0

    def toks_of(texts: list[str]) -> list[str]:
        toks: list[str] = []
        for t in texts:
            t = re.sub(r"//.*", "", t)
            t = t.replace("|", " ").replace("/", " ")
            for wd in t.split():
                if toks and toks[-1].endswith("-"):
                    toks[-1] = toks[-1][:-1] + wd
                else:
                    toks.append(wd)
        return [w for w in toks if w]

    def flush(marker_ln: int, key: tuple[int, int]):
        texts = [s for _, s in buf]
        first_ln = buf[0][0] if buf else marker_ln
        units[key] = (toks_of(texts), [first_ln, marker_ln])

    for ln, line in enumerate(raw, start=1):
        t = line.strip()
        if not t or t.startswith("###"):
            continue
        m = re.match(r"^::C(\d+)\b", t)
        if m:
            ahnika = int(m.group(1))
            continue
        m = re.search(r"\[AbhT_(\d+)\.(\d+)\]\s*$", t)
        if m:
            pre = t[:m.start()].strip()
            if pre:
                buf.append((ln, pre))
            a = int(m.group(1))
            if a != ahnika:
                ahnika = a
            flush(ln, (ahnika, int(m.group(2))))
            buf = []
        else:
            buf.append((ln, t))
    return units, []


def source_spans(work: str) -> dict[int, list[str]] | None:
    """Full-work source spans {verse: tokens} via workcfg, or None if unregistered.

    One canonical code path: tools call this instead of per-kind branches.
    sivastotravali (song-numbered UtSst markers) is NOT covered — tools keep
    their load_gretil_song fallback for it.
    """
    cfg = work_config(work)
    if cfg is None or "songs" not in cfg:
        return None
    src = Path(cfg["source"])
    kind = cfg.get("kind")
    if kind == "segments":
        raw = cfg["source_bytes"]
        return {item["verse"]: raw[item["start"]:item["end"]].decode("utf-8").split()
                for item in cfg["segments"]}
    elif kind == "utajp":
        spans = parse_utajp(src)
    elif kind == "sambandha":
        spans, _ = parse_sambandha(src)
    elif kind == "isvara":
        spans, _ = parse_isvara(src)
    elif kind == "parapravesika":
        spans, _ = parse_parapravesika(src)
    elif kind == "bodhapanca":
        spans, _ = parse_bodhapanca(src)
    elif kind == "phrdaya":
        spans, _ = parse_phrdaya(src)
    elif kind == "krama":
        spans, _ = parse_krama(src)
    elif kind == "bodhavilasa":
        spans, _ = parse_bodhavilasa(src)
    elif kind == "bhairavanukarana":
        spans, _ = parse_bhairavanukarana(src)
    elif kind == "paryanta":
        spans, _ = parse_paryanta(src)
    elif kind == "paramartha":
        spans, _ = parse_paramartha(src)
    elif kind == "t1md":
        spans, _ = parse_t1md(src)
    elif kind == "ghata":
        spans, _ = parse_ghata(src)
    elif kind == "spanda":
        spans, _ = parse_spanda(src)
    elif kind == "abhts":
        units, _ = parse_abhts(src)
        ahnika = cfg.get("ahnika", 1)
        spans = {num: val for (a, num), val in units.items() if a == ahnika}
    elif kind == "taloka":
        units, _ = parse_taloka(src)
        ahnika = cfg.get("ahnika", 1)
        spans = {num: val for (a, num), val in units.items() if a == ahnika}
    else:
        return None
    return {v: toks for v, (toks, _) in spans.items()}
