"""Local content-bound approval guards and readback from committed Git only."""
import json
import re
from datetime import date
from pathlib import Path

from .grill_board.answers import AnswerRefused, _git, _text, _unchanged, committed_blob, sha256
from .grill_board.cards import Card, parse_card

INDEX = 'grill-board/pages/index.json'
APPROVALS = 'grill-board/page-approvals.md'
ROUTE = re.compile(r'/(?:[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*)?')
HASH = re.compile(r'sha256:[0-9a-f]{64}')
CARD_NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]*\.md')
APPROVAL_LINE = re.compile(
    r'^\*\*Owner answer \((?P<date>\d{4}-\d{2}-\d{2}), Grill Board card `(?P<card>[^`]+)`\):\*\* '
    r'Confirmed: Approve page (?P<path>/[^ ]*) \(.+\) at content hash (?P<hash>sha256:[0-9a-f]{64})\.$')


def committed_ref(root, rev='HEAD'):
    return _git(root, 'rev-parse', '--verify', '--end-of-options', f'{rev}^{{commit}}').strip()


def read_page_index(root, rev='HEAD'):
    blob = committed_blob(root, INDEX, rev)
    try:
        index = json.loads(blob) if blob is not None else None
    except (ValueError, UnicodeDecodeError):
        raise AnswerRefused('the current page index is not readable JSON') from None
    if (not isinstance(index, dict) or not isinstance(index.get('pages'), dict)
            or not isinstance(index.get('candidate'), str)
            or not re.fullmatch(r'[0-9a-f]{40,64}', index['candidate'])):
        raise AnswerRefused('the current page index is missing or invalid')
    for path, row in index['pages'].items():
        if (not ROUTE.fullmatch(path) or not isinstance(row, dict)
                or not isinstance(row.get('hash'), str) or not HASH.fullmatch(row['hash'])
                or not isinstance(row.get('card'), str) or not CARD_NAME.fullmatch(row['card'])):
            raise AnswerRefused('the current page index contains an invalid page identity')
    return index


def validate_page_confirmation(root, base, card, card_blob):
    """Recheck the committed card and index under the caller's Board lock."""
    actual = parse_card(card.file, _text(card_blob, card.file))
    if not isinstance(actual, Card):
        raise AnswerRefused('the committed card is invalid')
    is_page = any(c.fields.get('Page') or c.fields.get('Owner record') == APPROVALS for c in (card, actual))
    if not is_page:
        return
    fields = ('Page', 'Content hash', 'Title', 'Owner record', 'Write after', 'Recommendation')
    if any(card.fields.get(key) != actual.fields.get(key) for key in fields):
        raise AnswerRefused('the page card identity differs from its committed bytes')
    path, digest = actual.fields.get('Page', ''), actual.fields.get('Content hash', '')
    if (actual.stale is not None or not ROUTE.fullmatch(path) or not HASH.fullmatch(digest)
            or actual.fields.get('Owner record') != APPROVALS
            or actual.fields.get('Write after') != '## Approvals'
            or actual.fields.get('Recommendation') != f"Approve page {path} ({actual.fields.get('Title', '')}) at content hash {digest}."):
        raise AnswerRefused('the page card has no valid current approval identity')
    current = read_page_index(root, base)['pages'].get(path)
    if current is None or current['hash'] != digest or current['card'] != card.file:
        raise AnswerRefused('the page card differs from its current page index entry or hash')
    index_file = Path(root)
    for part in INDEX.split('/'):
        index_file /= part
        if index_file.is_symlink():
            raise AnswerRefused('the current page index crosses a symlink')
    blob = committed_blob(root, INDEX, base)
    _unchanged(root, base, INDEX, index_file, sha256(blob), 'current page index')


def read_approvals(root, rev='HEAD'):
    """Every generated approval line with its original committing identity.

    Blame follows retained lines across later insertions. The selected revision
    bounds the read: working-tree notes and approvals never enter the result.
    """
    commit = committed_ref(root, rev)
    blob = committed_blob(root, APPROVALS, commit)
    if blob is None:
        return []
    lines = _text(blob, APPROVALS).split('\n')
    if sum(line.removesuffix('\r') == '## Approvals' for line in lines) != 1:
        raise AnswerRefused('the committed approval record needs one unique Approvals section')
    blamed = []
    origin = None
    for line in _git(root, 'blame', '--line-porcelain', '--root', commit, '--', APPROVALS).split('\n'):
        if re.fullmatch(r'[0-9a-f]{40,64} \d+ \d+(?: \d+)?', line):
            origin = line.split(' ', 1)[0]
        elif line.startswith('\t'):
            if origin is None:
                raise AnswerRefused('the approval line commit identity is unavailable')
            blamed.append((line[1:], origin))
    # Git's text-mode subprocess output normalizes CRLF. Compare line content
    # with the same normalization; never rewrite the committed record bytes.
    expected_lines = lines[:-1] if lines[-1] == '' else lines
    if [text.removesuffix('\r') for text, _ in blamed] != [line.removesuffix('\r') for line in expected_lines]:
        raise AnswerRefused('the approval line identities differ from the committed record')
    entries, inside, fence = [], False, None
    for line, origin in blamed:
        line = line.removesuffix('\r')
        opening = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', line):
                fence = None
            continue
        if opening:
            marker = opening[1]
            fence = (marker[0], len(marker))
            continue
        if line == '## Approvals':
            inside = True
            continue
        if line.startswith('## '):
            inside = False
        match = APPROVAL_LINE.fullmatch(line) if inside else None
        if not match:
            if inside and line.startswith('**Owner answer ('):
                raise AnswerRefused('the committed approval line is malformed')
            continue
        entry = match.groupdict()
        try:
            date.fromisoformat(entry['date'])
        except ValueError:
            raise AnswerRefused('the committed approval date is invalid') from None
        if not ROUTE.fullmatch(entry['path']) or not CARD_NAME.fullmatch(entry['card']):
            raise AnswerRefused('the committed approval identity is invalid')
        entries.append({**entry, 'commit': origin})
    return entries


def page_status(root, rev='HEAD'):
    commit = committed_ref(root, rev)
    index, approvals = read_page_index(root, commit), read_approvals(root, commit)
    states = {}
    for path, row in sorted(index['pages'].items()):
        approval = next((a for a in approvals if a['path'] == path and a['hash'] == row['hash']), None)
        states[path] = {'hash': row['hash'], 'state': 'approved' if approval else 'draft', 'approval': approval}
    return {'commit': commit, 'candidate': index['candidate'], 'pages': states}
