#!/usr/bin/env python3
"""beam_client — thin OpenAI-compatible chat client for OpenCode Go, with
model cycling across the free tier.

Key NEVER hardcoded: reads $OPENCODE_GO_KEY (persisted in oracle vault).
Sends required harness headers: own User-Agent + stable x-opencode-session.
Stdlib only. Usage:
  from beam_client import chat
  text = chat(messages, session='ipvv-v3b-001', max_tokens=6000)

Model policy (owner-authorized 2026-11-08; supersedes the 2026-11-06
beam-free-only hardening): beam-free stays FIRST (calibration continuity —
all benchmarks were cut against it), then free-tier fallbacks in fixed
order. A model that 429s is parked for 30 min (shared file, so all workers
agree) and the call fails over immediately instead of sleeping 12 minutes
per call. Every served call is appended to process/beam/model_usage.jsonl
{ts, session, model} so calibration can be audited per model later.
Untested models are NOT trusted for meaning — the pydantic gates +
assessor review apply to every model equally (mistakes #20: a vote is not
evidence, and neither is a new model).
"""
from __future__ import annotations
import json, os, sys, time, urllib.request

ENDPOINT = 'https://opencode.ai/inference/go/openai/v1/chat/completions'
UA = 'translation-work-harness/1.0'
# Preference order. beam-free first (calibration); fallbacks verified live
# 2026-11-08 (HTTP 200 + real JSON content on this box while beam-free 429s).
# Per-model output ceilings from GET /inference/go/openai/v1/models.
MODELS: list[tuple[str, int]] = [
    ('beam-free', 131072),
    ('deepseek-v4.1-flash', 384000),
    ('mimo-v2.6-flash', 131072),
    ('glm-5.3-flash', 131072),
    ('qwen3.8-flash', 131072),
    ('kimi-k3', 131072),
    ('minimax-m3.1-flash', 512000),
]
MODEL = MODELS[0][0]  # default / first preference (kept for compat)
# Published limits: 1M context class; output ceiling is per-model above.
MAX_CONTEXT = 1000000
MAX_OUTPUT = 384000
COOLDOWN_SECS = 1800  # park a 429ing model for 30 min (matches watchdog PAUSE)


def _root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _health_path() -> str:
    return os.path.join(_root(), 'process', 'beam', 'model_health.json')


def _load_health() -> dict:
    try:
        with open(_health_path()) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _mark_down(model: str) -> None:
    try:
        h = _load_health()
        h[model] = time.time() + COOLDOWN_SECS
        tmp = _health_path() + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(h, f)
        os.replace(tmp, _health_path())
    except OSError:
        pass


def _mark_up(model: str) -> None:
    try:
        h = _load_health()
        if model in h:
            del h[model]
            tmp = _health_path() + '.tmp'
            with open(tmp, 'w') as f:
                json.dump(h, f)
            os.replace(tmp, _health_path())
    except OSError:
        pass


def _log_use(session: str, model: str) -> None:
    try:
        p = os.path.join(_root(), 'process', 'beam', 'model_usage.jsonl')
        with open(p, 'a') as f:
            f.write(json.dumps({'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                'session': session, 'model': model}) + '\n')
    except OSError:
        pass


def _key() -> str:
    k = os.environ.get('OPENCODE_GO_KEY', '')
    if not k:
        raise RuntimeError('OPENCODE_GO_KEY not set (pull from oracle vault)')
    return k


def _candidates() -> list[tuple[str, int]]:
    """Healthy models first (beam-free keeps pole position when healthy),
    parked ones last (still tried if everything else fails)."""
    h = _load_health()
    now = time.time()
    fresh = [(m, cap) for m, cap in MODELS if h.get(m, 0) <= now]
    stale = [(m, cap) for m, cap in MODELS if h.get(m, 0) > now]
    return fresh or stale


def health() -> tuple[bool, str]:
    """Cheap probe: True if ANY cycling model answers. Used by the watchdog
    to pause instead of hammering when the free tier is throttled."""
    for model, _ in MODELS:
        try:
            chat([{'role': 'user', 'content': 'Reply with exactly: PONG'}],
                 session=f'health-probe-{model}', max_tokens=50, tries=1,
                 timeout=30, _only=[model])
            return True, f'ok:{model}'
        except Exception:  # noqa: BLE001 - try next model
            continue
    return False, 'all models throttled'


def chat(messages: list, session: str, max_tokens: int = MAX_OUTPUT,
         temperature: float = 0.2, tries: int = 4, timeout: int = 300,
         _only: list[str] | None = None) -> str:
    # NOTE: free models spend budget on hidden reasoning; without a low
    # reasoning effort + generous budget the reply comes back null
    # (finish=length). Do not lower these without re-testing.
    order = [(m, c) for m, c in _candidates() if _only is None or m in _only]
    last: Exception | None = None
    for model, cap in order:
        body = json.dumps({'model': model, 'messages': messages,
                           'max_tokens': min(max_tokens, cap),
                           'temperature': temperature,
                           'reasoning_effort': 'low'}).encode()
        attempts = max(1, min(tries, 2)) if len(order) > 1 else tries
        for attempt in range(attempts):
            req = urllib.request.Request(
                ENDPOINT, data=body,
                headers={'Authorization': 'Bearer ' + _key(),
                         'Content-Type': 'application/json',
                         'User-Agent': UA,
                         'x-opencode-session': session})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    out = json.loads(r.read().decode())
                msg = out['choices'][0]['message']
                text = msg.get('content')
                if not text:
                    # refusal or empty: retry same model briefly, else move on
                    last = RuntimeError(
                        f"empty content (refusal={msg.get('refusal')!r}, "
                        f"finish={out['choices'][0].get('finish_reason')})")
                    time.sleep(2 * (attempt + 1))
                    continue
                _mark_up(model)
                _log_use(session, model)
                return text
            except Exception as e:  # noqa: BLE001 - classify, then move on
                last = e
                s = str(e).lower()
                if '429' in str(e) or 'rate limit' in s or 'too many' in s:
                    _mark_down(model)
                    break  # fail over immediately, don't sleep out the quota
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f'beam chat failed on {len(order)} model(s) '
                       f'(session {session}): {last}')


def beam(prompt_system: str, prompt_user: str, session: str, max_tokens: int = 6000) -> str:
    return chat([{'role': 'system', 'content': prompt_system},
                 {'role': 'user', 'content': prompt_user}],
                session=session, max_tokens=max_tokens)
