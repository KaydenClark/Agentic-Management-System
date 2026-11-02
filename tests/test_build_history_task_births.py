"""Task creation is immutable; materialization/removal changes execution owners."""
import json
import subprocess
from pathlib import Path

import pytest

from ams import build_history as bh
from test_build_history import _git, _write, git_runner

SPEC = 'workbench/specs/S-001-demo/SPEC.md'
TASK = 'workbench/specs/S-001-demo/tasks/TK-001/TASK.md'


def spec(rows=''):
    return ('# S-001 - Demo\n\n**Spec ID:** S-001\n**Status:** active\n\n'
            '## Vertical Implementation Slices\n\n'
            '| Task | Slice | Status | Blockers | Proof |\n|---|---|---|---|---|\n' + rows)


def native(slice='Original native task', status='ready', task='TK-001'):
    return (f'# {task} - {slice}\n\n**Task ID:** {task}\n**Spec ID:** S-001\n'
            f'**Slice:** {slice}\n**Status:** {status}\n')


def commit(repo, message, when='2026-11-01T10:00:00Z'):
    _git(repo, 'add', '-A')
    _git(repo, 'commit', '-qm', message, when=when)
    return _git(repo, 'rev-parse', 'HEAD')


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    _git(root, 'init', '-qb', 'main')
    return root


def records(repo, tasks, path=SPEC, ref='HEAD'):
    def lifecycle(args):
        item = {'id': 'S-001', 'path': path, 'title': 'Demo', 'status': 'active'}
        if args[0] == 'list':
            return json.dumps({'specs': [item]})
        return json.dumps({**item, 'tasks': tasks, 'retiredTasks': []})
    real_git = git_runner(repo)
    def git(args):
        return real_git([ref if a == 'HEAD' else a for a in args])
    return bh.record_rows(git, lifecycle)


def births(rows):
    return {row['source_ref']: row for row in rows if row['kind'] == 'task'}


def test_table_materialization_preserves_entire_creation_and_adds_receipt(repo):
    _write(repo, SPEC, spec('| TK-001 | Original planned task | ready | none | pending |\n'))
    commit(repo, 'Declare task')
    before = births(records(repo, [{'id': 'TK-001', 'slice': 'Original planned task', 'status': 'ready'}]))
    _write(repo, SPEC, spec())
    _write(repo, TASK, native('Different current slice', 'done') + '\n## Receipt\n\n'
           '| Run | Branch | HEAD SHA |\n|---|---|---|\n| 1 | feature/task | abc123 |\n')
    commit(repo, 'Materialize execution record', '2026-11-01T11:00:00Z')
    after = records(repo, [{'id': 'TK-001', 'slice': 'Different current slice', 'status': 'done'}])
    assert births(after) == before
    assert len([r for r in after if r['kind'] == 'task_receipt']) == 1


def test_removed_table_tasks_remain_births_without_current_assignments(repo):
    _write(repo, SPEC, spec('| TK-001 | Removed task | ready | none | pending |\n'))
    commit(repo, 'Declare planned task')
    before = births(records(repo, [{'id': 'TK-001', 'slice': 'Removed task', 'status': 'ready'}]))
    _write(repo, SPEC, spec())
    commit(repo, 'Remove current plan', '2026-11-01T11:00:00Z')
    assert births(records(repo, [])) == before
    assert not (repo / TASK).exists()


def test_native_birth_does_not_follow_mutable_slice_or_status(repo):
    _write(repo, SPEC, spec())
    _write(repo, TASK, native())
    commit(repo, 'Native birth')
    before = births(records(repo, [{'id': 'TK-001', 'slice': 'Original native task', 'status': 'ready'}]))
    _write(repo, TASK, native('Changed execution slice', 'done'))
    commit(repo, 'Change current assignment', '2026-11-01T11:00:00Z')
    assert births(records(repo, [{'id': 'TK-001', 'slice': 'Changed execution slice', 'status': 'done'}])) == before


