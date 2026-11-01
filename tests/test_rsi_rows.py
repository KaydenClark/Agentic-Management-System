"""Tests for the RSI run and result rows writer (S-006 TK-003).

Keys here are fake and no test reaches Supabase: a small in-memory PostgREST
stands in for the database and enforces the migration's contract (not-null
provenance, the run/result provenance link, the version guard, client
read-only access and hidden test rows). The live check runs only with
AMS_LIVE=1 (see the end).
"""

import json
import os
import random
import re
import string
import urllib.parse
from pathlib import Path

import pytest

from ams import rsi_rows

URL = "https://example-project.supabase.co"
_rng = random.Random(20261103)
_ALPHA = string.ascii_letters + string.digits
FAKE_SECRET = "sb_secret_" + "".join(_rng.choice(_ALPHA) for _ in range(40))
FAKE_PUBLISHABLE = "sb_publishable_" + "".join(_rng.choice(_ALPHA) for _ in range(30))
HEAD = "a8e253b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6"
SKILLS = "5f1e2d3c4b5a69788796a5b4c3d2e1f0a9b8c7d6"
ENV = {"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET,
       "SUPABASE_PUBLISHABLE_KEY": FAKE_PUBLISHABLE}

RUN_REQUIRED = ("run_key", "arm", "provider", "model", "effort", "runtime_commit",
                "controls_commit", "skills_commit", "grader_version", "state", "started_at",
                "source_kind", "source_ref", "strength", "is_test")
RESULT_REQUIRED = ("run_id", "arm", "provider", "model", "effort", "runtime_commit",
                   "controls_commit", "skills_commit", "grader_version", "task_id", "split",
                   "trial", "execution_state", "cost_usd", "input_tokens", "output_tokens",
                   "turns", "wall_seconds", "source_kind", "source_ref", "strength", "is_test")


class FakePostgrest:
    """Enough of PostgREST plus the migration's rules to exercise the writer."""

    def __init__(self, *, enforce_not_null=True, guard_versions=True, hide_test_rows=True,
                 anon_inserts_runs=False):
        self.tables = {"rsi_runs": {}, "rsi_results": {}}
        self.next_id = 1
        self.enforce_not_null = enforce_not_null
        self.guard_versions = guard_versions
        self.hide_test_rows = hide_test_rows
        self.anon_inserts_runs = anon_inserts_runs
        self.calls = []

    def __call__(self, method, url, headers, body):
        self.calls.append((method, url, dict(headers), body))
        parsed = urllib.parse.urlsplit(url)
        table = parsed.path.rsplit("/", 1)[-1]
        filters = {k: v[0][3:] for k, v in urllib.parse.parse_qs(parsed.query).items()
                   if k != "select"}
        rows = self.tables[table]
        anon = headers["apikey"] == FAKE_PUBLISHABLE
        payload = json.loads(body) if body else None
        anon_insert = self.anon_inserts_runs and method == "POST" and table == "rsi_runs"
        if anon and method != "GET" and not anon_insert:
            return 401, json.dumps({"code": "42501"}).encode()
        match = [r for r in rows.values()
                 if all(str(r.get(k)).lower() == v.lower() for k, v in filters.items())]
        if method == "GET":
            if anon and self.hide_test_rows:
                match = [r for r in match if not r["is_test"]]
            return 200, json.dumps(match).encode()
        if method == "POST":
            required = RUN_REQUIRED if table == "rsi_runs" else RESULT_REQUIRED
            for col in required:
                if self.enforce_not_null and payload.get(col) is None:
                    message = f'null value in column "{col}" of relation "{table}" violates not-null constraint'
                    return 400, json.dumps({"code": "23502", "message": message}).encode()
            link = ("run_id", *rsi_rows.PROVENANCE)
            # A composite foreign key is MATCH SIMPLE: a null column skips the check.
            if table == "rsi_results" and all(payload.get(c) is not None for c in link):
                run = self.tables["rsi_runs"].get(payload.get("run_id"))
                if run is None or any(run[c] != payload.get(c) for c in rsi_rows.PROVENANCE):
                    return 409, json.dumps({"code": "23503"}).encode()
            row = dict(payload, id=self.next_id, version=1)
            self.next_id += 1
            rows[row["id"]] = row
            return 201, json.dumps([row]).encode()
        if method == "PATCH":
            out = []
            for row in match:
                if self.guard_versions and payload.get("version") != row["version"] + 1:
                    return 409, json.dumps({"code": "PT409", "message": "stale update"}).encode()
                row.update(payload)
                if not self.guard_versions:
                    row["version"] = payload.get("version", row["version"])
                out.append(dict(row))
            return 200, json.dumps(out).encode()
        if method == "DELETE":
            if table == "rsi_runs":
                for row in match:
                    if any(r["run_id"] == row["id"] for r in self.tables["rsi_results"].values()):
                        return 409, json.dumps({"code": "23503"}).encode()
            for row in match:
                del rows[row["id"]]
            return 200, json.dumps(match).encode()
        raise AssertionError(method)


