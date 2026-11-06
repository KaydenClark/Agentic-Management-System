"""Owned native execution. This module grants no campaign or model authority.

The controller must supply its frozen release and durable S-006 intent before
execution. Raw native output belongs only in the controller's private evidence.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import math
import json
import os
from pathlib import Path
import select
import selectors
import signal
import stat
import subprocess
import time
import uuid

from ams import recovery


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
        self.cleanup_errors = ()

    def __enter__(self):
        try:
            self.rpc.__enter__()
            self.initialization = self.rpc.call('initialize', {
                'clientInfo': {'name': 'ams-native-worker', 'version': '0.1.0'},
                'capabilities': {'experimentalApi': True}})
            self.rpc.notify('initialized')
            return self
        except BaseException as error:
            self.__exit__(type(error), error, error.__traceback__)
            raise

    def __exit__(self, exception_type, exception, traceback):
        try:
            self.close()
        except BaseException as cleanup_error:
            if exception is None:
                raise
            # Keep the original failure/interrupt and the separate cleanup
            # uncertainty; raw peer payloads do not belong in exception notes.
            exception.add_note('native cleanup remains unconfirmed (' + type(cleanup_error).__name__ + ')')

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
        if (type(result) is not dict or set(result) != {'exitCode', 'stdout', 'stderr'}
                or type(result['exitCode']) is not int
                or any(type(result[key]) is not str for key in ('stdout', 'stderr'))):
            raise NativeProtocolError('native command result is malformed')
        # Receiving bytes is not a terminal state. A malformed/uncertain
        # completion retains cancellation ownership and cannot close cleanly.
        self.commands.pop(identity)
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
        failures = []
        try:
            with _defer_interrupts():
                for identity in list(self.commands):
                    try:
                        self.terminate_command(identity)
                    except BaseException as error:
                        failures.append(error)
                try:
                    self.rpc.close()
                except BaseException as error:
                    failures.append(error)
        except BaseException as error:
            # Include an interruption delivered when the signal mask restores.
            failures.append(error)
        if failures:
            self.cleanup_errors = tuple(failures)
            self.cleanup_unconfirmed = True
            if len(failures) > 1:
                failures[0].add_note(str(len(failures) - 1) + ' additional native cleanup failures retained')
            raise failures[0]
        self.closed = True


class PrivateEvidence:
    """Immutable private effect artifacts, never a second execution ledger.

    A matching artifact proves captured execution bytes only. It supplies no
    semantic grade, owner approval, invocation permission or attempt counter.
    The trusted controller owns this directory outside the untrusted case.
    """
    LIMIT = 64 * 1024 * 1024

    def __init__(self, root, *, case_root):
        supplied, case = Path(root), Path(case_root)
        if supplied.is_symlink() or case.is_symlink() or not case.is_dir():
            raise NativeProtocolError('private evidence requires ordinary separate roots')
        self.root, case = supplied.resolve(), case.resolve()
        if self.root.is_relative_to(case) or case.is_relative_to(self.root):
            raise NativeProtocolError('private evidence must be outside the untrusted case tree')
        self.root.mkdir(mode=0o700, exist_ok=True)
        info = self.root.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise NativeProtocolError('private evidence requires an owner-only directory')

    def _target(self, key):
        if type(key) is not str or len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
            raise NativeProtocolError('invalid native evidence identity')
        return self.root / key

    def _read(self, key):
        # Reject FIFOs/devices without waiting for a peer before fstat can
        # establish that this descriptor is a bounded private ordinary file.
        fd = os.open(self._target(key), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid()
                    or info.st_mode & 0o077 or info.st_size > self.LIMIT):
                raise NativeProtocolError('native evidence is not a bounded private ordinary file')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                raw = stream.read(self.LIMIT + 1)
        finally:
            os.close(fd)
        if len(raw) > self.LIMIT:
            raise NativeProtocolError('native evidence exceeds its byte bound')
        return raw

    @staticmethod
    def _observation(key, payload, outcome, artifact=None):
        value = {'effect_key': key, 'payload_digest': payload, 'outcome': outcome,
                 'object_id': 'native-' + key if artifact else None, 'artifact_digest': artifact}
        result = {**value, 'proof_digest': recovery.digest(value)}
        recovery.validate_observation(result)
        return result

    def lookup(self, key, payload):
        self._target(key)
        self._target(payload)
        try:
            raw = self._read(key)
        except NativeProtocolError:
            return self._observation(key, payload, 'conflict')
        except OSError:
            # Missing local bytes do not prove a reserved native call absent.
            return self._observation(key, payload, 'unavailable')
        artifact = hashlib.sha256(raw).hexdigest()
        try:
            value = _json_message(raw)
            valid = (set(value) == {'format_version', 'effect_key', 'payload_digest', 'packet'}
                     and type(value['format_version']) is int and value['format_version'] == 1
                     and value['effect_key'] == key and value['payload_digest'] == payload
                     and type(value['packet']) is dict and recovery.canonical(value).encode() == raw)
        except (NativeProtocolError, ValueError, UnicodeError):
            valid = False
        return self._observation(key, payload, 'matched' if valid else 'conflict', artifact)

    def contains(self, key):
        try:
            self._target(key).lstat()
            return True
        except FileNotFoundError:
            return False
        except OSError:
            raise NativeProtocolError('native evidence availability is unknown') from None

    def publish(self, key, payload, packet):
        path = self._target(key)
        self._target(payload)
        if type(packet) is not dict:
            raise NativeProtocolError('native execution packet must be structured private evidence')
        value = {'format_version': 1, 'effect_key': key, 'payload_digest': payload, 'packet': packet}
        raw = recovery.canonical(value).encode()
        if len(raw) > self.LIMIT:
            raise NativeProtocolError('native evidence exceeds its byte bound')
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            if self._read(key) != raw:
                raise NativeProtocolError('immutable native execution artifact differs')
        else:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            directory = os.open(self.root, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        result = self.lookup(key, payload)
        if result['outcome'] != 'matched':
            raise NativeProtocolError('native execution artifact did not read back')
        return result


def run_slot(store, job, claimant, slot_index, evidence, executor, *, expected_job_digest, lease_seconds=300):
    """Consume one existing released native worker slot; never create a campaign.

    The expected job digest must come from the independently retained release,
    not the mutable request being inspected. The trusted caller owns actual
    approval/grader/capacity verification and selects the exact executor source.
    Its payload digest binds the frozen input. This helper never grants those
    judgments, changes namespace/counters or turns captured execution into a grade.
    """
    definition = recovery._job(job)
    if (job['job_digest'] != expected_job_digest or type(slot_index) is not int
            or not 0 <= slot_index < len(definition['slots'])):
        raise NativeProtocolError('native job differs from the independent release pin')
    slot = definition['slots'][slot_index]
    if (slot['effect_type'] != 'native-call' or slot['role'] != 'worker'
            or executor.payload_digest != slot['payload_digest']):
        raise NativeProtocolError('native executor input or frozen slot differs')
    claimed = store.claim(job, claimant, lease_seconds=lease_seconds)
    original_error = None
    released, result = None, None
    try:
        if claimed['job_digest'] != expected_job_digest:
            raise NativeProtocolError('claimed native job differs from the release pin')
        reserved = store.begin_effect(claimed, slot_index)
        effect = reserved['effect']
        expected_key = recovery.effect_key(definition, slot)
        if (type(reserved.get('execute')) is not bool or effect.get('effect_key') != expected_key
                or effect.get('payload_digest') != slot['payload_digest']
                or reserved['job'].get('job_digest') != expected_job_digest):
            raise NativeProtocolError('native intent readback differs from its frozen identity')
        observed = evidence.lookup(expected_key, slot['payload_digest'])
        executed = False
        if reserved['execute'] and observed['outcome'] == 'unavailable' and not evidence.contains(expected_key):
            # The durable intent precedes the invocation. An existing or
            # uncertain native intent never reaches this execution branch.
            packet = executor.execute(expected_key)
            observed = evidence.publish(expected_key, slot['payload_digest'], packet)
            executed = True
        sealed = store.observe_effect(reserved['job'], expected_key, observed)
        result = {'executed': executed, 'effect': sealed['effect'], 'observation': observed,
                  'assessment_result': 'unknown'}
    except BaseException as error:
        original_error = error
        raise
    finally:
        try:
            live = store.get_job(definition['namespace'], definition['job_id'])
            if live.get('claimant') == claimant and live.get('fence') == claimed['fence']:
                released = store.release(live)
            elif original_error is None:
                raise NativeProtocolError('native claim ownership changed before release')
        except BaseException:
            if original_error is None:
                raise
            original_error.add_note('Durable claim release unconfirmed; original intent and pending evidence remain retained.')
    return {**result, 'job': released}
