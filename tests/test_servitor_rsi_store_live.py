"""Run with AMS_RSI_STORE_TEST_CONFIG pointing at a disposable loopback PostgREST fixture."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
from uuid import uuid4

import pytest


PUBLIC_COLUMNS = {
    "audit_run_id", "audit_set_id", "skill", "skills_commit", "contract_version",
    "contract_digest", "provider", "model", "model_tier", "quality_passed",
    "quality_total", "regression_passed", "regression_total", "critical_missed",
    "evidence_complete", "passed", "completed_at", "recorded_at", "assessment_grade",
}
STAMP = "2026-11-07T09:30:00Z"
SHA = "a" * 40
DIGEST = "b" * 64


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


@pytest.fixture
def rest():
    filename = os.environ.get("AMS_RSI_STORE_TEST_CONFIG")
    if not filename:
        pytest.skip("isolated RSI store config not supplied")
    config = json.loads(Path(filename).read_text())
    address = urlsplit(config["url"])
    assert address.scheme == "http" and address.hostname == "127.0.0.1"
    assert address.port and not address.username and not address.password

    def call(path, *, role="service", body=None, profile=None, prefer=None):
        headers = {"Content-Type": "application/json"}
        if role != "anon":
            headers["Authorization"] = "Bearer " + config[f"{role}_jwt"]
        if profile:
            headers["Accept-Profile"] = profile
        if prefer:
            headers["Prefer"] = prefer
        request = Request(config["url"].rstrip("/") + path, headers=headers,
                          data=None if body is None else json.dumps(body).encode())
        opener = build_opener(ProxyHandler({}), NoRedirect())
        try:
            response = opener.open(request, timeout=10)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None, response.headers

    return call


def rpc(rest, name, **params):
    status, data, _ = rest("/rpc/" + name, body=params)
    return status, data


def append_audit(rest, row):
    return rpc(rest, "ams_append_skill_audit", p_row=row)


def append_observation(rest, row):
    return rpc(rest, "ams_append_rsi_observation", p_row=row)


def audit(run_id, set_id, **overrides):
    return {
        "audit_run_id": run_id, "audit_set_id": set_id, "skill": "code-review",
        "skills_commit": SHA, "contract_version": "skill-audit-v1", "contract_digest": DIGEST,
        "provider": "codex", "model": "openai/fixture", "model_tier": "mid",
        "quality_passed": 8, "quality_total": 8, "regression_passed": 5, "regression_total": 5,
        "critical_missed": False, "evidence_complete": True, "completion_state": "completed",
        "completed_at": STAMP, "is_test": False, "is_public": True, **overrides,
    }


def assert_error(result, status, code):
    assert result[0] == status
    assert result[1]["code"] == code


def test_observations_replay_and_refuse_unlinked_or_private_requests(rest):
    prefix = "obs-" + uuid4().hex
    request = {
        "event_id": prefix + "-requested", "chat_id": prefix, "occurred_at": STAMP,
        "kind": "skill_requested", "skill": "code-review", "skill_revision": None,
        "request_event_id": None, "outcome": None, "evidence_id": None,
    }
    skipped = dict(request, event_id=prefix + "-skipped", kind="skill_used", outcome="skipped",
                   request_event_id=request["event_id"], evidence_id=prefix + "-evidence")
    assert_error(append_observation(rest, skipped), 400, "23514")
    assert append_observation(rest, request)[0] == 200
    loaded = dict(request, event_id=prefix + "-loaded", kind="skill_loaded", skill_revision=SHA,
                  request_event_id=request["event_id"], evidence_id=prefix + "-load-evidence")
    assert_error(append_observation(rest, dict(loaded, skill_revision=None)), 400, "23514")
    assert_error(append_observation(rest, dict(loaded, evidence_id=None)), 400, "23514")
    assert append_observation(rest, loaded)[0] == 200
    status, saved = append_observation(rest, skipped)
    assert status == 200
    assert {key: saved[key] for key in skipped if key != "occurred_at"} == {
        key: value for key, value in skipped.items() if key != "occurred_at"
    }
    assert append_observation(rest, dict(skipped, occurred_at="2026-11-07T02:30:00-07:00")) == (200, saved)
    assert rpc(rest, "ams_get_rsi_observation", p_event_id=skipped["event_id"]) == (200, saved)
    assert_error(append_observation(rest, dict(skipped, evidence_id="changed")), 409, "PT409")
    assert_error(append_observation(rest, dict(skipped, event_id=prefix + "-foreign", chat_id="other")), 400, "23514")
    assert_error(append_observation(rest, dict(skipped, event_id=prefix + "-wrong", evidence_id=42)), 400, "23514")
    assert_error(append_observation(rest, dict(skipped, event_id=prefix + "-unproved", evidence_id=None)), 400, "23514")
    assert rpc(rest, "ams_get_rsi_observation", p_event_id=prefix + "-missing") == (200, None)
    for role, denied in (("anon", 401), ("authenticated", 403)):
        assert_error(rest("/rpc/ams_get_rsi_observation", role=role,
                          body={"p_event_id": skipped["event_id"]}), denied, "42501")
        assert_error(rest("/rpc/ams_append_rsi_observation", role=role,
                          body={"p_row": skipped}), denied, "42501")
        assert_error(rest("/observations", role=role, profile="ams_rsi_private"), 406, "PGRST106")


def test_projection_counts_completed_failures_and_hides_private_and_test_rows(rest):
    prefix = "projection-" + uuid4().hex
    public_set = prefix + "-public"
    hidden_set = prefix + "-hidden"
    query = "/rsi_skill_audit_results?" + urlencode({
        "audit_run_id": f"like.{prefix}*", "order": "completed_at.desc,audit_run_id.asc",
    })
    assert rest(query, role="anon")[:2] == (200, [])
    rows = [
        audit(prefix + "-clean", public_set),
        audit(prefix + "-failed", public_set, quality_passed=7, critical_missed=True),
        audit(prefix + "-incomplete", public_set, evidence_complete=False, critical_missed=None),
        audit(prefix + "-no-checks", prefix + "-no-checks-set", quality_passed=0, quality_total=0,
              regression_passed=0, regression_total=0, critical_missed=None),
        audit(prefix + "-test", prefix + "-test-set", is_test=True),
        audit(prefix + "-private", hidden_set, is_public=False),
        audit(prefix + "-interrupted", hidden_set, completion_state="interrupted", completed_at=None,
              is_public=False, evidence_complete=False, quality_passed=3, critical_missed=None),
    ]
    for row in rows:
        status, saved = append_audit(rest, row)
        assert status == 200, saved
        assert rpc(rest, "ams_get_skill_audit", p_audit_run_id=row["audit_run_id"]) == (200, saved)

    for role, denied in (("anon", 401), ("authenticated", 403)):
        status, projected, headers = rest(query, role=role, prefer="count=exact")
        assert status == 200
        assert headers["Content-Range"] == "0-3/4"
        assert [row["audit_run_id"] for row in projected] == [row["audit_run_id"] for row in rows[:4]]
        assert all(set(row) == PUBLIC_COLUMNS for row in projected)
        assert [row["passed"] for row in projected] == [True, False, None, None]
        assert projected[1]["critical_missed"] is True and projected[2]["critical_missed"] is None
        assert_error(rest("/rsi_skill_audit_results", role=role, body={"audit_run_id": "insert"}), denied, "42501")
        assert_error(rest("/rpc/ams_append_skill_audit", role=role, body={"p_row": rows[0]}), denied, "42501")
        assert_error(rest("/rpc/ams_get_skill_audit", role=role,
                          body={"p_audit_run_id": rows[5]["audit_run_id"]}), denied, "42501")
        assert_error(rest("/skill_audits", role=role, profile="ams_rsi_private"), 406, "PGRST106")


def test_audit_concurrent_replay_and_set_capacity_preserve_one_history(rest):
    prefix = "concurrent-" + uuid4().hex
    row = audit(prefix + "-first", prefix)
    with ThreadPoolExecutor(4) as executor:
        replies = list(executor.map(lambda _: append_audit(rest, row), range(4)))
    assert replies[0][0] == 200 and all(reply == replies[0] for reply in replies)
    assert_error(append_audit(rest, dict(row, model="changed")), 409, "PT409")
    assert_error(append_audit(rest, audit(prefix + "-incompatible", prefix, contract_digest="d" * 64)), 409, "PT409")
    for field, value in (("provider", "claude"), ("model", "changed"), ("model_tier", "high")):
        incompatible = audit(prefix + "-changed-" + field, prefix, **{field: value})
        assert_error(append_audit(rest, incompatible), 409, "PT409")
    assert_error(append_audit(rest, audit(prefix + "-numeric", prefix, quality_total="8")), 400, "23514")
    assert_error(append_audit(rest, audit(prefix + "-unknown", prefix, transcript="rejected")), 400, "23514")
    attempts = [audit(f"{prefix}-{index}", prefix) for index in range(4)]
    with ThreadPoolExecutor(4) as executor:
        replies = list(executor.map(lambda attempt: append_audit(rest, attempt), attempts))
    assert sorted(status for status, _ in replies) == [200, 200, 409, 409]
    for reply in replies:
        if reply[0] == 409:
            assert_error(reply, 409, "PT409")
    query = "/rsi_skill_audit_results?" + urlencode({"audit_set_id": "eq." + prefix})
    assert len(rest(query, role="anon")[1]) == 3
    assert rpc(rest, "ams_get_skill_audit", p_audit_run_id=row["audit_run_id"])[1]["model"] == row["model"]



@pytest.mark.parametrize(("run_changes", "expected"), [
    ([dict(quality_passed=6, quality_total=7, regression_passed=4, regression_total=4),
      dict(quality_passed=6, quality_total=6, regression_passed=4, regression_total=4, critical_missed=True),
      dict(quality_passed=7, quality_total=7, regression_passed=4, regression_total=4)], "Broken"),
    ([{}, {}, {"quality_passed": 7, "regression_passed": 4}], "Functional"),
    ([{}, {}, {"quality_passed": 7}], "Stable"),
    ([{}, {}, {}], "Excellent"),
    ([{}, {}, {"evidence_complete": False}], None),
    ([{}, {}, {"quality_passed": 7, "evidence_complete": False}], "Stable"),
    ([dict(quality_passed=0, quality_total=0, regression_passed=0, regression_total=0,
           critical_missed=None)] * 3, None),
    ([{}, {"critical_missed": True}], None),
    ([{"is_test": True}] * 3, None),
    ([{}, {"quality_passed": 7}, {"is_public": False, "critical_missed": True}], None),
    ([{}, {}, dict(completion_state="interrupted", completed_at=None,
                   is_public=False, evidence_complete=False)], None),
], ids=["critical", "regression", "quality", "clean", "incomplete-evidence", "observed-miss",
        "no-applicable-checks", "two-runs", "all-test", "private-third", "interrupted-third"])
def test_public_assessment_grade_requires_three_visible_completed_runs(rest, run_changes, expected):
    set_id = "grade-" + uuid4().hex
    rows = [audit(f"{set_id}-{index}", set_id, **changes) for index, changes in enumerate(run_changes)]
    for row in rows:
        status, saved = append_audit(rest, row)
        assert status == 200, saved
        assert "assessment_grade" not in saved

    visible_ids = [row["audit_run_id"] for row in rows if row["is_public"] and not row["is_test"]]
    query = "/rsi_skill_audit_results?" + urlencode({"audit_set_id": "eq." + set_id})
    for role in ("anon", "authenticated", "service"):
        status, projected, _ = rest(query, role=role)
        assert status == 200
        assert {row["audit_run_id"] for row in projected} == set(visible_ids)
        assert all(row["assessment_grade"] == expected for row in projected)
    if expected == "Broken":
        assert sum(row["quality_passed"] for row in projected) == 19
        assert sum(row["quality_total"] for row in projected) == 20
        assert sum(row["regression_passed"] for row in projected) == 12
        assert sum(row["regression_total"] for row in projected) == 12
        one_run = "/rsi_skill_audit_results?" + urlencode({"audit_run_id": "eq." + visible_ids[0]})
        assert rest(one_run, role="anon")[1][0]["assessment_grade"] == "Broken"