def store(http):
    return rsi_rows.Store(URL, FAKE_SECRET, http)


def a_run(**changes):
    row = {
        "run_key": "trial-run-1", "arm": "ams", "provider": "anthropic",
        "model": "claude-opus-5-5", "effort": "high", "runtime_commit": HEAD,
        "controls_commit": HEAD, "skills_commit": SKILLS, "grader_version": HEAD,
        "state": "running", "started_at": "2026-11-01T13:00:00Z", "source_kind": "path",
        "source_ref": "evals/runs/trial-run-1.json", "strength": "single_trial", "is_test": True,
    }
    row.update(changes)
    return row


def a_result(run, **changes):
    fields = {"task_id": "EV-001", "split": "dev", "trial": 1, "execution_state": "completed",
              "passed": True, "cost_usd": 0.42, "input_tokens": 1200, "output_tokens": 300,
              "turns": 4, "wall_seconds": 61.5, "source_kind": "path",
              "source_ref": "evals/runs/trial-run-1.json", "strength": "single_trial"}
    fields.update(changes)
    return rsi_rows.result_for(run, **fields)


def assert_no_key(text, key):
    for size in range(len(key) - 1, 12, -1):
        for start in range(0, len(key) - size + 1):
            assert key[start : start + size] not in text


# --- the writer refuses a missing skills commit before sending ----------------


@pytest.mark.parametrize("missing", [None, "", "   ", "absent"])
def test_result_without_skills_commit_is_refused_and_nothing_is_sent(missing):
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    row = a_result(run)
    if missing == "absent":
        del row["skills_commit"]
    else:
        row["skills_commit"] = missing
    sent_before = len(http.calls)
    with pytest.raises(rsi_rows.Refused, match="skills_commit"):
        store(http).insert(rsi_rows.RESULT_TABLE, row)
    assert len(http.calls) == sent_before


def test_run_without_skills_commit_is_refused_and_nothing_is_sent():
    http = FakePostgrest()
    with pytest.raises(rsi_rows.Refused, match="skills_commit"):
        store(http).insert(rsi_rows.RUN_TABLE, a_run(skills_commit=None))
    assert http.calls == []


@pytest.mark.parametrize("field,value", [
    ("skills_commit", "main"), ("runtime_commit", "abc123"), ("grader_version", None),
    ("arm", "baseline"), ("provider", ""), ("model", None), ("effort", " "),
    ("strength", "vibes"), ("source_ref", ""), ("is_test", None),
])
def test_run_with_a_bad_provenance_field_is_refused(field, value):
    with pytest.raises(rsi_rows.Refused, match=field):
        rsi_rows.check_run(a_run(**{field: value}))


@pytest.mark.parametrize("changes", [
    {"split": "test"}, {"trial": 0}, {"task_id": ""}, {"cost_usd": -1},
    {"input_tokens": None}, {"execution_state": "done"},
    {"execution_state": "completed", "passed": None},
    {"execution_state": "runner_error", "passed": False},
])
def test_result_with_a_bad_field_is_refused(changes):
    run = dict(a_run(), id=1, version=1)
    with pytest.raises(rsi_rows.Refused):
        rsi_rows.check_result(a_result(run, **changes))


def test_a_runner_error_is_a_row_with_no_grade():
    run = dict(a_run(), id=1, version=1)
    rsi_rows.check_result(a_result(run, execution_state="runner_error", passed=None))


def test_a_score_alone_does_not_grade_a_completed_trial():
    # Review L2: pass rate and cost per pass need a pass (ADR-002J); score is optional detail.
    run = dict(a_run(), id=1, version=1)
    with pytest.raises(rsi_rows.Refused, match="passed"):
        rsi_rows.check_result(a_result(run, passed=None, score=0.75))
    rsi_rows.check_result(a_result(run, passed=True, score=0.75))
    with pytest.raises(rsi_rows.Refused, match="score"):
        rsi_rows.check_result(a_result(run, execution_state="runner_error", passed=None,
                                       score=0.5))


