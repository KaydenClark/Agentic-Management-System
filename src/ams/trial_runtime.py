"""Strict, tool-free Claude transport and a separate host-command sandbox probe.

No import or preflight makes a model request. ClaudeAdapter.execute is a private
caller seam for a separately authorized frozen series, not a CLI run command.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys

from ams.assessment import Refused, require

MODEL = 'claude-opus-5-5'
EFFORT = 'medium'
CANARIES = ('fixtureRead', 'fixtureWrite', 'outsideReadDenied', 'outsideWriteDenied', 'networkDenied')
ENVIRONMENT = ('PATH', 'HOME', 'TMPDIR', 'USER', 'LOGNAME', 'SHELL',
               '__CF_USER_TEXT_ENCODING', 'XPC_SERVICE_NAME')


def clean_environment(environ=None):
    """Keep OS/keychain context, never inherit provider/API credentials or config overrides."""
    values = os.environ if environ is None else environ
    return {key: values[key] for key in ENVIRONMENT if key in values}


def claude_command(binary='claude', *, system_prompt=None):
    command = [binary, '--restricted', '--safe-mode', '--tools', '', '--strict-mcp-config',
            '--mcp-config', '{"mcpServers":{}}', '--no-chrome', '--disable-slash-commands',
            '--no-session-persistence', '--permission-mode', 'dontAsk', '--permission-prompts',
            'none', '--model', MODEL, '--effort', EFFORT, '--print', '--input-format',
            'stream-json', '--output-format', 'stream-json', '--verbose']
    if system_prompt is not None:
        require(isinstance(system_prompt, str) and bool(system_prompt.strip()), 'system prompt required')
        command.extend(['--system-prompt', system_prompt])
    return command


def _count(value):
    require(type(value) is int and value >= 0, 'invalid provider token count')
    return value


def _usage(event):
    models = event.get('modelUsage')
    require(isinstance(models, dict) and set(models) == {MODEL}, 'model usage changed or missing')
    model = models[MODEL]
    require(model.get('provider') == 'firstParty' and model.get('canonicalModel') == MODEL,
            'provider/model identity changed')
    usage = event.get('usage')
    require(isinstance(usage, dict), 'provider usage missing')
    fields = {'inputTokens': 'input_tokens', 'outputTokens': 'output_tokens',
              'cacheReadInputTokens': 'cache_read_input_tokens',
              'cacheCreationInputTokens': 'cache_creation_input_tokens'}
    result = {}
    for target, source in fields.items():
        result[target] = _count(usage.get(source))
        require(type(model.get(target)) is int and model[target] == result[target],
                'provider usage totals disagree')
    tools = usage.get('server_tool_use')
    require(isinstance(tools, dict) and type(tools.get('web_search_requests')) is int
            and type(tools.get('web_fetch_requests')) is int
            and tools['web_search_requests'] == tools['web_fetch_requests'] == 0,
            'outward server tool use observed or unavailable')
    require(type(model.get('webSearchRequests')) is int and model['webSearchRequests'] == 0,
            'model web-search count changed or unavailable')
    cost = event.get('total_cost_usd')
    model_cost = model.get('costUSD')
    require(type(cost) in (int, float) and math.isfinite(cost) and cost >= 0
            and type(model_cost) in (int, float) and math.isfinite(model_cost) and model_cost >= 0
            and cost == model_cost,
            'equivalent API cost unavailable or inconsistent')
    return result, cost


class ClaudeAdapter:
    def execute(self, prompt, *, cwd=None, transport=None, system_prompt=None):
        require(isinstance(prompt, str) and bool(prompt.strip()), 'prompt required')
        self.last_failure = None
        if transport is None:
            from ams.trial_transport import ClaudeProcess
            stream = ClaudeProcess(cwd, system_prompt=system_prompt)
        else:
            stream = transport
        try:
            initialized = stream.initialize()
            require(initialized.get('commands') == [], 'custom commands unexpectedly available')
            require(stream.mcp_status() == [], 'MCP channels unexpectedly available')
            init = False
            text = []
            completed = None
            for event in stream.responses(prompt):
                require(isinstance(event, dict), 'malformed runtime message')
                kind = event.get('type')
                if kind == 'system' and event.get('subtype') == 'init':
                    require(not init and event.get('tools') == [] and event.get('mcp_servers') == [],
                            'runtime tools/MCP inventory changed or missing')
                    require(event.get('model') == MODEL and event.get('permissionMode') == 'dontAsk',
                            'runtime model/permission mode changed')
                    init = True
                elif kind == 'assistant':
                    require(init, 'assistant output before runtime inventory')
                    message = event.get('message', {})
                    require(message.get('model') == MODEL, 'assistant model changed')
                    content = message.get('content')
                    require(isinstance(content, list), 'assistant content malformed')
                    for block in content:
                        require(isinstance(block, dict) and block.get('type') in ('text', 'thinking', 'redacted_thinking'),
                                'tool use or unknown assistant block observed')
                        if block['type'] == 'text':
                            require(isinstance(block.get('text'), str), 'assistant text malformed')
                            text.append(block['text'])
                elif kind == 'result':
                    require(init and completed is None, 'runtime inventory/result missing or duplicate')
                    require(event.get('subtype') == 'success' and event.get('is_error') is False,
                            'provider execution did not succeed')
                    require(type(event.get('num_turns')) is int and event['num_turns'] == 1,
                            'unexpected number of provider turns')
                    require(event.get('permission_denials') == [], 'provider permission denial')
                    require(isinstance(event.get('result'), str) and event['result'] == ''.join(text),
                            'final result differs from observed assistant text')
                    usage, cost = _usage(event)
                    completed = {'model': MODEL, 'provider': 'firstParty', 'effort': EFFORT,
                                 'tools': [], 'mcpServers': [], 'response': event['result'],
                                 'usage': usage, 'equivalentApiCostUsd': cost,
                                 'actualSubscriptionCostUsd': None}
                elif kind not in ('system', 'rate_limit_event'):
                    raise Refused('unexpected runtime message; execution refused')
            require(completed is not None, 'provider result missing')
            return completed
        except Exception as error:
            if hasattr(stream, 'failure_diagnostic'):
                try:
                    self.last_failure = stream.failure_diagnostic(type(error).__name__, str(error))
                except (OSError, Refused):
                    self.last_failure = {'recorded': False, 'reason': 'private diagnostics unavailable'}
            raise
        finally:
            stream.close()


def shell_preflight(worker):
    """A Codex-host command probe, independent of Claude's tool-free model boundary."""
    if sys.platform != 'darwin':
        return {'status': 'unavailable', 'scope': 'host-command-canaries', 'reason': 'macOS-only probe'}
    worker = Path(worker).resolve()
    import tempfile
    with tempfile.TemporaryDirectory(prefix='ams-command-probe-') as temp:
        root = Path(temp).resolve()
        fixture = root/'fixture'; fixture.mkdir()
        (fixture/'inside').write_text('inert')
        outside = root/'outside'; outside.write_text('inert')
        profile = {':root': 'deny', ':minimal': 'read', ':tmpdir': 'deny', ':slash_tmp': 'deny',
                   str(root): 'deny', str(outside): 'deny', str(fixture): 'write'}
        # Explicit temporary denials matter: implicit tmp grants beat a root-only denial.
        table = '{'+','.join(json.dumps(k)+'='+json.dumps(v) for k, v in profile.items())+'}'
        args = ['codex', '-c', 'permissions.ams-probe.filesystem='+table,
                '-c', 'permissions.ams-probe.network.enabled=false', 'sandbox', '-P', 'ams-probe',
                '-C', str(fixture), '/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', '/bin/sh', '-c',
                'cat "$1/inside" >/dev/null 2>&1 && echo fixtureRead; '
                'echo inert >"$1/written" && echo fixtureWrite; '
                'if cat "$2" >/dev/null 2>&1; then :; else echo outsideReadDenied; fi; '
                'if (echo inert >"$3") 2>/dev/null; then :; else echo outsideWriteDenied; fi; '
                '/usr/bin/python3 -c \'import socket, errno\n'
                'try:\n s=socket.socket(); s.connect(("127.0.0.1",9))\n'
                'except OSError as e:\n'
                ' if e.errno == errno.EPERM: print("NETWORK_DENIED_EPERM")\n'
                ' else: raise\' 2>&1',
                'probe', str(fixture), str(outside), str(root/'forbidden')]
        try:
            run = subprocess.run(args, capture_output=True, text=True, timeout=15, check=False,
                                 env=clean_environment())
        except (OSError, subprocess.TimeoutExpired):
            return {'status': 'unavailable', 'scope': 'host-command-canaries', 'reason': 'sandbox command unavailable'}
        if 'sandbox_apply: Operation not permitted' in run.stderr:
            return {'status': 'unavailable', 'scope': 'host-command-canaries', 'reason': 'enclosing sandbox refuses nested Seatbelt'}
        lines = run.stdout.splitlines()
        checks = {name: name in lines for name in CANARIES[:-1]}
        # Connection refused merely means no listener; EPERM establishes a denied syscall.
        checks['networkDenied'] = 'NETWORK_DENIED_EPERM' in lines
        return {'status': 'passed' if all(checks.values()) else 'failed',
                'scope': 'host-command-canaries', 'checks': checks}
