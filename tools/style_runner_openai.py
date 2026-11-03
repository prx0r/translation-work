#!/usr/bin/env python3
"""Opt-in runner for a private style brief using an OpenAI-compatible endpoint.

Set STYLE_API_URL, STYLE_MODEL, and optionally STYLE_API_KEY in the environment.
The caller chooses the endpoint and is responsible for the scholar's consent and
the model's pricing. This script does not save the brief or model response.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse


def main() -> int:
    url = os.environ.get("STYLE_API_URL", "")
    model = os.environ.get("STYLE_MODEL", "")
    key = os.environ.get("STYLE_API_KEY", "")
    parsed = urlparse(url)
    local = parsed.hostname in ("localhost", "127.0.0.1")
    if not model or not parsed.netloc or not (parsed.scheme == "https" or
                                               (local and parsed.scheme == "http")):
        print("ERROR: configure STYLE_MODEL and an HTTPS STYLE_API_URL (or localhost HTTP)", file=sys.stderr)
        return 1
    try:
        brief = json.load(sys.stdin)
        layer = brief["target"]["layer"]
        field = "plain_english" if layer == "l2" else "lines"
        system = ("Return a single JSON object with one content property. That property must "
                  f"contain only {field}. Follow the source and translation evidence, and use "
                  "the scholar examples only as guidance for diction and cadence. Do not add "
                  "unsupported claims. Preserve uncertainties. Do not include markdown fences.")
        body = json.dumps({"model": model, "temperature": 0,
                           "messages": [{"role": "system", "content": system},
                                        {"role": "user", "content": json.dumps(brief, ensure_ascii=False)}]},
                          ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if key:
            headers["Authorization"] = "Bearer " + key
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.load(response)
        text = result["choices"][0]["message"]["content"]
        generated = json.loads(text)
        if not isinstance(generated, dict) or not isinstance(generated.get("content"), dict):
            raise ValueError("model response must contain a content object")
        print(json.dumps({"model": result.get("model") or model,
                          "content": generated["content"]}, ensure_ascii=False))
    except (KeyError, IndexError, TypeError, ValueError, OSError, urllib.error.URLError) as exc:
        print(f"ERROR: style generation failed ({type(exc).__name__})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
