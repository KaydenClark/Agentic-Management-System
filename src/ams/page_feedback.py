"""Private page-feedback capture and safe committed voice references.

Original owner words never belong in the public voice record. Version zero
names an empty record and asserts no feedback or owner judgment.
"""
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import stat
import uuid

from .grill_board import answers as board
from .grill_board.answers import AnswerRefused, _git, _text, committed_entry, sha256
from .grill_board.cards import parse_card
from .grill_board.cards import CardSourceError
from .page_approvals import APPROVALS, CARDS, CARD_NAME, HASH, INDEX, ROUTE, validate_page_confirmation
from .project_paths import MANIFEST, feedback_paths, safe_voice_path

INITIAL_VOICE = (b'# Page feedback voice and taste\n\n**Version:** 0\n\n'
                 b'Original words stay private; entries contain only safe references and dispositions.\n\n'
                 b'## Entries\n')


@dataclass(frozen=True)
class VoiceRecord:
    version: int
    blob: bytes | None
    sha: str
    mode: str
    path: str


def read_voice(root, rev='HEAD'):
    relative = feedback_paths(root, rev).voice
    entry = committed_entry(root, relative, rev)
    if entry is None:
        if _git(root, 'ls-tree', '-z', rev, '--', relative):
            raise AnswerRefused('the voice record is not a committed regular file')
        if _git(root, 'log', '-1', '--format=%H', rev, '--', relative).strip():
            raise AnswerRefused('the voice record was removed; restore its committed history')
        return VoiceRecord(0, None, '', '100644', relative)
    mode, blob = entry
    lines = _text(blob, relative).splitlines()
    if lines.count('## Entries') != 1:
        raise AnswerRefused('the voice record needs one Entries section')
    header = lines[:lines.index('## Entries')]
    counters = [line for line in header if line.startswith('**Version:**')]
    match = re.fullmatch(r'\*\*Version:\*\* ([0-9]{1,18})', counters[0]) if len(counters) == 1 else None
    if match is None:
        raise AnswerRefused('the voice record needs one valid version counter')
    return VoiceRecord(int(match[1]), blob, sha256(blob), mode, relative)


def card_voice_version(card, voice_path):
    reference = card.fields.get('Voice record')
    if reference is not None:
        match = re.fullmatch(re.escape(voice_path) + r' version ([0-9]{1,18})', reference)
        if not match:
            raise AnswerRefused('the page card voice reference is invalid')
        return int(match[1])
    section = card.voice_record
    if section is None:
        return None
    version = section.get('Version', '')
    if section.get('Record') != voice_path or not re.fullmatch(r'[0-9]{1,18}', version):
        raise AnswerRefused('the page card voice reference is invalid')
    return int(version)


class FeedbackOutcomeUnknown(Exception):
    """Keep the original request and reconcile its private/public outcome."""


@dataclass(frozen=True)
class PageRequest:
    kind: str
    card: str
    value: str
    note: str
    card_sha: str
    record_sha: str
    voice_sha: str
    event_id: str

    def validate(self):
        if not all(isinstance(value, str) for value in asdict(self).values()):
            raise AnswerRefused('To save page feedback privately, reload the current page context and keep a copy of your note.')
        valid_value = (self.kind == 'answer' and self.value in board.VERDICTS
                       or self.kind == 'rate' and self.value in board.RATINGS
                       or self.kind == 'flag' and self.value == '')
        if (not valid_value or not CARD_NAME.fullmatch(self.card)
                or not re.fullmatch(r'[0-9a-f]{32}', self.event_id)
                or not isinstance(self.note, str) or len(self.note) > 4000
                or not re.fullmatch(r'[0-9a-f]{64}', self.card_sha)
                or not re.fullmatch(r'(?:[0-9a-f]{64})?', self.record_sha)
                or not re.fullmatch(r'(?:[0-9a-f]{64})?', self.voice_sha)):
            raise AnswerRefused('To save page feedback privately, reload the current page context and keep a copy of your note.')


def is_page_card(cards_dir, card):
    if card.fields.get('Page') or card.fields.get('Owner record') == APPROVALS:
        return True
    blob = board.committed_blob(board.repo_root(cards_dir), INDEX)
    try:
        return any(row.get('card') == card.file for row in json.loads(blob or b'{}').get('pages', {}).values())
    except (ValueError, AttributeError, TypeError):
        return card.file.startswith('page-')


