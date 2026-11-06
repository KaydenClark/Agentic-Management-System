"""Collect review content from one trusted, immutable website tree.

The runner owns execution and cleanup. The collector never checks out a ref,
copies host configuration, or chooses page ownership from a historical commit.
"""

import base64
from contextlib import contextmanager
import io
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tarfile
import tempfile
import threading
import time
import uuid
from urllib.parse import urlsplit

from .grill_board.answers import AnswerRefused, _git
from .pages import PageRefused, _metadata, _safe_file, content_hash

AMS_ORIGIN = "https://github.com/KaydenClark/Agentic-Management-System.git"
PUBLIC_CONFIG = {"NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY"}
SHA = re.compile(r"[0-9a-f]{40,64}")


@contextmanager
def owned_process(arguments, *, cwd, environment, output=None, grace=2.0):
    """Own a new POSIX process group through normal exit and interruption.

    Only trusted host runtime clients and inert test fixtures use this seam.
    Candidate programs execute inside the container, which has separate cleanup.
    """
    if os.name != "posix":
        raise PageRefused("owned process groups require a supported POSIX host")
    process = subprocess.Popen(arguments, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                               stdout=output if output is not None else subprocess.DEVNULL,
                               stderr=subprocess.STDOUT, start_new_session=True)
    try:
        yield process
    finally:
        def send(which):
            try:
                os.killpg(process.pid, which)
                return True
            except ProcessLookupError:
                return False
        send(signal.SIGTERM)
        deadline = time.monotonic() + grace
        while time.monotonic() < deadline and send(0):
            time.sleep(0.025)
        if send(0):
            send(signal.SIGKILL)
        process.wait()


def public_configuration(values=None):
    """Accept only explicitly supplied public read-only site configuration."""
    values = dict(values or {})
    if set(values) - PUBLIC_CONFIG:
        raise PageRefused("only explicit public read-only site configuration is accepted")
    if values and set(values) != PUBLIC_CONFIG:
        raise PageRefused("public site URL and anonymous key must be supplied together")
    if not values:
        return values
    url = urlsplit(values["NEXT_PUBLIC_SUPABASE_URL"])
    if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment or url.path not in {"", "/"}:
        raise PageRefused("public site configuration requires an HTTPS origin")
    key = values["NEXT_PUBLIC_SUPABASE_ANON_KEY"]
    if not isinstance(key, str):
        raise PageRefused("site key must identify the anonymous presentation role")
    if key.startswith("sb_publishable_") and len(key) > len("sb_publishable_"):
        return values
    try:
        encoded = key.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
    except (IndexError, ValueError, UnicodeDecodeError):
        raise PageRefused("site key must identify the anonymous presentation role") from None
    if not isinstance(claims, dict) or claims.get("role") != "anon":
        raise PageRefused("site key must identify the anonymous presentation role")
    return values


@contextmanager
def _termination_guard():
    # SIGINT already raises KeyboardInterrupt. Make SIGTERM take the same
    # cleanup path for this CLI lifetime, restoring the caller's handler.
    main_thread = threading.current_thread() is threading.main_thread()
    previous = signal.getsignal(signal.SIGTERM) if main_thread else None
    if main_thread:
        def interrupted(_number, _frame):
            raise KeyboardInterrupt
        signal.signal(signal.SIGTERM, interrupted)
    try:
        yield
    finally:
        if main_thread:
            signal.signal(signal.SIGTERM, previous)


