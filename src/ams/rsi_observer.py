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


# Accept an observation object containing only event_id, chat_id, occurred_at, kind, skill, skill_revision, request_event_id, outcome and evidence_id, fill omitted fields with null, and validate the event and chat tokens and canonical UTC event time.
def _event(payload):
    require(isinstance(payload, dict) and payload.keys() <= EVENT_FIELDS, 'unknown observation fields')
    event = {field: payload.get(field) for field in EVENT_FIELDS}
    for field in ('event_id', 'chat_id'):
        token(event[field], field)
    event['occurred_at'] = timestamp(event['occurred_at'], 'occurred_at')
    # Accept skill_requested with skill and optional evidence_id, skill_loaded with skill, skill_revision, optional request_event_id and evidence_id, skill_used with skill, optional skill_revision and request_event_id, outcome and optional evidence_id, failure with optional skill and skill_revision, outcome and evidence_id, and work_status with outcome and optional evidence_id, refusing all other kinds and nonnull fields outside the selected kind.
    kind = event['kind']
    require(isinstance(kind, str) and kind in KINDS, 'unknown observation kind')
    permitted = {'event_id', 'chat_id', 'occurred_at', 'kind'} | KINDS[kind]
    require(all(value is None for field, value in event.items() if field not in permitted),
            'observation fields do not match kind')
    # Validate supplied link and evidence IDs as opaque tokens and supplied skill names as skill slugs, and require a skill when a supplied observed revision is validated as a full commit pin.
    for field in ('request_event_id', 'evidence_id'):
        if event[field] is not None:
            token(event[field], field)
    if kind.startswith('skill_') or event['skill'] is not None:
        token(event['skill'], 'skill', skill_audit.SKILL)
    if event['skill_revision'] is not None:
        assessment.revision(event['skill_revision'], 'observed skill revision')
        require(event['skill'] is not None, 'observed revision needs a skill')
    # Loads, observed uses, failures and finished or blocked work states each require evidence.
    # A skip also requires an explicit request. Unknown use can remain unresolved.
    outcome = event['outcome']
    # Require a pinned revision and an evidence reference for a load, and keep an unconfirmed load out of that observed-load state.
    if kind == 'skill_loaded':
        require(event['skill_revision'] is not None and event['evidence_id'] is not None,
                'observed skill load needs a pinned revision and evidence')
    # Accept used, skipped or unknown for use, require evidence for used or skipped, and require an explicit request link for skipped.
    elif kind == 'skill_used':
        require(outcome in ('used', 'skipped', 'unknown'), 'invalid skill use outcome')
        require(outcome == 'unknown' or event['evidence_id'] is not None,
                'observed skill use or skip needs evidence')
        require(outcome != 'skipped' or event['request_event_id'] is not None,
                'a skipped use needs an explicit request')
    # Accept routine or blocking for failure and require evidence, and accept ongoing, finished or blocked for work status with evidence required for finished or blocked.
    elif kind == 'failure':
        require(outcome in ('routine', 'blocking') and event['evidence_id'] is not None,
                'a failure needs a routine/blocking outcome and evidence')
    elif kind == 'work_status':
        require(outcome in ('ongoing', 'finished', 'blocked'), 'invalid work status')
        require(outcome == 'ongoing' or event['evidence_id'] is not None,
                'finished or blocked status needs evidence')
    return event


