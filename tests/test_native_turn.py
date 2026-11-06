"""Inert protocol peers test software, never native model/skill qualification."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from ams import native_turn, recovery


def test_missing_external_readiness_refuses_before_claim_or_intent():
    class UntouchedStore:
        def __getattr__(self, name):
            raise AssertionError('Readiness refusal reached durable store: ' + name)

    with pytest.raises(recovery.Refused, match='external readiness'):
        native_turn.run_native_slot(UntouchedStore(), None, 'inert-controller', 0,
                                    None, None, expected_job_digest='a' * 64)


PEER = r'''
import json,os,pathlib,signal,subprocess,sys,time
data=json.loads(pathlib.Path(sys.argv[1]).read_text());log=pathlib.Path(sys.argv[2]);mode=sys.argv[3]
thread='inert-thread';turn='inert-turn';children=[]
def emit(value):print(json.dumps(value),flush=True)
def event(method,params):emit({'method':method,'params':params})
def terminal(status):event('turn/completed',{'threadId':thread,'turn':{'id':turn,'items':[],'status':status}})
for line in sys.stdin:
    value=json.loads(line)
    with log.open('a') as handle:handle.write(json.dumps(value)+'\n')
    if 'id' not in value:continue
    request=value['id'];method=value['method'];params=value.get('params')
    if method=='initialize':result={'userAgent':'inert-turn-peer'}
    elif method=='config/read':
        result=data['configuration']
        if mode=='outward':result['config']['features']['apps']=True
    elif method=='permissionProfile/list':result={'data':[{'id':data['profile_id'],'allowed':True}],'nextCursor':None}
    elif method=='mcpServerStatus/list':result={'data':[],'nextCursor':None}
    elif method=='thread/start':
        result={'thread':{'id':thread},'model':data['model'],'modelProvider':data['provider'],
                'reasoningEffort':'low','approvalPolicy':'never','approvalsReviewer':'user','cwd':data['cwd'],
                'sandbox':{'type':'readOnly'},'activePermissionProfile':{'id':data['profile_id']},
                'runtimeWorkspaceRoots':[data['cwd']],'instructionSources':[]}
        if mode=='wrong-model':result['model']='unapproved-model'
    elif method=='turn/start':
        emit({'id':request,'result':{'turn':{'id':turn,'status':'madeUp' if mode=='bad-turn' else 'inProgress','items':[]}}})
        event('turn/started',{'threadId':thread,'turn':{'id':turn,'status':'inProgress','items':[]}})
        if mode in ('approval','input','bad-request'):
            event_name='item/permissions/requestApproval' if mode=='approval' else 'item/tool/requestUserInput'
            emit({'id':'held-server-request','method':event_name,'params':{'threadId':thread,'turnId':False if mode=='bad-request' else turn,'questions':[{'question':'Which occurrence?'}]}})
            continue
        if mode in ('timeout','survivor','signal'):
            if mode=='survivor':
                child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'],start_new_session=True,
                    stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                pathlib.Path(data['child_file']).write_text(str(child.pid));children.append(child)
            event('item/started',{'threadId':thread,'turnId':turn,'startedAtMs':1,
                'item':{'id':'tool1','type':'commandExecution','command':'inert command','commandActions':[],
                        'cwd':data['cwd'],'status':'inProgress','processId':'PTY-not-an-OS-PID'}})
            if mode=='signal':
                pathlib.Path(data['child_file']).write_text(str(os.getpid()))
                os.kill(os.getppid(),signal.SIGINT)
            continue
        if mode in ('skill-read','bad-command'):
            event('item/completed',{'threadId':thread,'turnId':turn,'completedAtMs':2,
                'item':{'id':'read1','type':'commandExecution','command':'cat -- '+data['skill_path'],
                        'commandActions':[],'cwd':data['cwd'],'status':'completed','exitCode':'0' if mode=='bad-command' else 0,
                        'aggregatedOutput':pathlib.Path(data['skill_path']).read_text(),'processId':None}})
        if mode=='reroute':event('model/rerouted',{'threadId':thread,'turnId':turn,'fromModel':data['model'],'toModel':'other','reason':'modelNotAvailable'})
        if mode not in ('no-final','failed','interrupted'):
            event('item/completed',{'threadId':'foreign-thread' if mode=='wrong-id' else thread,'turnId':turn,'completedAtMs':3,
                'item':{'id':'answer','type':'agentMessage','phase':'final' if mode=='unsupported-phase' else None if mode=='unknown-phase' else 'final_answer','text':'Which concrete occurrence? Recommended first occurrence; why and impact.'}})
        terminal('failed' if mode=='failed' else 'interrupted' if mode=='interrupted' else 'completed')
        continue
    elif method=='turn/interrupt':
        if mode!='survivor':
            event('item/completed',{'threadId':thread,'turnId':turn,'completedAtMs':4,
                'item':{'id':'tool1','type':'commandExecution','command':'inert command','commandActions':[],
                        'cwd':data['cwd'],'status':'failed','exitCode':-9,'processId':'PTY-not-an-OS-PID'}})
        terminal('interrupted');result={}
    elif method=='thread/unsubscribe':result={'status':'unsubscribed'}
    else:emit({'id':request,'error':{'code':-32000,'message':'unexpected inert request'}});continue
    emit({'id':request,'result':result})
'''


def utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def readiness(call, job):
    return {'status': 'accepted', 'mode': 'inert', 'release_digest': call.data['release_digest'],
            'input_digest': call.payload_digest, 'job_digest': job['job_digest'],
            'approval_digest': '1' * 64, 'labels_digest': '2' * 64, 'grader_digest': '3' * 64,
            'capacity': {'state': 'available', 'observed_at': utc(), 'proof_digest': 'f' * 64}}


@pytest.fixture
def make_case(tmp_path):
    count = 0
    def make(mode='normal'):
        nonlocal count
        count += 1
        root = tmp_path / ('host' + str(count))
        root.mkdir()
        case = root / 'case'
        case.mkdir()
        subprocess.run(['git', 'init', '-q', str(case)], check=True)
        (case / 'input').write_text('synthetic fixture input\n')
        subprocess.run(['git', '-C', str(case), 'add', 'input'], check=True)
        subprocess.run(['git', '-C', str(case), '-c', 'user.name=inert', '-c', 'user.email=inert@example.invalid',
                        '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'synthetic fixture'], check=True)
        (case / 'unrelated').write_text('preserve untracked bytes\n')
        skill = root / 'skill.md'
        skill.write_text('Synthetic inert skill text; not a loaded production skill.\n')
        peer = root / 'peer.py'
        peer.write_text(PEER)
        profile_id = 'inert-read-only'
        profile = {'filesystem': {':root': 'deny', ':minimal': 'read', str(case): 'read'}, 'network': {'enabled': False}}
        profile['filesystem'].update({':tmpdir': 'deny', ':slash_tmp': 'deny'})
        if mode == 'broad-profile':
            profile['filesystem']['/'] = 'read'
        origins = {'fixture': {'source': 'inert'}}
        config = {'features': {key: False for key in native_turn.DISABLED_FEATURES},
                  'web_search': 'disabled', 'default_permissions': profile_id,
                  'forced_login_method': 'chatgpt',
                  'shell_environment_policy': {'inherit': 'none', 'set': {'PATH': '/usr/bin:/bin'}},
                  'permissions': {profile_id: profile}, 'mcp_servers': {'inert-connector': {'enabled': False}}}
        config['features']['hooks'] = True
        data = {'configuration': {'config': config, 'origins': origins}, 'profile_id': profile_id,
                'model': 'inert-model-v1', 'provider': 'inert-provider', 'cwd': str(case),
                'skill_path': str(skill), 'child_file': str(root / 'child')}
        datafile = root / 'peer-data.json'
        datafile.write_text(json.dumps(data))
        manifest = {'format_version': 1, 'case_digest': recovery.digest('distinct synthetic inert case'),
                    'skills_commit': 'c' * 40, 'source_commit': 'a' * 40, 'release_digest': 'e' * 64,
                    'cwd': str(case), 'prompt': 'Synthetic inert protocol test only.',
                    'model': data['model'], 'provider': data['provider'], 'effort': 'low',
                    'skill': {'name': 'grilling', 'path': str(skill), 'sha256': hashlib.sha256(skill.read_bytes()).hexdigest()},
                    'sources': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (peer, skill, datafile, Path(sys.executable).resolve())},
                    'fixture_digest': native_turn.fixture_digest(case), 'profile_id': profile_id,
                    'profile_digest': recovery.digest(profile), 'origins_digest': recovery.digest(origins),
                    'command': [sys.executable, '-u', str(peer), str(datafile), str(root / 'requests'), mode],
                    'resolved_executable': str(Path(sys.executable).resolve()),
                    'environment': {'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME']},
                    'limits': {'timeout_seconds': 0.3, 'cancel_seconds': 0.3, 'max_output_bytes': 1024 * 1024,
                               'max_events': 128, 'capacity_max_age_seconds': 300}}
        return root, native_turn.NativeCall(manifest)
    return make


class MemoryStore:
    """Protocol tests only; actual SQL claims are exercised separately."""
    def __init__(self, call):
        c = call.data
        definition = {'namespace': 'test-inert-turn', 'job_id': 'inert-turn-job', 'spec_id': 'S-000B',
                      'task_id': 'TK-002P', 'campaign_id': 'synthetic-inert-turn', 'case_id': 'inert-case',
                      'candidate_id': 'inert-candidate', 'case_digest': c['case_digest'], 'skills_commit': c['skills_commit'],
                      'release_digest': c['release_digest'], 'source_commit': c['source_commit'], 'is_test': True,
                      'synthetic': True, 'slots': [{'role': 'worker', 'arm': 'inert-peer', 'repetition': 1,
                                                  'effect_type': 'native-call', 'payload_digest': call.payload_digest}]}
        self.job = {'job_text': recovery.canonical(definition), 'job_digest': recovery.digest(definition),
                    'chain_id': 'inert-chain', 'attempt': 0, 'version': 1, 'fence': 0, 'claimant': None,
                    'lease_until': None, 'approved': True, 'capacity': 'available', 'capacity_digest': 'f' * 64,
                    'capacity_observed_at': utc(), 'stop_requested': False, 'terminal_state': None}
        self.calls, self.consumed = [], False

    def get_job(self, *_):
        return dict(self.job)

    def claim(self, job, claimant, *, lease_seconds):
        self.calls.append('claim')
        self.job.update(version=self.job['version'] + 1, fence=self.job['fence'] + 1, claimant=claimant,
                        lease_until=(datetime.now(timezone.utc) + timedelta(seconds=lease_seconds)).isoformat())
        return dict(self.job)

    def begin_effect(self, job, slot_index):
        self.calls.append('begin')
        definition = recovery._job(job)
        key = recovery.effect_key(definition, definition['slots'][slot_index])
        self.effect = {'effect_key': key, 'payload_digest': definition['slots'][slot_index]['payload_digest'],
                       'job_id': definition['job_id'], 'intent_fence': job['fence'], 'state': 'pending'}
        result = {'job': dict(self.job), 'effect': dict(self.effect), 'execute': not self.consumed}
        self.consumed = True
        return result

    def observe_effect(self, job, key, observation):
        self.calls.append('observe')
        self.effect['state'] = 'completed' if observation['outcome'] == 'matched' else 'uncertain'
        return {'job': dict(self.job), 'effect': dict(self.effect)}

    def release(self, job):
        self.calls.append('release')
        self.job.update(claimant=None, lease_until=None, version=self.job['version'] + 1)
        return dict(self.job)

    def snapshot(self, namespace):
        text = recovery.canonical({'namespace': namespace, 'jobs': [self.job],
                                   'effects': [self.effect] if self.consumed else []})
        return {'snapshot_text': text, 'head': hashlib.sha256(text.encode()).hexdigest()}


def execute_case(root, call, store=None, reader=readiness, cleanup=True, lease_seconds=300):
    from ams.native_worker import PrivateEvidence
    store = store or MemoryStore(call)
    evidence = PrivateEvidence(root / 'evidence', case_root=call.data['cwd'])

    def observed_cleanup(context):
        child = root / 'child'
        if child.exists():
            try:
                os.kill(int(child.read_text()), 0)
                return None
            except ProcessLookupError:
                pass
        return {'status': 'confirmed', 'mode': 'inert', 'input_digest': call.payload_digest,
                'proof_digest': recovery.digest({'inert_observation': context['server_pid']})}

    class InertSession(native_turn.NativeTurnSession):
        transport_kind = 'inert'

    return native_turn.run_native_slot(store, store.job, 'inert-controller', 0, evidence, call,
                                       expected_job_digest=store.job['job_digest'], readiness_reader=reader,
                                       lease_seconds=lease_seconds,
                                       session_factory=lambda c: InertSession(c, trace_root=root / 'traces',
                                                                             cleanup_reader=observed_cleanup if cleanup else lambda _: None))


@pytest.mark.parametrize('field', ['approval_digest', 'labels_digest', 'grader_digest', 'capacity'])
def test_incomplete_external_readiness_does_not_consume_intent(make_case, field):
    root, call = make_case()
    store = MemoryStore(call)
    def missing(c, job):
        proof = readiness(c, job)
        proof.pop(field)
        return proof
    with pytest.raises(recovery.Refused):
        execute_case(root, call, store, reader=missing)
    assert store.calls == [] and not store.consumed
    assert not (root / 'requests').exists()


def test_outward_configuration_refuses_before_consuming_intent(make_case):
    root, call = make_case('outward')
    store = MemoryStore(call)
    with pytest.raises(recovery.Refused, match='containment'):
        execute_case(root, call, store)
    assert store.calls == []
    assert 'turn/start' not in (root / 'requests').read_text()


def test_completed_inert_turn_persists_capture_without_semantic_or_load_claim(make_case):
    root, call = make_case()
    result = execute_case(root, call)
    assert result['executed'] is True and result['assessment_result'] == 'unknown'
    packet = json.loads((root / 'evidence' / result['effect']['effect_key']).read_text())['packet']
    assert packet['capture_status'] == 'complete' and packet['final_response']
    assert packet['observed_model'] is None and packet['skill_load']['status'] == 'unknown'
    assert packet['cleanup']['status'] == 'confirmed' and packet['assessment_result'] == 'unknown'
    assert packet['synthetic_inert'] is True and packet['model_calls'] == 0


@pytest.mark.parametrize('mode', ['wrong-id', 'reroute', 'no-final'])
def test_invalid_turn_facts_never_become_successful_capture(make_case, mode):
    root, call = make_case(mode)
    store = MemoryStore(call)
    with pytest.raises((native_turn.NativeProtocolError, recovery.Refused)):
        execute_case(root, call, store)
    assert store.consumed and not list((root / 'evidence').iterdir())
    assert list((root / 'traces').iterdir()), 'Partial native facts were lost'


def test_preparatory_model_mismatch_refuses_without_consuming_intent(make_case):
    root, call = make_case('wrong-model')
    store = MemoryStore(call)
    with pytest.raises(recovery.Refused, match='configured model'):
        execute_case(root, call, store)
    assert store.calls == [] and not store.consumed
    assert 'turn/start' not in (root / 'requests').read_text()


@pytest.mark.parametrize('mode', ['failed', 'interrupted', 'approval', 'input'])
def test_valid_incomplete_captures_do_not_manufacture_a_final_response(make_case, mode):
    root, call = make_case(mode)
    result = execute_case(root, call)
    packet = json.loads((root / 'evidence' / result['effect']['effect_key']).read_text())['packet']
    assert packet['capture_status'] == 'incomplete' and packet['final_response'] is None
    assert packet['assessment_result'] == 'unknown'
    requests = [json.loads(line) for line in (root / 'requests').read_text().splitlines()]
    assert not any('result' in request for request in requests), 'A native server question/approval was answered'


def test_missing_cleanup_proof_cannot_close_success_or_make_a_safe_retry(make_case):
    root, call = make_case()
    store = MemoryStore(call)
    with pytest.raises(native_turn.CleanupIncomplete):
        execute_case(root, call, store, cleanup=False)
    assert store.consumed and not list((root / 'evidence').iterdir())
    request_count = (root / 'requests').read_text().count('turn/start')
    second = execute_case(root, call, store)
    assert second['executed'] is False and second['effect']['state'] == 'uncertain'
    assert (root / 'requests').read_text().count('turn/start') == request_count


def test_completed_native_read_parser_does_not_treat_skill_input_echo_as_load(make_case):
    root, call = make_case('skill-read')
    result = execute_case(root, call)
    packet = json.loads((root / 'evidence' / result['effect']['effect_key']).read_text())['packet']
    assert packet['skill_load']['status'] == 'observed-read'
    assert packet['skill_load']['sha256'] == call.data['skill']['sha256']
    assert packet['synthetic_inert'] is True


def test_inert_external_release_cannot_use_default_native_transport(make_case):
    from ams.native_worker import PrivateEvidence
    root, call = make_case()
    store = MemoryStore(call)
    with pytest.raises(recovery.Refused, match='inert release'):
        native_turn.run_native_slot(store, store.job, 'inert-controller', 0,
            PrivateEvidence(root / 'evidence', case_root=call.data['cwd']), call,
            expected_job_digest=store.job['job_digest'], readiness_reader=readiness)
    assert not store.consumed and not (root / 'requests').exists()


def test_cleanup_observer_must_exist_before_a_native_intent(make_case):
    from ams.native_worker import PrivateEvidence
    root, call = make_case()
    store = MemoryStore(call)
    class InertSession(native_turn.NativeTurnSession):
        transport_kind = 'inert'
    with pytest.raises(recovery.Refused, match='cleanup observer'):
        native_turn.run_native_slot(store, store.job, 'inert-controller', 0,
            PrivateEvidence(root / 'evidence', case_root=call.data['cwd']), call,
            expected_job_digest=store.job['job_digest'], readiness_reader=readiness,
            session_factory=lambda c: InertSession(c, trace_root=root / 'traces'))
    assert not store.consumed and not (root / 'requests').exists()


def test_protected_eval_or_broad_read_grant_is_not_a_runtime_closure(make_case):
    root, call = make_case('broad-profile')
    store = MemoryStore(call)
    with pytest.raises(recovery.Refused, match='containment'):
        execute_case(root, call, store)
    assert not store.consumed
    manifest = call.data
    forbidden = root / '.eval' / 'private-grader'
    forbidden.parent.mkdir()
    forbidden.write_text('must never enter the native runtime')
    manifest['sources'][str(forbidden)] = hashlib.sha256(forbidden.read_bytes()).hexdigest()
    with pytest.raises(recovery.Refused, match='evaluation'):
        native_turn.NativeCall(manifest)


def test_changed_gate_immediately_before_turn_never_starts_the_turn(make_case):
    root, call = make_case()
    store = MemoryStore(call)
    reads = 0
    def withdrawn(c, job):
        nonlocal reads
        reads += 1
        proof = readiness(c, job)
        if reads == 3:
            proof['status'] = 'held'
        return proof
    with pytest.raises(recovery.Refused):
        execute_case(root, call, store, reader=withdrawn)
    assert store.consumed and reads == 3
    assert 'turn/start' not in (root / 'requests').read_text()


def test_separate_owned_child_surviving_terminal_ack_is_never_closed_success(make_case):
    root, call = make_case('survivor')
    store = MemoryStore(call)
    sentinel = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'], start_new_session=True)
    try:
        with pytest.raises((native_turn.CleanupIncomplete, native_turn.NativeProtocolError)):
            execute_case(root, call, store)
        assert store.consumed and not list((root / 'evidence').iterdir())
        child = int((root / 'child').read_text())
        os.kill(child, 0)
        assert sentinel.poll() is None
    finally:
        if (root / 'child').exists():
            try:os.killpg(int((root / 'child').read_text()), signal.SIGKILL)
            except ProcessLookupError:pass
        sentinel.kill()
        sentinel.wait(timeout=3)


@pytest.mark.parametrize('mode', ['bad-turn', 'bad-command', 'bad-request'])
def test_malformed_terminal_or_request_shapes_cannot_be_persisted_as_valid_capture(make_case, mode):
    root, call = make_case(mode)
    store = MemoryStore(call)
    with pytest.raises(native_turn.NativeProtocolError):
        execute_case(root, call, store)
    assert store.consumed and not list((root / 'evidence').iterdir())


def test_real_inert_controller_sigint_preserves_interrupt_and_consumed_intent(make_case):
    root, call = make_case('signal')
    manifest = root / 'worker-call.json'
    manifest.write_text(recovery.canonical(call.data))
    worker_code = '''import json,pathlib,sys
from ams.native_turn import NativeCall
sys.path.insert(0,sys.argv[3])
from test_native_turn import MemoryStore,execute_case
root=pathlib.Path(sys.argv[1]);call=NativeCall(json.loads(pathlib.Path(sys.argv[2]).read_text()));store=MemoryStore(call)
try:execute_case(root,call,store)
except KeyboardInterrupt as error:
    (root/'interrupted.json').write_text(json.dumps({'consumed':store.consumed,'calls':store.calls,'original_interrupt':True}))
    raise SystemExit(130)
raise AssertionError('The inert controller did not receive SIGINT')
'''
    sentinel = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'], start_new_session=True)
    try:
        result = subprocess.run([sys.executable, '-c', worker_code, str(root), str(manifest), str(Path(__file__).parent)],
                                capture_output=True, timeout=8)
        assert result.returncode == 130, result.stderr.decode()
        observed = json.loads((root / 'interrupted.json').read_text())
        assert observed['consumed'] and observed['original_interrupt']
        assert observed['calls'].count('begin') == 1
        assert not list((root / 'evidence').iterdir())
        with pytest.raises(ProcessLookupError):
            os.kill(int((root / 'child').read_text()), 0)
        assert sentinel.poll() is None
    finally:
        sentinel.kill()
        sentinel.wait(timeout=3)


@pytest.mark.parametrize('stage', ['preparation', 'cleanup'])
def test_one_total_deadline_and_one_aggregate_cleanup_budget(make_case, stage):
    root, call = make_case('normal' if stage == 'preparation' else 'input')
    peer = root / 'peer.py'
    original = "request=value['id'];method=value['method'];params=value.get('params')"
    delay = ';time.sleep(0.15)' if stage == 'preparation' else ";time.sleep(0.2 if method in ('turn/interrupt','thread/unsubscribe') else 0)"
    peer.write_text(peer.read_text().replace(original, original + delay))
    data = call.data
    data['sources'][str(peer)] = hashlib.sha256(peer.read_bytes()).hexdigest()
    call = native_turn.NativeCall(data)
    store = MemoryStore(call)
    started = time.monotonic()
    with pytest.raises((native_turn.NativeProtocolError, native_turn.CleanupIncomplete, recovery.Refused)):
        execute_case(root, call, store)
    assert time.monotonic() - started < 0.85, 'Fresh per-operation budgets exceeded the declared total bounds'
    assert not list((root / 'evidence').iterdir())
    assert store.consumed is (stage == 'cleanup')


@pytest.mark.parametrize('mode', ['unsupported-phase', 'unknown-phase'])
def test_only_schema_terminal_phase_can_supply_a_normal_final_response(make_case, mode):
    # Codex0.159.3 generated schema e77b7d14: commentary | final_answer;
    # absent/null phase is explicitly unknown, not a spelling alias.
    root, call = make_case(mode)
    store = MemoryStore(call)
    with pytest.raises(native_turn.NativeProtocolError):
        execute_case(root, call, store)
    assert store.consumed and not list((root / 'evidence').iterdir())


class HistoryPeer:
    """Only the three supported persisted-history reads are available."""
    def __init__(self, call, mode='normal'):
        self.call_input, self.mode, self.calls = call, mode, []

    def call(self, method, params, *, timeout):
        assert method in ('thread/read', 'thread/turns/list', 'thread/items/list')
        assert 0 < timeout <= 5
        self.calls.append((method, params))
        c = self.call_input.data
        if self.mode == 'not-found':
            raise native_turn.NativeProtocolError('inert history unavailable')
        if method == 'thread/read':
            return {'thread': {'id': 'foreign' if self.mode == 'wrong-thread' else 'retained-thread',
                               'cliVersion': 'inert-version', 'modelProvider': c['provider'], 'model': c['model'], 'turns': []}}
        if method == 'thread/turns/list':
            first = params.get('cursor') is None
            return {'data': [] if first else [{'id': 'different-turn' if self.mode == 'missing-turn' else 'retained-turn',
                                               'items': [], 'status': 'completed', 'itemsView': 'summary'}],
                    'nextCursor': 'turn-page2' if first or self.mode == 'cursor-loop' else None}
        items = [{'id': 'user', 'type': 'userMessage', 'content': [
                    {'type': 'skill', 'name': c['skill']['name'], 'path': c['skill']['path']},
                    {'type': 'text', 'text': c['prompt'], 'text_elements': []}]},
                 {'id': 'final', 'type': 'agentMessage', 'phase': 'final_answer', 'text': 'Retained private question?'}]
        return {'data': [{'turnId': 'foreign' if self.mode == 'wrong-item-turn' else 'retained-turn', 'item': item}
                         for item in items], 'nextCursor': None}


def history_pin(call, job, effect):
    return {'format_version': 1, 'effect_key': effect['effect_key'], 'input_digest': call.payload_digest,
            'job_digest': job['job_digest'], 'release_digest': call.data['release_digest'],
            'source_commit': call.data['source_commit'], 'thread_id': 'retained-thread', 'turn_id': 'retained-turn',
            'cli_version': 'inert-version', 'native_binding_digest': recovery.digest('independently retained inert binding')}


@pytest.mark.parametrize('mode', ['normal', 'wrong-thread', 'missing-turn', 'wrong-item-turn', 'cursor-loop', 'not-found'])
def test_missing_packet_history_reconciliation_is_bounded_read_only_and_never_retry_permission(make_case, mode):
    root, call = make_case()
    store = MemoryStore(call)
    reserved = store.begin_effect(store.claim(store.job, 'interrupted', lease_seconds=300), 0)
    store.release(reserved['job'])
    pin = history_pin(call, store.job, reserved['effect'])
    peer = HistoryPeer(call, mode)
    before = store.snapshot('test-inert-turn')
    result = native_turn.reconcile_native_history(peer, store, store.job, call, pin,
        expected_pin_digest=recovery.digest(pin), expected_job_digest=store.job['job_digest'], max_pages=4)
    assert result['status'] == ('observed' if mode == 'normal' else 'unavailable' if mode == 'not-found' else 'untrusted')
    assert result['execution_allowed'] is False and result['assessment_result'] == 'unknown'
    assert result['observed_model'] is None and result['cleanup']['status'] == 'unknown'
    assert result['observation']['outcome'] == 'unavailable'
    assert store.snapshot('test-inert-turn') == before
    assert len(peer.calls) <= 5 and all(method in ('thread/read', 'thread/turns/list', 'thread/items/list') for method, _ in peer.calls)
    if mode == 'normal':
        assert result['private_history']['final_response'] == 'Retained private question?'
    assert not (root / 'evidence').exists()


def test_history_pin_mismatch_refuses_before_any_store_or_native_read(make_case):
    _, call = make_case()
    store = MemoryStore(call)
    reserved = store.begin_effect(store.claim(store.job, 'interrupted', lease_seconds=300), 0)
    pin = history_pin(call, store.job, reserved['effect'])
    expected = recovery.digest(pin)
    pin['turn_id'] = 'untrusted-replacement'
    peer = HistoryPeer(call)
    with pytest.raises(recovery.Refused, match='independent'):
        native_turn.reconcile_native_history(peer, store, store.job, call, pin,
            expected_pin_digest=expected, expected_job_digest=store.job['job_digest'])
    assert peer.calls == []


@pytest.mark.parametrize('limit', [{'max_pages': 2}, {'max_bytes': 64}])
def test_history_aggregate_limits_preserve_unknown_and_consumed_intent(make_case, limit):
    _, call = make_case()
    store = MemoryStore(call)
    reserved = store.begin_effect(store.claim(store.job, 'interrupted', lease_seconds=300), 0)
    pin = history_pin(call, store.job, reserved['effect'])
    peer = HistoryPeer(call)
    before = store.snapshot('test-inert-turn')
    result = native_turn.reconcile_native_history(peer, store, store.job, call, pin,
        expected_pin_digest=recovery.digest(pin), expected_job_digest=store.job['job_digest'], **limit)
    assert result['status'] == 'untrusted' and result['execution_allowed'] is False
    assert result['observation']['outcome'] == 'unavailable'
    assert store.snapshot('test-inert-turn') == before
    assert len(peer.calls) <= 3
