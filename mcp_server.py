#!/usr/bin/env python3
"""shastra MCP server — translation-work as callable tools (FastMCP, stdio).

Two lanes, one gate:
  SMALL (crystal-ipvv): one verse/work end-to-end by hand — status, validate,
    lore, concept lookup. The agent IS the assessor; the server never authors.
  LARGE (largetext swarm): beam drafters (DUMB) + assessor (SMART) + scripts.
    Seed -> review -> decide -> promote. Beam NEVER writes data/, NEVER marks
    PASS. Promotion is an assessor act and always machine-proposed.

Usage:
  python3 mcp_server.py --serve        # MCP stdio for Muse/ChatGPT/pi
  python3 mcp_server.py --list         # list tools
  python3 mcp_server.py <tool> '<json-args>'   # CLI call (testing)

No pushes, no signoffs, no PASS minting. Ever.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))

from fastmcp import FastMCP

mcp = FastMCP("shastra")


def _run(cmd: list[str], timeout: int = 300) -> dict:
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT,
                       capture_output=True, text=True, timeout=timeout)
    try:
        data = json.loads(r.stdout) if r.stdout.strip() else {}
    except ValueError:
        data = {"raw": r.stdout[-2000:], "stderr": r.stderr[-2000:]}
    data["_rc"] = r.returncode
    return data


def _registry() -> dict:
    return json.loads((ROOT / "REGISTRY.json").read_text())


def _lore_path(work: str) -> Path | None:
    """Transmission brief for a work's front (tal-aNN.md convention)."""
    ahn = work.split("tantraloka-a")[-1] if work.startswith("tantraloka-a") else ""
    if ahn:
        p = ROOT / "process" / "beam" / "lore" / f"tal-a{ahn}.md"
        if p.exists():
            return p
    return None


@mcp.tool()
def status(work: str, song: str = "") -> dict:
    """SMALL+LARGE entry point: work state — REGISTRY row, STATUS.json, data
    counts, proof gate, lore-brief presence, and size routing
    (<1k source tokens: assessor writes directly; >1k: seed the swarm)."""
    reg = _registry()
    row = next((w for w in reg["works"] if w["work"] == work), None)
    out: dict = {"registry": row}
    sp = ROOT / work / "STATUS.json"
    if sp.exists():
        out["STATUS"] = json.loads(sp.read_text())
    if song:
        dd = ROOT / work / "data"
        counts = {}
        for suf in ("t1", "l0", "argmap", "l2", "l3", "l4", "c1"):
            f = dd / f"{song}.{suf}.json"
            if f.exists():
                try:
                    d = json.loads(f.read_text())
                    counts[suf] = len(d) if isinstance(d, list) else len(d.get("essence", [])) if suf == "c1" else 1
                except ValueError:
                    counts[suf] = "unparseable"
        out["data_counts"] = counts
        pf = dd.parent / "proof" / f"proof-{song}.json"
        alt = ROOT / work / "proof" / f"proof-{song}.json"
        for cand in (pf, alt):
            if cand.exists():
                try:
                    out["proof"] = json.loads(cand.read_text())
                except ValueError:
                    pass
    brief = _lore_path(work)
    out["lore_brief"] = str(brief.relative_to(ROOT)) if brief else None
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import workcfg
        spans = workcfg.source_spans(work)
        if spans:
            toks = sum(len(t) for t in spans.values())
            out["source_tokens"] = toks
            out["routing"] = "assessor-direct (<1k)" if toks < 1000 else "swarm-first (>1k, windowed briefs + triple)"
    except Exception as e:
        out["routing"] = f"unknown ({e})"
    return out


@mcp.tool()
def validate(work: str, song: str) -> dict:
    """Run the deterministic gates: validate_song (schemas + cross-layer
    invariants) + proof_record --shastra. Read-only report; fixes nothing.
    Exit nonzero in the payload when errors exist."""
    v = _run(["tools/validate_song.py", "--song", song, "--work", work])
    p = _run(["tools/proof_record.py", "--song", song, "--work", work, "--shastra"])
    return {"validate": v, "proof": p}


