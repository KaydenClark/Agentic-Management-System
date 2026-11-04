"""Read native DQC views and submit native transactions; never edit their records."""

import copy
import functools
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .answers import AnswerRefused, AnswerWrittenIndexStale, repo_root
from .cards import Card, CardSourceError, Refusal, _git, committed_snapshot, load_cards

TOOL = 'workbench/tools/landmark-tracker.mjs'


class OutcomeUnknown(AnswerRefused):
    """The native action may have committed; preserve its exact retry identity."""


def _native(root, arguments, payload=None):
    tool = root / TOOL
    if not tool.is_file() or tool.is_symlink() or not tool.resolve().is_relative_to(root.resolve()):
        raise CardSourceError('The supported native tracker tool is unavailable; preserve work and restore it through setup-workbench.')
    try:
        result = subprocess.run(['node', TOOL, *arguments, '--json'], cwd=root,
                                input=json.dumps(payload, ensure_ascii=False) if payload is not None else None,
                                text=True, capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        if payload is None:
            raise CardSourceError('The native tracker view timed out; the current source is unavailable.') from None
        raise OutcomeUnknown('The native tracker did not return. Check or retry the original action below.') from None
    except OSError:
        raise CardSourceError('The native tracker could not be started.') from None
    try:
        value = json.loads(result.stdout)
        if not isinstance(value, dict):
            raise ValueError
        if value.get('status') == 'blocked':
            error = value.get('error')
            if not isinstance(error, dict) or not isinstance(error.get('code'), str) or not isinstance(error.get('message'), str):
                raise ValueError
            message = f"{error['code']}: {error['message']}"
            if error['code'] == 'committed-index-failure':
                raise AnswerWrittenIndexStale(message)
            raise AnswerRefused(message)
        if result.returncode:
            raise ValueError
        if payload is not None:
            if value.get('status') not in ('committed', 'replayed') or not re.fullmatch(r'[0-9a-f]{40}', value.get('commit', '')) or not isinstance(value.get('changedFiles'), list):
                raise ValueError
        elif value.get('status') != 'shown' or not isinstance(value.get('tracker'), dict):
            raise ValueError
    except (ValueError, TypeError):
        if payload is not None:
            raise OutcomeUnknown('The save receipt was unreadable. The original action may already be saved; check or retry it below.') from None
        raise CardSourceError('The native tracker returned an invalid view.') from None
    return value


@functools.lru_cache(maxsize=16)
def _committed(root, head):
    value = _native(Path(root), ['show', '--committed'])
    if value.get('head') != head or not isinstance(value.get('tracker', {}).get('questions'), list):
        raise CardSourceError('The project changed while reading the Board; reload to read one committed snapshot.')
    tracker = value['tracker']
    try:
        for card in tracker['questions']:
            life = card['lifecycle']
            if not all(isinstance(card[key], str) for key in ('id', 'title', 'question')) or not isinstance(card['revision'], int):
                raise ValueError
            if life['state'] not in ('pending','reopened','confirmed','needs-rewrite','deferred','superseded'):
                raise ValueError
            if not isinstance(life['events'], list) or not isinstance(life['confirmations'], list):
                raise ValueError
            proposal = life['proposal']
            if proposal is not None:
                if not all(isinstance(proposal[key], str) for key in ('readback','why','source','scope','round')) or not isinstance(proposal['dependencies'], list):
                    raise ValueError
                for key in ('priority','value'):
                    if proposal[key]['value'] not in (1,2,3,4) or not isinstance(proposal[key]['reason'], str):
                        raise ValueError
            for event in life['events']:
                if not isinstance(event, dict) or not isinstance(event['eventId'], str) or not isinstance(event['type'], str) or not isinstance(event['revision'], int):
                    raise ValueError
                if any(event.get(key) is not None and not isinstance(event[key], str) for key in ('source','note','at','kind')):
                    raise ValueError
                if event.get('rating') is not None and event['rating'] not in (1,2,3,4,5):
                    raise ValueError
            for saved in life['confirmations']:
                if not isinstance(saved, dict) or not isinstance(saved['source'], str):
                    raise ValueError
                if any(saved.get(key) is not None and not isinstance(saved[key], str) for key in ('readback','scope')):
                    raise ValueError
            if not isinstance(card.get('history', []), list) or not isinstance(card.get('related', []), list):
                raise ValueError
            for entry in card.get('history', []):
                if not isinstance(entry['revision'], int) or not isinstance(entry['reason'], str) or not isinstance(entry['changes'], list):
                    raise ValueError
                for change in entry['changes']:
                    if not isinstance(change['field'], str):
                        raise ValueError
                    if change['field'] == 'lifecycle':
                        previous = change['to'].get('proposal')
                        if previous and not all(isinstance(previous[key], str) for key in ('readback','why')):
                            raise ValueError
            for item in card.get('related', []):
                if not all(isinstance(item[key], str) for key in ('key','reason')):
                    raise ValueError
                if any(item.get(key) is not None and not isinstance(item[key], str) for key in ('state','resolution')):
                    raise ValueError
            if card.get('result') is not None and not isinstance(card['result']['summary'], str):
                raise ValueError
            if not isinstance(card.get('uncertainty', []), list) or any(not isinstance(item, str) for item in card.get('uncertainty', [])):
                raise ValueError
            if proposal and any(not isinstance(item, str) for item in proposal['dependencies']):
                raise ValueError
        if not isinstance(tracker.get('rounds', []), list):
            raise ValueError
        for item in tracker.get('rounds', []):
            if not isinstance(item['id'], str) or not isinstance(item['changed'], list):
                raise ValueError
            for change in item['changed']:
                if not isinstance(change['id'], str) or not isinstance(change['revision'], int) or not isinstance(change.get('events', []), list):
                    raise ValueError
                if not isinstance(change.get('dependencies', []), list) or any(not isinstance(dependency, str) for dependency in change.get('dependencies', [])):
                    raise ValueError
            receipt = item.get('receipt')
            if receipt is not None:
                if not all(isinstance(receipt[key], str) for key in ('outcome','nextFrontier')) or not isinstance(receipt['sources'], list) or any(not isinstance(source, str) for source in receipt['sources']):
                    raise ValueError
    except (AttributeError, KeyError, TypeError, ValueError):
        raise CardSourceError('The native tracker returned an incomplete view; no current questions can be presented safely.') from None
    return value['tracker']


@dataclass
class DqcCard(Card):
    dqc: dict | None = None
    blocked: list = field(default_factory=list)

    @property
    def waiting(self):
        life = self.dqc['lifecycle']
        return bool(life.get('proposal') and life['proposal'].get('actionable', True)
                    and life['state'] in ('pending', 'reopened') and not self.blocked)

    @property
    def rating(self):
        ratings = [event['rating'] for event in self.dqc['lifecycle']['events'] if event['type'] == 'rate']
        return str(ratings[-1]) if ratings else ''


def load_board(cards_dir, legacy_loader=load_cards):
    root = repo_root(cards_dir)
    head, _ = committed_snapshot(cards_dir)
    cards, refusals = legacy_loader(cards_dir)
    if any(card.commit != head for card in cards):
        raise CardSourceError('The project changed while reading legacy cards; reload.')
    manifest_blob = _git(root, 'ls-tree', '--name-only', head, '--', 'workbench/manifest.json') if head else ''
    tracker = None
    if manifest_blob.strip():
        try:
            manifest = json.loads(_git(root, 'show', f'{head}:workbench/manifest.json'))
            if manifest.get('landmarkTracker'):
                tracker = copy.deepcopy(_committed(str(root), head))
                by_id = {data['id']:data for data in tracker['questions']}
                for data in tracker['questions']:
                    life = data['lifecycle']; proposal = life.get('proposal')
                    # Old records without a proposal remain navigable context, never a fabricated question.
                    p = proposal or {}
                    priority, value = p.get('priority', {}), p.get('value', {})
                    cards.append(DqcCard(file=data['id'], question=data['question'],
                        priority=f"P{priority.get('value', 4)}", priority_reason=priority.get('reason', 'No owner priority recorded.'),
                        value=f"V{value.get('value', 4)}", value_reason=value.get('reason', 'No owner value recorded.'),
                        fields={'Topic': data['title']}, commit=head, sha=life.get('digest') or '', dqc=data,
                        blocked=[ident for ident in p.get('dependencies', []) if by_id.get(ident, {}).get('lifecycle', {}).get('state') != 'confirmed'],
                        answer={'Verdict':'Confirmed'} if life['state'] == 'confirmed' else None,
                        flag={'Too taxing':'yes'} if life['state'] == 'needs-rewrite' else None))
                # An explicitly linked legacy card is retained as history; its DQC alone asks the question.
                ids = {c['id'] for c in tracker['questions']}
                for card in cards:
                    if not isinstance(card, DqcCard) and card.fields.get('DQC') in ids and card.waiting:
                        card.flag = {'Migrated':card.fields['DQC']}
        except (ValueError, AnswerRefused, CardSourceError) as error:
            refusals.append(Refusal('DQC tracker', [str(error)]))
            tracker = {'error':str(error)}
    return sorted(cards, key=lambda card:card.sort_key), refusals, tracker, head


def submit(cards_dir, form, endpoint):
    """Map the Board's own fields to an owning native action, including retry identity."""
    root = repo_root(cards_dir)
    payload = {'eventId':form.get('eventId', ''), 'expectHead':form.get('expectHead', ''),
               'source':'Owner action on the local Grill Board'}
    ident = form.get('card', '')
    if endpoint == '/round':
        payload.update(type='finish-round', round=form.get('round', ''))
        arguments = ['action', '--stdin']
    else:
        try:
            revision = int(form.get('expectRevision', ''))
        except ValueError:
            raise AnswerRefused('The displayed DQC revision is missing; reload.') from None
        if not ident.startswith('DQC-') or '/' in ident or '\\' in ident:
            raise AnswerRefused('The displayed DQC identity is invalid.')
        payload.update(expectRevision=revision, digest=form.get('digest', ''))
        if endpoint == '/answer':
            verdict = form.get('verdict')
            if verdict == 'confirm':
                payload.update(type='confirm', scope=form.get('scope', ''), note=form.get('note', ''))
            elif verdict in ('rework-wording', 'change-the-why', 'change'):
                payload.update(type='correct', kind=verdict, note=form.get('note', ''))
            else:
                raise AnswerRefused('Unknown DQC verdict.')
        elif endpoint == '/rate':
            try:
                rating = int(form.get('rating', ''))
            except ValueError:
                raise AnswerRefused('A rating must be a whole number from 1 to 5.') from None
            payload.update(type='rate', rating=rating, note=form.get('comment', ''))
        elif endpoint == '/flag':
            payload.update(type='flag', note=form.get('comment', ''))
        else:
            raise AnswerRefused('Unknown DQC action.')
        arguments = ['action', ident, '--stdin']
    return _native(root, arguments, payload)
