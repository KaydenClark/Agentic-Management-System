"""Write RSI run and result rows to Supabase (S-006 TK-003).

Tables (migration ``*_rsi_rows.sql``): ``rsi_runs`` holds one arm of one round
at one pinned system version; ``rsi_results`` holds one trial of one task in a
run. Every row names provider, model, effort, arm, the runtime, controls and
skills commits, the grader version, its source and strength, and ``is_test``.
Results add task, split, trial, grade, cost, tokens, turns, wall time and
execution state. The site's publishable key reads only rows with
``is_test = false``.

Python API, for the S-002 runner::

    store = Store(settings.url, settings.key, urllib_http)
    run = store.insert(RUN_TABLE, {...})              # refused without skills_commit
    store.insert(RESULT_TABLE, result_for(run, task_id=..., split=..., ...))
    store.update(RUN_TABLE, run, {"state": "completed", "finished_at": ...})

``update`` sends the version it read and claims the next one; if the row has
changed since it was read the update is refused with ``Conflict`` and nothing
is written (ADR-002U). The database enforces the same rule with a trigger.

Command ``ams-rsi livecheck`` (service key, then publishable key) inserts one
test run and one test result, proves the writer and the database each refuse
a missing skills commit and a stale update, proves the site key sees neither
test row and cannot insert, update or delete on either table, then deletes the
test rows. It never writes a non-test row.

Keys load as in ``ams.keycheck``; no key value, HTTP error body or transport
error text is printed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from urllib.parse import quote

from ams import keycheck, writer

REPO_ROOT = keycheck.REPO_ROOT
RUN_TABLE = "rsi_runs"
RESULT_TABLE = "rsi_results"
PROVENANCE = ("arm", "provider", "model", "effort", "runtime_commit", "controls_commit",
              "skills_commit", "grader_version", "is_test")
ARMS = ("ams", "no_ams", "plain_instructions")
SPLITS = ("dev", "held_out")
RUN_STATES = ("running", "completed", "stopped", "failed")
EXECUTION_STATES = ("completed", "runner_error", "auth_error", "timeout", "capped")
STRENGTHS = ("recorded_fact", "anecdote", "single_trial", "repeated_trials",
             "held_out_with_interval")
SOURCE_KINDS = ("commit", "pr", "path", "jot")
BOOKKEEPING = ("id", "version", "recorded_at", "updated_at")
STALE = "PT409"
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_COLUMN = re.compile(r'column "([a-z_]+)"')


class Refused(Exception):
    """A write the writer or the database refused. The message holds no key or body text."""


class AlreadyRecorded(Refused):
    """The row's natural key (run_key, or run/task/trial) is already stored."""


class Conflict(Refused):
    """The row changed after it was read; nothing was written."""


# --- row checks ---------------------------------------------------------------


def _label(row, column):
    value = row.get(column)
    if not isinstance(value, str) or not value.strip():
        raise Refused(f"refused: {column} missing")


def _commit(row, column):
    _label(row, column)
    if not _COMMIT.match(row[column]):
        raise Refused(f"refused: {column} is not a full commit SHA")


def _choice(row, column, allowed):
    if row.get(column) not in allowed:
        raise Refused(f"refused: {column} must be one of {', '.join(allowed)}")


def _count(row, column, minimum=0):
    value = row.get(column)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < minimum:
        raise Refused(f"refused: {column} must be a number >= {minimum}")


def _common(row):
    _choice(row, "arm", ARMS)
    for column in ("provider", "model", "effort", "source_ref"):
        _label(row, column)
    # The skills pin first, so its absence is the reason given (ADR-002R).
    for column in ("skills_commit", "runtime_commit", "controls_commit", "grader_version"):
        _commit(row, column)
    _choice(row, "source_kind", SOURCE_KINDS)
    _choice(row, "strength", STRENGTHS)
    if not isinstance(row.get("is_test"), bool):
        raise Refused("refused: is_test must be true or false")


