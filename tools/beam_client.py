#!/usr/bin/env python3
"""beam_client — thin OpenAI-compatible chat client for OpenCode Go.

Key NEVER hardcoded: reads $OPENCODE_GO_KEY (persisted in oracle vault).
Sends required harness headers: own User-Agent + stable x-opencode-session.
Stdlib only. Usage:
  from beam_client import chat
  text = chat(messages, session='ipvv-v3b-001', max_tokens=6000)

FREE ONLY. Only models with zero price may be called (owner directive:
2026-11-06 beam-free-only; 2026-11-08 free-only cycling — a wrong turn into
Go-allowance models was reverted the same session). The /go endpoint lists
30 models but exactly TWO are free: beam-free (1M ctx / 131k out) and
iceman-contributor-free (262k ctx / 131k out). Everything else
(deepseek/mimo/glm/qwen/kimi/...) bills Go allowance — never call them.
crouton-alpha-free is also free but region-blocked here (RegionError).
beam-free stays FIRST (all benchmarks were cut against it); iceman is the
failover. A model that 429s is parked 30 min (shared file, so all workers
agree) and the call fails over immediately. Every served call is appended
to process/beam/model_usage.jsonl {ts, session, model} so usage stays
auditable. Untested models are NOT trusted for meaning — the pydantic gates
+ assessor review apply to every model equally.
"""
from __future__ import annotations
import json, os, sys, time, urllib.request

ENDPOINT = 'https://opencode.ai/inference/go/openai/v1/chat/completions'
UA = 'translation-work-harness/1.0'
# HARDCODED: beam-free only. Other models fail in this harness (owner
# FREE ONLY (owner directive 2026-11-06 beam-free-only, extended 2026-11-08
# to free-only cycling: the /go catalogue beyond beam-free bills Go
# allowances, EXCEPT iceman-contributor-free which is zero-price like
# beam-free). Do not add an env override. Only the MODELS list below may
# ever be called, and only zero-price entries may enter it.
MODEL = 'beam-free'
# FREE-ONLY preference order, verified live 2026-11-08 on this box.
# beam-free first (calibration continuity); iceman-contributor-free is the
# ONLY other zero-price model reachable here (crouton-alpha-free returns
# RegionError). Everything else on the endpoint bills Go allowance — never
# add it here.
MODELS: list[tuple[str, int]] = [
    ('beam-free', 131072),
    ('iceman-contributor-free', 131072),
]
COOLDOWN_SECS = 1800  # park a 429ing model for 30 min (shared file, all workers agree)
# Published limits (GET /inference/go/openai/v1/models): context 1,048,576,
# output 131,072. Use the ceiling — fewer, bigger requests also avoid the
# 429 rate limiter seen with many small calls.
MAX_CONTEXT = 1000000
MAX_OUTPUT = 131072

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
            json.dump({'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                       'session': session, 'model': model}, f)
            f.write('\n')
    except OSError:
        pass


def _key() -> str:
    k = os.environ.get('OPENCODE_GO_KEY', '')
    if not k:
        raise RuntimeError('OPENCODE_GO_KEY not set (pull from oracle vault)')
    return k


def _candidates() -> list:
    h = _load_health()
    now = time.time()
    fresh = [(m, c) for m, c in MODELS if h.get(m, 0) <= now]
    return fresh or list(MODELS)


def health() -> tuple:
    """Cheap probe: True if ANY free model answers. Used by the watchdog to
    pause instead of hammering when the free tier is throttled."""
    for model, _cap in MODELS:
        try:
            chat([{'role': 'user', 'content': 'Reply with exactly: PONG'}],
                 session='health-probe-' + model, max_tokens=50, tries=1,
                 timeout=30, _only=[model])
            return True, 'ok:' + model
        except Exception:
            continue
    return False, 'all free models throttled'


def chat(messages: list, session: str, max_tokens: int = MAX_OUTPUT,
         temperature: float = 0.2, tries: int = 4, timeout: int = 300,
         _only: list = None) -> str:
    # NOTE: free models spend budget on hidden reasoning; without a low
    # reasoning effort + generous budget the reply comes back null
    # (finish=length). Do not lower these without re-testing.
    order = [(m, c) for m, c in _candidates() if _only is None or m in _only]
    last = None
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
                    # refusal or empty: retry same model briefly, then move on
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
                    break  # fail over immediately, never sleep out the quota
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f'beam chat failed on {len(order)} free model(s) '
                       f'(session {session}): {last}')

def beam(prompt_system: str, prompt_user: str, session: str, max_tokens: int = 6000) -> str:
    return chat([{'role': 'system', 'content': prompt_system},
                 {'role': 'user', 'content': prompt_user}],
                session=session, max_tokens=max_tokens)