@pytest.mark.parametrize('form', ['table', 'native'])
def test_registered_spec_rename_keeps_original_birth_source(repo, form):
    _write(repo, SPEC, spec('| TK-001 | Original planned task | ready | none | pending |\n' if form == 'table' else ''))
    if form == 'native':
        _write(repo, TASK, native('Original planned task'))
    commit(repo, 'Birth')
    task = [{'id': 'TK-001', 'slice': 'Original planned task', 'status': 'ready'}]
    before = births(records(repo, task))
    new = 'workbench/specs/S-001-renamed/SPEC.md'
    _git(repo, 'mv', str(Path(SPEC).parent), str(Path(new).parent))
    commit(repo, 'Rename registered owner', '2026-11-01T11:00:00Z')
    assert births(records(repo, task, path=new)) == before


def test_pinned_before_and_after_and_nonmonotone_clock_use_graph_birth(repo):
    _write(repo, SPEC, spec('| TK-001 | Original | ready | none | pending |\n'))
    first = commit(repo, 'Original declaration', '2026-11-01T10:30:00Z')
    _write(repo, SPEC, spec('| TK-001 | Changed | done | none | passed |\n'))
    second = commit(repo, 'Changed with earlier clock', '2026-11-01T10:00:00Z')
    original = births(records(repo, [{'id': 'TK-001', 'slice': 'Original', 'status': 'ready'}], ref=first))
    assert births(records(repo, [{'id': 'TK-001', 'slice': 'Changed', 'status': 'done'}], ref=second)) == original


def test_incomparable_independent_births_refuse_instead_of_timestamp_tiebreak(repo):
    _write(repo, SPEC, spec())
    base = commit(repo, 'Spec only')
    _write(repo, TASK, native('Branch A'))
    commit(repo, 'A birth', '2026-11-01T10:10:00Z')
    _git(repo, 'switch', '-qc', 'other', base)
    _write(repo, TASK, native('Branch B'))
    commit(repo, 'B birth', '2026-11-01T10:20:00Z')
    _git(repo, 'switch', '-q', 'main')
    _git(repo, 'merge', '-q', '--no-ff', '-s', 'ours', 'other', '-m', 'Keep A content')
    with pytest.raises(bh.RefusedError, match='ambiguous|conflicting'):
        records(repo, [{'id': 'TK-001', 'slice': 'Branch A', 'status': 'ready'}])


def test_unregistered_same_id_path_is_not_birth_authority(repo):
    _write(repo, 'unregistered/SPEC.md', spec('| TK-001 | Foreign | ready | none | pending |\n'))
    commit(repo, 'Unregistered lookalike')
    _write(repo, SPEC, spec())
    _write(repo, TASK, native())
    actual = commit(repo, 'Registered native birth', '2026-11-01T11:00:00Z')
    row = births(records(repo, [{'id': 'TK-001', 'slice': 'Original native task', 'status': 'ready'}]))['S-001/TK-001']
    assert row['source_url'] == bh._blob_url(actual, TASK)


def test_inline_code_cannot_supply_native_identity_fields(repo):
    _write(repo, SPEC, spec())
    _write(repo, TASK, '# TK-001 - Example\n\nExample ``\n**Task ID:** TK-001\n'
           '**Status:** ready\nend ``\n')
    commit(repo, 'Literal metadata is not a Task identity')
    with pytest.raises(bh.RefusedError, match='identity'):
        records(repo, [])


@pytest.mark.parametrize('wrapper', ['fence', 'comment', 'inline'])
def test_code_and_comment_tables_cannot_declare_births(repo, wrapper):
    table = spec('| TK-001 | Only an example | ready | none | pending |\n').split('## ', 1)[1]
    table = '## ' + table
    wrappers = {'fence': '```markdown\n' + table + '```\n',
                'comment': '<!--\n' + table + '-->\n',
                'inline': 'Example ``\n' + '\n'.join('    ' + line for line in table.splitlines() if line) + '\nend ``\n'}
    _write(repo, SPEC, spec().split('## ', 1)[0] + wrappers[wrapper])
    commit(repo, 'Table-shaped examples')
    assert births(records(repo, [])) == {}


