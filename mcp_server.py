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
def swarm_seed(work: str, song: str, group: int = 24) -> dict:
    """Seed swarmable triple tasks (gloss+CM+argmap+L2 per verse-group) for a
    song. Writes queue.json ONLY. Requires a lore brief (see lore tool) —
    unbriefed seeds degenerate (mistakes #21). 24 verses/group default;
    auto-halves on output ceiling."""
    if _lore_path(work) is None and work.startswith("tantraloka-a"):
        return {"seeded": 0, "warning": "no transmission brief for this front — write lore first"}
    sys.path.insert(0, str(ROOT / "tools"))
    import tal_stage
    wt = tal_stage.stage_parse(work, song)
    before = len(tal_stage.load_q())
    tal_stage.stage_seed_triple(work, song, group=group)
    after = len(tal_stage.load_q())
    return {"seeded": after - before, "verses": len(wt), "group": group}


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
    drafts = {}
    for sub in ("gloss", "cm", "am", "brief"):
        for cand in runs.glob(f"{task_id}*/{sub}.json"):
            try:
                drafts[cand.parent.name + "/" + sub] = json.loads(cand.read_text())
            except ValueError:
                pass
        for cand in runs.glob(f"{task_id}/{sub}.json"):
            try:
                drafts[sub] = json.loads(cand.read_text())
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
    return {"promoted": True, "gate": gate, "proof": p,
            "note": "machine-proposed, needs human review. No push performed."}


TOOLS = ["status", "validate", "lore", "swarm_status",
         "swarm_seed", "swarm_review", "swarm_decide", "promote"]


if __name__ == "__main__":
    if "--serve" in sys.argv:
        mcp.run(transport="stdio")
    elif "--list" in sys.argv or len(sys.argv) == 1:
        print("shastra MCP — translation-work tools\n")
        for name in TOOLS:
            fn = mcp.get_tool(name)
            print(f"  shastra.{name}: {(fn.description or '').splitlines()[0] if fn.description else ''}")
    else:
        tool = sys.argv[1].removeprefix("shastra.")
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        print(json.dumps(mcp.call_tool(tool, args), indent=2, default=str))
