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
