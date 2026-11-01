"""Tests for the Supabase writer and its publishable-key read-back (S-006 TK-002).

Keys here are fake. The HTTP and Git layers are stubbed, so no test reaches
Supabase. The live round trip runs only with AMS_LIVE=1 (see the end).
"""

import base64
import json
import os
import random
import string
from pathlib import Path

import pytest

from ams import writer

URL = "https://example-project.supabase.co"
_rng = random.Random(20261102)
_ALPHA = string.ascii_letters + string.digits
FAKE_SECRET = "sb_secret_" + "".join(_rng.choice(_ALPHA) for _ in range(40))
FAKE_PUBLISHABLE = "sb_publishable_" + "".join(_rng.choice(_ALPHA) for _ in range(30))

SHA = "884d0215f3ea2693b691f2275e16bcba715fbc88"
MERGE_SHOW = "\n".join(
    [
        SHA,
        "0a7d04edd7074fbf37a201b5812df1b36cb29239 7a26437437098d35cadc643cc7c75b62a6ab4db6",
        "2026-11-01T06:20:13-07:00",
        "Merge pull request #15 from KaydenClark/feat/s006-tk001-key-check",
        "S-006 TK-001: ams-keycheck reports whether the Supabase service key loads and authenticates",
        "",
    ]
)


def fake_git(output):
    calls = []

    def git(args):
        calls.append(list(args))
        return output

    git.calls = calls
    return git


class StubHttp:
    """Answers each request from a per-method table; records every call."""

    def __init__(self, answers):
        self.answers = answers
        self.calls = []

    def __call__(self, method, url, headers, body):
        self.calls.append((method, url, dict(headers), body))
        answer = self.answers[method]
        if callable(answer):
            answer = answer(url, body)
        if isinstance(answer, Exception):
            raise answer
        status, payload = answer
        return status, json.dumps(payload).encode() if payload is not None else b""


ENV = {
    "SUPABASE_URL": URL,
    "SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET,
    "SUPABASE_PUBLISHABLE_KEY": FAKE_PUBLISHABLE,
}


def run(capsys, argv, http, env=ENV, git=None, tmp_path=None):
    code = writer.main(
        argv,
        environ=env,
        dotenv_path=Path("/nonexistent/ams-test-dotenv"),
        http=http,
        git=git or fake_git(MERGE_SHOW),
    )
    out, err = capsys.readouterr()
    return code, out, err


def assert_no_key(text, key):
    for size in range(len(key) - 1, 12, -1):
        for start in range(0, len(key) - size + 1):
            assert key[start : start + size] not in text


# --- building the row from Git ---------------------------------------------


def test_merge_row_comes_from_git_with_source_and_strength():
    git = fake_git(MERGE_SHOW)
    row = writer.merge_event(SHA, git=git)
    assert git.calls and SHA in git.calls[0]
    assert row["kind"] == "merge"
    assert row["subject"] == "PR #15"
    assert row["summary"].startswith("S-006 TK-001: ams-keycheck")
    assert row["occurred_at"] == "2026-11-01T06:20:13-07:00"
    assert row["source_kind"] == "commit"
    assert row["source_ref"] == SHA
    assert row["source_url"] == writer.REPO_URL + "/commit/" + SHA
    assert row["strength"] == "recorded_fact"
    assert row["is_test"] is False
    assert row["detail"]["pr"] == 15
    assert row["detail"]["pr_url"] == writer.REPO_URL + "/pull/15"
    assert row["detail"]["branch"] == "KaydenClark/feat/s006-tk001-key-check"
    assert len(row["detail"]["parents"]) == 2


def test_non_merge_commit_is_refused():
    single_parent = MERGE_SHOW.replace(
        "0a7d04edd7074fbf37a201b5812df1b36cb29239 ", ""
    )
    with pytest.raises(ValueError):
        writer.merge_event(SHA, git=fake_git(single_parent))


def test_merge_without_pr_number_is_refused():
    plain = MERGE_SHOW.replace(
        "Merge pull request #15 from", "Merge branch 'x' of"
    )
    with pytest.raises(ValueError):
        writer.merge_event(SHA, git=fake_git(plain))


# --- record-merge: inserts with the service key ------------------------------


