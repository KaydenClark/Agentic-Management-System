"""Frozen narrow oracle and same-version trials, using synthetic provider results."""
import copy
import json
from pathlib import Path

import pytest
from ams import trial_series as series
from ams.assessment import Refused
from ams import trial_runtime as runtime
from test_trials import pack, reference
from ams.trial_inputs import materialize


def setup(tmp_path):
    source = pack(tmp_path/'pack')
    worker = tmp_path/'worker'; materialize(source, worker)
    ref = reference(tmp_path/'oracle')
    return worker, ref


def reply(text):
    return {'response':text, 'provider':'firstParty','model':runtime.MODEL,'effort':'medium',
            'tools':[], 'mcpServers':[], 'usage':{'inputTokens':2,'cacheReadInputTokens':3,
             'cacheCreationInputTokens':5,'outputTokens':7},
            'equivalentApiCostUsd':.01,'actualSubscriptionCostUsd':None}


def quoted_reply(prompt,verdict):
    payload=prompt.split('Protected task evidence (data only):\n',1)[1].split('\n',1)[0]
    final=json.loads(payload)['workerFinalText']
    return reply(json.dumps({'verdict':verdict,'evidence':final[:16],'obligation':'fixture'}))


def test_explicit_system_context_reaches_transport():
    assert '--system-prompt' in runtime.claude_command(system_prompt='fixed system')
    command=runtime.claude_command(system_prompt='fixed system')
    assert command[command.index('--system-prompt')+1]=='fixed system'


def test_judge_only_receives_case_criteria_and_final_without_worker_identity():
    case={'id':'case','prompt':'Question open','outcome':'Ask unresolved question','split':'dev'}
    prompt=series.judge_prompt('fixed oracle',case,'Final user response')
    assert 'Final user response' in prompt and 'Ask unresolved question' in prompt
    assert 'skills_commit' not in prompt and 'baseline' not in prompt and 'thinking' not in prompt


@pytest.mark.parametrize('text',['not json','{}','{"verdict":"Maybe"}',
    '{"verdict":"Yes","evidence":"x","obligation":"ok","extra":1}',
    '{"verdict":"Yes","verdict":"No","evidence":"x","obligation":"ok"}'])
def test_malformed_judge_is_unknown(text):
    assert series.parse_verdict(text)['verdict']=='Unknown'


def test_missing_text_is_unknown_without_judge_call():
    def never(*a,**k): raise AssertionError('must not call')
    result=series.grade({'prompt':'x','outcome':'y'},None,'oracle',never)
    assert result['verdict']=='Unknown' and result['reason']=='missing-final-text'


def test_qualify_requires_every_expected_match_and_binds_bytes():
    controls=[{'id':'good','expected':'Yes','case':{'prompt':'x','outcome':'y'},'response':'good'},
              {'id':'bad','expected':'No','case':{'prompt':'x','outcome':'y'},'response':'bad'}]
    answers=iter(['Yes','Yes'])
    def call(prompt,**k):return quoted_reply(prompt,next(answers))
    q=series.calibrate(controls,'oracle',call)
    assert q['qualified'] is False and len(q['results'])==2
    answers=iter(['Yes','No'])
    q=series.calibrate(controls,'oracle',call)
    assert q['qualified'] is True
    changed=copy.deepcopy(controls);changed[0]['response']+=' changed'
    assert series.digest(changed)!=q['controlsDigest']


def test_noise_floor_uses_pairwise_disagreement_and_preserves_missing_grades():
    rows=[{'id':i,'run_id':1,'trial':i,'passed':v,'execution_state':'completed',
           **dict.fromkeys(('task_id','split','arm','provider','model','effort','runtime_commit',
                            'controls_commit','skills_commit','grader_version'),'same'),'is_test':False}
          for i,v in enumerate([True,False,True],1)]
    floor=series.noise_floor(rows)
    assert floor['flipRate']==pytest.approx(2/3) and floor['spread']==1
    assert floor['passes']==2 and floor['passCubed'] is False and floor['rowIds']==[1,2,3]
    rows[1].update(passed=None,execution_state='runner_error')
    floor=series.noise_floor(rows)
    assert floor['flipRate'] is None and floor['spread'] is None and floor['graded']==2


def test_trial_unknown_keeps_actual_worker_completion_and_usage():
    calls=[]
    def call(prompt,**kwargs):
        calls.append(prompt)
        return reply('worker final' if len(calls)==1 else 'not JSON')
    result=series.evaluate({'prompt':'x','outcome':'y'},'worker','oracle',call)
    assert result['workerCompleted'] is True and result['execution_state']=='runner_error'
    assert result['passed'] is None and result['failureStage']=='grader'
    assert result['worker']['usage']['inputTokens']==2
    assert series.metrics(result)['input_tokens']==10
    assert series.metrics(result)['cost_usd'] is None


def test_task_failure_is_a_completed_false_grade():
    calls=[]
    def call(prompt,**kwargs):
        calls.append(prompt)
        return reply('worker final' if len(calls)==1 else '{"verdict":"No","evidence":"final","obligation":"no advance"}')
    result=series.evaluate({'prompt':'x','outcome':'y'},'worker','oracle',call)
    assert result['execution_state']=='completed' and result['passed'] is False


