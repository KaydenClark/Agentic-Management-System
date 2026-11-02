"""Task birth metadata refresh is bounded, undoable and conditional."""
import copy
import json

import pytest

from ams import build_history as bh, writer
from test_build_history import StubSupabase, _settings, URL, FAKE_PUBLISHABLE

PATH = 'workbench/specs/S-001-demo/tasks/TK-001/TASK.md'
SHA = 'a' * 40


def task():
    return {'kind': 'task', 'subject': 'S-001 TK-001', 'summary': 'Original Task declaration',
            'occurred_at': '2026-11-01T10:00:00Z', 'source_kind': 'path',
            'source_ref': 'S-001/TK-001', 'source_url': f'{writer.REPO_URL}/blob/{SHA}/{PATH}',
            'strength': 'recorded_fact', 'is_test': False,
            'detail': {'spec': 'S-001', 'task': 'TK-001', 'status': 'ready',
                       'record': PATH, 'created_commit': SHA}}


def stale_store(want):
    store = StubSupabase(copy.deepcopy([want]))
    store.rows[0]['detail']['status'] = 'done'
    return store


def test_metadata_only_mismatch_is_named_without_writing(capsys):
    want = task(); store = stale_store(want)
    assert bh.readcheck([want], URL, FAKE_PUBLISHABLE, store) == 1
    assert 'detail' in capsys.readouterr().out
    assert bh.import_rows([want], _settings(), store) == 0
    assert 'changed: 1 (not updated' in capsys.readouterr().out
    assert store.rows[0]['detail']['status'] == 'done'
    assert not [c for c in store.calls if c[0] == 'PATCH']


def test_refresh_preserves_annotations_history_and_direct_current_birth_metadata(capsys):
    want = task(); store = stale_store(want); saved = store.rows[0]
    prior = {'at': '2026-11-01T09:00:00Z', 'previous': {'summary': 'Old summary'}}
    annotation = {'quoted': 'commas, quotes " and slash\\', 'unicode': 'λ', 'array': [1, True]}
    saved['detail'].update(annotation=annotation, refreshed=[prior])
    original = copy.deepcopy(saved['detail'])
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 0
    # Direct current readback, not a historical state accepted by readcheck.
    for key, value in want['detail'].items():
        assert saved['detail'][key] == value
    assert saved['detail']['annotation'] == annotation
    assert saved['detail']['refreshed'][0] == prior
    previous = saved['detail']['refreshed'][-1]['previous']['detail']
    assert previous == {key: original[key] for key in want['detail']}
    assert 'refreshed' not in previous and 'annotation' not in previous
    before_retry = copy.deepcopy(saved)
    patches = len([c for c in store.calls if c[0] == 'PATCH'])
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 0
    assert saved == before_retry
    assert len([c for c in store.calls if c[0] == 'PATCH']) == patches


def test_task_metadata_refresh_states_preserve_old_pin_without_hiding_current_state():
    want = task(); old = copy.deepcopy(want); old['detail']['status'] = 'done'
    store = StubSupabase(copy.deepcopy([old]))
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 0
    assert store.rows[0]['detail']['status'] == 'ready'
    assert bh.readcheck([old], URL, FAKE_PUBLISHABLE, store) == 0
    assert bh.readcheck([want], URL, FAKE_PUBLISHABLE, store) == 0
    unknown = copy.deepcopy(want); unknown['detail']['status'] = 'never recorded'
    assert bh.readcheck([unknown], URL, FAKE_PUBLISHABLE, store) == 1


@pytest.mark.parametrize('mutation', ['annotation', 'audit', 'canonical', 'boolean-type'])
def test_task_metadata_or_audit_race_is_refused_without_overwrite(mutation):
    want = task(); store = stale_store(want); saved = store.rows[0]
    saved['detail']['typed_note'] = True
    concurrent = None
    def racing(method, url, headers, body):
        nonlocal concurrent
        if method == 'PATCH':
            if mutation == 'annotation':
                saved['detail']['annotation'] = 'Concurrent author'
            elif mutation == 'audit':
                saved['detail']['refreshed'] = [{'at': '2026-11-02T09:00:00Z', 'previous': {'summary': 'Concurrent'}}]
            elif mutation == 'boolean-type':
                saved['detail']['typed_note'] = 1
            else:
                saved['detail']['record'] = 'different-source.md'
            concurrent = copy.deepcopy(saved)
        return store(method, url, headers, body)
    assert bh.import_rows([want], _settings(), racing, refresh_changed=True) == 1
    assert saved == concurrent


def test_task_metadata_source_key_presence_and_undo_are_preserved():
    want = task(); del want['detail']['created_commit']; want['detail']['recorded_commit'] = SHA
    old = task(); store = StubSupabase(copy.deepcopy([old]))
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 0
    saved = store.rows[0]
    assert 'created_commit' not in saved['detail'] and saved['detail']['recorded_commit'] == SHA
    assert saved['detail']['refreshed'][-1]['previous']['detail'] == old['detail']
    assert bh.readcheck([old], URL, FAKE_PUBLISHABLE, store) == 0


@pytest.mark.parametrize('detail', [None, [], 'not an object'])
def test_unsupported_stored_task_detail_refuses_before_patch(detail):
    want = task(); store = StubSupabase(copy.deepcopy([want])); store.rows[0]['detail'] = detail
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 1
    assert not [c for c in store.calls if c[0] == 'PATCH']


def test_unrelated_event_metadata_stays_outside_comparison():
    want = task(); want.update(kind='spec_event', source_ref='spec#evidence-1')
    store = stale_store(want)
    assert bh.readcheck([want], URL, FAKE_PUBLISHABLE, store) == 0
    assert bh.import_rows([want], _settings(), store, refresh_changed=True) == 0
    assert not [c for c in store.calls if c[0] == 'PATCH']



def test_task_undo_with_same_timestamp_keeps_real_intermediate_state(monkeypatch):
    monkeypatch.setattr(bh, 'utc', lambda _: '2026-11-02T12:00:00Z')
    first = task(); store = stale_store(first)
    assert bh.import_rows([first], _settings(), store, refresh_changed=True) == 0
    final = copy.deepcopy(first); final['summary'] = 'Corrected source wording'
    assert bh.import_rows([final], _settings(), store, refresh_changed=True) == 0
    assert bh.readcheck([first], URL, FAKE_PUBLISHABLE, store) == 0
    never = copy.deepcopy(final); never['detail']['status'] = 'done'
    assert bh.readcheck([never], URL, FAKE_PUBLISHABLE, store) == 1


def test_task_refresh_does_not_accept_a_success_body_with_stale_current_metadata():
    want = task(); store = stale_store(want)
    def stale_response(method, url, headers, body):
        if method == 'PATCH':
            return 200, json.dumps(store.rows).encode()
        return store(method, url, headers, body)
    assert bh.import_rows([want], _settings(), stale_response, refresh_changed=True) == 1
    assert store.rows[0]['detail']['status'] == 'done'
