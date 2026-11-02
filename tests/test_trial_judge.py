"""Synthetic structured-serialization protocol; no provider/authentication calls."""
import copy
import json
import pytest
from ams.assessment import Refused
from ams import trial_runtime as runtime
from ams import trial_judge as judge
from test_trial_runtime import Transport,events as worker_events


def events(turns=1):
    value={'verdict':'No','evidence':'final','obligation':'does not advance'}
    final=worker_events()[-1]
    final.update(result='',num_turns=turns,structured_output=value)
    stream=[{'type':'system','subtype':'init','model':runtime.MODEL,'tools':['StructuredOutput'],
             'mcp_servers':[],'permissionMode':'dontAsk'},
            {'type':'assistant','message':{'id':'message-1','model':runtime.MODEL,'content':[
                {'type':'tool_use','id':'serialization-1','name':'StructuredOutput','input':value}]}},
            {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'serialization-1',
                 'content':'Structured output provided successfully','is_error':False}]}}]
    if turns==2:stream.append({'type':'assistant','message':{'id':'message-2','model':runtime.MODEL,
                                                          'content':[{'type':'text','text':''}]}})
    return stream+[final]


@pytest.mark.parametrize('turns',[1,2])
def test_judge_returns_only_verified_terminal_schema_and_actual_turns(turns):
    t=Transport(events(turns));result=judge.ClaudeJudgeAdapter().execute('private criterion',transport=t)
    assert json.loads(result['response'])==result['structuredOutput']==events()[-1]['structured_output']
    assert result['providerTurns']==turns and result['serializationCalls']==1
    assert result['tools']==['StructuredOutput'] and result['mcpServers']==[]
    assert result['actualSubscriptionCostUsd'] is None and t.closed
    command=judge.judge_command(system_prompt='fixed')
    assert json.loads(command[command.index('--json-schema')+1])==judge.SCHEMA
    assert command[command.index('--max-turns')+1]=='2'
    assert '--json-schema' not in runtime.claude_command() and '--max-turns' not in runtime.claude_command()


@pytest.mark.parametrize('fault',['extra-tool','missing-tool','mcp','mode','model','missing-init',
    'tool-name','duplicate-use','invalid-schema','unknown-field','use-id','result-id','result-error',
    'duplicate-result','missing-tool-result','missing-terminal','terminal-mismatch','terminal-missing',
    'too-many-turns','boolean-turns','hidden-turn','duplicate-message','fallback','retraction','result-error-terminal'])
def test_judge_refuses_any_expansion_or_retry(fault):
    stream=events()
    if fault=='extra-tool':stream[0]['tools'].append('Read')
    if fault=='missing-tool':stream[0]['tools']=[]
    if fault=='mcp':stream[0]['mcp_servers']=[{'name':'unexpected'}]
    if fault=='mode':stream[0]['permissionMode']='bypassPermissions'
    if fault=='model':stream[0]['model']='alias'
    if fault=='missing-init':stream.pop(0)
    if fault=='tool-name':stream[1]['message']['content'][0]['name']='Read'
    if fault=='duplicate-use':stream.insert(2,copy.deepcopy(stream[1]))
    if fault=='invalid-schema':stream[1]['message']['content'][0]['input']={'verdict':'Yes'}
    if fault=='unknown-field':stream[1]['message']['content'][0]['input']={**stream[-1]['structured_output'],'private':'x'}
    if fault=='use-id':stream[1]['message']['content'][0]['id']=''
    if fault=='result-id':stream[2]['message']['content'][0]['tool_use_id']='other'
    if fault=='result-error':stream[2]['message']['content'][0]['is_error']=True
    if fault=='duplicate-result':stream.insert(3,copy.deepcopy(stream[2]))
    if fault=='missing-tool-result':stream.pop(2)
    if fault=='missing-terminal':stream.pop()
    if fault=='terminal-mismatch':stream[-1]['structured_output']={**stream[-1]['structured_output'],'verdict':'Yes'}
    if fault=='terminal-missing':stream[-1].pop('structured_output')
    if fault=='too-many-turns':stream[-1]['num_turns']=3
    if fault=='boolean-turns':stream[-1]['num_turns']=True
    if fault=='hidden-turn':stream[-1]['num_turns']=2
    if fault=='duplicate-message':stream[1]['message']['content'].append(copy.deepcopy(stream[1]['message']['content'][0]))
    if fault=='fallback':stream[1]['message']['model']='fallback'
    if fault=='retraction':stream.insert(3,{'type':'system','subtype':'structured_output_retracted'})
    if fault=='result-error-terminal':stream[-1]['subtype']='error_max_structured_output_retries'
    t=Transport(stream)
    with pytest.raises(Refused):judge.ClaudeJudgeAdapter().execute('criterion',transport=t)
    assert t.closed


def test_invalid_first_serialization_aborts_before_favorable_retry_is_read():
    stream=events();stream[1]['message']['content'][0]['input']={'verdict':'Yes'}
    class Counting(Transport):
        def __init__(self):super().__init__(stream+events()[1:]);self.read=0
        def responses(self,prompt):
            for item in self.stream:self.read+=1;yield item
    t=Counting()
    with pytest.raises(Refused):judge.ClaudeJudgeAdapter().execute('criterion',transport=t)
    assert t.read==2 and t.closed


def test_role_router_propagates_only_judge_mode_and_actual_turn_count(monkeypatch):
    from ams import trial_transport
    from ams.trial_series import WORKER_SYSTEM,JUDGE_SYSTEM
    seen=[]
    def factory(cwd,*,system_prompt=None,structured_output=False):
        seen.append((cwd,system_prompt,structured_output))
        return Transport(events(2)if structured_output else worker_events())
    monkeypatch.setattr(trial_transport,'ClaudeProcess',factory)
    adapter=judge.InterviewAdapter()
    worker=adapter.execute('worker',cwd='neutral',system_prompt=WORKER_SYSTEM)
    grader=adapter.execute('judge',cwd='neutral',system_prompt=JUDGE_SYSTEM)
    assert seen==[('neutral',WORKER_SYSTEM,False),('neutral',JUDGE_SYSTEM,True)]
    assert worker['providerTurns']==1 and worker['tools']==[] and grader['providerTurns']==2
    with pytest.raises(Refused):adapter.execute('x',system_prompt='candidate-selected context')


def test_structured_jsonl_rejects_duplicate_keys_before_protocol_interpretation():
    import os
    from types import SimpleNamespace
    from ams.trial_transport import ClaudeProcess
    r,w=os.pipe()
    try:
        os.write(w,b'{"type":"assistant","message":{"id":"one","id":"two"}}\n')
        process=ClaudeProcess.__new__(ClaudeProcess)
        process.structured_output=True;process.buffer=b'';process.pending=[]
        key=SimpleNamespace(data='stdout',fileobj=SimpleNamespace(fileno=lambda:r))
        with pytest.raises(Refused,match='malformed'):process._read_ready(key)
    finally:os.close(r);os.close(w)
