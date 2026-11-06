"""Owned native execution. This module grants no campaign or model authority.

The controller must supply its frozen release and durable S-006 intent before
execution. Raw native output belongs only in the controller's private evidence.
"""
from __future__ import annotations

from contextlib import contextmanager
import math
import os
import selectors
import signal
import subprocess
import time


class CleanupIncomplete(RuntimeError):
    """Owned process cleanup was not confirmed; execution cannot be trusted."""


class OutputLimit(RuntimeError):
    """Bounded private partial output; callers must not publish these bytes."""

    def __init__(self, stdout, stderr):
        super().__init__('native output exceeded its frozen byte limit')
        self.stdout, self.stderr = stdout, stderr


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


def run_owned(arguments, *, cwd, environment, input_bytes, timeout, cleanup_grace=1,
              max_output_bytes=16 * 1024 * 1024):
    """Run one explicit argument vector and clean only its new POSIX group.

    Ownership is installed while termination signals are deferred; the outer
    finally also covers interruption at signal restoration before communication.
    Authentication, permission and release checks remain the caller's job.
    """
    if os.name != 'posix':
        raise ValueError('native process ownership requires POSIX process groups')
    if (type(input_bytes) is not bytes or type(max_output_bytes) is not int or max_output_bytes < 1
            or type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0
            or type(cleanup_grace) not in (int, float) or not math.isfinite(cleanup_grace) or cleanup_grace <= 0):
        raise ValueError('native execution requires finite bounds and byte input')
    process = None
    deadline = time.monotonic() + timeout
    try:
        with _defer_interrupts():
            process = subprocess.Popen(arguments, cwd=cwd, env=environment,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True, bufsize=0)
        stdout, stderr = _exchange(process, arguments, input_bytes, deadline, timeout, max_output_bytes)
        return subprocess.CompletedProcess(arguments, process.returncode, stdout, stderr)
    finally:
        if process is not None:
            _close_owned_group(process, cleanup_grace)
