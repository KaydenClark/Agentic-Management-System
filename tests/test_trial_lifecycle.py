"""Whole actual-adapter lifetime errors retain evidence without a second query."""
import pytest
from ams import trial_transport,trial_judge,trial_series as series
from ams.assessment import Refused
from test_trial_series import campaign
from test_trial_actual_halts import WireFactory,_assert_public_privacy


@pytest.mark.parametrize('phase',['qualification','worker','grader'])
@pytest.mark.parametrize('fault',['cleanup-interrupt','body-refused-cleanup-interrupt',
    'body-interrupt-cleanup-error','body-refused-cleanup-error','cleanup-interrupt-diagnostic-interrupt'])
def test_entire_actual_lifetime_preserves_both_causes_and_terminal(tmp_path,monkeypatch,phase,fault):
    wires=WireFactory(phase,'no-fault')
    target={'qualification':1,'worker':6,'grader':7}[phase]
    def factory(cwd,**kwargs):
        wire=wires(cwd,**kwargs)
        if len(wires.streams)!=target:return wire
        responses=wire.responses;close=wire.close
        if fault.startswith('body-'):
            def body(prompt):
                for index,event in enumerate(responses(prompt)):
                    yield event
                    if index==1:
                        if 'body-refused'in fault:raise Refused('PRIVATE_BODY_CAUSE')
                        raise KeyboardInterrupt('PRIVATE_BODY_CANCEL')
            wire.responses=body
        def cleanup():
            close()
            if 'cleanup-interrupt'in fault:raise KeyboardInterrupt('PRIVATE_CLEANUP_CANCEL')
            raise OSError('PRIVATE_CLEANUP_CAUSE')
        wire.close=cleanup
        if 'diagnostic-interrupt'in fault:
            def diagnostic(*args):raise KeyboardInterrupt('PRIVATE_DIAGNOSTIC_CANCEL')
            wire.failure_diagnostic=diagnostic
        return wire
    monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    c=campaign(tmp_path,monkeypatch,trial_judge.InterviewAdapter().execute);wires.campaign=c
    if phase!='qualification':assert c.qualify()['qualified']
    with pytest.raises(KeyboardInterrupt):c.qualify()if phase=='qualification'else c.run_one(0)
    identity='qualification-owner-positive-r1'if phase=='qualification'else'trial-1-cancelled'
    row=series.read_private(c.store,identity)['evidence'];failure=row['privateDiagnostic']
    controlled=fault=='body-refused-cleanup-error'
    assert row['ownerCancellation']is(not controlled)
    assert row['reason']==('runtime-refused'if controlled else'cancelled')
    facts=failure['runtimeDiagnostic']if controlled else failure
    causes=facts['failures']
    assert causes['cleanup']['errorClass']==('KeyboardInterrupt'if'cleanup-interrupt'in fault else'OSError')
    if fault.startswith('body-'):
        assert causes['body']['errorClass']==('Refused'if'body-refused'in fault else'KeyboardInterrupt')
        assert facts['terminalExecution']is None
    else:
        assert causes['body']is None and facts['terminalExecution']['usage']['inputTokens']==2
        available=failure['availableExecution']
        assert available['returned']is False and available['execution']==facts['terminalExecution']
        assert available['role']==('worker'if phase=='worker'else'judge')
    if 'diagnostic-interrupt'in fault:assert causes['diagnostic']['errorClass']=='KeyboardInterrupt'
    assert len(wires.streams)==target and all(s.closed for s in wires.streams)
    if phase=='qualification':
        assert row['verdict']=='Unknown' and not(c.store/'qualification-final.json').exists()
        with pytest.raises(Refused):c.qualify()
    else:
        assert row['passed']is None and row['grade']is None
        assert row['workerCompleted']is(phase=='grader')
        known=phase=='grader'or not fault.startswith('body-')
        assert (series.metrics(row)['input_tokens']is not None)is known
        _assert_public_privacy(row,('PRIVATE_BODY_CAUSE','PRIVATE_BODY_CANCEL','PRIVATE_CLEANUP_CANCEL',
                                    'PRIVATE_CLEANUP_CAUSE','PRIVATE_DIAGNOSTIC_CANCEL'))
        with pytest.raises(Refused):c.run_one(0)
        with pytest.raises(FileNotFoundError):c.run_one(1)
    assert len(wires.streams)==target


@pytest.mark.parametrize('error',[Refused('PRIVATE_ACQUISITION'),KeyboardInterrupt('PRIVATE_ACQUISITION')])
def test_acquisition_failure_is_inside_evidence_boundary(tmp_path,monkeypatch,error):
    calls=[]
    def factory(*args,**kwargs):calls.append(1);raise error
    monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    c=campaign(tmp_path,monkeypatch,trial_judge.InterviewAdapter().execute)
    with pytest.raises(KeyboardInterrupt):c.qualify()
    row=series.read_private(c.store,'qualification-owner-positive-r1')['evidence']
    failure=row['privateDiagnostic']
    if isinstance(error,Refused):failure=failure['runtimeDiagnostic']
    assert failure['failures']['body']['errorClass']==type(error).__name__
    assert failure['failures']['cleanup']is None and failure['terminalExecution']is None
    assert failure['observedProviderTurns']is None and row['verdict']=='Unknown'
    with pytest.raises(Refused):c.qualify()
    assert calls==[1]
