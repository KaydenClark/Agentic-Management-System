"""Actual owned processes, with an unrelated process as a preservation canary."""
from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from ams.native_worker import run_owned
from ams import native_worker


TREE = r'''
import json,os,pathlib,subprocess,sys
child=subprocess.Popen([sys.executable,'-c',
    'import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)'],
    stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
pathlib.Path(sys.argv[1]).write_text(json.dumps([os.getpid(),child.pid]))
if len(sys.argv)>2 and sys.argv[2]=='execute':
    import signal,time
    os.kill(os.getppid(),signal.SIGINT)
    time.sleep(60)
if len(sys.argv)>2 and sys.argv[2]=='timeout':
    import time
    time.sleep(60)
data=sys.stdin.buffer.read()
sys.stdout.buffer.write(b'received:'+data)
'''

WORKER = r'''
import json,os,pathlib,signal,subprocess,sys
from ams import native_worker
root=pathlib.Path(sys.argv[1]);phase=sys.argv[2]
tree=(root/'tree.py').read_text()
original=subprocess.Popen
def spawn(*args,**kwargs):
    process=original(*args,**kwargs)
    (root/'owner.json').write_text(json.dumps({'pid':process.pid}))
    if phase=='acquire':os.kill(os.getpid(),signal.SIGINT)
    original_wait=process.wait
    fired=False
    def wait(*args,**kwargs):
        nonlocal fired
        blocked=signal.pthread_sigmask(signal.SIG_BLOCK,set())
        if phase in ('cleanup','cleanup-exception') and signal.SIGINT in blocked and not fired:
            fired=True
            if phase=='cleanup-exception':raise KeyboardInterrupt
            os.kill(os.getpid(),signal.SIGINT)
        return original_wait(*args,**kwargs)
    process.wait=wait
    return process
native_worker.subprocess.Popen=spawn
if phase in ('cleanup-no-kill','probe-transient-denial','probe-denied'):
    original_killpg=os.killpg
    denied=False
    def killpg(group,value):
        global denied
        if value==0 and phase in ('probe-transient-denial','probe-denied'):
            if phase=='probe-denied' or not denied:
                denied=True
                raise PermissionError('planted probe denial')
        if phase!='cleanup-no-kill' or value!=signal.SIGKILL:original_killpg(group,value)
    native_worker.os.killpg=killpg
try:
    arguments=[sys.executable,'-c',tree,str(root/'owned-pids.json'),phase]
    if phase=='planted-leak':
        process=spawn(arguments,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        process.communicate(b'fixture')
    else:
        native_worker.run_owned(arguments,cwd=root,environment=dict(os.environ),input_bytes=b'fixture',
                                timeout=0.5 if phase=='timeout' else 3,cleanup_grace=0.1)
except KeyboardInterrupt:
    raise SystemExit(130)
except subprocess.TimeoutExpired:
    raise SystemExit(124)
except native_worker.CleanupIncomplete:
    raise SystemExit(125)
'''


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def dead_within(pids, seconds=3):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if not any(alive(pid) for pid in pids):
            return True
        time.sleep(0.02)
    return not any(alive(pid) for pid in pids)


def reap_owned_fixture(pids):
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_normal_exit_reaps_owned_descendant_and_preserves_unrelated_process(tmp_path):
    sentinel = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'], start_new_session=True)
    pids_file = tmp_path / 'owned-pids.json'
    try:
        result = run_owned([sys.executable, '-c', TREE, str(pids_file)],
                           cwd=tmp_path, environment=dict(os.environ), input_bytes=b'fixture input\n',
                           timeout=3, cleanup_grace=0.1)
        assert result.returncode == 0
        assert result.stdout == b'received:fixture input\n'
        pids = json.loads(pids_file.read_text())
        assert dead_within(pids), 'The owned child or descendant survived completion'
        assert sentinel.poll() is None
    finally:
        if pids_file.exists():
            reap_owned_fixture(json.loads(pids_file.read_text()))
        sentinel.kill()
        sentinel.wait(timeout=3)


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
@pytest.mark.parametrize('phase,expected', [('acquire', 130), ('execute', 130), ('cleanup', 130),
                                           ('cleanup-exception', 130), ('timeout', 124)])