def test_record_merge_posts_with_service_key_and_prints_no_key(capsys):
    http = StubHttp({"POST": (201, [{"id": 7, "kind": "merge", "source_ref": SHA}])})
    code, out, err = run(capsys, ["record-merge", SHA], http)
    assert code == 0
    method, url, headers, body = http.calls[0]
    assert method == "POST"
    assert url == URL + "/rest/v1/build_events"
    assert headers["apikey"] == FAKE_SECRET
    assert "Authorization" not in headers  # sb_secret keys are not JWTs
    assert headers["Prefer"] == "return=representation"
    sent = json.loads(body)
    assert sent["source_ref"] == SHA and sent["is_test"] is False
    assert "inserted: id=7" in out
    assert_no_key(out + err, FAKE_SECRET)


def test_record_merge_with_legacy_jwt_sends_bearer(capsys):
    seg = lambda obj: base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()
    jwt = ".".join([seg({"alg": "HS256"}), seg({"role": "service_role"}),
                    "".join(_rng.choice(_ALPHA) for _ in range(43))])  # fake, built at run time
    http = StubHttp({"POST": (201, [{"id": 1}])})
    env = dict(ENV, SUPABASE_SERVICE_ROLE_KEY=jwt)
    code, out, err = run(capsys, ["record-merge", SHA], http, env=env)
    assert code == 0
    headers = http.calls[0][2]
    assert headers["apikey"] == jwt and headers["Authorization"] == "Bearer " + jwt
    assert_no_key(out + err, jwt)


def test_record_merge_twice_reports_already_recorded(capsys):
    http = StubHttp({"POST": (409, {"code": "23505", "message": "duplicate key"})})
    code, out, _ = run(capsys, ["record-merge", SHA], http)
    assert code == 0
    assert "already recorded" in out


def test_record_merge_failure_exits_nonzero_without_key(capsys):
    http = StubHttp({"POST": (500, {"message": "boom " + FAKE_SECRET})})
    code, out, err = run(capsys, ["record-merge", SHA], http)
    assert code == 1
    assert "insert failed: http status 500" in out
    assert_no_key(out + err, FAKE_SECRET)


def test_record_merge_transport_error_drops_its_text(capsys):
    http = StubHttp({"POST": OSError("failed for " + FAKE_SECRET)})
    code, out, err = run(capsys, ["record-merge", SHA], http)
    assert code == 1
    assert_no_key(out + err, FAKE_SECRET)


def test_record_merge_without_service_key_sends_nothing(capsys):
    http = StubHttp({})
    env = {k: v for k, v in ENV.items() if k != "SUPABASE_SERVICE_ROLE_KEY"}
    code, out, _ = run(capsys, ["record-merge", SHA], http, env=env)
    assert code == 1
    assert "loaded: no" in out
    assert http.calls == []


def test_record_merge_test_flag_marks_the_row(capsys):
    http = StubHttp({"POST": (201, [{"id": 2}])})
    code, _, _ = run(capsys, ["record-merge", SHA, "--test"], http)
    assert code == 0
    assert json.loads(http.calls[0][3])["is_test"] is True


# --- readcheck: publishable key reads, every client write refused ------------

ROW = {"id": 7, "kind": "merge", "subject": "PR #15", "source_ref": SHA,
       "strength": "recorded_fact", "summary": "S-006 TK-001"}


def refusing(status=401):
    return (status, {"code": "42501", "message": "permission denied for table build_events"})


def test_readcheck_reads_with_publishable_key_and_all_writes_refused(capsys):
    http = StubHttp({"GET": (200, [ROW]), "POST": refusing(), "PATCH": refusing(),
                     "DELETE": refusing()})
    code, out, err = run(capsys, ["readcheck", SHA], http)
    assert code == 0, out
    for method, url, headers, _ in http.calls:
        assert headers["apikey"] == FAKE_PUBLISHABLE
        assert FAKE_SECRET not in json.dumps(headers)
    methods = [c[0] for c in http.calls]
    assert methods == ["GET", "POST", "PATCH", "DELETE", "GET"]
    assert "source_ref=eq." + SHA in http.calls[0][1]
    assert "rows: 1" in out
    for verb in ("insert", "update", "delete"):
        assert f"{verb}: refused (http status 401)" in out
    assert "row unchanged: yes" in out
    assert_no_key(out + err, FAKE_SECRET)


@pytest.mark.parametrize("accepted", ["POST", "PATCH", "DELETE"])
def test_readcheck_fails_when_any_client_write_is_accepted(capsys, accepted):
    answers = {"GET": (200, [ROW]), "POST": refusing(), "PATCH": refusing(),
               "DELETE": refusing()}
    answers[accepted] = (200, [])  # an RLS no-op still counts as accepted
    code, out, _ = run(capsys, ["readcheck", SHA], StubHttp(answers))
    assert code == 1
    assert "ACCEPTED" in out


