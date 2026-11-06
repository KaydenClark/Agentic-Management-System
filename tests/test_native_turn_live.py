"""Actual isolated O persistence with inert peers; no native/model/skill calls."""
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

from ams import lineage, native_turn, recovery
from test_native_turn import HistoryPeer, MemoryStore, execute_case, history_pin, make_case, readiness, utc


@pytest.fixture
def turn_store(make_case):
    filename = os.environ.get('AMS_LINEAGE_TEST_CONFIG')
    if not filename:
        pytest.skip('isolated native-turn database configuration not supplied')
    config = json.loads(Path(filename).read_text())
    assert urlparse(config['url']).hostname in ('127.0.0.1', 'localhost')
    root, call = make_case()
    namespace = 'test-inert-turn-' + uuid.uuid4().hex
    definition = recovery._job(MemoryStore(call).job)
    definition.pop('chain_id')
    definition.pop('attempt')
    definition['namespace'] = namespace
    definition['case_id'], definition['candidate_id'] = 'inert-case', 'inert-candidate'
    def row(kind, record_id, parents, attributes):
        return {'namespace': namespace, 'kind': kind, 'record_id': record_id, 'parents': parents,
                'attributes': attributes, 'source_commit': call.data['source_commit'],
                'artifact_digest': call.data['case_digest'], 'occurred_at': utc(), 'is_test': True, 'synthetic': True}
    records = [row('failure', 'inert-occurrence', {}, {'failure_id': 'synthetic-native-turn',
                   'family': 'inert-turn-controller-test', 'chain_id': 'inert-' + uuid.uuid4().hex}),
               row('case', 'inert-case', {'failure': 'inert-occurrence'}, {'version': 1, 'rsi_task_id': 'synthetic-inert-turn'}),
               row('candidate', 'inert-candidate', {'case': 'inert-case'}, {'attempt': 0, 'skills_commit': call.data['skills_commit']})]
    lineage.Store(config['url'], config['service_jwt'], rest_path=config['rest_path']).append(records, expected_head=None)
    store = recovery.Store(config['url'], config['service_jwt'], rest_path=config['rest_path'], pending_dir=root / 'pending')
    created = store.create_job(definition)
    store.job = store.gates(created, approved=True, capacity='available', observed_at=utc(), capacity_digest='f' * 64)
    return root, call, store, Path(filename)


@pytest.mark.parametrize('missing', ['approval_digest', 'labels_digest', 'grader_digest', 'capacity'])
def test_external_readiness_refuses_without_any_actual_durable_mutation(turn_store, missing):
    root, call, store, _ = turn_store
    before = store.snapshot(recovery._job(store.job)['namespace'])
    def incomplete(c, job):
        proof = readiness(c, job)
        proof.pop(missing)
        return proof
    with pytest.raises(recovery.Refused):
        execute_case(root, call, store, reader=incomplete)
    assert store.snapshot(recovery._job(store.job)['namespace']) == before
    assert not (root / 'requests').exists()


def test_actual_durable_slot_captures_once_and_keeps_private_facts_out_of_store(turn_store):
    root, call, store, _ = turn_store
    first = execute_case(root, call, store)
    second = execute_case(root, call, store)
    assert first['executed'] is True and second['executed'] is False
    assert first['effect']['effect_key'] == second['effect']['effect_key']
    assert second['effect']['state'] == 'completed' and second['assessment_result'] == 'unknown'
    assert (root / 'requests').read_text().count('"method": "turn/start"') == 1
    snapshot = store.snapshot(recovery._job(store.job)['namespace'])
    assert str(root) not in snapshot['snapshot_text'] and call.data['prompt'] not in snapshot['snapshot_text']
    assert all(row['synthetic'] for row in lineage.Store(store.url, store._key, rest_path=store.rest_path).read(recovery._job(store.job)['namespace']))


