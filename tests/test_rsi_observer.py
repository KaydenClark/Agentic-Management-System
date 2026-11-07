"""Synthetic public observer and audit controls."""
import copy
import json
import subprocess
import sys

import pytest

REV = 'a' * 40


def event(event_id, kind, **fields):
    return {
        'event_id': event_id, 'chat_id': 'chat-1',
        'occurred_at': '2026-11-07T09:00:00Z', 'kind': kind,
        **fields,
    }


def cli(project, command, payload=None, *, ok=True):
    result = subprocess.run(
        [sys.executable, '-m', 'ams.rsi_observer', '--project', str(project), *command],
        input=json.dumps(payload) if payload is not None else None,
        text=True, capture_output=True,
    )
    assert (result.returncode == 0) is ok, result.stderr
    return json.loads(result.stdout) if ok else result.stderr


def test_cli_restart_keeps_explicit_request_use_and_work_status_separate(tmp_path):
    root = tmp_path
    assert cli(root, ['status', 'chat-1'])['work_status'] == 'unknown'
    assert not (root / 'workbench').exists()
    request = event('request-1', 'skill_requested', skill='setup-workbench')
    cli(root, ['record'], request)
    loaded = event('load-1', 'skill_loaded', skill='setup-workbench', request_event_id='request-1',
                   skill_revision=REV, evidence_id='proof-load')
    cli(root, ['record'], loaded)
    cli(root, ['record'], loaded)
    pending = cli(root, ['status', 'chat-1'])
    assert pending['pending_event_ids'] == ['request-1', 'load-1']
    assert pending['requested_uses']['request-1']['outcome'] == 'unknown'
    assert pending['work_status'] == 'unknown'

    blocked = event('status-1', 'work_status', outcome='blocked', evidence_id='proof-1')
    cli(root, ['record'], blocked)
    assert cli(root, ['status', 'chat-1'])['work_status'] == 'blocked'
    skipped = event('use-1', 'skill_used', skill='setup-workbench', outcome='skipped',
                    request_event_id='request-1', evidence_id='proof-2')
    cli(root, ['record'], skipped)
    cli(root, ['record'], event('failure-1', 'failure', skill='setup-workbench',
                                outcome='blocking', evidence_id='FAIL-001'))
    cli(root, ['record'], event('status-2', 'work_status', outcome='finished', evidence_id='proof-3'))
    finished = cli(root, ['status', 'chat-1'])
    assert finished['work_status'] == 'finished'
    assert finished['requested_uses']['request-1']['outcome'] == 'skipped'
    assert finished['critical_failure_ids'] == ['use-1']
    assert 'immutable' in cli(root, ['record'], dict(loaded, skill_revision='b' * 40), ok=False)


def test_cli_refuses_unsupported_inputs_without_fabricating_uses(tmp_path):
    root = tmp_path
    request = event('request-1', 'skill_requested', skill='setup-workbench')
    cli(root, ['record'], request)
    cli(root, ['record'], event('status-1', 'work_status', outcome='finished'), ok=False)
    cli(root, ['record'], event('load-1', 'skill_loaded', skill='setup-workbench',
                                request_event_id='request-1', skill_revision=REV), ok=False)
    cli(root, ['record'], event('load-1', 'skill_loaded', skill='setup-workbench',
                                request_event_id='request-1', evidence_id='proof-load'), ok=False)
    cli(root, ['record'], event('use-1', 'skill_used', skill='setup-workbench', outcome='skipped',
                                request_event_id='request-1'), ok=False)
    cli(root, ['record'], event('use-1', 'skill_used', skill='setup-workbench', outcome='skipped',
                                request_event_id='request-1', chat_id='other', evidence_id='proof'), ok=False)
    cli(root, ['record'], dict(request, transcript='private raw text'), ok=False)
    state = cli(root, ['status', 'chat-1'])
    assert state['work_status'] == 'unknown'
    assert state['critical_failure_ids'] == []
    assert state['pending_event_ids'] == ['request-1']


def audit_packet():
    from ams.assessment import RUBRIC
    inventory = [
        {'id': 'A01-04', 'class': 'Quality'},
        {'id': 'site-regression', 'class': 'Regression'},
        {'id': 'requested-use', 'class': 'Critical'},
    ]
    evidence = [{'type': 'behavioral-test', 'revision': REV, 'locator': 'fixture-proof'}]
    return {
        'version': 'skill-audit-v1', 'audit_set_id': 'set-1', 'skill': 'setup-workbench',
        'skills_commit': REV, 'candidate': REV, 'baseline': 'b' * 40, 'rubric': RUBRIC,
        'conditions': {'provider': 'fixture', 'model': 'fixture-model', 'model_tier': 'mid',
                       'effort': 'fixture', 'host': 'fixture', 'tools': ['test'],
                       'loaded_artifacts': ['fixture-skill']},
        'evaluator': {'model': 'fixture-grader', 'prompt_revision': 'c' * 40,
                      'qualification': 'unqualified', 'qualification_evidence': []},
        'inventory': inventory,
        'runs': [
            {'audit_run_id': f'audit-{index}', 'completion_state': 'completed',
             'completed_at': f'2026-11-07T09:00:0{index}Z',
             'rows': [{'id': check['id'], 'result': 'Yes', 'evidence': evidence}
                      for check in inventory]}
            for index in range(1, 4)
        ],
    }


