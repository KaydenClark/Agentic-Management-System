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
import signal
import subprocess
import tarfile
import tempfile
import time
from urllib.parse import urlsplit

from .grill_board.answers import AnswerRefused, _git
from .pages import PageRefused, _metadata, content_hash

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
    if claims.get("role") != "anon":
        raise PageRefused("site key must identify the anonymous presentation role")
    return values


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
    app = Path(exported) / "site/.next/server/app"
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