# Resolve the selected Workbench root, use its workbench/rsi-observer/.local/observer.sqlite3 state, return an empty read when the state file is absent, and refuse state that resolves through a symbolic link to another path.
class Outbox:
    def __init__(self, project):
        self.path = Path(project).resolve() / DATABASE

    @contextmanager
    def _open(self, *, create=False):
        require(self.path.resolve() == self.path,
                'observer state must be a local file')
        if not create and not self.path.exists():
            yield None
            return
        # When recording creates state, request creation mode 0700 for the state directory and 0600 for the database file, and open the file without following a symbolic link.
        if create:
            self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
            os.close(descriptor)
        # Use a 15-second SQLite lock wait and ensure the existing transactional outbox and audit-set tables exist.
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

    # Store the canonical safe row and any canonical private data under the channel and stable identity, report an identical replay as already recorded, and refuse a changed replay without replacing any evidence.
    @staticmethod
    def _insert(db, channel, row, *, private=None):
        _, identity_key, _ = CHANNELS[channel]
        identity = row[identity_key]
        content = canonical(row)
        details = canonical(private) if private is not None else None
        # Replay only identical content. A changed payload cannot replace evidence under an existing identity.
        previous = db.execute('SELECT content, private FROM outbox WHERE channel=? AND id=?',
                              (channel, identity)).fetchone()
        if previous is not None:
            require(previous == (content, details), 'outbox identity is immutable')
            return False
        db.execute('INSERT INTO outbox(channel, id, chat_id, content, private) VALUES (?,?,?,?,?)',
                   (channel, identity, row.get('chat_id'), content, details))
        return True

    # Validate the event before opening state for writes, and record it in a transaction that checks any linked parent is an already recorded skill_requested event of the same chat and skill at or before the new event time.
    def record(self, payload):
        event = _event(payload)
        with self._open(create=True) as db:
            db.execute('BEGIN IMMEDIATE')
            # Validate the earlier same-chat request and its single resolved use in the recording transaction.
            parent_id = event['request_event_id']
            if parent_id is not None:
                parent_row = db.execute("SELECT content FROM outbox WHERE channel='observation' AND id=?",
                                        (parent_id,)).fetchone()
                parent = json.loads(parent_row[0]) if parent_row else {}
                require(parent.get('kind') == 'skill_requested' and parent['chat_id'] == event['chat_id']
                        and parent['skill'] == event['skill']
                        and parent['occurred_at'] <= event['occurred_at'],
                        'linked observation needs an earlier matching request in this chat')
                # Permit multiple loads and unknown uses for a request, but allow only one resolved linked used or skipped event across distinct identities, then return event_id and whether an insertion occurred.
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

    # Score the incoming audit and derive its writer rows before opening state for writes, and return a zero-run preview without creating durable evidence.
    def record_audit(self, packet, *, is_test=False, is_public=False):
        result = skill_audit.score(packet)
        rows = skill_audit.transport_rows(packet, result, is_test=is_test, is_public=is_public)
        # A scoring preview with no runs has no durable evidence to append.
        if not rows:
            return result
        # In one write transaction freeze the packet without its runs and the synthetic marker for that audit_set_id, refuse a changed frozen contract, and save each immutable writer row together with the supplied private run and its normalized completion timestamp.
        contract = {key: value for key, value in packet.items() if key != 'runs'}
        with self._open(create=True) as db:
            db.execute('BEGIN IMMEDIATE')
            # Freeze the set contract and retain private evidence atomically with the safe transport rows.
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
            # Recover all retained private runs for the set in record order, rescore them together, and commit only after the recovered set validates so a partial upload cannot remove earlier runs or commit a conflicting or fourth run.
            saved_runs = db.execute('''
                SELECT private FROM outbox WHERE channel='audit'
                AND json_extract(content,'$.audit_set_id')=? ORDER BY sequence
            ''', (set_id,)).fetchall()
            result = skill_audit.score(dict(contract, runs=[json.loads(row[0]) for row in saved_runs]))
        return result

    # Return chat_id, work_status, requested_uses, critical_failure_ids, failure_ids, pending_event_ids and events for the selected chat, defaulting work_status and unresolved requested use to unknown and exposing events and pending delivery IDs in record order.
    def status(self, chat_id):
        token(chat_id, 'chat_id')
        with self._open() as db:
            events = db.execute(
                "SELECT content, delivered FROM outbox WHERE chat_id=? ORDER BY sequence", (chat_id,)
            ).fetchall() if db is not None else []
        status = {'chat_id': chat_id, 'work_status': 'unknown', 'requested_uses': {},
                  'critical_failure_ids': [], 'failure_ids': [], 'pending_event_ids': [], 'events': []}
        # Choose the latest explicit work_status by event time with record order breaking equal timestamps, keep failure IDs separately, and track each request with its skill, load_event_ids, resolved outcome and use_event_id.
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
            # Attach linked load IDs without changing use, ignore an unknown use as a resolution, and classify only an evidenced resolved skip of an explicit request as Critical even when work finishes or the skill never loads.
            parent = status['requested_uses'].get(event['request_event_id'])
            if parent is not None and kind == 'skill_loaded':
                parent['load_event_ids'].append(event_id)
            if parent is not None and kind == 'skill_used' and outcome != 'unknown':
                parent.update(outcome=outcome, use_event_id=event_id)
                if outcome == 'skipped':
                    status['critical_failure_ids'].append(event_id)
        return status

    # Read the pending outbox rows in append order and deliver each row through the supplied trusted transport before acknowledging that exact local row in its own local transaction.
    def flush(self, transport):
        """Reconcile exact remote identity before writing, then acknowledge locally."""
        with self._open() as db:
            pending = db.execute(
                'SELECT sequence, channel, content FROM outbox WHERE delivered=0 ORDER BY sequence'
            ).fetchall() if db is not None else []
        # Deliver in record order so linked requests reach the writer first. Keep failures pending for replay.
        # Stop on a delivery failure or mismatched readback, preserve every acknowledgement already committed, and leave the failed row and later rows pending.
        acknowledged = 0
        for sequence, channel, content in pending:
            row = json.loads(content)
            transport.deliver(channel, row)
            with self._open() as db:
                updated = db.execute('UPDATE outbox SET delivered=1 WHERE sequence=? AND content=? AND delivered=0', (sequence, content))
                acknowledged += updated.rowcount
        # Return acknowledged as the number of pending rows reconciled in this invocation, and reuse the same row identity for a restart after an uncertain external effect.
        return {'acknowledged': acknowledged}


