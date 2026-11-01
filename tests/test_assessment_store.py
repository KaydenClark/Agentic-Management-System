"""Private remote persistence at its import/readback seam; synthetic records only."""
import copy
import json
import threading
from urllib.parse import urlsplit, parse_qs

import pytest
from ams import assessment, assessment_store as remote
from test_assessment import packet


class Database:
    def __init__(self):
        self.rows = []
        self.calls = []
        self.lock = threading.Lock()
        self.lose_response = False

    def __call__(self, method, url, headers, body):
        q = parse_qs(urlsplit(url).query)
        p = json.loads(body) if body else None
        self.calls.append((method, q, p))
        if headers['apikey'] == 'client':
            return 401, b'{"code":"42501"}'
        if method == 'GET':
            rows = [r for r in self.rows if r['is_test'] == (q['is_test'][0] == 'eq.true')]
            if 'id' in q:
                for f in q['id']:
                    op, n = f.split('.')
                    rows = [r for r in rows if r['id'] > int(n)] if op == 'gt' else [r for r in rows if r['id'] <= int(n)]
            rows.sort(key=lambda r:r['id'], reverse=q['order'][0]=='id.desc')
            return 200, json.dumps(rows[:int(q.get('limit',['100'])[0])]).encode()
        with self.lock:
            e = p['p_row']
            for old in self.rows:
                if old['assessment_id'] == e['assessment_id']:
                    if all(old[k] == v for k,v in e.items()):
                        return 200, json.dumps(old).encode()
                    return 409, b'{"code":"PT409"}'
            history = [r for r in self.rows if r['failure_id']==e['failure_id'] and r['is_test']==e['is_test']]
            prev = history[-1]['content_digest'] if history else None
            if e['previous_digest'] != prev or e['attempt'] != len(history):
                return 409, b'{"code":"PT409"}'
            row = dict(e,id=len(self.rows)+1)
            self.rows.append(copy.deepcopy(row))
            if self.lose_response:
                self.lose_response = False
                raise OSError('lost response')
            return 200, json.dumps(row).encode()


def chain(tmp_path, count=2):
    for i in range(count):
        p=packet(); p.update(assessmentId=f'fixture-{i}',attempt=i)
        assessment.record(p,tmp_path)
    return assessment.read_records(tmp_path)


def store(db, size=1):
    return remote.Store('https://example.invalid','service',db,page_size=size)


def test_roundtrip_pagination_and_idempotent_resume(tmp_path):
    records=chain(tmp_path,3); db=Database(); s=store(db)
    assert s.import_local(tmp_path,is_test=True)==3
    assert s.read(is_test=True)==records
    assert s.import_local(tmp_path,is_test=True)==0
    assert len(db.rows)==3
    assert sum(c[0]=='GET' for c in db.calls)>6


def test_local_and_remote_tamper_refused_before_append(tmp_path):
    chain(tmp_path); db=Database(); s=store(db)
    s.import_local(tmp_path,is_test=True)
    db.rows[0]['envelope']['result']['level']='Broken'
    with pytest.raises(assessment.Refused): s.read(is_test=True)
    db.rows.clear()
    f=next(tmp_path.glob('*.json')); e=json.loads(f.read_text()); e['result']['level']='Broken';f.write_text(json.dumps(e))
    with pytest.raises(assessment.Refused): s.import_local(tmp_path,is_test=True)
    assert not db.rows


def test_divergent_prefix_and_changed_identity_refused(tmp_path):
    chain(tmp_path); db=Database(); s=store(db); s.import_local(tmp_path,is_test=True)
    other=copy.deepcopy(db.rows[0]); other['envelope']['packet']['label']='changed'
    with pytest.raises(assessment.Refused): s.append(other['envelope'],is_test=True,previous_digest=None)
    assert len(db.rows)==2
    f=next(tmp_path.glob('*.json')); e=json.loads(f.read_text());e['packet']['label']='changed';f.write_text(json.dumps(e))
    with pytest.raises(assessment.Refused): s.import_local(tmp_path,is_test=True)
    assert len(db.rows)==2


def test_partial_import_and_lost_response_retry(tmp_path):
    records=chain(tmp_path);db=Database();s=store(db)
    db.lose_response=True
    with pytest.raises(assessment.Refused): s.import_local(tmp_path,is_test=True)
    assert len(db.rows)==1
    assert s.import_local(tmp_path,is_test=True)==1
    assert s.read(is_test=True)==records


