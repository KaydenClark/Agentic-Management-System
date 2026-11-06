"""Isolated synthetic controller identities; never reserve the grilling slot."""
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse
import uuid

import pytest

from ams import lineage, native_worker, recovery


@dataclass
class Controller:
    store: recovery.Store
    namespace: str
    job: dict
    job_digest: str
    payload_digest: str
    evidence: native_worker.PrivateEvidence
    config: dict = field(repr=False)


@pytest.fixture
def controller(tmp_path):
    filename = os.environ.get('AMS_LINEAGE_TEST_CONFIG')
    if not filename:
        pytest.skip('isolated controller database configuration not supplied')
    config = json.loads(Path(filename).read_text())
    assert urlparse(config['url']).hostname in ('127.0.0.1', 'localhost')
    identity = uuid.uuid4().hex
    namespace = 'test-native-controller-' + identity
    case_digest = hashlib.sha256(b'synthetic-no-model-controller-v1').hexdigest()
    payload = hashlib.sha256(b'synthetic-controller-input-v1').hexdigest()
    def row(kind, record_id, parents, attributes):
        return dict(namespace=namespace, kind=kind, record_id=record_id, parents=parents, attributes=attributes,
                    source_commit='a' * 40, artifact_digest=case_digest, occurred_at='2026-11-06T00:00:00Z',
                    is_test=True, synthetic=True)
    # Hex source values are explicitly synthetic fixture data, never loaded skill claims.
    records = [row('failure', 'controller-occurrence', {}, {'failure_id': 'synthetic-controller-event',
                   'family': 'native-controller-test', 'chain_id': 'controller-' + identity}),
               row('case', 'controller-case-v1', {'failure': 'controller-occurrence'},
                   {'version': 1, 'rsi_task_id': 'synthetic-no-model-controller'}),
               row('candidate', 'controller-baseline', {'case': 'controller-case-v1'},
                   {'attempt': 0, 'skills_commit': 'c' * 40})]
    lineage.Store(config['url'], config['service_jwt'], rest_path=config['rest_path']).append(records, expected_head=None)
    store = recovery.Store(config['url'], config['service_jwt'], rest_path=config['rest_path'], pending_dir=tmp_path / 'pending')
    definition = dict(namespace=namespace, job_id='controller-job', spec_id='S-000B', task_id='TK-002P',
                      campaign_id='synthetic-no-model-controller', case_id='controller-case-v1', candidate_id='controller-baseline',
                      case_digest=case_digest, skills_commit='c' * 40, release_digest='e' * 64, source_commit='a' * 40,
                      is_test=True, synthetic=True, slots=[dict(role='worker', arm='no-model-controller', repetition=1,
                                                             effect_type='native-call', payload_digest=payload)])
    job = store.create_job(definition)
    job = store.gates(job, approved=True, capacity='available',
                      observed_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'), capacity_digest='f' * 64)
    case = tmp_path / 'case'
    case.mkdir()
    evidence = native_worker.PrivateEvidence(tmp_path / 'evidence', case_root=case)
    return Controller(store, namespace, job, recovery.digest(definition), payload, evidence, config)


class NoModelExecutor:
    def __init__(self, payload):
        self.payload_digest, self.calls = payload, 0

    def execute(self, effect_key):
        self.calls += 1
        return {'kind': 'synthetic-no-model-controller-test', 'modelCalls': 0,
                'executionCompleted': True, 'effect_key': effect_key}


def test_fifo_refusal_is_bounded_and_does_not_mutate_existing_pending_intent(controller):
    c = controller
    reserved = c.store.begin_effect(c.store.claim(c.job, 'fifo-probe-owner'), 0)
    c.store.release(reserved['job'])
    key = reserved['effect']['effect_key']
    os.mkfifo(c.evidence.root / key, 0o600)
    before = c.store.snapshot(c.namespace)
    program = '''import sys
from ams.native_worker import PrivateEvidence
e=PrivateEvidence(sys.argv[1],case_root=sys.argv[2])
assert e.lookup(sys.argv[3],sys.argv[4])['outcome']=='conflict'
print('refused',flush=True)
'''
    # This bounded private read must not consume/release/re-arm a durable slot.
    with subprocess.Popen([sys.executable, '-c', program, str(c.evidence.root),
                           str(c.evidence.root.parent / 'case'), key, c.payload_digest],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=1)
            assert process.returncode == 0, stderr.decode()
            assert stdout == b'refused\n'
        finally:
            if process.poll() is None:
                process.kill()
            process.wait(timeout=3)
    assert c.store.snapshot(c.namespace) == before


def test_existing_durable_slot_recovers_private_artifact_without_executing_again(controller):
    c = controller
    execute = NoModelExecutor(c.payload_digest)
    first = native_worker.run_slot(c.store, c.job, 'controller-first', 0, c.evidence, execute,
                                   expected_job_digest=c.job_digest)
    assert execute.calls == 1 and first['executed'] is True
    assert first['effect']['state'] == 'completed' and first['assessment_result'] == 'unknown'
    second = native_worker.run_slot(c.store, c.store.get_job(c.namespace, 'controller-job'), 'controller-fresh',
                                    0, c.evidence, execute, expected_job_digest=c.job_digest)
    assert execute.calls == 1 and second['executed'] is False
    assert second['observation'] == first['observation']
    assert second['effect']['effect_key'] == first['effect']['effect_key']
    assert second['job']['claimant'] is None
    assert json.loads(second['job']['job_text'])['synthetic'] is True and second['job']['attempt'] == 0


def test_consumed_native_intent_without_artifact_stays_unknown_without_replay(controller):
    c = controller
    reserved = c.store.begin_effect(c.store.claim(c.job, 'before-interruption'), 0)
    c.store.release(reserved['job'])
    execute = NoModelExecutor(c.payload_digest)
    result = native_worker.run_slot(c.store, c.store.get_job(c.namespace, 'controller-job'), 'fresh-controller',
                                    0, c.evidence, execute, expected_job_digest=c.job_digest)
    assert execute.calls == 0 and result['executed'] is False
    assert result['observation']['outcome'] == 'unavailable' and result['effect']['state'] == 'uncertain'
    assert result['assessment_result'] == 'unknown'


def test_independent_job_and_input_pins_refuse_before_claim(controller):
    c = controller
    before = c.store.snapshot(c.namespace)
    with pytest.raises(native_worker.NativeProtocolError):
        native_worker.run_slot(c.store, c.job, 'wrong-pin', 0, c.evidence,
                               NoModelExecutor(c.payload_digest), expected_job_digest='0' * 64)
    with pytest.raises(native_worker.NativeProtocolError):
        native_worker.run_slot(c.store, c.job, 'wrong-input', 0, c.evidence,
                               NoModelExecutor('0' * 64), expected_job_digest=c.job_digest)
    assert c.store.snapshot(c.namespace) == before


def test_competing_controllers_execute_one_claimed_native_slot(controller):
    c = controller
    execute = NoModelExecutor(c.payload_digest)
    def run(actor):
        try:
            return native_worker.run_slot(c.store, c.job, actor, 0, c.evidence, execute,
                                          expected_job_digest=c.job_digest)
        except recovery.DatabaseRefused as error:
            assert error.database_code == 'PT409'
            return None
    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(run, ['controller-one', 'controller-two']))
    assert sum(result is not None for result in results) == 1
    assert execute.calls == 1
    assert len(json.loads(c.store.snapshot(c.namespace)['snapshot_text'])['effects']) == 1


@pytest.mark.parametrize('gate', ['approval', 'unknown-capacity', 'exhausted-capacity', 'stop'])
def test_controller_does_not_execute_past_held_server_gates(controller, gate):
    c = controller
    job = c.store.gates(c.job, approved=gate != 'approval',
                        capacity='unknown' if gate == 'unknown-capacity' else 'exhausted' if gate == 'exhausted-capacity' else 'available',
                        observed_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                        capacity_digest='f' * 64, stopped=gate == 'stop')
    execute = NoModelExecutor(c.payload_digest)
    with pytest.raises(recovery.DatabaseRefused) as held:
        native_worker.run_slot(c.store, job, 'held-controller', 0, c.evidence, execute,
                               expected_job_digest=c.job_digest)
    assert held.value.database_code == 'PT409'
    assert execute.calls == 0
    assert not json.loads(c.store.snapshot(c.namespace)['snapshot_text'])['effects']
