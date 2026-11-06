"""Private durable job/effect recovery; no model or external tool is invoked.

The controller owns permission, capacity and effect-specific reconciliation.
A consumed native slot is never repeated just because its lease expired.
Checkpoints preserve a declared safe projection, not live lease authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import uuid

from ams import lineage, writer

Refused, Unavailable = lineage.Refused, lineage.Unavailable
require, canonical, digest = lineage.require, lineage.canonical, lineage.digest
RPC = "ams_recovery"
FORMAT = 1
PROJECTION = "safe-lineage-job-effects-v1"
SNAPSHOT_KINDS = ("lineage","jobs","effects","externals")
JOB_FIELDS = {"namespace", "job_id", "spec_id", "task_id", "campaign_id", "case_id", "candidate_id",
              "case_digest", "skills_commit", "release_digest", "source_commit", "is_test", "synthetic", "slots"}
SLOT_FIELDS = {"role", "arm", "repetition", "effect_type", "payload_digest"}
OBS_FIELDS = {"effect_key", "payload_digest", "outcome", "object_id", "artifact_digest", "proof_digest"}
JOB_PROJECTION = {"job_text", "job_digest", "chain_id", "attempt", "version", "fence", "terminal_state", "evidence_digest"}
EFFECT_PROJECTION = {"effect_key", "job_id", "key_text", "payload_digest", "intent_fence", "version", "state", "observation_text", "receipt_digest"}
LINEAGE_PROJECTION = {"ordinal", "record_text", "record_digest", "previous_digest", "format_version"}
MANIFEST_FIELDS = {"format_version", "reader_version", "reader_digest", "schema_digest", "projection", "namespace", "complete",
                   "export_id", "previous_export", "snapshot_text", "source_head", "counts", "records", "manifest_digest"}


class DatabaseRefused(Refused):
    """Only safe HTTP/SQLSTATE metadata, never a database body or input text."""
    def __init__(self,status,body):
        value=body.get("code") if type(body) is dict else None
        self.database_code=value if type(value) is str and re.fullmatch(r"[A-Z0-9]{5}",value) else None
        self.http_status=status
        super().__init__("recovery refused (HTTP "+str(status)+", SQLSTATE "+str(self.database_code)+")")


def _string(value, pattern=lineage.ID):
    return (type(value) is str and pattern.fullmatch(value) and
            not value.startswith(("sb_secret_","sk-")) and not(value.startswith("eyJ") and value.count(".")==2))


def _integer(value, low=0):
    return type(value) is int and low <= value <= 2**63-1


def validate_job(job):
    require(type(job) is dict and job.keys() == JOB_FIELDS, "job fields are allowlisted")
    require(_string(job["namespace"], lineage.NAMESPACE), "invalid namespace")
    for key in JOB_FIELDS - {"namespace", "slots", "is_test", "synthetic"}:
        pattern = lineage.DIGEST if key.endswith("digest") else lineage.COMMIT if key.endswith("commit") else lineage.ID
        require(_string(job[key], pattern), "invalid " + key)
    require(type(job["is_test"]) is bool and type(job["synthetic"]) is bool, "job labels must be booleans")
    require(job["is_test"] == job["namespace"].startswith("test-") and
            (not job["synthetic"] or job["is_test"]), "test/synthetic labels must remain isolated")
    require(type(job["slots"]) is list and 1 <= len(job["slots"]) <= 64, "freeze a finite slot inventory")
    identities = set()
    for slot in job["slots"]:
        require(type(slot) is dict and slot.keys() == SLOT_FIELDS, "slot fields are allowlisted")
        require(slot["role"] in ("worker", "grader", "publication", "checkpoint"), "unsupported slot role")
        require(_string(slot["arm"]) and _integer(slot["repetition"], 1), "invalid frozen slot")
        require(slot["effect_type"] in ("native-call", "keyed-file") and
                _string(slot["payload_digest"], lineage.DIGEST), "invalid effect contract")
        identity = (slot["role"], slot["arm"], slot["repetition"])
        require(identity not in identities, "duplicate frozen execution slot")
        identities.add(identity)
    return job


def key_material(job, slot):
    return {"protocol": FORMAT, "chain_id": job["chain_id"], "attempt": job["attempt"],
            "case_digest": job["case_digest"], "role": slot["role"], "arm": slot["arm"],
            "repetition": slot["repetition"]}


def effect_key(job, slot):
    return digest(key_material(job, slot))


def validate_observation(value):
    require(type(value) is dict and value.keys() == OBS_FIELDS, "observation fields are allowlisted")
    for key in ("effect_key", "payload_digest", "proof_digest"):
        require(_string(value[key], lineage.DIGEST), "invalid observation digest")
    require(value["outcome"] in ("matched", "absent", "unavailable", "conflict"), "invalid observed outcome")
    require(value["object_id"] is None or _string(value["object_id"]), "unsafe object identity")
    require(value["artifact_digest"] is None or _string(value["artifact_digest"], lineage.DIGEST), "invalid artifact digest")
    require(value["outcome"] != "matched" or (value["object_id"] is not None and value["artifact_digest"] is not None),
            "matching effect needs readback identity")
    return value


def _job(row):
    require(type(row) is dict and type(row.get("job_text")) is str, "malformed job readback")
    try: value=json.loads(row["job_text"])
    except ValueError: raise Refused("malformed job artifact") from None
    validate_job(value)
    require(canonical(value)==row["job_text"] and digest(value)==row.get("job_digest"), "job identity/digest changed")
    require(all(key not in row or row[key]==value[key] for key in
                ("namespace","job_id","candidate_id","case_digest","release_digest")),"job row projection differs")
    require(_string(row.get("chain_id")) and _integer(row.get("attempt")) and row["attempt"] <= 3 and
            _integer(row.get("version"),1) and _integer(row.get("fence")) and row["version"]>row["fence"],
            "invalid job high-water identity")
    return {**value, "chain_id": row["chain_id"], "attempt": row["attempt"]}


def _snapshot(text):
    try: value=json.loads(text)
    except (ValueError,TypeError): raise Refused("malformed recovery snapshot") from None
    require(type(value) is dict and value.keys()=={"namespace",*SNAPSHOT_KINDS}, "snapshot fields are allowlisted")
    require(_string(value["namespace"],lineage.NAMESPACE),"invalid snapshot namespace")
    for key in SNAPSHOT_KINDS:require(type(value[key]) is list,"incomplete snapshot")
    records=[];previous=None
    for ordinal,row in enumerate(value["lineage"],1):
        require(type(row) is dict and row.keys()==LINEAGE_PROJECTION,"unsafe lineage projection")
        try: record=json.loads(row["record_text"])
        except (ValueError,TypeError):raise Refused("malformed lineage projection") from None
        require(row["ordinal"]==ordinal and row["format_version"]==lineage.FORMAT and
                row["previous_digest"]==previous and row["record_digest"]==digest(record) and
                canonical(record)==row["record_text"] and record["namespace"]==value["namespace"],"lineage snapshot identity differs")
        records.append(record);previous=row["record_digest"]
    lineage.validate_graph(records);by_id={r["record_id"]:r for r in records};jobs={}
    expected_externals={("rsi_runs",r["attributes"]["rsi_run_id"]) if r["kind"]=="run" else
                        ("rsi_results",r["attributes"]["rsi_result_id"]) for r in records
                        if r["kind"] in ("run","result") and not r["synthetic"]}
    actual_externals=set()
    for row in value["externals"]:
        require(type(row) is dict and row.keys()=={"table","id","digest"} and row["table"] in ("rsi_runs","rsi_results")
                and _integer(row["id"],1) and _string(row["digest"],lineage.DIGEST),"unsafe canonical parent reference")
        identity=(row["table"],row["id"])
        require(identity not in actual_externals,"duplicate canonical parent reference")
        actual_externals.add(identity)
    require(actual_externals==expected_externals,"missing canonical parent reference")
    roots={}
    for record in records:
        roots[record["record_id"]]=(record["attributes"]["chain_id"] if record["kind"]=="failure"
                                   else roots[next(iter(record["parents"].values()))])
    for row in value["jobs"]:
        require(type(row) is dict and row.keys()==JOB_PROJECTION,"unsafe job projection")
        job=_job(row)
        require(job["namespace"]==value["namespace"] and job["job_id"] not in jobs,"job snapshot identity differs")
        case,candidate=by_id.get(job["case_id"]),by_id.get(job["candidate_id"])
        require(case is not None and candidate is not None and case["kind"]=="case" and candidate["kind"]=="candidate",
                "job lineage parents missing")
        require(roots[job["case_id"]]==roots[job["candidate_id"]]==job["chain_id"] and
                candidate["attributes"]["attempt"]==job["attempt"] and
                case["artifact_digest"]==job["case_digest"] and candidate["attributes"]["skills_commit"]==job["skills_commit"] and
                all(job[k]==case[k]==candidate[k] for k in ("is_test","synthetic")),"job source/chain differs")
        require(row["terminal_state"] in (None,"completed","failed","stopped") and
                (row["evidence_digest"] is None or _string(row["evidence_digest"],lineage.DIGEST)),"invalid terminal evidence")
        jobs[job["job_id"]]=(job,row)
    effects={}
    for row in value["effects"]:
        require(type(row) is dict and row.keys()==EFFECT_PROJECTION,"unsafe effect projection")
        require(row["job_id"] in jobs and _string(row["effect_key"],lineage.DIGEST) and
                row["effect_key"] not in effects,"effect parent/identity differs")
        job,saved=jobs[row["job_id"]]
        try: material=json.loads(row["key_text"])
        except (ValueError,TypeError):raise Refused("malformed slot identity") from None
        slot=next((s for s in job["slots"] if key_material(job,s)==material),None)
        require(slot is not None and canonical(material)==row["key_text"] and digest(material)==row["effect_key"] and
                row["payload_digest"]==slot["payload_digest"] and _integer(row["intent_fence"],1) and
                row["intent_fence"]<=saved["fence"] and _integer(row["version"],1),"effect slot/source differs")
        require(row["state"] in ("pending","uncertain","absent","completed"),"invalid effect state")
        if row["observation_text"] is not None:
            try: observed=json.loads(row["observation_text"])
            except (ValueError,TypeError):raise Refused("malformed observation") from None
            validate_observation(observed)
            require(canonical(observed)==row["observation_text"] and observed["effect_key"]==row["effect_key"] and
                    observed["payload_digest"]==row["payload_digest"],"effect readback differs")
        else:observed=None
        require((row["state"]=="pending" and observed is None) or
                (observed is not None and ((row["state"]=="completed" and observed["outcome"]=="matched") or
                  (row["state"]=="absent" and observed["outcome"]=="absent") or
                  (row["state"]=="uncertain" and observed["outcome"] in ("unavailable","conflict")))),
                "effect state/observation differs")
        require((row["state"]=="completed") == (row["receipt_digest"] is not None),"missing or invented effect receipt")
        if row["state"]=="completed":
            require(observed is not None and observed["outcome"]=="matched" and
                    row["receipt_digest"]==digest(observed),"completed receipt differs")
        effects[row["effect_key"]]=row
    for job_id,(_,row) in jobs.items():
        if row["terminal_state"]=="completed":
            owned=[e for e in effects.values() if e["job_id"]==job_id]
            require(len(owned)==len(jobs[job_id][0]["slots"]) and all(e["state"]=="completed" for e in owned),
                    "completed job has missing/pending effects")
    return value


def reader_digest():return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def schema_digest():
    root=Path(__file__).resolve().parents[2]
    return hashlib.sha256((root/"supabase/lineage.sql").read_bytes()+(root/"supabase/recovery.sql").read_bytes()).hexdigest()


def _record_digests(snapshot):
    result=[]
    for kind in SNAPSHOT_KINDS:
        for row in snapshot[kind]:
            rid=(json.loads(row["record_text"])["record_id"] if kind=="lineage" else
                 json.loads(row["job_text"])["job_id"] if kind=="jobs" else row["effect_key"] if kind=="effects"
                 else row["table"]+":"+str(row["id"]))
            result.append({"kind":kind,"id":rid,"text":canonical(row),"digest":digest(row)})
    return result


def validate_checkpoint(manifest):
    require(type(manifest) is dict and manifest.keys()==MANIFEST_FIELDS,"checkpoint fields are allowlisted")
    require(type(manifest["format_version"]) is int and manifest["format_version"]==FORMAT and
            type(manifest["reader_version"]) is int and manifest["reader_version"]==FORMAT and manifest["complete"] is True and
            manifest["reader_digest"]==reader_digest() and manifest["schema_digest"]==schema_digest() and
            manifest["projection"]==PROJECTION,"unsupported checkpoint reader/schema")
    require(_string(manifest["export_id"]) and
            (manifest["previous_export"] is None or _string(manifest["previous_export"],lineage.DIGEST)),"invalid export identity")
    snapshot=_snapshot(manifest["snapshot_text"])
    require(manifest["namespace"]==snapshot["namespace"] and
            manifest["source_head"]==hashlib.sha256(manifest["snapshot_text"].encode()).hexdigest(),"checkpoint head differs")
    require(manifest["counts"]=={k:len(snapshot[k]) for k in SNAPSHOT_KINDS} and
            all(type(n) is int for n in manifest["counts"].values()) and
            manifest["records"]==_record_digests(snapshot),"partial or changed checkpoint")
    require(manifest["manifest_digest"]==digest({k:v for k,v in manifest.items() if k!="manifest_digest"}),"checkpoint manifest digest differs")
    return snapshot


class Store:
    def __init__(self,url,key,http=writer.urllib_http,*,pending_dir,rest_path="/rest/v1"):
        require(rest_path in ("","/rest/v1"),"unsupported REST mount")
        self.url,self._key,self.http=url.rstrip("/"),key,http
        self.pending_dir,self.rest_path=Path(pending_dir),rest_path
        self.pending_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
        require(not self.pending_dir.is_symlink(),"pending directory must be owned and nonsymlink")

    def __repr__(self):return "PrivateRecoveryStore()"

    def _pending(self,action,request):
        value={"action":action,"request":request};text=canonical(value);name=digest(value)
        target=self.pending_dir/(name+".pending.json")
        if not target.exists():
            fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,"w") as f:f.write(text);f.flush();os.fsync(f.fileno())
        else:require(target.read_text()==text,"pending intake identity changed")
        return target

    def _rpc(self,action,request,*,mutating=False):
        pending=self._pending(action,request) if mutating else None
        status,body=writer._call(self.http,"POST",self.url+self.rest_path+"/rpc/"+RPC,self._key,
                                 {"p_action":action,"p_request":request})
        if status is None or status>=500 or (200<=status<300 and type(body) is not dict):
            raise Unavailable("recovery unavailable; original safe request remains pending")
        if not 200<=status<300 and pending is not None:
            pending.replace(pending.with_suffix(".refused.json"))
        if not 200<=status<300:raise DatabaseRefused(status,body)
        if body.get("job") is not None:_job(body["job"])
        if action=="create":require(body.get("job",{}).get("job_text")==request["job_text"],"job creation readback differs")
        if action=="restore":
            expected=json.loads(request["manifest_text"])["source_head"]
            require(body.get("head")==expected,"restored checkpoint readback differs")
        if pending is not None:
            # The server response validates its committed transaction. Preserve
            # the original request as a local receipt copy, never live truth.
            pending.replace(pending.with_suffix(".ack.json"))
        return body

    def create_job(self,job):
        validate_job(job)
        result=self._rpc("create",{"job_text":canonical(job),"job_digest":digest(job)},mutating=True)
        require(result.get("job",{}).get("job_text")==canonical(job),"job creation readback differs")
        return result["job"]

    def get_job(self,namespace,job_id):
        require(_string(namespace,lineage.NAMESPACE) and _string(job_id),"invalid job location")
        return self._rpc("get",{"namespace":namespace,"job_id":job_id})["job"]

    @staticmethod
    def _handle(job):
        definition=_job(job)
        return {"namespace":definition["namespace"],"job_id":definition["job_id"],"expected_version":job["version"]}

    def gates(self,job,*,approved,capacity,observed_at,capacity_digest,stopped=False):
        require(type(approved) is bool and type(stopped) is bool and capacity in ("available","unknown","exhausted"),"invalid release gates")
        require(_string(observed_at,lineage.TIME) and _string(capacity_digest,lineage.DIGEST),"capacity evidence must be pinned")
        return self._rpc("gates",{**self._handle(job),"approved":approved,"capacity":capacity,
            "observed_at":observed_at,"capacity_digest":capacity_digest,"stopped":stopped},mutating=True)["job"]

    def claim(self,job,claimant,*,lease_seconds=30):
        require(_string(claimant) and type(lease_seconds) is int and 1<=lease_seconds<=300,"invalid claim/lease")
        return self._rpc("claim",{**self._handle(job),"claimant":claimant,"lease_seconds":lease_seconds},mutating=True)["job"]

    def renew(self,job,*,lease_seconds=30):
        require(type(lease_seconds) is int and 1<=lease_seconds<=300,"invalid lease")
        return self._rpc("renew",{**self._fenced(job),"lease_seconds":lease_seconds},mutating=True)["job"]

    def release(self,job):
        return self._rpc("release",self._fenced(job),mutating=True)["job"]

    def _fenced(self,job):
        require(_string(job.get("claimant")) and _integer(job.get("fence"),1),"missing current claim")
        return {**self._handle(job),"claimant":job["claimant"],"fence":job["fence"]}

    def begin_effect(self,job,slot_index):
        definition=_job(job)
        require(type(slot_index) is int and 0<=slot_index<len(definition["slots"]),"unknown frozen execution slot")
        slot=definition["slots"][slot_index];material=key_material(definition,slot)
        return self._rpc("begin",{**self._fenced(job),"slot_index":slot_index,"key_text":canonical(material),
            "effect_key":digest(material)},mutating=True)

    def observe_effect(self,job,effect_key,observation):
        validate_observation(observation)
        require(observation["effect_key"]==effect_key,"effect observation identity differs")
        return self._rpc("observe",{**self._fenced(job),"effect_key":effect_key,
            "observation_text":canonical(observation),"observation_digest":digest(observation)},mutating=True)

    def retry_keyed_absent(self,job,effect_key):
        return self._rpc("retry_absent",{**self._fenced(job),"effect_key":effect_key},mutating=True)

    def finish(self,job,state,*,evidence_digest):
        require(state in ("awaiting_evidence","completed","failed","stopped","blocked") and
                _string(evidence_digest,lineage.DIGEST),"invalid finish evidence")
        return self._rpc("finish",{**self._fenced(job),"state":state,"evidence_digest":evidence_digest},mutating=True)["job"]

    def snapshot(self,namespace):
        require(_string(namespace,lineage.NAMESPACE),"invalid namespace")
        result=self._rpc("snapshot",{"namespace":namespace})
        _snapshot(result.get("snapshot_text"))
        require(result.get("head")==hashlib.sha256(result["snapshot_text"].encode()).hexdigest(),"snapshot readback head differs")
        return result

    def export(self,namespace,*,previous_export=None):
        result=self.snapshot(namespace);snapshot=_snapshot(result["snapshot_text"])
        manifest={"format_version":FORMAT,"reader_version":FORMAT,"reader_digest":reader_digest(),"schema_digest":schema_digest(),
            "projection":PROJECTION,"namespace":namespace,"complete":True,"export_id":"export-"+uuid.uuid4().hex,
            "previous_export":previous_export,"snapshot_text":result["snapshot_text"],"source_head":result["head"],
            "counts":{k:len(snapshot[k]) for k in SNAPSHOT_KINDS},"records":_record_digests(snapshot)}
        manifest["manifest_digest"]=digest(manifest);validate_checkpoint(manifest);return manifest

    def restore(self,manifest,*,expected_head,expected_manifest_digest):
        validate_checkpoint(manifest)
        require(expected_head is None or _string(expected_head,lineage.DIGEST),"invalid expected checkpoint head")
        require(_string(expected_manifest_digest,lineage.DIGEST) and manifest["manifest_digest"]==expected_manifest_digest,
                "checkpoint differs from independently pinned manifest")
        payload={k:v for k,v in manifest.items() if k!="manifest_digest"}
        result=self._rpc("restore",{"manifest_text":canonical(payload),"manifest_digest":manifest["manifest_digest"],
            "expected_head":expected_head,"expected_manifest_digest":expected_manifest_digest,
            "reader_digest":reader_digest(),"schema_digest":schema_digest()},mutating=True)
        require(result.get("head")==manifest["source_head"],"restored checkpoint readback differs")
        return result


class KeyedFileEffect:
    """One explicitly scoped, immutable keyed-object seam; not a native-call guarantee."""
    def __init__(self,root):
        self.root=Path(root)
        require(self.root.is_dir() and not self.root.is_symlink(),"effect directory must exist without symlinks")

    def _observation(self,key,expected,outcome,artifact=None):
        value={"effect_key":key,"payload_digest":expected,"outcome":outcome,
               "object_id":key if artifact is not None else None,"artifact_digest":artifact}
        return {**value,"proof_digest":digest(value)}

    def lookup(self,key,expected):
        require(_string(key,lineage.DIGEST) and _string(expected,lineage.DIGEST),"invalid keyed effect")
        if not self.root.is_dir() or self.root.is_symlink():return self._observation(key,expected,"unavailable")
        try:
            path=self.root/key
            if path.is_symlink():return self._observation(key,expected,"conflict")
            raw=path.read_bytes()
        except FileNotFoundError:return self._observation(key,expected,"absent")
        except OSError:return self._observation(key,expected,"unavailable")
        actual=hashlib.sha256(raw).hexdigest()
        return self._observation(key,expected,"matched" if actual==expected else "conflict",actual)

    def apply(self,key,payload):
        require(type(payload) is bytes and _string(key,lineage.DIGEST),"invalid effect input")
        expected=hashlib.sha256(payload).hexdigest()
        require(self.root.is_dir() and not self.root.is_symlink(),"effect store unavailable")
        try:
            fd=os.open(self.root/key,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        except FileExistsError:return self.lookup(key,expected)
        with os.fdopen(fd,"wb") as stream:
            stream.write(payload);stream.flush();os.fsync(stream.fileno())
        directory=os.open(self.root,os.O_RDONLY)
        try:os.fsync(directory)
        finally:os.close(directory)
        return self.lookup(key,expected)