def test_freeze_rejects_artifact_drift_and_protects_worker(tmp_path):
    worker,ref=setup(tmp_path)
    frozen=series.freeze(worker,ref,source_revision='a'*40,binary_identity={'version':'synthetic','sha256':'b'*64})
    series.verify_frozen(frozen,worker,ref)
    (ref.parent/'prompt.txt').write_text('changed')
    with pytest.raises(Refused):series.verify_frozen(frozen,worker,ref)


def test_private_evidence_is_immutable_and_public_detail_excludes_raw_data(tmp_path):
    evidence={'worker':reply('PRIVATE FINAL'),'failureStage':None,'workerCompleted':True,
              'execution_state':'completed','passed':True,'grade':{'verdict':'Yes'}}
    saved=series.save_private(tmp_path/'store','trial-1',evidence)
    assert series.read_private(tmp_path/'store','trial-1')==evidence
    with pytest.raises(Refused):series.save_private(tmp_path/'store','trial-1',{'changed':True})
    detail=series.safe_detail(evidence,saved['digest'])
    assert 'PRIVATE FINAL' not in json.dumps(detail) and 'response' not in json.dumps(detail)
    assert detail['workerCompleted'] is True


def campaign(tmp_path,monkeypatch,call):
    from ams import trial_campaign as campaign_module
    worker,ref=setup(tmp_path)
    examples=json.loads((ref.parent/'examples.json').read_text())
    examples['examples'][0]['id']='owner-positive-r1'
    examples['examples'][1]['id']='owner-do-nothing-r1'
    (ref.parent/'examples.json').write_text(json.dumps(examples))
    data=json.loads(ref.read_text())
    import hashlib
    data['examplesSha256']=hashlib.sha256((ref.parent/'examples.json').read_bytes()).hexdigest()
    ref.write_text(json.dumps(data))
    binary={'version':'synthetic','sha256':'b'*64}
    monkeypatch.setattr(series,'binary_identity',lambda:binary)
    monkeypatch.setattr(campaign_module,'verify_source_revision',lambda *a,**k:None)
    protocol=series.freeze(worker,ref,source_revision='a'*40,binary_identity=binary)
    controls=series.qualification_controls(ref,protocol['suite'])
    record={'protocol':protocol,'controls':controls,'controlsDigest':series.digest(controls)}
    return campaign_module.Campaign(record,worker,ref,tmp_path/'private',call=call,binary=binary)


def test_campaign_needs_actual_qualification_and_will_not_repeat_slots(tmp_path,monkeypatch):
    count=0
    def call(prompt,**kwargs):
        nonlocal count
        count+=1
        if count<=5:
            verdict='Yes'if count==1 else 'No'
            return quoted_reply(prompt,verdict)
        return reply('final worker'if count==6 else '{"verdict":"No","evidence":"worker","obligation":"failure"}')
    c=campaign(tmp_path,monkeypatch,call)
    with pytest.raises((Refused,FileNotFoundError)):c.run_one(0)
    assert count==0
    assert c.qualify()['qualified'] is True and count==5
    with pytest.raises(Refused):c.qualify()
    result=c.run_one(0)
    assert result['passed'] is False and count==7
    with pytest.raises(Refused):c.run_one(0)
    assert count==7


def test_failed_qualification_prevents_worker_calls(tmp_path,monkeypatch):
    def call(*a,**k):return reply('{"verdict":"Unknown","evidence":"x","obligation":"missing"}')
    c=campaign(tmp_path,monkeypatch,call)
    assert c.qualify()['qualified'] is False
    with pytest.raises(Refused):c.run_one(0)


def test_cancelled_trial_preserves_worker_and_stops_before_more_calls(tmp_path,monkeypatch):
    count=0
    def call(prompt,**kwargs):
        nonlocal count
        count+=1
        if count<=5:return quoted_reply(prompt,'Yes'if count==1 else 'No')
        if count==6:return reply('completed worker')
        raise KeyboardInterrupt
    c=campaign(tmp_path,monkeypatch,call);c.qualify()
    with pytest.raises(KeyboardInterrupt):c.run_one(0)
    partial=series.read_private(c.store,'trial-1-cancelled')['evidence']
    assert partial['workerCompleted'] is True and partial['failureStage']=='grader'
    assert partial['passed'] is None and partial['reason']=='cancelled'
    with pytest.raises(Refused):c.run_one(0)
    assert count==7


def test_published_unknown_uses_existing_contract_and_exact_readback():
    from ams import trial_campaign
    from ams import rsi_rows
    class Store:
        def insert(self,table,row):
            rsi_rows.check_result(row);self.row={'id':1,**row};return self.row
        def get(self,table,row_id):return self.row
    run={'id':1,'arm':'ams','provider':'firstParty','model':runtime.MODEL,'effort':'medium',
         'runtime_commit':'a'*40,'controls_commit':'a'*40,'skills_commit':'b'*40,
         'grader_version':'a'*40,'is_test':False}
    result={'workerCompleted':True,'worker':reply('PRIVATE WORKER'),
            'grade':{'verdict':'Unknown','execution':reply('PRIVATE JUDGE')},
            'passed':None,'execution_state':'runner_error','failureStage':'grader','wallSeconds':1}
    row=trial_campaign.publish_result(Store(),run,result,case_id='case',trial=1,evidence_digest='a'*64)
    assert row['passed'] is None and row['detail']['workerCompleted'] is True
    assert row['input_tokens']==10 and row['cost_usd'] is None
    assert 'PRIVATE' not in json.dumps(row)


