#!/usr/bin/env python3
"""Authenticated Scholar submission service backed by isolated Git worktrees.

The service defaults to localhost. Put it behind HTTPS for remote use. Its
private token file maps SHA-256 bearer-token hashes to contributor names.
Submissions become separate Git branches for review; they do not change main.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
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


def validate_candidate(checkout: Path, work: str, version: dict) -> None:
    """Validate a candidate in a disposable checkout, restoring canonical bytes."""
    layer, target = version['layer'], version['target']
    song = scholar.song_of(target, layer)
    proof_path = checkout / work / 'proof' / f'proof-{song}.json'
    if not proof_path.is_file():
        raise ValueError('canonical proof not available')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    if proof.get('work') != work or proof.get('song') != song or proof.get('deterministic_gate') != 'PASS':
        raise ValueError('canonical source is not PASS gated')
    if (checkout / work / 'source/manifest.json').exists():
        current = {}
        for name in scholar.LAYERS:
            layer_file = checkout / work / 'data' / f'{song}.{name}.json'
            if layer_file.exists():
                current[name] = scholar.sha(json.loads(layer_file.read_text(encoding='utf-8')))
        if proof.get('layer_sha256',{}) != current:
            raise ValueError('canonical proof is stale')
    path = checkout / work / 'data' / f'{song}.{layer}.json'
    original = path.read_bytes()
    try:
        values = json.loads(original)
        if layer in scholar.layer_registry.SONG_LAYERS:
            updated = version['content']
        elif layer == 'l0':
            replacement = version['content']
            if not isinstance(replacement,list): raise ValueError('invalid L0 candidate')
            positions = [i for i,row in enumerate(values) if row.get('verse_id') == target]
            if not positions: raise ValueError('candidate target not found')
            updated = values[:positions[0]] + replacement + [row for row in values[positions[0]:] if row.get('verse_id') != target]
        else:
            positions = [i for i,row in enumerate(values) if row.get('verse_id') == target]
            if len(positions) != 1: raise ValueError('candidate target not found uniquely')
            updated = list(values); updated[positions[0]] = version['content']
        path.write_text(json.dumps(updated,ensure_ascii=False),encoding='utf-8')
        result = subprocess.run([sys.executable,str(checkout/'tools/validate_song.py'),'--work',work,'--song',song],
                                cwd=checkout,capture_output=True,text=True,timeout=45,check=False)
        if result.returncode:
            raise ValueError('cross-layer validation failed: '+(result.stdout or result.stderr)[:4000])
    finally:
        path.write_bytes(original)


def submit(repo: Path, payload: dict, author: str, push_remote: str | None = None,
           account_approval: dict | None = None) -> dict:
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
                    if account_approval and (repo.parent/'ipvv').is_dir():
                        os.symlink(repo.parent/'ipvv',Path(directory)/'ipvv')
                    submission_file = Path(directory) / "submission.json"
                    submission_file.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(checkout / "tools/scholar.py"), "import", "--file", str(submission_file)],
                        cwd=checkout, text=True, capture_output=True, check=False)
                    if result.returncode:
                        raise ValueError(result.stderr.strip() or "submission validation failed")
                    work = request["work"]
                    if account_approval:
                        mapping = json.loads(result.stdout)['versions']
                        version_id = mapping[request['versions'][-1]['version_id']]
                        versions = [json.loads(line) for line in (checkout/work/'scholar/versions.jsonl').read_text().splitlines() if line]
                        version = next(row for row in versions if row['version_id'] == version_id)
                        validate_candidate(checkout,work,version)
                        approval = subprocess.run([sys.executable,str(checkout/'tools/scholar.py'),'approve-version',
                            '--work',work,'--version',version_id,'--by',author,'--account-id',account_approval['account_id'],
                            '--signoff-id',account_approval['id'],'--snapshot-sha256',account_approval['snapshot_sha256'],
                            '--rights',account_approval['rights']],cwd=checkout,capture_output=True,text=True,timeout=45,check=False)
                        if approval.returncode: raise ValueError(approval.stderr.strip() or 'author approval failed')
                    git(checkout, "add", "--", f"{work}/scholar/versions.jsonl",
                        f"{work}/scholar/objects")
                    if account_approval:
                        git(checkout,'add','--',f'{work}/scholar/reviews.jsonl')
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


def submit_essay(repo: Path, payload: dict, push_remote: str | None = None) -> dict:
    snap, approval = payload['snapshot'], payload['signoff']
    work = snap['work']
    if not (repo/work/'data').is_dir() or not snap['title'].strip():
        raise ValueError('essay needs an existing work and title')
    if snap['target']:
        song=scholar.song_of(snap['target'],'t1')
        source=repo/work/'data'/f'{song}.t1.json';proof_path=repo/work/'proof'/f'proof-{song}.json'
        if not source.is_file() or not proof_path.is_file():raise ValueError('essay source passage is unavailable')
        rows=json.loads(source.read_text(encoding='utf-8'));proof=json.loads(proof_path.read_text(encoding='utf-8'))
        if (not any(row.get('verse_id')==snap['target'] for row in rows) or proof.get('work')!=work or
            proof.get('song')!=song or proof.get('deterministic_gate')!='PASS'):
            raise ValueError('essay source passage is not PASS gated')
        if (repo/work/'source/manifest.json').exists():
            current={}
            for layer in scholar.LAYERS:
                f=repo/work/'data'/f'{song}.{layer}.json'
                if f.exists():current[layer]=scholar.sha(json.loads(f.read_text(encoding='utf-8')))
            if proof.get('layer_sha256',{})!=current:raise ValueError('essay source proof is stale')
    entry = {'format':'scholar-essay/1','work':work,'target':snap['target'],'title':snap['title'],
             'text':snap['content']['text'],'author':payload['author'],'author_id':payload['account_id'],
             'identity_state':'SELF_ATTESTED','rights':approval['rights'],'signoff':approval,'snapshot':snap,
             'assisted':bool(snap['content'].get('assisted')),'model':str(snap['content'].get('model',''))[:120],
             'validation_scope':'essay structure and declared source link'}
    digest = scholar.sha(entry); entry['essay_id'] = 'essay:'+digest
    ref = f'refs/heads/scholar/essay-{digest}'
    with SUBMISSION_LOCK:
        existing = git(repo,'rev-parse','--verify',ref,check=False)
        if existing.returncode == 0:
            commit = existing.stdout.strip()
        else:
            base = git(repo,'rev-parse','HEAD').stdout.strip()
            with tempfile.TemporaryDirectory(prefix='scholar-essay-') as directory:
                checkout = Path(directory)/'checkout'; added = False
                try:
                    git(repo,'worktree','add','--quiet','--detach',str(checkout),base);added=True
                    folder=checkout/work/'scholar/essays';folder.mkdir(parents=True,exist_ok=True)
                    (folder/f'{digest}.json').write_bytes(scholar.canon(entry))
                    git(checkout,'add','--',f'{work}/scholar/essays/{digest}.json')
                    git(checkout,'-c','user.name=Svatantrya Scholar Service','-c','user.email=scholar@localhost',
                        'commit','--quiet','-m',f'Scholar essay for {work}')
                    commit=git(checkout,'rev-parse','HEAD').stdout.strip()
                    created=git(repo,'update-ref',ref,commit,'',check=False)
                    if created.returncode:commit=git(repo,'rev-parse','--verify',ref).stdout.strip()
                finally:
                    if added:git(repo,'worktree','remove','--force',str(checkout),check=False)
        if push_remote:
            pushed=git(repo,'push',push_remote,f'{ref}:{ref}',check=False)
            if pushed.returncode:raise RuntimeError('essay saved locally but branch push failed')
    return {'status':'submitted','branch':ref.removeprefix('refs/heads/'),'commit':commit,
            'remote_pushed':bool(push_remote),'essay_id':entry['essay_id']}


def submit_account(repo: Path, payload: dict, push_remote: str | None = None) -> dict:
    if not isinstance(payload,dict) or payload.get('format') != 'scholar-account-submission/1':
        raise ValueError('invalid account submission')
    account,author,snap,approval=(payload.get(k) for k in ('account_id','author','snapshot','signoff'))
    if (not isinstance(account,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',account) or
        not isinstance(author,str) or not author.strip() or len(author)>120 or any(ord(c)<32 for c in author) or
        not isinstance(snap,dict) or not isinstance(approval,dict)):
        raise ValueError('invalid contributor or snapshot')
    content=snap.get('content')
    if (not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}',str(snap.get('work',''))) or
        not isinstance(snap.get('target'),str) or (snap['target'] and not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',snap['target'])) or
        not isinstance(snap.get('title'),str) or len(snap['title'])>300 or
        not isinstance(payload.get('revision'),int) or isinstance(payload['revision'],bool) or payload['revision']<1 or
        not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',str(payload.get('document_id',''))) or
        not re.fullmatch(r'signoff:[A-Za-z0-9-]{1,100}',str(approval.get('id',''))) or
        not isinstance(approval.get('created_at'),str) or len(approval['created_at'])>60 or
        not isinstance(content,dict) or not isinstance(content.get('text'),str) or
        not content['text'].strip() or len(content['text'])>60000 or
        approval.get('rights') not in ('all-rights-reserved','cc-by-4.0','cc0')):
        raise ValueError('invalid submission content')
    if scholar.sha(snap) != approval.get('snapshot_sha256'):
        raise ValueError('sign-off does not match the submitted snapshot')
    if snap.get('kind') == 'essay':return submit_essay(repo,payload,push_remote)
    if snap.get('kind') != 'translation' or snap.get('layer') not in scholar.LAYERS:
        raise ValueError('unsupported submission kind or layer')
    layer=snap['layer']
    if layer in ('t1','l2','l3','l4'): value={'text':content['text']}
    else:
        try:value=json.loads(content['text'])
        except ValueError:raise ValueError('this layer needs valid JSON')
    base=content.get('base_sha256','');parent=content.get('parent') or None
    if not re.fullmatch(r'[0-9a-f]{64}',str(base)):raise ValueError('canonical base hash is required')
    if parent and not re.fullmatch(r'sv:[0-9a-f]{16,64}',str(parent)):raise ValueError('published parent version is invalid')
    note='Account author approval; rights: '+approval['rights']+'; signoff: '+approval['id']+'; account: '+account
    if content.get('assisted'):note+='; AI-assisted ('+re.sub(r'[^A-Za-z0-9_.-]','',str(content.get('model','agent')))[:120]+')'
    entry={'version_id':'local:account-'+scholar.sha({'account':account,'snapshot':approval['snapshot_sha256']}),
           'work':snap['work'],'layer':layer,'target':snap['target'],'parent':parent,'base_sha256':base,
           'author':author,'author_kind':'human','note':note,'content':value}
    return submit(repo,{'work':snap['work'],'versions':[entry]},author,push_remote,
                  {'account_id':account,'id':approval['id'],'snapshot_sha256':approval['snapshot_sha256'],'rights':approval['rights']})


def session_secret() -> bytes | None:
    """Same HMAC secret the worker signs svsess cookies with (rotated together —
    see worker/AUTH-SETUP.md). File wins over env; must be mode 600."""
    env_secret = os.environ.get("SESSION_SECRET", "").strip()
    path = Path.home() / ".scholar" / "session_secret"
    if path.exists():
        if path.stat().st_mode & 0o077:
            raise ValueError("session_secret file must be mode 600")
        return path.read_text(encoding="utf-8").strip().encode("utf-8")
    return env_secret.encode("utf-8") if env_secret else None


def session_author(cookie: str, auth_header: str) -> str | None:
    """The svread login session IS the credential (owner directive: one account).
    Verifies svsess HMAC + expiry locally, then resolves the display name from
    the worker — attribution comes from the identity service, never the client.
    Raises on identity-service failure (caller maps to 502); returns None when
    the token itself is simply absent/invalid (401)."""
    token = ""
    for part in (cookie or "").split(";"):
        key, _, value = part.strip().partition("=")
        if key == "svsess":
            token = value
            break
    if not token and auth_header.startswith("Svsess "):
        token = auth_header[7:].strip()
    if not token or "." not in token:
        return None
    secret = session_secret()
    if not secret:
        return None
    body, _, sig = token.rpartition(".")
    try:
        mac = hmac.new(secret, body.encode("utf-8"), hashlib.sha256).digest()
        want = base64.urlsafe_b64encode(mac).rstrip(b"=").decode("ascii")
        if not hmac.compare_digest(want, sig):
            return None
        payload = json.loads(base64.b64decode(body + "=" * (-len(body) % 4)))
        if int(payload.get("e", 0)) < int(time.time() * 1000):
            return None
    except Exception:
        return None
    req = urllib.request.Request(
        "https://ipvv-api.tradesprior.workers.dev/api/auth/me",
        headers={"Cookie": f"svsess={token}",
                 "Origin": "https://svread.pages.dev",   # passes the worker's auth origin guard
                 "User-Agent": "svread-scholar/1.0"})    # default urllib UA is 403'd at the edge
    with urllib.request.urlopen(req, timeout=5) as resp:
        profile = json.loads(resp.read()).get("profile") or {}
    name = str(profile.get("display_name") or profile.get("email") or "").strip()
    if not name:
        raise RuntimeError("session profile has no display name")
    return name


def resolve_author(headers, users: list[dict]) -> tuple[str | None, int | None]:
    """Bearer (legacy) first, then the shared svread session. Returns (author, error_status)."""
    auth = headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        legacy = authenticated_author(auth[7:], users)
        if legacy:
            return legacy, None
    try:
        author = session_author(headers.get("Cookie", ""), auth)
    except Exception:
        return None, 502
    return (author, None) if author else (None, 401)


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


def handler_for(repo: Path, users: list[dict], allowed_origin: str, push_remote: str | None,
                bridge_secret: bytes | None = None):
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
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type, Cookie")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def do_GET(self):
            if self.path != "/v1/scholar/whoami":
                return self.response(404, {"error": "not found"})
            author, err = resolve_author(self.headers, users)
            if not author:
                if err == 502:
                    return self.response(502, {"error": "identity service unreachable"})
                return self.response(401, {"error": "authentication required"})
            return self.response(200, {"author": author, "via": "svread-session"})

        def do_POST(self):
            if self.path not in ("/v1/scholar/submissions",'/v1/scholar/account-submissions'):
                return self.response(404, {"error": "not found"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > MAX_BODY:
                    return self.response(413, {"error": "invalid submission size"})
                raw=self.rfile.read(size)
                if self.path == '/v1/scholar/account-submissions':
                    stamp=self.headers.get('X-Scholar-Time',''); signature=self.headers.get('X-Scholar-Signature','')
                    if not bridge_secret or not stamp.isdigit() or abs(time.time()-int(stamp))>120:
                        return self.response(401,{'error':'authentication required'})
                    message=f'scholar-bridge/v1\n{stamp}\n{hashlib.sha256(raw).hexdigest()}'.encode()
                    expected=hmac.new(bridge_secret,message,hashlib.sha256).hexdigest()
                    if not hmac.compare_digest(signature,expected):
                        return self.response(401,{'error':'authentication required'})
                    result=submit_account(repo,json.loads(raw),push_remote)
                else:
                    author,err=resolve_author(self.headers,users)
                    if not author:
                        if err==502:return self.response(502,{'error':'identity service unreachable'})
                        return self.response(401,{'error':'authentication required'})
                    result=submit(repo,json.loads(raw),author,push_remote)
                return self.response(200, result)
            except (ValueError, json.JSONDecodeError) as exc:
                return self.response(400, {"error": str(exc)})
            except (OSError, subprocess.SubprocessError, RuntimeError):
                return self.response(500, {"error": "submission could not be saved"})
    return Handler


def load_bridge_secret(path: Path, repo: Path) -> bytes:
    path=path.resolve()
    if path.is_relative_to(repo.resolve()) or path.stat().st_mode & 0o077:
        raise ValueError('bridge secret must be outside the repository and owner-only')
    value=path.read_bytes().strip()
    if len(value)<32:raise ValueError('bridge secret needs at least 32 bytes')
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokens-file", help="optional private bearer-token mapping")
    parser.add_argument('--bridge-secret-file',help='owner-only shared Worker bridge secret')
    parser.add_argument("--origin", required=True, help="exact allowed browser origin")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--push-remote", help="optional Git remote for submission branches")
    args = parser.parse_args()
    try:
        users = load_users(Path(args.tokens_file), ROOT) if args.tokens_file else []
        bridge_secret=load_bridge_secret(Path(args.bridge_secret_file),ROOT) if args.bridge_secret_file else None
        if not users and not bridge_secret and not session_secret():
            raise ValueError('configure a token file, Worker bridge secret or shared session secret')
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
                                     handler_for(ROOT, users, args.origin, args.push_remote,bridge_secret))
        print(f"Scholar submission service listening on {args.bind}:{args.port}", flush=True)
        server.serve_forever()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
