"""Real isolated checkpoint restore; no live authorization is restored."""
from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib
import json
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import pytest

from ams import lineage,recovery
from test_lineage import chain
from test_recovery_live import local,prepared


@pytest.fixture
def destination(local):
    path=os.environ.get("AMS_RECOVERY_RESTORE_CONFIG")
    if not path:pytest.skip("isolated restore database config not supplied")
    config=json.loads(Path(path).read_text())
    assert urlparse(config["url"]).hostname in ("127.0.0.1","localhost")
    return recovery.Store(config["url"],config["service_jwt"],rest_path=config["rest_path"],pending_dir=local.root/"restore-pending")


def pg_json(value):
    """Match JSONB text for these typed ASCII fixtures; verified against export."""
    if type(value) is dict:
        keys=sorted(value,key=lambda key:(len(key.encode()),key.encode()))
        return "{"+", ".join(json.dumps(k)+": "+pg_json(value[k]) for k in keys)+"}"
    if type(value) is list:return "["+", ".join(pg_json(v) for v in value)+"]"
    return json.dumps(value,ensure_ascii=False,allow_nan=False)


def resign(manifest,mutate):
    result=deepcopy(manifest);data=json.loads(result["snapshot_text"])
    assert pg_json(data)==result["snapshot_text"]
    mutate(data)
    result["snapshot_text"]=pg_json(data)
    result["source_head"]=hashlib.sha256(result["snapshot_text"].encode()).hexdigest()
    result["counts"]={k:len(data[k]) for k in recovery.SNAPSHOT_KINDS}
    result["records"]=recovery._record_digests(data)
    result["manifest_digest"]=recovery.digest({k:v for k,v in result.items() if k!="manifest_digest"})
    return result


def raw_restore(store,manifest,*,expected_head=None,expected_pin=None):
    payload={k:v for k,v in manifest.items() if k!="manifest_digest"}
    return store._rpc("restore",{"manifest_text":recovery.canonical(payload),"manifest_digest":manifest["manifest_digest"],
        "expected_manifest_digest":manifest["manifest_digest"] if expected_pin is None else expected_pin,
        "expected_head":expected_head,"reader_digest":recovery.reader_digest(),"schema_digest":recovery.schema_digest()},mutating=True)


@contextmanager
def rejected(*codes):
    with pytest.raises(recovery.DatabaseRefused) as caught:yield
    assert caught.value.database_code in codes