def check_run(row: Mapping) -> None:
    _common(row)
    _label(row, "run_key")
    _choice(row, "state", RUN_STATES)
    _label(row, "started_at")


def check_result(row: Mapping) -> None:
    _common(row)
    _count(row, "run_id", 1)
    _label(row, "task_id")
    _choice(row, "split", SPLITS)
    _count(row, "trial", 1)
    _choice(row, "execution_state", EXECUTION_STATES)
    for column in ("cost_usd", "input_tokens", "output_tokens", "turns", "wall_seconds"):
        _count(row, column)
    graded = row.get("passed") is not None or row.get("score") is not None
    if (row["execution_state"] == "completed") != graded:
        raise Refused("refused: only a completed trial carries passed or score")


CHECKS = {RUN_TABLE: check_run, RESULT_TABLE: check_result}


def result_for(run: Mapping, **fields) -> dict:
    """A result row that repeats its saved run's id and provenance."""
    row = {"run_id": run["id"], **{column: run.get(column) for column in PROVENANCE}}
    row.update(fields)
    return row


# --- the store ----------------------------------------------------------------


class Store:
    def __init__(self, url: str, key: str, http: writer.Http):
        self.url, self.http = url, http
        self._key = key

    def __repr__(self):
        return f"Store({self.url!r})"

    def _endpoint(self, table, **filters):
        if table not in CHECKS:
            raise Refused(f"refused: unknown table {table}")
        base = self.url.rstrip("/") + "/rest/v1/" + table
        query = "&".join(f"{k}=eq.{quote(str(v), safe='')}" for k, v in filters.items())
        return base + ("?" + query if query else "")

    def _send(self, method, url, payload=None):
        return writer._call(self.http, method, url, self._key, payload)

    def insert(self, table: str, row: Mapping) -> dict:
        url = self._endpoint(table)  # refuses an unknown table
        CHECKS[table](row)
        status, body = self._send("POST", url, dict(row))
        if status == 201 and isinstance(body, list) and body:
            return body[0]
        if status == 409 and _code(body) == "23505":
            raise AlreadyRecorded(f"already recorded in {table}")
        raise Refused(_failure("insert", status, body))

    def get(self, table: str, row_id: int) -> dict | None:
        status, body = self._send("GET", self._endpoint(table, id=row_id))
        if writer._ok(status) and isinstance(body, list):
            return body[0] if body else None
        raise Refused(_failure("read", status, body))

    def update(self, table: str, read: Mapping, changes: Mapping) -> dict:
        """Apply changes only if the row is still at the version that was read."""
        if table not in CHECKS:
            raise Refused(f"refused: unknown table {table}")
        for column in BOOKKEEPING:
            if column in changes:
                raise Refused(f"refused: {column} is set by the database")
        merged = {**read, **changes}
        merged.pop("id", None)
        CHECKS[table](merged)  # the row as it would stand after the update
        read_version = read["version"]
        payload = {**changes, "version": read_version + 1}
        url = self._endpoint(table, id=read["id"], version=read_version)
        status, body = self._send("PATCH", url, payload)
        if writer._ok(status) and isinstance(body, list) and body:
            return body[0]
        if writer._ok(status) and isinstance(body, list):
            current = self.get(table, read["id"])
            if current is None:
                raise Refused(f"refused: no {table} row {read['id']}")
            raise Conflict(f"stale: {table} row {read['id']} is at version "
                           f"{current['version']}, read at version {read_version}")
        if status == 409 and _code(body) == STALE:
            raise Conflict(f"stale: {table} row {read['id']} changed since version {read_version}")
        raise Refused(_failure("update", status, body))

    def delete_test_rows(self, table: str, **filters) -> int:
        """Delete test rows only; the filter always includes is_test=true."""
        status, body = self._send("DELETE", self._endpoint(table, is_test="true", **filters))
        if writer._ok(status) and isinstance(body, list):
            return len(body)
        raise Refused(_failure("delete", status, body))


def _code(body):
    return body.get("code") if isinstance(body, dict) else None


