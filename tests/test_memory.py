"""Behavior at the public memory CLI seam, using isolated public fixtures."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import pytest

HEADER = '''---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - synthetic public fixture
source_paths:
  - workbench/wiki
last_verified: 2026-11-05
---
'''


def page(root, name, body, header=HEADER):
    path = root / 'workbench/wiki' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + body)
    return path


@pytest.fixture
def room(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / 'workbench').mkdir()
    (tmp_path / 'workbench/manifest.json').write_text(json.dumps({'lanes': {'wiki': 'workbench/wiki'}}))
    page(tmp_path, 'MEMORY.md', '# Memory\n\n- [Violet navigation](context-violet.md) - violet purpose and corrections\n')
    page(tmp_path, 'context-violet.md', '# Violet memory\n\n## Purpose\n\nViolet engines recover the durable orchard explanation. Never assume release authority.\n\n## Open questions\n\nThe winter schedule remains unresolved.\n')
    return tmp_path


def cli(root, *args, ok=True):
    run = subprocess.run([sys.executable, '-m', 'ams.memory', '--project', str(root), *args, '--json'], capture_output=True, text=True)
    if ok:
        assert run.returncode == 0, run.stderr + run.stdout
    else:
        assert run.returncode != 0
    return json.loads(run.stdout)


def jot(id, content, supersedes='none'):
    return f'''\n<!-- jot-entry -->
### {id}
Kind: intent
State: confirmed
Recorded: 2026-11-05T00:00:00Z
Author: synthetic owner
Source: chat:synthetic-public
Topic: violet
Supersedes: {supersedes}

{content}
<!-- /jot-entry -->
'''


def bindings(claims):
    return '\n<!-- ams-memory-bindings\n' + json.dumps({'version': 1, 'claims': claims}) + '\n-->\n'


def source(identity, content):
    return {'identity': identity, 'reviewed_public': True, 'observations': [{'sha256': hashlib.sha256(content).hexdigest(), 'revision': 'a'*40, 'observed_at': '2026-11-05'}]}


def test_query_recovers_contextual_prose_and_abstains(room):
    before = (room / 'workbench/wiki/context-violet.md').read_bytes()
    result = cli(room, 'query', 'violet orchard purpose')
    assert result['status'] == 'ok'
    hit = result['hits'][0]
    assert hit['page_title'] == 'Violet memory'
    assert hit['heading'] == 'Purpose'
    assert hit['kind'] == 'section'
    assert hit['state'] == 'active'
    assert hit['navigation']['page'] == 'workbench/wiki/MEMORY.md'
    assert 'release authority' in hit['content']
    assert hit['revision'].startswith('sha256:')
    assert (room / 'workbench/wiki/context-violet.md').read_bytes() == before
    assert cli(room, 'query', 'quasar marmalade')['status'] == 'unknown'


def test_correction_returns_current_entry_and_original_context(room):
    old, new = 'JOT-old', 'JOT-new'
    with (room / 'workbench/wiki/context-violet.md').open('a') as f:
        f.write(jot(old, 'Violet moon belongs to the obsolete orchard.'))
        f.write(jot(new, 'The corrected violet owner is independent.', old))
    result = cli(room, 'query', 'obsolete orchard', '--limit', '6', '--max-chars', '12000')
    corrected = next(h for h in result['hits'] if h.get('id') == new)
    assert corrected['state'] == 'confirmed'
    assert corrected['subject'] == 'The corrected violet owner is independent.'
    assert corrected['source'] == 'chat:synthetic-public'
    assert corrected['correction_context'][0]['id'] == old
    assert corrected['correction_context'][0]['state'] == 'superseded'
    assert all(h.get('id') != old for h in result['hits'])


def test_multiple_claims_sources_change_missing_restore_and_unbound(room):
    first = page(room, 'source-a.md', '# Source A\n\nPublic stable evidence.\n')
    second = page(room, 'source-b.md', '# Source B\n\nPublic second evidence.\n')
    subprocess.run(['git', '-C', str(room), 'add', '--', str(first), str(second)], check=True)
    claims = [{'id': 'claim-a', 'anchor': 'purpose', 'supersedes': None, 'sources': [source('workbench/wiki/source-a.md', first.read_bytes()), source('workbench/wiki/source-b.md', second.read_bytes())]}, {'id': 'claim-b', 'anchor': 'open-questions', 'supersedes': 'claim-older', 'sources': [source('workbench/wiki/source-b.md', second.read_bytes())]}]
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text() + bindings(claims))
    original = owner.read_bytes()
    initial = cli(room, 'check')
    assert len(initial['claims']) == 2
    assert all(s['status'] == 'unchanged' for c in initial['claims'] for s in c['sources'])
    assert initial['unbound']
    saved = first.read_bytes()
    first.write_text(first.read_text() + 'Changed evidence.\n')
    changed = cli(room, 'check')
    assert [c['id'] for c in changed['claims'] if c['possibly_stale']] == ['claim-a']
    previous = room / 'previous.json'
    previous.write_text(json.dumps(changed))
    first.write_bytes(saved)
    restored = cli(room, 'check', '--previous', str(previous))
    assert restored['claims'][0]['sources'][0]['status'] == 'restored'
    second.unlink()
    missing = cli(room, 'check')
    assert all(c['possibly_stale'] for c in missing['claims'])
    assert missing['claims'][0]['sources'][1]['status'] == 'missing'
    assert owner.read_bytes() == original
    assert cli(room, 'query', 'violet purpose')['hits'][0]['claims'][0]['id'] == 'claim-a'


@pytest.mark.parametrize('metadata', ['sensitivity: private', 'sensitivity: restricted', 'sensitivity: normal\nsensitivity: private', 'sensitivity: [normal]', 'sensitivity: "normal', 'sensitivity: NORMAL'])
def test_handling_excludes_before_body_read(room, monkeypatch, metadata):
    from ams.memory import query
    protected = page(room, 'secret.md', '# Never read\nSECRET-SENTINEL\n', HEADER.replace('sensitivity: normal', metadata))
    original = Path.open
    def guard(self, *args, **kwargs):
        handle = original(self, *args, **kwargs)
        if self == protected:
            class HeaderOnly:
                def __enter__(self): return self
                def __exit__(self, *a): handle.close()
                def readline(self, size=-1):
                    assert handle.tell() < len(HEADER.replace('sensitivity: normal', metadata).encode())
                    return handle.readline(size)
                def read(self, *a): pytest.fail('excluded body read')
            return HeaderOnly()
        return handle
    monkeypatch.setattr(Path, 'open', guard)
    result = query(room, 'SECRET-SENTINEL')
    assert result['status'] == 'unknown'
    assert result['excluded']


def test_ignored_hidden_symlinks_escape_and_external_sources(room):
    page(room, 'ignored.md', '# Ignored\nSECRET-SENTINEL\n')
    (room / '.gitignore').write_text('workbench/wiki/ignored.md\n')
    page(room, '.jot-private-local.md', '# Private\nSECRET-SENTINEL\n')
    (room / 'workbench/wiki/escape.md').symlink_to(room / '.gitignore')
    result = cli(room, 'query', 'SECRET-SENTINEL')
    assert result['status'] == 'unknown'
    assert any(e['reason'] == 'unsafe-path' for e in result['excluded'])
    assert 'SECRET-SENTINEL' not in json.dumps(result).replace(result['query'], '')
    # Explicit source review cannot turn a secret-bearing root file into a body source.
    (room / '.env').write_text('NEVER-FINGERPRINT')
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text() + bindings([{'id': 'bad', 'anchor': 'purpose', 'sources': [source('.env', b'NEVER-FINGERPRINT'), source('../outside.md', b'outside'), source('https://example.test/secret', b'external')]}]))
    checked = cli(room, 'check')
    assert all(s['status'] == 'unavailable' for s in checked['claims'][0]['sources'])


def test_malformed_jot_or_binding_fails_closed_per_page(room):
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text() + '\n<!-- jot-entry -->\nMalformed secret orchard\n')
    result = cli(room, 'query', 'orchard')
    assert not result['hits']
    assert any(e['reason'] == 'invalid-jot' for e in result['excluded'])
    owner.write_text(HEADER + '# Violet\n\nOrchard\n' + '\n<!-- ams-memory-bindings\n{bad}\n-->')
    assert any(e['reason'] == 'invalid-bindings' for e in cli(room, 'query', 'orchard')['excluded'])


def test_output_bound_is_full_json_not_just_excerpt(room):
    with (room / 'workbench/wiki/MEMORY.md').open('a') as f:
        f.write('\n- [Huge violet orchard](huge.md) - violet orchard purpose\n')
    page(room, 'huge.md', '# Huge violet\n\n## Purpose\n\n' + 'violet orchard '*3000)
    result = cli(room, 'query', 'violet orchard', '--max-chars', '1200', '--limit', '2')
    assert len(json.dumps(result, ensure_ascii=False, indent=2)) + 1 <= 1200
    assert result['continuation']
    assert result['omitted'] > 0 or result['truncated']
    assert cli(room, 'query', 'violet', '--max-chars', '12', ok=False)['status'] == 'blocked'


def test_query_does_not_treat_code_fences_as_claim_headings(room):
    page(room, 'code.md', '# Code violet\n\n## Example\n\n```md\n# invented violet heading\n```\n\nActual violet example.\n')
    result = cli(room, 'query', 'invented violet', '--max-chars', '12000')
    assert all(h['heading'] != 'invented violet heading' for h in result['hits'])


def test_untracked_reviewed_source_is_not_read(room, monkeypatch):
    from ams.memory import check
    untracked = page(room, 'untracked.md', '# Untracked\nPRIVATE-SENTINEL\n')
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text() + bindings([{'id': 'claim', 'anchor': 'purpose', 'sources': [source('workbench/wiki/untracked.md', untracked.read_bytes())]}]))
    result = check(room)
    assert result['claims'][0]['sources'][0]['reason'] == 'source-not-tracked'


def test_empty_baseline_cannot_establish_same_source(room):
    from ams.memory import evaluate, MemoryError
    cases = {'version': 1, 'split': 'development', 'source_revision': 'a'*40, 'cases': [{'id': 'valid', 'query': 'violet', 'expected_sources': []}], 'budget': {'limit': 6, 'max_chars': 6400}}
    with pytest.raises(MemoryError, match='invalid-baseline'):
        evaluate(room, cases, {'version': 1, 'source_revision': 'a'*40, 'wiki_sha256': {}, 'budget': cases['budget']})


def test_partial_lexical_overlap_does_not_answer_unknown(room):
    assert cli(room, 'query', 'quasar marmalade orchard')['status'] == 'unknown'


def test_long_correction_context_is_recoverable_and_truncation_explicit(room):
    old = 'violet obsolete orchard ' + 'retained source evidence ' * 300
    with (room / 'workbench/wiki/context-violet.md').open('a') as f:
        f.write(jot('JOT-old-long', old))
        f.write(jot('JOT-current-long', 'Violet orchard now has the corrected independent owner.', 'JOT-old-long'))
    roomy = cli(room, 'query', 'violet obsolete orchard', '--limit', '1', '--max-chars', '18000')
    hit = roomy['hits'][0]
    assert hit['id'] == 'JOT-current-long'
    previous = hit['correction_context'][0]
    assert previous['content'] == old
    assert previous['content_truncated'] is False
    small = cli(room, 'query', 'violet obsolete orchard', '--limit', '1', '--max-chars', '4000')
    assert len(json.dumps(small, ensure_ascii=False, indent=2)) + 1 <= 4000
    short = small['hits'][0]['correction_context'][0]
    assert short['content_truncated'] is True
    assert short['continuation'] == 'workbench/wiki/context-violet.md#jot-old-long'
    assert small['truncated'] and small['continuation']
    assert cli(room, 'query', 'violet obsolete orchard', '--limit', '1', '--max-chars', '18000')['hits'][0]['correction_context'][0]['content'] == old


def test_duplicate_heading_binding_selects_same_anchor_and_subtree(room):
    selected = '## Purpose\n\nSecond meadow evidence.\n\n### Detail\n\nNested retained evidence.\n\n'
    original = '# Repeated source\n\n## Purpose\n\nFirst meadow evidence.\n\n' + selected + '## Limits\n\nUnrelated limit.\n'
    evidence = page(room, 'repeated.md', original)
    subprocess.run(['git', '-C', str(room), 'add', '--', str(evidence)], check=True)
    owner = room / 'workbench/wiki/context-violet.md'
    owner.write_text(owner.read_text() + bindings([{'id': 'second-source', 'anchor': 'purpose', 'sources': [source('workbench/wiki/repeated.md#purpose-1', selected.encode())]}]))
    initial = cli(room, 'check')['claims'][0]['sources'][0]
    assert initial['status'] == 'unchanged'
    found = cli(room, 'query', 'second meadow', '--max-chars', '12000')
    assert any(h['anchor'] == 'purpose-1' for h in found['hits'])
    evidence.write_text(evidence.read_text().replace('First meadow', 'Changed first meadow'))
    assert cli(room, 'check')['claims'][0]['sources'][0]['status'] == 'unchanged'
    saved = evidence.read_bytes()
    evidence.write_text(evidence.read_text().replace('Nested retained', 'Nested changed'))
    changed = cli(room, 'check')
    assert changed['claims'][0]['sources'][0]['status'] == 'possibly-stale'
    previous = room / 'previous-duplicate.json'
    previous.write_text(json.dumps(changed))
    evidence.write_bytes(saved)
    assert cli(room, 'check', '--previous', str(previous))['claims'][0]['sources'][0]['status'] == 'restored'


def test_empty_evaluation_cases_are_not_a_passing_comparison(room):
    cases = room / 'empty-cases.json'
    cases.write_text(json.dumps({'version': 1, 'split': 'development', 'source_revision': 'a'*40, 'budget': {'limit': 6, 'max_chars': 6400}, 'cases': []}))
    result = cli(room, 'evaluate', '--cases', str(cases), ok=False)
    assert result['reason'] == 'invalid-evaluation'
