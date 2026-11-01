"""Deterministic S-002 contract tests, using synthetic evidence only."""
import copy
import json
from pathlib import Path

import pytest

from ams import assessment

REV = 'a' * 40
BASE = 'b' * 40
RUBRIC = {'revision': 'r1', 'sha256': '96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578', 'checkVersion': 1}


def evidence(revision=REV):
    return [{'type': 'behavioral-test', 'revision': revision, 'locator': 'synthetic:test-known-outcome'}]


def packet(ids=('A04-01',)):
    return {
        'schema': 1, 'assessedAt': '2026-11-01T18:00:00Z', 'assessmentId': 'test-baseline', 'failureId': 'synthetic-failure',
        'attempt': 0, 'scope': 'bounded', 'rubric': dict(RUBRIC),
        'candidate': REV, 'baseline': BASE, 'skillsCommit': 'c' * 40,
        'inventoryRevision': 'd' * 40, 'excludedChecks': {k: 'Outside this synthetic fixture' for k in assessment.CHECKS if k not in ids},
        'conditions': {'host': 'synthetic', 'tools': ['pytest'], 'workerModel': 'fixture-v1', 'effort': 'fixed', 'loadedArtifacts': ['synthetic:skill@' + 'c'*40]},
        'evaluator': {'model': 'deterministic-fixture-v1', 'promptRevision': 'e'*40, 'qualification': 'qualified', 'qualificationEvidence': evidence()},
        'inventory': [{'id': k, 'class': assessment.CHECKS[k]} for k in ids],
        'runs': [{'runId': f'run-{i}', 'rows': [{'id': k, 'result': 'Yes', 'qualification': 'qualified', 'evidence': evidence()} for k in ids]} for i in range(3)],
        'retests': [], 'historicalFindings': [],
    }


def regression_packet():
    p = packet()
    p['inventory'][0].update({'class': 'Regression', 'baselineEvidence': [dict(item, result='Yes', qualification='qualified') for item in evidence(BASE)]})
    return p


def test_exact_pooled_counts_instead_of_average_percentages():
    ids = tuple(k for k,v in assessment.CHECKS.items() if v == 'Quality')[:10]
    p = packet(ids)
    for n, run in enumerate(p['runs']):
        for i, row in enumerate(run['rows']):
            if n and i >= 2:
                row.update(result='N/A', reason='Not applicable in this run')
            elif i >= (8 if n == 0 else 1):
                row['result'] = 'No'
    r = assessment.score(p)
    assert r['alignment'] == {'passed': 10, 'applicable': 14, 'percentageNumerator': 500, 'percentageDenominator': 7}
    assert r['level'] == 'Excellent'  # Quality failures alone do not fail runs.
    assert r['assessmentAccepted'] is True
    assert r['scope'] == 'bounded' and r['retentionAccepted'] is False


@pytest.mark.parametrize('passing,level', [(0,'Broken'), (1,'Functional'), (2,'Stable'), (3,'Excellent')])
def test_all_levels(passing, level):
    p = regression_packet()
    for run in p['runs'][passing:]:
        run['rows'][0]['result'] = 'No'
    r = assessment.score(p)
    assert r['level'] == level and r['passingRuns'] == passing
    assert r['assessmentAccepted'] is (passing == 3)  # unresolved Regression remains open


def test_critical_overrides_two_passing_runs():
    p = packet(('A04-04',))
    p['runs'][0]['rows'][0]['result'] = 'No'
    r = assessment.score(p)
    assert r['passingRuns'] == 2 and r['level'] == 'Broken'
    assert not r['assessmentAccepted']


@pytest.mark.parametrize('outcome', ['Unknown', 'Unrun', 'refused', 'interrupted'])
def test_unknown_and_missing_proof_remain_no(outcome):
    p = packet(('A04-04',))
    p['runs'][0]['rows'][0].update(result=outcome, evidence=[])
    r = assessment.score(p)
    assert r['alignment']['applicable'] == 3 and r['alignment']['passed'] == 2
    assert r['level'] == 'Broken' and r['evidenceState'] == 'incomplete'


