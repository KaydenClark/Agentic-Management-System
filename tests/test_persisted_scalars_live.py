"""Raw PostgREST inputs must retain the reader's scalar types and exact bytes."""
from copy import deepcopy
import json
import hashlib
import pytest
from ams import lineage,recovery,writer
from test_lineage import chain
from test_recovery import job
from test_recovery_live import local,prepared


def raw_snapshot(local,namespace):
    return local.store._rpc("snapshot",{"namespace":namespace})


def raw_append(local,namespace,records,transform=lambda text:text):
    return writer._call(writer.urllib_http,"POST",local.config["url"]+local.config["rest_path"]+"/rpc/"+lineage.RPC,
        local.config["service_jwt"],{"p_namespace":namespace,"p_expected_head":None,
        "p_records":[{"record_text":transform(lineage.canonical(row)),
                      "record_digest":hashlib.sha256(transform(lineage.canonical(row)).encode()).hexdigest()} for row in records]})


@pytest.mark.parametrize("field",["proof_digest","payload_digest"])
def test_raw_observation_numeric_digest_cannot_poison_export(local,field):
    definition=job(local.namespace);definition["slots"][0]["payload_digest"]="7"*64
    reserved=local.store.begin_effect(local.store.claim(prepared(local,slots=definition["slots"]),"owner"),0)
    effect=reserved["effect"]
    observation=dict(effect_key=effect["effect_key"],payload_digest=effect["payload_digest"],outcome="absent",
                     object_id=None,artifact_digest=None,proof_digest="7"*64)
    observation[field]=int("7"*64);before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:
        local.store._rpc("observe",{**local.store._fenced(reserved["job"]),"effect_key":effect["effect_key"],
            "observation_text":lineage.canonical(observation),"observation_digest":lineage.digest(observation)},mutating=True)
    assert refused.value.database_code=="23514"
    assert raw_snapshot(local,local.namespace)==before
    local.store.export(local.namespace)


@pytest.mark.parametrize("field",["record_id","source_commit","artifact_digest"])
def test_raw_lineage_numeric_identity_or_pin_refuses_atomically(local,field):
    namespace=local.namespace+"-scalar";records=chain(namespace)[:1]
    records[0][field]=7 if field=="record_id" else int("7"*(40 if field=="source_commit" else 64))
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


def digit_chain(namespace):
    records=chain(namespace);mapping={row["record_id"]:str(i) for i,row in enumerate(records,1)}
    for row in records:
        row["record_id"]=mapping[row["record_id"]];row["parents"]={key:mapping[value] for key,value in row["parents"].items()}
        row.update(source_commit="9"*40,artifact_digest="7"*64)
        for key,value in row["attributes"].items():
            if type(value) is str and key not in ("execution_state","decision","outcome"):
                row["attributes"][key]="7"*(40 if key.endswith("commit") else 64 if key.endswith("digest") else 1)
    records[3]["attributes"]["skills_commit"]="8"*40
    records[8]["attributes"]["adopted_commit"]="8"*40
    return records


PARENTS=[pytest.param(i,role,id=row["kind"]+"-"+role) for i,row in enumerate(chain()) for role in row["parents"]]


@pytest.mark.parametrize("index,role",PARENTS)
def test_raw_numeric_parent_does_not_alias_digit_string_identity(local,index,role):
    namespace=local.namespace+"-parents";records=digit_chain(namespace)
    records[index]["parents"][role]=int(records[index]["parents"][role])
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


ATTR_STRINGS=[pytest.param(i,key,id=row["kind"]+"-"+key) for i,row in enumerate(chain())
              for key,value in row["attributes"].items() if type(value) is str and value not in ("completed","retained","success")]


