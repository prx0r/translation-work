#!/usr/bin/env python3
"""build_search_index.py — one gate-labeled, license-tagged index over everything.

Records: canon passages (22 projected works), pushing probes, published
essays, theme adjudications. Gate labels enforced at build (BLOCKED English
never embedded) and again at retrieval. Embeddings: CF Workers AI bge-m3
(free tier). Output is a build artifact (--out, default
~/.scholar/search-index/): records.jsonl + vectors.json + meta.json.

  build_search_index.py --work paramarthasara   # pilot one work
  build_search_index.py                         # full build (resume-safe)
  build_search_index.py --rebuild               # ignore existing output
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

TW = Path(os.environ.get("TRANSLATION_WORK_ROOT", "/root/translation-work"))
SVREAD = Path(os.environ.get("SVREAD_ROOT", "/root/svread"))
IPVV = Path(os.environ.get("IPVV_ROOT", "/root/ipvv"))
NIB = Path(os.environ.get("NIBBANAHELP_ROOT", "/root/nibbanahelp"))
DEFAULT_OUT = Path.home() / ".scholar" / "search-index"
MODEL = "@cf/baai/bge-m3"


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def sha(x) -> str:
    return hashlib.sha256(canon(x)).hexdigest()


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def gate_of(work: str, song: str | None) -> str:
    gates = load_json(TW / work / "GATE.json") or {}
    if song and isinstance(gates.get(song), dict):
        return gates[song].get("deterministic_gate", "UNKNOWN")
    return "UNKNOWN"


def song_of(target: str) -> str:
    return target.rsplit("-v", 1)[0] if "-v" in target else target


def passage_records(work: str, proj: dict) -> list:
    originals = proj.get("originals", {}) or {}
    verses = proj.get("source_verses", {}) or {}
    arg_q = {}
    for path in sorted((IPVV / "site" / "data" / "arguments").glob(f"{work}-*.json")):
        p = load_json(path) or {}
        key = p.get("passage_id", "") or ""
        if key and p.get("question"):
            arg_q[key.split(":")[-1]] = p["question"][:200]
            arg_q[p.get("id", "")] = p["question"][:200]
    out = []
    for target in sorted(verses):
        song = song_of(target)
        gate = gate_of(work, song)
        t1 = originals.get("t1", {}).get(target)
        l2 = originals.get("l2", {}).get(target)
        parts = [f"{work} {target}"]
        if isinstance(t1, dict):
            gl = " ".join(f"{t.get('surface','')}({t.get('gloss','')})"
                          for t in t1.get("tokens", [])[:40]
                          if isinstance(t, dict))
            if gl:
                parts.append("T1: " + gl[:600])
        elif isinstance(t1, str):
            parts.append("T1: " + t1[:600])
        if gate == "PASS" and isinstance(l2, (str, dict)):
            text = l2 if isinstance(l2, str) else l2.get("plain_english", "") or l2.get("text", "")
            if text:
                parts.append("EN: " + str(text)[:800])
        elif gate != "PASS":
            parts.append("(English withheld: gate " + gate + ")")
        q = arg_q.get(target, "")
        text = ("passage: " + (q + " " if q else "") + " ".join(parts))[:1500]
        out.append({"id": f"chunk:{work}:{target}", "kind": "passage",
                    "work": work, "ref": target,
                    "verses": (verses[target] if isinstance(verses[target], str)
                               else "")[:200] if isinstance(verses.get(target), str) else "",
                    "text": text, "gate": gate if gate in ("PASS", "BLOCKED") else "UNKNOWN",
                    "license": "CC-BY-NC-SA (vendored Sanskrit); our English free use",
                    "source": f"svread data/scholar/{work}.json"})
    return out


def probe_records() -> list:
    cat = load_json(SVREAD / "data" / "pushing-catalog.json") or {}
    out = []
    for r in cat.get("records", []) if isinstance(cat, dict) else []:
        out.append({"id": f"crux:{r.get('work')}:{Path(r.get('file','')).stem}",
                    "kind": "probe", "work": r.get("work", ""),
                    "ref": r.get("file", ""),
                    "text": ("question: " + str(r.get("question", "")) + " — " +
                             str(r.get("title", "")))[:500],
                    "gate": "OWNER", "license": "ours",
                    "source": "pushing catalog"})
    return out


def essay_records() -> list:
    out = []
    idx = SVREAD / "data" / "scholar"
    if not idx.is_dir():
        return out
    for proj_path in sorted(idx.glob("*.json")):
        if proj_path.name == "index.json":
            continue
        proj = load_json(proj_path) or {}
        for e in proj.get("essays", []) or []:
            if not isinstance(e, dict):
                continue
            out.append({"id": f"essay:scholar:{proj.get('work')}:{e.get('essay_id')}",
                        "kind": "essay", "work": proj.get("work", ""),
                        "ref": e.get("essay_id", ""),
                        "text": ("question: " + str(e.get("title", "")) + " " +
                                 str(e.get("text", ""))[:800]),
                        "gate": "PUBLISHED", "license": str(e.get("rights", "")),
                        "source": "scholar projection"})
    return out


def theme_records() -> list:
    out = []
    tdir = IPVV / "site" / "data" / "themes"
    for name in ("adjudication-cl3.json", "theme-map-ipvv-v0.json"):
        d = load_json(tdir / name)
        if not d:
            continue
        items = d if isinstance(d, list) else [d]
        for i, t in enumerate(items):
            if not isinstance(t, dict):
                continue
            label = (t.get("proposed_theme", {}) or {}).get("label", t.get("label", name))
            claim = (t.get("proposed_theme", {}) or {}).get("core_claim", "")
            out.append({"id": f"theme:{name}:{i}", "kind": "theme",
                        "work": t.get("theme_id", t.get("work", "")),
                        "ref": name,
                        "text": ("question: " + str(label) + " — " + str(claim))[:600],
                        "gate": "OWNER", "license": "ours",
                        "source": f"ipvv themes/{name}"})
    return out


def cf_token():
    for path in (Path("/root/.r2-env"), Path.home() / ".cf-api-token"):
        try:
            text = path.read_text()
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("CF_API_TOKEN="):
                return line.split("=", 1)[1].strip()
        if path.name == ".cf-api-token" and text.strip() and "=" not in text:
            return text.strip()
    return os.environ.get("CF_API_TOKEN", "") or os.environ.get("CLOUDFLARE_API_TOKEN", "")


def account_id():
    try:
        text = Path("/root/.r2-env").read_text()
    except OSError:
        text = ""
    for line in text.splitlines():
        if line.strip().startswith("CF_ACCOUNT_ID="):
            return line.split("=", 1)[1].strip()
    return os.environ.get("CF_ACCOUNT_ID", "954612afb5a97bb15dddcdc70176813d")


def embed_batch(texts, token, account):
    url = (f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/"
           + MODEL.replace("@cf/", "@cf/"))
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/@cf/baai/bge-m3",
        data=json.dumps({"text": texts}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "svread-scholar-mcp/0.1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return result["result"]["data"]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="build_search_index.py")
    p.add_argument("--work", default=None)
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--rebuild", action="store_true")
    p.add_argument("--batch", type=int, default=10)
    args = p.parse_args(argv)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    records = []
    idx = SVREAD / "data" / "scholar"
    works = [args.work] if args.work else sorted(
        p.stem for p in idx.glob("*.json") if p.stem != "index")
    for work in works:
        proj = load_json(idx / f"{work}.json")
        if not proj:
            print(f"skip {work}: no projection", file=sys.stderr)
            continue
        records.extend(passage_records(work, proj))
    records.extend(probe_records())
    records.extend(essay_records())
    records.extend(theme_records())
    print(f"records: {len(records)}", file=sys.stderr)

    token, account = cf_token(), account_id()
    if not token:
        raise SystemExit("error: no CF token (CF_API_TOKEN env or /root/.r2-env)")
    ids = [r["id"] for r in records]
    vecpath = outdir / "vectors.json"
    have = {}
    if vecpath.is_file() and not args.rebuild:
        try:
            old = json.loads(vecpath.read_text(encoding="utf-8"))
            have = dict(zip(old.get("ids", []), old.get("vectors", [])))
        except ValueError:
            pass
    vectors, done = [], 0
    todo = [(i, r) for i, r in enumerate(records) if r["id"] not in have]
    for start in range(0, len(todo), args.batch):
        batch = todo[start:start + args.batch]
        data = embed_batch([r["text"] for _, r in batch], token, account)
        # bge-m3 returns one vector per input, in request order
        for (_, r), vec in zip(batch, data):
            have[r["id"]] = [round(float(x), 5) for x in vec]
            done += 1
        print(f"embedded {done}/{len(todo)}", file=sys.stderr)
        time.sleep(1)
    (outdir / "records.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8")
    (outdir / "vectors.json").write_text(
        json.dumps({"ids": ids, "vectors": [have[i] for i in ids]}),
        encoding="utf-8")
    (outdir / "meta.json").write_text(json.dumps(
        {"model": MODEL, "count": len(records), "works": works,
         "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
        indent=1), encoding="utf-8")
    print(f"wrote {outdir} ({len(records)} records)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
