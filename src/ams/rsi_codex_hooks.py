"""Optional, local-only Codex hook adapter; all hook failures are non-blocking."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys

from ams.rsi_observer import Outbox
from ams.skill_audit import SKILL

CONFIG = Path('workbench/rsi-observer/codex-opt-in.json')
MENTION = re.compile(r'(?<![\w$])\$([a-z0-9][a-z0-9-]{0,63})(?![\w-])')
FIRST = re.compile(r'^\s*\$([a-z0-9][a-z0-9-]{0,63})(?=\s|$)')


def digest(*values):
    return hashlib.sha256(json.dumps(values, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()


def observe(project, payload):
    project = Path(project).resolve()
    # Participation belongs to this project and defaults off; malformed or
    # symlinked configuration cannot silently enable observation.
    config_path = project / CONFIG
    if not config_path.is_file() or config_path.is_symlink():
        return
    config = json.loads(config_path.read_text())
    if not isinstance(config, dict) or config.keys() != {'enabled', 'skills'} or config['enabled'] is not True:
        return
    skills = config['skills']
    if not isinstance(skills, list) or not all(isinstance(s, str) and re.fullmatch(SKILL, s) for s in skills):
        return
    if not isinstance(payload, dict) or payload.get('hook_event_name') != 'UserPromptSubmit':
        return  # SessionStart has no stable occurrence ID; never invent one.
    session, turn, prompt, cwd = (payload.get(k) for k in ('session_id', 'turn_id', 'prompt', 'cwd'))
    if not all(isinstance(v, str) and v and len(v) <= 256 for v in (session, turn, cwd)):
        return
    if not isinstance(prompt, str) or len(prompt) > 262144 or Path(cwd).resolve() != project:
        return
    # Accept only a leading explicit invocation with no second skill token.
    # The prompt is examined in memory and never enters the event payload.
    match = FIRST.match(prompt)
    mentions = MENTION.findall(prompt)
    if match is None or mentions != [match.group(1)] or match.group(1) not in skills:
        return
    skill = match.group(1)
    # Hash host IDs before persistence; one turn can reserve only one request.
    chat_id = 'codex-chat-' + digest(session)
    event_id = 'codex-request-' + digest(session, turn)
    outbox = Outbox(project)
    # Reserve the first observation time by identity. Replays retain it instead
    # of changing an immutable event; no prompt, transcript or raw host ID is stored.
    with outbox._open(create=True) as db:
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE IF NOT EXISTS codex_request_times (id TEXT PRIMARY KEY, skill TEXT NOT NULL, occurred_at TEXT NOT NULL)')
        saved = db.execute('SELECT skill, occurred_at FROM codex_request_times WHERE id=?', (event_id,)).fetchone()
        if saved is None:
            when = datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
            db.execute('INSERT INTO codex_request_times VALUES (?,?,?)', (event_id, skill, when))
        else:
            if saved[0] != skill:
                return
            when = saved[1]
    outbox.record({'event_id': event_id, 'chat_id': chat_id, 'occurred_at': when,
                   'kind': 'skill_requested', 'skill': skill})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    try:
        args = parser.parse_args()
        raw = sys.stdin.read(262145)
        if len(raw) <= 262144:
            observe(args.project, json.loads(raw))
    except (OSError, ValueError, TypeError, sqlite3.Error):
        pass  # Observer failure cannot block the user's turn or emit prompt data.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
