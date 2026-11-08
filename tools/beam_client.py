#!/usr/bin/env python3
"""beam_client — thin OpenAI-compatible chat client for OpenCode Go (beam-free).

Key NEVER hardcoded: reads $OPENCODE_GO_KEY (persisted in oracle vault).
Sends required harness headers: own User-Agent + stable x-opencode-session.
Stdlib only. Usage:
  from beam_client import chat
  text = chat(messages, session='ipvv-v3b-001', max_tokens=6000)
"""
from __future__ import annotations
import json, os, sys, time, urllib.request

ENDPOINT = 'https://opencode.ai/inference/go/openai/v1/chat/completions'
UA = 'translation-work-harness/1.0'
# HARDCODED: beam-free only. Other models fail in this harness (owner
# directive 2026-11-06). Do not add an env override, do not swap models.
MODEL = 'beam-free'
# Published limits (GET /inference/go/openai/v1/models, 2026-11-08):
# deepseek-v4.1-flash -> context 1,000,000, output 384,000. Use the full
# context (assemble whole-ahnika packets) and the full output ceiling —
# fewer, bigger requests also avoid the 429 limiter seen with many small calls.
MAX_CONTEXT = 1000000
MAX_OUTPUT = 384000

def _key() -> str:
    k = os.environ.get('OPENCODE_GO_KEY', '')
    if not k:
        raise RuntimeError('OPENCODE_GO_KEY not set (pull from oracle vault)')
    return k

def health() -> tuple[bool, str]:
    """Cheap probe: True if beam-free answers. Used by the watchdog to pause
    instead of hammering when the free tier is throttled."""
    try:
        # NOTE: budget must clear hidden-reasoning burn (mistakes #22) —
        # a 32-token probe nulls deterministically even when beam is healthy.
        chat([{'role': 'user', 'content': 'Reply with exactly: PONG'}],
             session='health-probe', max_tokens=2000, tries=1, timeout=60)
        return True, 'ok'
    except Exception as e:  # noqa: BLE001
        return False, str(e)[:200]


def chat(messages: list, session: str, max_tokens: int = MAX_OUTPUT,
         temperature: float = 0.2, tries: int = 4, timeout: int = 300) -> str:
    # NOTE: beam-free spends budget on hidden reasoning; without a low
    # reasoning effort + generous budget the reply comes back null
    # (finish=length). Do not lower these without re-testing.
    body = json.dumps({'model': MODEL, 'messages': messages,
                       'max_tokens': min(max_tokens, MAX_OUTPUT),
                       'temperature': temperature,
                       'reasoning_effort': 'low'}).encode()
    last = None
    for attempt in range(tries):
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
                # refusal or empty: retry; surface refusal reason on last try
                last = RuntimeError(f"empty content (refusal={msg.get('refusal')!r}, "
                                    f"finish={out['choices'][0].get('finish_reason')})")
                time.sleep(2 * (attempt + 1))
                continue
            return text
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            last = e
            msg = str(e).lower()
            wait = 180 * (attempt + 1) if ('429' in str(e) or 'rate limit' in msg) else 3 * (attempt + 1)
            time.sleep(wait)
    raise RuntimeError(f'beam chat failed x{tries} (session {session}): {last}')

def beam(prompt_system: str, prompt_user: str, session: str, max_tokens: int = 6000) -> str:
    return chat([{'role': 'system', 'content': prompt_system},
                 {'role': 'user', 'content': prompt_user}],
                session=session, max_tokens=max_tokens)
