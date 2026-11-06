"""Owned native execution. This module grants no campaign or model authority.

The controller must supply its frozen release and durable S-006 intent before
execution. Raw native output belongs only in the controller's private evidence.
"""
from __future__ import annotations

from contextlib import contextmanager
import math
import json
import os
import select
import selectors
import signal
import subprocess
import time
import uuid


class CleanupIncomplete(RuntimeError):
    """Owned process cleanup was not confirmed; execution cannot be trusted."""


class OutputLimit(RuntimeError):
    """Bounded private partial output; callers must not publish these bytes."""

    def __init__(self, stdout, stderr):
        super().__init__('native output exceeded its frozen byte limit')
        self.stdout, self.stderr = stdout, stderr


class NativeProtocolError(RuntimeError):
    """No verified native result; raw peer messages remain private."""


class RequiredApproval(NativeProtocolError):
    """A native server requested an owner decision; do not approve or retry."""


@contextmanager
def _defer_interrupts():
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
    try:
        yield
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


def _signal_owned_group(process, value):
    try:
        os.killpg(process.pid, value)
    except ProcessLookupError:
        pass


def _confirm_group_gone(process, timeout):
    deadline = time.monotonic() + timeout
    while True:
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            # A denied probe proves neither presence nor absence. Reconcile
            # with bounded read-only probes; only actual ESRCH proves gone.
            pass
        if time.monotonic() >= deadline:
            raise CleanupIncomplete('owned native process group remains unconfirmed')
        time.sleep(0.01)


def _close_owned_group(process, grace):
    # Do not mark a resource closed before poll/wait/termination has completed.
    # Pending OS interruption is delivered after the owned group is reaped.
    with _defer_interrupts():
        try:
            _signal_owned_group(process, signal.SIGTERM)
            try:
                process.wait(timeout=grace)
            except subprocess.TimeoutExpired:
                pass
        finally:
            try:
                # A normally exited leader may leave descendants behind.
                _signal_owned_group(process, signal.SIGKILL)
                process.wait(timeout=max(1, grace))
                _confirm_group_gone(process, max(1, grace))
            finally:
                for pipe in (process.stdin, process.stdout, process.stderr):
                    if pipe is not None:
                        pipe.close()


