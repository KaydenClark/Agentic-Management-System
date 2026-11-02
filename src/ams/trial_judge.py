"""Bounded judge-only JSON serialization; workers retain their original adapter."""
from __future__ import annotations

from ams.assessment import Refused,require,same_artifact
from ams import trial_runtime as runtime
from ams.trial_inputs import encoded,digest

TOOL='StructuredOutput'
MAX_TURNS=2
SCHEMA={'type':'object','properties':{
    'verdict':{'type':'string','enum':['Yes','No','Unknown']},
    'evidence':{'type':'string','minLength':1},
    'obligation':{'type':'string','minLength':1}},
    'required':['verdict','evidence','obligation'],'additionalProperties':False}


def validate_value(value):
    require(isinstance(value,dict) and set(value)=={'verdict','evidence','obligation'},
            'serialization schema fields changed')
    require(value['verdict'] in ('Yes','No','Unknown') and all(
        isinstance(value[k],str) and bool(value[k].strip())for k in ('evidence','obligation')),
        'serialization schema value invalid')
    return value


def judge_command(*,system_prompt=None):
    # No documented retry-disable flag exists. Reject first invalid serialization
    # and any second use; max-turns is the independent CLI hard ceiling.
    return runtime.claude_command(system_prompt=system_prompt)+[
        '--json-schema',encoded(SCHEMA).decode(),'--max-turns',str(MAX_TURNS)]


class ClaudeJudgeAdapter:
    def execute(self,prompt,*,cwd=None,transport=None,system_prompt=None):
        require(isinstance(prompt,str) and bool(prompt.strip()),'prompt required')
        self.last_failure=None
        if transport is None:
            from ams.trial_transport import ClaudeProcess
            stream=ClaudeProcess(cwd,system_prompt=system_prompt,structured_output=True)
        else:stream=transport
        initialized=False;use_id=None;value=None;tool_result=False;completed=None;messages=set();uses=0
        try:
            control=stream.initialize()
            require(isinstance(control,dict),'judge initialize body malformed')
            require(control.get('commands')==[],'unexpected commands')
            require(stream.mcp_status()==[],'unexpected MCP channels')
            for event in stream.responses(prompt):
                require(isinstance(event,dict),'malformed judge message')
                kind=event.get('type')
                if kind=='system' and event.get('subtype')=='init':
                    require(not initialized and event.get('tools')==[TOOL]
                            and event.get('mcp_servers')==[],'judge inventory changed')
                    require(event.get('model')==runtime.MODEL and event.get('permissionMode')=='dontAsk',
                            'judge model/permission changed')
                    initialized=True
                elif kind=='assistant':
                    require(initialized and completed is None,'assistant outside judge turn')
                    message=event.get('message')
                    require(isinstance(message,dict),'judge message object missing')
                    require(message.get('model')==runtime.MODEL,'judge fallback/model drift')
                    identity=message.get('id')
                    require(isinstance(identity,str) and bool(identity),'provider message identity missing')
                    messages.add(identity)
                    require(len(messages)<=MAX_TURNS,'judge provider-turn cap exceeded')
                    blocks=message.get('content')
                    require(isinstance(blocks,list),'judge content malformed')
                    for block in blocks:
                        require(isinstance(block,dict),'malformed judge block')
                        if block.get('type')=='tool_use':
                            uses+=1
                            require(uses==1,'repeated serialization attempt')
                            require(use_id is None and block.get('name')==TOOL,
                                    'unexpected or repeated serialization/tool use')
                            require(isinstance(block.get('id'),str) and bool(block['id']),
                                    'serialization use identity missing')
                            # Validate immediately, before consuming a tool error or
                            # a later favorable retry from this same stream.
                            value=validate_value(block.get('input'));use_id=block['id']
                        else:
                            require(block.get('type') in ('text','thinking','redacted_thinking'),
                                    'unknown judge block')
                            if block['type']=='text':require(isinstance(block.get('text'),str),'invalid text')
                elif kind=='user':
                    require(initialized and use_id is not None and not tool_result
                            and completed is None,'unexpected/duplicate tool result')
                    message=event.get('message')
                    require(isinstance(message,dict),'tool result message object missing')
                    blocks=message.get('content')
                    require(isinstance(blocks,list) and len(blocks)==1,'tool result shape changed')
                    block=blocks[0]
                    require(isinstance(block,dict) and block.get('type')=='tool_result'
                            and block.get('tool_use_id')==use_id,'serialization result ID changed')
                    require(block.get('is_error',False) is False,'serialization failed; no retry accepted')
                    require(block.get('content')=='Structured output provided successfully',
                            'serialization result content changed')
                    tool_result=True
                elif kind=='result':
                    require(initialized and completed is None and tool_result,'judge proof incomplete/duplicate')
                    require(event.get('subtype')=='success' and event.get('is_error') is False,
                            'judge structured output error/retraction')
                    turns=event.get('num_turns')
                    require(type(turns)is int and 1<=turns<=MAX_TURNS and turns==len(messages),
                            'judge turn count missing, hidden or outside cap')
                    require(event.get('permission_denials')==[],'judge permission denial')
                    final=validate_value(event.get('structured_output'))
                    require(same_artifact(final,value),'terminal serialization identity changed')
                    require(isinstance(event.get('result'),str),'judge final text missing')
                    models=event.get('modelUsage')
                    require(isinstance(models,dict) and set(models)=={runtime.MODEL}
                            and isinstance(models[runtime.MODEL],dict),'judge usage object missing')
                    usage,cost=runtime._usage(event)
                    completed={'model':runtime.MODEL,'provider':'firstParty','effort':runtime.EFFORT,
                        'tools':[TOOL],'mcpServers':[],'response':encoded(final).decode(),
                        'structuredOutput':final,'outputChannel':'result.structured_output',
                        'rawFinalText':event['result'],'schemaDigest':digest(SCHEMA),
                        'providerTurns':turns,'serializationCalls':1,'usage':usage,
                        'equivalentApiCostUsd':cost,'actualSubscriptionCostUsd':None}
                elif kind!='rate_limit_event':
                    raise Refused('unexpected judge event; no retry/fallback accepted')
            require(completed is not None,'judge terminal output missing')
            return completed
        except (Exception,KeyboardInterrupt) as error:
            diagnostic=None
            if hasattr(stream,'failure_diagnostic'):
                try:diagnostic=stream.failure_diagnostic(type(error).__name__,str(error))
                except (OSError,Refused):diagnostic={'recorded':False}
            self.last_failure={'diagnostic':diagnostic,'observedProviderTurns':len(messages)or None,
                               'turnCountComplete':False,'serializationCalls':uses,'terminalExecution':completed}
            raise
        finally:stream.close()


class InterviewAdapter:
    """Route only the two fixed role contexts; no candidate chooses capabilities."""
    def execute(self,prompt,*,cwd=None,system_prompt=None):
        from ams.trial_series import WORKER_SYSTEM,JUDGE_SYSTEM
        require(system_prompt in (WORKER_SYSTEM,JUDGE_SYSTEM),'unfrozen role context')
        adapter=ClaudeJudgeAdapter()if system_prompt==JUDGE_SYSTEM else runtime.ClaudeAdapter()
        self.last_failure=None
        try:
            result=adapter.execute(prompt,cwd=cwd,system_prompt=system_prompt)
            if system_prompt==WORKER_SYSTEM:result={**result,'providerTurns':1}
            return result
        except BaseException:
            self.last_failure=getattr(adapter,'last_failure',None)
            raise