@pytest.mark.parametrize('field,value', [('Task ID', 'TK-999'), ('Spec ID', 'S-999')])
def test_native_parent_or_task_identity_conflict_refuses(repo, field, value):
    _write(repo, SPEC, spec())
    text = native().replace(f'**{field}:** ' + ('TK-001' if field == 'Task ID' else 'S-001'),
                            f'**{field}:** {value}')
    _write(repo, TASK, text)
    commit(repo, 'Conflicting canonical record identity')
    with pytest.raises(bh.RefusedError, match='identity'):
        records(repo, [])


def test_table_and_native_conflicting_same_commit_birth_refuses(repo):
    _write(repo, SPEC, spec('| TK-001 | A different task | ready | none | pending |\n'))
    _write(repo, TASK, native())
    commit(repo, 'Two incompatible original definitions')
    with pytest.raises(bh.RefusedError, match='ambiguous|conflicting'):
        records(repo, [])


def resolved_scaffold(repo, resolution='valid', competing=False, proof=None, proof_form='field'):
    _write(repo, SPEC, spec())
    base = commit(repo, 'Register Spec')
    _git(repo, 'switch', '-qc', 'owner')
    owner = native('Original owner assignment') + '\n## Acceptance\n\n- [ ] Original check.\n'
    _write(repo, TASK, owner)
    commit(repo, 'Declare actual Task', '2026-11-01T12:00:00Z')
    expected = births(records(repo, []))
    claimed = owner.replace('**Status:** ready', '**Status:** in-progress\n**Claimed by:** fixture-owner\n**Current claimant:** fixture-owner')
    _write(repo, TASK, claimed)
    commit(repo, 'Claim S-001 TK-001', '2026-11-01T11:00:00Z')
    _git(repo, 'switch', '-qc', 'scaffold', base)
    scaffold_text = native('Generated corrective scaffold')
    if proof is not None:
        field = '**Proof:** ' + proof + '\n'
        scaffold_text += field if proof_form == 'field' else '\n## Check\n\n' + field if proof_form == 'bodyfield' else '```markdown\n' + field + '```\n'
    _write(repo, TASK, scaffold_text)
    scaffold = commit(repo, 'Historical verdict scaffold', '2026-11-01T09:00:00Z')
    if competing:
        _write(repo, TASK, native('Generated corrective scaffold', 'in-progress') +
               '**Claimed by:** another-owner\n**Current claimant:** another-owner\n')
        commit(repo, 'Claim S-001 TK-001')
    _git(repo, 'switch', '-q', 'owner')
    _git(repo, 'merge', '--no-ff', '--no-commit', '-s', 'ours', 'scaffold')
    declaration = ('The native failed verdict generated this same Task ID. '
                   'Its generic assignment and the already claimed bounded assignment describe the same correction; preserve the current claimant, detailed acceptance '
                   'and original failed-review row. Native verdict source commit '
                   f'`{scaffold}` is merged into this branch.')
    if resolution == 'code':
        declaration = '```markdown\n' + declaration + '\n```'
    elif resolution == 'comment':
        declaration = '<!-- ' + declaration + ' -->'
    elif resolution == 'inline':
        declaration = '``' + declaration + '``'
    elif resolution == 'wrong-source':
        declaration = declaration.replace(scaffold, base)
    elif resolution == 'duplicate':
        declaration += '\n\n## Native corrective provenance\n\n' + declaration
    document = claimed if resolution == 'absent' else claimed + '\n## Native corrective provenance\n\n' + declaration + '\n'
    if resolution == 'changed-assignment':
        document = document.replace('Original check.', 'Different check.')
    _write(repo, TASK, document)
    commit(repo, 'Resolve historical scaffold into claimed Task', '2026-11-01T08:00:00Z')
    return expected


