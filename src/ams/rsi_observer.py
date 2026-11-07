"""Optional per-Workbench event recording and trusted RSI transport."""
from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
import json
import os
from pathlib import Path
import sqlite3
import sys

from ams import assessment, keycheck, skill_audit, writer
from ams.skill_audit import canonical, require, timestamp, token

DATABASE = Path('workbench/rsi-observer/.local/observer.sqlite3')
EVENT_FIELDS = {
    'event_id', 'chat_id', 'occurred_at', 'kind', 'skill', 'skill_revision',
    'request_event_id', 'outcome', 'evidence_id',
}
KINDS = {
    'skill_requested': {'skill', 'evidence_id'},
    'skill_loaded': {'skill', 'skill_revision', 'request_event_id', 'evidence_id'},
    'skill_used': {'skill', 'skill_revision', 'request_event_id', 'outcome', 'evidence_id'},
    'failure': {'skill', 'skill_revision', 'outcome', 'evidence_id'},
    'work_status': {'outcome', 'evidence_id'},
}
CHANNELS = {
    'observation': ('rsi_observation', 'event_id', 'occurred_at'),
    'audit': ('skill_audit', 'audit_run_id', 'completed_at'),
}


def _event(payload):
    require(isinstance(payload, dict) and payload.keys() <= EVENT_FIELDS, 'unknown observation fields')
    event = {field: payload.get(field) for field in EVENT_FIELDS}
    for field in ('event_id', 'chat_id'):
        token(event[field], field)
    event['occurred_at'] = timestamp(event['occurred_at'], 'occurred_at')
    kind = event['kind']
    require(isinstance(kind, str) and kind in KINDS, 'unknown observation kind')
    permitted = {'event_id', 'chat_id', 'occurred_at', 'kind'} | KINDS[kind]
    require(all(value is None for field, value in event.items() if field not in permitted),
            'observation fields do not match kind')
    for field in ('request_event_id', 'evidence_id'):
        if event[field] is not None:
            token(event[field], field)
    if kind.startswith('skill_') or event['skill'] is not None:
        token(event['skill'], 'skill', skill_audit.SKILL)
    if event['skill_revision'] is not None:
        assessment.revision(event['skill_revision'], 'observed skill revision')
        require(event['skill'] is not None, 'observed revision needs a skill')
    outcome = event['outcome']
    if kind == 'skill_loaded':
        require(event['skill_revision'] is not None and event['evidence_id'] is not None,
                'observed skill load needs a pinned revision and evidence')
    elif kind == 'skill_used':
        require(outcome in ('used', 'skipped', 'unknown'), 'invalid skill use outcome')
        require(outcome == 'unknown' or event['evidence_id'] is not None,
                'observed skill use or skip needs evidence')
        require(outcome != 'skipped' or event['request_event_id'] is not None,
                'a skipped use needs an explicit request')
    elif kind == 'failure':
        require(outcome in ('routine', 'blocking') and event['evidence_id'] is not None,
                'a failure needs a routine/blocking outcome and evidence')
    elif kind == 'work_status':
        require(outcome in ('ongoing', 'finished', 'blocked'), 'invalid work status')
        require(outcome == 'ongoing' or event['evidence_id'] is not None,
                'finished or blocked status needs evidence')
    return event