def _failure(verb, status, body):
    """Name the HTTP status, the SQLSTATE and a column; never echo the body."""
    parts = [f"{verb} failed: http status {status if status is not None else 'none'}"]
    code = _code(body)
    if isinstance(code, str) and re.fullmatch(r"[0-9A-Z]{5}|PGRST\d+", code):
        parts.append(f"code {code}")
    message = body.get("message") if isinstance(body, dict) else None
    column = _COLUMN.search(message) if isinstance(message, str) else None
    if column:
        parts.append(f"column {column.group(1)}")
    return ", ".join(parts)


# --- livecheck ----------------------------------------------------------------


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _probe_rows(head: str, run_key: str):
    run = {"run_key": run_key, "arm": "ams", "provider": "livecheck", "model": "livecheck",
           "effort": "none", "runtime_commit": head, "controls_commit": head,
           "skills_commit": head, "grader_version": head, "state": "running",
           "started_at": _now(), "source_kind": "commit", "source_ref": head,
           "strength": "anecdote", "is_test": True,
           "detail": {"purpose": "ams-rsi livecheck probe; deleted when the check ends"}}
    result = {"task_id": "livecheck", "split": "dev", "trial": 1,
              "execution_state": "completed", "passed": True, "cost_usd": 0,
              "input_tokens": 0, "output_tokens": 0, "turns": 0, "wall_seconds": 0,
              "source_kind": "commit", "source_ref": head, "strength": "anecdote"}
    return run, result


def livecheck(settings: keycheck.Settings, publishable: str, http: writer.Http, head: str) -> int:
    service = Store(settings.url, settings.key, http)
    site = Store(settings.url, publishable, http)
    run_key = f"livecheck-{uuid.uuid4().hex[:12]}"
    run_row, result_fields = _probe_rows(head, run_key)
    ok = True
    run = None
    try:
        run = service.insert(RUN_TABLE, run_row)
        result = service.insert(RESULT_TABLE, result_for(run, **result_fields))
        print(f"inserted test rows: run id={run['id']}, result id={result['id']} (is_test=true)")

        # 1. A missing skills commit: the writer refuses before sending, then the
        #    database refuses a raw insert that bypasses the writer.
        missing = result_for(run, **dict(result_fields, trial=2))
        missing.pop("skills_commit")
        try:
            service.insert(RESULT_TABLE, missing)
            ok = False
            print("missing skills_commit: ACCEPTED by the writer")
        except Refused:
            print("missing skills_commit: refused by the writer")
        status, body = service._send("POST", service._endpoint(RESULT_TABLE), missing)
        if status is not None and 400 <= status < 500 and _code(body) == "23502" \
                and "skills_commit" in _failure("insert", status, body):
            print("missing skills_commit: refused by the database (code 23502, column skills_commit)")
        elif writer._ok(status):
            ok = False
            print("missing skills_commit: ACCEPTED by the database")
        else:
            ok = False
            print(f"missing skills_commit: inconclusive ({_failure('insert', status, body)})")

        # 2. A stale update: two readers of version 1; the second write is refused
        #    by the writer, and a raw PATCH claiming a stale version by the database.
        first = service.get(RESULT_TABLE, result["id"])
        second = service.get(RESULT_TABLE, result["id"])
        winner = service.update(RESULT_TABLE, first, {"passed": False})
        try:
            service.update(RESULT_TABLE, second, {"passed": True})
            ok = False
            print("stale update: ACCEPTED by the writer")
        except Conflict:
            print("stale update: refused by the writer")
        status, body = service._send("PATCH", service._endpoint(RESULT_TABLE, id=result["id"]),
                                     {"passed": True, "version": second["version"] + 1})
        if status == 409 and _code(body) == STALE:
            print("stale update: refused by the database (http status 409, code PT409)")
        elif writer._ok(status):
            ok = False
            print("stale update: ACCEPTED by the database")
        else:
            ok = False
            print(f"stale update: inconclusive ({_failure('update', status, body)})")
        unchanged = service.get(RESULT_TABLE, result["id"]) == winner
        ok = ok and unchanged
        print(f"row unchanged: {'yes' if unchanged else 'no'}")

        # 3. The site key: test rows invisible, every client write refused.
        seen = []
        for table, filters in ((RUN_TABLE, {"id": run["id"]}), (RESULT_TABLE, {"run_id": run["id"]})):
            total = len(_rows(service, table, filters))
            visible = len(_rows(site, table, filters))
            seen.append((visible, total))
            ok = ok and visible == 0 and total > 0
        print(f"site key sees test rows: {seen[0][0]} of {seen[0][1]} runs, "
              f"{seen[1][0]} of {seen[1][1]} results")
        probes = {RUN_TABLE: (dict(run_row, run_key=run_key + "-client"), run["id"]),
                  RESULT_TABLE: (result_for(run, **dict(result_fields, trial=3)), result["id"])}
        for table, (insert_row, row_id) in probes.items():
            for verb, method, url, payload in (
                    ("insert", "POST", site._endpoint(table), insert_row),
                    ("update", "PATCH", site._endpoint(table, id=row_id),
                     {"detail": {"client": "write probe"}}),
                    ("delete", "DELETE", site._endpoint(table, id=row_id), None)):
                status, body = site._send(method, url, payload)
                shown = status if status is not None else "none"
                if writer._denied(status, body):
                    print(f"{table} {verb}: refused (http status {shown})")
                else:
                    ok = False
                    label = "ACCEPTED" if writer._ok(status) else "inconclusive"
                    print(f"{table} {verb}: {label} (http status {shown})")
    except Refused as error:
        ok = False
        print(str(error))
    finally:
        ok = _cleanup(service, run, run_key) and ok
    return 0 if ok else 1


