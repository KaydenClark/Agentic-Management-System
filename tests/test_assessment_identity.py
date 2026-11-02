"""Exact immutable artifact identity, distinct from Python numeric equality."""
import copy
import json

import pytest
from ams import assessment, assessment_store
from test_assessment import packet
from test_assessment_store import Database

PAIRS=[(True,1),(1e20,100000000000000000000),(1.0,1),(-0.0,0.0)]


@pytest.mark.parametrize('before,after',PAIRS)
def test_changed_remote_prefix_and_duplicate_refuse_without_writes(tmp_path,before,after):
    original=packet();original['measurementMetadata']={'observed':before}
    changed=copy.deepcopy(original);changed['measurementMetadata']['observed']=after
    assessment.record(original,tmp_path/'original');assessment.record(changed,tmp_path/'changed')
    first=assessment.read_records(tmp_path/'original')[0]
    second=assessment.read_records(tmp_path/'changed')[0]
    assert assessment._encoded(first)!=assessment._encoded(second)
    db=Database();store=assessment_store.Store('https://synthetic.invalid','fixture',db)
    assert store.import_local(tmp_path/'original',is_test=True)==1
    saved=copy.deepcopy(db.rows)
    with pytest.raises(assessment.Refused,match='diverged'):
        store.import_local(tmp_path/'changed',is_test=True)
    with pytest.raises(assessment.Refused,match='immutable'):
        store.append(second,is_test=True,previous_digest=None)
    assert assessment._encoded(db.rows)==assessment._encoded(saved) and len(db.rows)==1
    assert assessment._encoded(store.read(is_test=True))==assessment._encoded([first])
    assert store.import_local(tmp_path/'original',is_test=True)==0
    assert store.append(first,is_test=True,previous_digest=None)['envelope_text']==assessment._encoded(first).decode()


@pytest.mark.parametrize('before,after',PAIRS)
def test_changed_local_duplicate_and_frozen_metadata_refuse(tmp_path,before,after):
    p=packet();p['measurementMetadata']={'observed':before}
    assessment.record(p,tmp_path/'duplicate')
    changed=copy.deepcopy(p);changed['measurementMetadata']['observed']=after
    with pytest.raises(assessment.Refused,match='immutable'):
        assessment.record(changed,tmp_path/'duplicate')
    assert len(assessment.read_records(tmp_path/'duplicate'))==1


@pytest.mark.parametrize('before,after',PAIRS)
def test_changed_frozen_metadata_refuses(tmp_path,before,after):
    p=packet();p['conditions']['syntheticFrozenFlag']=before
    assessment.record(p,tmp_path)
    candidate=copy.deepcopy(p);candidate.update(assessmentId='synthetic-candidate',attempt=1)
    candidate['conditions']['syntheticFrozenFlag']=after
    with pytest.raises(assessment.Refused,match='frozen comparison'):
        assessment.record(candidate,tmp_path)
    assert len(assessment.read_records(tmp_path))==1
    assert assessment.record(p,tmp_path)==assessment.read_records(tmp_path)[0]['result']


@pytest.mark.parametrize('field,value',[('assessmentAccepted',1),('retentionAccepted',0),('alignment',True)])
def test_typed_result_tamper_cannot_pass_replay(tmp_path,field,value):
    p=packet();assessment.record(p,tmp_path)
    file=next(tmp_path.glob('*.json'));saved=json.loads(file.read_text())
    if field=='alignment':saved['result']['alignment']['percentageDenominator']=value
    else:saved['result'][field]=value
    file.write_text(json.dumps(saved))
    with pytest.raises(assessment.Refused,match='recomputed history'):
        assessment.read_records(tmp_path)


def test_boolean_version_cannot_impersonate_approved_rubric():
    p=packet();p['rubric']['checkVersion']=True
    with pytest.raises(assessment.Refused,match='rubric'):
        assessment.score(p)


@pytest.mark.parametrize('version',[True,1.0])
def test_schema_identifier_requires_the_exact_approved_integer(version):
    p=packet();p['schema']=version
    with pytest.raises(assessment.Refused,match='schema'):
        assessment.score(p)


@pytest.mark.parametrize('before,after',PAIRS)
def test_recorded_historical_observation_cannot_change_scalar_identity(tmp_path,before,after):
    p=packet();p['historicalFindings']=[{'findingId':'historical-quality','checkId':'A01-04',
        'class':'Quality','candidate':'b'*40,'sourceRunId':'historical-run','observation':{'observed':before}}]
    assessment.record(p,tmp_path)
    saved=assessment._encoded(assessment.read_records(tmp_path))
    changed=copy.deepcopy(p);changed.update(assessmentId='changed-source',attempt=1)
    changed['historicalFindings'][0]['observation']['observed']=after
    with pytest.raises(assessment.Refused,match='historical source'):
        assessment.record(changed,tmp_path)
    assert assessment._encoded(assessment.read_records(tmp_path))==saved