@mcp.tool()
def lore(work: str) -> dict:
    """Return the cached 1-page transmission brief for a front
    (what it IS / MOVES / TRAPS / APPROACH), or list available briefs when
    none exists — write it first (web scholarship), then queue tasks."""
    b = _lore_path(work)
    if b:
        return {"brief": b.name, "text": b.read_text()[:8000]}
    have = sorted(p.name for p in (ROOT / "process" / "beam" / "lore").glob("tal-*.md"))
    return {"brief": None, "available": have,
            "note": "no brief for this front: 10 min of scholarship now saves hours of bounce cycles"}


@mcp.tool()
def swarm_status() -> dict:
    """Queue at a glance: pending/claimed/done/failed by kind + worker
    liveness. Read-only."""
    import datetime
    q = json.loads((ROOT / "process" / "beam" / "queue.json").read_text())
    by: dict[str, dict[str, int]] = {}
    for t in q:
        by.setdefault(t["kind"], {}).setdefault(t["status"], 0)
        by[t["kind"]][t["status"]] += 1
    import subprocess as _sp
    ps = _sp.run(["ps", "-eo", "cmd"], capture_output=True, text=True).stdout
    workers = sum(1 for ln in ps.splitlines() if "beam_swarm.py worker" in ln)
    return {"queue_by_kind": by, "workers_alive": workers,
            "total": len(q), "note": "workers exit when empty — relaunch per batch"}


@mcp.tool()
def swarm_seed(work: str, song: str, group: int = 24, token_budget: int = 0) -> dict:
    """Seed swarmable triple tasks (gloss+CM+argmap+L2 per verse-group) for a
    song. Writes queue.json ONLY. Requires a lore brief (see lore tool) —
    unbriefed seeds degenerate (mistakes #21). 24 verses/group default;
    auto-halves on output ceiling. token_budget>0 packs by source tokens
    instead (prose-heavy units: 24-verse windows blow output; ~250 works)."""
    if _lore_path(work) is None and work.startswith("tantraloka-a"):
        return {"seeded": 0, "warning": "no transmission brief for this front — write lore first"}
    sys.path.insert(0, str(ROOT / "tools"))
    import tal_stage
    import subprocess as _sp
    _chk = _sp.run([sys.executable, "tools/check_front.py",
                    "--work", work, "--song", song],
                   capture_output=True, text=True, cwd=str(ROOT))
    _warnings = [ln for ln in _chk.stdout.splitlines() if ln.startswith("WARN:")]
    if _chk.returncode not in (0,):
        return {"seeded": 0, "blocked": True,
                "detail": (_chk.stdout + _chk.stderr)[-800:]}
    if not token_budget and not work.startswith("tantraloka-a"):
        token_budget = 250  # prose-heavy non-TAL fronts: size by tokens
    wt = tal_stage.stage_parse(work, song)
    before = len(tal_stage.load_q())
    tal_stage.stage_seed_triple(work, song, group=group, token_budget=token_budget)
    after = len(tal_stage.load_q())
    out = {"seeded": after - before, "verses": len(wt), "group": group,
           "token_budget": token_budget}
    if _warnings:
        out["warnings"] = _warnings
    return out


@mcp.tool()
def swarm_review(task_id: str) -> dict:
    """Assessor review packet for one DONE task: draft + selfcheck + the
    meaning checklist (question sharp? premises terse? uncertainties honest?
    traces resolve?). Read-only — decide with swarm_decide."""
    import tal_stage  # noqa: F401 (ensures tool path)
    q = json.loads((ROOT / "process" / "beam" / "queue.json").read_text())
    t = next((x for x in q if x["id"] == task_id), None)
    if not t:
        return {"error": f"unknown task {task_id}"}
    runs = ROOT / "process" / "beam" / "runs"
    drafts: dict = {}
    args = t.get("args", {})
    song = args.get("song", "")
    verses = args.get("verses") or ([args["verse"]] if "verse" in args else [])
    for v in verses:
        for sub in ("gloss", "cm", "am"):
            cand = runs / f"{song}-{sub}-v{v:02d}" / f"{sub}.json"
            if cand.exists():
                try:
                    drafts[f"v{v:02d}/{sub}"] = json.loads(cand.read_text())
                except ValueError:
                    pass
    if not drafts:  # brief/pilot tasks keep single-file outputs
        for sub in ("brief", "gloss", "cm", "am"):
            for cand in list(runs.glob(f"{task_id}/{sub}.json")) + list(runs.glob(f"{task_id}*/{sub}.json")):
                try:
                    drafts[cand.parent.name + "/" + sub] = json.loads(cand.read_text())
                except ValueError:
                    pass
    checklist = [
        "question is the verse's own (not meta: no 'what argument does this passage make')",
        "premises terse logical steps (compress ~19->~8 for passages), no paraphrase-as-argument",
        "uncertainties honest and specific (no smoothing, no invented certainty)",
        "no fork adjudication, no witness cites, no PASS language (bounce if present)",
        "traces: surfaces byte-exact vs working-t1, rows cover every token",
    ]
    return {"task": t, "drafts": drafts, "checklist": checklist}