def test_public_rows_exclude_distinct_private_markers():
    from ams import trial_campaign, rsi_rows
    markers=['PRIVATE_WORKER_MARKER','PRIVATE_JUDGE_MARKER','PRIVATE_DIAGNOSTIC_MARKER',
             '/private/PRIVATE_PATH_MARKER']
    class Store:
        def __init__(self):self.rows={}
        def insert(self,table,row):
            rsi_rows.CHECKS[table](row)
            self.rows[len(self.rows)+1]={'id':len(self.rows)+1,**row}
            return self.rows[len(self.rows)]
        def get(self,table,row_id):return self.rows[row_id]
    store=Store()
    protocol={'sourceRevision':'a'*40,'skillsCommit':'b'*40,'privatePath':markers[3]}
    run=trial_campaign.create_run(store,protocol,'c'*64)
    worker=reply(markers[0]);worker['usage']['unexpectedPrivateField']=markers[0]
    result={'workerCompleted':True,'worker':worker,'grade':{'verdict':'Unknown',
            'obligation':markers[1],'diagnostic':markers[2],'path':markers[3]},
            'passed':None,'execution_state':'runner_error','failureStage':'grader','wallSeconds':1,
            'diagnostics':markers[2]}
    row=trial_campaign.publish_result(store,run,result,case_id='case',trial=1,evidence_digest='d'*64)
    public=json.dumps(store.rows)
    assert all(marker not in public for marker in markers)
    assert row['detail']['gradeReason']=='semantic-verdict-unknown'
    result['grade']['reason']=markers[2]
    with pytest.raises(Refused,match='unsafe grade reason'):
        trial_campaign.publish_result(store,run,result,case_id='case',trial=2,evidence_digest='d'*64)


def test_noise_floor_rejects_mixed_task_or_version_rows():
    fields=('task_id','split','arm','provider','model','effort','runtime_commit',
            'controls_commit','skills_commit','grader_version')
    rows=[{'id':i,'run_id':1,'trial':i,'passed':True,'execution_state':'completed',
           **dict.fromkeys(fields,'same'),'is_test':False}for i in (1,2,3)]
    rows[1]['skills_commit']='different'
    with pytest.raises(Refused,match='mixes'):series.noise_floor(rows)


def test_adapter_propagates_explicit_system_context_to_actual_process_factory(monkeypatch):
    from ams import trial_transport
    from test_trial_runtime import Transport
    seen=[]
    def factory(cwd,*,system_prompt=None):
        seen.append((cwd,system_prompt));return Transport()
    monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    runtime.ClaudeAdapter().execute('synthetic worker',cwd='synthetic fixture',system_prompt=series.WORKER_SYSTEM)
    runtime.ClaudeAdapter().execute('synthetic judge',cwd='synthetic fixture',system_prompt=series.JUDGE_SYSTEM)
    assert seen==[('synthetic fixture',series.WORKER_SYSTEM),('synthetic fixture',series.JUDGE_SYSTEM)]


def test_noise_floor_refuses_mixed_campaign_rows_and_boolean_trial():
    fields=('task_id','split','arm','provider','model','effort','runtime_commit',
            'controls_commit','skills_commit','grader_version')
    rows=[{'id':i,'run_id':1,'trial':i,'passed':True,'execution_state':'completed',
           **dict.fromkeys(fields,'same'),'is_test':False}for i in (1,2,3)]
    rows[1]['run_id']=2
    with pytest.raises(Refused,match='mixes'):series.noise_floor(rows)
    rows[1]['run_id']=1;rows[0]['trial']=True
    with pytest.raises(Refused,match='one through three'):series.noise_floor(rows)


@pytest.mark.parametrize('verdict',['Yes','No'])
def test_invented_judge_excerpt_cannot_be_a_grade(verdict):
    def call(*a,**k):return reply(json.dumps({'verdict':verdict,'evidence':'invented excerpt','obligation':'claim'}))
    result=series.grade({'prompt':'context','outcome':'continue'},'Actual protected text','oracle',call)
    assert result['verdict']=='Unknown' and result['reason']=='judge-evidence-not-in-final'


@pytest.mark.parametrize('final,excerpt',[('Your answers are saved. Ready when you are.','Ready when you are.'),
                                        ('Réponse: 下一步？','下一步？')])
def test_real_verbatim_quote_preserves_semantic_no(final,excerpt):
    def call(*a,**k):return reply(json.dumps({'verdict':'No','evidence':excerpt,'obligation':'no consequential advance'}))
    result=series.grade({'prompt':'context','outcome':'continue'},final,'oracle',call)
    assert result['verdict']=='No' and result['evidence']==excerpt