def test_omitted_row_and_empty_yes_evidence_cannot_pass():
    p = packet(('A04-04',))
    p['runs'][0]['rows'] = []
    p['runs'][1]['rows'][0]['evidence'] = []
    r = assessment.score(p)
    assert r['alignment']['passed'] == 1 and r['alignment']['applicable'] == 3
    assert not r['assessmentAccepted']


def test_empty_inventory_has_no_percentage_or_acceptance():
    r = assessment.score(packet(()))
    assert r['alignment'] == {'passed': 0, 'applicable': 0, 'percentageNumerator': None, 'percentageDenominator': None}
    assert not r['assessmentAccepted']


@pytest.mark.parametrize('mutation', [
    lambda p: p['inventory'][0].update({'class':'Quality'}),
    lambda p: p['inventory'][0].update({'id':'invented'}),
    lambda p: p['rubric'].update({'checkVersion':2}),
    lambda p: p.update(scope='whole'),
    lambda p: p['runs'].append(copy.deepcopy(p['runs'][0])),
    lambda p: p['runs'][0]['rows'][0].update(result='N/A'),
    lambda p: p['runs'][0]['rows'].append(copy.deepcopy(p['runs'][0]['rows'][0])),
    lambda p: p['runs'][0]['rows'][0]['evidence'][0].update(revision=BASE),
])
def test_malformed_or_misrepresented_assessments_are_refused(mutation):
    p = packet(('A04-04',))
    mutation(p)
    with pytest.raises(assessment.Refused):
        assessment.score(p)


def test_regression_requires_baseline_pass_proof():
    p = regression_packet()
    del p['inventory'][0]['baselineEvidence']
    with pytest.raises(assessment.Refused, match='baseline'):
        assessment.score(p)


def test_unqualified_result_keeps_score_but_cannot_be_accepted():
    p = packet()
    p['evaluator']['qualification'] = 'unqualified'
    r = assessment.score(p)
    assert r['alignment']['passed'] == 3 and r['level'] == 'Excellent'
    assert r['qualification'] == 'unqualified' and not r['assessmentAccepted']


def test_baseline_zero_and_three_failures_then_stop_even_after_rename(tmp_path):
    p = packet(('A04-04',))
    p['runs'][0]['rows'][0]['result'] = 'No'
    assessment.record(p, tmp_path)
    for i in range(1,4):
        p.update(assessmentId=f'candidate-{i}', attempt=i, candidate=str(i)*40, label=f'renamed-{i}')
        for run in p['runs']:
            run['rows'][0]['evidence'] = evidence(str(i)*40)
        p['evaluator']['qualificationEvidence'] = evidence(str(i)*40)
        r = assessment.record(p, tmp_path)
        assert r['nextAction'] == ('stop' if i == 3 else 'revise')
    p.update(assessmentId='renamed-again', attempt=1)
    with pytest.raises(assessment.Refused, match='three|attempt'):
        assessment.record(p, tmp_path)
    assert len(list(tmp_path.glob('*.json'))) == 4


def test_immutable_retry_and_readback(tmp_path):
    p = packet()
    r = assessment.record(p, tmp_path)
    assert assessment.read_records(tmp_path)[0]['result'] == r
    assert assessment.record(p, tmp_path) == r
    p['runs'][0]['rows'][0]['result'] = 'No'
    with pytest.raises(assessment.Refused, match='immutable'):
        assessment.record(p, tmp_path)


