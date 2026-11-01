"""Write build events to Supabase and check what the site's key can do (S-006 TK-002).

Two commands:

``ams-writer record-merge SHA [--test]``
    Reads a merge commit from Git, builds one ``build_events`` row from it
    (kind ``merge``, source the commit SHA, strength ``recorded_fact``) and
    inserts it through PostgREST with the service key. A second run reports
    ``already recorded``. ``--test`` marks the row so the site never sees it.

``ams-writer readcheck SHA``
    With the publishable key only: selects the row for SHA, then tries an
    insert, an update and a delete, and selects again. It passes only when the
    row is visible, every write gets an authorization denial (401, 403 or a
    42501 body) and the row is unchanged; a timeout, 5xx or other status is
    reported ``inconclusive`` and fails the check.

Keys are loaded as in ``ams.keycheck``: the process environment first, then the
gitignored env file at the repository root. No key value is ever printed,
logged or raised; HTTP error bodies and transport errors are not echoed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Mapping, Sequence

from ams import keycheck, source_rules

REPO_ROOT = keycheck.REPO_ROOT
REPO_URL = "https://github.com/KaydenClark/Agentic-Management-System"
TABLE = "build_events"
PUBLISHABLE_VAR = "SUPABASE_PUBLISHABLE_KEY"
# Public by design: ADR-003C and the env example name it; the site ships it.
DEFAULT_PUBLISHABLE_KEY = "sb_publishable_juFt2irDgR8h0Wr3S7I4_A_eSEa06gv"
# PostgREST answers a denied privilege (42501) with 401 for anon, 403 otherwise.
DENIED = (401, 403)
PERMISSION_DENIED = "42501"
READ_COLUMNS = "id,kind,subject,summary,occurred_at,source_kind,source_ref,source_url,strength,detail"

Http = Callable[[str, str, Mapping[str, str], bytes | None], tuple[int, bytes]]
Git = Callable[[Sequence[str]], str]

_MERGE_SUBJECT = re.compile(r"^Merge pull request #(\d+) from (\S+)")


# --- the row -----------------------------------------------------------------


def run_git(args: Sequence[str]) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args], check=True, capture_output=True, text=True
    ).stdout


def merge_event(sha: str, *, git: Git = run_git, is_test: bool = False) -> dict:
    """Build a build_events row for a PR merge commit, from Git only."""
    lines = git(["show", "-s", "--format=%H%n%P%n%cI%n%s%n%b", sha]).splitlines()
    if len(lines) < 4:
        raise ValueError(f"git show gave no commit for {sha}")
    full_sha, parents, committed, subject = lines[0], lines[1].split(), lines[2], lines[3]
    if len(parents) < 2:
        raise ValueError(f"{full_sha} is not a merge commit")
    match = _MERGE_SUBJECT.match(subject)
    if not match:
        raise ValueError(f"{full_sha} is not a GitHub pull-request merge")
    pr, branch = int(match.group(1)), match.group(2)
    title = next((line.strip() for line in lines[4:] if line.strip()), subject)
    return {
        "kind": "merge",
        "subject": f"PR #{pr}",
        "summary": title,
        "occurred_at": committed,
        "source_kind": "commit",
        "source_ref": full_sha,
        "source_url": f"{REPO_URL}/commit/{full_sha}",
        "strength": "recorded_fact",
        "is_test": is_test,
        "detail": {"pr": pr, "pr_url": f"{REPO_URL}/pull/{pr}", "branch": branch,
                   "parents": parents},
    }


# --- HTTP --------------------------------------------------------------------


def urllib_http(method: str, url: str, headers: Mapping[str, str], body: bytes | None):
    request = urllib.request.Request(url, data=body, headers=dict(headers), method=method)
    try:
        with urllib.request.urlopen(request, timeout=keycheck.TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def _headers(key: str) -> dict[str, str]:
    headers = {"apikey": key, "Content-Type": "application/json",
               "Prefer": "return=representation"}
    if keycheck.key_format(key) == "legacy-jwt":
        headers["Authorization"] = "Bearer " + key
    return headers


def _call(http: Http, method: str, url: str, key: str, payload=None):
    """Return (status, parsed body) or (None, None); never surfaces error text."""
    body = None if payload is None else json.dumps(payload).encode()
    try:
        status, raw = http(method, url, _headers(key), body)
    except Exception:
        return None, None
    try:
        return status, json.loads(raw) if raw else None
    except ValueError:
        return status, None


def insert_event(url: str, key: str, http: Http, row: Mapping):
    """Insert one build_events row after the shared source rule; raises ValueError first."""
    source_rules.check_source(row)
    return _call(http, "POST", _rest(url), key, dict(row))


def _ok(status) -> bool:
    return status is not None and 200 <= status < 300


# --- commands ----------------------------------------------------------------


def record_merge(sha: str, is_test: bool, settings: keycheck.Settings, http: Http, git: Git) -> int:
    if settings.key is None:
        print("loaded: no")
        return 1
    if keycheck.key_format(settings.key) == "unrecognized":
        print("loaded: yes\nformat: unrecognized")
        return 1
    try:
        row = merge_event(sha, git=git, is_test=is_test)
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"refused: {error}" if isinstance(error, ValueError) else f"refused: no commit {sha}")
        return 1
    status, body = insert_event(settings.url, settings.key, http, row)
    if status == 201 and isinstance(body, list) and body:
        saved = body[0]
        print(f"inserted: id={saved.get('id')} kind={row['kind']} subject={row['subject']} "
              f"source_ref={row['source_ref']} strength={row['strength']} is_test={is_test}")
        return 0
    if status == 409:
        print(f"already recorded: kind={row['kind']} source_ref={row['source_ref']}")
        return 0
    print(f"insert failed: http status {status if status is not None else 'none'}")
    return 1


def readcheck(sha: str, url: str, key: str, http: Http) -> int:
    if keycheck.key_format(key) != "unrecognized" or not key.startswith("sb_publishable_"):
        print("refused: the publishable slot holds a key that is not a publishable key")
        return 1
    query = f"{_rest(url)}?source_ref=eq.{sha}&select={READ_COLUMNS}"
    status, before = _call(http, "GET", query, key)
    rows = before if _ok(status) and isinstance(before, list) else []
    print(f"select: http status {status if status is not None else 'none'}, rows: {len(rows)}")
    for row in rows:
        print("row: " + json.dumps(row, sort_keys=True))
    target = f"{_rest(url)}?source_ref=eq.{sha}"
    probe = {"kind": "merge", "subject": "client write probe", "summary": "must be refused",
             "occurred_at": "2026-11-01T00:00:00Z", "source_kind": "commit",
             "source_ref": "client-write-probe", "strength": "anecdote", "is_test": True}
    attempts = [("insert", "POST", _rest(url), probe),
                ("update", "PATCH", target, {"summary": "client write probe"}),
                ("delete", "DELETE", target, None)]
    refused_all = True
    for verb, method, endpoint, payload in attempts:
        status, body = _call(http, method, endpoint, key, payload)
        shown = status if status is not None else "none"
        if _denied(status, body):
            print(f"{verb}: refused (http status {shown})")
        elif _ok(status):
            refused_all = False
            print(f"{verb}: ACCEPTED (http status {shown})")
        else:
            # A timeout, 5xx or other status does not show permission enforcement.
            refused_all = False
            print(f"{verb}: inconclusive (http status {shown})")
    status, after = _call(http, "GET", query, key)
    unchanged = bool(rows) and _ok(status) and after == before
    print(f"row unchanged: {'yes' if unchanged else 'no'}")
    return 0 if rows and refused_all and unchanged else 1


def _denied(status, body) -> bool:
    """True only for an explicit authorization denial, never for a timeout or 5xx."""
    if status in DENIED:
        return True
    code = body.get("code") if isinstance(body, dict) else None
    return status is not None and 400 <= status < 500 and code == PERMISSION_DENIED


def _rest(url: str) -> str:
    return url.rstrip("/") + "/rest/v1/" + TABLE


def publishable_key(environ: Mapping[str, str], dotenv_path: Path) -> str:
    value = (environ.get(PUBLISHABLE_VAR) or "").strip()
    if not value:
        value = keycheck.read_dotenv(dotenv_path, (PUBLISHABLE_VAR,)).get(PUBLISHABLE_VAR, "").strip()
    return value or DEFAULT_PUBLISHABLE_KEY


def main(
    argv: list[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    dotenv_path: Path | None = None,
    http: Http | None = None,
    git: Git | None = None,
) -> int:
    parser = argparse.ArgumentParser(prog="ams-writer", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record-merge", help="insert one PR merge commit as a build event")
    record.add_argument("sha")
    record.add_argument("--test", action="store_true", help="mark the row as a test row")
    check = sub.add_parser("readcheck", help="read with the publishable key; try every write")
    check.add_argument("sha")
    args = parser.parse_args(argv)

    environ = os.environ if environ is None else environ
    dotenv_path = keycheck.DOTENV_PATH if dotenv_path is None else dotenv_path
    settings = keycheck.load_settings(environ, dotenv_path)
    http = http or urllib_http
    if args.command == "record-merge":
        return record_merge(args.sha, args.test, settings, http, git or run_git)
    sha = args.sha
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        try:
            sha = (git or run_git)(["rev-parse", "--verify", sha + "^{commit}"]).strip()
        except subprocess.CalledProcessError:
            print(f"refused: no commit {sha}")
            return 1
    return readcheck(sha, settings.url, publishable_key(environ, dotenv_path), http)


if __name__ == "__main__":
    sys.exit(main())