def test_the_database_requires_passed_on_a_completed_trial():
    sql = re.sub(r"\(\s+", "(", re.sub(r"\s+", " ", _all_migrations()))
    assert "drop constraint rsi_results_graded_when_completed" in sql
    assert ("add constraint rsi_results_passed_when_completed check "
            "((execution_state = 'completed') = (passed is not null))") in sql
    assert ("add constraint rsi_results_score_when_completed check "
            "(score is null or execution_state = 'completed')") in sql


def test_all_three_arms_and_both_splits_are_accepted():
    for arm in ("ams", "no_ams", "plain_instructions"):
        run = dict(a_run(arm=arm), id=1, version=1)
        rsi_rows.check_run(run)
        for split in ("dev", "held_out"):
            rsi_rows.check_result(a_result(run, split=split))


# --- inserts ------------------------------------------------------------------


def test_insert_posts_with_the_service_key_and_returns_the_saved_row():
    http = FakePostgrest()
    saved = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    method, url, headers, body = http.calls[0]
    assert (method, url) == ("POST", URL + "/rest/v1/rsi_runs")
    assert headers["apikey"] == FAKE_SECRET and headers["Prefer"] == "return=representation"
    assert json.loads(body)["skills_commit"] == SKILLS
    assert saved["id"] == 1 and saved["version"] == 1


def test_result_for_copies_the_run_provenance():
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run(arm="no_ams"))
    row = a_result(run)
    assert row["run_id"] == run["id"]
    for column in rsi_rows.PROVENANCE:
        assert row[column] == run[column]
    saved = store(http).insert(rsi_rows.RESULT_TABLE, row)
    assert saved["arm"] == "no_ams" and saved["skills_commit"] == SKILLS


def test_a_database_refusal_names_the_column_and_code_only():
    def refuse(method, url, headers, body):
        message = 'null value in column "skills_commit" of relation "rsi_results" ' + FAKE_SECRET
        return 400, json.dumps({"code": "23502", "message": message}).encode()

    with pytest.raises(rsi_rows.Refused) as caught:
        store(refuse).insert(rsi_rows.RUN_TABLE, a_run())
    text = str(caught.value)
    assert "23502" in text and "skills_commit" in text
    assert_no_key(text, FAKE_SECRET)


def test_a_duplicate_insert_is_reported_as_already_recorded():
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    store(http).insert(rsi_rows.RESULT_TABLE, a_result(run))
    dup = lambda m, u, h, b: (409, json.dumps({"code": "23505"}).encode())
    with pytest.raises(rsi_rows.AlreadyRecorded):
        store(dup).insert(rsi_rows.RESULT_TABLE, a_result(run))


def test_a_transport_error_is_refused_without_its_text():
    def boom(method, url, headers, body):
        raise OSError("connection reset " + FAKE_SECRET)

    with pytest.raises(rsi_rows.Refused) as caught:
        store(boom).insert(rsi_rows.RUN_TABLE, a_run())
    assert_no_key(str(caught.value), FAKE_SECRET)


# --- stale updates are refused ------------------------------------------------


def test_update_names_the_version_it_read_and_claims_the_next():
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    saved = store(http).update(rsi_rows.RUN_TABLE, run, {"state": "completed"})
    method, url, headers, body = http.calls[-1]
    assert method == "PATCH"
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
    assert query["id"] == ["eq.1"] and query["version"] == ["eq.1"]
    assert json.loads(body) == {"state": "completed", "version": 2}
    assert saved["state"] == "completed" and saved["version"] == 2


def test_an_update_against_a_row_changed_since_it_was_read_is_refused():
    http = FakePostgrest()
    s = store(http)
    run = s.insert(rsi_rows.RUN_TABLE, a_run())
    first = s.get(rsi_rows.RUN_TABLE, run["id"])
    second = s.get(rsi_rows.RUN_TABLE, run["id"])
    winner = s.update(rsi_rows.RUN_TABLE, first, {"state": "completed"})
    with pytest.raises(rsi_rows.Conflict, match="version 2"):
        s.update(rsi_rows.RUN_TABLE, second, {"state": "failed"})
    assert s.get(rsi_rows.RUN_TABLE, run["id"]) == winner


def test_a_database_version_refusal_is_a_conflict():
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    stale = lambda m, u, h, b: (409, json.dumps({"code": "PT409"}).encode())
    with pytest.raises(rsi_rows.Conflict):
        store(stale).update(rsi_rows.RUN_TABLE, run, {"state": "completed"})


