"""Tests for the source and strength rules on every table the site reads (S-006 TK-005).

Keys are fake and no test reaches Supabase: a small in-memory PostgREST enforces
the migrations' source rules (not-null source kind and ref, a non-blank ref, the
closed strength and source-kind lists) and hides test rows from the publishable
key. The live check runs only with AMS_LIVE=1 (see the end).
"""

import json
import os
import random
import re
import string
import urllib.parse
from pathlib import Path

import pytest

from ams import build_history, rsi_rows, source_rules, writer

URL = "https://example-project.supabase.co"
_rng = random.Random(20261105)
_ALPHA = string.ascii_letters + string.digits
FAKE_SECRET = "sb_secret_" + "".join(_rng.choice(_ALPHA) for _ in range(40))
FAKE_PUBLISHABLE = "sb_publishable_" + "".join(_rng.choice(_ALPHA) for _ in range(30))
HEAD = "a8e253b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6"
ENV = {"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET,
       "SUPABASE_PUBLISHABLE_KEY": FAKE_PUBLISHABLE}
TABLES = ("build_events", "rsi_runs", "rsi_results")
GOOD_SOURCE = {"source_kind": "path", "source_ref": "evals/runs/one.json",
               "strength": "single_trial"}


class FakePostgrest:
    """PostgREST plus the migrations' source rules, for all three site tables."""

    def __init__(self, *, enforce_sources=True, hide_test_rows=True):
        self.tables = {table: {} for table in TABLES}
        self.next_id = 1
        self.enforce_sources = enforce_sources
        self.hide_test_rows = hide_test_rows
        self.calls = []

    def __call__(self, method, url, headers, body):
        self.calls.append((method, url, dict(headers), body))
        parsed = urllib.parse.urlsplit(url)
        table = parsed.path.rsplit("/", 1)[-1]
        filters = {k: v[0][3:] for k, v in urllib.parse.parse_qs(parsed.query).items()
                   if k not in ("select", "on_conflict")}
        rows = self.tables[table]
        anon = headers["apikey"] == FAKE_PUBLISHABLE
        if anon and method != "GET":
            return 401, json.dumps({"code": "42501"}).encode()
        payload = json.loads(body) if body else None

        def value(row, key):
            if key.startswith("detail->>"):
                return (row.get("detail") or {}).get(key[len("detail->>"):])
            return row.get(key)

        match = [r for r in rows.values()
                 if all(str(value(r, k)).lower() == v.lower() for k, v in filters.items())]
        if method == "GET":
            if anon and self.hide_test_rows:
                match = [r for r in match if not r["is_test"]]
            return 200, json.dumps(match).encode()
        if method == "POST":
            if self.enforce_sources:
                for col in ("source_kind", "source_ref", "strength"):
                    if payload.get(col) is None:
                        message = f'null value in column "{col}" of relation "{table}"'
                        return 400, json.dumps({"code": "23502", "message": message}).encode()
                if (not payload["source_ref"].strip()
                        or payload["strength"] not in source_rules.STRENGTHS
                        or payload["source_kind"] not in source_rules.SOURCE_KINDS):
                    return 400, json.dumps({"code": "23514", "message": "check"}).encode()
            row = dict(payload, id=self.next_id, version=1)
            row.setdefault("is_test", False)
            self.next_id += 1
            rows[row["id"]] = row
            return 201, json.dumps([row]).encode()
        if method == "DELETE":
            for row in match:
                del rows[row["id"]]
            return 200, json.dumps(match).encode()
        raise AssertionError(method)


def assert_no_key(text, key):
    for size in range(len(key) - 1, 12, -1):
        for start in range(0, len(key) - size + 1):
            assert key[start : start + size] not in text


# --- one closed list, one source rule -----------------------------------------


