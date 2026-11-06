"""Real isolated checkpoint restore; no live authorization is restored."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import os
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
        with pytest.raises(recovery.Refused,match="HTTP 409"):
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
    with pytest.raises(recovery.Refused,match="HTTP 409"):
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
    with pytest.raises(recovery.Refused,match="HTTP 4"):
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
        with pytest.raises(recovery.Refused,match="HTTP 4"):
            raw_restore(destination,forged)
    assert json.loads(destination.snapshot(local.namespace)["snapshot_text"])["jobs"]==[]