def test_actual_consumed_intent_without_packet_never_starts_a_turn(turn_store):
    root, call, store, _ = turn_store
    reserved = store.begin_effect(store.claim(store.job, 'before-inert-crash'), 0)
    store.release(reserved['job'])
    result = execute_case(root, call, store)
    assert result['executed'] is False and result['effect']['state'] == 'uncertain'
    assert result['assessment_result'] == 'unknown'
    assert '"method": "turn/start"' not in (root / 'requests').read_text()


def test_read_only_native_history_does_not_complete_or_rearm_actual_consumed_intent(turn_store):
    root, call, store, _ = turn_store
    reserved = store.begin_effect(store.claim(store.job, 'uncertain-native-owner'), 0)
    live = store.release(reserved['job'])
    pin = history_pin(call, live, reserved['effect'])
    before = store.snapshot(recovery._job(live)['namespace'])
    peer = HistoryPeer(call)
    history = native_turn.reconcile_native_history(peer, store, live, call, pin,
        expected_pin_digest=recovery.digest(pin), expected_job_digest=live['job_digest'])
    assert history['status'] == 'observed' and history['execution_allowed'] is False
    assert history['assessment_result'] == 'unknown' and history['cleanup']['status'] == 'unknown'
    assert history['observation']['outcome'] == 'unavailable'
    assert store.snapshot(recovery._job(live)['namespace']) == before
    result = execute_case(root, call, store)
    assert result['executed'] is False and result['effect']['state'] == 'uncertain'
    assert '"method": "turn/start"' not in (root / 'requests').read_text()


def test_actual_fresh_process_recovers_fsynced_capture_after_exit23_without_new_turn(turn_store):
    root, call, store, configfile = turn_store
    definition = recovery._job(store.job)
    manifest = root / 'restart-input.json'
    manifest.write_text(recovery.canonical({'call': call.data, 'namespace': definition['namespace'], 'job_id': definition['job_id']}))
    code = '''import json,os,pathlib,sys
from ams import native_turn,recovery
sys.path.insert(0,sys.argv[4])
from test_native_turn import execute_case
root=pathlib.Path(sys.argv[1]);value=json.loads((root/'restart-input.json').read_text());config=json.loads(pathlib.Path(sys.argv[2]).read_text())
class CrashBeforeReceipt(recovery.Store):
    def observe_effect(self,*args,**kwargs):os._exit(23)
kind=CrashBeforeReceipt if sys.argv[3]=='crash' else recovery.Store
store=kind(config['url'],config['service_jwt'],rest_path=config['rest_path'],pending_dir=root/(sys.argv[3]+'-pending'))
store.job=store.get_job(value['namespace'],value['job_id'])
result=execute_case(root,native_turn.NativeCall(value['call']),store,lease_seconds=6)
print(json.dumps({'executed':result['executed'],'key':result['effect']['effect_key'],'fence':result['job']['fence'],'state':result['effect']['state'],'assessment':result['assessment_result']}))
'''
    def worker(mode):
        return subprocess.run([sys.executable, '-c', code, str(root), str(configfile), mode, str(Path(__file__).parent)],
                              capture_output=True, text=True, timeout=15)
    first = worker('crash')
    assert first.returncode == 23, first.stderr
    packets = list((root / 'evidence').iterdir())
    assert len(packets) == 1
    packet = packets[0]
    before = (packet.stat().st_mtime_ns, hashlib.sha256(packet.read_bytes()).hexdigest())
    assert (root / 'requests').read_text().count('"method": "turn/start"') == 1
    time.sleep(6.1)
    fresh = worker('resume')
    assert fresh.returncode == 0, fresh.stderr
    result = json.loads(fresh.stdout)
    assert result == {'executed': False, 'key': packet.name, 'fence': 2, 'state': 'completed', 'assessment': 'unknown'}
    assert before == (packet.stat().st_mtime_ns, hashlib.sha256(packet.read_bytes()).hexdigest())
    assert (root / 'requests').read_text().count('"method": "turn/start"') == 1
