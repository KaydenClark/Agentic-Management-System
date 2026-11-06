"""Raw service RPC type checks at the authoritative SQL seam."""
import pytest
from ams import recovery
from test_recovery import job
from test_recovery_live import local,prepared

INVALID_ENUMS=[pytest.param(None,id="null"),pytest.param("omitted",id="missing"),
              pytest.param(7,id="number"),pytest.param(False,id="boolean"),
              pytest.param([],id="array"),pytest.param({},id="object"),pytest.param("unsupported",id="unknown")]


def altered(value,key,replacement):
    if replacement=="omitted":value.pop(key)
    else:value[key]=replacement


@pytest.mark.parametrize("field",["role","effect_type"])
@pytest.mark.parametrize("invalid",INVALID_ENUMS)
def test_raw_job_slot_enum_refuses_atomically(local,field,invalid):
    value=job(local.namespace);altered(value["slots"][0],field,invalid)
    before=local.store.snapshot(local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:
        local.store._rpc("create",{"job_text":recovery.canonical(value),"job_digest":recovery.digest(value)},mutating=True)
    assert refused.value.database_code=="23514"
    assert local.store.snapshot(local.namespace)==before


@pytest.mark.parametrize("invalid",INVALID_ENUMS)
def test_raw_observation_enum_refuses_atomically(local,invalid):
    reserved=local.store.begin_effect(local.store.claim(prepared(local),"owner"),0)
    effect=reserved["effect"]
    observed=recovery.KeyedFileEffect(local.root).lookup(effect["effect_key"],effect["payload_digest"])
    altered(observed,"outcome",invalid);before=local.store.snapshot(local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:
        local.store._rpc("observe",{**local.store._fenced(reserved["job"]),"effect_key":effect["effect_key"],
            "observation_text":recovery.canonical(observed),"observation_digest":recovery.digest(observed)},mutating=True)
    assert refused.value.database_code=="23514"
    assert local.store.snapshot(local.namespace)==before


@pytest.mark.parametrize("effect_type",["keyed-file","native-call"])
def test_absent_retry_requires_explicit_keyed_contract(local,effect_type):
    value=job(local.namespace);value["slots"][0]["effect_type"]=effect_type
    ready=prepared(local,slots=value["slots"])
    reserved=local.store.begin_effect(local.store.claim(ready,"owner"),0)
    observed=recovery.KeyedFileEffect(local.root).lookup(reserved["effect"]["effect_key"],reserved["effect"]["payload_digest"])
    absent=local.store.observe_effect(reserved["job"],reserved["effect"]["effect_key"],observed)
    before=local.store.snapshot(local.namespace)
    if effect_type=="keyed-file":
        retried=local.store.retry_keyed_absent(absent["job"],absent["effect"]["effect_key"])
        assert retried["execute"] is True and retried["effect"]["effect_key"]==reserved["effect"]["effect_key"]
    else:
        with pytest.raises(recovery.DatabaseRefused) as refused:
            local.store.retry_keyed_absent(absent["job"],absent["effect"]["effect_key"])
        assert refused.value.database_code=="PT409"
        assert local.store.snapshot(local.namespace)==before


@pytest.mark.parametrize("action,field,code",[
    ("claim","expected_version","PT409"),("claim","claimant","23514"),("claim","lease_seconds","23514"),
    ("gates","approved","23514"),("gates","capacity","23514"),("gates","observed_at","23514"),
    ("renew","lease_seconds","23514"),("renew","fence","23514"),
    ("release","claimant","23514"),("finish","state","23514"),("begin","slot_index","23514"),
])
def test_raw_null_control_parameters_refuse_without_state_change(local,action,field,code):
    ready=prepared(local)
    current=local.store.claim(ready,"owner") if action in ("renew","release","finish","begin") else ready
    request=local.store._fenced(current) if action in ("renew","release","finish","begin") else local.store._handle(current)
    if action in ("claim","renew"):request.update(claimant="owner",lease_seconds=30)
    if action=="gates":request.update(approved=True,capacity="available",observed_at="2026-11-06T00:00:00Z",capacity_digest="f"*64,stopped=False)
    if action=="finish":request.update(state="blocked",evidence_digest="f"*64)
    if action=="begin":
        definition=recovery._job(current);material=recovery.key_material(definition,definition["slots"][0])
        request.update(slot_index=0,key_text=recovery.canonical(material),effect_key=recovery.digest(material))
    request[field]=None;before=local.store.snapshot(local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:local.store._rpc(action,request,mutating=True)
    assert refused.value.database_code==code
    assert local.store.snapshot(local.namespace)==before