@pytest.mark.parametrize(('failed_check', 'grade'), [
    (None, 'Excellent'), (0, 'Stable'), (1, 'Functional'), (2, 'Broken'),
])
def test_audit_grade_is_worst_failure_across_three_runs(tmp_path, failed_check, grade):
    packet = audit_packet()
    if failed_check is not None:
        packet['runs'][-1]['rows'][failed_check]['result'] = 'No'
    result = cli(tmp_path, ['audit-score'], packet)
    assert result['grade'] == grade
    assert result['completed_audit_run_ids'] == ['audit-1', 'audit-2', 'audit-3']
    assert result['quality'] == {'passed': 2 if failed_check == 0 else 3, 'total': 3}
    assert result['regression'] == {'passed': 2 if failed_check == 1 else 3, 'total': 3}
    assert result['critical_missed'] is (failed_check == 2)
    assert result['qualified'] is False


def test_partial_audit_distinguishes_actual_run_from_missing_and_interrupted(tmp_path):
    packet = audit_packet()
    packet['runs'].pop()
    packet['runs'][1].update(completion_state='interrupted', completed_at=None, rows=[])
    partial = cli(tmp_path, ['audit-score'], packet)
    assert partial['completed_audit_run_ids'] == ['audit-1']
    assert partial['grade'] is None and partial['evidence_complete'] is False
    assert partial['quality'] == {'passed': 1, 'total': 1}

    packet = audit_packet()
    packet['runs'][-1]['rows'] = []
    missing = cli(tmp_path, ['audit-score'], packet)
    assert len(missing['completed_audit_run_ids']) == 3
    assert missing['grade'] == 'Broken'
    assert missing['quality'] == {'passed': 2, 'total': 3}
    assert missing['evidence_complete'] is False
    packet['runs'][1] = copy.deepcopy(packet['runs'][0])
    assert 'duplicate' in cli(tmp_path, ['audit-score'], packet, ok=False)


def test_outbox_reconciles_interrupted_delivery_without_rewriting_remote(tmp_path):
    from ams.keycheck import Settings
    from ams.rsi_observer import Outbox, Store

    cli(tmp_path, ['record'], event('request-1', 'skill_requested', skill='setup-workbench'))
    packet = audit_packet()
    packet['runs'] = packet['runs'][:1]
    cli(tmp_path, ['audit-record', '--test', '--public'], packet)
    remote = {}
    writes = []

    def http(method, url, headers, body):
        assert method == 'POST' and headers['apikey'] == 'sb_secret_fixture'
        action = url.rsplit('/', 1)[-1]
        payload = json.loads(body)
        if action.startswith('ams_get_'):
            return 200, json.dumps(remote.get(next(iter(payload.values())))).encode()
        row = payload['p_row']
        identity = row.get('event_id') or row['audit_run_id']
        writes.append(identity)
        assert identity not in remote
        remote[identity] = dict(row)
        for key in ('completed_at', 'occurred_at'):
            if remote[identity].get(key):
                remote[identity][key] = remote[identity][key].replace('Z', '+00:00')
        if identity == 'request-1':
            raise OSError('connection closed after commit')
        assert action == 'ams_append_skill_audit'
        assert row['is_test'] and row['is_public']
        assert 'rows' not in row and 'conditions' not in row
        return 200, json.dumps(dict(remote[identity], passed=True)).encode()

    settings = Settings('http://example.invalid', 'sb_secret_fixture')
    with pytest.raises(ValueError, match='pending evidence retained'):
        Outbox(tmp_path).flush(Store(settings, http))
    assert cli(tmp_path, ['status', 'chat-1'])['pending_event_ids'] == ['request-1']
    assert Outbox(tmp_path).flush(Store(settings, http)) == {'acknowledged': 2}
    assert cli(tmp_path, ['status', 'chat-1'])['pending_event_ids'] == []
    assert Outbox(tmp_path).flush(Store(settings, http)) == {'acknowledged': 0}
    assert writes == ['request-1', 'audit-1']


