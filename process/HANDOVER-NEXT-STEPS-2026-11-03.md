# HANDOVER — next steps (2026-11-03 evening, post-PR-integration)

*Read after HANDOVER-2026-11-03.md (L4 craft) and SCHOLAR.md. Session log:
SESSION-2026-11-03.md. Ownership map: ../AGENT-MAP.md.*

## 0. Integration state — the four draft PRs are DONE

Merged in the owner's order and fully released:

| PR | Repo | State | Verified how |
|---|---|---|---|
| #3 Scholar account hardening | ipvv | MERGED + **deployed** | live: email-only claim → 409 · signup 200 · bad login 401 · foreign-origin logout 403; `tests/scholar-auth.test.mjs` 3/3 |
| #1 versioned agent contracts + Scholar submissions | translation-work | MERGED | `check.py` CANONICAL: 0 · `pytest tests/` 18 passed |
| #2 verse source alignment + argument rebuild | ipvv | MERGED + released | kram/param argmaps rebuilt, questions now verse-specific; `tests/test_build_arguments.py` passed; **full release build → SITE GATES PASS** |
| #1 Scholar drafts → submissions | svread | MERGED + deployed | `tests/scholar-smoke.cjs` 0 fails |

Post-merge regeneration done: anubhavanivedana (L4 4/4), spandasandoha, paramarthasara,
kramastotra re-emitted with current emitters; 48 texts re-vendored into svread; ipvv built
(arguments 894 / receipts 2090 parity) + deployed; svread deployed (SW auto-bump each time).

Note: `node --test tests/` (dir mode) reports a failure while each file passes standalone —
reproduce/fix in the test todo; run files individually until then.

## 1. Open threads → next steps (priority order)

### A. Finish the integration (autonomous-safe)
1. **CLAIMS.md closures with evidence** (`ipvv/process/CLAIMS.md`, 6 open):
   - *grouped-L2 leak* — VERIFIED STALE (0 multi-verse PASS groups exist post-reshape). Close with evidence.
   - *kramastotra argmap template* — PR#2 rewrote packets (p07 question now verse-specific). Verify p07–p29 all distinct → close.
   - *kramastotra T1 mispairing* — verify p04/p06 gloss↔Sanskrit vs GRETIL; close or write the exact remaining pairs.
   - *work_id="tantrasara"* — **STILL REAL (32 files)** → fix `tools/ingest_batch.py` (derive work from batch key) + mechanical backfill, then close.
2. **Credential unification** (owner flagged): `tools/scholar_service.py` (submission service) vs `/api/auth/*` login use separate credentials — share the session (service verifies `svsess` HMAC instead of its own secret).
3. **All suites green, one command**: svread `node tests/scholar-smoke.cjs` ✓ · translation `pytest tests/` ✓ · ipvv `pytest tests/` ✓ + `node --test tests/` dir-mode bug (diagnose; files pass standalone).

### B. Owner-only gates (prepare, never execute)
4. **ORCID phase 2** — owner does Developer Tools step (redirect URI in `worker/AUTH-SETUP.md`), then build `/api/auth/orcid/start|callback` + profile autofill (`profiles.orcid` column exists).
5. **Zenodo token** (`.zenodo-env`) → `tools/publish_zenodo.py` (essays + translation releases → DOI → ORCID trusted-party sync).
6. **paramarthasara signoffs 2–12** (`scholar.py signoff --song param-p0X --by owner`) + one pushing probe session — the receipts' pushing gate honestly FAILs until pushing exists.

### C. Feature queue (safe lanes)
7. **Readiness matrix** — `tools/readiness.py`: per-work gaps (signoffs / pushing / C1 / L4 / receipts) as a burn-down table for all94 works.
8. **89 verify warnings** — mostly `works/tantraloka-aXX` DONE-with-0-PASS → STAGED vocabulary sweep.
9. **Qwen realtime** — protocol + model verified on disk (`voiceagent/docs/QWEN_OMNI.md`, `bridge.py` → `qwen3.8-omni-flash-realtime`); browser needs a **WS proxy in our worker** (auth header can't go browser-direct). Next build after chat polish.
10. **Browser→ledger write** (replace Export JSON), **web-save endpoint** = scholar lane (other agent's territory — coordinate via CLAIMS).

### D. Don't touch (other agent's live lanes)
- L4 songs (spandasandoha v2 etc.), C2 renders (kramastotra + phrdaya merged), Tier-2 transformations (stavacintamani in flight), scholar-submission service internals until (2) lands.
- Their working tree in translation-work may be dirty — `git pull --rebase` only when clean; push via PR branch if blocked (proven pattern today).

## 2. State of the gates (must stay green)

```bash
cd translation-work && python3 check.py        # CANONICAL: 0 (incl. scholar-valid)
cd ipvv && python3 tools/verify_site.py        # SITE GATES PASS (89 warnings, warn-only)
cd svread && node tests/scholar-smoke.cjs      # 0 fails
# release train: emit → trace → site/build.py (FULL) → verify → deploy → re-vendor → deploy svread
# deploy svread ONLY via ./deploy.sh (bumps SW cache every time)
```

## 3. Live URLs

reader https://svread.pages.dev/?work=paramarthasara · scholar hub `…&view=scholar` ·
ipvv https://ipvv-a8u.pages.dev · worker https://ipvv-api.tradesprior.workers.dev
(auth: `POST /api/auth/access` · account-claim blocked until verification · `EN_READ_OFF=false`).