def test_stale_concurrent_append_has_one_winner(tmp_path):
    records=chain(tmp_path);db=Database();s=store(db)
    old=s.append(records[0],is_test=True,previous_digest=None)
    e=copy.deepcopy(records[1]); other=copy.deepcopy(e);other['packet']['assessmentId']='other'
    results=[]
    def append(value):
        try:s.append(value,is_test=True,previous_digest=old['content_digest']);results.append('ok')
        except assessment.Refused:results.append('refused')
    ts=[threading.Thread(target=append,args=(v,)) for v in (e,other)]
    for t in ts:t.start()
    for t in ts:t.join()
    assert sorted(results)==['ok','refused'] and len(db.rows)==2


def test_refuses_changed_scorer_marker_symlink_and_private_client(tmp_path):
    records=chain(tmp_path,1);db=Database();s=store(db);s.import_local(tmp_path,is_test=True)
    db.rows[0]['scorer_digest']='0'*64
    with pytest.raises(assessment.Refused):s.read(is_test=True)
    (tmp_path/'.record-lock').mkdir()
    with pytest.raises(assessment.Refused):s.import_local(tmp_path,is_test=True)
    client=remote.Store('https://example.invalid','client',db)
    with pytest.raises(assessment.Refused):client.read(is_test=True)


def test_findings_retests_and_recurrence_survive_roundtrip(tmp_path):
    p=packet(('A04-04',));p['runs'][0]['rows'][0]['result']='No'
    r=assessment.record(p,tmp_path);fid=r['findings'][0]['findingId']
    for i,rev,outcome in ((1,'f'*40,'Yes'),(2,'e'*40,'No'),(3,'d'*40,'Yes')):
        p.update(assessmentId=f'repair-{i}',attempt=i,candidate=rev)
        p['retests']=[{'findingId':fid,'revision':rev,'originalCheckId':'A04-04',
                      'regressionExclusionReason':'Synthetic case has no affected regressions'}]
        for run in p['runs']:
            run['rows'][0]['result']=outcome
            run['rows'][0]['evidence'][0]['revision']=rev
        p['evaluator']['qualificationEvidence'][0]['revision']=rev
        assessment.record(p,tmp_path)
    db=Database();s=store(db);s.import_local(tmp_path,is_test=True)
    saved=s.read(is_test=True)
    assert [e['result']['findings'][0]['status'] for e in saved]==['open','verified-resolved','recurred','verified-resolved']
    assert saved[-1]['result']['retentionAccepted'] is False


@pytest.mark.parametrize('change', ['reset','fourth','frozen','collision','filename','symlink'])
def test_invalid_local_history_never_writes_remote(tmp_path,change):
    chain(tmp_path); files=list(tmp_path.glob('*.json'));f=files[0];e=json.loads(f.read_text())
    if change=='reset':e['packet']['attempt']=0
    elif change=='fourth':e['packet']['attempt']=4
    elif change=='frozen':e['packet']['conditions']['effort']='changed'
    elif change=='collision':e['packet']['assessmentId']='fixture-0'
    elif change=='filename':f.rename(tmp_path/'wrong.json')
    else:
        original=f.read_text();f.unlink();target=tmp_path/'outside';target.write_text(original);f.symlink_to(target)
    if change not in ('filename','symlink'):
        # Recompute standalone totals so replay must challenge history, not just a stale digest.
        if change not in ('fourth',):
            e['result']=assessment.score(e['packet'])
            e['result'].update(attempt=e['packet']['attempt'],nextAction='revise')
        f.write_text(json.dumps(e))
    db=Database()
    with pytest.raises(assessment.Refused):store(db).import_local(tmp_path,is_test=True)
    assert not db.rows


def test_cli_outputs_counts_without_private_packet(monkeypatch,tmp_path,capsys):
    from test_rsi_rows import FAKE_SECRET
    p=packet();p['conditions']['host']='private-probe-only';p['privateNote']='never-print-this-packet'
    assessment.record(p,tmp_path)
    db=Database();s=store(db)
    monkeypatch.setattr(remote.keycheck,'load_settings',lambda:remote.keycheck.Settings('https://example.invalid',FAKE_SECRET))
    monkeypatch.setattr(remote,'Store',lambda *a,**k:s)
    assert remote.main(['import','--store',str(tmp_path),'--test'])==0
    output=capsys.readouterr()
    assert 'verified private assessments: 1' in output.out
    assert 'private-probe-only' not in output.out and 'never-print-this-packet' not in output.out
    assert not output.err
