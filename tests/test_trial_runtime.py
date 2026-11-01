"""Tool-free runtime and socket-boundary contracts; provider calls are all synthetic."""
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
from ams import trial_runtime as runtime
from ams import trials

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


def test_equal_numeric_measurements_do_not_require_same_json_spelling():
    stream=events();stream[2]['total_cost_usd']=0
    stream[2]['modelUsage'][runtime.MODEL]['costUSD']=0.0
    assert runtime.ClaudeAdapter().execute('fixture',transport=Transport(stream))['equivalentApiCostUsd']==0


def test_network_permission_error_outside_socket_probe_is_not_a_pass(tmp_path,monkeypatch):
    class Run:
        stdout='\n'.join(runtime.CANARIES[:-1])+'\nPermissionError: file import Operation not permitted\n'
        stderr='';returncode=1
    monkeypatch.setattr(runtime.sys,'platform','darwin')
    monkeypatch.setattr(runtime.subprocess,'run',lambda *args,**kwargs:Run())
    result=runtime.shell_preflight(tmp_path)
    assert result['status']=='failed' and result['checks']['networkDenied'] is False


def test_failed_transport_retains_bounded_private_actionable_diagnostic(tmp_path,monkeypatch):
    from ams import trial_transport
    real_popen=trial_transport.subprocess.Popen
    monkeypatch.chdir(tmp_path)
    auth={'loggedIn':True,'authMethod':'claude.ai','apiKeySource':None}
    monkeypatch.setattr(trial_transport.subprocess,'run',lambda *args,**kwargs:
                        SimpleNamespace(stdout=json.dumps(auth),stderr='',returncode=0))
    def inert_process(*args,**kwargs):
        return real_popen([sys.executable,'-c',
            'import sys;sys.stderr.write("x"*20000+"\\nfixture denied startup sk-ant-fixture-secret\\n");sys.stderr.flush();sys.exit(7)'],**kwargs)
    monkeypatch.setattr(trial_transport.subprocess,'Popen',inert_process)
    with pytest.raises(trials.Refused):runtime.ClaudeAdapter().execute('private text must never be logged',cwd=tmp_path)
    files=list((tmp_path/'.local/trial-diagnostics').glob('*.json'))
    assert len(files)==1
    row=json.loads(files[0].read_text())
    assert 'fixture denied startup' in row['stderr'] and len(row['stderr'].encode())<=16384
    assert row['exitStatus']==7 and 'sk-ant-fixture-secret' not in files[0].read_text()
    assert 'private text must never be logged' not in files[0].read_text()