def test_readcheck_fails_when_row_is_not_visible(capsys):
    http = StubHttp({"GET": (200, []), "POST": refusing(), "PATCH": refusing(),
                     "DELETE": refusing()})
    code, out, _ = run(capsys, ["readcheck", SHA], http)
    assert code == 1
    assert "rows: 0" in out


def test_readcheck_fails_when_row_changed_after_writes(capsys):
    reads = iter([[ROW], [dict(ROW, summary="changed")]])
    http = StubHttp({"GET": lambda url, body: (200, next(reads)), "POST": refusing(),
                     "PATCH": refusing(), "DELETE": refusing()})
    code, out, _ = run(capsys, ["readcheck", SHA], http)
    assert code == 1
    assert "row unchanged: no" in out


def test_readcheck_refuses_a_secret_key_in_the_publishable_slot(capsys):
    http = StubHttp({})
    env = dict(ENV, SUPABASE_PUBLISHABLE_KEY=FAKE_SECRET)
    code, out, err = run(capsys, ["readcheck", SHA], http, env=env)
    assert code == 1
    assert http.calls == []
    assert_no_key(out + err, FAKE_SECRET)


def test_readcheck_falls_back_to_the_public_publishable_key(capsys):
    http = StubHttp({"GET": (200, [ROW]), "POST": refusing(), "PATCH": refusing(),
                     "DELETE": refusing()})
    env = {"SUPABASE_URL": URL}
    code, _, _ = run(capsys, ["readcheck", SHA], http, env=env)
    assert code == 0
    assert http.calls[0][2]["apikey"] == writer.DEFAULT_PUBLISHABLE_KEY


# --- migration shape ---------------------------------------------------------


def test_migration_grants_clients_select_only_and_hides_test_rows():
    path = next(Path(writer.REPO_ROOT, "supabase", "migrations").glob("*_build_events.sql"))
    sql = path.read_text().lower()
    assert "grant select on public.build_events to anon, authenticated;" in sql
    assert "revoke all on public.build_events from anon, authenticated;" in sql
    assert "using (not is_test)" in sql
    for verb in ("insert", "update", "delete"):
        assert f"for {verb}" not in sql
    assert "source_ref  text not null" in sql and "strength    public.ams_strength not null" in sql


# --- live round trip (opt-in) ------------------------------------------------


@pytest.mark.skipif(os.environ.get("AMS_LIVE") != "1", reason="set AMS_LIVE=1 for the live round trip")
def test_live_record_and_readcheck(capsys):
    assert writer.main(["record-merge", SHA]) == 0
    assert writer.main(["readcheck", SHA]) == 0
    out = capsys.readouterr().out
    assert "rows: 1" in out and "row unchanged: yes" in out


@pytest.mark.parametrize("outcome", [OSError("timed out"), TimeoutError("read timed out"),
                                     (500, {"message": "boom"}), (503, None), (404, None),
                                     (400, {"code": "PGRST100"}), (500, {"code": "42501"})])
@pytest.mark.parametrize("probe", ["POST", "PATCH", "DELETE"])
def test_readcheck_fails_when_a_write_probe_is_inconclusive(capsys, probe, outcome):
    answers = {"GET": (200, [ROW]), "POST": refusing(), "PATCH": refusing(),
               "DELETE": refusing()}
    answers[probe] = outcome  # only an authorization denial proves refusal
    code, out, _ = run(capsys, ["readcheck", SHA], StubHttp(answers))
    assert code == 1
    assert "inconclusive" in out


def test_readcheck_accepts_403_as_an_authorization_denial(capsys):
    http = StubHttp({"GET": (200, [ROW]), "POST": refusing(403), "PATCH": refusing(403),
                     "DELETE": refusing(403)})
    code, out, _ = run(capsys, ["readcheck", SHA], http)
    assert code == 0, out


def test_readcheck_accepts_a_42501_permission_error_body(capsys):
    denied = (400, {"code": "42501", "message": "permission denied for table build_events"})
    http = StubHttp({"GET": (200, [ROW]), "POST": denied, "PATCH": refusing(), "DELETE": refusing()})
    code, out, _ = run(capsys, ["readcheck", SHA], http)
    assert code == 0, out
    assert "insert: refused (http status 400)" in out


def test_readcheck_labels_an_unexpected_2xx_as_accepted_and_fails(capsys):
    http = StubHttp({"GET": (200, [ROW]), "POST": (201, [{"id": 9}]), "PATCH": refusing(),
                     "DELETE": refusing()})
    code, out, _ = run(capsys, ["readcheck", SHA], http)
    assert code == 1
    assert "insert: ACCEPTED (http status 201)" in out