def test_an_update_of_a_missing_row_is_refused_not_a_conflict():
    http = FakePostgrest()
    ghost = dict(a_run(), id=99, version=1)
    with pytest.raises(rsi_rows.Refused) as caught:
        store(http).update(rsi_rows.RUN_TABLE, ghost, {"state": "completed"})
    assert not isinstance(caught.value, rsi_rows.Conflict)


@pytest.mark.parametrize("column", ["id", "version", "updated_at"])
def test_an_update_may_not_set_the_bookkeeping_columns(column):
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    sent = len(http.calls)
    with pytest.raises(rsi_rows.Refused, match=column):
        store(http).update(rsi_rows.RUN_TABLE, run, {column: 5})
    assert len(http.calls) == sent


def test_an_update_that_drops_the_skills_commit_is_refused():
    http = FakePostgrest()
    run = store(http).insert(rsi_rows.RUN_TABLE, a_run())
    with pytest.raises(rsi_rows.Refused, match="skills_commit"):
        store(http).update(rsi_rows.RUN_TABLE, run, {"skills_commit": None})


# --- livecheck: test rows only, then cleaned up ------------------------------


def livecheck(capsys, http, env=ENV):
    code = rsi_rows.main(["livecheck"], environ=env, dotenv_path=Path("/nonexistent/ams-test"),
                         http=http, git=lambda args: HEAD + "\n")
    out, err = capsys.readouterr()
    return code, out, err


def test_livecheck_passes_and_leaves_nothing_behind(capsys):
    http = FakePostgrest()
    code, out, err = livecheck(capsys, http)
    assert code == 0, out
    for line in ("missing skills_commit: refused by the writer",
                 "missing skills_commit: refused by the database (code 23502, column skills_commit)",
                 "stale update: refused by the writer",
                 "stale update: refused by the database",
                 "row unchanged: yes",
                 "site key sees test rows: 0 of 1 runs, 0 of 1 results",
                 "cleanup: deleted 1 results, 1 runs; remaining 0"):
        assert line in out
    assert http.tables == {"rsi_runs": {}, "rsi_results": {}}
    for method, url, headers, body in http.calls:
        if method == "POST" and headers["apikey"] == FAKE_SECRET:
            assert json.loads(body)["is_test"] is True
    assert_no_key(out + err, FAKE_SECRET)
    assert_no_key(out + err, FAKE_PUBLISHABLE)


def test_livecheck_probes_client_writes_on_both_tables(capsys):
    http = FakePostgrest()
    code, out, _ = livecheck(capsys, http)
    assert code == 0
    for table in ("rsi_runs", "rsi_results"):
        for verb in ("insert", "update", "delete"):
            assert f"{table} {verb}: refused (http status 401)" in out


@pytest.mark.parametrize("broken,flag", [
    ("enforce_not_null", "missing skills_commit: ACCEPTED by the database"),
    ("guard_versions", "stale update: ACCEPTED by the database"),
    ("hide_test_rows", "site key sees test rows: 1 of 1 runs, 1 of 1 results"),
])
def test_livecheck_fails_when_a_rule_is_not_enforced_and_still_cleans_up(capsys, broken, flag):
    http = FakePostgrest(**{broken: False})
    code, out, _ = livecheck(capsys, http)
    assert code == 1
    assert flag in out
    assert http.tables == {"rsi_runs": {}, "rsi_results": {}}


@pytest.mark.parametrize("answer", [(503, None), (401, {"code": "42501"}), OSError("timed out"),
                                    (200, {"not": "a list"}), (200, b"{not json")])
def test_livecheck_fails_when_the_site_key_read_is_not_a_successful_query(capsys, answer):
    """An unreadable endpoint is not proof that test rows are hidden (Codex P2 4435897333)."""
    http = FakePostgrest(hide_test_rows=False)

    def site_get_fails(method, url, headers, body):
        if method == "GET" and headers["apikey"] == FAKE_PUBLISHABLE:
            http.calls.append((method, url, dict(headers), body))
            if isinstance(answer, Exception):
                raise answer
            status, payload = answer
            if isinstance(payload, bytes):
                return status, payload
            return status, json.dumps(payload).encode() if payload is not None else b""
        return http(method, url, headers, body)

    code, out, _ = livecheck(capsys, site_get_fails)
    assert code == 1, out
    assert "site key sees test rows" not in out
    assert "read failed" in out
    assert http.tables == {"rsi_runs": {}, "rsi_results": {}}


