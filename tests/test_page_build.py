"""One pinned current Git tree, complete routes and owned runtime lifetime."""
from contextlib import contextmanager
import json
import subprocess
from pathlib import Path

import pytest

from ams.page_build import collect_current
from ams.pages import PageRefused

ORIGIN = "https://github.com/KaydenClark/Agentic-Management-System.git"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "source"
    (root / "site").mkdir(parents=True)
    git(root, "init", "-q", "-b", "dev")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "remote", "add", "origin", ORIGIN)
    (root / "README.md").write_text("Synthetic collector fixture.\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture provenance")
    provenance = git(root, "rev-parse", "HEAD")
    rows = [{"path": p, "title": "Synthetic " + p, "spec": "S-003", "task": "TK-001", "landed": {"branch": "dev", "commit": provenance, "pr": 1}} for p in ["/", "/skills/new", "/_not-found"]]
    (root / "site/page-list.json").write_text(json.dumps({"pages": rows}))
    (root / "site/content.txt").write_text("Pinned current content")
    git(root, "add", ".")
    git(root, "commit", "-qm", "synthetic current website")
    return root


@contextmanager
def fixture_build(export, candidate, public_config):
    assert not (export / ".git").exists()
    assert not (export / "site/.env.local").exists()
    out = export / "site/.next/server/app"
    out.mkdir(parents=True)
    content = (export / "site/content.txt").read_text()
    built = {"/": f'<main id="main">{content}</main>', "/skills/new": '<main id="main">Synthetic skill</main>', "/_not-found": '<main id="main">Synthetic visitor404</main>'}
    for path, html in built.items():
        target = out / ("index.html" if path == "/" else path.strip("/") + ".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)
    (out / "_global-error.html").write_text("Internal framework fallback")
    def read(path, expected_status):
        assert expected_status == (404 if path == "/_not-found" else 200)
        return built[path]
    yield read


def test_collection_freezes_one_tree_and_classifies_every_built_surface(source):
    candidate = git(source, "rev-parse", "HEAD")
    (source / "site/content.txt").write_text("Unrelated newer dirty work")
    (source / "site/.env.local").write_text("PRIVATE_SYNTHETIC_CANARY=never-export\n")
    original_status = git(source, "status", "--porcelain")
    exported = []
    @contextmanager
    def build(export, frozen, config):
        exported.append(export)
        assert frozen == candidate and config == {}
        with fixture_build(export, frozen, config) as read:
            yield read
    result = collect_current(source, "dev", candidate, build_start=build)
    assert result["candidate"] == candidate
    assert set(result["html"]) == {"/", "/skills/new", "/_not-found"}
    assert result["html"]["/"] == '<main id="main">Pinned current content</main>'
    assert result["kinds"]["/_not-found"] == "visitor-404"
    assert result["excluded"] == {"_global-error.html": "internal framework fallback"}
    assert all(not path.exists() for path in exported)
    assert git(source, "status", "--porcelain") == original_status


def test_missing_page_owner_and_moving_pin_refuse_without_source_changes(source):
    candidate = git(source, "rev-parse", "HEAD")
    page_list = source / "site/page-list.json"
    rows = json.loads(page_list.read_text())
    rows["pages"] = [row for row in rows["pages"] if row["path"] != "/skills/new"]
    page_list.write_text(json.dumps(rows))
    git(source, "add", ".")
    git(source, "commit", "-qm", "synthetic missing owner")
    before = git(source, "rev-parse", "HEAD")
    called = []
    @contextmanager
    def build(export, frozen, config):
        called.append(frozen)
        with fixture_build(export, frozen, config) as read:
            yield read
    with pytest.raises(PageRefused, match="candidate.*changed"):
        collect_current(source, "dev", candidate, build_start=build)
    assert called == []
    with pytest.raises(PageRefused, match="/skills/new.*page-list owner"):
        collect_current(source, "dev", before, build_start=build)
    assert called == [before]
    assert git(source, "rev-parse", "HEAD") == before


def test_owned_process_cleanup_on_actual_interrupt_preserves_unrelated_process(tmp_path):
    import os
    import signal
    import sys
    import time
    from ams.page_build import owned_process
    marker = tmp_path / "owned-pids.json"
    program = "import json,os,subprocess,sys,time; child=subprocess.Popen([sys.executable, '-c', 'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)']); open(sys.argv[1], 'w').write(json.dumps([os.getpid(),child.pid])); time.sleep(60)"
    wrapper = "from ams.page_build import owned_process; import sys; from pathlib import Path; "+"\nwith owned_process([sys.executable,'-c',sys.argv[1],sys.argv[2]], cwd=Path.cwd(), environment={}, grace=0.5) as child:\n child.wait()\n"
    env = {"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), "PATH": os.environ["PATH"]}
    unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True)
    observed = subprocess.Popen([sys.executable, "-c", wrapper, program, str(marker)], cwd=tmp_path, env=env, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    owned = []
    try:
        deadline = time.monotonic() + 10
        while not marker.exists() and observed.poll() is None and time.monotonic() < deadline:
            time.sleep(0.02)
        assert marker.exists(), "fixture runtime did not start"
        owned = json.loads(marker.read_text())
        os.kill(observed.pid, signal.SIGINT)
        assert observed.wait(timeout=10) != 0
        for pid in owned:
            status = subprocess.run(["ps", "-p", str(pid), "-o", "stat="], capture_output=True, text=True).stdout.strip()
            assert not status or status.startswith("Z"), f"owned process {pid} still executes: {status}"
        assert unrelated.poll() is None, "unrelated process was stopped"
    finally:
        if observed.poll() is None:
            os.killpg(observed.pid, signal.SIGKILL)
        observed.wait()
        if owned:
            try: os.killpg(owned[0], signal.SIGKILL)
            except ProcessLookupError: pass
        unrelated.terminate(); unrelated.wait()


def test_container_runner_requires_an_immutable_image_before_execution():
    from ams.page_build import DockerBuild
    with pytest.raises(PageRefused, match="immutable"):
        DockerBuild("node:latest")


def test_public_configuration_rejects_privileged_or_unexpected_values():
    import base64
    from ams.page_build import public_configuration
    def token(role):
        encoded = base64.urlsafe_b64encode(json.dumps({"role": role}).encode()).decode().rstrip("=")
        return "synthetic." + encoded + ".signature"
    public = {"NEXT_PUBLIC_SUPABASE_URL": "https://fixture.supabase.co", "NEXT_PUBLIC_SUPABASE_ANON_KEY": token("anon")}
    assert public_configuration(public) == public
    with pytest.raises(PageRefused, match="anonymous"):
        public_configuration({**public, "NEXT_PUBLIC_SUPABASE_ANON_KEY": token("service_role")})
    with pytest.raises(PageRefused, match="only explicit public"):
        public_configuration({"GITHUB_TOKEN": "synthetic-private-canary"})


def test_build_artifact_directory_link_refuses_before_reading_outside(source, tmp_path):
    candidate = git(source, "rev-parse", "HEAD")
    outside = tmp_path / "unrelated-artifacts"
    outside.mkdir()
    (outside / "index.html").write_text("Synthetic private canary")
    @contextmanager
    def linked(export, frozen, config):
        app = export / "site/.next/server"
        app.mkdir(parents=True)
        (app / "app").symlink_to(outside, target_is_directory=True)
        yield lambda *_: pytest.fail("unsafe artifacts reached served collection")
    with pytest.raises(PageRefused, match="symlink"):
        collect_current(source, "dev", candidate, build_start=linked)
    assert (outside / "index.html").read_text() == "Synthetic private canary"


def prepare_container_fixture(source, canary):
    package = {"name": "synthetic-page-build", "version": "1.0.0", "scripts": {"build": "node fixture-build.mjs"}}
    (source / "site/package.json").write_text(json.dumps(package))
    (source / "site/package-lock.json").write_text(json.dumps({"name": package["name"], "version": "1.0.0", "lockfileVersion": 3, "requires": True, "packages": {"": package}}))
    script = r'''import fs from 'node:fs';
const forbidden = ['OPENAI_API_KEY','SUPABASE_SERVICE_ROLE_KEY','GITHUB_TOKEN','NODE_OPTIONS'];
if (forbidden.some(k => process.env[k]) || process.env.HOME !== '/tmp/ams-pages-home') throw Error('private context reached candidate');
if (fs.existsSync('/workspace/.git') || fs.existsSync(CANARY)) throw Error('host context was mounted');
let denied = false;
try { fs.writeFileSync('/etc/ams-page-test','forbidden'); } catch { denied = true; }
if (!denied) throw Error('container root is writable');
const pages = {'/':'<main id="main">Synthetic current home</main>', '/skills/new':'<main id="main">Synthetic skill</main>', '/_not-found':'<main id="main">Synthetic visitor404</main>'};
for (const [route,html] of Object.entries(pages)) {
 const file = '.next/server/app/' + (route === '/' ? 'index' : route.slice(1)) + '.html';
 fs.mkdirSync(file.slice(0,file.lastIndexOf('/')), {recursive:true}); fs.writeFileSync(file,html);
}
fs.writeFileSync('.next/server/app/_global-error.html','Internal framework fallback');
const server = `const http=require('node:http'), cp=require('node:child_process');
const pages=${JSON.stringify(pages)};
const child=cp.spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{detached:true,stdio:'ignore'}); child.unref();
http.createServer((req,res)=>{const known=Object.hasOwn(pages,req.url)&&req.url!=='/_not-found';res.writeHead(known?200:404,{'content-type':'text/html'});res.end(known?pages[req.url]:pages['/_not-found']);}).listen(3000,'127.0.0.1');`;
fs.mkdirSync('node_modules/next/dist/bin',{recursive:true}); fs.writeFileSync('node_modules/next/dist/bin/next',server);
'''
    (source / "site/fixture-build.mjs").write_text(script.replace("CANARY", json.dumps(str(canary))))
    git(source, "add", "."); git(source, "commit", "-qm", "synthetic container execution fixture")
    return git(source, "rev-parse", "HEAD")


def docker_image():
    import os
    image = os.environ.get("AMS_PAGES_DOCKER_IMAGE")
    if not image:
        pytest.skip("explicit approved immutable Node image required for local container proof")
    return image


def test_real_container_build_served_collection_and_cleanup(source, tmp_path, monkeypatch):
    from ams.page_build import DockerBuild
    image = docker_image()
    canary = tmp_path / "unrelated-private-canary"
    canary.write_text("must stay private and unchanged")
    candidate = prepare_container_fixture(source, canary)
    for key in ["OPENAI_API_KEY", "SUPABASE_SERVICE_ROLE_KEY", "GITHUB_TOKEN", "NODE_OPTIONS"]:
        monkeypatch.setenv(key, "synthetic-private-canary")
    runtime = DockerBuild(image, timeout=60)
    result = collect_current(source, "dev", candidate, build_start=runtime)
    assert len(result["html"]) == 3 and result["kinds"]["/_not-found"] == "visitor-404"
    assert runtime.cleanup_verified and runtime.container_id
    absent = subprocess.run(["docker", "inspect", "--format", "{{.Id}}", runtime.container_id], capture_output=True, text=True)
    assert absent.returncode != 0 and "no such" in absent.stderr.lower()
    assert canary.read_text() == "must stay private and unchanged"
    assert not git(source, "status", "--porcelain")


def test_actual_sigint_removes_owned_container_including_detached_child(source, tmp_path):
    import os, signal, sys, time
    image = docker_image()
    canary = tmp_path / "unrelated-private-canary"
    canary.write_text("unchanged")
    candidate = prepare_container_fixture(source, canary)
    marker = tmp_path / "container-ready.json"
    wrapper = '''import json,sys,time
from contextlib import contextmanager
from pathlib import Path
from ams.page_build import DockerBuild,collect_current
runtime=DockerBuild(sys.argv[3],timeout=60)
@contextmanager
def build(export,candidate,config):
 with runtime(export,candidate,config) as read:
  Path(sys.argv[4]).write_text(json.dumps({'id':runtime.container_id}))
  time.sleep(60)
  yield read
collect_current(Path(sys.argv[1]),'dev',sys.argv[2],build_start=build)
'''
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")}
    log = (tmp_path / "interrupted-container.log").open("wb")
    process = subprocess.Popen([sys.executable,"-c",wrapper,str(source),candidate,image,str(marker)], env=env, stdout=log, stderr=log, start_new_session=True)
    identity = None
    try:
        until=time.monotonic()+60
        while not marker.exists() and process.poll() is None and time.monotonic()<until:
            time.sleep(0.05)
        assert marker.exists(), "container did not reach ready fixture; inspect retained private log"
        identity=json.loads(marker.read_text())["id"]
        os.kill(process.pid,signal.SIGINT)
        assert process.wait(timeout=20)!=0
        absent=subprocess.run(["docker","inspect","--format","{{.Id}}",identity],capture_output=True,text=True)
        assert absent.returncode!=0 and "no such" in absent.stderr.lower(), "owned container survived interruption"
        assert canary.read_text()=="unchanged"
    finally:
        if process.poll() is None:
            os.kill(process.pid,signal.SIGINT); process.wait(timeout=20)
        log.close()
        if identity:
            subprocess.run(["docker","rm","--force",identity],capture_output=True)


def test_cleanup_reaps_an_exited_leader_before_group_observation(tmp_path):
    import os, sys, time
    from ams.page_build import owned_process
    process = None
    try:
        with owned_process([sys.executable, '-c', 'pass'], cwd=tmp_path, environment={}) as process:
            until = time.monotonic() + 3
            while time.monotonic() < until:
                status = subprocess.run(['/bin/ps', '-p', str(process.pid), '-o', 'stat='], capture_output=True, text=True).stdout.strip()
                if status.startswith('Z'):
                    break
                time.sleep(0.01)
            assert status.startswith('Z'), 'fixture leader did not reach the unreaped state'
        assert process.returncode == 0
        with pytest.raises(ProcessLookupError):
            os.killpg(process.pid, 0)
    finally:
        if process is not None:
            process.wait(timeout=3)


def test_exit_between_poll_and_group_signal_retries_only_after_reap(tmp_path, monkeypatch):
    import errno, signal
    import ams.page_build as module
    class Process:
        pid = 123456789  # synthetic; every signal is intercepted below
        returncode = None
        polls = 0
        def poll(self):
            self.polls += 1
            if self.polls >= 2:
                self.returncode = 0
            return self.returncode
        def wait(self, timeout=None):
            self.returncode = 0
            return 0
        def kill(self):
            self.returncode = -9
    process = Process()
    calls = []
    def signal_group(pid, which):
        assert pid == process.pid
        calls.append((which, process.returncode))
        if len(calls) == 1:
            raise PermissionError(errno.EPERM, 'synthetic exit-before-probe race')
        raise ProcessLookupError(errno.ESRCH, 'synthetic reaped group')
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *args, **kwargs: process)
    monkeypatch.setattr(module.os, 'killpg', signal_group)
    with module.owned_process(['synthetic'], cwd=tmp_path, environment={}):
        pass
    assert calls[:2] == [(signal.SIGTERM, None), (signal.SIGTERM, 0)]


def test_genuine_group_permission_error_is_not_hidden(tmp_path, monkeypatch):
    import errno
    import ams.page_build as module
    class Process:
        pid = 123456789
        returncode = None
        def poll(self): return self.returncode
        def wait(self, timeout=None): return self.returncode
        def kill(self): self.returncode = -9
    process = Process()
    calls = []
    def denied(pid, which):
        calls.append((pid, which))
        raise PermissionError(errno.EPERM, 'synthetic genuine permission denial')
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *args, **kwargs: process)
    monkeypatch.setattr(module.os, 'killpg', denied)
    with pytest.raises(PermissionError, match='genuine permission'):
        with module.owned_process(['synthetic'], cwd=tmp_path, environment={}):
            pass
    assert len(calls) == 1, 'live-leader permission denial was retried or swallowed'