@mcp.tool()
def swarm_decide(task_id: str, verdict: str, note: str = "") -> dict:
    """Approve or bounce a reviewed task. Bounce notes must be ACTIONABLE
    (span format, missing verses, flabby question, paraphrase-not-argument).
    Max 3 attempts, then escalate to assessor hand-draft. Writes queue only —
    never data/, never PASS."""
    if verdict not in ("approve", "bounce"):
        return {"error": "verdict must be approve|bounce"}
    if verdict == "bounce" and len(note.strip()) < 10:
        return {"error": "bounce notes must be actionable (>=10 chars): name the fix"}
    sys.path.insert(0, str(ROOT / "tools"))
    from beam_swarm import load_q, save_q
    q = load_q()
    t = next((x for x in q if x["id"] == task_id), None)
    if not t:
        return {"error": f"unknown task {task_id}"}
    if verdict == "approve":
        if t["kind"] not in ("tal_brief", "pilot_pair", "lore_distill"):
            return {"error": f"kind {t['kind']} is not approvable here (triple assembles via promote)"}
        t["status"] = "approved"
        t["note"] = (t.get("note", "") + " | assessor approved via MCP").strip(" |")
    else:
        if t["attempts"] >= t.get("max_attempts", 3):
            t["status"] = "failed"
            t["note"] = f"escalated to assessor hand-draft after {t['attempts']} attempts: {note}"
        else:
            t["status"] = "pending"
            t["note"] = f"bounce: {note}"
    import datetime
    t["updated"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_q(q)
    return {"task": t["id"], "status": t["status"], "note": t["note"]}


@mcp.tool()
def promote(work: str, song: str) -> dict:
    """Assessor promotion: assemble runs -> working files -> data/*.json ->
    validate_song + proof_record. Records STATUS/REGISTRY as machine-proposed
    (minimal: L3/L4 waived). REFUSES on gate failure. Never pushes, never
    signs off, never marks final."""
    v = _run(["tools/validate_song.py", "--song", song, "--work", work])
    if v["_rc"] != 0:
        return {"promoted": False, "reason": "validate_song has errors — fix first", "validate": v}
    p = _run(["tools/proof_record.py", "--song", song, "--work", work, "--shastra"])
    gate = p.get("gate")
    if gate != "PASS":
        return {"promoted": False, "reason": f"proof gate={gate} — BLOCKED needs recorded disposition",
                "proof": p}
    sp = ROOT / work / "STATUS.json"
    st = json.loads(sp.read_text()) if sp.exists() else {"work": work}
    st.update({"next": "minimal gold complete; L3/L4 waived; human review pending"})
    st.setdefault("counts", {})["proof"] = "PASS"
    import datetime
    st["updated"] = datetime.datetime.now().date().isoformat()
    sp.write_text(json.dumps(st, indent=1, ensure_ascii=False))
    rp = ROOT / "REGISTRY.json"
    reg = json.loads(rp.read_text())
    n = v.get("validate", {}).get("counts", {}).get("t1", 0)
    for w in reg["works"]:
        if w["work"] == work:
            w.update({"status": "gold (machine-proposed, minimal: L3/L4 waived)",
                      "gold": True, "verses": n or w.get("verses"),
                      "note": "minimal gold via swarm: T1/L0/argmap/L2/C1-essence, proof PASS; L3/L4 waived."})
    reg["gold"] = sum(1 for w in reg["works"] if w.get("gold"))
    reg["pending"] = sum(1 for w in reg["works"] if not w.get("gold"))
    reg["total_works"] = len(reg["works"])
    rp.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    _run([str(ROOT / "tools" / "manifest.py"), "gen"], timeout=300)
    return {"promoted": True, "gate": gate, "proof": p,
            "note": "machine-proposed, needs human review. STATUS+REGISTRY updated. No push performed."}


@mcp.tool()
def skill(name: str) -> dict:
    """Return the governing SKILL.md for a lane (the law the swarm obeys).
    name: crystal-ipvv (single-verse gold drill, the ONLY path to gold) or
    largetext (swarm scaffolding: beam drafters + assessor gate + transmission
    briefs + calibration). Read FIRST before any translation action."""
    key = name.strip().lower().replace("_", "-")
    mapping = {"crystal-ipvv": "skills/crystal-ipvv/SKILL.md",
               "crystal": "skills/crystal-ipvv/SKILL.md",
               "largetext": "skills/largetext/SKILL.md",
               "large": "skills/largetext/SKILL.md"}
    rel = mapping.get(key)
    if not rel:
        return {"error": f"unknown skill {name!r}: crystal-ipvv|largetext"}
    text = (ROOT / rel).read_text()
    ex = ROOT / rel.replace("SKILL.md", "EXAMPLES.md")
    out = {"skill": key, "text": text[:12000]}
    if ex.exists():
        out["examples"] = ex.read_text()[:12000]
    return out


@mcp.tool()
def concepts(term: str, top: int = 5) -> dict:
    """Grounds for hand-glossing: concept-database entry (if built) +
    frequency-ranked MITRA senses with attestations for a Sanskrit headword.
    Returns the `grounds + source` shape L0 options require. Read-only —
    unknown headwords return [], never invented."""
    g = _run(["tools/mitra_grounds.py", term, "--top", str(top)], timeout=60)
    c = _run(["tools/lookup_concept.py", term], timeout=60)
    return {"mitra_grounds": g, "concept_db": c}


@mcp.tool()
def recycle(dry_run: bool = False) -> dict:
    """Halve + requeue retryable failed triples (the failure recycler).
    Safe: one generation only (rc2- ids), skips covered ranges."""
    return _run(["--", "recycle_failed.py"] + (["--dry"] if dry_run else []))


@mcp.tool()
def watchdog() -> dict:
    """Alias of progress(): hourly health line with flags (for scheduled tasks)."""
    return _run(["--", "watchdog_progress.py"])


@mcp.tool()
def progress() -> dict:
    """One-shot system health + progress watchdog (queue counts, workers,
    failure classes, assembled songs, host load/mem/disk, flags). Safe to
    call hourly from a ChatGPT scheduled task."""
    return _run(["--", "watchdog_progress.py"])


@mcp.tool()
def queue_guard(fix: bool = False) -> dict:
    """Structural duplicate guard for the burn queue. Every seeding agent
    MUST run this (or the guarded seeder) before adding tasks: enforces
    unique ids and non-overlapping tal_triple verse ranges per song.
    fix=true marks overlapping pending/claimed rows 'superseded'."""
    return _run(["--", "queue_guard.py"] + (["--fix"] if fix else []))


@mcp.tool()
def gates() -> dict:
    """The one gate (SKILL largetext §10): manifest freshness + proof sweep
    + passages ledger + dbread coverage. Read-only report; exit nonzero in
    payload when unshippable."""
    return _run(["tools/validate_all.py", "--quick"], timeout=600)


@mcp.tool()
def recon(work: str) -> dict:
    """Recon report for a work (read-only): source spans + verse census,
    workcfg registration, legacy T1 presence, lore-brief presence, beam
    coverage per song. Start every new front here — never queue tasks blind."""
    out: dict = {"work": work}
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import workcfg
        cfg = workcfg.work_config(work)
        out["registered"] = cfg is not None
        if cfg is not None:
            out["kind"] = cfg.get("kind")
            out["songs"] = {s: len(workcfg.song_verses(work, s)) for s in cfg.get("songs", {})}
        spans = workcfg.source_spans(work)
        if spans:
            out["spans"] = len(spans)
            out["tokens"] = sum(len(t) for t in spans.values())
    except Exception as e:
        out["error"] = str(e)[:300]
    brief = _lore_path(work)
    out["lore_brief"] = str(brief.relative_to(ROOT)) if brief else None
    dd = ROOT / work / "data"
    cov = {}
    if dd.exists():
        from pathlib import Path as _P
        for f in sorted(dd.glob("*.t1.json")):
            try:
                cov[f.name] = len(json.loads(f.read_text()))
            except ValueError:
                cov[f.name] = "unparseable"
    out["data_t1"] = cov
    legacy = list((ROOT / work).glob("T1*.md"))
    out["legacy_T1"] = [p.name for p in legacy][:10]
    return out


@mcp.tool()
def assemble(work: str, song: str) -> dict:
    """Assessor act: assemble beam runs -> working-T1/L0 + data t1/l0/argmap/
    l2 (+C1-essence skeleton) -> validate_song + proof_record. Writes working
    + data files as machine-proposed. Requires complete runs; use swarm_seed
    + workers first. Promote with `promote` after this passes."""
    return _run(["tools/tal_stage.py", "--work", work, "--song", song], timeout=600)


@mcp.tool()
def supervise(start_missing: bool = False) -> dict:
    """Report the autonomous loop. On this box systemd unit `tal-campaign`
    (Restart=always) -> watchdog.sh is the ONE supervisor: it health-gates
    (429 pause), starts the tal driver once (flock), and brings workers up
    staggered 1->2->3 (cap 3). With start_missing=true this (re)starts the
    systemd unit if it is inactive — it never spawns continue.sh/ralph.sh by
    hand (that creates duplicate supervisors), never pushes."""
    import subprocess as _sp
    want = {"continue.sh": "tools/continue.sh", "ralph.sh": "tools/ralph.sh",
            "watchdog.sh": "tools/watchdog.sh", "tal_run_all.sh": "tools/tal_run_all.sh",
            "tal_stage.py": "tools/tal_stage.py"}
    ps = _sp.run(["ps", "-eo", "cmd"], capture_output=True, text=True).stdout
    state = {}
    for name in want:
        state[name] = sum(1 for ln in ps.splitlines() if name in ln and "grep" not in ln)
    workers = sum(1 for ln in ps.splitlines() if "beam_swarm.py worker" in ln)
    state["beam_workers"] = workers
    # systemd unit state (the canonical supervisor here)
    unit = "tal-campaign"
    unit_active = None
    try:
        unit_active = _sp.run(["systemctl", "is-active", unit],
                              capture_output=True, text=True).returncode == 0
    except Exception:
        unit_active = None
    state["systemd_unit"] = unit_active
    started = []
    if start_missing:
        if unit_active is False:
            r = _sp.run(["systemctl", "start", unit], capture_output=True, text=True)
            started.append(f"systemd:{unit}" if r.returncode == 0
                            else f"systemd:{unit}:FAILED {r.stderr[:120]}")
        elif unit_active is None:
            # no systemd unit — fall back to one watchdog (never both)
            import os as _os
            if state["watchdog.sh"] == 0 and state["continue.sh"] == 0:
                env = dict(_os.environ)
                try:
                    kv = _sp.run(["agent-vault", "vault", "credential", "get",
                                  "OPENCODE_GO_KEY", "--vault", "oracle"],
                                 capture_output=True, text=True, timeout=30)
                    if kv.returncode == 0 and kv.stdout.strip():
                        env["OPENCODE_GO_KEY"] = kv.stdout.strip()
                except Exception:
                    pass
                _sp.Popen(["setsid", "nohup", "bash", "tools/watchdog.sh"],
                          stdout=open(ROOT / "process/beam/watchdog.log", "ab"),
                          stderr=_sp.STDOUT, stdin=_sp.DEVNULL, env=env,
                          cwd=str(ROOT))
                started.append("watchdog.sh(fallback)")
    return {"supervisors": state, "started": started,
            "policy": "systemd tal-campaign owns the loop (unit runs harness.sh); "
                      "harness health-gates (PAUSE 30m on 429), ensures "
                      "continue/watchdog/LOOP, staggers workers w1->w2->w3 (cap 3). Do not "
                      "start continue.sh/ralph.sh by hand alongside it.",
            "note": "single supervisor: harness.sh via systemd. tal_run_all driver starts "
                    "on healthy passes (flock singleton). 429 pauses are health-gated, not failures."}


@mcp.tool()
def swarm_workers(action: str = "status", target: str = "1") -> dict:
    """Beam-worker throttle (don't pound the free tier). Actions:
    status (live workers + what each holds); start (launch up to `target`
    free slots of w1..w5, staggered ~8s, health-gated: refuses while beam
    is down — start ONE, add more later); stop (kill slots named in
    `target`, e.g. 'w4,w5' — claims self-heal via 15-min stale expiry)."""
    return _workers(action, target)


def _workers(action: str, target: str = "1") -> dict:
    import subprocess as _sp, time as _t, os as _os
    def live() -> dict[str, int]:
        out = {}
        ps = _sp.run(["pgrep", "-f", "beam_swarm.py worker w"],
                     capture_output=True, text=True).stdout
        pids = [p for p in ps.split() if p.strip().isdigit()]
        for pid in pids:
            try:
                cmd = open(f"/proc/{pid}/cmdline", "rb").read().decode().replace("\x00", " ")
            except OSError:
                continue
            for w in ("w1", "w2", "w3", "w4", "w5"):
                if f"worker {w}" in cmd:
                    out[w] = int(pid)
        return out
    if action == "status":
        holding = {}
        try:
            q = json.loads((ROOT / "process" / "beam" / "queue.json").read_text())
            for t in q:
                if t.get("status") == "claimed":
                    holding[t.get("worker", "?")] = t["id"]
        except (OSError, ValueError):
            pass
        return {"workers": live(), "holding": holding}
    if action == "start":
        try:
            n = max(1, min(int(target), 5))
        except ValueError:
            return {"error": "start target must be a number 1..5"}
        # House policy: the systemd harness owns w1..w3 (cap 3). This tool
        # launches only canonical slots and never exceeds 3 live workers
        # total — starting w4/w5 by hand alongside the harness created
        # duplicate-supervisor churn. Need more? Change HARNESS_WORKERS.
        key = _os.environ.get("OPENCODE_GO_KEY", "")
        if not key:
            try:
                r = _sp.run(["agent-vault", "vault", "credential", "get",
                             "OPENCODE_GO_KEY", "--vault", "oracle"],
                            capture_output=True, text=True, timeout=30)
                if r.returncode == 0 and r.stdout.strip():
                    key = r.stdout.strip()
            except Exception:
                pass
        if not key:
            return {"started": [], "reason": "no OPENCODE_GO_KEY available"}
        _os.environ["OPENCODE_GO_KEY"] = key
        sys.path.insert(0, str(ROOT / "tools"))
        try:
            from beam_client import health
            ok, msg = health()
        except Exception as e:
            ok, msg = False, str(e)[:200]
        if not ok:
            return {"started": [], "reason": f"beam down, not starting: {msg}"}
        env = dict(_os.environ)
        alive = live()
        if len(alive) >= 3:
            return {"started": [], "reason": f"cap 3 reached ({sorted(alive)} live) — stop one first or let the harness manage"}
        started = []
        for w in ("w1", "w2", "w3"):
            if len(started) >= n or len(alive) + len(started) >= 3:
                break
            if w in alive:
                continue
            log = open(ROOT / f"process/beam/{w}.log", "ab")
            _sp.Popen(["setsid", "nohup", sys.executable, "-u",
                       "tools/beam_swarm.py", "worker", w],
                      stdout=log, stderr=_sp.STDOUT, stdin=_sp.DEVNULL,
                      env=env, cwd=str(ROOT), start_new_session=True)
            started.append(w)
            _t.sleep(8)
        return {"started": started, "note": "staggered ~8s; add more only if quota healthy"}
    if action == "stop":
        slots = [s.strip() for s in target.split(",") if s.strip() in ("w1", "w2", "w3", "w4", "w5")]
        alive = live()
        killed = []
        for s in slots:
            if s in alive:
                try:
                    _os.kill(alive[s], 15)
                    killed.append(s)
                except OSError:
                    pass
        return {"stopped": killed,
                "note": "claims self-heal via 15-min stale expiry"}
    return {"error": "action must be status|start|stop"}


@mcp.tool()
def review_sweep() -> dict:
    """Run the assessor daemon sweep: mechanical verdicts for new DONE
    triples (question/premise/uncertainty shape), escalate content-failures
    at max to the hand-draft backlog, seed lore_queries for unbriefed fronts.
    Never bounces, never approves prose, never writes data/. The loop's eyes
    while the model sleeps — meaning judgment stays queued for assessor."""
    return _run(["tools/assessor_sweep.py"], timeout=300)


@mcp.tool()
def beam_review(task_id: str = "", max_new: int = 1, apply: bool = False) -> dict:
    """SMART-beam reviewer over DUMB drafts (bounce-only, never approves).
    Reviews newest unreviewed DONE drafts against the shape+honesty checklist
    (max_new, default 1 — cheap on quota, instant backoff on 429). Bounces
    only mechanical fails with actionable notes when apply=true; meaning,
    forks, and PASS stay queued for the human assessor. task_id reviews one
    specific task instead of sweeping."""
    if task_id:
        return _run(["tools/beam_review.py", "--task", task_id] + (["--apply"] if apply else []), timeout=300)
    return _run(["tools/beam_review.py", "--sweep", "--max", str(max_new)] + (["--apply"] if apply else []), timeout=600)


@mcp.tool()
def bibliography(catalog: str = "", title: str = "", q: str = "") -> dict:
    """Final Muktabodha bibliography — THE base layer for translation priority
    (baseline 2026-11-12). Paths + per-work record (editions, has_translation,
    availability join). Args: catalog (M00031) OR title OR q (substring search).
    No args → paths() where the bibliography lives. Read-only."""
    if catalog or title:
        return _run(["tools/bibliography.py", "get",
                     "--catalog", catalog, "--title", title], timeout=60)
    if q:
        return _run(["tools/bibliography.py", "search", q, "--limit", "20"], timeout=60)
    return _run(["tools/bibliography.py", "paths"], timeout=30)


@mcp.tool()
def priority(limit: int = 20, untranslated_only: bool = True) -> dict:
    """Ranked translation order from the final bibliography base layer.
    Rule: untranslated first, shortest first within T; machine-complete and
    in-progress sink. T comes from burn_research/editions first (newest-first),
    then curated FAMOUS + local work_state. Returns top `limit` rows with
    burn_rank, catalog, title, verses, T, T_why, edition_count. Read-only —
    does not seed the swarm (use swarm_seed after picking a work)."""
    return _run(["tools/bibliography.py", "priority",
                 "--limit", str(limit)]
                + (["--untranslated-only"] if untranslated_only else []),
                timeout=60)


@mcp.tool()
def schema() -> dict:
    """Data structures for ALL bibliography surfaces (fields, types, values,
    paths) so any agent can query without reading files. Covers burn_flat,
    editions, links, research_matrix, availability_index, ranked_burn.
    Read-only. Companion: translation pipeline layers in DATATYPES.json."""
    return _run(["tools/bibliography.py", "schema"], timeout=60)


@mcp.tool()
def stats() -> dict:
    """Bibliography aggregate stats: 499 catalog rows, positives, editions,
    languages, availability coverage, link domains, ranked counts, top-5.
    Read-only orientation before browsing."""
    return _run(["tools/bibliography.py", "stats"], timeout=60)


@mcp.tool()
def works(has_translation: str = "", language: str = "", min_verses: int = 0,
          max_verses: int = 0, limit: int = 50, offset: int = 0) -> dict:
    """Browse/list works with filters (the list endpoint for agents).
    has_translation: "" (all) | "true" | "false". language: en|hi|fr|…
    Untranslated rows are shortest-first; translated rows by edition count.
    Returns catalog, title, author, verses, edition_count, languages,
    info_url, download_url. Paginated (limit/offset). Read-only."""
    cmd = ["tools/bibliography.py", "works",
           "--limit", str(limit), "--offset", str(offset),
           "--min-verses", str(min_verses), "--max-verses", str(max_verses)]
    if has_translation in ("true", "false"):
        cmd += ["--has-translation", has_translation]
    if language:
        cmd += ["--language", language]
    return _run(cmd, timeout=60)


@mcp.tool()
def editions(catalog: str = "", language: str = "", tier: str = "",
             downloadable_only: bool = False, limit: int = 50, offset: int = 0) -> dict:
    """Browse translation editions (the translation LINKS live here: translator,
    year, language, scope, publisher, access_tier, info_url, download_url,
    corroboration_url, confidence, verification_status, evidence). Filter by
    catalog / language / tier; downloadable_only=true for direct URLs.
    Paginated. Read-only."""
    cmd = ["tools/bibliography.py", "editions",
           "--limit", str(limit), "--offset", str(offset)]
    if catalog:
        cmd += ["--catalog", catalog]
    if language:
        cmd += ["--language", language]
    if tier:
        cmd += ["--tier", tier]
    if downloadable_only:
        cmd += ["--downloadable-only"]
    return _run(cmd, timeout=60)


@mcp.tool()
def links(catalog: str = "", domain: str = "", edition_related: str = "",
          limit: int = 50, offset: int = 0) -> dict:
    """Browse 718 bibliographic URL links (catalog ↔ URL relationships) with
    source roles (CANONICAL_INFO_URL | EDITION_INFO_URL | …), domain, whether
    edition-related, and evidence notes. NOT every link is a translation.
    edition_related: "" (all) | "true" | "false". Paginated. Read-only."""
    cmd = ["tools/bibliography.py", "links",
           "--limit", str(limit), "--offset", str(offset)]
    if catalog:
        cmd += ["--catalog", catalog]
    if domain:
        cmd += ["--domain", domain]
    if edition_related in ("true", "false"):
        cmd += ["--edition-related", edition_related]
    return _run(cmd, timeout=60)


@mcp.tool()
def availability(catalog: str = "", work: str = "", language: str = "",
                 coverage: str = "", missing: str = "",
                 limit: int = 50, offset: int = 0) -> dict:
    """Query the compiled translation-availability index (743 works; the API
    surface that openpatala serves). Filter by catalog / work / language /
    coverage (full|partial|none) / missing (true|false). Returns has_english,
    coverage, languages, translations[], english_urls, copyright_hint.
    Paginated. Read-only."""
    cmd = ["tools/bibliography.py", "availability",
           "--limit", str(limit), "--offset", str(offset)]
    for flag, val in (("--catalog", catalog), ("--work", work),
                      ("--language", language), ("--coverage", coverage)):
        if val:
            cmd += [flag, val]
    if missing in ("true", "false"):
        cmd += ["--missing", missing]
    return _run(cmd, timeout=60)


TOOLS = ["status", "validate", "lore", "swarm_status",
         "swarm_seed", "swarm_review", "swarm_decide", "promote",
         "skill", "concepts", "gates", "recon", "assemble", "supervise",
         "swarm_workers", "review_sweep", "beam_review",
         "bibliography", "priority", "schema", "stats", "works",
         "editions", "links", "availability"]


if __name__ == "__main__":
    import asyncio

    async def _list():
        print("shastra MCP — translation-work tools (full docs: MCP.md)\n")
        for name in TOOLS:
            fn = await mcp.get_tool(name)
            desc = (fn.description or "").splitlines()[0] if fn.description else ""
            print(f"  shastra.{name}: {desc}")

    if "--serve-http" in sys.argv:
        # HTTP (streamable) transport for remote MCP clients (ChatGPT connector)
        port = 8930
        for i, a in enumerate(sys.argv):
            if a == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
        mcp.run(transport="http", host="127.0.0.1", port=port, path="/mcp")
    elif "--serve" in sys.argv:
        mcp.run(transport="stdio")
    elif "--list" in sys.argv or len(sys.argv) == 1:
        asyncio.run(_list())
    else:
        tool = sys.argv[1].removeprefix("shastra.")
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

        async def _call():
            res = await mcp.call_tool(tool, args)
            if hasattr(res, "data") and res.data is not None:
                return res.data
            content = getattr(res, "content", None)
            if isinstance(content, (list, tuple)) and len(content) == 1 and hasattr(content[0], "text"):
                try:
                    return json.loads(content[0].text)
                except ValueError:
                    return content[0].text
            if isinstance(content, (list, tuple)):
                return [r.text if hasattr(r, "text") else str(r) for r in content]
            return str(res)

        print(json.dumps(asyncio.run(_call()), indent=2, default=str))