def test_livecheck_cleans_up_a_run_the_site_key_was_wrongly_allowed_to_insert(capsys):
    """Codex P2 4435926325: the client-insert probe run must be cleaned up too."""
    http = FakePostgrest(anon_inserts_runs=True)
    code, out, _ = livecheck(capsys, http)
    assert code == 1
    assert "rsi_runs insert: ACCEPTED" in out
    assert "cleanup: deleted 1 results, 2 runs; remaining 0" in out
    assert http.tables == {"rsi_runs": {}, "rsi_results": {}}


def test_livecheck_cleans_up_a_wrongly_inserted_client_run_whose_response_was_lost(capsys):
    http = FakePostgrest(anon_inserts_runs=True)

    def lose_client_insert(method, url, headers, body):
        answer = http(method, url, headers, body)
        if method == "POST" and headers["apikey"] == FAKE_PUBLISHABLE and "rsi_runs" in url:
            raise TimeoutError("response lost")
        return answer

    code, out, _ = livecheck(capsys, lose_client_insert)
    assert code == 1
    assert "rsi_runs insert: inconclusive" in out
    assert "remaining 0" in out
    assert http.tables == {"rsi_runs": {}, "rsi_results": {}}


def test_livecheck_without_the_service_key_sends_nothing(capsys):
    http = FakePostgrest()
    env = {k: v for k, v in ENV.items() if k != "SUPABASE_SERVICE_ROLE_KEY"}
    code, out, _ = livecheck(capsys, http, env=env)
    assert code == 1 and "loaded: no" in out and http.calls == []


# --- migration shape ----------------------------------------------------------


def _migration():
    path = next(Path(rsi_rows.REPO_ROOT, "supabase", "migrations").glob("*_rsi_rows.sql"))
    return path.read_text().lower()


def _all_migrations():
    folder = Path(rsi_rows.REPO_ROOT, "supabase", "migrations")
    return "\n".join(p.read_text().lower() for p in sorted(folder.glob("*.sql")))


def _table_body(sql, table):
    match = re.search(rf"create table public\.{table} \((.*?)\n\);", sql, re.S)
    assert match, table
    return match.group(1)


@pytest.mark.parametrize("table", ["rsi_runs", "rsi_results"])
def test_migration_requires_the_provenance_and_hides_test_rows(table):
    sql = _migration()
    body = _table_body(sql, table)
    for column in ("skills_commit", "runtime_commit", "controls_commit", "grader_version",
                   "provider", "model", "effort", "arm", "source_ref"):
        assert re.search(rf"^\s*{column}\s+\S+.*not null", body, re.M), (table, column)
    assert re.search(r"^\s*strength\s+public\.ams_strength not null", body, re.M)
    assert re.search(r"^\s*source_kind\s+public\.ams_source_kind not null", body, re.M)
    assert re.search(r"^\s*is_test\s+boolean not null", body, re.M)
    assert re.search(r"^\s*version\s+integer not null", body, re.M)
    assert f"revoke all on public.{table} from anon, authenticated;" in sql
    assert f"grant select on public.{table} to anon, authenticated;" in sql
    assert f"alter table public.{table} enable row level security;" in sql
    assert re.search(rf"create policy \w+ on public\.{table}\s+for select to anon, authenticated\s+using \(not is_test\);", sql)
    assert re.search(rf"create trigger \w+\s+before insert or update on public\.{table}", sql)


def test_migration_results_carry_task_split_trial_cost_and_tokens():
    body = _table_body(_migration(), "rsi_results")
    for column in ("task_id", "split", "trial", "execution_state", "cost_usd", "input_tokens",
                   "output_tokens", "turns", "wall_seconds"):
        assert re.search(rf"^\s*{column}\s+\S+.*not null", body, re.M), column
    assert "foreign key (run_id," in body and "references public.rsi_runs (id," in body


def test_migration_grants_no_client_write():
    sql = _migration()
    for verb in ("insert", "update", "delete"):
        assert f"for {verb}" not in sql
        assert not re.search(rf"grant [^;]*{verb}[^;]* to [^;]*(anon|authenticated)", sql)


# --- live check (opt-in) ------------------------------------------------------


@pytest.mark.skipif(os.environ.get("AMS_LIVE") != "1", reason="set AMS_LIVE=1 for the live check")
def test_live_livecheck(capsys):
    assert rsi_rows.main(["livecheck"]) == 0
    out = capsys.readouterr().out
    assert "row unchanged: yes" in out and "remaining 0" in out
