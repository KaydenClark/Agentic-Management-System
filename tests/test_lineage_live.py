"""Opt-in probes against an isolated local Supabase DB and real PostgREST.

Set AMS_LINEAGE_TEST_CONFIG to an outside-repository private client file.
Neither production credentials nor production namespaces are accepted here.
"""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from urllib.parse import urlparse
import uuid

import pytest

from ams import lineage, rsi_rows, writer
from test_lineage import chain, exhausted_chain, recurrence_reset


@dataclass
class Local:
    store: lineage.Store
    config: dict = field(repr=False)
    namespace: str

    def __iter__(self):
        return iter((self.store, self.config, self.namespace))


@pytest.fixture
def local():
    filename = os.environ.get("AMS_LINEAGE_TEST_CONFIG")
    if not filename:
        pytest.skip("isolated Supabase config not supplied")
    config = json.loads(Path(filename).read_text())
    assert urlparse(config["url"]).hostname in ("127.0.0.1", "localhost")
    store = lineage.Store(config["url"], config["service_jwt"], rest_path=config["rest_path"], page_size=3)
    namespace = "test-lineage-" + uuid.uuid4().hex
    return Local(store, config, namespace)


def raw_append(store, namespace, records, head=None):
    return store._call("POST", "rpc/" + lineage.RPC, {
        "p_namespace": namespace, "p_expected_head": head,
        "p_records": [{"record_text": lineage.canonical(r), "record_digest": lineage.digest(r)} for r in records],
    })


def test_real_writer_store_readback_and_immutable_retry(local):
    store, _, namespace = local
    records = chain(namespace)
    assert len(store.append(records, expected_head=None)) == len(records)
    assert store.read(namespace) == records
    assert all(record["synthetic"] for record in store.read(namespace))
    assert len(store.append(records, expected_head=None)) == len(records)
    changed = deepcopy(records[-1]); changed["attributes"]["outcome"] = "failure"
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, [changed])
    assert store.read(namespace) == records


@pytest.mark.parametrize("mutation", [
    lambda rs: rs[1]["parents"].update(failure="missing"),
    lambda rs: rs[1]["parents"].update(failure={"private": "secret"}),
    lambda rs: rs[0]["attributes"].update(raw={"transcript": "private"}),
    lambda rs: rs[0]["attributes"].update(family={"private": "secret"}),
    lambda rs: rs[3]["attributes"].update(attempt=3),
    lambda rs: rs[-1].update(synthetic=False),
    lambda rs: rs[7]["attributes"].update(decision="rejected"),
    lambda rs: rs.append(deepcopy(rs[0])),
])
def test_database_rejects_invalid_batch_atomically_without_python_guard(local, mutation):
    store, _, namespace = local
    records = chain(namespace); mutation(records)
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, records)
    assert store.read(namespace) == []


def test_concurrent_different_appends_require_same_expected_head_once(local):
    store, _, namespace = local
    first = chain(namespace)[0]; second = deepcopy(first); second["record_id"] = "occurrence-2"
    def append(record):
        try:
            raw_append(store, namespace, [record]); return "written"
        except lineage.Unavailable:
            raise
        except lineage.Refused:
            return "conflict"
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(append, [first, second]))
    assert sorted(outcomes) == ["conflict", "written"]
    assert len(store.read(namespace)) == 1


def test_client_roles_cannot_read_write_or_invoke_operations(local):
    store, config, namespace = local
    store.append(chain(namespace), expected_head=None)
    for key in (config["anon_jwt"], config["authenticated_jwt"]):
        for method, endpoint, payload in [
            ("GET", lineage.TABLE, None), ("POST", lineage.TABLE, {}),
            ("PATCH", lineage.TABLE + "?namespace=eq." + namespace, {"kind": "failure"}),
            ("DELETE", lineage.TABLE + "?namespace=eq." + namespace, None),
            ("POST", "rpc/" + lineage.RPC, {"p_namespace": namespace, "p_expected_head": None, "p_records": []}),
        ]:
            status, body = writer._call(writer.urllib_http, method,
                config["url"] + config["rest_path"] + "/" + endpoint, key, payload)
            assert writer._denied(status, body), (method, status)
    assert len(store.read(namespace)) == 10


