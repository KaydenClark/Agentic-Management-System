"""Opt-in real PostgreSQL/REST concurrency and restart proof in isolated namespaces."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import dataclass,field
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlparse
import uuid

import pytest

from ams import lineage,recovery,writer
from test_lineage import chain
from test_recovery import job


@dataclass
class Local:
    store: recovery.Store
    config:dict=field(repr=False)
    config_path:str=field(repr=False)
    namespace:str
    root:Path


@pytest.fixture
def local(tmp_path):
    filename=os.environ.get("AMS_LINEAGE_TEST_CONFIG")
    if not filename:pytest.skip("isolated Supabase config not supplied")
    config=json.loads(Path(filename).read_text())
    assert urlparse(config["url"]).hostname in ("127.0.0.1","localhost")
    namespace="test-recovery-"+uuid.uuid4().hex
    lineage.Store(config["url"],config["service_jwt"],rest_path=config["rest_path"]).append(chain(namespace)[:5],expected_head=None)
    store=recovery.Store(config["url"],config["service_jwt"],rest_path=config["rest_path"],pending_dir=tmp_path/"pending")
    return Local(store,config,filename,namespace,tmp_path)


def prepared(local,*,slots=None):
    value=job(local.namespace)
    if slots is not None:value["slots"]=slots
    saved=local.store.create_job(value)
    return local.store.gates(saved,approved=True,capacity="available",
        observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="f"*64)


def worker(local,mode,claimant,*,version=None):
    objects=local.root/"objects";objects.mkdir(exist_ok=True)
    args=[sys.executable,str(Path(__file__).with_name("recovery_worker.py")),mode,local.config_path,
          local.namespace,str(objects),str(local.root/(claimant+"-pending")),claimant]
    if version is not None:args += ["--expected-version",str(version)]
    # No inherited provider/database credentials enter the probe process.
    env={key:value for key,value in os.environ.items() if key in ("PATH","PYTHONPATH","LANG","LC_ALL")}
    return subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)


def test_duplicate_intake_and_competing_processes_execute_one_effect(local):
    ready=prepared(local)
    assert local.store.create_job(job(local.namespace))["job_id"]=="job-1"
    workers=[worker(local,"race",name,version=ready["version"]) for name in ("worker-a","worker-b")]
    results=[]
    for process in workers:
        out,err=process.communicate(timeout=30)
        assert process.returncode==0,err
        results.append(json.loads(out))
    assert sum(result["executed"] for result in results)==1
    assert sum(result["won"] for result in results)==1
    assert len(list((local.root/"objects").iterdir()))==1
    saved=local.store.get_job(local.namespace,"job-1")
    assert saved["state"]=="completed" and saved["attempt"]==1


def test_crash_after_effect_recovers_in_fresh_process_without_repeating_slot(local):
    prepared(local)
    first=worker(local,"crash","crashed-worker");out,err=first.communicate(timeout=30)
    assert first.returncode==23,err
    objects=list((local.root/"objects").iterdir());assert len(objects)==1
    before=objects[0].stat();time.sleep(1.1)
    second=worker(local,"recover","fresh-worker");out,err=second.communicate(timeout=30)
    assert second.returncode==0,err
    result=json.loads(out)
    assert result["executed"] is False and result["effect_key"]==objects[0].name
    assert objects[0].stat().st_mtime_ns==before.st_mtime_ns
    saved=local.store.get_job(local.namespace,"job-1")
    assert saved["fence"]==2 and saved["state"]=="completed" and saved["attempt"]==1


def test_stale_fence_cannot_publish_receipt(local):
    ready=prepared(local)
    first=local.store.claim(ready,"first",lease_seconds=1)
    reserved=local.store.begin_effect(first,0)
    adapter=recovery.KeyedFileEffect(local.root)
    observed=adapter.apply(reserved["effect"]["effect_key"],b"safe synthetic effect")
    time.sleep(1.1)
    # Correct version/fence still cannot publish after lease expiry.
    with pytest.raises(recovery.DatabaseRefused) as expired:
        local.store.observe_effect(local.store.get_job(local.namespace,"job-1"),reserved["effect"]["effect_key"],observed)
    assert expired.value.database_code=="PT409"
    second=local.store.claim(local.store.get_job(local.namespace,"job-1"),"second",lease_seconds=30)
    with pytest.raises(recovery.Refused,match="HTTP 409"):
        local.store.observe_effect(reserved["job"],reserved["effect"]["effect_key"],observed)
    # Correct current version/actor with only the old fence also refuses.
    wrong_fence=deepcopy(second);wrong_fence["fence"]=first["fence"]
    with pytest.raises(recovery.DatabaseRefused) as fenced:
        local.store.observe_effect(wrong_fence,reserved["effect"]["effect_key"],observed)
    assert fenced.value.database_code=="PT409"
    recovered=local.store.begin_effect(second,0)
    assert recovered["execute"] is False
    sealed=local.store.observe_effect(recovered["job"],reserved["effect"]["effect_key"],observed)
    assert sealed["effect"]["state"]=="completed"


@pytest.mark.parametrize("gate",["approval","capacity","stop"])
def test_release_boundaries_refuse_new_effects(local,gate):
    saved=local.store.create_job(job(local.namespace))
    gated=local.store.gates(saved,approved=gate!="approval",capacity="unknown" if gate=="capacity" else "available",
        observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="f"*64,stopped=gate=="stop")
    if gate=="stop":
        with pytest.raises(recovery.Refused,match="HTTP 409"):local.store.claim(gated,"worker")
    else:
        claimed=local.store.claim(gated,"worker")
        with pytest.raises(recovery.Refused,match="HTTP 409"):local.store.begin_effect(claimed,0)


def test_unknown_or_absent_native_completion_does_not_rearm_model_slot(local):
    slot=job(local.namespace)["slots"][0];slot.update(role="worker",effect_type="native-call")
    ready=prepared(local,slots=[slot]);claimed=local.store.claim(ready,"worker")
    reserved=local.store.begin_effect(claimed,0)
    adapter=recovery.KeyedFileEffect(local.root)
    observation=adapter.lookup(reserved["effect"]["effect_key"],slot["payload_digest"])
    assert observation["outcome"]=="absent"
    absent=local.store.observe_effect(reserved["job"],reserved["effect"]["effect_key"],observation)
    with pytest.raises(recovery.Refused,match="HTTP 409"):
        local.store.retry_keyed_absent(absent["job"],reserved["effect"]["effect_key"])
    again=local.store.begin_effect(absent["job"],0)
    assert again["execute"] is False and again["reconcile"] is True


def test_private_operations_and_direct_service_writes_are_denied(local):
    saved=prepared(local)
    for key in (local.config["anon_jwt"],local.config["authenticated_jwt"]):
        for method,path,payload in [("GET","rsi_jobs",None),("GET","rsi_effects",None),
            ("POST","rpc/"+recovery.RPC,{"p_action":"get","p_request":{"namespace":local.namespace,"job_id":"job-1"}})]:
            status,body=writer._call(writer.urllib_http,method,local.config["url"]+local.config["rest_path"]+"/"+path,key,payload)
            assert writer._denied(status,body),(method,status)
    for table in ("rsi_jobs","rsi_effects"):
        for method,payload in (("POST",{}),("PATCH",{"version":99}),("DELETE",None)):
            status,body=writer._call(writer.urllib_http,method,
                local.config["url"]+local.config["rest_path"]+"/"+table+"?namespace=eq."+local.namespace,
                local.config["service_jwt"],payload)
            assert writer._denied(status,body),(table,method,status)
    assert local.store.get_job(local.namespace,"job-1")["version"]==saved["version"]


def test_equivalent_slot_encoding_cannot_reserve_another_effect(local):
    ready=prepared(local);claimed=local.store.claim(ready,"worker")
    reserved=local.store.begin_effect(claimed,0)
    definition=recovery._job(reserved["job"])
    material=recovery.key_material(definition,definition["slots"][0])
    differently_encoded=json.dumps(material,indent=2)
    request={**local.store._fenced(reserved["job"]),"slot_index":0,"key_text":differently_encoded,
             "effect_key":hashlib.sha256(differently_encoded.encode()).hexdigest()}
    with pytest.raises(recovery.DatabaseRefused) as duplicate:
        local.store._rpc("begin",request,mutating=True)
    assert duplicate.value.database_code=="23514"


def test_renew_release_and_same_label_cannot_steal_active_claim(local):
    ready=prepared(local);claimed=local.store.claim(ready,"owner")
    with pytest.raises(recovery.DatabaseRefused) as duplicate:
        local.store.claim(claimed,"owner")
    assert duplicate.value.database_code=="PT409"
    renewed=local.store.renew(claimed,lease_seconds=30)
    assert renewed["fence"]==claimed["fence"] and renewed["version"]>claimed["version"]
    released=local.store.release(renewed)
    assert released["lease_until"] is None and released["claimant"] is None
    next_owner=local.store.claim(released,"next")
    assert next_owner["fence"]>claimed["fence"]
    reserved=local.store.begin_effect(next_owner,0)
    with pytest.raises(recovery.DatabaseRefused) as incomplete:
        local.store.finish(reserved["job"],"completed",evidence_digest="f"*64)
    assert incomplete.value.database_code=="23514"


def test_renamed_released_job_cannot_repeat_consumed_slot(local):
    ready=prepared(local);claimed=local.store.claim(ready,"first")
    original=local.store.begin_effect(claimed,0)
    changed=job(local.namespace,job_id="renamed-job");changed.update(campaign_id="new-label",release_digest="1"*64)
    created=local.store.create_job(changed)
    gated=local.store.gates(created,approved=True,capacity="available",observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="f"*64)
    second=local.store.claim(gated,"second")
    with pytest.raises(recovery.DatabaseRefused) as duplicate:
        local.store.begin_effect(second,0)
    assert duplicate.value.database_code=="PT409"
    assert original["job"]["attempt"]==second["attempt"]==1


def test_actual_transport_outage_preserves_intake_for_idempotent_readback(local):
    # An actual unbound loopback endpoint, not a mocked HTTP result.
    import socket
    with socket.socket() as socket_probe:
        socket_probe.bind(("127.0.0.1",0));port=socket_probe.getsockname()[1]
    pending=local.root/"outage-pending"
    unavailable=recovery.Store("http://127.0.0.1:"+str(port),local.config["service_jwt"],rest_path="",pending_dir=pending)
    with pytest.raises(recovery.Unavailable):unavailable.create_job(job(local.namespace))
    files=list(pending.glob("*.pending.json"));assert len(files)==1
    assert local.config["service_jwt"] not in files[0].read_text()
    assert local.store.get_job(local.namespace,"job-1") is None
    saved=local.store.create_job(job(local.namespace))
    assert local.store.create_job(job(local.namespace))["job_digest"]==saved["job_digest"]
    assert local.store.get_job(local.namespace,"job-1")["version"]==1
