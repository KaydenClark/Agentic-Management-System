"""The lineage public seam rejects fabricated joins before publication."""
from copy import deepcopy
import json

import pytest

from ams import lineage


def chain(namespace="test-lineage"):
    def row(kind, name, parents, attributes):
        return dict(namespace=namespace, kind=kind, record_id=name, parents=parents,
                    attributes=attributes, source_commit="a" * 40,
                    artifact_digest="b" * 64, occurred_at="2026-11-05T00:00:00Z",
                    is_test=True, synthetic=True)
    return [
        row("failure", "occurrence-1", {}, {"failure_id": "FAIL-034", "family": "grilling-resume", "chain_id": "grilling-resume-repair-r1"}),
        row("case", "case-v1", {"failure": "occurrence-1"}, {"version": 1}),
        row("candidate", "baseline", {"case": "case-v1"}, {"attempt": 0, "skills_commit": "c" * 40}),
        row("candidate", "candidate-1", {"case": "case-v1", "previous_candidate": "baseline"},
            {"attempt": 1, "skills_commit": "d" * 40}),
        row("comparison", "comparison-1", {"case": "case-v1", "current_candidate": "baseline", "candidate": "candidate-1"},
            {"campaign_id": "synthetic-campaign", "contract_digest": "e" * 64}),
        row("run", "run-1", {"comparison": "comparison-1", "candidate": "candidate-1"}, {"run_key": "synthetic-run"}),
        row("result", "result-1", {"run": "run-1"}, {"execution_state": "completed", "passed": True}),
        row("disposition", "decision-1", {"comparison": "comparison-1", "result": "result-1"}, {"decision": "retained"}),
        row("adoption", "adoption-1", {"candidate": "candidate-1", "disposition": "decision-1"},
            {"receipt_digest": "f" * 64, "adopted_commit": "d" * 40}),
        row("use", "use-1", {"adoption": "adoption-1"},
            {"task_id": "TK-002N", "loaded_digest": "d" * 64, "outcome": "success"}),
    ]


def test_complete_chain_preserves_identity_and_synthetic_label():
    rows = chain()
    assert lineage.validate_graph(rows) == rows
    assert lineage.trace(rows, "use-1")[0]["record_id"] == "occurrence-1"
    assert all(r["synthetic"] for r in lineage.trace(rows, "use-1"))


@pytest.mark.parametrize("mutation", [
    lambda rs: rs[1]["parents"].update(failure="absent"),
    lambda rs: rs[-1]["parents"].update(adoption="result-1"),
    lambda rs: rs[-1].update(synthetic=False),
    lambda rs: rs[3]["attributes"].update(attempt=3),
    lambda rs: rs[0]["attributes"].update(transcript="private"),
    lambda rs: rs[0]["attributes"].update(failure_id="/not-a-record-id"),
    lambda rs: rs[0].update(source_commit="main"),
    lambda rs: rs[0].update(namespace="production"),
    lambda rs: rs[6]["attributes"].update(execution_state="timeout"),
    lambda rs: rs[7]["attributes"].update(decision="rejected"),
    lambda rs: rs.append(deepcopy(rs[0])),
])
def test_invalid_graph_refuses(mutation):
    rows = chain()
    mutation(rows)
    with pytest.raises(lineage.Refused):
        lineage.validate_graph(rows)


def test_new_case_name_cannot_reset_exhausted_candidate_family():
    rows = chain()
    next_case = deepcopy(rows[1]); next_case["record_id"] = "case-v2"
    new_baseline = deepcopy(rows[2]); new_baseline["record_id"] = "new-baseline"
    new_baseline["parents"]["case"] = "case-v2"
    with pytest.raises(lineage.Refused, match="attempt"):
        lineage.validate_graph(rows + [next_case, new_baseline])


def exhausted_chain(namespace="test-lineage"):
    records = chain(namespace)
    for attempt in (2, 3):
        candidate = deepcopy(records[3])
        candidate["record_id"] = "candidate-" + str(attempt)
        candidate["attributes"]["attempt"] = attempt
        candidate["parents"]["previous_candidate"] = "candidate-" + str(attempt - 1)
        records.append(candidate)
    return records


def recurrence_reset(records, attempt):
    occurrence = deepcopy(records[0]); occurrence["record_id"] = "occurrence-2"
    occurrence["attributes"]["failure_id"] = "FAIL-035"
    case = deepcopy(records[1]); case["record_id"] = "fresh-case"
    case["parents"]["failure"] = "occurrence-2"
    candidate = deepcopy(records[2]); candidate["record_id"] = "fresh-candidate"
    candidate["parents"]["case"] = "fresh-case"; candidate["attributes"]["attempt"] = attempt
    if attempt: candidate["parents"]["previous_candidate"] = "candidate-3"
    return [occurrence, case, candidate]


@pytest.mark.parametrize("attempt", [0, 4])
def test_recurrence_cannot_reset_underlying_exhausted_chain(attempt):
    records = exhausted_chain()
    with pytest.raises(lineage.Refused, match="attempt"):
        lineage.validate_graph(records + recurrence_reset(records, attempt))


def test_unrelated_chain_parent_cannot_replace_candidate_origin():
    records = chain()
    other = deepcopy(records[0]); other["record_id"] = "other-occurrence"
    other["attributes"] = {"failure_id": "FAIL-999", "family": "grilling-resume", "chain_id": "unrelated-chain"}
    case = deepcopy(records[1]); case["record_id"] = "other-case"; case["parents"]["failure"] = other["record_id"]
    candidate = deepcopy(records[3]); candidate["record_id"] = "mixed-candidate"; candidate["parents"]["case"] = case["record_id"]
    with pytest.raises(lineage.Refused, match="conflicting"):
        lineage.validate_graph(records + [other, case, candidate])


def test_run_can_use_declared_current_candidate_arm():
    records = chain()
    records[5]["parents"]["candidate"] = "baseline"
    # This arm is read back before any result, disposition or adoption exists.
    assert lineage.validate_graph(records[:6]) == records[:6]


def test_run_cannot_use_undeclared_comparison_source():
    records = exhausted_chain()
    run = deepcopy(records[5]); run["record_id"] = "undeclared-source-run"
    run["parents"]["candidate"] = "candidate-2"
    with pytest.raises(lineage.Refused, match="run candidate"):
        lineage.validate_graph(records + [run])


def test_readback_rejects_tampering_and_transport_errors_never_echo_body():
    calls = []
    def http(method, url, headers, body):
        calls.append((method, url))
        return 200, json.dumps([{"record_text": "private", "record_digest": "a" * 64}]).encode()
    store = lineage.Store("http://127.0.0.1:54321", "test-key", http=http)
    with pytest.raises(lineage.Refused, match="readback"):
        store.read("test-lineage")
    assert "test-key" not in repr(store)
    def unavailable(*args):
        raise RuntimeError("private token")
    store.http = unavailable
    with pytest.raises(lineage.Unavailable) as error:
        store.read("test-lineage")
    assert "private token" not in str(error.value)


def test_append_validates_entire_batch_before_remote_write():
    calls = []
    def http(*args):
        calls.append(args)
        return 200, b"[]"
    rows = chain(); rows[-1]["parents"]["adoption"] = "missing"
    with pytest.raises(lineage.Refused):
        lineage.Store("http://localhost", "key", http=http).append(rows, expected_head=None)
    assert all(call[0] == "GET" for call in calls)