@pytest.mark.parametrize('reply', [b'', b'garbage', b'{}'])
def test_bad_remote_readback_never_implies_absent_or_acknowledged(tmp_path, reply):
    from ams.keycheck import Settings
    from ams.rsi_observer import Outbox, Store

    cli(tmp_path, ['record'], event('request-1', 'skill_requested', skill='setup-workbench'))

    def http(method, url, headers, body):
        assert url.endswith('/ams_get_rsi_observation')
        return 200, reply

    with pytest.raises(ValueError, match='malformed|missing'):
        Outbox(tmp_path).flush(Store(Settings('http://example.invalid', 'sb_secret_fixture'), http))
    assert cli(tmp_path, ['status', 'chat-1'])['pending_event_ids'] == ['request-1']


def test_event_time_orders_explicit_status_and_linked_request(tmp_path):
    cli(tmp_path, ['record'], event('request-1', 'skill_requested', skill='setup-workbench'))
    cli(tmp_path, ['record'], event('load-1', 'skill_loaded', skill='setup-workbench',
                                    request_event_id='request-1', skill_revision=REV, evidence_id='proof-load',
                                    occurred_at='2026-11-07T09:00:00.123Z'))
    cli(tmp_path, ['record'], event('status-1', 'work_status', outcome='blocked', evidence_id='proof-1',
                                    occurred_at='2026-11-07T09:00:00.123Z'))
    cli(tmp_path, ['record'], event('status-2', 'work_status', outcome='finished', evidence_id='proof-2'))
    assert cli(tmp_path, ['status', 'chat-1'])['work_status'] == 'blocked'


def test_audit_run_replay_and_set_frozen_identity(tmp_path):
    packet = audit_packet()
    packet['runs'] = packet['runs'][:1]
    cli(tmp_path, ['audit-record', '--test'], packet)
    cli(tmp_path, ['audit-record', '--test'], packet)
    new_packet = audit_packet()
    cli(tmp_path, ['audit-record', '--test'], new_packet)
    new_packet['conditions']['host'] = 'another-host'
    for run in new_packet['runs']:
        run['audit_run_id'] += '-rerun'
    assert 'frozen contract' in cli(tmp_path, ['audit-record', '--test'], new_packet, ok=False)


def test_empty_denominators_and_na_do_not_invent_a_score(tmp_path):
    packet = audit_packet()
    for run in packet['runs']:
        for row in run['rows']:
            row.update(result='N/A', reason='Outside the fixture scenario')
    result = cli(tmp_path, ['audit-score'], packet)
    assert result['quality'] == result['regression'] == {'passed': 0, 'total': 0}
    assert result['critical_missed'] is None
    assert result['grade'] is None
    assert result['qualified'] is False


def test_audit_pools_counts_and_keeps_critical_separate(tmp_path):
    from ams.assessment import CHECKS

    packet = audit_packet()
    quality_ids = [check for check, kind in CHECKS.items() if kind == 'Quality'][:8]
    quality = [{'id': check, 'class': 'Quality'} for check in quality_ids]
    regression = [{'id': f'site-regression-{index}', 'class': 'Regression'} for index in range(4)]
    packet['inventory'] = [*quality, *regression, {'id': 'requested-use', 'class': 'Critical'}]
    for index, run in enumerate(packet['runs']):
        proof = run['rows'][0]['evidence']
        run['rows'] = [
            {'id': check, 'result': 'Yes', 'evidence': proof}
            if index == 0 or n < 6
            else {'id': check, 'result': 'N/A', 'reason': 'Outside the fixture scenario'}
            for n, check in enumerate(quality_ids)
        ] + [
            {'id': check['id'], 'result': 'Yes', 'evidence': proof} for check in regression
        ] + [
            {'id': 'requested-use', 'result': 'No' if index == 2 else 'Yes', 'evidence': proof}
        ]
    packet['runs'][1]['rows'][0]['result'] = 'No'
    result = cli(tmp_path, ['audit-score'], packet)
    assert result['quality'] == {'passed': 19, 'total': 20}
    assert result['regression'] == {'passed': 12, 'total': 12}
    assert result['critical_missed'] is True and result['grade'] == 'Broken'


def test_same_identity_with_changed_readback_stays_pending(tmp_path):
    from ams.keycheck import Settings
    from ams.rsi_observer import Outbox, Store

    cli(tmp_path, ['record'], event('request-1', 'skill_requested', skill='setup-workbench'))
    [row] = cli(tmp_path, ['status', 'chat-1'])['events']

    def http(method, url, headers, body):
        assert url.endswith('/ams_get_rsi_observation')
        return 200, json.dumps(dict(row, skill='another-skill')).encode()

    with pytest.raises(ValueError, match='readback differs'):
        Outbox(tmp_path).flush(Store(Settings('http://example.invalid', 'sb_secret_fixture'), http))
    assert cli(tmp_path, ['status', 'chat-1'])['pending_event_ids'] == ['request-1']


def test_skill_audit_requires_exact_shared_rubric_identity(tmp_path):
    packet = audit_packet()
    packet['rubric'] = dict(packet['rubric'], checkVersion=True)
    assert 'approved r1' in cli(tmp_path, ['audit-score'], packet, ok=False)