# Construct the separate writer only for explicit transport with a recognized secret or legacy JWT credential from the trusted writer settings, and use the shared writer headers to POST canonical JSON to the configured Supabase RPC endpoint.
class Store:
    def __init__(self, settings, http=writer.urllib_http):
        require(settings.key is not None and keycheck.key_format(settings.key) != 'unrecognized',
                'trusted RSI writer credentials are unavailable')
        self._settings, self._http = settings, http

    # Refuse unavailable transport, a response other than HTTP 200 or malformed JSON while leaving the pending evidence recoverable and keeping credential values out of the error.
    def _call(self, function, payload):
        url = self._settings.url.rstrip('/') + '/rest/v1/rpc/' + function
        try:
            status, raw = self._http('POST', url, writer._headers(self._settings.key), canonical(payload).encode())
        except Exception:
            raise assessment.Refused('RSI transport unavailable; pending evidence retained') from None
        require(status == 200, f'RSI transport refused (HTTP {status}); pending evidence retained')

        def reject_nonfinite(_value):
            raise ValueError('nonfinite JSON number')

        try:
            return json.loads(raw, parse_constant=reject_nonfinite)
        except ValueError:
            raise assessment.Refused('RSI transport returned malformed JSON; pending evidence retained') from None

    def deliver(self, channel, row):
        relation, identity, time_key = CHANNELS[channel]
        # Only a successful read of JSON null authorizes an append.
        # Confirm the persisted projection before the caller acknowledges the local row.
        # Read the observation identity through ams_get_rsi_observation with p_event_id or the audit identity through ams_get_skill_audit with p_audit_run_id before attempting an append.
        saved = self._call('ams_get_' + relation, {'p_' + identity: row[identity]})
        # Append the safe row as p_row through ams_append_rsi_observation or ams_append_skill_audit only on a successful JSON null read, and require the get or append response to contain every projected field.
        if saved is None:
            saved = self._call('ams_append_' + relation, {'p_row': row})
        require(isinstance(saved, dict) and row.keys() <= saved.keys(), 'missing RSI row readback')
        # Normalize the returned occurrence or completion timestamp when present, compare the canonical projection of fields present in the original row while ignoring extra remote fields, and permit local acknowledgement only on an exact match.
        projection = {key: saved[key] for key in row}
        if projection[time_key] is not None:
            projection[time_key] = timestamp(projection[time_key], time_key)
        require(canonical(projection) == canonical(row), 'RSI identity readback differs; pending evidence retained')


# Support record, status, audit-score, audit-record and flush under an optional --project root, read record and audit inputs as JSON from a file or standard input, and keep audit-score as a local scoring preview.
def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest='command', required=True)
    # Accept --test and --public only for audit-record, use the trusted writer environment or selected project's .env only for flush, print the successful JSON result and exit zero, and report expected input, filesystem and database failures to standard error with a nonzero status.
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