@contextmanager
def _private_store(root, *, create=False):
    """Bind IO to owned, nonlinked directory handles; no original enters Git."""
    relative = feedback_paths(root).private
    opened = []
    missing = False
    try:
        if _git(root, 'ls-files', '-z', '--', relative + '/'):
            raise AnswerRefused('Private feedback storage must stay outside tracked Git files.')
        try:
            _git(root, 'check-ignore', '--quiet', '--', relative + '/')
        except AnswerRefused:
            raise AnswerRefused('Private feedback storage must be Git-ignored.') from None
        parent = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        opened.append(parent)
        parts = relative.split('/')
        for number, name in enumerate(parts):
            private = number == len(parts) - 1
            try:
                fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            except FileNotFoundError:
                if not create:
                    missing = True
                    break
                os.mkdir(name, mode=0o700, dir_fd=parent)
                os.fsync(parent)
                fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            opened.append(fd)
            info = os.fstat(fd)
            permissions = stat.S_IMODE(info.st_mode)
            if info.st_uid != os.getuid() or permissions & 0o022 or (private and permissions != 0o700):
                raise AnswerRefused('Private feedback storage permissions need an agent repair; keep your note.')
            parent = fd
    except (AnswerRefused, OSError):
        raise FeedbackOutcomeUnknown('Private feedback storage needs agent repair. Keep your note and retry this exact action after recovery.') from None
    else:
        yield None if missing else _Store(parent)
    finally:
        for fd in reversed(opened):
            os.close(fd)


class _Store:
    def __init__(self, directory_fd):
        self.fd = directory_fd

    def read(self, event_id):
        try:
            fd = os.open(event_id + '.json', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
        except FileNotFoundError:
            return None
        try:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid()
                    or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 65536):
                raise FeedbackOutcomeUnknown('The private feedback record needs recovery; keep your note and original action.')
            with os.fdopen(fd, 'rb', closefd=False) as source:
                raw = source.read(65537)
            packet = json.loads(raw)
            if (not isinstance(packet, dict) or packet.get('schema') != 1
                    or not isinstance(packet.get('request'), dict)
                    or packet['request'].get('event_id') != event_id
                    or packet.get('state') not in {'captured', 'planned', 'prepared', 'committed'}):
                raise ValueError
            PageRequest(**packet['request']).validate()
            context = packet.get('context')
            if (not isinstance(context, dict)
                    or not isinstance(context.get('page'), str) or not ROUTE.fullmatch(context['page'])
                    or not isinstance(context.get('hash'), str) or not HASH.fullmatch(context['hash'])
                    or not isinstance(context.get('when'), str)
                    or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', context['when'])
                    or not safe_voice_path(context.get('voice'))
                    or context.get('kind') not in {*board.VERDICTS, 'rate', 'flag'}
                    or context.get('version') is not None and (type(context['version']) is not int or context['version'] < 1)):
                raise ValueError
            plan = _checked_plan(packet)
            candidate = packet.get('candidate')
            if (candidate is not None and (not isinstance(candidate, str) or not re.fullmatch(r'[0-9a-f]{40,64}', candidate))
                    or packet['state'] == 'captured' and (plan is not None or candidate is not None)
                    or packet['state'] == 'planned' and (plan is None or candidate is not None)
                    or packet['state'] in {'prepared', 'committed'} and (plan is None or candidate is None)):
                raise ValueError
            return packet
        except (AnswerRefused, ValueError, TypeError, UnicodeDecodeError):
            raise FeedbackOutcomeUnknown('The private feedback record cannot be verified; keep your note and original action.') from None
        finally:
            os.close(fd)

    def write(self, packet, *, create=False):
        event_id = packet['request']['event_id']
        previous = self.read(event_id)
        if (create and previous is not None or not create and previous is None
                or previous is not None and previous['request'] != packet['request']):
            raise FeedbackOutcomeUnknown('The private feedback identity changed; keep the original action for recovery.')
        raw = (json.dumps(packet, ensure_ascii=True, sort_keys=True) + '\n').encode()
        if len(raw) > 65536:
            raise AnswerRefused('The private feedback record exceeds its safe size; keep your note.')
        temporary = '.feedback-' + event_id + '-' + uuid.uuid4().hex + '.tmp'
        handle = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
        try:
            with os.fdopen(handle, 'wb') as target:
                target.write(raw)
                target.flush()
                os.fsync(target.fileno())
            os.replace(temporary, event_id + '.json', src_dir_fd=self.fd, dst_dir_fd=self.fd)
            os.fsync(self.fd)
        finally:
            try:
                os.unlink(temporary, dir_fd=self.fd)
            except FileNotFoundError:
                pass


def _public_path(root, relative):
    path = Path(root)
    for part in relative.split('/'):
        path /= part
        if path.is_symlink():
            raise AnswerRefused('A public feedback record crosses a symlink; no action was rebound.')
    return path