@pytest.mark.parametrize("index,key",ATTR_STRINGS)
def test_raw_numeric_attribute_never_replaces_string_pin(local,index,key):
    namespace=local.namespace+"-attrs";records=digit_chain(namespace)
    records[index]["attributes"][key]=int(records[index]["attributes"][key])
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("key",["is_test","synthetic"])
@pytest.mark.parametrize("value",[1,"true",None])
def test_raw_lineage_boolean_type_is_not_coerced(local,key,value):
    namespace=local.namespace+"-bool";records=chain(namespace);records[0][key]=value
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("index,key",[(1,"version"),(3,"attempt"),(5,"rsi_run_id"),(6,"rsi_result_id")])
@pytest.mark.parametrize("value",[1.0,True,"1",None])
def test_raw_lineage_integer_representation_is_preserved(local,index,key,value):
    namespace=local.namespace+"-ints";records=chain(namespace);records[index]["attributes"][key]=value
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("transform",[
    pytest.param(lambda text:json.dumps(json.loads(text)),id="whitespace"),
    pytest.param(lambda text:text.replace('"version":1','"version":1e0'),id="integer-exponent"),
    pytest.param(lambda text:text.replace('"record_id":"1"',r'"record_id":"\u0031"'),id="escaped-id"),
])
def test_noncanonical_lineage_bytes_refuse_before_reader_poison(local,transform):
    namespace=local.namespace+"-bytes";before=raw_snapshot(local,namespace)
    status,body=raw_append(local,namespace,digit_chain(namespace),transform)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("timestamp",["2026-11-06T24:00:00Z","2026-11-06T23:59:60Z"])
def test_database_timestamp_must_fit_python_reader(local,timestamp):
    namespace=local.namespace+"-time";records=chain(namespace)[:1];records[0]["occurred_at"]=timestamp
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("key",sorted(recovery.JOB_FIELDS-{"slots","is_test","synthetic"}))
def test_raw_job_identity_fields_require_json_strings(local,key):
    value=job(local.namespace);value[key]=int("7"*(40 if key.endswith("commit") else 64 if key.endswith("digest") else 1))
    before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:
        local.store._rpc("create",{"job_text":lineage.canonical(value),"job_digest":lineage.digest(value)},mutating=True)
    assert refused.value.database_code=="23514"
    assert raw_snapshot(local,local.namespace)==before


@pytest.mark.parametrize("where",["job","job-exponent","observation","slot-key","slot-key-exponent"])
def test_noncanonical_recovery_bytes_cannot_persist(local,where):
    before=raw_snapshot(local,local.namespace)
    if where.startswith("job"):
        value=job(local.namespace);text=json.dumps(value) if where=="job" else lineage.canonical(value).replace('"repetition":1','"repetition":1e0')
        request={"job_text":text,"job_digest":hashlib.sha256(text.encode()).hexdigest()};action="create"
    else:
        reserved=local.store.begin_effect(local.store.claim(prepared(local),"owner"),0);effect=reserved["effect"]
        request={**local.store._fenced(reserved["job"]),"effect_key":effect["effect_key"]}
        if where=="observation":
            value=recovery.KeyedFileEffect(local.root).lookup(effect["effect_key"],effect["payload_digest"]);text=json.dumps(value)
            request.update(observation_text=text,observation_digest=hashlib.sha256(text.encode()).hexdigest());action="observe"
        else:
            definition=recovery._job(reserved["job"]);material=recovery.key_material(definition,definition["slots"][0])
            text=json.dumps(material) if where=="slot-key" else lineage.canonical(material).replace('"repetition":1','"repetition":1e0')
            request.update(slot_index=0,key_text=text,effect_key=hashlib.sha256(text.encode()).hexdigest());action="begin"
        before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:local.store._rpc(action,request,mutating=True)
    assert refused.value.database_code=="23514"
    assert raw_snapshot(local,local.namespace)==before


@pytest.mark.parametrize("field",["namespace","kind","occurred_at"])
def test_raw_lineage_remaining_root_strings_require_types(local,field):
    namespace=local.namespace+"-roots";records=chain(namespace)[:1];records[0][field]=7
    before=raw_snapshot(local,namespace);status,body=raw_append(local,namespace,records)
    assert status==400 and body["code"]=="23514"
    assert raw_snapshot(local,namespace)==before


@pytest.mark.parametrize("key",["is_test","synthetic"])
def test_raw_job_boolean_fields_do_not_accept_integer_labels(local,key):
    value=job(local.namespace);value[key]=1;before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:
        local.store._rpc("create",{"job_text":lineage.canonical(value),"job_digest":lineage.digest(value)},mutating=True)
    assert refused.value.database_code=="23514" and raw_snapshot(local,local.namespace)==before


@pytest.mark.parametrize("where",["job-id","arm","object-id"])
def test_raw_safe_id_rules_match_private_reader(local,where):
    if where in ("job-id","arm"):
        value=job(local.namespace)
        if where=="job-id":value["job_id"]="sk-fixture"
        else:value["slots"][0]["arm"]="sk-fixture"
        action="create";request={"job_text":lineage.canonical(value),"job_digest":lineage.digest(value)}
    else:
        reserved=local.store.begin_effect(local.store.claim(prepared(local),"owner"),0);effect=reserved["effect"]
        value=recovery.KeyedFileEffect(local.root).lookup(effect["effect_key"],effect["payload_digest"]);value["object_id"]="sk-fixture"
        action="observe";request={**local.store._fenced(reserved["job"]),"effect_key":effect["effect_key"],
            "observation_text":lineage.canonical(value),"observation_digest":lineage.digest(value)}
    before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:local.store._rpc(action,request,mutating=True)
    assert refused.value.database_code=="23514" and raw_snapshot(local,local.namespace)==before


