"""Tool-free runtime and socket-boundary contracts; provider calls are all synthetic."""
import json
import os
from pathlib import Path
import signal
import sys
import time
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


def test_shutdown_is_bounded_when_descendant_retains_stderr(tmp_path,monkeypatch):
    from ams import trial_transport
    real_popen=trial_transport.subprocess.Popen
    auth={'loggedIn':True,'authMethod':'claude.ai','apiKeySource':None}
    monkeypatch.setattr(trial_transport.subprocess,'run',lambda *args,**kwargs:
                        SimpleNamespace(stdout=json.dumps(auth),stderr='',returncode=0))
    program=('import subprocess,sys; '
             'p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(3)"],stdout=subprocess.DEVNULL,stderr=sys.stderr); '
             'print(p.pid,flush=True)')
    monkeypatch.setattr(trial_transport.subprocess,'Popen',lambda *args,**kwargs:
                        real_popen([sys.executable,'-c',program],**kwargs))
    stream=trial_transport.ClaudeProcess(tmp_path)
    descendant=int(stream.process.stdout.readline())
    stream.process.wait(timeout=2)
    try:
        start=time.monotonic();stream.close()
        assert time.monotonic()-start<1, 'shutdown waited for inherited stderr EOF'
    finally:
        try:os.kill(descendant,signal.SIGTERM)
        except ProcessLookupError:pass


def test_early_exit_broken_stdin_does_not_erase_failure_diagnostic(tmp_path,monkeypatch):
    from ams import trial_transport
    real_popen=trial_transport.subprocess.Popen
    monkeypatch.chdir(tmp_path)
    auth={'loggedIn':True,'authMethod':'claude.ai','apiKeySource':None}
    monkeypatch.setattr(trial_transport.subprocess,'run',lambda *args,**kwargs:
                        SimpleNamespace(stdout=json.dumps(auth),stderr='',returncode=0))
    monkeypatch.setattr(trial_transport.subprocess,'Popen',lambda *args,**kwargs:
                        real_popen([sys.executable,'-c','raise SystemExit(7)'],**kwargs))
    stream=trial_transport.ClaudeProcess(tmp_path);stream.process.wait(timeout=2)
    adapter=runtime.ClaudeAdapter()
    with pytest.raises(trials.Refused):adapter.execute('private',transport=stream)
    assert isinstance(adapter.last_failure,str)
    row=json.loads(Path(adapter.last_failure).read_text())
    assert row['exitStatus']==7 and row['stage']=='initialize'