def _checked_plan(packet):
    plan = packet.get('plan')
    if plan is None:
        return None
    card = packet['request']['card']
    voice_path = packet['context'].get('voice')
    if not safe_voice_path(voice_path):
        raise FeedbackOutcomeUnknown('The private voice identity needs agent recovery.')
    allowed = {CARDS + '/' + card, voice_path, APPROVALS}
    if (not isinstance(plan, dict) or not isinstance(plan.get('base'), str)
            or not re.fullmatch(r'[0-9a-f]{40,64}', plan['base'])
            or not isinstance(plan.get('writes'), list) or not 1 <= len(plan['writes']) <= 3):
        raise FeedbackOutcomeUnknown('The pending public feedback plan needs an agent recovery.')
    paths = []
    for write in plan['writes']:
        if (not isinstance(write, dict) or write.get('path') not in allowed
                or write.get('mode') not in board.REGULAR_MODES
                or not isinstance(write.get('new'), str) or not re.fullmatch(r'[0-9a-f]{64}', write['new'])
                or write.get('old') is not None and (not isinstance(write['old'], str) or not re.fullmatch(r'[0-9a-f]{64}', write['old']))):
            raise FeedbackOutcomeUnknown('The pending public feedback plan needs an agent recovery.')
        paths.append(write['path'])
    if len(paths) != len(set(paths)) or CARDS + '/' + card not in paths:
        raise FeedbackOutcomeUnknown('The pending public feedback plan has conflicting paths.')
    return plan


def _receipt(root, packet):
    candidate = packet.get('candidate')
    if candidate is None:
        return None
    plan = _checked_plan(packet)
    if not re.fullmatch(r'[0-9a-f]{40,64}', candidate) or plan is None:
        raise FeedbackOutcomeUnknown('The public feedback receipt cannot be verified.')
    try:
        if _git(root, 'merge-base', candidate, 'HEAD').strip() != candidate:
            return None
        if _git(root, 'show', '-s', '--format=%P', candidate).strip() != plan['base']:
            raise FeedbackOutcomeUnknown('The public feedback parent identity differs.')
        for write in plan['writes']:
            blob = board.committed_blob(root, write['path'], candidate)
            if blob is None or sha256(blob) != write['new']:
                raise FeedbackOutcomeUnknown('The public feedback receipt differs from its private plan.')
        card = board.committed_blob(root, CARDS + '/' + packet['request']['card'], candidate)
        if ('**Feedback event:** ' + packet['request']['event_id']).encode() not in card:
            raise FeedbackOutcomeUnknown('The public feedback event identity is absent.')
        return candidate
    except AnswerRefused:
        raise FeedbackOutcomeUnknown('The public feedback outcome is unavailable; retry the original action.') from None


def _reconcile_worktree(root, packet, *, committed):
    """Restore only exact planned bytes; unknown or later work is untouched."""
    plan = _checked_plan(packet)
    if plan is None:
        return
    repairs, refresh = [], []
    for write in plan['writes']:
        relative = write['path']
        desired = board.committed_blob(root, relative)
        wanted = sha256(desired) if desired is not None else None
        if committed and wanted != write['new']:
            continue  # A later committed edit/deletion is never undone by replay.
        if not committed and wanted != write['old']:
            raise AnswerRefused('The pending feedback source changed; an agent must reconcile the retained original.')
        path = _public_path(root, relative)
        if path.exists() and (not path.is_file() or path.stat().st_nlink != 1):
            raise AnswerRefused('The pending feedback path is not an ordinary file.')
        actual = path.read_bytes() if path.exists() else None
        actual_sha = sha256(actual) if actual is not None else None
        listed = _git(root, 'ls-files', '--stage', '-z', '--', relative).split('\0')
        rows = [row for row in listed if row]
        index_sha = None
        if rows:
            if len(rows) != 1 or rows[0].split('\t', 1)[0].split()[2] != '0':
                raise AnswerRefused('The public feedback index needs reconciliation.')
            mode, object_id, _ = rows[0].split('\t', 1)[0].split()
            if mode != write['mode']:
                raise AnswerRefused('The public feedback index mode changed.')
            index_sha = sha256(_git(root, 'cat-file', 'blob', object_id, binary=True))
        recognized = {write['old'], write['new']}
        if actual_sha not in recognized or index_sha not in recognized:
            raise AnswerRefused('Unrelated feedback-file work is preserved; an agent must reconcile it.')
        if not committed and index_sha != wanted:
            raise AnswerRefused('Staged feedback-file work is preserved; an agent must reconcile it.')
        if actual != desired:
            repairs.append((path, desired))
        if committed and index_sha != wanted:
            refresh.append(relative)
    for path, desired in repairs:
        if desired is None:
            path.unlink(missing_ok=True)
        else:
            board._replace(path, desired)
    if refresh:
        _git(root, 'update-index', '--add', '--', *refresh)


