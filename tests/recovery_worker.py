"""Fresh-process isolated recovery probe; never invokes a model or prints keys."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from ams import recovery

p=argparse.ArgumentParser();p.add_argument("mode",choices=("race","crash","recover"));p.add_argument("config")
p.add_argument("namespace");p.add_argument("objects");p.add_argument("pending");p.add_argument("claimant")
p.add_argument("--expected-version",type=int);a=p.parse_args()
config=json.loads(Path(a.config).read_text())
store=recovery.Store(config["url"],config["service_jwt"],rest_path=config["rest_path"],pending_dir=a.pending)
job=store.get_job(a.namespace,"job-1")
if a.expected_version is not None:job["version"]=a.expected_version
try:
    claimed=store.claim(job,a.claimant,lease_seconds=1 if a.mode=="crash" else 30)
except recovery.Unavailable:raise
except recovery.Refused as error:
    if a.mode!="race" or "HTTP 409" not in str(error):raise
    print(json.dumps({"won":False,"executed":False}));raise SystemExit(0)
reserved=store.begin_effect(claimed,0)
key=reserved["effect"]["effect_key"];adapter=recovery.KeyedFileEffect(a.objects)
payload=b"safe synthetic effect";expected=hashlib.sha256(payload).hexdigest()
if a.mode=="recover" and reserved["execute"]:raise RuntimeError("fresh recovery would blindly repeat consumed slot")
if reserved["execute"]:
    observation=adapter.apply(key,payload)
    if a.mode=="crash":os._exit(23)
else:observation=adapter.lookup(key,expected)
if observation["outcome"]!="matched":raise RuntimeError("expected actual keyed effect readback")
sealed=store.observe_effect(reserved["job"],key,observation)
final=store.finish(sealed["job"],"completed",evidence_digest=observation["artifact_digest"])
print(json.dumps({"won":True,"executed":reserved["execute"],"effect_key":key,"state":final["state"]}))
