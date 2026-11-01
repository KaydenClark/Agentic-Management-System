"""Private, bounded diagnostics and JSONL IPC for the tool-free trial adapter."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import time
import uuid

from ams.assessment import Refused, require
from ams.trial_runtime import claude_command, clean_environment

class ClaudeProcess:
    """JSONL control handshake before sending the one authorized caller prompt."""
    def __init__(self, cwd):
        self.process = None
        self.selector = None
        self.stderr = b''
        self.closed = False
        self.stage = 'authentication'
        self.diagnostic_file = None
        env = clean_environment()
        try:
            status = subprocess.run(['claude', 'auth', 'status', '--json'], env=env,
                                    capture_output=True, text=True, timeout=15, check=False)
            self.stderr = status.stderr.encode()[-16384:]
            auth = json.loads(status.stdout)
            require(status.returncode == 0 and auth.get('loggedIn') is True
                    and auth.get('authMethod') in ('claude.ai', 'oauth', 'subscription')
                    and not auth.get('apiKeySource'), 'subscription-only authentication unavailable')
            self.stage = 'startup'
            self.process = subprocess.Popen(claude_command(), cwd=cwd, env=env, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            self.failure_diagnostic(type(error).__name__, str(error))
            raise Refused('Claude runtime/authentication unavailable; inspect private trial diagnostics') from None
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ, 'stdout')
        self.selector.register(self.process.stderr, selectors.EVENT_READ, 'stderr')
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
                if key.data == 'stderr':
                    if chunk:
                        self.stderr = (self.stderr+chunk)[-16384:]
                    else:
                        self.selector.unregister(key.fileobj)
                    continue
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
        self.stage = subtype
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
        self.stage = 'execution'
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
        if self.closed:
            return
        self.closed = True
        if self.process is not None:
            if self.process.poll() is None:
                self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.stderr = (self.stderr+self.process.stderr.read(65536))[-16384:]
            if self.selector is not None:
                self.selector.close()
            for pipe in (self.process.stdin, self.process.stdout, self.process.stderr):
                pipe.close()

    def failure_diagnostic(self, error_kind, reason):
        """Retain a bounded private cause, never worker prompts, stdout or auth payloads."""
        self.close()
        if self.diagnostic_file is not None:
            return str(self.diagnostic_file)
        def redact(value):
            value = re.sub(r'(?i)(?:bearer\s+|sk-ant-|sk-|sb_secret_)[A-Za-z0-9_./+=:-]+', '[redacted]', value)
            value = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[redacted]', value)
            return value[:16384]
        folder = Path('.local/trial-diagnostics')
        require(not any(p.is_symlink() for p in (folder, *folder.absolute().parents)),
                'private diagnostic path is a symlink')
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.diagnostic_file = folder/(uuid.uuid4().hex+'.json')
        data = {'schema': 1, 'kind': 'private-transport-failure', 'stage': self.stage,
                'errorKind': error_kind, 'reason': redact(reason),
                'exitStatus': self.process.returncode if self.process is not None else None,
                'stderr': redact(self.stderr.decode(errors='replace')),
                'workerPromptRecorded': False, 'stdoutRecorded': False}
        with self.diagnostic_file.open('x') as output:
            json.dump(data, output)
        self.diagnostic_file.chmod(0o600)
        return str(self.diagnostic_file)
