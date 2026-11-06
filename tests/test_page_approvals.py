"""Synthetic page approvals through the real Board transaction and committed readback."""
import json
from datetime import datetime, timezone

import pytest

from ams import pages
from ams.grill_board.answers import AnswerRefused, answer, render_hashes
from ams.grill_board.cards import load_cards
from test_pages import git, html, inventory, room

NOW = datetime(2026, 11, 7, 12, 0, tzinfo=timezone.utc)


def prepare(room, paths=('/',)):
    listed = inventory(room, paths)
    candidate = git(room, 'rev-parse', 'HEAD')
    built = {path: html('Synthetic ' + path) for path in paths}
    pages.generate(room, listed, built, candidate=candidate)
    return listed, built, candidate


def confirm(room, path='/'):
    card = next(c for c in load_cards(room / pages.CARDS)[0] if c.fields['Page'] == path and c.stale is None)
    card_sha, owner_sha = render_hashes(room / pages.CARDS, card)
    commit = answer(room / pages.CARDS, card, 'confirm', '', card_sha, owner_sha, now=NOW)
    return card, commit


def test_confirmation_refuses_a_changed_committed_index_without_writes(room):
    listed = inventory(room, ('/',))
    pages.generate(room, listed, {'/': html()}, candidate=git(room, 'rev-parse', 'HEAD'))
    card = load_cards(room / pages.CARDS)[0][0]
    card_sha, owner_sha = render_hashes(room / pages.CARDS, card)
    index = room / pages.INDEX
    value = json.loads(index.read_text())
    value['pages']['/']['hash'] = 'sha256:' + 'b' * 64
    index.write_text(json.dumps(value) + '\n')
    git(room, 'add', pages.INDEX)
    git(room, 'commit', '-qm', 'Synthetic index drift after render')
    before = git(room, 'rev-parse', 'HEAD')
    original = {p: (room / p).read_bytes() for p in (pages.INDEX, pages.APPROVALS, pages.CARDS + '/' + card.file)}
    with pytest.raises(AnswerRefused, match='current.*index|index.*hash'):
        answer(room / pages.CARDS, card, 'confirm', '', card_sha, owner_sha)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert all((room / p).read_bytes() == data for p, data in original.items())


def test_confirm_once_and_parse_all_original_approval_commits(room):
    from ams.page_approvals import read_approvals
    prepare(room, ('/', '/skills/grilling'))
    before = int(git(room, 'rev-list', '--count', 'HEAD'))
    first, first_commit = confirm(room)
    assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    assert set(git(room, 'diff-tree', '--no-commit-id', '--name-only', '-r', first_commit).splitlines()) == {
        pages.APPROVALS, pages.CARDS + '/' + first.file}
    second, second_commit = confirm(room, '/skills/grilling')
    (room / 'README.md').write_text('Synthetic unrelated later commit.\n')
    git(room, 'add', 'README.md')
    git(room, 'commit', '-qm', 'Synthetic unrelated change')
    assert read_approvals(room) == [
        {'path': '/skills/grilling', 'hash': second.fields['Content hash'], 'date': '2026-11-07', 'card': second.file, 'commit': second_commit},
        {'path': '/', 'hash': first.fields['Content hash'], 'date': '2026-11-07', 'card': first.file, 'commit': first_commit},
    ]
    assert len(read_approvals(room, first_commit)) == 1


def test_changed_main_is_draft_but_footer_only_change_retains_approval(room):
    listed, built, candidate = prepare(room)
    assert pages.page_status(room)['pages']['/']['state'] == 'draft'
    card, approved_commit = confirm(room)
    approved_bytes = (room / pages.APPROVALS).read_bytes()
    assert pages.page_status(room)['pages']['/']['approval']['commit'] == approved_commit
    assert not pages.generate(room, listed, {'/': built['/'].replace('<footer>abc', '<footer>new')}, candidate=candidate)['changed']
    assert pages.page_status(room)['pages']['/']['state'] == 'approved'
    pages.generate(room, listed, {'/': built['/'].replace('Synthetic /', 'Synthetic /!')}, candidate=candidate)
    assert pages.page_status(room)['pages']['/']['state'] == 'draft'
    assert pages.page_status(room, approved_commit)['pages']['/']['state'] == 'approved'
    assert (room / pages.APPROVALS).read_bytes() == approved_bytes
    assert (room / pages.CARDS / card.file).read_text().count('## Answer') == 1


def test_status_cli_reads_committed_records_and_explicit_old_revision(room, capsys):
    listed, built, candidate = prepare(room)
    _, approved = confirm(room)
    pages.generate(room, listed, {'/': html('Synthetic changed page')}, candidate=candidate)
    index = room / pages.INDEX
    value = json.loads(index.read_text())
    value['pages']['/']['hash'] = pages.content_hash(built['/'])
    index.write_text(json.dumps(value))
    (room / pages.APPROVALS).write_text('Synthetic dirty approval text must be ignored.\n')
    pages.main(['status', '--project', str(room)])
    assert json.loads(capsys.readouterr().out)['pages']['/']['state'] == 'draft'
    pages.main(['status', '--project', str(room), '--ref', approved])
    result = json.loads(capsys.readouterr().out)
    assert result['commit'] == approved and result['pages']['/']['state'] == 'approved'