def _exchange(process, arguments, input_bytes, deadline, timeout, output_limit):
    output = {'stdout': bytearray(), 'stderr': bytearray()}
    sent = 0
    with selectors.DefaultSelector() as ready:
        for name in output:
            pipe = getattr(process, name)
            os.set_blocking(pipe.fileno(), False)
            ready.register(pipe, selectors.EVENT_READ, name)
        os.set_blocking(process.stdin.fileno(), False)
        if input_bytes:
            ready.register(process.stdin, selectors.EVENT_WRITE, 'stdin')
        else:
            process.stdin.close()
        while ready.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(arguments, timeout, bytes(output['stdout']), bytes(output['stderr']))
            for key, _ in ready.select(remaining):
                pipe, name = key.fileobj, key.data
                if name == 'stdin':
                    try:
                        sent += os.write(pipe.fileno(), memoryview(input_bytes)[sent:sent + 65536])
                    except BlockingIOError:
                        continue
                    except BrokenPipeError:
                        sent = len(input_bytes)
                    if sent == len(input_bytes):
                        ready.unregister(pipe)
                        pipe.close()
                else:
                    try:
                        block = os.read(pipe.fileno(), 65536)
                    except BlockingIOError:
                        continue
                    if not block:
                        ready.unregister(pipe)
                        pipe.close()
                        continue
                    available = output_limit - sum(map(len, output.values()))
                    output[name].extend(block[:available])
                    if len(block) > available:
                        raise OutputLimit(bytes(output['stdout']), bytes(output['stderr']))
    try:
        process.wait(timeout=max(0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        raise subprocess.TimeoutExpired(arguments, timeout, bytes(output['stdout']), bytes(output['stderr'])) from None
    return bytes(output['stdout']), bytes(output['stderr'])


@contextmanager
def owned_process(arguments, *, cwd, environment, cleanup_grace=1):
    """Own only this new POSIX group; native child sessions need host cancellation.

    Ownership is installed while termination signals are deferred; the outer
    finally also covers interruption at signal restoration before communication.
    """
    if os.name != 'posix':
        raise ValueError('native process ownership requires POSIX process groups')
    process = None
    try:
        with _defer_interrupts():
            process = subprocess.Popen(arguments, cwd=cwd, env=environment,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True, bufsize=0)
        yield process
    finally:
        if process is not None:
            _close_owned_group(process, cleanup_grace)


def run_owned(arguments, *, cwd, environment, input_bytes, timeout, cleanup_grace=1,
              max_output_bytes=16 * 1024 * 1024):
    """Run bounded byte IO; authentication, permission and release are external."""
    if (type(input_bytes) is not bytes or type(max_output_bytes) is not int or max_output_bytes < 1
            or type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0
            or type(cleanup_grace) not in (int, float) or not math.isfinite(cleanup_grace) or cleanup_grace <= 0):
        raise ValueError('native execution requires finite bounds and byte input')
    deadline = time.monotonic() + timeout
    with owned_process(arguments, cwd=cwd, environment=environment, cleanup_grace=cleanup_grace) as process:
        stdout, stderr = _exchange(process, arguments, input_bytes, deadline, timeout, max_output_bytes)
        return subprocess.CompletedProcess(arguments, process.returncode, stdout, stderr)


def _json_message(raw):
    def constant(_):
        raise ValueError('non-finite native JSON number')

    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise NativeProtocolError('native protocol contains duplicate fields')
            result[key] = value
        return result
    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeDecodeError):
        raise NativeProtocolError('native protocol is not strict JSON') from None
    if type(value) is not dict or value.get('jsonrpc', '2.0') != '2.0':
        raise NativeProtocolError('native protocol message shape differs')
    return value


class NativeRpc:
    """Bounded stdio for one owned native server; it grants no model authority.

    Host adapters must cancel their own active turns/command sessions before
    closing this transport. Process-group cleanup alone cannot cover sessions
    detached by a native tool host. All events and raw output remain private.
    """
    def __init__(self, arguments, *, cwd, environment, timeout=15, cleanup_grace=1,
                 max_output_bytes=16 * 1024 * 1024):
        if (type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0
                or type(max_output_bytes) is not int or max_output_bytes < 1):
            raise ValueError('native RPC requires finite transport bounds')
        self.arguments, self.cwd, self.environment = tuple(arguments), cwd, dict(environment)
        self.timeout, self.cleanup_grace, self.limit = timeout, cleanup_grace, max_output_bytes
        self.events, self._responses, self._pending = [], {}, set()
        self._next_id, self._event_cursor = 1, 0
        self._raw, self._line = {'stdout': bytearray(), 'stderr': bytearray()}, bytearray()
        self._process, self._owner = None, None
        self._cleanup_unconfirmed = False

    def __enter__(self):
        self._owner = owned_process(self.arguments, cwd=self.cwd, environment=self.environment,
                                    cleanup_grace=self.cleanup_grace)
        try:
            self._process = self._owner.__enter__()
            self._readers = {self._process.stdout.fileno(): 'stdout', self._process.stderr.fileno(): 'stderr'}
            for pipe in (self._process.stdin, self._process.stdout, self._process.stderr):
                os.set_blocking(pipe.fileno(), False)
            return self
        except BaseException:
            self.close()
            raise

    def __exit__(self, *exception):
        self.close()

    def close(self):
        if self._cleanup_unconfirmed:
            raise CleanupIncomplete('native RPC cleanup remains unconfirmed; operator reconciliation required')
        if self._owner is not None:
            owner = self._owner
            try:
                owner.__exit__(None, None, None)
            except BaseException:
                self._cleanup_unconfirmed = True
                raise
            self._owner, self._process = None, None

    def _message(self, value):
        if 'method' in value:
            if 'id' in value:
                raise RequiredApproval('native server decision requires approval; execution held')
            if (type(value['method']) is not str or set(value) - {'method', 'params', 'jsonrpc', 'emittedAtMs'}
                    or ('emittedAtMs' in value and (type(value['emittedAtMs']) is not int or value['emittedAtMs'] < 0))):
                raise NativeProtocolError('native notification shape differs')
            self.events.append(value)
        elif ('id' in value and type(value['id']) is int and value['id'] in self._pending
              and value['id'] not in self._responses and ('result' in value) != ('error' in value)
              and not (set(value) - {'id', 'result', 'error', 'jsonrpc'})):
            self._responses[value['id']] = value
        else:
            raise NativeProtocolError('native response identity differs or repeats')

    def _pump(self, deadline, pending=b''):
        if self._process is None:
            raise NativeProtocolError('native RPC transport is closed')
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise NativeProtocolError('native RPC deadline expired')
        readable, writable, _ = select.select(list(self._readers),
                                              [self._process.stdin.fileno()] if pending else [], [], remaining)
        sent = 0
        if writable:
            try:
                sent = os.write(writable[0], memoryview(pending)[:65536])
            except BlockingIOError:
                pass
            except BrokenPipeError:
                raise NativeProtocolError('native RPC input closed') from None
        for fd in readable:
            name = self._readers[fd]
            try:
                block = os.read(fd, 65536)
            except BlockingIOError:
                continue
            if not block:
                self._readers.pop(fd)
                if name == 'stdout':
                    raise NativeProtocolError('native RPC output closed before requested evidence')
                continue
            available = self.limit - sum(map(len, self._raw.values()))
            self._raw[name].extend(block[:available])
            if len(block) > available:
                raise OutputLimit(bytes(self._raw['stdout']), bytes(self._raw['stderr']))
            if name == 'stdout':
                self._line.extend(block)
                while b'\n' in self._line:
                    line, _, rest = self._line.partition(b'\n')
                    self._line[:] = rest
                    self._message(_json_message(line))
        return sent

    def _send(self, value, deadline):
        text = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode() + b'\n'
        offset = 0
        while offset < len(text):
            offset += self._pump(deadline, memoryview(text)[offset:])

    def notify(self, method, params=None):
        value = {'method': method}
        if params is not None:
            value['params'] = params
        self._send(value, time.monotonic() + self.timeout)

    def request(self, method, params=None):
        identity = self._next_id
        self._next_id += 1
        self._pending.add(identity)
        self._send({'id': identity, 'method': method, 'params': params}, time.monotonic() + self.timeout)
        return identity

    def wait(self, identity, *, timeout=None):
        if identity not in self._pending:
            raise NativeProtocolError('unknown native request identity')
        deadline = time.monotonic() + (self.timeout if timeout is None else timeout)
        while identity not in self._responses:
            self._pump(deadline)
        value = self._responses.pop(identity)
        self._pending.remove(identity)
        if 'error' in value:
            raise NativeProtocolError('native server refused the requested operation')
        return value['result']

    def call(self, method, params=None, *, timeout=None):
        return self.wait(self.request(method, params), timeout=timeout)

    def next_event(self, *, timeout=None):
        deadline = time.monotonic() + (self.timeout if timeout is None else timeout)
        while self._event_cursor >= len(self.events):
            self._pump(deadline)
        event = self.events[self._event_cursor]
        self._event_cursor += 1
        return event


class CodexHost:
    """A dedicated server and its connection-scoped standalone tool commands.

    This pre-model seam uses supported command cancellation before terminating
    the server group. It does not yet establish model-turn cleanup or qualify
    a case, and accepts no model-call authority from these utility commands.
    """
    def __init__(self, arguments, *, cwd, environment, timeout=15, cleanup_grace=1):
        self.rpc = NativeRpc(arguments, cwd=cwd, environment=environment,
                             timeout=timeout, cleanup_grace=cleanup_grace)
        self.cwd, self.timeout = str(cwd), timeout
        self.commands = {}
        self.closed, self.cleanup_unconfirmed = False, False

    def __enter__(self):
        try:
            self.rpc.__enter__()
            self.initialization = self.rpc.call('initialize', {
                'clientInfo': {'name': 'ams-native-worker', 'version': '0.1.0'},
                'capabilities': {'experimentalApi': True}})
            self.rpc.notify('initialized')
            return self
        except BaseException:
            self.close()
            raise

    def __exit__(self, *exception):
        self.close()

    def start_command(self, arguments, *, timeout_ms=10000, output_bytes_cap=65536):
        if self.closed or self.cleanup_unconfirmed:
            raise NativeProtocolError('native command host is not available')
        identity = 'ams-command-' + uuid.uuid4().hex
        # This client is synchronous. Install ownership before a send that may
        # be interrupted after the host started a separate process session.
        request = self.rpc._next_id
        self.commands[identity] = request
        observed = self.rpc.request('command/exec', {
            'command': list(arguments), 'cwd': self.cwd, 'processId': identity,
            'streamStdoutStderr': True, 'timeoutMs': timeout_ms, 'outputBytesCap': output_bytes_cap})
        if observed != request:
            raise NativeProtocolError('native command request identity differs')
        return identity

    def wait_command(self, identity, *, timeout=None):
        if identity not in self.commands:
            raise NativeProtocolError('native command is not owned by this connection')
        result = self.rpc.wait(self.commands[identity], timeout=timeout)
        self.commands.pop(identity)
        if (type(result) is not dict or set(result) != {'exitCode', 'stdout', 'stderr'}
                or type(result['exitCode']) is not int
                or any(type(result[key]) is not str for key in ('stdout', 'stderr'))):
            raise NativeProtocolError('native command result is malformed')
        return result

    def terminate_command(self, identity):
        if identity not in self.commands:
            raise NativeProtocolError('native command is not owned by this connection')
        self.rpc.call('command/exec/terminate', {'processId': identity}, timeout=min(5, self.timeout))
        return self.wait_command(identity, timeout=min(5, self.timeout))

    def close(self):
        if self.cleanup_unconfirmed:
            raise CleanupIncomplete('native tool cancellation remains unconfirmed')
        if self.closed:
            return
        try:
            with _defer_interrupts():
                try:
                    for identity in list(self.commands):
                        self.terminate_command(identity)
                finally:
                    self.rpc.close()
            self.closed = True
        except BaseException:
            self.cleanup_unconfirmed = True
            raise
