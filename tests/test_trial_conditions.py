"""Owned neutral cwd and actual predecessor binding without provider calls."""
import json
from pathlib import Path
import pytest
from ams.assessment import Refused
from ams import trial_conditions as conditions
from ams import trial_series as series
from test_trial_series import campaign,reply
from test_trials import pack,reference
from ams.trial_inputs import materialize


def setup(tmp_path):
    worker=tmp_path/'worker-baseline';materialize(pack(tmp_path/'pack'),worker)
    ref=reference(tmp_path/'oracle');return worker,ref


def test_neutral_execution_is_owned_separate_and_refuses_drift(tmp_path):
    worker,ref=setup(tmp_path);execution=tmp_path/'neutral-execution'
    frozen=conditions.execution_context(execution,worker,ref,create=True)
    assert frozen['path']==str(execution) and list(execution.iterdir())==[execution/conditions.MARKER]
    assert conditions.execution_context(execution,worker,ref)==frozen
    (execution/'unexpected').write_text('preserve')
    with pytest.raises(Refused):conditions.execution_context(execution,worker,ref)
    assert (execution/'unexpected').read_text()=='preserve'


@pytest.mark.parametrize('where',['worker','oracle','ancestor','arm-name'])
def test_execution_cannot_expose_source_or_arm_paths(tmp_path,where):
    worker,ref=setup(tmp_path)
    path={'worker':worker/'execution','oracle':ref.parent/'execution',
          'ancestor':tmp_path,'arm-name':tmp_path/'candidate-room'}[where]
    with pytest.raises(Refused):conditions.execution_context(path,worker,ref,create=True)


def test_both_roles_share_exact_neutral_cwd(tmp_path,monkeypatch):
    seen=[]
    def call(prompt,**kwargs):
        seen.append(kwargs['cwd'])
        from test_trial_series import quoted_reply
        return quoted_reply(prompt,'Yes' if len(seen)==1 else 'No')
    c=campaign(tmp_path,monkeypatch,call)
    c.qualify()
    assert seen==[c.execution]*5 and c.execution!=c.worker


def test_context_drift_halts_before_a_second_query_and_preserves_data(tmp_path,monkeypatch):
    from ams.trial_campaign import RuntimeHalt
    seen=[];c=None
    def call(prompt,**kwargs):
        seen.append(1);(c.execution/'unexpected').write_text('preserve')
        from test_trial_series import quoted_reply
        return quoted_reply(prompt,'Yes')
    c=campaign(tmp_path,monkeypatch,call)
    with pytest.raises(RuntimeHalt):c.qualify()
    assert len(seen)==1 and (c.execution/'unexpected').read_text()=='preserve'
    stopped=series.read_private(c.store,'qualification-owner-positive-r1')['evidence']
    assert stopped['verdict']=='Unknown' and stopped['reason']=='runtime-refused'
    assert stopped['ownerCancellation'] is False


def test_actual_predecessor_byte_change_invalidates_frozen_series(tmp_path,monkeypatch):
    from test_trial_series import quoted_reply
    c=campaign(tmp_path,monkeypatch,lambda prompt,**kwargs:quoted_reply(prompt,'Yes'))
    q=Path(c.protocol['predecessor']['paths']['qualification'])
    data=json.loads(q.read_text());data['value']['evidence']['results'][0]['actual']['verdict']='No'
    q.write_text(json.dumps(data))
    with pytest.raises(Refused):c.qualify()


def test_unknown_previous_slot_blocks_next_without_another_query(tmp_path,monkeypatch):
    from test_trial_series import quoted_reply
    calls=[]
    def call(prompt,**kwargs):
        calls.append(1)
        if len(calls)<=5:return quoted_reply(prompt,'Yes'if len(calls)==1 else 'No')
        return reply('worker final'if len(calls)==6 else 'not JSON')
    c=campaign(tmp_path,monkeypatch,call);assert c.qualify()['qualified']
    assert c.run_one(0)['passed'] is None
    with pytest.raises(Refused,match='Unknown'):c.run_one(1)
    assert len(calls)==7


def test_neutral_cwd_cannot_inherit_moving_git_context(tmp_path):
    worker,ref=setup(tmp_path);repo=tmp_path/'repository';repo.mkdir();(repo/'.git').mkdir()
    with pytest.raises(Refused,match='Git context'):
        conditions.execution_context(repo/'neutral-execution',worker,ref,create=True)


def test_predecessor_true_label_cannot_hide_actual_disagreement(tmp_path,monkeypatch):
    from test_trial_series import quoted_reply
    c=campaign(tmp_path,monkeypatch,lambda prompt,**kwargs:quoted_reply(prompt,'Yes'))
    q=Path(c.protocol['predecessor']['paths']['qualification'])
    data=json.loads(q.read_text());data['value']['evidence']['results'][0]['actual']['verdict']='No'
    data['digest']=series.digest(data['value']);q.write_text(json.dumps(data))
    with pytest.raises(Refused,match='outcome'):c.qualify()


def test_rehashed_oracle_prompt_change_cannot_reuse_predecessor_labels(tmp_path,monkeypatch):
    import hashlib
    from test_trial_series import quoted_reply
    c=campaign(tmp_path,monkeypatch,lambda prompt,**kwargs:quoted_reply(prompt,'Yes'))
    prompt=c.reference.parent/'prompt.txt';prompt.write_text(prompt.read_text()+'changed criterion')
    ref=json.loads(c.reference.read_text());ref['promptSha256']=hashlib.sha256(prompt.read_bytes()).hexdigest()
    c.reference.write_text(json.dumps(ref))
    with pytest.raises(Refused,match='semantic'):c.qualify()


def test_malformed_handshake_becomes_controlled_unknown_without_prompt(tmp_path,monkeypatch):
    from ams import trial_judge,trial_transport
    from ams.trial_campaign import RuntimeHalt
    from test_trial_runtime import Transport
    stream=Transport();stream.initialize=lambda:None
    monkeypatch.setattr(trial_transport,'ClaudeProcess',lambda *a,**k:stream)
    c=campaign(tmp_path,monkeypatch,trial_judge.InterviewAdapter().execute)
    with pytest.raises(RuntimeHalt):c.qualify()
    row=series.read_private(c.store,'qualification-owner-positive-r1')['evidence']
    assert row['verdict']=='Unknown' and row['reason']=='runtime-refused' and row['ownerCancellation']is False
    assert not stream.prompts and stream.closed and c.last_failure is not None
    assert not (c.store/'qualification-final.json').exists()