def test_resolved_unclaimed_scaffold_uses_original_native_owner_birth(repo):
    expected = resolved_scaffold(repo)
    assert births(records(repo, [])) == expected
    text = (repo / TASK).read_text().replace('**Slice:** Original owner assignment', '**Slice:** Changed current assignment')
    _write(repo, TASK, text)
    commit(repo, 'Later description has no birth authority', '2026-11-01T07:00:00Z')
    assert births(records(repo, [])) == expected


def test_independently_claimed_collision_still_refuses(repo):
    resolved_scaffold(repo, competing=True)
    with pytest.raises(bh.RefusedError, match='ambiguous|conflicting'):
        records(repo, [])


@pytest.mark.parametrize('resolution', ['absent', 'code', 'comment', 'inline', 'wrong-source',
                                         'duplicate', 'changed-assignment'])
def test_unsupported_scaffold_resolution_still_refuses(repo, resolution):
    resolved_scaffold(repo, resolution)
    with pytest.raises(bh.RefusedError, match='ambiguous|conflicting'):
        records(repo, [])


def test_duplicate_native_metadata_refuses(repo):
    _write(repo, SPEC, spec())
    _write(repo, TASK, native() + '**Task ID:** TK-001\n')
    commit(repo, 'Duplicate identity field')
    with pytest.raises(bh.RefusedError, match='metadata'):
        records(repo, [])


def test_symlink_cannot_supply_native_birth(repo):
    _write(repo, SPEC, spec())
    (repo / TASK).parent.mkdir(parents=True)
    (repo / TASK).symlink_to('untrusted-outside-record.md')
    commit(repo, 'Task path is not a regular blob')
    with pytest.raises(bh.RefusedError, match='regular blob'):
        records(repo, [])


def test_nonancestor_task_is_not_a_birth_source(repo):
    _write(repo, SPEC, spec())
    base = commit(repo, 'Register Spec')
    _git(repo, 'switch', '-qc', 'unmerged')
    _write(repo, TASK, native())
    commit(repo, 'Unmerged task')
    _git(repo, 'switch', '-q', 'main')
    assert births(records(repo, [])) == {}


def test_replace_object_cannot_change_a_birth(repo):
    _write(repo, SPEC, spec('| TK-001 | Actual original | ready | none | pending |\n'))
    original = commit(repo, 'Genuine creation')
    expected = births(records(repo, []))
    _write(repo, SPEC, spec('| TK-999 | Forged replacement | ready | none | pending |\n'))
    _git(repo, 'add', '-A')
    forged_tree = _git(repo, 'write-tree')
    forged = _git(repo, 'commit-tree', forged_tree, '-m', 'Unrelated forged root')
    _git(repo, 'replace', original, forged)
    assert births(records(repo, [])) == expected


def test_missing_source_object_refuses_without_fetch(repo):
    _write(repo, SPEC, spec('| TK-001 | Original | ready | none | pending |\n'))
    commit(repo, 'Original source')
    oid = _git(repo, 'rev-parse', 'HEAD:' + SPEC)
    (repo / '.git' / 'objects' / oid[:2] / oid[2:]).unlink()
    with pytest.raises(bh.RefusedError, match='unavailable'):
        records(repo, [])


@pytest.mark.parametrize('proof', ['Completed corrective test execution: recorded success before merge.',
                                 'Completed `pytest` successfully.'])
@pytest.mark.parametrize('form', ['field', 'bodyfield'])
def test_scaffold_with_canonical_recorded_proof_still_refuses(repo, proof, form):
    resolved_scaffold(repo, proof=proof, proof_form=form)
    with pytest.raises(bh.RefusedError, match='ambiguous|conflicting'):
        records(repo, [])


def test_literal_proof_example_does_not_claim_scaffold_execution(repo):
    expected = resolved_scaffold(repo, proof='Example completed test output.', proof_form='fence')
    assert births(records(repo, [])) == expected


def test_empty_proof_field_does_not_claim_scaffold_execution(repo):
    expected = resolved_scaffold(repo, proof='')
    assert births(records(repo, [])) == expected
