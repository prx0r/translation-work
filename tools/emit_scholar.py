#!/usr/bin/env python3
"""tools/emit_scholar.py — project a work's scholar/ ledgers + layer originals to svread.

  python3 tools/emit_scholar.py --work paramarthasara

Writes `/root/svread/data/scholar/<work>.json` (+ `index.json`) for the Scholar hub.
Originals come from the canonical `data/<song>.<layer>.json` files (the same bytes
`tools/scholar.py show` prints) — the hub never re-derives them.

Read-only: never writes back into this repo.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVREAD = ROOT.parent / "svread"
sys.path.insert(0, str(ROOT / "tools"))
import scholar as sch  # noqa: E402  (reuse the exact loaders + hashers)
import agent_contract  # noqa: E402

# Remove only after the complete source and all dependent layers have been
# independently repaired and revalidated. A PASS proof did not detect the
# missing first lines in this work's current data.
SOURCE_COVERAGE_HOLDS = {
    'ghatakarpara': 'Source alignment incomplete: all 21 numbered verses require upstream repair and review.'
}


def song_craft(work: str, originals: dict) -> dict:
    """Expose editorial rationale only for an exact match to the eligible L4."""
    result, canonical = {}, originals.get('l4', {})
    for path in sorted((ROOT / work).glob('L4-*.DRAFT.json')):
        try:
            draft = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        rows = draft if isinstance(draft,list) else draft.get('verses',[draft]) if isinstance(draft,dict) else []
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('l4'),dict):
                continue
            verse = row['l4'].get('verse_id')
            if verse not in canonical or row['l4'] != canonical[verse]:
                continue
            notes = {key:row[key] for key in ('craft','craft_notes','rejected','reads','reads_against') if key in row}
            if notes:
                result.setdefault(verse,[]).append({'file':str(path.relative_to(ROOT)),
                    'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'l4_sha256':sch.sha(row['l4']),'notes':notes})
    return result


def displayed_sources(work: str, eligible: set[str], originals: dict) -> dict:
    """Display existing public source with provenance; never create an edition."""
    path = ROOT.parent / 'ipvv/site/data/translations' / f'{work}.json'
    rows = json.loads(path.read_text(encoding='utf-8')) if path.is_file() else []
    result = {}
    for row in rows:
        target = row.get('chunk','')
        if (target not in originals.get('t1',{}) or row.get('gate') != 'PASS' or
            not row.get('sanskrit') or sch.song_of(target,'l3') not in eligible):
            continue
        result[target] = {'text':row['sanskrit'],'source_file':row.get('source_file',''),
            'source_license':row.get('source_license',''),'source_origin':row.get('source_origin',''),
            'source_lines':(row.get('links') or {}).get('source_lines'),
            'note':'Site source display; check the cited edition and full source coverage.'}
    # Some site files are passage-shaped. Restrict reconstruction to source
    # mappings audited in this repo or byte-pinned intake manifests; other
    # legacy mappings need a source audit before they become model evidence.
    try:
        import workcfg
        if work not in ('paramarthasara','kramastotra') and not (ROOT / work / 'source/manifest.json').is_file():
            return result
        cfg=workcfg.work_config(work)
        spans=workcfg.source_spans(work) if cfg else None
        source=Path(cfg['source']) if cfg else None
        if spans is not None and source and source.is_file():
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            try: name=str(source.relative_to(ROOT.parent))
            except ValueError: name=source.name
            for target,row in originals.get('t1',{}).items():
                tokens=spans.get(row.get('verse'))
                if target not in result and tokens:
                    result[target]={'text':' '.join(tokens),'source_file':name,'source_sha256':digest,
                        'source_lines':row.get('source_lines'),
                        'note':'Parser-reconstructed tokens; consult the edition for exact typography.'}
    except (OSError,ValueError,KeyError,TypeError):
        pass
    return result

def build(work: str) -> dict:
    # layer originals for every verse/song target in the work's canonical data
    originals: dict = {layer: {} for layer in sch.LAYERS}
    songs = sorted({p.name[:-(len(layer) + 6)]
                    for layer in sch.LEGACY_STACK_LAYERS
                    for p in (ROOT / work / "data").glob(f"*.{layer}.json")})
    if not songs:
        raise SystemExit(f"{work}: no canonical layer data")
    reviews = sch.jsonl_read(sch.rpath(work))
    eligible = set()
    c2_eligible = set()
    for song in songs:
        proof_path = ROOT / work / "proof" / f"proof-{song}.json"
        if not proof_path.exists():
            continue
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
        if (proof.get("work") != work or proof.get("song") != song or
            proof.get("deterministic_gate") != "PASS"):
            continue
        # A legacy work without an intake manifest still needs a fresh proof.
        # Never project a PASS recorded for different or incomplete layer data.
        recorded = proof.get("layer_sha256", {})
        current = {}
        for layer in sch.LAYERS:
            path = ROOT / work / "data" / f"{song}.{layer}.json"
            if path.exists():
                current[layer] = sch.sha(json.loads(path.read_text(encoding="utf-8")))
        if not {"t1", "l0", "argmap", "l2", "c1"}.issubset(current) or recorded != current:
            continue
        eligible.add(song)
        signoff = sch.load_signoff(work, song)
        if signoff:
            current_hash, _ = sch.stack_sha(work, song)
            if any(r.get("review_target", {}).get("object_ref") == f"original:{work}:{song}"
                   and r.get("review_target", {}).get("hash") == current_hash
                   and r.get("decision") in ("ACCEPT", "ACCEPT_WITH_QUALIFICATION")
                   for r in reviews):
                c2_eligible.add(song)
    if work in SOURCE_COVERAGE_HOLDS:
        eligible.clear()
        c2_eligible.clear()
    for layer in sch.LAYERS:
        for song in songs:
            if song not in eligible or (layer == "c2" and song not in c2_eligible):
                continue
            f = ROOT / work / "data" / f"{song}.{layer}.json"
            if not f.exists():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            if layer in sch.layer_registry.SONG_LAYERS:
                originals[layer][song] = d
                continue
            for row in d:
                tid = row.get("verse_id")
                if tid:
                    if layer == "l0":
                        originals[layer].setdefault(tid, []).append(row)
                    else:
                        originals[layer][tid] = row

    versions = []
    for version in sch.load_versions(work):
        song = sch.song_of(version["target"], version["layer"])
        if song in eligible and (version["layer"] != "c2" or song in c2_eligible):
            versions.append(version)
    version_ids = {version["version_id"] for version in versions}
    def visible_target(reference):
        if reference in version_ids:
            return True
        return any(reference == f"original:{work}:{song}" for song in eligible)
    reviews = [review for review in reviews
               if visible_target(review.get("review_target", {}).get("object_ref"))]
    review_ids = {review["review_id"] for review in reviews}
    promotions = [promotion for promotion in sch.jsonl_read(sch.ppath(work))
                  if visible_target(promotion.get("object_ref"))
                  and all(review in review_ids for review in promotion.get("basis", []))]
    signoffs = []
    stack_hashes = {}
    for song in songs:
        if song not in eligible:
            continue
        cur, _ = sch.stack_sha(work, song)
        stack_hashes[song] = cur
        so = sch.load_signoff(work, song)
        if so:
            so = dict(so)
            # back the signoff with its review id (the live binding)
            rv = [r for r in reviews if r.get("review_target", {}).get("object_ref")
                  == f"original:{work}:{song}"]
            so["review_id"] = rv[-1]["review_id"] if rv else ""
            so["stack_sha"] = rv[-1].get("review_target", {}).get("hash", "") if rv else ""
            so["current_stack_sha"] = cur
            so["review_current"] = bool(rv and so["stack_sha"] == cur)
            signoffs.append(so)

    # the Sanskrit original's edition (WORK ID on the hub) from passages.jsonl
    src_ed = ""
    for pf in sorted((ROOT / work).glob("passages.jsonl")):
        for line in pf.read_text(encoding="utf-8").splitlines():
            if line.strip():
                src_ed = json.loads(line).get("source_edition", "") or src_ed
                if src_ed:
                    break
        if src_ed:
            break

    contract = agent_contract.describe()
    essays=[]
    for path in sorted((ROOT/work/'scholar/essays').glob('*.json')):
        try:
            essay=json.loads(path.read_text(encoding='utf-8'))
            if not sch.essay_errors(essay,work,path.name) and (not essay.get('target') or essay['target'] in originals.get('t1',{})):
                essays.append(essay)
        except (OSError,ValueError,TypeError):
            continue
    times = [item.get("created_at", "") for item in versions + reviews]
    last_event = max((time for time in times if time), default=None)
    doc = {
        "work": work,
        "generated": last_event,
        "source": "translation-work canonical data + scholar/ ledgers (emit_scholar.py)",
        "source_edition": src_ed,
        "contract": {
            "contract_version": contract["contract_version"],
            "contract_sha256": agent_contract.content_hash(contract),
            "schema_version": contract["schema_version"],
            "structural_schema_version": contract["structural_schema_version"],
            "structural_schema_snapshot_sha256": contract["structural_schema_snapshot_sha256"],
            "order": contract["order"],
            "schemas": {item["id"]: item["schema"] for item in contract["layers"]},
            "layers": [{"id": item["id"], "scope": item["scope"],
                        "depends_on": item["depends_on"], "validator": item["validator"],
                        "validator_sha256": item["validator_sha256"],
                        "example": {key: value for key, value in item["example"].items()
                                    if key != "content"}} for item in contract["layers"]],
        },
        "rights": {
            "translation": "FREE — our English (L1–L4, commentary) is free use",
            "scholar": "Contributors declare rights; authorship and copyright depend on the work and law.",
        },
        "originals": originals,
        "source_verses": displayed_sources(work, eligible, originals),
        "l4_craft": song_craft(work, originals),
        "withheld_songs": sorted(set(songs) - eligible),
        "original_hashes": {layer: {target: sch.sha(content) for target, content in rows.items()}
                            for layer, rows in originals.items()},
        "versions": versions,
        "essays": essays,
        "reviews": reviews,
        "promotions": promotions,
        "signoffs": signoffs,
        "stack_hashes": stack_hashes,
    }
    if work in SOURCE_COVERAGE_HOLDS:
        doc['withheld_reason'] = SOURCE_COVERAGE_HOLDS[work]
    try:
        from pathlib import Path as _P
        _rec = _P(__file__).resolve().parent.parent / work / 'source' / 'record.json'
        _om = _P(__file__).resolve().parent.parent / 'source-maps' / 'openpatala.json'
        if _rec.is_file():
            _r = json.loads(_rec.read_text(encoding='utf-8'))
            _o = {}
            try:
                _o = json.loads(_om.read_text(encoding='utf-8')).get('works', {}).get(work, {})
            except (OSError, ValueError):
                pass
            if _r.get('status') == 'RECORDED':
                doc['source_ref'] = {
                    'record_sha256': sch.sha(_r),
                    'mapping_status': _o.get('mapping_status', 'UNMAPPED'),
                    'note': 'uniform source record + openpatala mapping; edition candidate, witness UNKNOWN',
                }
    except (OSError, ValueError):
        pass
    doc["projection_sha256"] = sch.sha(doc)
    return doc

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="paramarthasara")
    ap.add_argument('--all',action='store_true',help='emit every work with canonical T1 data')
    ap.add_argument("--out", default=str(SVREAD / "data" / "scholar"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    # index of all emitted works (small, for the hub's work list)
    idx_path = out / "index.json"
    # A full rebuild depends only on the current work set, not on any previous
    # index. A single-work update preserves the other indexed works.
    # Registered-but-untranslatable projections (e.g. ipvv: withheld until
    # gold-lane proofs) have no canonical T1 rows, so --all would drop them.
    # Carry forward any on-disk projection that still hash-verifies instead.
    idx = {} if a.all else (json.loads(idx_path.read_text(encoding='utf-8')) if idx_path.exists() else {})
    works=sorted({p.parent.parent.name for p in ROOT.glob('*/data/*.t1.json')}) if a.all else [a.work]
    for work in works:
        doc=build(work);p=out/f'{work}.json'
        p.write_text(json.dumps(doc,ensure_ascii=False,indent=1),encoding='utf-8')
        idx[work]={'title':work,'versions':len(doc['versions']),'reviews':len(doc['reviews']),
                   'signoffs':len(doc['signoffs']),'generated':doc['generated']}
        print(f"emitted {p} ({p.stat().st_size//1024} KB) — {len(doc['versions'])} versions, "
              f"{len(doc['reviews'])} reviews, {len(doc['signoffs'])} signoffs, originals: " +
              ', '.join(f'{layer}:{len(rows)}' for layer,rows in doc['originals'].items() if rows))
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    if a.all:
        for extra in sorted(out.glob('*.json')):
            if extra.name == 'index.json' or extra.stem in works:
                continue
            try:
                doc = json.loads(extra.read_text(encoding='utf-8'))
            except ValueError:
                continue
            body = {k: v for k, v in doc.items() if k != 'projection_sha256'}
            if doc.get('work') != extra.stem or sch.sha(body) != doc.get('projection_sha256'):
                print(f"NOT carried forward: {extra.name} (hash mismatch — needs re-emit)")
                continue
            idx[extra.stem] = {'title': extra.stem, 'versions': len(doc.get('versions', [])),
                               'reviews': len(doc.get('reviews', [])),
                               'signoffs': len(doc.get('signoffs', [])),
                               'generated': doc.get('generated')}
            print(f"carried forward: {extra.name} (registered, untranslatable yet)")
        idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())