class Outbox:
    def __init__(self, project):
        self.path = Path(project).resolve() / DATABASE

    @contextmanager
    def _open(self, *, create=False):
        if not create and not self.path.exists():
            yield None
            return
        require(self.path.resolve() == self.path,
                'observer state must be a local file')
        if create:
            self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
            os.close(descriptor)
        with closing(sqlite3.connect(self.path, timeout=15)) as db, db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS outbox (
                    sequence INTEGER PRIMARY KEY, channel TEXT NOT NULL, id TEXT NOT NULL,
                    chat_id TEXT, content TEXT NOT NULL, private TEXT,
                    delivered INTEGER NOT NULL DEFAULT 0, UNIQUE(channel, id)
                )
            ''')
            db.execute('''
                CREATE TABLE IF NOT EXISTS audit_sets (
                    id TEXT PRIMARY KEY, contract TEXT NOT NULL, is_test INTEGER NOT NULL
                )
            ''')
            yield db

    @staticmethod
    def _insert(db, channel, row, *, private=None):
        _, identity_key, _ = CHANNELS[channel]
        identity = row[identity_key]
        content = canonical(row)
        details = canonical(private) if private is not None else None
        previous = db.execute('SELECT content, private FROM outbox WHERE channel=? AND id=?',
                              (channel, identity)).fetchone()
        if previous is not None:
            require(previous == (content, details), 'outbox identity is immutable')
            return False
        db.execute('INSERT INTO outbox(channel, id, chat_id, content, private) VALUES (?,?,?,?,?)',
                   (channel, identity, row.get('chat_id'), content, details))
        return True

    def record(self, payload):
        event = _event(payload)
        with self._open(create=True) as db:
            db.execute('BEGIN IMMEDIATE')
            parent_id = event['request_event_id']
            if parent_id is not None:
                parent_row = db.execute("SELECT content FROM outbox WHERE channel='observation' AND id=?",
                                        (parent_id,)).fetchone()
                parent = json.loads(parent_row[0]) if parent_row else {}
                require(parent.get('kind') == 'skill_requested' and parent['chat_id'] == event['chat_id']
                        and parent['skill'] == event['skill']
                        and parent['occurred_at'] <= event['occurred_at'],
                        'linked observation needs an earlier matching request in this chat')
                if event['kind'] == 'skill_used' and event['outcome'] != 'unknown':
                    conflicts = db.execute('''
                        SELECT id FROM outbox WHERE channel='observation' AND chat_id=?
                        AND json_extract(content,'$.kind')='skill_used'
                        AND json_extract(content,'$.request_event_id')=?
                        AND json_extract(content,'$.outcome') IN ('used','skipped') AND id<>?
                    ''', (event['chat_id'], parent_id, event['event_id'])).fetchone()
                    require(conflicts is None, 'request already has a recorded use outcome')
            inserted = self._insert(db, 'observation', event)
        return {'event_id': event['event_id'], 'inserted': inserted}

    def record_audit(self, packet, *, is_test=False, is_public=False):
        result = skill_audit.score(packet)
        rows = skill_audit.transport_rows(packet, result, is_test=is_test, is_public=is_public)
        if not rows:
            return result
        contract = {key: value for key, value in packet.items() if key != 'runs'}
        with self._open(create=True) as db:
            db.execute('BEGIN IMMEDIATE')
            set_id = result['audit_set_id']
            saved = db.execute('SELECT contract, is_test FROM audit_sets WHERE id=?', (set_id,)).fetchone()
            if saved is None:
                db.execute('INSERT INTO audit_sets(id, contract, is_test) VALUES (?,?,?)',
                           (set_id, canonical(contract), is_test))
            else:
                require(saved == (canonical(contract), is_test), 'audit set frozen contract differs')
            for row, supplied in zip(rows, packet['runs']):
                run = dict(supplied, completed_at=row['completed_at'])
                self._insert(db, 'audit', row, private=run)
            saved_runs = db.execute('''
                SELECT private FROM outbox WHERE channel='audit'
                AND json_extract(content,'$.audit_set_id')=? ORDER BY sequence
            ''', (set_id,)).fetchall()
            result = skill_audit.score(dict(contract, runs=[json.loads(row[0]) for row in saved_runs]))
        return result

    def status(self, chat_id):
        token(chat_id, 'chat_id')
        with self._open() as db:
            events = db.execute(
                "SELECT content, delivered FROM outbox WHERE chat_id=? ORDER BY sequence", (chat_id,)
            ).fetchall() if db is not None else []
        status = {'chat_id': chat_id, 'work_status': 'unknown', 'requested_uses': {},
                  'critical_failure_ids': [], 'failure_ids': [], 'pending_event_ids': [], 'events': []}
        latest_status_at = ''
        for content, delivered in events:
            event = json.loads(content)
            status['events'].append(event)
            event_id, kind, outcome = event['event_id'], event['kind'], event['outcome']
            if not delivered:
                status['pending_event_ids'].append(event_id)
            if kind == 'work_status' and event['occurred_at'] >= latest_status_at:
                status['work_status'], latest_status_at = outcome, event['occurred_at']
            if kind == 'skill_requested':
                status['requested_uses'][event_id] = {'skill': event['skill'], 'outcome': 'unknown',
                                                      'load_event_ids': [], 'use_event_id': None}
            if kind == 'failure':
                status['failure_ids'].append(event_id)
            parent = status['requested_uses'].get(event['request_event_id'])
            if parent is not None and kind == 'skill_loaded':
                parent['load_event_ids'].append(event_id)
            if parent is not None and kind == 'skill_used' and outcome != 'unknown':
                parent.update(outcome=outcome, use_event_id=event_id)
                if outcome == 'skipped':
                    status['critical_failure_ids'].append(event_id)
        return status

    def flush(self, transport):
        """Reconcile exact remote identity before writing, then acknowledge locally."""
        with self._open() as db:
            pending = db.execute(
                'SELECT sequence, channel, content FROM outbox WHERE delivered=0 ORDER BY sequence'
            ).fetchall() if db is not None else []
        for sequence, channel, content in pending:
            row = json.loads(content)
            transport.deliver(channel, row)
            with self._open() as db:
                db.execute('UPDATE outbox SET delivered=1 WHERE sequence=? AND content=?', (sequence, content))
        return {'acknowledged': len(pending)}


class Store:
    def __init__(self, settings, http=writer.urllib_http):
        require(settings.key is not None and keycheck.key_format(settings.key) != 'unrecognized',
                'trusted RSI writer credentials are unavailable')
        self._settings, self._http = settings, http

    def _call(self, function, payload):
        url = self._settings.url.rstrip('/') + '/rest/v1/rpc/' + function
        try:
            status, raw = self._http('POST', url, writer._headers(self._settings.key), canonical(payload).encode())
        except Exception as exc:
            raise assessment.Refused('RSI transport unavailable; pending evidence retained') from exc
        require(status == 200, f'RSI transport refused (HTTP {status}); pending evidence retained')
        try:
            return json.loads(raw)
        except ValueError as exc:
            raise assessment.Refused('RSI transport returned malformed JSON; pending evidence retained') from exc

    def deliver(self, channel, row):
        relation, identity, time_key = CHANNELS[channel]
        saved = self._call('ams_get_' + relation, {'p_' + identity: row[identity]})
        if saved is None:
            saved = self._call('ams_append_' + relation, {'p_row': row})
        require(isinstance(saved, dict) and row.keys() <= saved.keys(), 'missing RSI row readback')
        projection = {key: saved[key] for key in row}
        if projection[time_key] is not None:
            projection[time_key] = timestamp(projection[time_key], time_key)
        require(canonical(projection) == canonical(row), 'RSI identity readback differs; pending evidence retained')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('record', 'audit-score', 'audit-record'):
        sub = commands.add_parser(command)
        sub.add_argument('input', nargs='?', default='-', help='JSON file or - for stdin')
        if command == 'audit-record':
            sub.add_argument('--test', action='store_true', help='mark synthetic rows')
            sub.add_argument('--public', action='store_true', help='allow completed rows in public projection')
    commands.add_parser('status').add_argument('chat_id')
    commands.add_parser('flush', help='use the trusted Supabase writer to reconcile the local outbox')
    args = parser.parse_args(argv)
    outbox = Outbox(args.project)
    try:
        if args.command == 'status':
            result = outbox.status(args.chat_id)
        elif args.command == 'flush':
            result = outbox.flush(Store(keycheck.load_settings(dotenv_path=args.project / '.env')))
        else:
            payload = json.load(sys.stdin) if args.input == '-' else json.loads(Path(args.input).read_text())
            if args.command == 'record':
                result = outbox.record(payload)
            elif args.command == 'audit-score':
                result = skill_audit.score(payload)
            else:
                result = outbox.record_audit(payload, is_test=args.test, is_public=args.public)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, TypeError, sqlite3.Error) as exc:
        print(f'RSI observer refused: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