def test_interruption_and_timeout_reap_owned_tree_before_controller_returns(tmp_path, phase, expected):
    (tmp_path / 'tree.py').write_text(TREE)
    (tmp_path / 'worker.py').write_text(WORKER)
    sentinel = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'], start_new_session=True)
    worker = None
    try:
        worker = subprocess.Popen([sys.executable, str(tmp_path / 'worker.py'), str(tmp_path), phase],
                                  env=dict(os.environ), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  start_new_session=True)
        stdout, stderr = worker.communicate(timeout=8)
        assert worker.returncode == expected, stderr.decode()
        owner = json.loads((tmp_path / 'owner.json').read_text())['pid']
        pids = [owner]
        if (tmp_path / 'owned-pids.json').exists():
            pids.extend(json.loads((tmp_path / 'owned-pids.json').read_text()))
        assert dead_within(pids), 'Interruption returned while an owned process remained alive'
        assert sentinel.poll() is None
    finally:
        if worker is not None and worker.poll() is None:
            worker.kill()
            worker.wait(timeout=3)
        if (tmp_path / 'owned-pids.json').exists():
            reap_owned_fixture(json.loads((tmp_path / 'owned-pids.json').read_text()))
        if (tmp_path / 'owner.json').exists():
            reap_owned_fixture([json.loads((tmp_path / 'owner.json').read_text())['pid']])
        sentinel.kill()
        sentinel.wait(timeout=3)


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_cleanup_detector_rejects_a_planted_lingering_descendant(tmp_path):
    (tmp_path / 'tree.py').write_text(TREE)
    (tmp_path / 'worker.py').write_text(WORKER)
    try:
        result = subprocess.run([sys.executable, str(tmp_path / 'worker.py'), str(tmp_path), 'planted-leak'],
                                env=dict(os.environ), capture_output=True, timeout=5)
        assert result.returncode == 0, result.stderr.decode()
        pids = json.loads((tmp_path / 'owned-pids.json').read_text())
        assert not dead_within(pids, seconds=0.1), 'The planted leak was not observed'
    finally:
        if (tmp_path / 'owned-pids.json').exists():
            reap_owned_fixture(json.loads((tmp_path / 'owned-pids.json').read_text()))


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_an_unconfirmed_group_cleanup_cannot_report_execution_success(tmp_path):
    (tmp_path / 'tree.py').write_text(TREE)
    (tmp_path / 'worker.py').write_text(WORKER)
    try:
        result = subprocess.run([sys.executable, str(tmp_path / 'worker.py'), str(tmp_path), 'cleanup-no-kill'],
                                env=dict(os.environ), capture_output=True, timeout=5)
        assert result.returncode == 125, result.stderr.decode()
        pids = json.loads((tmp_path / 'owned-pids.json').read_text())
        assert alive(pids[1]), 'The planted failed-kill control did not retain its descendant'
    finally:
        if (tmp_path / 'owned-pids.json').exists():
            reap_owned_fixture(json.loads((tmp_path / 'owned-pids.json').read_text()))


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
@pytest.mark.parametrize('phase,expected', [('probe-transient-denial', 0), ('probe-denied', 125)])
def test_probe_denial_is_unknown_until_actual_group_disappearance(tmp_path, phase, expected):
    (tmp_path / 'tree.py').write_text(TREE)
    (tmp_path / 'worker.py').write_text(WORKER)
    try:
        result = subprocess.run([sys.executable, str(tmp_path / 'worker.py'), str(tmp_path), phase],
                                env=dict(os.environ), capture_output=True, timeout=5)
        assert result.returncode == expected, result.stderr.decode()
        pids = json.loads((tmp_path / 'owned-pids.json').read_text())
        assert dead_within(pids)
    finally:
        if (tmp_path / 'owned-pids.json').exists():
            reap_owned_fixture(json.loads((tmp_path / 'owned-pids.json').read_text()))


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_output_limit_stops_and_cleans_a_flooding_process(tmp_path):
    code = '''import os,pathlib,sys
pathlib.Path(sys.argv[1]).write_text(str(os.getpid()))
while True:os.write(1,b'x'*8192)
'''
    pid_file = tmp_path / 'pid'
    try:
        with pytest.raises(native_worker.OutputLimit) as failure:
            run_owned([sys.executable, '-c', code, str(pid_file)], cwd=tmp_path,
                      environment=dict(os.environ), input_bytes=b'', timeout=3,
                      cleanup_grace=0.1, max_output_bytes=65536)
        assert len(failure.value.stdout) + len(failure.value.stderr) <= 65536
        assert dead_within([int(pid_file.read_text())])
    finally:
        if pid_file.exists():
            reap_owned_fixture([int(pid_file.read_text())])


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_large_duplex_io_does_not_deadlock_or_change_bytes(tmp_path):
    payload = b'input\x00line\n' * 200000
    code = 'import os,sys;os.write(2,b"e"*100000);sys.stdout.buffer.write(sys.stdin.buffer.read())'
    result = run_owned([sys.executable, '-c', code], cwd=tmp_path, environment=dict(os.environ),
                       input_bytes=payload, timeout=5, cleanup_grace=0.1,
                       max_output_bytes=len(payload) + 100000)
    assert result.returncode == 0
    assert result.stdout == payload
    assert result.stderr == b'e' * 100000