def test_omission_does_not_close_findings_and_three_run_retest_does(tmp_path):
    p = packet(('A04-01', 'A04-02'))
    p['runs'][0]['rows'][0]['result'] = 'No'
    initial = assessment.record(p, tmp_path)
    fid = initial['findings'][0]['findingId']
    p.update(assessmentId='candidate-1', attempt=1, candidate='f'*40)
    for run in p['runs']:
        for row in run['rows']:
            row.update(result='Yes', evidence=evidence('f'*40))
    p['evaluator']['qualificationEvidence'] = evidence('f'*40)
    r = assessment.record(p, tmp_path)
    assert r['findings'][0]['status'] == 'open'
    p.update(assessmentId='candidate-2', attempt=2)
    p['retests'] = [{'findingId': fid, 'revision': 'f'*40, 'originalCheckId': 'A04-01', 'regressionCheckIds': ['A04-02']}]
    r = assessment.record(p, tmp_path)
    assert r['findings'][0]['status'] == 'verified-resolved'
    p.update(assessmentId='candidate-3', attempt=3)
    p['retests'] = []
    p['runs'][0]['rows'][0]['result'] = 'No'
    r = assessment.record(p, tmp_path)
    assert r['findings'][0]['status'] == 'recurred'


def test_original_pass_regression_fail_cannot_close(tmp_path):
    p = packet(('A04-01','A04-02'))
    p['runs'][0]['rows'][0]['result'] = 'No'
    fid = assessment.record(p,tmp_path)['findings'][0]['findingId']
    p.update(assessmentId='candidate-1',attempt=1)
    for run in p['runs']:
        run['rows'][0]['result'] = 'Yes'
    p['runs'][2]['rows'][1]['result'] = 'No'
    p['retests'] = [{'findingId':fid,'revision':REV,'originalCheckId':'A04-01','regressionCheckIds':['A04-02']}]
    r = assessment.record(p,tmp_path)
    assert r['findings'][0]['status'] == 'open'
    assert len(r['findings']) == 2 and r['rejectedRetests']


def test_cli_good_bad_and_do_nothing(tmp_path, capsys):
    source = tmp_path/'packet.json'
    p = packet()
    source.write_text(json.dumps(p))
    assert assessment.main(['score', str(source)]) == 0
    assert json.loads(capsys.readouterr().out)['assessmentAccepted']
    p['runs'] = [{'runId': f'run-{i}', 'rows': []} for i in range(3)]
    source.write_text(json.dumps(p))
    assert assessment.main(['record', str(source), '--store', str(tmp_path/'store')]) == 0
    assert not json.loads(capsys.readouterr().out)['assessmentAccepted']
    source.write_text('{}')
    assert assessment.main(['score', str(source)]) == 1
    assert 'refused' in capsys.readouterr().err


def test_zero_score_preserves_exact_zero_ratio():
    p = packet()
    for run in p['runs']:
        run['rows'][0]['result'] = 'No'
    assert assessment.score(p)['alignment'] == {'passed':0,'applicable':3,'percentageNumerator':0,'percentageDenominator':1}


def test_changed_grader_cannot_reset_attempt_series(tmp_path):
    p = packet()
    assessment.record(p,tmp_path)
    p.update(assessmentId='new-name',attempt=1)
    p['evaluator']['model'] = 'changed-judge'
    with pytest.raises(assessment.Refused,match='frozen'):
        assessment.record(p,tmp_path)


def test_locked_store_refuses_without_writing(tmp_path):
    (tmp_path/'.record-lock').mkdir()
    with pytest.raises(assessment.Refused,match='locked'):
        assessment.record(packet(),tmp_path)
    assert not list(tmp_path.glob('*.json'))


def test_edited_totals_are_not_trusted_on_readback(tmp_path):
    assessment.record(packet(),tmp_path)
    file = next(tmp_path.glob('*.json'))
    raw = json.loads(file.read_text())
    raw['result']['level'] = 'Broken'
    file.write_text(json.dumps(raw))
    with pytest.raises(assessment.Refused,match='recomputed'):
        assessment.read_records(tmp_path)


def test_historical_unmapped_finding_blocks_acceptance():
    p = packet()
    p['historicalFindings'] = [{'findingId':'old-unmapped','observation':'missing class mapping'}]
    assert not assessment.score(p)['assessmentAccepted']


def test_regression_baseline_locator_without_pass_is_insufficient():
    p = regression_packet()
    p['inventory'][0]['baselineEvidence'][0]['result'] = 'No'
    with pytest.raises(assessment.Refused,match='baseline'):
        assessment.score(p)