from test_recovery_checkpoint_live import destination,resign,raw_restore


@pytest.mark.parametrize("category,key,value",[
    ("lineage","ordinal","1"),("lineage","format_version","1"),("lineage","record_digest",7),("lineage","previous_digest",7),
    ("jobs","attempt","1"),("jobs","version","1"),("jobs","fence","1"),("jobs","chain_id",7),("jobs","evidence_digest",7),
    ("effects","intent_fence","1"),("effects","version","1"),("effects","payload_digest",7),
    ("effects","observation_text",7),("effects","receipt_digest",7),
])
def test_raw_restore_projection_scalar_types_are_not_reinterpreted(local,destination,category,key,value):
    reserved=local.store.begin_effect(local.store.claim(prepared(local),"owner"),0)
    manifest=local.store.export(local.namespace)
    forged=resign(manifest,lambda data:data[category][0].update({key:value}))
    before=raw_snapshot(local,local.namespace);target_before=destination.snapshot(local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:raw_restore(destination,forged)
    assert refused.value.database_code=="23514"
    assert destination.snapshot(local.namespace)==target_before and raw_snapshot(local,local.namespace)==before


def test_digit_string_identities_and_pins_survive_full_chain_export_restore(local,destination):
    from datetime import datetime,timezone
    namespace=local.namespace+"-digits";records=digit_chain(namespace)
    source=lineage.Store(local.config["url"],local.config["service_jwt"],rest_path=local.config["rest_path"])
    source.append(records,expected_head=None);assert source.read(namespace)==records
    definition=job(namespace,job_id="7");definition.update(case_id="2",candidate_id="4",case_digest="7"*64,
        skills_commit="8"*40,source_commit="9"*40,release_digest="7"*64)
    definition["slots"][0].update(arm="7",payload_digest="7"*64)
    created=local.store.create_job(definition)
    gated=local.store.gates(created,approved=True,capacity="available",observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="7"*64)
    reserved=local.store.begin_effect(local.store.claim(gated,"7"),0);effect=reserved["effect"]
    observation=dict(effect_key=effect["effect_key"],payload_digest="7"*64,outcome="absent",object_id=None,artifact_digest=None,proof_digest="7"*64)
    local.store.observe_effect(reserved["job"],effect["effect_key"],observation)
    manifest=local.store.export(namespace);assert manifest["counts"]["lineage"]==10
    copied=destination.restore(manifest,expected_head=None,expected_manifest_digest=manifest["manifest_digest"])
    assert copied["restored"] and copied["head"]==manifest["source_head"]
    projection=json.loads(destination.snapshot(namespace)["snapshot_text"])
    assert all(json.loads(row["record_text"])["synthetic"] for row in projection["lineage"])
    observed=json.loads(projection["effects"][0]["observation_text"])
    assert observed["payload_digest"]==observed["proof_digest"]=="7"*64
    assert destination.restore(manifest,expected_head=copied["head"],expected_manifest_digest=manifest["manifest_digest"])["restored"] is False


@pytest.mark.parametrize("action,field",[("claim","claimant"),("gates","capacity_digest"),("finish","evidence_digest")])
def test_control_identity_and_digest_strings_are_not_coerced(local,action,field):
    from datetime import datetime,timezone
    ready=prepared(local);current=local.store.claim(ready,"owner") if action=="finish" else ready
    request=local.store._fenced(current) if action=="finish" else local.store._handle(current)
    if action=="claim":request.update(claimant="7",lease_seconds=30)
    if action=="gates":request.update(approved=True,capacity="available",observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),capacity_digest="7"*64,stopped=False)
    if action=="finish":request.update(state="blocked",evidence_digest="7"*64)
    request[field]=int(request[field]);before=raw_snapshot(local,local.namespace)
    with pytest.raises(recovery.DatabaseRefused) as refused:local.store._rpc(action,request,mutating=True)
    assert refused.value.database_code=="23514" and raw_snapshot(local,local.namespace)==before
