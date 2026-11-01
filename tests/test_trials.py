"""Bootstrap public seams. All provider streams and source packs here are synthetic."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from ams import trials
from ams import trial_runtime as runtime
from test_trial_runtime import Transport


def pack(folder):
    folder.mkdir()
    (folder / 'fixture-skill').mkdir()
    data = b'Synthetic instruction fixture, never a measured skill.\n'
    (folder / 'fixture-skill/SKILL.md').write_bytes(data)
    entry = {'path':'fixture-skill/SKILL.md','bytes':len(data),
             'sha256':hashlib.sha256(data).hexdigest(),
             'gitBlob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),
             'sourceUrl':'https://example.invalid/source'}
    manifest = {'schema':1,'repository':'fixture/skills','condition':'baseline',
                'sourceCommit':'a'*40,'entries':[entry]}
    path = folder / 'manifest.json'
    path.write_text(json.dumps(manifest))
    return path


def reference(folder):
    folder.mkdir()
    (folder / 'prompt.txt').write_text('Synthetic protected judge, not qualified.\n')
    examples={'kind':'narrow-oracle-seeds','source':'synthetic tests, no owner qualification',
              'examples':[{'id':'good','label':'Yes','response':'Synthetic continuation'},
                          {'id':'noop','label':'No','response':'Synthetic no-op'}]}
    for example in examples['examples']:
        example['responseSha256']=hashlib.sha256(example['response'].encode()).hexdigest()
    (folder/'examples.json').write_text(json.dumps(examples))
    r = {'schema':1,'kind':'interview-grader-reference','model':runtime.MODEL,
         'effort':'medium','promptFile':'prompt.txt',
         'promptSha256':hashlib.sha256((folder/'prompt.txt').read_bytes()).hexdigest(),
         'qualification':'unqualified','sourceRevision':'b'*40,'examplesFile':'examples.json',
         'examplesSha256':hashlib.sha256((folder/'examples.json').read_bytes()).hexdigest()}
    path = folder/'reference.json';path.write_text(json.dumps(r))
    return path






def test_materialize_reset_and_protected_reference(tmp_path):
    source=pack(tmp_path/'pack'); target=tmp_path/'worker'
    before=source.read_bytes();outside=tmp_path/'unrelated';outside.write_text('preserve')
    receipt=trials.materialize(source,target)
    assert (target/'artifacts/fixture-skill/SKILL.md').read_text().startswith('Synthetic')
    (target/'artifacts/fixture-skill/SKILL.md').write_text('dirty tracked fixture artifact')
    trials.materialize(source,target,reset=True)
    assert (target/'artifacts/fixture-skill/SKILL.md').read_text().startswith('Synthetic')
    assert outside.read_text()=='preserve'
    assert source.read_bytes()==before
    ref=reference(tmp_path/'protected')
    frozen=trials.grader_reference(ref,target)
    assert frozen['qualification']=='unqualified'
    assert receipt['sourceCommit']=='a'*40
    assert not list(target.rglob('reference.json'))
    with pytest.raises(trials.Refused,match='protected'):
        trials.grader_reference(ref,tmp_path)


@pytest.mark.parametrize('fault',['bytes','extra','traversal','symlink','duplicate','boolean-size'])
def test_bad_pack_refused_without_creating_worker(tmp_path,fault):
    source=pack(tmp_path/'pack');m=json.loads(source.read_text());target=tmp_path/'worker'
    if fault=='bytes':(source.parent/'fixture-skill/SKILL.md').write_text('changed')
    if fault=='extra':(source.parent/'unlisted').write_text('extra')
    if fault=='traversal':m['entries'][0]['path']='../outside'
    if fault=='symlink':
        f=source.parent/'fixture-skill/SKILL.md';f.unlink();f.symlink_to(source)
    if fault=='duplicate':m['entries']*=2
    if fault=='boolean-size':m['entries'][0]['bytes']=True
    source.write_text(json.dumps(m))
    with pytest.raises(trials.Refused):trials.materialize(source,target)
    assert not target.exists()


def test_reset_refuses_unowned_or_symlinked_fixture(tmp_path):
    source=pack(tmp_path/'pack');target=tmp_path/'worker';target.mkdir()
    (target/'precious').write_text('keep')
    with pytest.raises(trials.Refused):trials.materialize(source,target,reset=True)
    assert (target/'precious').read_text()=='keep'
    target2=tmp_path/'owned';trials.materialize(source,target2)
    (target2/'link').symlink_to(target)
    with pytest.raises(trials.Refused):trials.materialize(source,target2,reset=True)
    assert (target/'precious').read_text()=='keep'


def test_reset_refuses_unlisted_recovery_files(tmp_path):
    source=pack(tmp_path/'pack');target=tmp_path/'worker';trials.materialize(source,target)
    recovery=target/'owner-recovery.txt';recovery.write_text('keep')
    with pytest.raises(trials.Refused):trials.materialize(source,target,reset=True)
    assert recovery.read_text()=='keep'
    recovery.unlink()
    recovery=target/'artifacts/owner-recovery.txt';recovery.write_text('keep')
    with pytest.raises(trials.Refused):trials.materialize(source,target,reset=True)
    assert recovery.read_text()=='keep'












def test_prompt_uses_verified_artifacts_and_case_without_protected_reference(tmp_path):
    source=pack(tmp_path/'pack');target=tmp_path/'worker';trials.materialize(source,target)
    prompt,identity=trials.worker_prompt(target,'grill-context-link-r1')
    assert 'Synthetic instruction fixture' in prompt and 'Assessment scope is still unanswered' in prompt
    assert identity['caseId']=='grill-context-link-r1' and identity['nativeInstallation'] is False
    assert 'ownerExamples' not in prompt and 'Your answers are saved. Ready when you are.' not in prompt
    (target/'artifacts/fixture-skill/SKILL.md').write_text('changed')
    with pytest.raises(trials.Refused):trials.worker_prompt(target,'grill-context-link-r1')


def test_changed_owner_label_bytes_invalidate_reference(tmp_path):
    ref=reference(tmp_path/'protected');worker=tmp_path/'worker';worker.mkdir()
    trials.grader_reference(ref,worker)
    data=json.loads((ref.parent/'examples.json').read_text())
    data['examples'][0]['response']+=' changed'
    (ref.parent/'examples.json').write_text(json.dumps(data))
    with pytest.raises(trials.Refused):trials.grader_reference(ref,worker)


def test_ancestor_reference_cannot_put_owner_examples_inside_worker(tmp_path):
    ref=reference(tmp_path/'protected');worker=ref.parent/'worker';worker.mkdir()
    data=json.loads(ref.read_text());data['examplesFile']='worker/examples.json'
    (worker/'examples.json').write_bytes((ref.parent/'examples.json').read_bytes())
    ref.write_text(json.dumps(data))
    with pytest.raises(trials.Refused):trials.grader_reference(ref,worker)








def evidence():
    result=runtime.ClaudeAdapter().execute('fixture',transport=Transport())
    return trials.execution_evidence('fixture-preflight',result,'external-cli-smoke','c'*64)


def test_safe_immutable_evidence_readback_and_tamper_refusal(tmp_path):
    row=evidence();saved=trials.save_evidence(row,tmp_path)
    assert trials.save_evidence(copy.deepcopy(row),tmp_path)==saved
    assert trials.read_evidence(tmp_path)==[row]
    assert 'Fixture response' not in json.dumps(row) and 'prompt' not in row
    changed=copy.deepcopy(row);changed['usage']['inputTokens']=True
    with pytest.raises(trials.Refused):trials.save_evidence(changed,tmp_path)
    changed=copy.deepcopy(row);changed['privateLocator']='/private/example'
    with pytest.raises(trials.Refused):trials.save_evidence(changed,tmp_path)
    file=next(tmp_path.glob('*.json'));file.write_text(file.read_text().replace('"inputTokens":2','"inputTokens":7'))
    with pytest.raises(trials.Refused):trials.read_evidence(tmp_path)


def test_cli_materialize_preflight_readback_without_model(tmp_path,monkeypatch,capsys):
    source=pack(tmp_path/'pack');target=tmp_path/'worker';ref=reference(tmp_path/'protected')
    assert trials.main(['materialize',str(source),str(target)])==0
    capsys.readouterr()
    monkeypatch.setattr(runtime,'shell_preflight',lambda root:{'status':'passed','scope':'host-command-canaries',
                         'checks':{k:True for k in runtime.CANARIES}})
    assert trials.main(['preflight',str(target),'--reference',str(ref),'--id','fixture','--store',str(tmp_path/'evidence')])==0
    out=json.loads(capsys.readouterr().out)
    assert out['readyForControlledTrials'] is False
    assert 'semantic-grader-unqualified' in out['gates']
    assert trials.main(['readback','--store',str(tmp_path/'evidence')])==0
    assert len(json.loads(capsys.readouterr().out))==1


def test_public_suite_has_three_dev_cases_and_no_private_oracle():
    suite=json.loads(Path('evals/interview-dev-cases.json').read_text())
    assert len(suite['cases'])==3 and {c['split']for c in suite['cases']}=={'dev'}
    assert suite['scope']=='tool-free-transcript-interview-preservation'
    assert all('expectedResponse'not in c and 'ownerExamples'not in c for c in suite['cases'])


def test_invalid_cli_input_refuses_before_command_execution(tmp_path,monkeypatch,capsys):
    ref=reference(tmp_path/'protected')
    def unexpected(*args):
        raise AssertionError('sandbox command ran before input validation')
    monkeypatch.setattr(runtime,'shell_preflight',unexpected)
    assert trials.main(['preflight',str(tmp_path/'missing'),'--reference',str(ref),'--id','bad'])==1
    assert not capsys.readouterr().out


@pytest.mark.parametrize('value',[[],None,True,1])
def test_scalar_manifest_cli_errors_are_controlled(tmp_path,capsys,value):
    folder=tmp_path/'pack';folder.mkdir();path=folder/'manifest.json';path.write_text(json.dumps(value))
    assert trials.main(['materialize',str(path),str(tmp_path/'worker')])==1
    assert not (tmp_path/'worker').exists()
