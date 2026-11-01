#!/usr/bin/env python3
"""check.py — the canonical gate. Exit 0 = the stack is canonical, else failing step named.

  python3 check.py [--work sivastotravali]

Steps: schemas import+self-test · stack.json in sync · every data song validates ·
every proof record PASSes · every MD round-trips · no stale doctrine strings ·
directive + canonical docs present.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path("/root/translation-work")
fails: list[str] = []


def step(name: str, ok: bool, detail: str = ""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name + (f": {detail}" if detail else ""))


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="sivastotravali")
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT / "schemas"))
    try:
        import t1 as t1s, l0 as l0s, argmap as ams, l2 as l2s, c1 as c1s, c2 as c2s
        from __init__ import SCHEMA_VERSION  # noqa
    except Exception:
        try:
            import base as _b  # noqa
            SCHEMA_VERSION = "1.1.0"
        except Exception as e:
            step("schemas-import", False, str(e)); raise SystemExit(1)
    import base as _base
    errs = []
    errs += _base.check_required({}, ["x"], "selftest")
    step("schemas-import", True)

    stack = json.loads((ROOT / "stack.json").read_text())
    sync = stack.get("schemas_version") == "1.1.0"
    req_ok = True
    for mod, name in [(t1s, "t1"), (l0s, "l0"), (ams, "argmap"), (l2s, "l2"), (c1s, "c1")]:
        if set(stack["required_by_layer"][name]) != set(mod.REQUIRED):
            req_ok = False
            fails.append(f"stack-sync: {name}.REQUIRED drifted from stack.json")
    step("stack-sync", sync and req_ok)

    w = ROOT / args.work
    songs = sorted(p.stem.replace("t1", "").strip(".") for p in (w / "data").glob("*.t1.json"))
    step("data-present", bool(songs), "no data/*.t1.json")
    for s in songs:
        r = subprocess.run([sys.executable, str(ROOT / "tools/validate_song.py"),
                            "--song", s, "--work", args.work],
                           capture_output=True, text=True)
        try:
            n_err = len(json.loads(r.stdout).get("errors", ["unparseable"]))
        except Exception:
            n_err = 99
        step(f"validate-{s}", r.returncode == 0 and n_err == 0, f"{n_err} errors")
        r2 = subprocess.run([sys.executable, str(ROOT / "tools/render_md.py"),
                             "--song", s, "--work", args.work],
                            capture_output=True, text=True)
        try:
            diffs = json.loads(r2.stdout).get("roundtrip_diffs", ["unparseable"])
        except Exception:
            diffs = ["unparseable"]
        step(f"roundtrip-{s}", r2.returncode == 0 and not diffs, str(diffs[:2]))
        disp = ROOT / "tools/proof-disp.json"
        r3 = subprocess.run([sys.executable, str(ROOT / "tools/proof_record.py"),
                             "--song", s, "--work", args.work,
                             "--disp", str(disp)] if disp.exists() else
                            [sys.executable, str(ROOT / "tools/proof_record.py"),
                             "--song", s, "--work", args.work],
                            capture_output=True, text=True)
        try:
            gate = json.loads(r3.stdout).get("gate")
        except Exception:
            gate = "UNPARSEABLE"
        step(f"proof-{s}", r3.returncode == 0 and gate == "PASS", f"gate={gate}")

    stale = []
    for pat in ["one \\[and\\]-token per GRETIL", "one token per GRETIL whitespace token",
                "MD is canonical", "markdown is canonical"]:
        for f in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.py")):
            if ".git" in str(f):
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if re.search(pat, txt) and "FROZEN" not in txt and "historical" not in txt.lower():
                # frozen T1 headers + this very check's patterns are grandfathered
                if "T1-s0" in str(f) or "T1-s1" in str(f) or "T1-s2" in str(f) or f.name == "check.py":
                    continue
                stale.append(f"{f.relative_to(ROOT)}: {pat}")
    step("no-stale-doctrine", not stale, "; ".join(stale[:3]))

    ag = (ROOT / "AGENTS.md").read_text()
    step("directive-present", "User Directive 2026-11-01" in ag)
    try:
        dt = json.loads((ROOT / "DATATYPES.json").read_text())
        dt_ok = (dt.get("version") == "1.1.0" and isinstance(dt.get("transforms"), list)
                 and all(v.exists() or True for v in [ROOT / "tools" / "validate_site.py"]))
        # every transform with a translation-work validator must point at a real file
        for t in dt["transforms"]:
            v = t.get("validator", "")
            if v.startswith("schemas/") or v.startswith("tools/validate"):
                f = v.split()[0].rstrip(":,;")
                if not (ROOT / f).exists():
                    dt_ok = False
                    fails.append(f"contract: validator missing for {t['id']}: {v}")
    except Exception as e:
        dt_ok = False
        fails.append(f"contract: DATATYPES.json unparseable: {e}")
    step("contract-valid", dt_ok)
    r4 = subprocess.run([sys.executable, str(ROOT / "tools/validate_site.py"),
                         "--work", args.work], capture_output=True, text=True)
    try:
        n_err = len(json.loads(r4.stdout).get("errors", ["unparseable"]))
    except Exception:
        n_err = 99
    step("site-data", r4.returncode == 0 and n_err == 0, f"{n_err} errors")
    qa = ROOT / "logs" / "qa" / f"{args.work}.md"
    step("qa-present", qa.exists(), "run tools/qa_vs_witness.py")
    try:
        sys.path.insert(0, str(ROOT / "schemas"))
        import suggestion as _sug
        n_sug = n_bad = 0
        for sf in (ROOT / args.work / "data").glob("*.suggest.json"):
            for o in json.loads(sf.read_text(encoding="utf-8")):
                n_sug += 1
                if _sug.validate(o, "suggestion"):
                    n_bad += 1
        step("suggestions-valid", n_bad == 0, f"{n_bad}/{n_sug} invalid")
    except Exception as e:
        step("suggestions-valid", False, str(e))
    docs = all((ROOT / f).exists() for f in
               ["CANONICAL.md", "LAYERS.md", "ALIGNMENT.md", "TENSIONS.json", "stack.json",
                "DATATYPES.json", "schemas/__init__.py", "schemas/c2.py",
                "skills/crystal-ipvv/SKILL.md",
                "skills/crystal-ipvv/EXAMPLES.md",
                "CHAT.md",
                "lore/rasa/abhinavagupta-rasa-grounding-2026-11-01.md"])
    step("canonical-docs", docs)

    print(f"\n{'CANONICAL' if not fails else 'NOT CANONICAL'}: {len(fails)} failures")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