def test_complete_checkpoint_restores_ids_receipts_and_matching_noop(local,destination):
    ready=prepared(local);claimed=local.store.claim(ready,"source")
    reserved=local.store.begin_effect(claimed,0)
    adapter=recovery.KeyedFileEffect(local.root)
    observation=adapter.apply(reserved["effect"]["effect_key"],b"safe synthetic effect")
    sealed=local.store.observe_effect(reserved["job"],reserved["effect"]["effect_key"],observation)
    final=local.store.finish(sealed["job"],"completed",evidence_digest=observation["artifact_digest"])
    manifest=local.store.export(local.namespace)
    assert "safe synthetic effect" not in recovery.canonical(manifest)
    assert manifest["counts"]=={"lineage":5,"jobs":1,"effects":1,"externals":0}
    restored=destination.restore(manifest,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    assert restored["head"]==manifest["source_head"] and restored["restored"] is True
    copied=destination.get_job(local.namespace,"job-1")
    for key in ("job_text","job_digest","chain_id","attempt","version","fence","terminal_state","evidence_digest"):
        assert copied[key]==final[key]
    assert copied["approved"] is False and copied["capacity"]=="unknown"
    assert copied["claimant"] is None and copied["lease_until"] is None
    assert destination.restore(manifest,expected_head=manifest["source_head"],
        expected_manifest_digest=manifest["manifest_digest"])["restored"] is False


def test_pending_checkpoint_restores_no_lease_or_execution_permission(local,destination):
    ready=prepared(local);claimed=local.store.claim(ready,"source")
    reserved=local.store.begin_effect(claimed,0)
    manifest=local.store.export(local.namespace)
    destination.restore(manifest,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    copied=destination.get_job(local.namespace,"job-1")
    assert copied["state"]=="blocked" and not copied["approved"] and copied["lease_until"] is None
    fresh=destination.claim(copied,"fresh")
    existing=destination.begin_effect(fresh,0)
    assert existing["execute"] is False and existing["reconcile"] is True
    assert existing["effect"]["effect_key"]==reserved["effect"]["effect_key"]
    assert existing["job"]["attempt"]==1 and existing["job"]["fence"]>claimed["fence"]


def test_stale_or_divergent_restore_retains_newer_canonical_state(local,destination):
    prepared(local);manifest=local.store.export(local.namespace)
    destination.restore(manifest,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    copied=destination.get_job(local.namespace,"job-1")
    destination.gates(copied,approved=False,capacity="unknown",observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="f"*64)
    current=destination.snapshot(local.namespace)
    for expected in (manifest["source_head"],current["head"]):
        with rejected("PT409"):
            destination.restore(manifest,expected_head=expected,expected_manifest_digest=manifest["manifest_digest"])
        assert destination.snapshot(local.namespace)==current


@pytest.mark.parametrize("omit",["independent-chain","effect-leaf"])
def test_recomputed_omission_cannot_replace_independently_trusted_checkpoint(local,destination,omit):
    ready=prepared(local)
    if omit=="independent-chain":
        other=chain(local.namespace)[:5]
        mapping={r["record_id"]:"other-"+r["record_id"] for r in other}
        for row in other:
            row["record_id"]=mapping[row["record_id"]]
            row["parents"]={k:mapping[v] for k,v in row["parents"].items()}
        other[0]["attributes"].update(failure_id="FAIL-999",chain_id="independent-chain")
        original=lineage.Store(local.config["url"],local.config["service_jwt"],rest_path=local.config["rest_path"])
        old=original.rows(local.namespace);original.append(other,expected_head=old[-1]["record_digest"])
    else:
        claimed=local.store.claim(ready,"source");local.store.begin_effect(claimed,0)
    manifest=local.store.export(local.namespace)
    if omit=="independent-chain":
        forged=resign(manifest,lambda data:data.update(lineage=[r for r in data["lineage"]
            if not json.loads(r["record_text"])["record_id"].startswith("other-")]))
    else:forged=resign(manifest,lambda data:data.update(effects=[]))
    # Deliberately self-consistent: internal hashes/counts do not prove origin.
    recovery.validate_checkpoint(forged)
    with pytest.raises(recovery.Refused,match="independently pinned"):
        destination.restore(forged,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    with rejected("PT409"):
        raw_restore(destination,forged,expected_pin=manifest["manifest_digest"])
    assert json.loads(destination.snapshot(local.namespace)["snapshot_text"])["lineage"]==[]


@pytest.mark.parametrize("malformed",["private","missing-parent","counter","external"])
def test_raw_restore_rejects_private_or_broken_projection_atomically(local,destination,malformed):
    prepared(local);manifest=local.store.export(local.namespace)
    def mutate(data):
        if malformed=="external":
            data["externals"].append({"table":"rsi_runs","id":9223372036854775807,"digest":"a"*64});return
        row=data["jobs"][0]
        if malformed=="counter":row["attempt"]=3;return
        value=json.loads(row["job_text"])
        if malformed=="private":value["slots"][0]["prompt"]={"raw":"private test content"}
        else:value["case_id"]="missing-case"
        row["job_text"]=recovery.canonical(value);row["job_digest"]=recovery.digest(value)
    forged=resign(manifest,mutate)
    with rejected("PT409" if malformed=="external" else "23514"):
        raw_restore(destination,forged)
    data=json.loads(destination.snapshot(local.namespace)["snapshot_text"])
    assert all(data[k]==[] for k in recovery.SNAPSHOT_KINDS)


def test_partial_inventory_and_unsupported_reader_refuse(local,destination):
    prepared(local);manifest=local.store.export(local.namespace)
    for change in (lambda m:m["records"].pop(),lambda m:m.update(reader_version=2)):
        forged=deepcopy(manifest);change(forged)
        forged["manifest_digest"]=recovery.digest({k:v for k,v in forged.items() if k!="manifest_digest"})
        with pytest.raises(recovery.Refused):
            destination.restore(forged,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
        with rejected("23514"):
            raw_restore(destination,forged)
    assert json.loads(destination.snapshot(local.namespace)["snapshot_text"])["jobs"]==[]


def test_matching_lineage_prefix_can_append_but_old_snapshot_cannot_roll_back(local,destination):
    prepared(local);full=local.store.export(local.namespace)
    initial=chain(local.namespace)[:3]
    target_config=json.loads(Path(os.environ["AMS_RECOVERY_RESTORE_CONFIG"]).read_text())
    target_lineage=lineage.Store(target_config["url"],target_config["service_jwt"],rest_path=target_config["rest_path"])
    target_lineage.append(initial,expected_head=None)
    older=destination.export(local.namespace)
    imported=destination.restore(full,expected_head=older["source_head"],expected_manifest_digest=full["manifest_digest"])
    assert imported["head"]==full["source_head"]
    with rejected("PT409"):
        destination.restore(older,expected_head=full["source_head"],expected_manifest_digest=older["manifest_digest"])
    assert destination.snapshot(local.namespace)["head"]==full["source_head"]


@pytest.mark.parametrize("field",["manifest_text","manifest_digest","expected_manifest_digest","expected_head"])
def test_raw_invalid_restore_pin_types_refuse_atomically(local,destination,field):
    prepared(local);manifest=local.store.export(local.namespace)
    payload={k:v for k,v in manifest.items() if k!="manifest_digest"}
    request={"manifest_text":recovery.canonical(payload),"manifest_digest":manifest["manifest_digest"],
        "expected_manifest_digest":manifest["manifest_digest"],"expected_head":None,
        "reader_digest":recovery.reader_digest(),"schema_digest":recovery.schema_digest()}
    request[field]={} if field=="expected_head" else None
    before=destination.snapshot(local.namespace)
    with rejected("23514"):destination._rpc("restore",request,mutating=True)
    assert destination.snapshot(local.namespace)==before


def test_matching_preexisting_canonical_parents_restore_without_raw_evidence(local,destination):
    # A separately provisioned canonical-reference schema fixture, never a
    # synthetic lineage chain relabeled as observed model measurements.
    fixture=local.config.get("canonical_parent_fixture")
    if fixture is None:pytest.skip("matching canonical-parent fixture not supplied")
    namespace="test-canonical-restore-"+uuid.uuid4().hex
    target_config=json.loads(Path(os.environ["AMS_RECOVERY_RESTORE_CONFIG"]).read_text())
    source=lineage.Store(local.config["url"],local.config["service_jwt"],rest_path=local.config["rest_path"])
    target=lineage.Store(target_config["url"],target_config["service_jwt"],rest_path=target_config["rest_path"])
    refs={}
    for table,key in (("rsi_runs","run_id"),("rsi_results","result_id")):
        source_rows=source._call("GET",table+"?id=eq."+str(fixture[key]))
        assert len(source_rows)==1 and source_rows==target._call("GET",table+"?id=eq."+str(fixture[key]))
        refs[table]=source_rows[0]
        assert refs[table]["is_test"] is True and refs[table]["model"]=="no-model-call"
        for config in (local.config,target_config):
            public=lineage.Store(config["url"],config["anon_jwt"],rest_path=config["rest_path"])
            assert public._call("GET",table+"?id=eq."+str(fixture[key]))==[]
    assert refs["rsi_results"]["execution_state"]=="runner_error" and refs["rsi_results"]["passed"] is None
    def record(kind,name,parents,attributes):
        return dict(namespace=namespace,kind=kind,record_id=name,parents=parents,attributes=attributes,
                    source_commit="a"*40,artifact_digest="b"*64,occurred_at="2026-11-06T00:00:00Z",
                    is_test=True,synthetic=False)
    records=[
        record("failure","fixture-occurrence",{},dict(failure_id="schema-fixture-only",family="canonical-restore-fixture",chain_id="canonical-restore-fixture")),
        record("case","case-v1",dict(failure="fixture-occurrence"),dict(version=1,rsi_task_id=refs["rsi_results"]["task_id"])),
        record("candidate","baseline",dict(case="case-v1"),dict(attempt=0,skills_commit="c"*40)),
        record("candidate","candidate-1",dict(case="case-v1",previous_candidate="baseline"),dict(attempt=1,skills_commit="d"*40)),
        record("comparison","fixture-comparison",dict(case="case-v1",current_candidate="baseline",candidate="candidate-1"),dict(campaign_id="canonical-fixture-only",contract_digest="e"*64)),
        record("run","fixture-run",dict(comparison="fixture-comparison",candidate="candidate-1"),dict(run_key=refs["rsi_runs"]["run_key"],rsi_run_id=fixture["run_id"])),
        record("result","fixture-result",dict(run="fixture-run"),dict(execution_state="runner_error",passed=None,rsi_result_id=fixture["result_id"])),
    ]
    source.append(records,expected_head=None)
    from test_recovery import job
    definition=job(namespace);definition.update(synthetic=False,campaign_id="canonical-fixture-only")
    local.store.create_job(definition)
    manifest=local.store.export(namespace)
    projection=json.loads(manifest["snapshot_text"])
    assert len(projection["externals"])==2
    assert all(row.keys()=={"table","id","digest"} for row in projection["externals"])
    assert all(not json.loads(row["record_text"])["synthetic"] for row in projection["lineage"])
    assert all(json.loads(row["record_text"])["is_test"] for row in projection["lineage"])
    restored=destination.restore(manifest,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    assert restored["restored"] is True and restored["head"]==manifest["source_head"]
    assert target.read(namespace)==records
    assert destination.restore(manifest,expected_head=restored["head"],expected_manifest_digest=manifest["manifest_digest"])["restored"] is False


@pytest.mark.parametrize("field",["projection","effect-state","observation-outcome","slot-role","slot-effect-type"])
def test_raw_restore_null_enums_refuse_without_partial_write(local,destination,field):
    claimed=local.store.claim(prepared(local),"source")
    reserved=local.store.begin_effect(claimed,0)
    observed=recovery.KeyedFileEffect(local.root).lookup(reserved["effect"]["effect_key"],reserved["effect"]["payload_digest"])
    local.store.observe_effect(reserved["job"],reserved["effect"]["effect_key"],observed)
    manifest=local.store.export(local.namespace)
    def mutate(data):
        if field.startswith("slot-"):
            definition=json.loads(data["jobs"][0]["job_text"])
            definition["slots"][0]["role" if field=="slot-role" else "effect_type"]=None
            data["jobs"][0].update(job_text=recovery.canonical(definition),job_digest=recovery.digest(definition))
        elif field=="effect-state":data["effects"][0]["state"]=None
        elif field=="observation-outcome":
            observation=json.loads(data["effects"][0]["observation_text"]);observation["outcome"]=None
            data["effects"][0]["observation_text"]=recovery.canonical(observation)
    forged=resign(manifest,mutate)
    if field=="projection":
        forged["projection"]=None
        forged["manifest_digest"]=recovery.digest({k:v for k,v in forged.items() if k!="manifest_digest"})
    before=destination.snapshot(local.namespace)
    with rejected("23514"):raw_restore(destination,forged)
    assert destination.snapshot(local.namespace)==before
