"""Bootstrap public seams. All provider streams and source packs here are synthetic."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from ams import trials
from ams import trial_runtime as runtime


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


def events():
    return [
        {'type':'system','subtype':'init','model':runtime.MODEL,'tools':[],
         'mcp_servers':[],'permissionMode':'dontAsk'},
        {'type':'assistant','message':{'model':runtime.MODEL,
                                     'content':[{'type':'text','text':'Fixture response'}]}},
        {'type':'result','subtype':'success','is_error':False,'result':'Fixture response',
         'num_turns':1,'permission_denials':[],
         'usage':{'input_tokens':2,'output_tokens':3,'cache_read_input_tokens':4,
                  'cache_creation_input_tokens':5,'server_tool_use':{'web_search_requests':0,'web_fetch_requests':0}},
         'modelUsage':{runtime.MODEL:{'inputTokens':2,'outputTokens':3,'cacheReadInputTokens':4,
                      'cacheCreationInputTokens':5,'webSearchRequests':0,'provider':'firstParty',
                      'canonicalModel':runtime.MODEL,'costUSD':0.01}},'total_cost_usd':0.01}]


class Transport:
    def __init__(self, stream=None):
        self.stream=events() if stream is None else stream
        self.closed=False;self.prompts=[]

    def initialize(self):
        return {'commands':[]}

    def mcp_status(self):
        return []

    def responses(self,prompt):
        self.prompts.append(prompt)
        yield from self.stream

    def close(self):
        self.closed=True


def test_materialize_reset_and_protected_reference(tmp_path):
    source=pack(tmp_path/'pack'); target=tmp_path/'worker'
    before=source.read_bytes();outside=tmp_path/'unrelated';outside.write_text('preserve')
    receipt=trials.materialize(source,target)
    assert (target/'artifacts/fixture-skill/SKILL.md').read_text().startswith('Synthetic')
    (target/'scratch.txt').write_text('discard only inside the owned fixture')
    trials.materialize(source,target,reset=True)
    assert not (target/'scratch.txt').exists() and outside.read_text()=='preserve'
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


def test_runtime_success_preserves_exact_model_unknown_cost_and_private_text():
    t=Transport();result=runtime.ClaudeAdapter().execute('private fixture prompt',transport=t)
    assert result['response']=='Fixture response' and result['model']==runtime.MODEL
    assert result['actualSubscriptionCostUsd'] is None
    assert result['usage']['cacheCreationInputTokens']==5
    assert result['equivalentApiCostUsd']==0.01
    assert t.closed and t.prompts==['private fixture prompt']
    command=runtime.claude_command()
    assert command[command.index('--tools')+1]==''
    assert command[command.index('--model')+1]==runtime.MODEL
    assert '--fallback-model' not in command and '--bare' not in command
    assert '--dangerously-skip-permissions' not in command


@pytest.mark.parametrize('fault',['tools','mcp','runtime-model','assistant-model','usage-model',
                                  'provider','tool-use','missing-init','error','boolean-turns',
                                  'negative-tokens','missing-result','text-mismatch','permission','usage-mismatch'])
def test_runtime_refuses_unsafe_incomplete_or_drifted_streams(fault):
    stream=events()
    if fault=='tools':stream[0]['tools']=['Read']
    if fault=='mcp':stream[0]['mcp_servers']=[{'name':'outward'}]
    if fault=='runtime-model':stream[0]['model']='alias'
    if fault=='assistant-model':stream[1]['message']['model']='other'
    if fault=='usage-model':stream[2]['modelUsage']['other']=stream[2]['modelUsage'].pop(runtime.MODEL)
    if fault=='provider':stream[2]['modelUsage'][runtime.MODEL]['provider']='thirdParty'
    if fault=='tool-use':stream[1]['message']['content']=[{'type':'tool_use','name':'Read'}]
    if fault=='missing-init':stream.pop(0)
    if fault=='error':stream[2]['is_error']=True
    if fault=='boolean-turns':stream[2]['num_turns']=True
    if fault=='negative-tokens':stream[2]['usage']['input_tokens']=-1
    if fault=='missing-result':stream.pop()
    if fault=='text-mismatch':stream[2]['result']='invented'
    if fault=='permission':stream[0]['permissionMode']='bypassPermissions'
    if fault=='usage-mismatch':stream[2]['usage']['input_tokens']=9
    t=Transport(stream)
    with pytest.raises(trials.Refused):runtime.ClaudeAdapter().execute('fixture',transport=t)
    assert t.closed


def test_mcp_refusal_precedes_sending_prompt():
    t=Transport();t.mcp_status=lambda:[{'name':'unexpected'}]
    with pytest.raises(trials.Refused):runtime.ClaudeAdapter().execute('fixture',transport=t)
    assert not t.prompts and t.closed


def test_environment_keeps_os_auth_context_without_provider_keys():
    env=runtime.clean_environment({'PATH':'/bin','USER':'fixture','LOGNAME':'fixture',
                                   'ANTHROPIC_API_KEY':'do-not-forward','CLAUDE_CODE_OAUTH_TOKEN':'do-not-forward',
                                   'SUPABASE_SERVICE_ROLE_KEY':'do-not-forward','UNRELATED':'no'})
    assert env=={'PATH':'/bin','USER':'fixture','LOGNAME':'fixture'}


@pytest.mark.parametrize('value',[float('inf'),True])
def test_provider_cost_identity_cannot_smuggle_nonfinite_or_boolean(value):
    stream=events();stream[2]['total_cost_usd']=float('inf') if value is not True else 1
    stream[2]['modelUsage'][runtime.MODEL]['costUSD']=value
    with pytest.raises(trials.Refused):runtime.ClaudeAdapter().execute('fixture',transport=Transport(stream))


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