@pytest.mark.parametrize('change', ['missing-route', 'different-card', 'dirty-index', 'symlink-index'])
def test_confirm_refuses_other_index_identity_and_safety_changes(room, tmp_path, change):
    prepare(room)
    card = load_cards(room / pages.CARDS)[0][0]
    sha, owner = render_hashes(room / pages.CARDS, card)
    index = room / pages.INDEX
    value = json.loads(index.read_text())
    if change == 'missing-route':
        value['pages'].pop('/')
    elif change == 'different-card':
        value['pages']['/']['card'] = 'page-synthetic-other.md'
    elif change == 'dirty-index':
        value['synthetic_uncommitted'] = True
    else:
        outside = tmp_path / 'synthetic-external.json'
        outside.write_bytes(index.read_bytes())
        index.unlink()
        index.symlink_to(outside)
    if change != 'symlink-index':
        index.write_text(json.dumps(value))
    if change in ('missing-route', 'different-card'):
        git(room, 'add', pages.INDEX)
        git(room, 'commit', '-qm', 'Synthetic committed index identity change')
    before = git(room, 'rev-parse', 'HEAD')
    originals = [(room / p).read_bytes() for p in (pages.CARDS + '/' + card.file, pages.APPROVALS)]
    with pytest.raises(AnswerRefused, match='index'):
        answer(room / pages.CARDS, card, 'confirm', '', sha, owner)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert [(room / p).read_bytes() for p in (pages.CARDS + '/' + card.file, pages.APPROVALS)] == originals


def test_reader_ignores_quoted_fenced_and_other_section_examples(room):
    from ams.page_approvals import read_approvals
    prepare(room)
    _, approved = confirm(room)
    record = room / pages.APPROVALS
    text = record.read_text()
    line = next(line for line in text.splitlines() if line.startswith('**Owner answer'))
    record.write_text(text + '\n> ' + line + '\n\n```markdown\n' + line + '\n```\n\n## Examples\n\n' + line + '\n')
    git(room, 'add', pages.APPROVALS)
    git(room, 'commit', '-qm', 'Synthetic documentation examples')
    entries = read_approvals(room)
    assert len(entries) == 1 and entries[0]['commit'] == approved


def test_reader_preserves_unicode_and_accepts_committed_crlf_records(room):
    from ams.page_approvals import read_approvals
    listed = inventory(room, ('/',))
    listed['pages'][0]['title'] = 'Synthetic café (reader)'
    pages.generate(room, listed, {'/': html()}, candidate=git(room, 'rev-parse', 'HEAD'))
    card, approved = confirm(room)
    record = room / pages.APPROVALS
    record.write_bytes(record.read_bytes().replace(b'\n', b'\r\n'))
    git(room, 'add', pages.APPROVALS)
    git(room, 'commit', '-qm', 'Synthetic CRLF record')
    entry = read_approvals(room)[0]
    assert entry['card'] == card.file and entry['commit'] == approved
    assert pages.page_status(room)['pages']['/']['state'] == 'approved'


@pytest.mark.parametrize('field', ['path', 'hash', 'date', 'card'])
def test_substantive_approval_identity_edits_keep_their_actual_committing_sha(room, field):
    from ams.page_approvals import read_approvals
    prepare(room)
    card, _ = confirm(room)
    old, new = {
        'path': ('Approve page / (', 'Approve page /synthetic-other ('),
        'hash': (card.fields['Content hash'], 'sha256:' + 'a' * 64),
        'date': ('2026-11-07', '2026-11-08'),
        'card': (card.file, 'page-synthetic-other.md'),
    }[field]
    record = room / pages.APPROVALS
    record.write_text(record.read_text().replace(old, new))
    git(room, 'add', pages.APPROVALS)
    git(room, 'commit', '-qm', 'Synthetic substantive approval correction')
    assert read_approvals(room)[0]['commit'] == git(room, 'rev-parse', 'HEAD')


def test_guard_uses_the_committed_recommendation_and_card_identity(room):
    prepare(room)
    card = load_cards(room / pages.CARDS)[0][0]
    sha, owner = render_hashes(room / pages.CARDS, card)
    card.fields['Recommendation'] = 'Synthetic altered in-memory recommendation'
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(AnswerRefused, match='committed bytes'):
        answer(room / pages.CARDS, card, 'confirm', '', sha, owner)
    assert git(room, 'rev-parse', 'HEAD') == before


@pytest.mark.parametrize('defect', ['invalid-date', 'invalid-hash', 'duplicate-anchor'])
def test_malformed_committed_approval_records_refuse_status(room, defect):
    prepare(room)
    confirm(room)
    record = room / pages.APPROVALS
    text = record.read_text()
    if defect == 'invalid-date':
        text = text.replace('2026-11-07', '2026-02-31')
    elif defect == 'invalid-hash':
        text = text.replace('sha256:', 'invalid-hash:')
    else:
        text += '\n## Approvals\n'
    record.write_text(text)
    git(room, 'add', pages.APPROVALS)
    git(room, 'commit', '-qm', 'Synthetic invalid approval record')
    with pytest.raises(AnswerRefused, match='approval|Approvals'):
        pages.page_status(room)