def test_poll_interruption_is_reraised_after_owned_cleanup(tmp_path, monkeypatch):
    import os, signal, sys, time
    import ams.page_build as module
    actual_popen = subprocess.Popen
    marker = tmp_path / 'poll-interrupt-ready.json'
    program = "import json,os,subprocess,sys,time; p=subprocess.Popen([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)']);open(sys.argv[1],'w').write(json.dumps([os.getpid(),p.pid]));time.sleep(60)"
    owned = []
    real = None
    class InterruptedPoll:
        interrupted = False
        def __init__(self, process): self.process = process
        def __getattr__(self, key): return getattr(self.process, key)
        def poll(self):
            if not self.interrupted:
                self.interrupted = True
                raise KeyboardInterrupt('synthetic cleanup poll interruption')
            return self.process.poll()
    def start(*args, **kwargs):
        nonlocal real
        real = actual_popen(*args, **kwargs)
        return InterruptedPoll(real)
    try:
        with monkeypatch.context() as patch:
            patch.setattr(module.subprocess, 'Popen', start)
            with pytest.raises(KeyboardInterrupt, match='cleanup poll interruption'):
                with module.owned_process([sys.executable,'-c',program,str(marker)], cwd=tmp_path, environment={}, grace=0.3):
                    until = time.monotonic() + 3
                    while not marker.exists() and time.monotonic() < until:
                        time.sleep(0.01)
                    owned = json.loads(marker.read_text())
        assert real.returncode is not None
        for pid in owned:
            status = subprocess.run(['/bin/ps','-p',str(pid),'-o','stat='],capture_output=True,text=True).stdout.strip()
            assert not status or status.startswith('Z'), 'poll interruption skipped descendant cleanup'
    finally:
        if real is not None and real.poll() is None:
            os.killpg(real.pid, signal.SIGKILL);real.wait()
        if owned:
            try: os.killpg(owned[0], signal.SIGKILL)
            except ProcessLookupError: pass