def test_the_closed_strength_list_keeps_recorded_fact_and_the_four_trial_labels():
    assert source_rules.STRENGTHS == ("recorded_fact", "anecdote", "single_trial",
                                      "repeated_trials", "held_out_with_interval")
    assert rsi_rows.STRENGTHS is source_rules.STRENGTHS
    assert rsi_rows.SOURCE_KINDS is source_rules.SOURCE_KINDS
    assert build_history.SOURCE_KINDS is source_rules.SOURCE_KINDS


@pytest.mark.parametrize("changes,column", [
    ({"source_kind": None, "source_ref": None}, "source_kind"),
    ({"source_kind": "web"}, "source_kind"),
    ({"source_ref": None}, "source_ref"),
    ({"source_ref": "  "}, "source_ref"),
    ({"source_url": "http://example.com"}, "source_url"),
    ({"strength": None}, "strength"),
    ({"strength": "vibes"}, "strength"),
    ({"strength": "Anecdote"}, "strength"),
])
def test_a_row_without_a_source_or_with_an_unlisted_strength_is_refused(changes, column):
    with pytest.raises(ValueError, match=column):
        source_rules.check_source({**GOOD_SOURCE, **changes})


def test_a_url_alone_is_not_a_source():
    row = {"source_url": "https://github.com/x/y/pull/1", "strength": "anecdote"}
    with pytest.raises(ValueError, match="source_kind"):
        source_rules.check_source(row)


@pytest.mark.parametrize("strength", ["recorded_fact", "anecdote", "single_trial",
                                      "repeated_trials", "held_out_with_interval"])
def test_every_listed_strength_with_a_source_is_accepted(strength):
    source_rules.check_source({**GOOD_SOURCE, "strength": strength,
                               "source_url": "https://github.com/x"})


# --- every writer applies it before sending -----------------------------------


def _event(**changes):
    row = {"kind": "probe", "subject": "s", "summary": "s", "occurred_at": "2026-11-01T00:00:00Z",
           "source_kind": "path", "source_ref": "a/b.md", "strength": "anecdote",
           "is_test": True, "detail": {}}
    row.update(changes)
    return row


@pytest.mark.parametrize("changes", [{"source_ref": ""}, {"source_kind": None},
                                     {"strength": "vibes"}])
def test_the_build_event_writer_refuses_before_sending(changes):
    http = FakePostgrest()
    with pytest.raises(ValueError):
        writer.insert_event(URL, FAKE_SECRET, http, _event(**changes))
    assert http.calls == []


def test_the_build_event_writer_sends_a_sourced_row():
    http = FakePostgrest()
    status, body = writer.insert_event(URL, FAKE_SECRET, http, _event())
    assert status == 201 and body[0]["source_ref"] == "a/b.md"


@pytest.mark.parametrize("table", ["rsi_runs", "rsi_results"])
@pytest.mark.parametrize("changes,column", [({"source_ref": ""}, "source_ref"),
                                            ({"source_kind": None}, "source_kind"),
                                            ({"strength": "vibes"}, "strength")])
def test_the_rsi_writer_refuses_before_sending(table, changes, column):
    run, result = rsi_rows._probe_rows(HEAD, "k")
    row = run if table == "rsi_runs" else rsi_rows.result_for(dict(run, id=1), **result)
    http = FakePostgrest()
    with pytest.raises(rsi_rows.Refused, match=column):
        rsi_rows.Store(URL, FAKE_SECRET, http).insert(table, {**row, **changes})
    assert http.calls == []


def test_the_history_importer_applies_the_shared_rule():
    good = {"kind": "commit", "subject": "s", "summary": "s",
            "occurred_at": "2026-11-01T00:00:00Z", "source_kind": "commit", "source_ref": HEAD,
            "source_url": "https://github.com/x", "strength": "recorded_fact", "is_test": False}
    build_history.validate(good)
    with pytest.raises(ValueError, match="source_kind"):
        build_history.validate(dict(good, source_kind="web"))


# --- every migration matches the list ----------------------------------------


