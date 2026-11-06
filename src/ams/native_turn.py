"""Bounded native turn software; external owners supply all call authority.

Configuration and captured bytes are not runtime-model/skill/cleanup proof.
This module neither grades a case nor grants campaign or installation authority.
"""
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shlex
import stat
import subprocess
import time
import uuid

from ams import native_worker, recovery

NativeProtocolError = native_worker.NativeProtocolError
CleanupIncomplete = native_worker.CleanupIncomplete
DISABLED_FEATURES = ('apps', 'multi_agent', 'multi_agent_v2', 'plugins', 'remote_plugin',
                     'browser_use', 'browser_use_external', 'browser_use_full_cdp_access',
                     'computer_use', 'image_generation', 'in_app_browser', 'code_mode_host',
                     'memories', 'goals', 'realtime_conversation', 'skill_mcp_dependency_install',
                     'unbounded_connection_retries')
ENVIRONMENT = {'HOME', 'USER', 'LOGNAME', 'TMPDIR', 'CODEX_HOME', 'LANG', 'LC_CTYPE',
               '__CF_USER_TEXT_ENCODING', 'PATH'}
FIELDS = {'format_version', 'case_digest', 'skills_commit', 'source_commit', 'release_digest',
          'cwd', 'prompt', 'model', 'provider', 'effort', 'skill', 'sources', 'fixture_digest',
          'profile_id', 'profile_digest', 'origins_digest', 'command', 'resolved_executable', 'environment', 'limits'}


def require(condition, message):
    if not condition:
        raise recovery.Refused(message)


