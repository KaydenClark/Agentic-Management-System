"""Replay one synthetic, actually drafted/reviewed occurrence, not a new review."""
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import uuid

import pytest

from ams import pages
from ams.grill_board.answers import rate
from ams.grill_board.cards import load_cards
from ams.page_feedback import read_voice
from test_page_feedback import assert_original_private, feedback_request, submit_feedback
from test_pages import git, inventory, room  # noqa: F401

FIXTURE = Path(__file__).with_name('fixtures') / 'page-feedback-consumption'


def recorded():
    return (json.loads((FIXTURE / 'case.json').read_text()),
            (FIXTURE / 'before.html').read_text(),
            (FIXTURE / 'draft.html').read_text(),
            (FIXTURE / 'draft.md').read_text(),
            json.loads((FIXTURE / 'review.json').read_text()))


def check_recorded_occurrence(case, draft, note, review):
    """Integrity and the declared criterion for this one retained example only.

    The independent judgment is recorded evidence, not supplied by this check.
    This is not a general validator of arbitrary agent drafting or feedback.
    """
    if not draft or not note or not review:
        raise ValueError('stored rating has no downstream draft and review')
    reference = f"{case['voice_record']} version {case['voice_version']}"
    if f'**Voice record:** {reference}\n' not in note or review.get('voice_record') != reference:
        raise ValueError('draft and review must cite the applicable voice version')
    if '**Disposition:** applied\n' not in note:
        raise ValueError('this recorded application is missing its disposition')
    text = draft.casefold()
    if (case['forbidden_phrase'] in text
            or any(phrase not in text for phrase in case['required_phrases'])):
        raise ValueError('draft fails the recorded evidence-strength criterion')
    digest = pages.content_hash(draft)
    if (review.get('draft_hash') != digest
            or review.get('draft_file_sha256') != hashlib.sha256(draft.encode()).hexdigest()
            or f'**Draft hash:** {digest}\n' not in note):
        raise ValueError('changed draft has a stale review binding')
    if review.get('result') != 'pass' or not review.get('reviewers'):
        raise ValueError('actual independent review is pending or failed')
    return digest


def test_recorded_correction_reaches_next_draft_review_and_survives_exact_retry(room):
    case, before, draft, note, review = recorded()
    digest = check_recorded_occurrence(case, draft, note, review)
    assert pages.content_hash(before) == case['original_hash'] != digest
    (room / '.gitignore').write_text('.local/\n')
    git(room, 'add', '.gitignore'); git(room, 'commit', '-qm', 'Synthetic private-store prerequisite')
    listed = inventory(room, ('/',))
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': before}, candidate=candidate)
    card = load_cards(room / pages.CARDS)[0][0]
    original = ('Synthetic private canary ' + uuid.uuid4().hex
                + '\r\nA local success does not support a universal reliability promise. '
                  'Place the limitation beside the observed result. \t')
    request = replace(feedback_request(room, card, 'rate', '1', original), event_id=case['event_id'])
    feedback_commit = rate(room / pages.CARDS, card, '1', original, request.card_sha,
                           now=datetime(2026, 11, 6, tzinfo=timezone.utc),
                           event_id=request.event_id, voice_sha=request.voice_sha)
    voice = read_voice(room)
    assert voice.version == case['voice_version'] == 1
    assert voice.sha == case['voice_blob_sha256']
    packet = room / '.local/page-feedback' / (request.event_id + '.json')
    assert stat.S_IMODE(packet.stat().st_mode) == 0o600
    assert stat.S_IMODE(packet.parent.stat().st_mode) == 0o700
    captured_request = json.loads(packet.read_text())['request']
    # The safe application supplements the original pending entry, never replaces it.
    supplement = (f'\n### Application for feedback version {voice.version}\n\n'
                  f'**Event:** {request.event_id}\n**Interpretation:** {case["interpretation"]}\n'
                  f'**Disposition:** applied in demonstration/draft.html\n'
                  f'**Draft hash:** {digest}\n**Review:** demonstration/review.json\n')
    (room / voice.path).write_bytes(voice.blob + supplement.encode())
    (room / 'demonstration').mkdir()
    for name, value in [('draft.html', draft), ('draft.md', note),
                        ('review.json', json.dumps(review, indent=2) + '\n')]:
        (room / 'demonstration' / name).write_text(value)
    git(room, 'add', voice.path, 'demonstration')
    git(room, 'commit', '-qm', 'Synthetic replay of recorded draft and independent review')
    assert (room / voice.path).read_bytes().startswith(voice.blob)
    next_candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': draft}, candidate=next_candidate)
    cards, refused = load_cards(room / pages.CARDS)
    assert not refused and len(cards) == 2
    assert next(c for c in cards if c.file == card.file).stale is not None
    current = next(c for c in cards if c.waiting)
    assert current.fields['Content hash'] == digest
    assert current.fields['Voice record'] == f'{voice.path} version 1'
    head = git(room, 'rev-parse', 'HEAD')
    for _ in range(2):
        assert submit_feedback(room, card, request) == feedback_commit
        assert git(room, 'rev-parse', 'HEAD') == head
        assert read_voice(room).version == 1
        assert json.loads(packet.read_text())['request'] == captured_request
    assert_original_private(room, request)
    assert not git(room, 'status', '--porcelain')


@pytest.mark.parametrize('adverse', ['rating-only', 'missing-draft-version', 'missing-review-version',
                                    'wrong-version', 'missing-disposition', 'unchanged-defect',
                                    'changed-after-review', 'pending-review'])
def test_recorded_consumption_rejects_planted_gaps(adverse):
    case, before, draft, note, review = recorded()
    if adverse == 'rating-only':
        draft = note = ''; review = None
    elif adverse == 'missing-draft-version':
        note = note.replace('**Voice record:**', '**Unrelated record:**')
    elif adverse == 'missing-review-version':
        review.pop('voice_record')
    elif adverse == 'wrong-version':
        review['voice_record'] = f'{case["voice_record"]} version 2'
    elif adverse == 'missing-disposition':
        note = note.replace('**Disposition:** applied', '**Disposition:** pending')
    elif adverse == 'unchanged-defect':
        draft = before
    elif adverse == 'changed-after-review':
        draft = draft.replace('A local check passed.', 'A different local check passed.')
    else:
        review['result'] = 'pending'
    reason = {'rating-only': 'stored rating', 'missing-draft-version': 'cite',
              'missing-review-version': 'cite', 'wrong-version': 'cite',
              'missing-disposition': 'disposition', 'unchanged-defect': 'criterion',
              'changed-after-review': 'stale review', 'pending-review': 'pending or failed'}[adverse]
    with pytest.raises(ValueError, match=reason):
        check_recorded_occurrence(case, draft, note, review)