class DockerBuild:
    """Use an existing local Docker engine with an explicitly pinned image.

    Only the exported public Git tree is mounted. The Docker client retains
    local engine discovery; none of that host context crosses into the build.
    No host npm fallback is available when the supported boundary refuses.
    """

    FETCH = """
const [route, expected] = process.argv.slice(1);
const response = await fetch('http://127.0.0.1:3000' + route, {
  redirect: 'manual', signal: AbortSignal.timeout(5000)
});
if (response.status !== Number(expected) ||
    !(response.headers.get('content-type') || '').startsWith('text/html'))
  throw new Error('served route status/type differs from build classification');
const html = await response.text();
if (Buffer.byteLength(html) > 10 * 1024 * 1024) throw new Error('page exceeds collection bound');
process.stdout.write(html);
"""
    READY = """
const until = Date.now() + 15000;
while (true) {
  try {
    const r = await fetch('http://127.0.0.1:3000/', {redirect:'manual', signal:AbortSignal.timeout(500)});
    if (r.status === 200) break;
  } catch {}
  if (Date.now() >= until) throw new Error('site did not become ready');
  await new Promise(resolve => setTimeout(resolve,100));
}
"""

    def __init__(self, image, *, timeout=300):
        if not isinstance(image, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
            raise PageRefused("an approved immutable Docker image identity is required")
        if not isinstance(timeout, (int, float)) or not 0 < timeout <= 3600:
            raise PageRefused("build timeout must be positive and at most one hour")
        binary = shutil.which("docker")
        if not binary:
            raise PageRefused("supported Docker runtime is unavailable")
        self.client = [str(Path(binary).resolve())]
        self.environment = {key: os.environ[key] for key in (
            "PATH", "HOME", "TMPDIR", "DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CONFIG",
            "XDG_RUNTIME_DIR", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH",
        ) if key in os.environ}
        self.image, self.timeout = image, timeout
        self.name = "ams-page-build-" + uuid.uuid4().hex
        self.owner = uuid.uuid4().hex
        self.container_id = None
        self.cleanup_verified = False
        self.last_diagnostic = ""

    def _command(self, arguments, *, check=True, timeout=None):
        with tempfile.TemporaryFile() as output:
            with owned_process(self.client + arguments, cwd=tempfile.gettempdir(),
                               environment=self.environment, output=output) as process:
                try:
                    code = process.wait(timeout=timeout or self.timeout)
                except subprocess.TimeoutExpired:
                    raise PageRefused(f"Docker {arguments[0]} exceeded its bounded timeout") from None
            output.seek(0)
            data = output.read(12 * 1024 * 1024 + 1)
        if len(data) > 12 * 1024 * 1024:
            raise PageRefused("runtime output exceeds the collection bound")
        text = data.decode("utf-8", "replace")
        if code and check:
            self.last_diagnostic = text[-16384:]
            raise PageRefused(f"Docker {arguments[0]} failed with exit {code}; no host-execution fallback")
        return subprocess.CompletedProcess(arguments, code, text)

    def _cleanup(self):
        target = self.container_id or self.name
        observed = self._command(["inspect", "--format", '{{.Id}} {{index .Config.Labels "ams.pages.owner"}}', target], check=False, timeout=10)
        if observed.returncode:
            if "no such" in observed.stdout.lower():
                self.cleanup_verified = True
                return
            raise PageRefused("owned container cleanup could not be verified")
        identity = observed.stdout.strip().split()
        if len(identity) != 2 or identity[1] != self.owner:
            raise PageRefused("container ownership differs; cleanup refused")
        self._command(["rm", "--force", identity[0]], timeout=10)
        absent = self._command(["inspect", "--format", "{{.Id}}", identity[0]], check=False, timeout=10)
        if absent.returncode == 0 or "no such" not in absent.stdout.lower():
            raise PageRefused("owned container remains or cleanup readback is unavailable")
        self.cleanup_verified = True

    @contextmanager
    def __call__(self, exported, candidate, public_config):
        config = public_configuration(public_config)
        endpoint = self._command(["context", "inspect", "--format", "{{.Endpoints.docker.Host}}"], timeout=10).stdout.strip()
        if not endpoint.startswith("unix://"):
            raise PageRefused("only the existing local Docker engine is permitted")
        self.client += ["--host", endpoint]
        self.environment.pop("DOCKER_CONTEXT", None)
        self.environment.pop("DOCKER_HOST", None)
        installed = self._command(["image", "inspect", "--format", "{{.Id}}", self.image], timeout=10).stdout.strip()
        if installed != self.image:
            raise PageRefused("approved immutable Node image is unavailable")
        env = {"HOME": "/tmp/ams-pages-home", "NPM_CONFIG_USERCONFIG": "/tmp/ams-pages-user.npmrc",
               "NPM_CONFIG_GLOBALCONFIG": "/tmp/ams-pages-global.npmrc", "NPM_CONFIG_CACHE": "/tmp/ams-pages-cache",
               "NEXT_TELEMETRY_DISABLED": "1", "VERCEL_GIT_COMMIT_SHA": candidate, **config}
        command = ["create", "--name", self.name, "--label", f"ams.pages.owner={self.owner}",
                   "--init", "--user", f"{os.getuid()}:{os.getgid()}", "--read-only",
                   "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", "256",
                   "--network", "bridge", "--tmpfs", "/tmp:rw,nosuid,nodev",
                   "--mount", f"type=bind,source={exported},target=/workspace",
                   "--workdir", "/workspace/site"]
        for key, value in env.items():
            command += ["--env", f"{key}={value}"]
        command += [self.image, "sh", "-c", "mkdir -p /tmp/ams-pages-home && touch /tmp/ams-pages-user.npmrc /tmp/ams-pages-global.npmrc && sleep infinity"]
        with _termination_guard():
            try:
                created = self._command(command).stdout.strip()
                if not re.fullmatch(r"[0-9a-f]{64}", created):
                    raise PageRefused("owned container identity was not returned")
                self.container_id = created
                self._command(["start", self.container_id])
                self._command(["exec", self.container_id, "npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund", "--registry=https://registry.npmjs.org"])
                # Package acquisition uses public registry access; candidate
                # build and serving retain only their own loopback afterwards.
                self._command(["network", "disconnect", "bridge", self.container_id])
                self._command(["exec", self.container_id, "npm", "run", "build"])
                with tempfile.TemporaryFile() as log:
                    with owned_process(self.client + ["exec", self.container_id, "node", "node_modules/next/dist/bin/next", "start", "--hostname", "127.0.0.1", "--port", "3000"],
                                       cwd=tempfile.gettempdir(), environment=self.environment, output=log) as server:
                        self._command(["exec", self.container_id, "node", "--input-type=module", "-e", self.READY], timeout=20)
                        def read(route, expected_status):
                            if server.poll() is not None:
                                raise PageRefused("owned site server exited before collection")
                            request = f"/__ams_review_missing_{self.owner}__" if route == "/_not-found" else route
                            return self._command(["exec", self.container_id, "node", "--input-type=module", "-e", self.FETCH, request, str(expected_status)], timeout=10).stdout
                        yield read
            finally:
                self._cleanup()


def _pin(source, ref, expected_candidate, expected_origin):
    if not SHA.fullmatch(expected_candidate):
        raise PageRefused("expected candidate must be an immutable commit")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/._-]{0,199}", ref) or ".." in ref:
        raise PageRefused("source ref must be a plain branch/ref or immutable commit")
    try:
        origin = _git(source, "remote", "get-url", "origin").strip()
        if origin != expected_origin:
            raise PageRefused("source repository does not match the trusted origin")
        candidate = _git(source, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    except AnswerRefused as error:
        raise PageRefused("trusted source repository/ref is unavailable") from error
    if candidate != expected_candidate:
        raise PageRefused("candidate changed: source ref no longer matches the frozen identity")
    return candidate


@contextmanager
def _export(source, candidate):
    """Export tracked bytes only; archive extraction cannot traverse outside."""
    archive = _git(source, "archive", "--format=tar", candidate, binary=True)
    with tempfile.TemporaryDirectory(prefix="ams-page-build-") as temporary:
        exported = Path(temporary) / "tree"
        exported.mkdir()
        try:
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tree:
                for member in tree.getmembers():
                    name = Path(member.name).name
                    if name in {".git", ".npmrc", ".netrc", ".gitconfig", ".env"} or (name.startswith(".env.") and not name.endswith(".example")):
                        raise PageRefused("candidate tree contains forbidden private/build configuration")
                tree.extractall(exported, filter="data")
        except (tarfile.TarError, OSError) as error:
            raise PageRefused("candidate tree cannot be safely exported") from error
        yield exported


def built_routes(exported):
    """Classify actual artifacts, including the visitor-facing 404 surface."""
    app = _safe_file(Path(exported), "site/.next/server/app")
    if not app.is_dir():
        raise PageRefused("runner produced no Next.js page build")
    routes, excluded = {}, {}
    for file in sorted(app.rglob("*.html")):
        if file.is_symlink():
            raise PageRefused("built page artifacts must be regular files")
        relative = file.relative_to(app).as_posix()
        if relative == "_global-error.html":
            excluded[relative] = "internal framework fallback"
            continue
        name = relative[:-5]
        route = "/" if name == "index" else "/" + name.removesuffix("/index")
        if route in routes:
            raise PageRefused(f"duplicate built route: {route}")
        routes[route] = {"file": file, "kind": "visitor-404" if route == "/_not-found" else "page"}
    if not routes:
        raise PageRefused("runner produced no public page artifacts")
    return routes, excluded


def collect_current(source, ref, expected_candidate, *, build_start, public_config=None,
                    expected_origin=AMS_ORIGIN):
    """Build/start one frozen tree through the supplied owned execution seam.

    ``build_start(exported_root, candidate, public_config)`` is a context manager
    yielding ``read(route, expected_status)``. Production uses the container
    runner; injection supplies inert deterministic fixtures, never live proof.
    """
    source = Path(source).resolve()
    config = public_configuration(public_config)
    candidate = _pin(source, ref, expected_candidate, expected_origin)
    with _export(source, candidate) as exported:
        try:
            listed = json.loads((exported / "site/page-list.json").read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise PageRefused("pinned tree has no readable page-owner inventory") from error
        with build_start(exported, candidate, config) as read:
            routes, excluded = built_routes(exported)
            # Refuse missing owners before requests or any Board operation.
            _metadata(listed, routes)
            served = {}
            for route, metadata in routes.items():
                expected = 404 if metadata["kind"] == "visitor-404" else 200
                html = read(route, expected)
                if content_hash(html) != content_hash(metadata["file"].read_text()):
                    raise PageRefused(f"{route}: served content differs from the frozen build")
                served[route] = html
            return {"candidate": candidate, "inventory": listed, "html": served,
                    "kinds": {route: value["kind"] for route, value in routes.items()}, "excluded": excluded}
