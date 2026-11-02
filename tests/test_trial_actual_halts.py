"""Actual role adapters, inert wire packets, protected halted-attempt readback."""
import json
import pytest
from ams import trial_judge,trial_series as series,trial_transport,trial_campaign,rsi_rows
from ams.assessment import Refused
from test_trial_runtime import Transport,events as worker_events
from test_trial_judge import events as judge_events
from test_trial_series import campaign,quoted_reply

MARKERS=('ACTUAL_HALT_WORKER','ACTUAL_HALT_RATIONALE','ACTUAL_HALT_DIAGNOSTIC',
         '/private/ACTUAL_HALT_PATH')


class WireFactory:
    def __init__(self,phase,fault):self.phase=phase;self.fault=fault;self.streams=[];self.campaign=None
    def __call__(self,cwd,**kwargs):
        role='judge'if kwargs.get('structured_output',False)else'worker'
        number=len(self.streams)+1
        target=(self.phase=='qualification'and number==1 or self.phase=='worker'and number==6
                or self.phase=='grader'and number==7)
        factory=self
        class Wire(Transport):
            def failure_diagnostic(self,*args):
                return {'pointer':MARKERS[3],'cause':MARKERS[2],
                        'worker':MARKERS[0],'rationale':MARKERS[1]}
            def responses(self,prompt):
                self.prompts.append(prompt)
                if role=='judge':
                    packets=judge_events()
                    value=json.loads(quoted_reply(prompt,'Yes'if number in (1,7)else'No')['response'])
                    value['obligation']=MARKERS[1]
                    packets[1]['message']['content'][0]['input']=value
                    packets[-1]['structured_output']=value
                    packets[-1]['result']=MARKERS[2]+MARKERS[3]
                else:
                    packets=worker_events();text='|'.join(MARKERS)
                    packets[1]['message']['id']='worker-message-1'
                    packets[1]['message']['content'][0]['text']=text;packets[-1]['result']=text
                if target and factory.fault=='partial-interrupt':
                    yield from packets[:2]
                    raise KeyboardInterrupt
                yield from packets
                if target and factory.fault=='terminal-interrupt':raise KeyboardInterrupt
                if target and factory.fault=='post-return-drift':
                    (factory.campaign.execution/'unexpected').write_text('preserve')
        stream=Wire();stream.role=role;stream.cwd=cwd;self.streams.append(stream);return stream


@pytest.mark.parametrize('phase',['qualification','worker','grader'])
@pytest.mark.parametrize('fault',['partial-interrupt','terminal-interrupt','post-return-drift'])
def test_actual_adapters_preserve_halted_facts_without_grade_or_next_query(tmp_path,monkeypatch,phase,fault):
    factory=WireFactory(phase,fault);monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    c=campaign(tmp_path,monkeypatch,trial_judge.InterviewAdapter().execute);factory.campaign=c
    if phase!='qualification':assert c.qualify()['qualified']
    with pytest.raises(KeyboardInterrupt):c.qualify()if phase=='qualification'else c.run_one(0)
    identity='qualification-owner-positive-r1'if phase=='qualification'else'trial-1-cancelled'
    row=series.read_private(c.store,identity)['evidence'];private=row['privateDiagnostic']
    assert private==c.last_failure
    assert row['ownerCancellation']is(fault!='post-return-drift')
    assert row['reason']==('runtime-refused'if fault=='post-return-drift'else'cancelled')
    if fault=='partial-interrupt':
        assert private['observedProviderTurns']==1 and private['turnCountComplete']is False
        assert private.get('serializationCalls',0)==(0 if phase=='worker'else 1)
        assert private['terminalExecution']is None
        assert all(marker in json.dumps(private)for marker in MARKERS)
    else:
        available=private['availableExecution']
        assert available['role']==('worker'if phase=='worker'else'judge')
        assert available['returned']is(fault=='post-return-drift')
        assert available['execution']['usage']['inputTokens']==2
        assert available['execution']['actualSubscriptionCostUsd']is None
        if phase!='worker':assert available['execution']['structuredOutput']['verdict']=='Yes'
    expected={'qualification':1,'worker':6,'grader':7}[phase]
    assert len(factory.streams)==expected and all(s.closed for s in factory.streams)
    assert all(s.cwd==c.execution for s in factory.streams)
    if phase=='qualification':
        assert row['verdict']=='Unknown' and not (c.store/'qualification-final.json').exists()
        with pytest.raises(Refused):c.qualify()
    else:
        assert row['passed']is None and row['execution_state']=='runner_error' and row['grade']is None
        assert row['workerCompleted']is(phase=='grader'or fault=='post-return-drift')
        measured=phase=='grader'or fault!='partial-interrupt'
        assert (row['worker']is not None)is measured
        metrics=series.metrics(row)
        assert (metrics['input_tokens']is not None)is measured
        assert metrics['cost_usd']is None
        assert not (c.store/'trial-1-result.json').exists()
        _assert_public_privacy(row)
        with pytest.raises(Refused):c.run_one(0)
        with pytest.raises(Refused if fault=='post-return-drift'else FileNotFoundError):c.run_one(1)
    assert len(factory.streams)==expected
    if fault=='post-return-drift':assert (c.execution/'unexpected').read_text()=='preserve'


def _assert_public_privacy(result):
    class Store:
        def __init__(self):self.rows={}
        def insert(self,table,value):
            rsi_rows.CHECKS[table](value);row={'id':len(self.rows)+1,**value}
            self.rows[row['id']]=row;return row
        def get(self,table,identity):return self.rows[identity]
    store=Store();run=trial_campaign.create_run(store,{'sourceRevision':'a'*40,'skillsCommit':'b'*40},'c'*64)
    row=trial_campaign.publish_result(store,run,result,case_id='case',trial=1,evidence_digest='d'*64)
    assert row['passed']is None and row['detail']['gradeState']=='unknown'
    public=json.dumps(store.rows)
    assert all(marker not in public for marker in MARKERS)