def _voice_write(root, voice, request, context):
    data = voice.blob if voice.blob is not None else INITIAL_VOICE
    header, entries = data.split(b'## Entries', 1)
    version = context['version']
    header = re.sub(rb'(?m)(^\*\*Version:\*\* )[0-9]+(?=\r?$)',
                    lambda match: match[1] + str(version).encode(), header, count=1)
    entry = (f'\n### Feedback version {version}\n\n**Page:** {context["page"]}\n'
             f'**Content hash:** {context["hash"]}\n**Date:** {context["when"][:10]}\n'
             f'**Card:** {request.card}\n**Kind:** {context["kind"]}\n'
             f'**Version:** {version}\n**Event:** {request.event_id}\n'
             '**Interpretation:** pending\n**Disposition:** pending\n')
    if request.kind == 'rate':
        entry += f'**Rating:** {request.value} of 5\n'
    new = header + b'## Entries' + entries + (b'' if data.endswith(b'\n') else b'\n') + entry.encode()
    return voice.path, _public_path(root, voice.path), voice.mode, voice.blob, new


def _public_writes(cards_dir, card, request, when):
    root, base, relative, path, mode, blob = board._checked_card(cards_dir, card, request.card_sha)
    if relative != CARDS + '/' + request.card:
        raise AnswerRefused('Page feedback must use the canonical page-review cards.')
    validate_page_confirmation(root, base, card, blob)
    actual = parse_card(card.file, _text(blob, relative))
    voice = read_voice(root, base)
    if voice.sha != request.voice_sha:
        raise AnswerRefused('The voice record changed since this page was shown; reload and keep your note.')
    paths = feedback_paths(root, base)
    board._unchanged(root, base, MANIFEST, _public_path(root, MANIFEST), paths.manifest_sha, 'page-feedback manifest')
    voice_path = _public_path(root, voice.path)
    if voice.blob is None:
        if voice_path.exists() or _git(root, 'status', '--porcelain', '--', voice.path).strip():
            raise AnswerRefused('The voice record has uncommitted work; keep your note.')
    else:
        board._unchanged(root, base, voice.path, voice_path, voice.sha, 'voice record')
    if actual.waiting and card_voice_version(actual, voice.path) is None:
        raise AnswerRefused('This page review needs an agent refresh before feedback can be saved; keep your note.')
    confirm = request.kind == 'answer' and request.value == 'confirm'
    if request.kind == 'answer':
        if actual.answer is not None or actual.flag is not None:
            raise AnswerRefused('This page card is already answered or held for rewrite.')
        if not confirm and not request.note.strip():
            raise AnswerRefused('A return needs a note saying what should change.')
    if request.kind == 'flag' and actual.flag is not None:
        raise AnswerRefused('This page card is already flagged too taxing.')
    context = {'voice': voice.path, 'page': actual.fields['Page'], 'hash': actual.fields['Content hash'],
               'when': when, 'kind': request.value if request.kind == 'answer' else request.kind,
               'version': None if confirm else voice.version + 1}
    writes = []
    if request.kind == 'answer':
        recorded = '**Returned:** yes\n'
        if confirm:
            writes.append(board._confirmation_write(root, base, actual, relative, path, request.record_sha, when))
            recorded = f'**Written to:** {APPROVALS}, after `## Approvals`\n'
        section = f'## Answer\n\n**Verdict:** {board.VERDICTS[request.value]}\n**Answered:** {when}\n{recorded}'
    elif request.kind == 'rate':
        section = f'## Rating\n\n**Rating:** {request.value} of 5\n**Rated:** {when}\n'
    else:
        section = f'## Flag\n\n{board.FLAG_LINE}\n**Flagged:** {when}\n'
    section += f'**Feedback event:** {request.event_id}\n**Original:** retained privately\n'
    if not confirm:
        section += f'**Voice version:** {context["version"]}\n**Interpretation:** pending\n'
        writes.append(_voice_write(root, voice, request, context))
    writes.append((relative, path, mode, blob, board._appended(blob, relative, section, '')))
    return root, base, context, writes


def _same_request(packet, request):
    if packet['request'] != asdict(request):
        raise AnswerRefused('That feedback event belongs to a different request; keep the original action.')


