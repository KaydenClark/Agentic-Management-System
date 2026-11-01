"""Source and strength rules for every table the site reads (S-006 TK-005).

A row in ``build_events``, ``rsi_runs`` or ``rsi_results`` must name its source,
as a ``source_kind`` from ``SOURCE_KINDS`` plus a non-blank ``source_ref`` (a
``source_url``, when given, links it and must be https; a URL alone is not a
source), and a ``strength`` from the closed list ``STRENGTHS``. Every writer
(``ams-writer``, ``ams-history``, ``ams-rsi``) applies ``check_source`` before
sending, and the migrations enforce the same lists as the ``ams_strength`` and
``ams_source_kind`` domains. ``recorded_fact`` is a row taken directly from a
Git, GitHub or record file; the four trial labels grade RSI evidence.

``is_test`` marks test and synthetic rows; the site's read policy on each table
returns only ``not is_test``.

Command ``ams-sources livecheck`` (service key, then publishable key) inserts
one marked test row per table, proves the writer and the database each refuse a
row with no source, a blank source_ref and an unlisted strength, proves the
site key sees none of the test rows, then deletes every probe row and confirms
none remain. It never writes a non-test row. No key value or HTTP body is
printed.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from urllib.parse import quote

from ams import keycheck

REPO_ROOT = keycheck.REPO_ROOT
STRENGTHS = ("recorded_fact", "anecdote", "single_trial", "repeated_trials",
             "held_out_with_interval")
SOURCE_KINDS = ("commit", "pr", "path", "jot")
TABLES = ("build_events", "rsi_runs", "rsi_results")
REFUSED_CODES = ("23502", "23514")  # not-null and check violations


def check_source(row: Mapping) -> None:
    """Raise ValueError unless the row names a source and a listed strength."""
    if row.get("source_kind") not in SOURCE_KINDS:
        raise ValueError(f"refused: source_kind must be one of {', '.join(SOURCE_KINDS)}")
    ref = row.get("source_ref")
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError("refused: source_ref missing")
    url = row.get("source_url")
    if url is not None and not (isinstance(url, str) and url.startswith("https://")):
        raise ValueError("refused: source_url must be an https link")
    if row.get("strength") not in STRENGTHS:
        raise ValueError(f"refused: strength must be one of {', '.join(STRENGTHS)}")


# --- livecheck ----------------------------------------------------------------

BAD_CASES = (("no source", {"source_kind": None, "source_ref": None}),
             ("blank source_ref", {"source_ref": " "}),
             ("strength vibes", {"strength": "vibes"}))


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _url(base: str, table: str, **filters) -> str:
    query = "&".join(f"{k}=eq.{quote(str(v), safe='')}" for k, v in filters.items())
    return base.rstrip("/") + "/rest/v1/" + table + ("?" + query if query else "")


def livecheck(settings: keycheck.Settings, publishable: str, http, head: str) -> int:
    from ams import rsi_rows, writer

    tag = "sources-" + uuid.uuid4().hex[:12]
    marker = {"probe": tag, "purpose": "ams-sources livecheck probe; deleted when the check ends"}
    service = rsi_rows.Store(settings.url, settings.key, http)

    def send(key, method, url, payload=None):
        return writer._call(http, method, url, key, payload)

    event = {"kind": "probe", "subject": "ams-sources livecheck", "summary": "test row",
             "occurred_at": _now(), "source_kind": "path", "source_ref": f"livecheck/{tag}",
             "strength": "anecdote", "is_test": True, "detail": marker}
    run_row, result_fields = rsi_rows._probe_rows(head, tag)
    run_row["detail"] = marker
    result_fields["detail"] = marker
    ok = True
    try:
        status, _ = writer.insert_event(settings.url, settings.key, http, event)
        if status != 201:
            raise rsi_rows.Refused(f"build_events insert failed: http status "
                                   f"{status if status is not None else 'none'}")
        run = service.insert(rsi_rows.RUN_TABLE, run_row)
        service.insert(rsi_rows.RESULT_TABLE, rsi_rows.result_for(run, **result_fields))

        def good(table, n):
            if table == "build_events":
                return dict(event, source_ref=f"livecheck/{tag}/{n}")
            if table == "rsi_runs":
                return dict(run_row, run_key=f"{tag}-{n}")
            return rsi_rows.result_for(run, **dict(result_fields, trial=10 + n))

        writers = {"build_events": lambda row: writer.insert_event(settings.url, settings.key,
                                                                    http, row),
                   "rsi_runs": lambda row: service.insert(rsi_rows.RUN_TABLE, row),
                   "rsi_results": lambda row: service.insert(rsi_rows.RESULT_TABLE, row)}
        for table in TABLES:
            for n, (case, changes) in enumerate(BAD_CASES, start=1):
                row = {**good(table, n), **changes}
                try:
                    writers[table](row)
                except (ValueError, rsi_rows.Refused):
                    print(f"{table} {case}: refused by the writer")
                else:
                    ok = False
                    print(f"{table} {case}: ACCEPTED by the writer")
                status, body = send(settings.key, "POST", _url(settings.url, table), row)
                code = body.get("code") if isinstance(body, dict) else None
                if status is not None and 400 <= status < 500 and code in REFUSED_CODES:
                    print(f"{table} {case}: refused by the database (code {code})")
                else:
                    ok = False
                    label = "ACCEPTED" if writer._ok(status) else "inconclusive"
                    print(f"{table} {case}: {label} by the database "
                          f"(http status {status if status is not None else 'none'})")
        for table in TABLES:
            seen = []
            for key in (settings.key, publishable):
                status, body = send(key, "GET", _url(settings.url, table,
                                                     **{"detail->>probe": tag}))
                if not (writer._ok(status) and isinstance(body, list)):
                    raise rsi_rows.Refused(f"{table} read failed: http status "
                                           f"{status if status is not None else 'none'}")
                seen.append(len(body))
            print(f"{table} test rows: service key sees {seen[0]}, site key sees {seen[1]}")
            ok = ok and seen[0] >= 1 and seen[1] == 0
    except (ValueError, rsi_rows.Refused) as error:
        ok = False
        print(str(error))
    finally:
        ok = _cleanup(settings, http, tag) and ok
    return 0 if ok else 1


def _cleanup(settings, http, tag) -> bool:
    """Delete every probe row, results before runs, test rows only."""
    from ams import writer

    left = 0
    try:
        for table in ("rsi_results", "rsi_runs", "build_events"):
            status, _ = writer._call(http, "DELETE", _url(settings.url, table, is_test="true",
                                                          **{"detail->>probe": tag}),
                                     settings.key)
            if not writer._ok(status):
                raise ValueError(f"{table} delete failed")
        for table in TABLES:
            status, body = writer._call(http, "GET", _url(settings.url, table,
                                                          **{"detail->>probe": tag}),
                                        settings.key)
            if not (writer._ok(status) and isinstance(body, list)):
                raise ValueError(f"{table} read failed")
            left += len(body)
    except ValueError as error:
        print(f"cleanup: {error}")
        return False
    print(f"cleanup: remaining {left}")
    return left == 0


def main(argv: list[str] | None = None, *, environ: Mapping[str, str] | None = None,
         dotenv_path: Path | None = None, http=None, git=None) -> int:
    from ams import writer

    parser = argparse.ArgumentParser(prog="ams-sources", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("livecheck", help="prove the source and test-row rules on every site table")
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
    return livecheck(settings, writer.publishable_key(environ, dotenv_path),
                     http or writer.urllib_http, head)


if __name__ == "__main__":
    sys.exit(main())
