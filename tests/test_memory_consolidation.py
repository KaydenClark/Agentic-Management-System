"""Public consolidation behavior; all prose and source claims are synthetic/public."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from test_memory import HEADER, cli, page, room, jot


def fingerprint(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def exercise(room):
    source = page(room, 'source-violet.md', '# Synthetic public source\n\nViolet belongs to an independent orchard. Winter remains unresolved.\n')
    subprocess.run(['git', '-C', str(room), 'add', '--', str(source)], check=True)
    summary = page(room, 'design-concepts/violet.md', '# Violet synthesis\n\n[Violet purpose](../context-violet.md#purpose) — Violet belongs to the obsolete orchard.\n')
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text().replace('Violet engines recover the durable orchard explanation.', 'Violet belongs to the obsolete orchard.'))
    request = {'topic': 'violet orchard purpose', 'owner': 'workbench/wiki/context-violet.md', 'changes': [
        {'id': 'correction', 'classification': 'correction', 'kind': 'observation', 'state': 'experimental', 'summary': 'Synthetic correction only; independent orchard, winter unresolved.', 'sources': [{'identity': 'workbench/wiki/source-violet.md', 'reviewed_public': True}]}
    ], 'edits': [
        {'target': 'workbench/wiki/context-violet.md', 'change': 'correction', 'before': 'Violet belongs to the obsolete orchard.', 'after': 'Violet belongs to an independent orchard. Winter remains unresolved.'},
        {'target': 'workbench/wiki/design-concepts/violet.md', 'change': 'correction', 'before': 'Violet belongs to the obsolete orchard.', 'after': 'Violet belongs to an independent orchard; winter unresolved.'}
    ], 'jots': []}
    return room, request


def save(root, name, value):
    path = root / name
    path.write_text(json.dumps(value))
    return str(path)


def plan(root, request, ok=True):
    return cli(root, 'consolidate', '--request', save(root, 'request.json', request), ok=ok)


def apply(root, result, ok=True, revisions=None, authorization=None):
    return cli(root, 'consolidate', '--apply', '--plan', save(root, 'plan.json', result), '--authorize', authorization or 'apply:' + result['plan_id'], '--revisions', save(root, 'revisions.json', revisions if revisions is not None else result['revisions']), ok=ok)


def test_plan_finds_existing_owner_and_actual_incoming_summaries_without_writes(exercise):
    root, request = exercise
    before = {str(p): p.read_bytes() for p in root.rglob('*.md')}
    result = plan(root, request)
    assert result['operation'] == 'consolidate-plan'
    assert result['owner'] == request['owner']
    assert result['classifications']['correction'] == ['correction']
    assert {i['page'] for i in result['incoming']} == {'workbench/wiki/MEMORY.md', 'workbench/wiki/design-concepts/violet.md'}
    assert result['sources'][0]['sha256'] == fingerprint((root / 'workbench/wiki/source-violet.md').read_bytes())
    assert all(p.read_bytes() == before[str(p)] for p in root.rglob('*.md'))


def test_apply_requires_exact_authority_revisions_and_corrects_prose(exercise):
    root, request = exercise
    result = plan(root, request)
    assert apply(root, result, ok=False, authorization='general-permission')['reason'] == 'operation-authority-required'
    assert apply(root, result, ok=False, revisions={'targets': {}, 'sources': {}})['reason'] == 'revision-acknowledgment-required'
    receipt = apply(root, result)
    assert receipt['status'] == 'applied'
    assert len(receipt['written']) == 2
    found = cli(root, 'query', 'violet independent orchard', '--max-chars', '16000')
    assert any('independent orchard' in h['content'] for h in found['hits'])
    assert all('obsolete orchard' not in h['content'] for h in found['hits'])


def test_native_correction_retains_anchored_source_and_exact_confirmed_entry(exercise):
    import shutil
    root, request = exercise
    shutil.copytree(Path(__file__).resolve().parents[1] / 'workbench/tools', root / 'workbench/tools')
    owner = root / request['owner']
    old = jot('JOT-old', 'Violet belongs to the obsolete orchard.').replace('Kind: intent\nState: confirmed', 'Kind: observation\nState: experimental')
    confirmed = jot('JOT-confirmed', 'EXACT SYNTHETIC OWNER READBACK: Winter remains unresolved.')
    evidence = jot('JOT-source', 'Violet belongs to an independent orchard.').replace('Kind: intent\nState: confirmed', 'Kind: observation\nState: current')
    owner.write_text(owner.read_text() + old + confirmed + evidence)
    subprocess.run(['git', '-C', str(root), 'add', '--', str(owner)], check=True)
    request['edits'][0]['before'] += ' Never assume release authority.'
    request['edits'][0]['after'] += ' Never assume release authority.'
    request['changes'][0]['sources'] = [{'identity': request['owner'] + '#jot-source', 'reviewed_public': True}]
    request['jots'] = [{'target': request['owner'], 'change': 'correction', 'kind': 'observation', 'state': 'experimental', 'source': request['owner'] + '#jot-source', 'author': 'synthetic public exercise', 'content': 'Violet belongs to an independent orchard. Winter remains unresolved.', 'supersedes': 'JOT-old'}]
    before_source = (root / 'workbench/wiki/source-violet.md').read_bytes()
    result = plan(root, request)
    applied = apply(root, result)
    assert applied['status'] == 'applied'
    raw = owner.read_text()
    assert old in raw and confirmed in raw and evidence in raw
    assert (root / 'workbench/wiki/source-violet.md').read_bytes() == before_source
    native = applied['native'][0]['entry']
    assert native['supersedes'] == 'JOT-old' and native['state'] == 'experimental'
    result = cli(root, 'query', 'violet independent orchard', '--max-chars', '24000')
    hit = next(h for h in result['hits'] if h.get('id') == native['id'])
    assert hit['correction_context'][0]['id'] == 'JOT-old'
    assert 'obsolete orchard' not in '\n'.join(h['content'] for h in result['hits'])


@pytest.mark.parametrize('failure', ['stale', 'missing', 'private', 'symlink', 'source-change'])
def test_whole_plan_preflight_refuses_without_partial_writes(exercise, failure):
    root, request = exercise
    result = plan(root, request)
    summary = root / request['edits'][1]['target']
    if failure == 'stale':
        summary.write_text(summary.read_text() + '\nConcurrent edit.\n')
    elif failure == 'missing':
        summary.unlink()
    elif failure == 'private':
        summary.write_text(summary.read_text().replace('sensitivity: normal', 'sensitivity: private'))
    elif failure == 'symlink':
        summary.unlink()
        summary.symlink_to(root / 'workbench/wiki/source-violet.md')
    else:
        source = root / 'workbench/wiki/source-violet.md'
        source.write_text(source.read_text() + '\nChanged evidence.\n')
    before = {str(p): p.read_bytes() for p in root.rglob('*.md') if p.is_file()}
    blocked = apply(root, result, ok=False)
    assert blocked['status'] == 'blocked'
    assert all(p.read_bytes() == before[str(p)] for p in root.rglob('*.md') if p.is_file())
    assert 'recovery' not in blocked


@pytest.mark.parametrize('target', ['../escape.md', 'workbench/wiki/unrelated.md', 'workbench/wiki/missing.md', 'RUNBOOK.md'])
def test_unsupported_targets_never_write(exercise, target):
    root, request = exercise
    page(root, 'unrelated.md', '# Unrelated\n\nViolet belongs to the obsolete orchard.\n')
    request['edits'][1]['target'] = target
    before = (root / request['owner']).read_bytes()
    assert plan(root, request, ok=False)['status'] == 'blocked'
    assert (root / request['owner']).read_bytes() == before


def test_pending_owner_intent_cannot_replace_confirmed_understanding(exercise):
    root, request = exercise
    request['changes'][0].update(kind='intent', state='unresolved', classification='contradiction')
    before = (root / request['owner']).read_bytes()
    result = plan(root, request, ok=False)
    assert result['reason'] == 'unresolved-governing-replacement'
    assert (root / request['owner']).read_bytes() == before
    request['edits'] = []
    result = plan(root, request)
    assert result['unresolved'] == ['correction']
    assert result['classifications']['contradiction'] == ['correction']
    assert result['proposed'] == {}


def test_inference_requires_attribution_limits_and_cannot_be_confirmed(exercise):
    root, request = exercise
    change = request['changes'][0]
    change.update(kind='inference', state='confirmed')
    assert plan(root, request, ok=False)['reason'] == 'unsupported-confirmation'
    change.update(state='experimental', attribution='Synthetic agent, from public observations', limits='One fixture only; winter unresolved.')
    result = plan(root, request)
    assert result['request']['changes'][0]['limits'] == change['limits']


def test_mid_write_failure_returns_recoverable_originals(exercise, monkeypatch):
    from ams import memory_consolidation as module
    root, request = exercise
    result = module.consolidation_plan(root, request)
    original = module._atomic_write
    calls = []
    def fail_second(path, raw):
        calls.append(path)
        if len(calls) == 2:
            raise OSError('synthetic disk failure')
        original(path, raw)
    monkeypatch.setattr(module, '_atomic_write', fail_second)
    receipt = module.consolidation_apply(root, result, 'apply:' + result['plan_id'], result['revisions'])
    assert receipt['status'] == 'failed' and len(receipt['written']) == 1
    recovery = Path(receipt['recovery'])
    journal = json.loads((recovery / 'journal.json').read_text())
    for target, row in journal['originals'].items():
        assert 'sha256:' + fingerprint((recovery / row['backup']).read_bytes()) == row['revision']
    assert 'obsolete orchard' in (root / request['edits'][1]['target']).read_text()


def test_unresolved_evidence_can_be_appended_without_replacing_established_claim(exercise):
    root, request = exercise
    request['changes'][0].update(classification='contradiction', state='unresolved')
    request['edits'] = [request['edits'][0]]
    request['edits'][0]['after'] = request['edits'][0]['before'] + ' Conflicting synthetic public evidence reports an independent orchard; unresolved.'
    result = plan(root, request)
    assert result['unresolved'] == ['correction']
    assert apply(root, result)['status'] == 'applied'
    found = cli(root, 'query', 'violet conflicting orchard')
    assert any('Conflicting synthetic public evidence' in h['content'] and 'obsolete orchard' in h['content'] for h in found['hits'])


def test_owner_discovery_without_explicit_owner_reuses_existing_topic(exercise):
    root, request = exercise
    del request['owner']
    result = plan(root, request)
    assert result['owner'] == 'workbench/wiki/context-violet.md'
    assert len(result['proposed']) == 2