def _completed(root, store, packet, commit):
    try:
        _reconcile_worktree(root, packet, committed=True)
    except (AnswerRefused, OSError):
        raise board.AnswerWrittenIndexStale(f'committed {commit[:7]}; the public worktree/index needs agent reconciliation') from None
    packet['state'] = 'committed'
    try:
        store.write(packet)
    except (AnswerRefused, FeedbackOutcomeUnknown, OSError):
        pass  # The durable prepared receipt and actual committed event remain replayable.
    return commit


@contextmanager
def _recoverable_io():
    try:
        yield
    except OSError:
        raise FeedbackOutcomeUnknown('Private capture or public save could not be verified. Keep your note and retry this exact action.') from None


def save_page_action(cards_dir, card, request, now=None):
    with _recoverable_io():
        return _save_page_action(cards_dir, card, request, now)


def _save_page_action(cards_dir, card, request, now=None):
    """Call under the existing Board lock; preserve exact text before any public write."""
    if not request.event_id and getattr(card, 'stale', None) is not None:
        raise AnswerRefused(f'{card.file} is stale; read its current replacement')
    request.validate()
    root = board.repo_root(cards_dir)
    with _private_store(root) as existing:
        packet = existing.read(request.event_id) if existing is not None else None
        if packet is not None:
            _same_request(packet, request)
            commit = _receipt(root, packet)
            if commit is not None:
                return _completed(root, existing, packet, commit)
            _reconcile_worktree(root, packet, committed=False)
    if packet is None and _git(root, 'log', '-1', '--format=%H', '--fixed-strings',
                               '--grep=Page feedback event ' + request.event_id, 'HEAD').strip():
        raise FeedbackOutcomeUnknown('A public event exists without its verified private receipt; keep the original action for agent recovery.')
    when = packet['context']['when'] if packet is not None else board._stamp(now)
    root, base, context, writes = _public_writes(cards_dir, card, request, when)
    return _save_prepared(root, base, context, writes, request, packet)


def _save_prepared(root, base, context, writes, request, packet):
    with _private_store(root, create=True) as store:
        if packet is None:
            packet = {'schema': 1, 'request': asdict(request), 'context': context,
                      'state': 'captured', 'plan': None, 'candidate': None}
            store.write(packet, create=True)
        packet['context'] = context
        packet['candidate'] = None
        packet['plan'] = {'base': base, 'writes': [{'path': relative, 'mode': mode,
                           'old': sha256(old) if old is not None else None, 'new': sha256(new)}
                          for relative, path, mode, old, new in writes]}
        packet['state'] = 'planned'
        store.write(packet)
        def before_cas(candidate):
            packet['candidate'], packet['state'] = candidate, 'prepared'
            store.write(packet)
        try:
            commit = board._write_and_commit(root, base, writes,
                f'Grill Board: {request.kind} page {request.card}',
                f'Page feedback event {request.event_id}; original privately captured; public references only.',
                before_cas=before_cas)
        except (KeyboardInterrupt, SystemExit):
            raise
        except (AnswerRefused, OSError, FeedbackOutcomeUnknown) as error:
            recorded = _receipt(root, packet)
            if recorded is not None:
                return _completed(root, store, packet, recorded)
            raise FeedbackOutcomeUnknown('Your original is retained privately; the public record is pending. Retry this exact action.') from None
        return _completed(root, store, packet, commit)


def request_from_form(form, action):
    kind = action.removeprefix('/')
    value = form.get('verdict', '') if kind == 'answer' else form.get('rating', '') if kind == 'rate' else ''
    return PageRequest(kind, form.get('card', ''), value,
                       form.get('note' if kind == 'answer' else 'comment', ''),
                       form.get('card_sha', ''), form.get('record_sha', '') if kind == 'answer' else '',
                       form.get('voice_sha', ''), form.get('event_id', ''))


def render_fields(cards_dir, card):
    if not is_page_card(cards_dir, card):
        return {}
    try:
        voice = read_voice(board.repo_root(cards_dir), card.commit or 'HEAD')
    except AnswerRefused as error:
        raise CardSourceError(str(error)) from error
    return {'event_id': uuid.uuid4().hex, 'voice_sha': voice.sha}


def replay_page_submission(cards_dir, form, action):
    """Resolve a durable receipt before current-card/state/source checks."""
    if not form.get('event_id'):
        return None
    request = request_from_form(form, action)
    request.validate()
    root = board.repo_root(cards_dir)
    with _recoverable_io(), board.repository_lock(root), _private_store(root) as store:
        packet = store.read(request.event_id) if store is not None else None
        if packet is None:
            return None
        _same_request(packet, request)
        commit = _receipt(root, packet)
        return _completed(root, store, packet, commit) if commit is not None else None
