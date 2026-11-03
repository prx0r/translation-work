#!/usr/bin/env python3
"""Authenticated Scholar submission service backed by isolated Git worktrees.

The service defaults to localhost. Put it behind HTTPS for remote use. Its
private token file maps SHA-256 bearer-token hashes to contributor names.
Submissions become separate Git branches for review; they do not change main.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import scholar  # noqa: E402

MAX_BODY = 2 * 1024 * 1024
SUBMISSION_LOCK = threading.Lock()


def git(repo: Path, *args: str, check: bool = True):
    return subprocess.run(["git", "-C", str(repo), *args], text=True,
                          capture_output=True, check=check)


def authenticated_author(token: str, users: list[dict]) -> str | None:
    if len(token) < 32:
        return None
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    found = None
    for user in users:
        expected = user.get("token_sha256", "")
        if isinstance(expected, str) and hmac.compare_digest(digest, expected):
            found = user.get("author")
    return found if isinstance(found, str) and found.strip() else None


def submit(repo: Path, payload: dict, author: str, push_remote: str | None = None) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("versions"), list):
        raise ValueError("a version submission is required")
    if not isinstance(payload.get("work"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", payload["work"]):
        raise ValueError("invalid work")
    if not author or len(author) > 120 or any(ord(char) < 32 for char in author):
        raise ValueError("invalid configured contributor")
    request = {"format": "scholar-submission/v1", "work": payload["work"], "versions": []}
    for entry in payload["versions"]:
        if not isinstance(entry, dict):
            raise ValueError("each version must be an object")
        # The authenticated server mapping determines attribution, not the request.
        request["versions"].append({**entry, "author": author, "author_kind": "human"})
    request_hash = scholar.sha(request)
    ref = f"refs/heads/scholar/submission-{request_hash}"
    with SUBMISSION_LOCK:
        existing = git(repo, "rev-parse", "--verify", ref, check=False)
        if existing.returncode == 0:
            commit = existing.stdout.strip()
        else:
            base = git(repo, "rev-parse", "HEAD").stdout.strip()
            with tempfile.TemporaryDirectory(prefix="scholar-submit-") as directory:
                checkout = Path(directory) / "checkout"
                added = False
                try:
                    git(repo, "worktree", "add", "--quiet", "--detach", str(checkout), base)
                    added = True
                    submission_file = Path(directory) / "submission.json"
                    submission_file.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(checkout / "tools/scholar.py"), "import", "--file", str(submission_file)],
                        cwd=checkout, text=True, capture_output=True, check=False)
                    if result.returncode:
                        raise ValueError(result.stderr.strip() or "submission validation failed")
                    work = request["work"]
                    git(checkout, "add", "--", f"{work}/scholar/versions.jsonl",
                        f"{work}/scholar/objects")
                    staged = git(checkout, "diff", "--cached", "--quiet", check=False)
                    if staged.returncode not in (0, 1):
                        raise RuntimeError("could not inspect submission changes")
                    if staged.returncode == 1:
                        git(checkout, "-c", "user.name=Svatantrya Scholar Service",
                            "-c", "user.email=scholar@localhost", "commit", "--quiet",
                            "-m", f"Scholar submission for {work}")
                        commit = git(checkout, "rev-parse", "HEAD").stdout.strip()
                    else:
                        commit = base
                    created = git(repo, "update-ref", ref, commit, "", check=False)
                    if created.returncode:
                        commit = git(repo, "rev-parse", "--verify", ref).stdout.strip()
                finally:
                    if added:
                        git(repo, "worktree", "remove", "--force", str(checkout), check=False)
        if push_remote:
            pushed = git(repo, "push", push_remote, f"{ref}:{ref}", check=False)
            if pushed.returncode:
                raise RuntimeError("submission was saved locally but its branch could not be pushed")
    return {"status": "submitted", "branch": ref.removeprefix("refs/heads/"),
            "commit": commit, "remote_pushed": bool(push_remote),
            "message": "Submission saved for review and publication."}


def load_users(path: Path, repo: Path) -> list[dict]:
    path = path.resolve()
    if path.is_relative_to(repo.resolve()):
        raise ValueError("token file must be outside the repository")
    if path.stat().st_mode & 0o077:
        raise ValueError("token file must not be accessible to group or others")
    data = json.loads(path.read_text(encoding="utf-8"))
    users = data.get("users") if isinstance(data, dict) else None
    if not isinstance(users, list) or not users:
        raise ValueError("token file needs a non-empty users list")
    for user in users:
        if (not isinstance(user, dict) or not re.fullmatch(r"[0-9a-f]{64}", user.get("token_sha256", ""))
            or not isinstance(user.get("author"), str) or not user["author"].strip()):
            raise ValueError("each user needs author and token_sha256")
    return users


def handler_for(repo: Path, users: list[dict], allowed_origin: str, push_remote: str | None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return  # Never log bearer tokens or submitted content.

        def response(self, code, body):
            encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Vary", "Origin")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def do_POST(self):
            if self.path != "/v1/scholar/submissions":
                return self.response(404, {"error": "not found"})
            auth = self.headers.get("Authorization", "")
            author = authenticated_author(auth[7:], users) if auth.startswith("Bearer ") else None
            if not author:
                return self.response(401, {"error": "authentication required"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > MAX_BODY:
                    return self.response(413, {"error": "invalid submission size"})
                payload = json.loads(self.rfile.read(size))
                result = submit(repo, payload, author, push_remote)
                return self.response(200, result)
            except (ValueError, json.JSONDecodeError) as exc:
                return self.response(400, {"error": str(exc)})
            except (OSError, subprocess.SubprocessError, RuntimeError):
                return self.response(500, {"error": "submission could not be saved"})
    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokens-file", required=True)
    parser.add_argument("--origin", required=True, help="exact allowed browser origin")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--push-remote", help="optional Git remote for submission branches")
    args = parser.parse_args()
    try:
        users = load_users(Path(args.tokens_file), ROOT)
        if not re.fullmatch(r"https://[A-Za-z0-9.-]+(?::\d+)?|http://(?:localhost|127\.0\.0\.1)(?::\d+)?", args.origin):
            raise ValueError("origin must be an HTTPS origin or localhost")
        if args.push_remote:
            remotes = git(ROOT, "remote").stdout.splitlines()
            if args.push_remote not in remotes:
                raise ValueError("push remote is not configured")
        if args.bind not in ("127.0.0.1", "localhost"):
            raise ValueError("bind to localhost and use an HTTPS reverse proxy for remote access")
        if git(ROOT, "diff-index", "--quiet", "HEAD", "--", check=False).returncode:
            raise ValueError("commit the service and canonical data before starting")
        server = ThreadingHTTPServer((args.bind, args.port),
                                     handler_for(ROOT, users, args.origin, args.push_remote))
        print(f"Scholar submission service listening on {args.bind}:{args.port}", flush=True)
        server.serve_forever()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
