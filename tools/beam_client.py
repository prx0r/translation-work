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
# MODEL override: beam-free is "limited time". If it goes away, set
# BEAM_MODEL to another Go model id (e.g. mimo-v2.5, qwen3.8-flash)
# without touching callers. Cost then counts against the Go plan.
MODEL = os.environ.get('BEAM_MODEL', 'beam-free')

def _key() -> str:
    k = os.environ.get('OPENCODE_GO_KEY', '')
    if not k:
        raise RuntimeError('OPENCODE_GO_KEY not set (pull from oracle vault)')
    return k

def chat(messages: list, session: str, max_tokens: int = 8000,
         temperature: float = 0.2, tries: int = 4) -> str:
    # NOTE: beam-free spends budget on hidden reasoning; without a low
    # reasoning effort + generous budget the reply comes back null
    # (finish=length). Do not lower these without re-testing.
    body = json.dumps({'model': MODEL, 'messages': messages,
                       'max_tokens': max_tokens, 'temperature': temperature,
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
            with urllib.request.urlopen(req, timeout=300) as r:
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
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f'beam chat failed x{tries} (session {session}): {last}')

def beam(prompt_system: str, prompt_user: str, session: str, max_tokens: int = 6000) -> str:
    return chat([{'role': 'system', 'content': prompt_system},
                 {'role': 'user', 'content': prompt_user}],
                session=session, max_tokens=max_tokens)