@pytest.mark.skipif(os.name != 'posix', reason='Owned POSIX process-group contract')
def test_nonreading_input_peer_obeys_the_same_deadline(tmp_path):
    code = 'import os,pathlib,sys,time;pathlib.Path(sys.argv[1]).write_text(str(os.getpid()));time.sleep(60)'
    pid_file = tmp_path / 'pid'
    try:
        with pytest.raises(subprocess.TimeoutExpired):
            run_owned([sys.executable, '-c', code, str(pid_file)], cwd=tmp_path,
                      environment=dict(os.environ), input_bytes=b'i' * 2000000,
                      timeout=0.5, cleanup_grace=0.1)
        assert dead_within([int(pid_file.read_text())])
    finally:
        if pid_file.exists():
            reap_owned_fixture([int(pid_file.read_text())])


RPC_PEER = r'''
import json,sys
for line in sys.stdin:
    value=json.loads(line)
    if 'id' not in value:continue
    if value['method']=='needsApproval':
        print(json.dumps({'id':700,'method':'item/commandExecution/requestApproval','params':{}}),flush=True)
    else:
        print(json.dumps({'method':'fixture/event','params':{'observed':True}}),flush=True)
        response=json.dumps({'id':value['id'],'result':value.get('params')},ensure_ascii=False).encode()+b'\n'
        for byte in response:sys.stdout.buffer.write(bytes([byte]));sys.stdout.buffer.flush()
'''


def test_owned_rpc_reads_fragmented_unicode_response_and_preserves_notifications(tmp_path):
    with native_worker.NativeRpc([sys.executable, '-u', '-c', RPC_PEER], cwd=tmp_path,
                                 environment=dict(os.environ), timeout=3, cleanup_grace=0.1) as peer:
        assert peer.call('echo', {'text': 'α\nλ'}) == {'text': 'α\nλ'}
        assert peer.events == [{'method': 'fixture/event', 'params': {'observed': True}}]


def test_native_server_approval_request_is_a_stop_boundary(tmp_path):
    with pytest.raises(native_worker.RequiredApproval):
        with native_worker.NativeRpc([sys.executable, '-u', '-c', RPC_PEER], cwd=tmp_path,
                                     environment=dict(os.environ), timeout=3, cleanup_grace=0.1) as peer:
            peer.call('needsApproval', {})