def test_unknown_model_cannot_claim_qualification():
    p = packet()
    p['evaluator']['model'] = 'unknown'
    with pytest.raises(assessment.Refused,match='exact model'):
        assessment.score(p)


def test_historical_class_without_check_mapping_still_blocks_acceptance():
    p = packet()
    p['historicalFindings'] = [{'findingId':'unmapped-quality','class':'Quality'}]
    assert not assessment.score(p)['assessmentAccepted']


def test_recurrence_needs_repair_after_its_latest_failed_revision(tmp_path):
    p = packet(('A04-04',))
    p['runs'][0]['rows'][0]['result'] = 'No'
    fid = assessment.record(p,tmp_path)['findings'][0]['findingId']
    p.update(assessmentId='fix-one',attempt=1,candidate='f'*40)
    for run in p['runs']:
        run['rows'][0].update(result='Yes',evidence=evidence('f'*40))
    p['evaluator']['qualificationEvidence'] = evidence('f'*40)
    p['retests'] = [{'findingId':fid,'revision':'f'*40,'originalCheckId':'A04-04',
                    'regressionExclusionReason':'No other workflow in this synthetic fixture'}]
    assert assessment.record(p,tmp_path)['findings'][0]['status']=='verified-resolved'
    p.update(assessmentId='recurrence',attempt=2)
    p['retests']=[]
    p['runs'][0]['rows'][0]['result']='No'
    assert assessment.record(p,tmp_path)['findings'][0]['status']=='recurred'
    p.update(assessmentId='same-revision-retry',attempt=3)
    p['runs'][0]['rows'][0]['result']='Yes'
    p['retests'] = [{'findingId':fid,'revision':'f'*40,'originalCheckId':'A04-04',
                    'regressionExclusionReason':'No affected regression'}]
    r=assessment.record(p,tmp_path)
    assert r['findings'][0]['status']=='recurred'
    assert not r['assessmentAccepted'] and r['nextAction']=='stop'


def test_retained_unmapped_finding_can_be_enriched_then_retested(tmp_path):
    p = packet(('A04-04',))
    original = {'findingId':'legacy','candidate':BASE,'sourceRunId':'legacy-run',
                'observation':'Original failure, preserve exact description'}
    p['historicalFindings'] = [dict(original)]
    assessment.record(p,tmp_path)
    p.update(assessmentId='mapping-only',attempt=1,candidate='f'*40)
    for run in p['runs']:
        run['rows'][0]['evidence']=evidence('f'*40)
    p['evaluator']['qualificationEvidence']=evidence('f'*40)
    p['historicalFindings']=[dict(original,checkId='A04-04',**{'class':'Critical'})]
    mapped=assessment.record(p,tmp_path)
    finding=next(f for f in mapped['findings'] if f['findingId']=='legacy')
    assert finding['checkId']=='A04-04' and finding['class']=='Critical'
    assert finding['status']=='open' and not mapped['assessmentAccepted']
    p.update(assessmentId='mapping-and-retest',attempt=2)
    p['retests']=[{'findingId':'legacy','revision':'f'*40,'originalCheckId':'A04-04',
                   'regressionExclusionReason':'No other workflow in this synthetic case'}]
    result=assessment.record(p,tmp_path)
    finding=next(f for f in result['findings'] if f['findingId']=='legacy')
    assert finding['status']=='verified-resolved' and result['assessmentAccepted']
    assert all(finding[k]==v for k,v in original.items())
    records=assessment.read_records(tmp_path)
    assert 'checkId' not in records[0]['packet']['historicalFindings'][0]
    p.update(assessmentId='conflicting-remap',attempt=3)
    p['historicalFindings'][0]['checkId']='A01-01'
    before=len(list(tmp_path.glob('*.json')))
    with pytest.raises(assessment.Refused,match='mapping'):
        assessment.record(p,tmp_path)
    assert len(list(tmp_path.glob('*.json')))==before


