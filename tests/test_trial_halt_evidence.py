"""Private halted-attempt evidence survives exit and stays outside public rows."""
import json
import pytest
from ams import trial_series as series,trial_campaign,rsi_rows
from ams.assessment import Refused
from test_trial_series import campaign,quoted_reply,reply

MARKERS=('PRIVATE_HALT_WORKER','PRIVATE_HALT_RATIONALE','PRIVATE_HALT_DIAGNOSTIC',
         '/private/PRIVATE_HALT_PATH')


class FaultCall:
    def __init__(self,phase,owner_cancel=False):
        self.phase=phase;self.owner_cancel=owner_cancel;self.calls=0;self.last_failure=None
    def execute(self,prompt,**kwargs):
        self.calls+=1
        if self.phase!='qualification' and self.calls<=5:
            return quoted_reply(prompt,'Yes'if self.calls==1 else 'No')
        if self.phase=='grader' and self.calls==6:return reply(MARKERS[0])
        self.last_failure={'diagnostic':{'pointer':MARKERS[3],'cause':MARKERS[2],
            'response':MARKERS[0],'rationale':MARKERS[1]},'observedProviderTurns':1,
            'turnCountComplete':False,'serializationCalls':1}
        if self.owner_cancel:raise KeyboardInterrupt
        raise Refused('synthetic runtime refusal')


def halted(tmp_path,monkeypatch,phase,owner_cancel=False):
    call=FaultCall(phase,owner_cancel);c=campaign(tmp_path,monkeypatch,call.execute)
    if phase!='qualification':assert c.qualify()['qualified']
    with pytest.raises(KeyboardInterrupt):
        c.qualify()if phase=='qualification'else c.run_one(0)
    identity='qualification-owner-positive-r1'if phase=='qualification'else'trial-1-cancelled'
    row=series.read_private(c.store,identity)['evidence']
    return c,call,row


@pytest.mark.parametrize('phase',['qualification','worker','grader'])
@pytest.mark.parametrize('owner_cancel',[False,True])
def test_private_halt_preserves_exact_call_failure_and_stops(tmp_path,monkeypatch,phase,owner_cancel):
    c,call,row=halted(tmp_path,monkeypatch,phase,owner_cancel)
    assert row['privateDiagnostic']==c.last_failure
    retained=row['privateDiagnostic']if owner_cancel else row['privateDiagnostic']['runtimeDiagnostic']
    assert retained==call.last_failure
    assert retained['observedProviderTurns']==1 and retained['turnCountComplete']is False
    assert retained['serializationCalls']==1
    assert row['ownerCancellation']is owner_cancel
    assert row['reason']==('cancelled'if owner_cancel else'runtime-refused')
    expected={'qualification':1,'worker':6,'grader':7}[phase]
    assert call.calls==expected
    if phase=='qualification':
        assert row['verdict']=='Unknown' and not (c.store/'qualification-final.json').exists()
        with pytest.raises(Refused):c.qualify()
    else:
        assert row['passed']is None and row['execution_state']=='runner_error'
        assert row['workerCompleted']is(phase=='grader')
        assert not (c.store/'trial-1-result.json').exists()
        with pytest.raises(Refused):c.run_one(0)
        with pytest.raises(FileNotFoundError):c.run_one(1)
    assert call.calls==expected


@pytest.mark.parametrize('phase',['worker','grader'])
def test_private_halt_markers_never_enter_public_payloads(tmp_path,monkeypatch,phase):
    c,call,row=halted(tmp_path,monkeypatch,phase)
    assert row['privateDiagnostic']==c.last_failure
    class Store:
        def __init__(self):self.rows={}
        def insert(self,table,value):
            rsi_rows.CHECKS[table](value)
            self.rows[len(self.rows)+1]={'id':len(self.rows)+1,**value}
            return self.rows[len(self.rows)]
        def get(self,table,identity):return self.rows[identity]
    store=Store()
    run=trial_campaign.create_run(store,{'sourceRevision':'a'*40,'skillsCommit':'b'*40},'c'*64)
    saved=trial_campaign.publish_result(store,run,row,case_id='case',trial=1,evidence_digest='d'*64)
    public=json.dumps(store.rows)
    assert all(marker not in public for marker in MARKERS)
    assert saved['passed']is None and saved['cost_usd']is None
    assert saved['detail']==series.safe_detail(row,'d'*64)
    assert all(marker not in json.dumps(series.metrics(row))for marker in MARKERS)