@pytest.mark.parametrize("attempt", [0, 4])
def test_database_recurrence_cannot_reset_exhausted_chain(local, attempt):
    store, _, namespace = local
    records = exhausted_chain(namespace)
    saved = store.append(records, expected_head=None)
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, recurrence_reset(records, attempt), head=saved[-1]["record_digest"])
    assert store.read(namespace) == records


def test_database_new_campaign_does_not_release_fourth_candidate(local):
    store, _, namespace = local
    records = exhausted_chain(namespace)
    saved = store.append(records, expected_head=None)
    campaign = deepcopy(records[4]); campaign["record_id"] = "new-comparison"
    campaign["attributes"]["campaign_id"] = "new-campaign-name"
    campaign["parents"]["candidate"] = "candidate-3"
    candidate = deepcopy(records[-1]); candidate["record_id"] = "candidate-4"
    candidate["attributes"]["attempt"] = 4; candidate["parents"]["previous_candidate"] = "candidate-3"
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, [campaign, candidate], head=saved[-1]["record_digest"])
    assert store.read(namespace) == records


def test_real_row_references_cannot_be_invented(local):
    store, _, namespace = local
    records = chain(namespace)
    for record in records: record["synthetic"] = False
    records[5]["attributes"]["rsi_run_id"] = 9223372036854775807
    records[6]["attributes"]["rsi_result_id"] = 9223372036854775807
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, records)
    assert store.read(namespace) == []


def test_database_reads_declared_current_and_candidate_run_arms(local):
    store, _, namespace = local
    records = chain(namespace)[:6]
    current = deepcopy(records[-1]); current["record_id"] = "current-arm-run"
    current["attributes"]["run_key"] = "current-arm"
    current["parents"]["candidate"] = "baseline"
    records.append(current)
    raw_append(store, namespace, records)
    assert store.read(namespace) == records


def test_database_undeclared_source_cannot_join_comparison(local):
    store, _, namespace = local
    records = exhausted_chain(namespace)
    saved = store.append(records, expected_head=None)
    run = deepcopy(records[5]); run["record_id"] = "undeclared-run"
    run["parents"]["candidate"] = "candidate-2"
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, [run], head=saved[-1]["record_digest"])
    assert store.read(namespace) == records


@pytest.mark.parametrize("cross", ["case", "chain"])
def test_database_crosscase_or_chain_joins_refuse(local, cross):
    store, _, namespace = local
    records = chain(namespace)
    saved = store.append(records, expected_head=None)
    case = deepcopy(records[1]); case["record_id"] = "different-case"
    if cross == "case":
        comparison = deepcopy(records[4]); comparison["record_id"] = "different-case-comparison"
        comparison["parents"]["case"] = case["record_id"]
        new = [case, comparison]
    else:
        failure = deepcopy(records[0]); failure["record_id"] = "different-chain-occurrence"
        failure["attributes"].update(failure_id="FAIL-999", chain_id="different-chain")
        case["parents"]["failure"] = failure["record_id"]
        candidate = deepcopy(records[3]); candidate["record_id"] = "different-chain-candidate"
        candidate["parents"]["case"] = case["record_id"]
        new = [failure, case, candidate]
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, new, head=saved[-1]["record_digest"])
    assert store.read(namespace) == records


def test_database_existing_run_source_must_match_declared_candidate(local):
    store, _, namespace = local
    # This is deliberately adversarial schema data: no model was invoked.
    # The lineage batch must reject; it cannot become a non-synthetic result.
    run_key = "source-mismatch-" + uuid.uuid4().hex
    run = dict(run_key=run_key, arm="ams", provider="schema-probe", model="no-model-call",
               effort="none", runtime_commit="a"*40, controls_commit="a"*40,
               skills_commit="e"*40, grader_version="a"*40, state="completed",
               started_at="2026-11-05T00:00:00Z", finished_at="2026-11-05T00:00:00Z",
               source_kind="commit", source_ref="a"*40, strength="anecdote", is_test=True,
               detail={"purpose": "synthetic source-mismatch rejection probe"})
    rsi_rows.check_run(run)
    saved = store._call("POST", "rsi_runs", run)
    assert len(saved) == 1
    records = chain(namespace)[:6]
    for record in records: record["synthetic"] = False
    records[-1]["attributes"].update(run_key=run_key, rsi_run_id=saved[0]["id"])
    with pytest.raises(lineage.Refused, match="HTTP 4"):
        raw_append(store, namespace, records)
    assert store.read(namespace) == []