def hex_digest(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _remaining(deadline):
    value = deadline - time.monotonic()
    if value <= 0:
        raise NativeProtocolError('native total deadline expired')
    return value


def file_digest(path, limit=512 * 1024 * 1024):
    """Hash ordinary descriptors without blocking on a FIFO or following a link."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size <= limit,
                'source is not a bounded ordinary file')
        value, size = hashlib.sha256(), 0
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            while block := stream.read(1024 * 1024):
                size += len(block)
                require(size <= limit, 'source exceeds its byte bound')
                value.update(block)
        return value.hexdigest()
    finally:
        os.close(fd)


def _source_matches(path, expected):
    if type(expected) is str:
        return file_digest(path) == expected
    return (Path(path).is_symlink() and os.readlink(path) == expected['link']
            and file_digest(Path(path).resolve()) == expected['sha256'])


def fixture_digest(root):
    """Independent byte/mode readback, including index, refs and dirty/untracked files."""
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'fixture root is not ordinary')
    rows = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        require(len(rows) + len(dirs) + len(files) <= 4096, 'fixture inventory exceeds its bound')
        for name in dirs:
            require(not (Path(directory) / name).is_symlink(), 'fixture directory link is not frozen')
        for name in sorted(files):
            path = Path(directory) / name
            rows.append([str(path.relative_to(root)), stat.S_IMODE(path.lstat().st_mode), file_digest(path, 16 * 1024 * 1024)])
    return recovery.digest(sorted(rows))


class NativeCall:
    """Private immutable input bytes, independently bound by a release reader."""
    def __init__(self, manifest):
        require(type(manifest) is dict and manifest.keys() == FIELDS, 'native input fields differ')
        self._text = recovery.canonical(manifest)
        self.payload_digest = hashlib.sha256(self._text.encode()).hexdigest()
        c = self.data
        require(c['format_version'] == 1 and type(c['format_version']) is int, 'native input version differs')
        require(all(hex_digest(c[key]) for key in ('case_digest', 'release_digest', 'fixture_digest',
                                                   'profile_digest', 'origins_digest')), 'native input digests differ')
        require(all(type(c[key]) is str and len(c[key]) == 40 and all(x in '0123456789abcdef' for x in c[key])
                    for key in ('skills_commit', 'source_commit')), 'native source identity differs')
        require(all(type(c[key]) is str and 0 < len(c[key]) <= 256 for key in ('model', 'provider', 'effort', 'profile_id')),
                'exact model/provider/effort/profile is required')
        require(type(c['prompt']) is str and 0 < len(c['prompt'].encode()) <= 256 * 1024, 'native prompt bound differs')
        require(type(c['skill']) is dict and c['skill'].keys() == {'name', 'path', 'sha256'}
                and type(c['skill']['name']) is str and c['skill']['name'] and hex_digest(c['skill']['sha256']),
                'native skill mapping differs')
        require(type(c['sources']) is dict and c['sources'] and len(c['sources']) <= 4096,
                'source closure is missing or unbounded')
        for path, value in c['sources'].items():
            require(type(path) is str and Path(path).is_absolute(), 'source closure identity differs')
            require('.eval' not in Path(path).parts, 'protected evaluation material is outside runtime closure')
            require(hex_digest(value) or (type(value) is dict and value.keys() == {'link', 'sha256'}
                    and type(value['link']) is str and value['link'] and hex_digest(value['sha256'])),
                    'source closure file/link identity differs')
        require(c['sources'].get(c['skill']['path']) == c['skill']['sha256'], 'skill is outside the source closure')
        require(type(c['cwd']) is str and Path(c['cwd']).is_absolute(), 'fixture cwd must be absolute')
        require(type(c['command']) is list and c['command'] and all(type(x) is str and x for x in c['command'])
                and Path(c['command'][0]).is_absolute(), 'native launch must use structured absolute arguments')
        require(type(c['resolved_executable']) is str and Path(c['resolved_executable']).is_absolute()
                and hex_digest(c['sources'].get(c['resolved_executable'])), 'launch executable is outside the source closure')
        require(type(c['environment']) is dict and c['environment'].keys() <= ENVIRONMENT
                and all(type(v) is str for v in c['environment'].values()), 'native environment is not allowlisted')
        for key in ('HOME', 'CODEX_HOME'):
            require(c['environment'].get(key) == os.environ.get(key), 'native home overrides are forbidden')
        limits = c['limits']
        require(type(limits) is dict and limits.keys() == {'timeout_seconds', 'cancel_seconds', 'max_output_bytes',
                                                          'max_events', 'capacity_max_age_seconds'}, 'native limits differ')
        for key in ('timeout_seconds', 'cancel_seconds'):
            require(type(limits[key]) in (int, float) and math.isfinite(limits[key]) and 0 < limits[key] <= 120,
                    'native deadlines must be finite and bounded')
        for key, high in (('max_output_bytes', 64 * 1024 * 1024), ('max_events', 100000), ('capacity_max_age_seconds', 300)):
            require(type(limits[key]) is int and 0 < limits[key] <= high, 'native evidence limits differ')

    @property
    def data(self):
        return json.loads(self._text)

    def verify_sources(self):
        c = self.data
        try:
            require(str(Path(c['command'][0]).resolve()) == c['resolved_executable'], 'launch executable alias changed')
            require(all(_source_matches(path, expected) for path, expected in c['sources'].items()), 'source closure changed')
            require(fixture_digest(c['cwd']) == c['fixture_digest'], 'fixture/index/unrelated bytes changed')
        except OSError:
            raise recovery.Refused('source/fixture readback is unavailable') from None


def _read_grant(path, call):
    c = call.data
    target, case = Path(path), Path(c['cwd'])
    require(target.is_absolute(), 'effective containment read grant is not absolute')
    require('.eval' not in target.parts, 'effective containment exposes protected evaluation material')
    if target == case or target.is_relative_to(case):
        return
    if str(target) in c['sources']:
        return
    require(target.is_dir() and not target.is_symlink() and not case.is_relative_to(target),
            'effective containment read grant exceeds the frozen closure')
    count = 0
    for directory, dirs, files in os.walk(target, followlinks=False):
        require('.eval' not in dirs, 'effective containment exposes protected evaluation material')
        for name in [*files, *(name for name in dirs if (Path(directory) / name).is_symlink())]:
            count += 1
            require(count <= 4096 and str(Path(directory) / name) in c['sources'],
                    'effective containment directory exceeds the frozen source closure')
    require(count > 0, 'effective containment empty directory is not a frozen source grant')


def _timestamp(value):
    require(type(value) is str, 'readiness timestamp is missing')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise recovery.Refused('readiness timestamp is malformed') from None
    require(parsed.tzinfo is not None, 'readiness timestamp lacks its zone')
    return parsed


def _fresh(value, call):
    age = (datetime.now(timezone.utc) - _timestamp(value)).total_seconds()
    require(0 <= age <= call.data['limits']['capacity_max_age_seconds'], 'capacity evidence is stale or future')


def _readiness(reader, call, job):
    proof = reader(call, job)
    fields = {'status', 'mode', 'release_digest', 'input_digest', 'job_digest', 'approval_digest',
              'labels_digest', 'grader_digest', 'capacity'}
    require(type(proof) is dict and proof.keys() == fields and proof['status'] == 'accepted'
            and proof['mode'] in ('native', 'inert'), 'accepted external readiness is incomplete')
    require(all(hex_digest(proof[key]) for key in fields - {'status', 'mode', 'capacity'}),
            'accepted external artifact identities are missing')
    require(proof['release_digest'] == call.data['release_digest'] and proof['input_digest'] == call.payload_digest
            and proof['job_digest'] == job['job_digest'], 'external release/input/job identity differs')
    capacity = proof['capacity']
    require(type(capacity) is dict and capacity.keys() == {'state', 'observed_at', 'proof_digest'}
            and capacity['state'] == 'available' and hex_digest(capacity['proof_digest']), 'external capacity is held')
    _fresh(capacity['observed_at'], call)
    if proof['mode'] == 'inert':
        definition = recovery._job(job)
        require(definition['synthetic'] and definition['is_test'], 'inert proof cannot authorize a production identity')
    return proof


def _gates(job, call, proof, *, claimant=None, fence=None):
    require(job.get('approved') is True and job.get('capacity') == 'available'
            and job.get('stop_requested') is False and job.get('terminal_state') is None, 'durable execution gate is held')
    require(job.get('capacity_digest') == proof['capacity']['proof_digest'], 'capacity proof differs from durable gates')
    _fresh(job.get('capacity_observed_at'), call)
    if claimant is not None:
        require(job.get('claimant') == claimant and job.get('fence') == fence
                and _timestamp(job.get('lease_until')) > datetime.now(timezone.utc), 'native claim/fence/lease is no longer current')


class _Trace:
    """Private bounded evidence only; O remains the sole job/attempt authority."""
    def __init__(self, root, call, effect_key):
        root, case = Path(root), Path(call.data['cwd']).resolve()
        require(not root.is_symlink(), 'private trace root cannot be a link')
        root = root.resolve()
        require(not root.is_relative_to(case) and not case.is_relative_to(root), 'trace must be outside the case')
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = root.stat()
        require(info.st_uid == os.getuid() and not info.st_mode & 0o077, 'trace root must be owner-only')
        self.path = root / (effect_key + '-' + uuid.uuid4().hex + '.jsonl')
        self.stream = os.fdopen(os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600), 'wb')
        self.size, self.limit = 0, call.data['limits']['max_output_bytes']

    def record(self, value):
        raw = recovery.canonical(value).encode() + b'\n'
        require(self.size + len(raw) <= self.limit, 'private native capture exceeds its byte bound')
        self.stream.write(raw)
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.size += len(raw)

    def close(self):
        self.stream.close()


class _TurnRpc(native_worker.NativeRpc):
    def __init__(self, *args, max_events, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests, self.sink = [], None
        self.message_count, self.max_events = 0, max_events
        self.active_deadline = None

    def __enter__(self):
        # Keep the reviewed general owner unchanged. This turn transport needs
        # a caller-owned aggregate close deadline, including the host group.
        try:
            _remaining(self.active_deadline)
            with native_worker._defer_interrupts():
                self._process = subprocess.Popen(self.arguments, cwd=self.cwd, env=self.environment,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    start_new_session=True, bufsize=0)
            self._readers = {self._process.stdout.fileno(): 'stdout', self._process.stderr.fileno(): 'stderr'}
            for pipe in (self._process.stdin, self._process.stdout, self._process.stderr):
                os.set_blocking(pipe.fileno(), False)
            return self
        except BaseException:
            # NativeTurnSession retains and closes any acquired process using
            # its independent cleanup budget, preserving the original error.
            raise

    def request(self, method, params=None):
        self.timeout = _remaining(self.active_deadline)
        return super().request(method, params)

    def _pump(self, deadline, pending=b''):
        _remaining(self.active_deadline)
        return super()._pump(min(deadline, self.active_deadline), pending)

    def close(self, deadline=None):
        if self._cleanup_unconfirmed:
            raise CleanupIncomplete('native bounded host cleanup remains unconfirmed')
        if self._process is None:
            return
        process, errors = self._process, []
        try:
            with native_worker._defer_interrupts():
                try:
                    native_worker._signal_owned_group(process, native_worker.signal.SIGTERM)
                    try:
                        process.wait(timeout=min(0.02, max(0, (deadline - time.monotonic()) / 3)))
                    except subprocess.TimeoutExpired:
                        pass
                except BaseException as error:
                    errors.append(error)
                try:
                    # Even an exited leader may have left same-group children.
                    native_worker._signal_owned_group(process, native_worker.signal.SIGKILL)
                    process.wait(timeout=max(0, deadline - time.monotonic()))
                    native_worker._confirm_group_gone(process, max(0, deadline - time.monotonic()))
                except BaseException as error:
                    errors.append(error)
                finally:
                    for pipe in (process.stdin, process.stdout, process.stderr):
                        if pipe is not None:
                            pipe.close()
        except BaseException as error:
            errors.append(error)
        if time.monotonic() >= deadline:
            errors.append(CleanupIncomplete('native aggregate cleanup deadline expired'))
        if errors:
            self._cleanup_unconfirmed = True
            raise CleanupIncomplete('owned native host cleanup is unconfirmed within its deadline') from errors[0]
        self._process = None

    def _message(self, value):
        self.message_count += 1
        if self.message_count > self.max_events:
            raise NativeProtocolError('native message count exceeds its frozen bound')
        if self.sink is not None:
            self.sink(value)
        if 'method' in value and 'id' in value:
            self.requests.append(value)
        super()._message(value)


class NativeTurnSession:
    """One dedicated protocol session; run_native_slot is the authority boundary.

    The default native transport cannot consume an inert test release. Tests
    provide their own inert subclass; no production bypass switch is exposed.
    """
    transport_kind = 'native'

    def __init__(self, call, *, trace_root, cleanup_reader=None):
        self.call, self.trace_root, self.cleanup_reader = call, trace_root, cleanup_reader
        c, limits = call.data, call.data['limits']
        self.rpc = _TurnRpc(c['command'], cwd=c['cwd'], environment=c['environment'],
                            timeout=max(limits['timeout_seconds'], limits['cancel_seconds']), cleanup_grace=0.1,
                            max_output_bytes=limits['max_output_bytes'], max_events=limits['max_events'])
        self.thread_id, self.turn_id, self.turn_request = None, None, None
        self.thread_requested, self.turn_requested = False, False
        self.terminal, self.final_response, self.incomplete_reason = None, None, None
        self.active_items, self.completed_items, self.turn_ids = set(), {}, set()
        self.skill_load = {'status': 'unknown'}
        self.closed_success, self.cleanup_unconfirmed = False, False
        self.cleanup, self.cleanup_errors, self.trace = {'status': 'unknown'}, (), None
        self.server_pid = None
        self.deadline = time.monotonic() + limits['timeout_seconds']
        self.cleanup_deadline = None

    def __enter__(self):
        try:
            self.rpc.active_deadline = self.deadline
            _remaining(self.deadline)
            self.trace = _Trace(self.trace_root, self.call, self.call.payload_digest)
            self.trace.record({'kind': 'native-preparation-not-execution', 'input_digest': self.call.payload_digest})
            self.rpc.sink = self.trace.record
            self.rpc.__enter__()
            self.server_pid = self.rpc._process.pid
            self.rpc.call('initialize', {'clientInfo': {'name': 'ams-native-turn', 'version': '0.1.0'},
                                         'capabilities': {'experimentalApi': True}})
            self.rpc.notify('initialized')
            return self
        except BaseException as error:
            self.__exit__(type(error), error, error.__traceback__)
            raise

    def __exit__(self, kind, error, traceback):
        try:
            self.close()
        except BaseException as cleanup:
            if error is None:
                raise
            error.add_note('native turn cleanup remains unconfirmed (' + type(cleanup).__name__ + ')')

    def prepare(self):
        _remaining(self.deadline)
        self._configuration()
        self._start_thread()
        self.prepared = True
        _remaining(self.deadline)

    def _configuration(self):
        c = self.call.data
        value = self.rpc.call('config/read', {'cwd': c['cwd'], 'includeLayers': True})
        require(type(value) is dict and type(value.get('config')) is dict and type(value.get('origins')) is dict,
                'effective containment readback is missing')
        config = value['config']
        require(recovery.digest(value['origins']) == c['origins_digest'], 'effective containment origins changed')
        features = config.get('features', {})
        require(all(features.get(key) is False for key in DISABLED_FEATURES) and features.get('hooks') is True,
                'effective containment features are missing or enabled')
        require(config.get('web_search') == 'disabled' and config.get('default_permissions') == c['profile_id'],
                'effective containment web/profile differs')
        require(config.get('forced_login_method') == 'chatgpt'
                and config.get('shell_environment_policy') == {'inherit': 'none', 'set': {'PATH': '/usr/bin:/bin'}},
                'effective containment subscription/environment differs')
        require(type(config.get('permissions')) is dict and c['profile_id'] in config['permissions']
                and recovery.digest(config['permissions'][c['profile_id']]) == c['profile_digest'],
                'effective containment profile bytes differ')
        profile = config['permissions'][c['profile_id']]
        require(type(profile) is dict and profile.keys() == {'filesystem', 'network'}
                and profile['network'] == {'enabled': False} and type(profile['filesystem']) is dict
                and profile['filesystem'].get(':root') == 'deny'
                and profile['filesystem'].get(':tmpdir') == 'deny' and profile['filesystem'].get(':slash_tmp') == 'deny'
                and profile['filesystem'].get(c['cwd']) == 'read'
                and all(v in ('read', 'deny') for v in profile['filesystem'].values()), 'effective containment grants differ')
        for path, grant in profile['filesystem'].items():
            if grant == 'read' and path != ':minimal':
                _read_grant(path, self.call)
        servers = config.get('mcp_servers')
        require(type(servers) is dict and all(type(v) is dict and v.get('enabled') is False for v in servers.values()),
                'effective containment has enabled or unknown connectors')
        # Never start connector discovery while the configuration is enabled/unknown.
        inventory = self.rpc.call('mcpServerStatus/list', {'limit': 1})
        require(type(inventory) is dict and inventory.get('data') == [] and inventory.get('nextCursor') is None,
                'effective containment connector inventory is not empty')
        profiles = self.rpc.call('permissionProfile/list', {'cwd': c['cwd'], 'limit': 100})
        require(type(profiles) is dict and profiles.get('nextCursor') is None and type(profiles.get('data')) is list
                and any(p.get('id') == c['profile_id'] and p.get('allowed') is True for p in profiles['data'] if type(p) is dict),
                'effective containment profile cannot be selected or is unbounded')

    def _start_thread(self):
        c = self.call.data
        self.thread_requested = True
        response = self.rpc.call('thread/start', {'cwd': c['cwd'], 'model': c['model'], 'modelProvider': c['provider'],
            'permissions': c['profile_id'], 'runtimeWorkspaceRoots': [c['cwd']], 'allowProviderModelFallback': False,
            'approvalPolicy': 'never', 'approvalsReviewer': 'user', 'ephemeral': False, 'dynamicTools': []})
        thread = response.get('thread', {}) if type(response) is dict else {}
        require(type(thread.get('id')) is str and thread['id'], 'native thread identity is missing')
        self.thread_id = thread['id']
        require(response.get('model') == c['model'] and response.get('modelProvider') == c['provider']
                and response.get('reasoningEffort') == c['effort'] and response.get('cwd') == c['cwd']
                and response.get('approvalPolicy') == 'never' and response.get('approvalsReviewer') == 'user'
                and response.get('activePermissionProfile', {}).get('id') == c['profile_id']
                and response.get('runtimeWorkspaceRoots') == [c['cwd']], 'native configured model/profile identity differs')
        sources = response.get('instructionSources')
        require(type(sources) is list and all(type(path) is str and path in c['sources'] for path in sources),
                'native instruction source is not frozen')
        self.configured_model = response['model']
        self._drain()

    def _bind_turn(self, value):
        if (type(value) is not dict or type(value.get('id')) is not str or not value['id']
                or value.get('status') not in ('inProgress', 'completed', 'failed', 'interrupted')
                or type(value.get('items')) is not list):
            raise NativeProtocolError('native turn identity is malformed')
        identity = value['id']
        self.turn_ids.add(identity)
        if self.turn_id is not None and self.turn_id != identity:
            raise NativeProtocolError('native turn identity changed')
        self.turn_id = identity

    def _item(self, item, complete):
        c = self.call.data
        if type(item) is not dict or type(item.get('id')) is not str or not item['id'] or type(item.get('type')) is not str:
            raise NativeProtocolError('native item identity is malformed')
        identity, kind = item['id'], item['type']
        if kind not in ('commandExecution', 'agentMessage', 'userMessage', 'reasoning', 'plan'):
            raise NativeProtocolError('native item exceeds the frozen local tool grant')
        if kind in ('agentMessage', 'plan') and type(item.get('text')) is not str:
            raise NativeProtocolError('native message text is malformed')
        if kind == 'agentMessage' and item.get('phase') not in (None, 'commentary', 'final_answer'):
            raise NativeProtocolError('native message phase differs from the pinned schema')
        if kind == 'userMessage' and type(item.get('content')) is not list:
            raise NativeProtocolError('native user-message content is malformed')
        if kind == 'commandExecution' and (
                type(item.get('command')) is not str or type(item.get('commandActions')) is not list
                or type(item.get('cwd')) is not str
                or (item.get('processId') is not None and type(item['processId']) is not str)
                or (item.get('exitCode') is not None and type(item['exitCode']) is not int)
                or (item.get('aggregatedOutput') is not None and type(item['aggregatedOutput']) is not str)):
            raise NativeProtocolError('native command item is malformed')
        if not complete:
            self.active_items.add(identity)
            return
        if identity in self.completed_items and self.completed_items[identity] != item:
            raise NativeProtocolError('native item completion conflicts')
        self.completed_items[identity] = item
        self.active_items.discard(identity)
        if kind == 'agentMessage' and item.get('phase') == 'final_answer':
            if type(item.get('text')) is not str or not item['text'].strip():
                raise NativeProtocolError('native final response is empty')
            if self.final_response is not None and self.final_response != item['text']:
                raise NativeProtocolError('native final response conflicts')
            self.final_response = item['text']
        elif kind == 'commandExecution':
            if item.get('status') not in ('completed', 'failed', 'declined') or item.get('cwd') != c['cwd']:
                raise NativeProtocolError('native command completion is malformed')
            # PTY processId is captured privately, never used for OS or standalone cancellation.
            try:
                words = shlex.split(item.get('command', ''))
            except ValueError:
                words = []
            read = words in (['cat', c['skill']['path']], ['cat', '--', c['skill']['path']],
                             ['/bin/cat', c['skill']['path']], ['/bin/cat', '--', c['skill']['path']])
            output = item.get('aggregatedOutput')
            if (read and item.get('status') == 'completed' and type(item.get('exitCode')) is int and item['exitCode'] == 0
                    and type(output) is str and hashlib.sha256(output.encode()).hexdigest() == c['skill']['sha256']):
                self.skill_load = {'status': 'observed-read', 'sha256': c['skill']['sha256'], 'item_id': identity}

    def _event(self, event):
        c = self.call.data
        method, params = event.get('method'), event.get('params')
        if method in ('skills/changed', 'mcpServerStatus/updated'):
            raise NativeProtocolError('native source/tool inventory changed')
        relevant = method in ('turn/started', 'turn/completed', 'item/started', 'item/completed',
                              'item/commandExecution/outputDelta', 'thread/settings/updated', 'model/rerouted')
        if not relevant:
            return
        if type(params) is not dict or params.get('threadId') != self.thread_id:
            raise NativeProtocolError('native event thread identity differs')
        if method.startswith('turn/'):
            self._bind_turn(params.get('turn'))
        elif method != 'thread/settings/updated':
            if params.get('turnId') != self.turn_id:
                raise NativeProtocolError('native event turn identity differs')
        if method == 'model/rerouted':
            raise NativeProtocolError('native model was rerouted; identity is not qualified')
        if method == 'thread/settings/updated':
            settings = params.get('threadSettings', {})
            if (settings.get('model') != c['model'] or settings.get('modelProvider') != c['provider']
                    or settings.get('effort') != c['effort'] or settings.get('approvalPolicy') != 'never'
                    or settings.get('approvalsReviewer') != 'user'):
                raise NativeProtocolError('native configured settings drifted')
        elif method in ('item/started', 'item/completed'):
            self._item(params.get('item'), method == 'item/completed')
        elif method == 'turn/completed':
            turn = params['turn']
            status = turn.get('status')
            if status not in ('completed', 'failed', 'interrupted') or type(turn.get('items')) is not list:
                raise NativeProtocolError('native terminal turn is malformed')
            if self.terminal is not None and self.terminal != status:
                raise NativeProtocolError('native terminal turn conflicts')
            for item in turn['items']:
                self._item(item, True)
            self.terminal = status

    def _drain(self, deadline=None):
        while self.rpc._event_cursor < len(self.rpc.events):
            _remaining(self.rpc.active_deadline)
            self._event(self.rpc.next_event())
        if deadline is not None and self.terminal is None:
            self._event(self.rpc.next_event(timeout=max(0.001, deadline - time.monotonic())))

    def _held_request(self):
        request = self.rpc.requests[-1]
        params = request.get('params')
        if type(params) is not dict or params.get('threadId') != self.thread_id:
            raise NativeProtocolError('native server request identity differs')
        turn = params.get('turnId')
        if type(turn) is not str or not turn:
            raise NativeProtocolError('native server request turn is malformed')
        self.turn_ids.add(turn)
        if self.turn_id is None:
            self.turn_id = turn
        elif self.turn_id != turn:
            raise NativeProtocolError('native server request turn differs')
        self.incomplete_reason = ('awaiting-input' if request.get('method') == 'item/tool/requestUserInput'
                                  else 'approval-held')

    def execute(self, effect_key, before_turn):
        require(getattr(self, 'prepared', False) and callable(before_turn), 'native turn is not externally prepared')
        self.trace.record({'kind': 'native-intent-binding', 'effect_key': effect_key, 'input_digest': self.call.payload_digest})
        c, primary = self.call.data, None
        try:
            _remaining(self.deadline)
            self._configuration()
            self._drain()
            before_turn()
            _remaining(self.deadline)
            self.turn_requested = True
            self.turn_request = self.rpc._next_id
            deadline = self.deadline
            self.rpc.timeout = max(0.001, deadline - time.monotonic())
            try:
                result = self.rpc.call('turn/start', {'threadId': self.thread_id, 'model': c['model'], 'effort': c['effort'],
                    'permissions': c['profile_id'], 'approvalPolicy': 'never', 'approvalsReviewer': 'user',
                    'input': [{'type': 'skill', 'name': c['skill']['name'], 'path': c['skill']['path']},
                              {'type': 'text', 'text': c['prompt'], 'text_elements': []}]}, timeout=max(0.001, deadline - time.monotonic()))
                self._bind_turn(result.get('turn') if type(result) is dict else None)
                while self.terminal is None:
                    self._drain(deadline)
                    if time.monotonic() >= deadline and self.terminal is None:
                        raise NativeProtocolError('native turn deadline expired')
            except native_worker.RequiredApproval:
                self._held_request()
            self._drain()
            if self.terminal == 'completed' and self.final_response is None:
                raise NativeProtocolError('normal native completion lacks a final response')
            _remaining(self.deadline)
        except BaseException as error:
            primary = error
            raise
        finally:
            try:
                self.close()
            except BaseException as cleanup:
                if primary is None:
                    raise
                primary.add_note('native turn cleanup remains unconfirmed (' + type(cleanup).__name__ + ')')
        self.call.verify_sources()
        _remaining(self.cleanup_deadline)
        return {'format_version': 1, 'effect_key': effect_key, 'input_digest': self.call.payload_digest,
                'turn_status': self.terminal, 'capture_status': 'complete' if self.terminal == 'completed' and not self.incomplete_reason else 'incomplete',
                'incomplete_reason': self.incomplete_reason, 'final_response': self.final_response,
                'requested_model': c['model'], 'configured_model': self.configured_model, 'observed_model': None,
                'skill_load': self.skill_load, 'cleanup': self.cleanup, 'assessment_result': 'unknown',
                'synthetic_inert': self.transport_kind == 'inert', 'model_calls': 0 if self.transport_kind == 'inert' else None,
                'events': self.rpc.events, 'server_requests': self.rpc.requests}

    def close(self):
        if self.cleanup_unconfirmed:
            raise CleanupIncomplete('native turn cleanup remains unconfirmed')
        if self.closed_success:
            return
        errors = []
        if self.cleanup_deadline is None:
            self.cleanup_deadline = time.monotonic() + self.call.data['limits']['cancel_seconds']
        # Keep part of the SAME budget for killing/reaping the host even when
        # a cancellation/unsubscribe peer consumes all protocol time.
        reserve = min(0.05, self.call.data['limits']['cancel_seconds'] / 3)
        protocol_deadline = self.cleanup_deadline - reserve
        self.rpc.active_deadline = protocol_deadline
        try:
            with native_worker._defer_interrupts():
                try:
                    self._drain()
                except BaseException as error:
                    errors.append(error)
                if self.turn_requested and (self.terminal is None or self.active_items):
                    # A turn-start reply may be lost while its correlated event was buffered.
                    try:
                        self._drain()
                    except BaseException as error:
                        errors.append(error)
                    cancel_deadline = protocol_deadline
                    for identity in list(self.turn_ids):
                        try:
                            remaining = cancel_deadline - time.monotonic()
                            if remaining <= 0:
                                raise CleanupIncomplete('native cancellation budget expired; owned identities retained')
                            self.rpc.timeout = remaining
                            reply = self.rpc.call('turn/interrupt', {'threadId': self.thread_id, 'turnId': identity},
                                                  timeout=remaining)
                            if type(reply) is not dict or reply:
                                raise NativeProtocolError('native interrupt acknowledgment is malformed')
                            while self.terminal is None:
                                if time.monotonic() >= cancel_deadline:
                                    raise CleanupIncomplete('native terminal cancellation outcome is unknown')
                                self._drain(cancel_deadline)
                        except BaseException as error:
                            errors.append(error)
                    if not self.turn_ids or self.terminal is None or self.active_items:
                        errors.append(CleanupIncomplete('native turn/items lack terminal ownership evidence'))
                if self.thread_id is not None:
                    try:
                        self.rpc.timeout = _remaining(protocol_deadline)
                        value = self.rpc.call('thread/unsubscribe', {'threadId': self.thread_id})
                        if type(value) is not dict or value.get('status') not in ('unsubscribed', 'notSubscribed', 'notLoaded'):
                            raise NativeProtocolError('native unsubscribe response is malformed')
                    except BaseException as error:
                        errors.append(error)
                try:
                    self.rpc.close(self.cleanup_deadline)
                except BaseException as error:
                    errors.append(error)
        except BaseException as error:
            errors.append(error)
        if self.thread_requested:
            try:
                _remaining(self.cleanup_deadline)
                proof = self.cleanup_reader({'server_pid': self.server_pid, 'thread_id': self.thread_id,
                                              'turn_id': self.turn_id, 'events': self.rpc.events,
                                              'deadline': self.cleanup_deadline}) if self.cleanup_reader else None
                _remaining(self.cleanup_deadline)
                require(type(proof) is dict and proof.keys() == {'status', 'mode', 'input_digest', 'proof_digest'}
                        and proof['status'] == 'confirmed' and proof['mode'] == self.transport_kind
                        and proof['input_digest'] == self.call.payload_digest and hex_digest(proof['proof_digest']),
                        'independent native tool-tree cleanup proof is unavailable')
                self.cleanup = proof
            except BaseException as error:
                errors.append(CleanupIncomplete('native tool-tree cleanup is unknown'))
        if errors:
            self.cleanup_errors, self.cleanup_unconfirmed = tuple(errors), True
        try:
            if self.trace is not None:
                self.trace.record({'kind': 'native-cleanup', 'tool_tree': self.cleanup,
                                   'uncertain': bool(errors), 'terminal': self.terminal,
                                   'incomplete_reason': self.incomplete_reason})
        except BaseException as error:
            errors.append(error)
            self.cleanup_errors, self.cleanup_unconfirmed = tuple(errors), True
        finally:
            self.rpc.sink = None
            if self.trace is not None:
                self.trace.close()
        if errors:
            if len(errors) > 1:
                errors[0].add_note(str(len(errors) - 1) + ' additional native cleanup facts retained')
            raise errors[0]
        if time.monotonic() >= self.cleanup_deadline:
            self.cleanup_unconfirmed = True
            raise CleanupIncomplete('native aggregate cleanup deadline expired')
        self.closed_success = True


class _FencedStore:
    """Retain this invocation's returned fencing facts, never another ledger."""
    def __init__(self, store, executor):
        self.store, self.executor = store, executor

    def __getattr__(self, name):
        return getattr(self.store, name)

    def begin_effect(self, job, slot_index):
        result = self.store.begin_effect(job, slot_index)
        self.executor.fence = result['effect']['intent_fence']
        return result


class _Executor:
    def __init__(self, store, job, claimant, call, reader, session):
        self.store, self.job, self.claimant = store, job, claimant
        self.call, self.reader, self.session = call, reader, session
        self.payload_digest, self.fence = call.payload_digest, None

    def execute(self, effect_key):
        def before_turn():
            live = self.store.get_job(recovery._job(self.job)['namespace'], recovery._job(self.job)['job_id'])
            require(live['job_digest'] == self.job['job_digest'], 'native job identity changed')
            proof = _readiness(self.reader, self.call, live)
            require(proof['mode'] == self.session.transport_kind, 'inert proof cannot authorize a native transport')
            _gates(live, self.call, proof, claimant=self.claimant, fence=self.fence)
            self.call.verify_sources()
        return self.session.execute(effect_key, before_turn)


def run_native_slot(store, job, claimant, slot_index, evidence, call, *, expected_job_digest,
                    readiness_reader=None, session_factory=None, cleanup_reader=None, lease_seconds=300):
    started = time.monotonic()
    if readiness_reader is None:
        raise recovery.Refused('accepted external readiness is required before a native intent')
    require(isinstance(call, NativeCall) and callable(readiness_reader), 'native input/readiness reader differs')
    definition, c = recovery._job(job), call.data
    deadline = started + c['limits']['timeout_seconds']
    require(job['job_digest'] == expected_job_digest and type(slot_index) is int and 0 <= slot_index < len(definition['slots']),
            'native job differs from its independent pin')
    require(all(definition[key] == c[key] for key in ('case_digest', 'skills_commit', 'source_commit', 'release_digest'))
            and definition['slots'][slot_index]['payload_digest'] == call.payload_digest, 'native call differs from its frozen job')
    require(type(lease_seconds) is int and math.ceil(c['limits']['timeout_seconds'] + c['limits']['cancel_seconds'] + 5) <= lease_seconds <= 300,
            'native lease does not cover the bounded call and cancellation')
    live = store.get_job(definition['namespace'], definition['job_id'])
    require(live['job_digest'] == expected_job_digest, 'current native job differs from its independent pin')
    proof = _readiness(readiness_reader, call, live)
    _remaining(deadline)
    _gates(live, call, proof)
    call.verify_sources()
    _remaining(deadline)
    if session_factory is None:
        require(proof['mode'] == 'native', 'inert release cannot start a native host')
        require(c['command'][-1] == 'app-server' and '--no-daemon' in c['command']
                and not any('bypass' in arg or arg == '--yolo' for arg in c['command']), 'native launch is not the supported owned server')
        session = NativeTurnSession(call, trace_root=evidence.root.parent / 'native-turn-traces', cleanup_reader=cleanup_reader)
    else:
        session = session_factory(call)
    require(session.transport_kind == proof['mode'], 'inert release cannot authorize a native transport')
    require(callable(session.cleanup_reader), 'independent cleanup observer is required before native intent')
    session.deadline = deadline
    with session:
        session.prepare()
        live = store.get_job(definition['namespace'], definition['job_id'])
        require(live['job_digest'] == expected_job_digest, 'prepared native job identity changed')
        proof = _readiness(readiness_reader, call, live)
        _gates(live, call, proof)
        call.verify_sources()
        _remaining(deadline)
        executor = _Executor(store, live, claimant, call, readiness_reader, session)
        return native_worker.run_slot(_FencedStore(store, executor), live, claimant, slot_index, evidence, executor,
                                      expected_job_digest=expected_job_digest, lease_seconds=lease_seconds)


def reconcile_native_history(rpc, store, job, call, pin, *, expected_pin_digest, expected_job_digest,
                             slot_index=0, max_pages=8, max_items=512, max_bytes=4 * 1024 * 1024,
                             timeout_seconds=5):
    """Missing-packet recovery: bounded private reads, never another invocation.

    The expected pin digest must come from independently retained original
    request/trace evidence, not from the history being inspected. The caller
    owns the initialized read-only RPC transport. This function performs no
    claim, intent, observation, resume or turn mutation. Even matching terminal
    history supplies no cleanup/runtime-model/skill/semantic qualification and
    therefore yields only an unavailable safe observation, never retry rights.
    """
    fields = {'format_version', 'effect_key', 'input_digest', 'job_digest', 'release_digest',
              'source_commit', 'thread_id', 'turn_id', 'cli_version', 'native_binding_digest'}
    require(type(pin) is dict and pin.keys() == fields and pin['format_version'] == 1
            and type(pin['format_version']) is int and hex_digest(expected_pin_digest)
            and recovery.digest(pin) == expected_pin_digest, 'native history differs from its independent pin')
    require(all(hex_digest(pin[key]) for key in ('effect_key', 'input_digest', 'job_digest', 'release_digest', 'native_binding_digest')),
            'native history pin has incomplete artifact identities')
    require(all(type(pin[key]) is str and 0 < len(pin[key]) <= 256 for key in ('thread_id', 'turn_id', 'cli_version')),
            'native history pin has malformed native identities')
    definition, c = recovery._job(job), call.data
    require(job['job_digest'] == expected_job_digest == pin['job_digest']
            and pin['input_digest'] == call.payload_digest and pin['release_digest'] == c['release_digest']
            and pin['source_commit'] == c['source_commit'], 'native history independent source binding differs')
    require(type(slot_index) is int and 0 <= slot_index < len(definition['slots']), 'native history slot is not frozen')
    slot = definition['slots'][slot_index]
    require(slot['effect_type'] == 'native-call' and slot['payload_digest'] == call.payload_digest
            and recovery.effect_key(definition, slot) == pin['effect_key'], 'native history effect/input join differs')
    require(type(max_pages) is int and 1 <= max_pages <= 32 and type(max_items) is int and 1 <= max_items <= 4096
            and type(max_bytes) is int and 1 <= max_bytes <= 64 * 1024 * 1024
            and type(timeout_seconds) in (int, float) and math.isfinite(timeout_seconds) and 0 < timeout_seconds <= 30,
            'native history reads need finite aggregate bounds')
    deadline = time.monotonic() + timeout_seconds
    capture, bytes_read, pages, entries = [], 0, 0, 0
    result = {'status': 'unavailable', 'effect_key': pin['effect_key'], 'execution_allowed': False,
              'assessment_result': 'unknown', 'observed_model': None, 'skill_load': {'status': 'unknown'},
              'cleanup': {'status': 'unknown'}, 'private_history': None, 'history_digest': None,
              'observation': native_worker.PrivateEvidence._observation(pin['effect_key'], call.payload_digest, 'unavailable')}

    def retain(value):
        nonlocal bytes_read
        bytes_read += len(recovery.canonical(value).encode())
        require(bytes_read <= max_bytes, 'native history aggregate byte limit exceeded')
        _remaining(deadline)

    def read(method, params):
        # Only these literal read methods are reachable; opaque cursors are data.
        remaining = _remaining(deadline)
        previous = getattr(rpc, 'timeout', None)
        if previous is not None:
            rpc.timeout = min(previous, remaining)
        try:
            value = rpc.call(method, params, timeout=remaining)
        finally:
            if previous is not None:
                rpc.timeout = previous
        retain(value)
        capture.append({'method': method, 'response': value})
        return value

    def paged(method, params):
        nonlocal pages, entries
        cursor, seen, values = None, set(), []
        while True:
            require(pages < max_pages and entries < max_items, 'native history aggregate page/item limit exceeded')
            page = read(method, {**params, 'cursor': cursor, 'limit': min(100, max_items - entries), 'sortDirection': 'asc'})
            pages += 1
            require(type(page) is dict and type(page.get('data')) is list, 'native history page is malformed')
            entries += len(page['data'])
            require(entries <= max_items, 'native history aggregate item limit exceeded')
            values.extend(page['data'])
            cursor = page.get('nextCursor')
            if cursor is None:
                return values
            require(type(cursor) is str and cursor and cursor not in seen, 'native history cursor repeats or differs')
            seen.add(cursor)

    try:
        snapshot = store.snapshot(definition['namespace'])
        text = snapshot.get('snapshot_text')
        require(type(text) is str and snapshot.get('head') == hashlib.sha256(text.encode()).hexdigest(),
                'authoritative history snapshot identity differs')
        retain(text)
        state = native_worker._json_message(text)
        require(state.get('namespace') == definition['namespace'], 'authoritative history namespace differs')
        jobs = [row for row in state.get('jobs', []) if row.get('job_digest') == expected_job_digest]
        effects = [row for row in state.get('effects', []) if row.get('effect_key') == pin['effect_key']]
        require(len(jobs) == 1 and len(effects) == 1 and effects[0].get('job_id') == definition['job_id']
                and effects[0].get('payload_digest') == call.payload_digest
                and type(effects[0].get('intent_fence')) is int and effects[0]['intent_fence'] >= 1
                and effects[0].get('state') in ('pending', 'uncertain', 'completed'),
                'authoritative consumed intent is missing or conflicting')
        meta = read('thread/read', {'threadId': pin['thread_id'], 'includeTurns': False})
        thread = meta.get('thread') if type(meta) is dict else None
        require(type(thread) is dict and thread.get('id') == pin['thread_id']
                and thread.get('cliVersion') == pin['cli_version'] and thread.get('modelProvider') == c['provider']
                and thread.get('model') in (None, c['model']), 'persisted native thread identity differs')
        turns = paged('thread/turns/list', {'threadId': pin['thread_id'], 'itemsView': 'full'})
        seen, target = set(), None
        for turn in turns:
            require(type(turn) is dict and type(turn.get('id')) is str and turn['id'] and turn['id'] not in seen
                    and turn.get('status') in ('inProgress', 'completed', 'failed', 'interrupted')
                    and type(turn.get('items')) is list, 'persisted native turn identity/shape differs')
            seen.add(turn['id'])
            if turn['id'] == pin['turn_id']:
                target = turn
        require(target is not None, 'pinned native turn is not present; absence is not established')
        rows = paged('thread/items/list', {'threadId': pin['thread_id'], 'turnId': pin['turn_id']})
        items, final, source_inputs = {}, None, []
        expected_input = [{'type': 'skill', 'name': c['skill']['name'], 'path': c['skill']['path']},
                          {'type': 'text', 'text': c['prompt']}]
        for row in rows:
            item = row.get('item') if type(row) is dict else None
            require(type(row) is dict and row.get('turnId') == pin['turn_id'] and type(item) is dict
                    and type(item.get('id')) is str and item['id'] and item['id'] not in items,
                    'persisted native item identity differs')
            kind = item.get('type')
            require(kind in ('userMessage', 'agentMessage', 'commandExecution', 'reasoning', 'plan'),
                    'persisted native item exceeds the frozen local grant')
            items[item['id']] = item
            if kind == 'userMessage':
                require(type(item.get('content')) is list, 'persisted input is malformed')
                # UserInput.text_elements has a documented [] default. Preserve
                # exact prompt/skill bytes while accepting that native default.
                content = []
                for value in item['content']:
                    require(type(value) is dict, 'persisted input element is malformed')
                    if value.get('type') == 'text':
                        require(value.keys() <= {'type', 'text', 'text_elements'} and value.get('text_elements', []) == [],
                                'persisted input formatting differs from the frozen call')
                        value = {key: data for key, data in value.items() if key != 'text_elements'}
                    content.append(value)
                source_inputs.append(content)
            elif kind == 'agentMessage':
                require(type(item.get('text')) is str and item.get('phase') in (None, 'commentary', 'final_answer'),
                        'persisted message phase/text differs from pinned schema')
                if item.get('phase') == 'final_answer':
                    require(item['text'].strip() and (final is None or final == item['text']), 'persisted final response conflicts')
                    final = item['text']
            elif kind == 'commandExecution':
                require(type(item.get('command')) is str and type(item.get('commandActions')) is list
                        and item.get('cwd') == c['cwd'] and item.get('status') in ('inProgress', 'completed', 'failed', 'declined')
                        and (item.get('exitCode') is None or type(item['exitCode']) is int)
                        and (item.get('processId') is None or type(item['processId']) is str), 'persisted command item is malformed')
        require(source_inputs == [expected_input], 'persisted complete input sequence differs from the independently pinned call')
        require(target['status'] != 'completed' or final is not None, 'normal persisted completion lacks a final response')
        if target.get('itemsView', 'full') == 'full':
            declared = {item.get('id'): item for item in target['items'] if type(item) is dict}
            require(len(declared) == len(target['items']) and declared == items, 'persisted turn/items pages conflict')
        result.update(status='observed' if target['status'] in ('completed', 'failed', 'interrupted') else 'incomplete',
                      private_history={'thread_id': pin['thread_id'], 'turn_id': pin['turn_id'],
                                       'turn_status': target['status'], 'items': list(items.values()), 'final_response': final},
                      history_digest=recovery.digest(capture))
    except (NativeProtocolError, recovery.Unavailable, OSError):
        result['status'] = 'unavailable'
    except (recovery.Refused, ValueError, TypeError, KeyError):
        result['status'] = 'untrusted'
    finally:
        result['private_read_capture'] = capture
    return result