def _rows(store: Store, table, filters):
    """Rows from a successful query; an error, timeout or malformed body is refused,
    never read as an empty result."""
    status, body = store._send("GET", store._endpoint(table, **filters))
    if writer._ok(status) and isinstance(body, list):
        return body
    raise Refused(_failure(f"{table} read", status, body))


def _cleanup(service: Store, run, run_key) -> bool:
    try:
        runs = _rows(service, RUN_TABLE, {"run_key": run_key})
        results = sum(service.delete_test_rows(RESULT_TABLE, run_id=r["id"]) for r in runs)
        deleted = service.delete_test_rows(RUN_TABLE, run_key=run_key)
        left = len(_rows(service, RUN_TABLE, {"run_key": run_key}))
        left += sum(len(_rows(service, RESULT_TABLE, {"run_id": r["id"]})) for r in runs)
    except Refused as error:
        print(f"cleanup: {error}")
        return False
    print(f"cleanup: deleted {results} results, {deleted} runs; remaining {left}")
    return left == 0


def main(
    argv: list[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    dotenv_path: Path | None = None,
    http: writer.Http | None = None,
    git: writer.Git | None = None,
) -> int:
    parser = argparse.ArgumentParser(prog="ams-rsi", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("livecheck", help="prove the RSI tables' rules with test rows, then delete them")
    parser.parse_args(argv)

    environ = os.environ if environ is None else environ
    dotenv_path = keycheck.DOTENV_PATH if dotenv_path is None else dotenv_path
    settings = keycheck.load_settings(environ, dotenv_path)
    if settings.key is None:
        print("loaded: no")
        return 1
    if keycheck.key_format(settings.key) == "unrecognized":
        print("loaded: yes\nformat: unrecognized")
        return 1
    try:
        head = (git or writer.run_git)(["rev-parse", "HEAD"]).strip()
    except subprocess.CalledProcessError:
        print("refused: no HEAD commit")
        return 1
    if not _COMMIT.match(head):
        print("refused: HEAD is not a full commit SHA")
        return 1
    return livecheck(settings, writer.publishable_key(environ, dotenv_path), http or writer.urllib_http,
                     head)


if __name__ == "__main__":
    sys.exit(main())