def inert_transport_probe(tmp_path, child_program, driver, timeout=2.5):
    """An outer watchdog can kill both owned groups even if the tested send blocks."""
    import subprocess
    program = f'''
import json,sys
from pathlib import Path
from types import SimpleNamespace
from ams import trial_transport as transport
from ams.assessment import Refused
real_popen=transport.subprocess.Popen
transport.subprocess.run=lambda *args,**kwargs:SimpleNamespace(stdout=json.dumps({{"loggedIn":True,"authMethod":"claude.ai","apiKeySource":None}}),stderr="",returncode=0)
transport.subprocess.Popen=lambda *args,**kwargs:real_popen([sys.executable,"-c",{child_program!r}],**kwargs)
stream=transport.ClaudeProcess(Path.cwd())
print(json.dumps({{"childPid":stream.process.pid}}),flush=True)
try:
{driver}
finally:
 stream.close()
'''
    process = subprocess.Popen([sys.executable, '-c', program], cwd=tmp_path,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    timed_out = False
    try:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            timed_out = True
            partial = (error.output or b'').splitlines()
            if partial:
                child_pid = json.loads(partial[0])['childPid']
                try: os.killpg(child_pid, signal.SIGKILL)
                except ProcessLookupError: pass
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        rows = [json.loads(line) for line in stdout.splitlines()]
        return {'timedOut': timed_out, 'rows': rows, 'stderr': stderr.decode(),
                'returncode': process.returncode}
    finally:
        for row in (locals().get('rows') or []):
            if 'childPid' in row:
                try: os.killpg(row['childPid'], signal.SIGKILL)
                except ProcessLookupError: pass


def test_large_prompt_survives_partial_writes_and_concurrent_output(tmp_path):
    import hashlib
    child = '''
import hashlib,json,os,select,sys
sys.stderr.write("fixture stderr flood\\n"*16384);sys.stderr.flush()
for _ in range(64):
 print(json.dumps({"type":"keepalive","data":"x"*8192}),flush=True)
data=b""
while b"\\n" not in data:
 data+=os.read(0,4096)
extra=os.read(0,4096) if select.select([0],[],[],.03)[0] else b""
print(json.dumps({"type":"result","receivedHash":hashlib.sha256(data).hexdigest(),"lines":data.count(b"\\n"),"extraBytes":len(extra)}),flush=True)
'''
    driver = ''' rows=list(stream.responses("x"*131072))
 print(json.dumps({"result":rows[-1],"eventCount":len(rows)}),flush=True)'''
    result = inert_transport_probe(tmp_path, child, driver)
    assert not result['timedOut'], 'send blocked before draining runtime output'
    assert result['returncode'] == 0, result['stderr']
    expected = {'type':'user','session_id':'','parent_tool_use_id':None,
                'message':{'role':'user','content':'x'*131072}}
    digest = hashlib.sha256(json.dumps(expected).encode()+b'\n').hexdigest()
    row = result['rows'][-1]
    assert row['eventCount'] == 65
    assert row['result'] == {'type':'result','receivedHash':digest,'lines':1,'extraBytes':0}


@pytest.mark.parametrize('phase', ['initialize', 'mcp_status', 'execution'])
def test_nonreading_runtime_refuses_by_phase_deadline_with_private_cause(tmp_path, phase):
    child = 'import sys,time;sys.stderr.write("fixture not reading stdin\\n"*16384);sys.stderr.flush();time.sleep(30)'
    call = 'list(stream.responses("x"*131072))' if phase == 'execution' else f'stream.{phase}()'
    driver = f''' transport.CONTROL_TIMEOUT=.15;transport.EXECUTION_TIMEOUT=.15
 try:
  {call}
  raise AssertionError("expected timeout")
 except Refused as error:
  path=stream.failure_diagnostic(type(error).__name__,str(error))
  row=json.loads(Path(path).read_text())
  print(json.dumps({{"stage":row["stage"],"reason":row["reason"],"stderrRetained":"fixture not reading stdin" in row["stderr"],"promptRecorded":row["workerPromptRecorded"],"stdoutRecorded":row["stdoutRecorded"],"exited":stream.process.poll() is not None}}),flush=True)'''
    result = inert_transport_probe(tmp_path, child, driver)
    assert not result['timedOut'], 'phase deadline failed to bound a nonreading runtime'
    assert result['returncode'] == 0, result['stderr']
    row = result['rows'][-1]
    assert row['stage'] == phase and 'timed out' in row['reason']
    assert row['stderrRetained'] and row['exited']
    assert not row['promptRecorded'] and not row['stdoutRecorded']


def test_send_and_reply_share_one_execution_deadline(tmp_path):
    child = '''
import sys,time
# Delay reading until a large write fills the pipe, then delay the reply too.
time.sleep(.11)
sys.stdin.buffer.readline()
time.sleep(.11)
print('{"type":"result"}',flush=True)
'''
    driver = ''' import time
 transport.EXECUTION_TIMEOUT=.18
 start=time.monotonic()
 try:
  list(stream.responses("x"*131072))
  raise AssertionError("send incorrectly reset the execution deadline")
 except Refused as error:
  print(json.dumps({"reason":str(error),"elapsed":time.monotonic()-start}),flush=True)'''
    result = inert_transport_probe(tmp_path, child, driver)
    assert not result['timedOut'] and result['returncode'] == 0, result['stderr']
    row = result['rows'][-1]
    assert 'timed out' in row['reason'] and row['elapsed'] < .4
