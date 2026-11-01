"""Strict, tool-free Claude transport and a separate host-command sandbox probe.

No import or preflight makes a model request. ClaudeAdapter.execute is a private
caller seam for a separately authorized frozen series, not a CLI run command.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time

from ams.assessment import Refused, require, same_artifact

MODEL = 'claude-opus-5-5'
EFFORT = 'medium'
CANARIES = ('fixtureRead', 'fixtureWrite', 'outsideReadDenied', 'outsideWriteDenied', 'networkDenied')
ENVIRONMENT = ('PATH', 'HOME', 'TMPDIR', 'USER', 'LOGNAME', 'SHELL',
               '__CF_USER_TEXT_ENCODING', 'XPC_SERVICE_NAME')


def clean_environment(environ=None):
    """Keep OS/keychain context, never inherit provider/API credentials or config overrides."""
    values = os.environ if environ is None else environ
    return {key: values[key] for key in ENVIRONMENT if key in values}


def claude_command(binary='claude'):
    return [binary, '--restricted', '--safe-mode', '--tools', '', '--strict-mcp-config',
            '--mcp-config', '{"mcpServers":{}}', '--no-chrome', '--disable-slash-commands',
            '--no-session-persistence', '--permission-mode', 'dontAsk', '--permission-prompts',
            'none', '--model', MODEL, '--effort', EFFORT, '--print', '--input-format',
            'stream-json', '--output-format', 'stream-json', '--verbose']


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
    require(type(cost) in (int, float) and math.isfinite(cost) and cost >= 0
            and same_artifact(cost, model.get('costUSD')),
            'equivalent API cost unavailable or inconsistent')
    return result, cost


class ClaudeAdapter:
    def execute(self, prompt, *, cwd=None, transport=None):
        require(isinstance(prompt, str) and bool(prompt.strip()), 'prompt required')
        stream = transport or _ClaudeProcess(cwd)
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
        finally:
            stream.close()


class _ClaudeProcess:
    """JSONL control handshake before sending the one authorized caller prompt."""
    def __init__(self, cwd):
        self.process = None
        env = clean_environment()
        try:
            status = subprocess.run(['claude', 'auth', 'status', '--json'], env=env,
                                    capture_output=True, text=True, timeout=15, check=False)
            auth = json.loads(status.stdout)
            require(status.returncode == 0 and auth.get('loggedIn') is True
                    and auth.get('authMethod') in ('claude.ai', 'oauth', 'subscription')
                    and not auth.get('apiKeySource'), 'subscription-only authentication unavailable')
            self.process = subprocess.Popen(claude_command(), cwd=cwd, env=env, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            raise Refused('Claude runtime/authentication unavailable') from None
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.buffer = b''
        self.pending = []

    def _send(self, value):
        try:
            self.process.stdin.write(json.dumps(value).encode() + b'\n')
            self.process.stdin.flush()
        except OSError:
            raise Refused('Claude transport write failed') from None

    def _receive(self, timeout):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.pending:
                return self.pending.pop(0)
            for key, _ in self.selector.select(min(.25, max(0, deadline-time.monotonic()))):
                chunk = os.read(key.fileobj.fileno(), 65536)
                require(bool(chunk), 'Claude transport exited before result')
                self.buffer += chunk
                require(len(self.buffer) <= 2_000_000, 'runtime message exceeds limit')
                while b'\n' in self.buffer:
                    line, self.buffer = self.buffer.split(b'\n', 1)
                    try:
                        self.pending.append(json.loads(line))
                    except ValueError:
                        raise Refused('malformed Claude JSONL') from None
        raise Refused('Claude transport timed out; preserve the attempt before retry')

    def _control(self, subtype):
        self._send({'type': 'control_request', 'request_id': subtype, 'request': {'subtype': subtype}})
        response = self._receive(15)
        require(response.get('type') == 'control_response', 'unexpected pre-prompt runtime message')
        data = response.get('response', {})
        require(data.get('request_id') == subtype and data.get('subtype') == 'success',
                'Claude initialization/control refused')
        return data.get('response', {})

    def initialize(self):
        return self._control('initialize')

    def mcp_status(self):
        return self._control('mcp_status').get('mcpServers')

    def responses(self, prompt):
        self._send({'type': 'user', 'session_id': '', 'parent_tool_use_id': None,
                    'message': {'role': 'user', 'content': prompt}})
        deadline = time.monotonic() + 55
        while time.monotonic() < deadline:
            event = self._receive(max(0, deadline-time.monotonic()))
            yield event
            if event.get('type') == 'result':
                return
        raise Refused('Claude execution timed out; preserve the attempt before retry')

    def close(self):
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.selector.close()
            for pipe in (self.process.stdin, self.process.stdout):
                pipe.close()


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
                '/usr/bin/python3 -c \'import socket; s=socket.socket(); s.connect(("127.0.0.1",9))\' 2>&1',
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
        checks['networkDenied'] = 'PermissionError' in run.stdout and 'Operation not permitted' in run.stdout
        return {'status': 'passed' if all(checks.values()) else 'failed',
                'scope': 'host-command-canaries', 'checks': checks}
