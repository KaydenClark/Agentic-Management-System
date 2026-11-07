import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys


def run(project, payload):
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1] / 'src'))
    return subprocess.run([sys.executable, '-m', 'ams.rsi_codex_hooks', '--project', str(project)], input=payload if isinstance(payload, str) else json.dumps(payload), text=True, capture_output=True, env=env)


def events(project):
    path = project / 'workbench/rsi-observer/.local/observer.sqlite3'
    if not path.exists(): return []
    with sqlite3.connect(path) as db:
        return [json.loads(row[0]) for row in db.execute("SELECT content FROM outbox WHERE channel='observation'")]


def config(project, enabled=True):
    folder=project/'workbench/rsi-observer'; folder.mkdir(parents=True, exist_ok=True)
    (folder/'codex-opt-in.json').write_text(json.dumps({'enabled':enabled,'skills':['journey','tdd']}))


def prompt(project, text='$journey do work', turn='turn-1'):
    return {'session_id':'session-1','turn_id':turn,'cwd':str(project),'hook_event_name':'UserPromptSubmit','prompt':text,'transcript_path':'PRIVATE-SHOULD-NOT-APPEAR'}


def test_explicit_request_replay_resume_and_privacy(tmp_path):
    config(tmp_path)
    body=prompt(tmp_path)
    for value in (body, body, {'session_id':'session-1','cwd':str(tmp_path),'hook_event_name':'SessionStart','source':'resume'}, body):
        r=run(tmp_path,value); assert r.returncode == 0 and not r.stdout and not r.stderr
    rows=events(tmp_path); assert len(rows)==1; assert rows[0]['kind']=='skill_requested'; assert rows[0]['skill']=='journey'
    assert 'PRIVATE-SHOULD-NOT-APPEAR' not in (tmp_path/'workbench/rsi-observer/.local/observer.sqlite3').read_bytes().decode(errors='ignore')
    assert rows[0]['outcome'] is None


def test_disabled_ambiguous_incidental_unknown_malformed_fail_open(tmp_path):
    for body in (prompt(tmp_path), '{bad json', {'hook_event_name':'Stop'}):
        r=run(tmp_path,body); assert r.returncode==0 and not r.stdout
    assert events(tmp_path)==[]
    config(tmp_path)
    for text in ('Please use journey', 'mention $journey', '$unknown do work', '$journey then $tdd', '`$journey`', '$journey-other'):
        assert run(tmp_path,prompt(tmp_path,text)).returncode==0
    assert events(tmp_path)==[]
    assert run(tmp_path,prompt(tmp_path,'$tdd verify', 'turn-2')).returncode==0
    assert [e['skill'] for e in events(tmp_path)]==['tdd']


def test_same_session_new_turn_and_refused_outbox_fail_open(tmp_path):
    config(tmp_path)
    assert run(tmp_path,prompt(tmp_path,'$journey verify','turn-1')).returncode==0
    assert run(tmp_path,prompt(tmp_path,'$tdd verify','turn-2')).returncode==0
    rows=events(tmp_path)
    assert len(rows)==2 and rows[0]['chat_id']==rows[1]['chat_id']
    assert rows[0]['event_id'] != rows[1]['event_id']
    assert all(row['kind']=='skill_requested' for row in rows)
    # An unusable local outbox cannot block a user's prompt or disclose it.
    other=tmp_path/'other'; config(other)
    state=other/'workbench/rsi-observer/.local/observer.sqlite3'; state.parent.mkdir(); state.write_text('not a database')
    result=run(other,prompt(other,'$journey PRIVATE-PROMPT'))
    assert result.returncode==0 and not result.stdout and not result.stderr


def test_wrong_project_and_disabled_flag_do_not_record(tmp_path):
    config(tmp_path, False)
    run(tmp_path,prompt(tmp_path)); assert events(tmp_path)==[]
    config(tmp_path)
    value=prompt(tmp_path); value['cwd']=str(tmp_path/'elsewhere')
    run(tmp_path,value); assert events(tmp_path)==[]