def _migrations():
    folder = Path(source_rules.REPO_ROOT, "supabase", "migrations")
    return "\n".join(p.read_text().lower() for p in sorted(folder.glob("*.sql")))


def test_the_database_lists_match_the_writer_lists():
    sql = _migrations()
    for domain, values in (("ams_strength", source_rules.STRENGTHS),
                           ("ams_source_kind", source_rules.SOURCE_KINDS)):
        body = re.search(rf"create domain public\.{domain} as text\s+check \(value in \((.*?)\)\)",
                         sql, re.S)
        assert body, domain
        listed = tuple(re.findall(r"'([a-z_]+)'", body.group(1)))
        assert listed == values, domain


@pytest.mark.parametrize("table", TABLES)
def test_every_site_table_requires_a_source_and_strength_and_hides_test_rows(table):
    sql = _migrations()
    body = re.search(rf"create table public\.{table} \((.*?)\n\);", sql, re.S).group(1)
    assert re.search(r"^\s*source_kind\s+public\.ams_source_kind not null", body, re.M)
    assert re.search(r"^\s*source_ref\s+\S+ not null", body, re.M)
    assert re.search(r"^\s*strength\s+public\.ams_strength not null", body, re.M)
    assert re.search(r"^\s*is_test\s+boolean not null", body, re.M)
    assert re.search(rf"create policy \w+ on public\.{table}\s+for select to anon, "
                     r"authenticated\s+using \(not is_test\);", sql)


# --- livecheck ---------------------------------------------------------------


def livecheck(capsys, http, env=ENV):
    code = source_rules.main(["livecheck"], environ=env, dotenv_path=Path("/nonexistent/ams"),
                             http=http, git=lambda args: HEAD + "\n")
    out, err = capsys.readouterr()
    return code, out, err


def test_livecheck_proves_every_refusal_and_hidden_test_row_then_leaves_nothing(capsys):
    http = FakePostgrest()
    code, out, err = livecheck(capsys, http)
    assert code == 0, out
    for table in TABLES:
        for case in ("no source", "blank source_ref", "strength vibes"):
            assert f"{table} {case}: refused by the writer" in out
            assert re.search(rf"{table} {case}: refused by the database \(code 235(02|14)", out)
        assert f"{table} test rows: service key sees 1, site key sees 0" in out
    assert "cleanup: remaining 0" in out
    assert http.tables == {table: {} for table in TABLES}
    for method, url, headers, body in http.calls:
        if method == "POST":
            assert json.loads(body)["is_test"] is True
    assert_no_key(out + err, FAKE_SECRET)
    assert_no_key(out + err, FAKE_PUBLISHABLE)


@pytest.mark.parametrize("broken,flag", [
    ("enforce_sources", "build_events no source: ACCEPTED by the database"),
    ("hide_test_rows", "rsi_results test rows: service key sees 1, site key sees 1"),
])
def test_livecheck_fails_when_a_rule_is_not_enforced_and_still_cleans_up(capsys, broken, flag):
    http = FakePostgrest(**{broken: False})
    code, out, _ = livecheck(capsys, http)
    assert code == 1
    assert flag in out
    assert "cleanup: remaining 0" in out
    assert http.tables == {table: {} for table in TABLES}


def test_livecheck_without_the_service_key_sends_nothing(capsys):
    http = FakePostgrest()
    env = {k: v for k, v in ENV.items() if k != "SUPABASE_SERVICE_ROLE_KEY"}
    code, out, _ = livecheck(capsys, http, env=env)
    assert code == 1 and "loaded: no" in out and http.calls == []


@pytest.mark.skipif(os.environ.get("AMS_LIVE") != "1", reason="set AMS_LIVE=1 for the live check")
def test_live_livecheck(capsys):
    assert source_rules.main(["livecheck"]) == 0
    assert "cleanup: remaining 0" in capsys.readouterr().out
