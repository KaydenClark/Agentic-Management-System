"""Real transport startup belongs to the adapter before auth/process/selector IO."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from types import SimpleNamespace
import pytest
from ams import trial_transport,trial_judge,trial_series as series
from ams.assessment import Refused
from test_trial_series import campaign
from test_trial_actual_halts import WireFactory,_assert_public_privacy


@pytest.mark.parametrize('phase',['qualification','worker'])
@pytest.mark.parametrize('fault',['auth-refusal','selector-interrupt'])
def test_owned_real_transport_startup_retains_diagnostic_and_reaps_child(tmp_path,monkeypatch,phase,fault):
    c=campaign(tmp_path,monkeypatch,trial_judge.InterviewAdapter().execute)
    wires=WireFactory(phase,'no-fault');wires.campaign=c
    real_transport=trial_transport.ClaudeProcess;real_run=subprocess.run;real_popen=subprocess.Popen
    children=[];transports=[];counts={'auth':0,'starts':0};marker='PRIVATE_STARTUP_STDERR_'+fault
    def factory(cwd,**kwargs):
        if phase=='worker'and kwargs.get('structured_output',False):return wires(cwd,**kwargs)
        stream=real_transport(cwd,**kwargs);transports.append(stream);return stream
    def auth(args,*a,**kwargs):
        if args[:3]==['claude','auth','status']:
            counts['auth']+=1
            return SimpleNamespace(returncode=0,stdout=json.dumps({'loggedIn':fault!='auth-refusal',
                'authMethod':'subscription'}),stderr=marker)
        return real_run(args,*a,**kwargs)
    def spawn(args,*a,**kwargs):
        if args[0]=='claude':
            counts['starts']+=1
            child=real_popen([sys.executable,'-I','-c','import time;time.sleep(20)'],env={},
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            children.append(child);return child
        return real_popen(args,*a,**kwargs)
    def interrupted_selector():raise KeyboardInterrupt('PRIVATE_SELECTOR_INTERRUPT')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    monkeypatch.setattr(trial_transport,'clean_environment',lambda:{})
    monkeypatch.setattr(subprocess,'run',auth);monkeypatch.setattr(subprocess,'Popen',spawn)
    if fault=='selector-interrupt':monkeypatch.setattr(trial_transport.selectors,'DefaultSelector',interrupted_selector)
    try:
        if phase=='worker':assert c.qualify()['qualified']
        with pytest.raises(KeyboardInterrupt):c.qualify()if phase=='qualification'else c.run_one(0)
        identity='qualification-owner-positive-r1'if phase=='qualification'else'trial-1-cancelled'
        row=series.read_private(c.store,identity)['evidence'];private=row['privateDiagnostic']
        facts=private['runtimeDiagnostic']if fault=='auth-refusal'else private
        pointer=facts['diagnostic'];assert isinstance(pointer,str)
        diagnostic=json.loads(Path(pointer).read_text())
        assert marker in diagnostic['stderr'] and marker not in json.dumps(row)
        assert diagnostic['workerPromptRecorded']is False and diagnostic['stdoutRecorded']is False
        assert len(transports)==1 and transports[0].closed
        assert all(child.poll()is not None for child in children)  # before fallback cleanup
        assert counts=={'auth':1,'starts':int(fault=='selector-interrupt')}
        assert row['ownerCancellation']is(fault=='selector-interrupt')
        assert facts['terminalExecution']is None and facts['observedProviderTurns']is None
        if phase=='qualification':
            assert row['verdict']=='Unknown'
            with pytest.raises(Refused):c.qualify()
        else:
            assert row['passed']is None and row['workerCompleted']is False and row['worker']is None
            _assert_public_privacy(row,(marker,'PRIVATE_SELECTOR_INTERRUPT'))
            with pytest.raises(Refused):c.run_one(0)
            with pytest.raises(FileNotFoundError):c.run_one(1)
        assert counts['auth']==1
    finally:
        for child in children:
            if child.poll()is None:os.killpg(child.pid,signal.SIGKILL)
            child.wait(timeout=3)
            for pipe in (child.stdin,child.stdout,child.stderr):pipe.close()
