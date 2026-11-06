"""Synthetic private page-feedback originals and safe public version references."""
import json
import re
import stat
import subprocess
import threading
import urllib.parse
import urllib.request
import uuid

import pytest

from ams import pages
from ams.grill_board.answers import answer, render_hashes
from ams.grill_board.cards import load_cards
from ams.grill_board.server import make_server
from test_pages import git, html, inventory, room
from test_grill_board_answers import post

VOICE = 'grill-board/voice-and-taste.md'


def prepare_feedback(room):
    (room / '.gitignore').write_text('.local/\n')
    git(room, 'add', '.gitignore')
    git(room, 'commit', '-qm', 'Synthetic private-store ignore rule')
    listed = inventory(room, ('/',))
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': html()}, candidate=candidate)
    return load_cards(room / pages.CARDS)[0][0]


def test_page_return_preserves_exact_private_original_and_only_safe_public_references(room):
    from ams.page_feedback import read_voice
    card = prepare_feedback(room)
    event_id = uuid.uuid4().hex
    token = 'Synthetic-private-' + uuid.uuid4().hex
    note = '\n ' + token + '\r\nKeep Unicode café and trailing space. \t'
    server = make_server(room / pages.CARDS, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        origin = f'http://127.0.0.1:{server.server_address[1]}'
        query = urllib.parse.urlencode({'topic': 'Website pages', 'card': card.file})
        with urllib.request.urlopen(origin + '/?' + query) as response:
            body = response.read().decode()
        form = body.split('<form class="answer"', 1)[1].split('</form>', 1)[0]
        fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', form))
        before = int(git(room, 'rev-list', '--count', 'HEAD'))
        status, body = post(server, {**fields, 'verdict': 'change', 'note': note,
                                   'event_id': event_id, 'voice_sha': read_voice(room).sha})
        assert status == 200 and 'Written and committed' in body
        assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    finally:
        server.shutdown()
        server.server_close()
    packet_file = room / '.local/page-feedback' / (event_id + '.json')
    packet = json.loads(packet_file.read_text())
    assert packet['request']['note'] == note
    assert stat.S_IMODE(packet_file.stat().st_mode) == 0o600
    assert stat.S_IMODE(packet_file.parent.stat().st_mode) == 0o700
    assert read_voice(room).version == 1
    voice = (room / VOICE).read_text()
    assert event_id in voice and '**Disposition:** pending' in voice
    objects = subprocess.check_output(['git', 'cat-file', '--batch-all-objects', '--batch'], cwd=room)
    assert token.encode() not in objects and note.encode() not in objects


def test_generated_open_pages_name_the_safe_voice_record_version(room):
    listed = inventory(room)
    built = {row['path']: html(row['title']) for row in listed['pages']}
    candidate = git(room, 'rev-parse', 'HEAD')
    result = pages.generate(room, listed, built, candidate=candidate)
    cards, refused = load_cards(room / pages.CARDS)
    assert not refused and len(cards) == 2
    assert all(card.fields.get('Voice record') == VOICE + ' version 0' for card in cards)
    assert '**Version:** 0' in (room / VOICE).read_text()
    assert '## Entries' in (room / VOICE).read_text()
    again = pages.generate(room, listed, built, candidate=candidate)
    assert not again['changed'] and again['commit'] == result['commit']


def test_legacy_open_card_gets_one_appended_reference_and_answered_bytes_stay(room):
    listed = inventory(room)
    candidate = git(room, 'rev-parse', 'HEAD')
    built = {row['path']: html(row['title']) for row in listed['pages']}
    entries = {}
    for number, row in enumerate(listed['pages']):
        digest = pages.content_hash(built[row['path']])
        name = f'legacy-synthetic-{number}.md'
        text = pages._new_card(row, digest, candidate)
        text = '\n'.join(line for line in text.splitlines() if not line.startswith('**Voice record:**')) + '\n'
        (room / pages.CARDS / name).write_text(text)
        entries[row['path']] = {'title': row['title'], 'landed': row['landed']['commit'],
                                'provenance_kind': 'historical-landing', 'hash': digest, 'card': name}
    (room / pages.INDEX).parent.mkdir()
    (room / pages.INDEX).write_text(json.dumps({'candidate': candidate, 'pages': entries, 'protection': None}))
    (room / pages.APPROVALS).write_text('# Synthetic approvals\n\n## Approvals\n')
    git(room, 'add', 'grill-board')
    git(room, 'commit', '-qm', 'Synthetic pre-voice legacy cards')
    cards, _ = load_cards(room / pages.CARDS)
    answered = next(card for card in cards if card.fields['Page'] == '/')
    card_sha, owner_sha = render_hashes(room / pages.CARDS, answered)
    answer(room / pages.CARDS, answered, 'confirm', '', card_sha, owner_sha)
    originals = {card.file: (room / pages.CARDS / card.file).read_bytes() for card in cards}
    result = pages.generate(room, listed, built, candidate=candidate)
    assert result['changed']
    current, refused = load_cards(room / pages.CARDS)
    assert not refused
    for card in current:
        data = (room / pages.CARDS / card.file).read_bytes()
        if card.file == answered.file:
            assert data == originals[card.file] and card.voice_record is None
        else:
            assert data.startswith(originals[card.file])
            assert data.count(b'## Voice record') == 1
            assert card.voice_record == {'Record': VOICE, 'Version': '0'}
    assert not pages.generate(room, listed, built, candidate=candidate)['changed']


@pytest.mark.parametrize('defect', ['duplicate-counter', 'invalid-counter', 'deleted-record'])
def test_invalid_or_removed_voice_record_refuses_without_replacing_history(room, defect):
    listed = inventory(room, ('/',))
    candidate = git(room, 'rev-parse', 'HEAD')
    built = {'/': html()}
    pages.generate(room, listed, built, candidate=candidate)
    voice = room / VOICE
    if defect == 'deleted-record':
        git(room, 'rm', VOICE)
    else:
        text = voice.read_text()
        if defect == 'duplicate-counter':
            text = text.replace('**Version:** 0', '**Version:** 0\n**Version:** invalid')
        else:
            text = text.replace('**Version:** 0', '**Version:** invalid')
        voice.write_text(text)
        git(room, 'add', VOICE)
    git(room, 'commit', '-qm', 'Synthetic invalid voice state')
    before = git(room, 'rev-parse', 'HEAD')
    cards = {p.name: p.read_bytes() for p in (room / pages.CARDS).glob('*.md')}
    with pytest.raises(pages.PageRefused, match='voice record'):
        pages.generate(room, listed, {'/': html('Synthetic changed page')}, candidate=candidate)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert {p.name: p.read_bytes() for p in (room / pages.CARDS).glob('*.md')} == cards


def current_card(room, name=None):
    cards, refused = load_cards(room / pages.CARDS)
    assert not refused
    return next(c for c in cards if name is None or c.file == name)


def feedback_request(room, card, kind='answer', value='change', note='Synthetic private correction.'):
    from ams.page_feedback import PageRequest, read_voice
    card_sha, owner_sha = render_hashes(room / pages.CARDS, card)
    return PageRequest(kind, card.file, value, note, card_sha,
                       owner_sha if kind == 'answer' else '', read_voice(room).sha, uuid.uuid4().hex)


def submit_feedback(room, card, request):
    from ams.grill_board import answers
    extra = {'event_id': request.event_id, 'voice_sha': request.voice_sha}
    if request.kind == 'answer':
        return answers.answer(room / pages.CARDS, card, request.value, request.note,
                              request.card_sha, request.record_sha, **extra)
    if request.kind == 'rate':
        return answers.rate(room / pages.CARDS, card, request.value, request.note, request.card_sha, **extra)
    return answers.flag(room / pages.CARDS, card, request.note, request.card_sha, **extra)


def assert_original_private(room, request):
    path = room / '.local/page-feedback' / (request.event_id + '.json')
    assert json.loads(path.read_text())['request']['note'] == request.note
    objects = subprocess.check_output(['git', 'cat-file', '--batch-all-objects', '--batch'], cwd=room)
    if request.note:
        assert request.note.encode() not in objects
    assert not git(room, 'ls-files', '--', '.local/')


@pytest.mark.parametrize('kind,value', [('answer', 'change'), ('answer', 'rework-wording'), ('answer', 'change-the-why'), ('rate', '2'), ('flag', '')])
def test_each_page_feedback_kind_is_one_safe_event_with_exact_original(room, kind, value):
    from dataclasses import replace
    from ams.page_feedback import read_voice
    from ams.grill_board.answers import AnswerRefused
    card = prepare_feedback(room)
    request = feedback_request(room, card, kind, value, '\n Synthetic-' + uuid.uuid4().hex + '\r\n café \t')
    before = int(git(room, 'rev-list', '--count', 'HEAD'))
    commit = submit_feedback(room, card, request)
    assert read_voice(room).version == 1
    assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    assert submit_feedback(room, current_card(room), request) == commit
    assert git(room, 'rev-parse', 'HEAD') == commit
    assert read_voice(room).version == 1
    with pytest.raises(AnswerRefused, match='different request'):
        submit_feedback(room, current_card(room), replace(request, note=request.note + ' changed'))
    assert_original_private(room, request)
    assert not git(room, 'status', '--porcelain')


def test_confirm_note_is_private_and_adds_no_voice_entry(room):
    from ams.page_feedback import read_voice
    from ams.page_approvals import read_approvals
    card = prepare_feedback(room)
    request = feedback_request(room, card, value='confirm', note='Synthetic-confirm-' + uuid.uuid4().hex)
    original = (room / VOICE).read_bytes()
    commit = submit_feedback(room, card, request)
    assert read_voice(room).version == 0 and (room / VOICE).read_bytes() == original
    assert len(read_approvals(room)) == 1
    assert submit_feedback(room, current_card(room), request) == commit
    assert_original_private(room, request)


def test_blank_ratings_and_flags_still_record_a_safe_version(room):
    from ams.page_feedback import read_voice
    card = prepare_feedback(room)
    for kind, value in [('rate', '3'), ('rate', '5'), ('flag', '')]:
        card = current_card(room)
        request = feedback_request(room, card, kind, value, '')
        submit_feedback(room, card, request)
        assert_original_private(room, request)
    assert read_voice(room).version == 3
    assert (room / VOICE).read_text().count('**Interpretation:** pending') == 3


@pytest.mark.parametrize('change', ['committed-voice', 'dirty-voice', 'dirty-card', 'staged-card'])
def test_changed_rendered_inputs_refuse_without_private_capture_or_git_write(room, change):
    from ams.grill_board.answers import AnswerRefused
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    path = room / (VOICE if 'voice' in change else pages.CARDS + '/' + card.file)
    path.write_bytes(path.read_bytes() + b'\nSynthetic concurrent work.\n')
    if change in ('committed-voice', 'staged-card'):
        git(room, 'add', str(path))
    if change == 'committed-voice':
        git(room, 'commit', '-qm', 'Synthetic concurrent voice edit')
    before = git(room, 'rev-parse', 'HEAD'), path.read_bytes(), git(room, 'diff', '--cached')
    with pytest.raises(AnswerRefused):
        submit_feedback(room, card, request)
    assert (git(room, 'rev-parse', 'HEAD'), path.read_bytes(), git(room, 'diff', '--cached')) == before
    assert not (room / '.local/page-feedback' / (request.event_id + '.json')).exists()


@pytest.mark.parametrize('cut', ['captured', 'planned', 'first-public-write', 'prepared', 'after-cas', 'index-refresh', 'committed'])
def test_interrupted_page_feedback_retries_original_event_once(room, monkeypatch, cut):
    from ams import page_feedback
    from ams.grill_board import answers
    card = prepare_feedback(room)
    request = feedback_request(room, card, note='Synthetic-crash-' + uuid.uuid4().hex)
    before = int(git(room, 'rev-list', '--count', 'HEAD'))
    original_write = page_feedback._Store.write
    original_replace = answers._replace
    original_git = answers._git
    calls = 0
    with monkeypatch.context() as patch:
        def write(store, packet, **kwargs):
            original_write(store, packet, **kwargs)
            if packet['state'] == cut:
                raise KeyboardInterrupt('synthetic interruption')
        def replace(path, data):
            nonlocal calls
            original_replace(path, data)
            calls += 1
            if cut == 'first-public-write' and calls == 1:
                raise KeyboardInterrupt('synthetic interruption')
        def interrupted_git(root, *args, **kwargs):
            if cut == 'index-refresh' and args[0] == 'update-index' and '--cacheinfo' not in args:
                raise KeyboardInterrupt('synthetic interruption')
            result = original_git(root, *args, **kwargs)
            if cut == 'after-cas' and args[0] == 'update-ref':
                raise KeyboardInterrupt('synthetic interruption')
            return result
        patch.setattr(page_feedback._Store, 'write', write)
        patch.setattr(answers, '_replace', replace)
        patch.setattr(answers, '_git', interrupted_git)
        with pytest.raises(KeyboardInterrupt):
            submit_feedback(room, card, request)
    assert_original_private(room, request)
    packet = json.loads((room / '.local/page-feedback' / (request.event_id + '.json')).read_text())
    prior_candidate = packet['candidate']
    commit = submit_feedback(room, current_card(room), request)
    assert git(room, 'rev-parse', 'HEAD') == commit
    if cut in ('after-cas', 'index-refresh', 'committed'):
        assert commit == prior_candidate
    assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    assert page_feedback.read_voice(room).version == 1
    assert (room / VOICE).read_text().count('**Event:** ' + request.event_id) == 1
    assert not git(room, 'status', '--porcelain')
    assert_original_private(room, request)


def test_receipt_replay_survives_later_card_deletion_and_never_undoes_other_work(room):
    from dataclasses import asdict
    from ams.page_feedback import replay_page_submission
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    commit = submit_feedback(room, card, request)
    git(room, 'rm', pages.CARDS + '/' + card.file)
    git(room, 'commit', '-qm', 'Synthetic later card deletion')
    later = git(room, 'rev-parse', 'HEAD')
    form = asdict(request)
    form['verdict'] = form.pop('value')
    assert replay_page_submission(room / pages.CARDS, form, '/answer') == commit
    assert git(room, 'rev-parse', 'HEAD') == later
    assert not (room / pages.CARDS / card.file).exists()


@pytest.mark.parametrize('unsafe', ['symlink-store', 'public-mode', 'symlink-local', 'tracked-private'])
def test_unsafe_private_storage_refuses_before_public_write(room, tmp_path, unsafe):
    from ams.grill_board.answers import AnswerRefused
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    local = room / '.local'
    outside = tmp_path / 'outside'
    outside.mkdir(mode=0o700)
    if unsafe == 'symlink-local':
        local.symlink_to(outside, target_is_directory=True)
    else:
        local.mkdir(mode=0o700)
        private = local / 'page-feedback'
        if unsafe == 'symlink-store':
            private.symlink_to(outside, target_is_directory=True)
        else:
            private.mkdir(mode=0o755 if unsafe == 'public-mode' else 0o700)
        if unsafe == 'tracked-private':
            (private / 'unsafe.txt').write_text('Synthetic tracked unrelated data.\n')
            git(room, 'add', '-f', '.local/page-feedback/unsafe.txt')
            git(room, 'commit', '-qm', 'Synthetic unsafe tracked store')
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(AnswerRefused):
        submit_feedback(room, card, request)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not list(outside.iterdir())


def test_interrupted_pending_event_preserves_unrelated_work_for_agent_recovery(room, monkeypatch):
    from ams import page_feedback
    from ams.grill_board import answers
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    original_replace = answers._replace
    with monkeypatch.context() as patch:
        def interrupted(path, data):
            original_replace(path, data)
            raise KeyboardInterrupt('synthetic interruption after first public write')
        patch.setattr(answers, '_replace', interrupted)
        with pytest.raises(KeyboardInterrupt):
            submit_feedback(room, card, request)
    voice = room / VOICE
    voice.write_bytes(voice.read_bytes() + b'\nSynthetic unrelated work; preserve it.\n')
    before = git(room, 'rev-parse', 'HEAD'), voice.read_bytes()
    with pytest.raises(answers.AnswerRefused, match='Unrelated'):
        submit_feedback(room, current_card(room), request)
    assert (git(room, 'rev-parse', 'HEAD'), voice.read_bytes()) == before
    assert_original_private(room, request)


@pytest.mark.parametrize('damage', ['hardlink', 'bad-request', 'bad-context', 'bad-plan'])
def test_private_receipt_damage_never_rebinds_or_duplicates_public_event(room, tmp_path, damage):
    from ams.page_feedback import FeedbackOutcomeUnknown
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    commit = submit_feedback(room, card, request)
    private = room / '.local/page-feedback' / (request.event_id + '.json')
    if damage == 'hardlink':
        (tmp_path / 'synthetic-second-link').hardlink_to(private)
    else:
        packet = json.loads(private.read_text())
        if damage == 'bad-request':
            packet['request'] = []
        elif damage == 'bad-context':
            packet['context'] = None
        else:
            packet['plan']['base'] = []
        private.write_text(json.dumps(packet))
    with pytest.raises(FeedbackOutcomeUnknown, match='recover|verif'):
        submit_feedback(room, current_card(room), request)
    assert git(room, 'rev-parse', 'HEAD') == commit
    assert (room / VOICE).read_text().count('**Event:** ' + request.event_id) == 1


def test_public_commit_with_lost_private_receipt_refuses_duplicate(room):
    from ams.page_feedback import FeedbackOutcomeUnknown
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    commit = submit_feedback(room, card, request)
    (room / '.local/page-feedback' / (request.event_id + '.json')).unlink()
    with pytest.raises(FeedbackOutcomeUnknown, match='without its verified private receipt'):
        submit_feedback(room, current_card(room), request)
    assert git(room, 'rev-parse', 'HEAD') == commit


def test_same_event_concurrent_calls_commit_once_under_shared_repository_lock(room):
    from concurrent.futures import ThreadPoolExecutor
    from ams.page_feedback import read_voice
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    before = int(git(room, 'rev-list', '--count', 'HEAD'))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: submit_feedback(room, card, request), range(2)))
    assert results[0] == results[1] == git(room, 'rev-parse', 'HEAD')
    assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    assert read_voice(room).version == 1
    assert_original_private(room, request)


def test_error_after_successful_branch_cas_recovers_known_commit_immediately(room, monkeypatch):
    from ams.grill_board import answers
    from ams.page_feedback import read_voice
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    original_git = answers._git
    before = int(git(room, 'rev-list', '--count', 'HEAD'))
    with monkeypatch.context() as patch:
        def lost_ack(root, *args, **kwargs):
            result = original_git(root, *args, **kwargs)
            if args[0] == 'update-ref':
                raise OSError('synthetic CAS acknowledgment loss')
            return result
        patch.setattr(answers, '_git', lost_ack)
        commit = submit_feedback(room, card, request)
    assert commit == git(room, 'rev-parse', 'HEAD')
    assert int(git(room, 'rev-list', '--count', 'HEAD')) == before + 1
    assert read_voice(room).version == 1 and not git(room, 'status', '--porcelain')
    assert_original_private(room, request)