def test_partial_enrichment_is_checked_against_retained_class(tmp_path):
    p=packet()
    p['historicalFindings']=[{'findingId':'legacy','class':'Critical','candidate':BASE}]
    assessment.record(p,tmp_path)
    p.update(assessmentId='bad-mapping',attempt=1)
    p['historicalFindings']=[{'findingId':'legacy','checkId':'A04-01'}]
    with pytest.raises(assessment.Refused,match='class'):
        assessment.record(p,tmp_path)
    assert len(list(tmp_path.glob('*.json')))==1


def test_mapping_update_cannot_rewrite_original_observation(tmp_path):
    p=packet()
    p['historicalFindings']=[{'findingId':'legacy','observation':'Original observation'}]
    assessment.record(p,tmp_path)
    p.update(assessmentId='rewrite-source',attempt=1)
    p['historicalFindings']=[{'findingId':'legacy','observation':'Replacement',
                              'checkId':'A04-01','class':'Quality'}]
    with pytest.raises(assessment.Refused,match='source'):
        assessment.record(p,tmp_path)
    assert len(list(tmp_path.glob('*.json')))==1


def test_invalid_class_only_enrichment_is_refused_before_write(tmp_path):
    p=packet()
    p['historicalFindings']=[{'findingId':'legacy','candidate':BASE}]
    assessment.record(p,tmp_path)
    p.update(assessmentId='partial-mapping',attempt=1)
    p['historicalFindings']=[{'findingId':'legacy','class':'invalid-class'}]
    with pytest.raises(assessment.Refused,match='class'):
        assessment.record(p,tmp_path)
    assert len(list(tmp_path.glob('*.json')))==1
    p['historicalFindings']=[{'findingId':'legacy','checkId':'A04-01','class':'Quality'}]
    finding=assessment.record(p,tmp_path)['findings'][0]
    assert finding['class']=='Quality' and finding['status']=='open'


def test_historical_quality_id_cannot_hide_current_regression_failure(tmp_path):
    p=regression_packet()
    p['historicalFindings']=[{'findingId':'synthetic-failure:A04-01',
                              'checkId':'A04-01','class':'Quality','candidate':BASE}]
    p['runs'][0]['rows'][0]['result']='No'
    with pytest.raises(assessment.Refused,match='collid'):
        assessment.score(p)
    with pytest.raises(assessment.Refused,match='collid'):
        assessment.record(p,tmp_path)
    assert not list(tmp_path.glob('*.json'))


def test_historical_retest_needs_known_failure_revision_and_allows_missing_revision_enrichment(tmp_path):
    p=packet(('A04-04',))
    p['historicalFindings']=[{'findingId':'legacy','checkId':'A04-04','class':'Critical'}]
    assessment.record(p,tmp_path)
    p.update(assessmentId='unknown-failure-revision',attempt=1)
    p['retests']=[{'findingId':'legacy','revision':REV,'originalCheckId':'A04-04',
                   'regressionExclusionReason':'No affected regression in this synthetic case'}]
    result=assessment.record(p,tmp_path)
    assert result['findings'][0]['status']=='open' and not result['assessmentAccepted']
    p.update(assessmentId='supply-same-failure-revision',attempt=2)
    p['historicalFindings'][0]['candidate']=REV
    result=assessment.record(p,tmp_path)
    assert result['findings'][0]['candidate']==REV
    assert result['findings'][0]['status']=='open' and not result['assessmentAccepted']
    p.update(assessmentId='actual-repair',attempt=3,candidate='f'*40)
    for run in p['runs']:
        run['rows'][0]['evidence']=evidence('f'*40)
    p['evaluator']['qualificationEvidence']=evidence('f'*40)
    p['retests'][0]['revision']='f'*40
    result=assessment.record(p,tmp_path)
    assert result['findings'][0]['status']=='verified-resolved' and result['assessmentAccepted']
    records=assessment.read_records(tmp_path)
    assert 'candidate' not in records[0]['packet']['historicalFindings'][0]
