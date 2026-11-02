"""Check that the Supabase service key loads and authenticates (S-006 TK-001).

Reads ``SUPABASE_URL`` and ``SUPABASE_SERVICE_ROLE_KEY`` from the process
environment; a variable that is unset there is read from the gitignored local
environment file at the repository root. Sends one GET to the REST root
(``/rest/v1/``) with the headers the writers use (``auth_headers``): the key in
``apikey``, and for a legacy JWT also as a bearer token. It prints only:

    loaded: yes|no
    format: sb_secret|legacy-jwt|unrecognized
    authenticated: yes|no
    http status: <code>|none

The key value, or any part of it beyond its format prefix, is never printed,
logged, raised or written.
"""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping

URL_VAR = "SUPABASE_URL"
KEY_VAR = "SUPABASE_SERVICE_ROLE_KEY"
# ADR-003C records the project; the URL is public, the key is not.
DEFAULT_URL = "https://hqvtnpvwwppbeurponnn.supabase.co"
REPO_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = REPO_ROOT / ".env"
TIMEOUT_SECONDS = 15

HttpGet = Callable[[str, Mapping[str, str]], int]


@dataclass(frozen=True)
class Settings:
    url: str
    key: str | None = field(repr=False)


def read_dotenv(path: Path, names: tuple[str, ...]) -> dict[str, str]:
    """Return the named variables from a dotenv file; a missing file gives {}."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return {}
    found: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        name, value = line.split("=", 1)
        name, value = name.strip(), value.strip()
        if name not in names:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        found[name] = value
    return found


def load_settings(
    environ: Mapping[str, str] | None = None, dotenv_path: Path | None = None
) -> Settings:
    environ = os.environ if environ is None else environ
    dotenv_path = DOTENV_PATH if dotenv_path is None else dotenv_path
    values = {name: (environ.get(name) or "").strip() for name in (URL_VAR, KEY_VAR)}
    missing = tuple(name for name, value in values.items() if not value)
    if missing:
        for name, value in read_dotenv(dotenv_path, missing).items():
            values[name] = value.strip()
    return Settings(url=values[URL_VAR] or DEFAULT_URL, key=values[KEY_VAR] or None)


def key_format(key: str) -> str:
    if key.startswith("sb_secret_"):
        return "sb_secret"
    if key.startswith("eyJ") and key.count(".") == 2:
        return "legacy-jwt"
    return "unrecognized"


def auth_headers(key: str) -> dict[str, str]:
    """The headers every AMS client authenticates with: ``apikey``, plus a bearer
    token for a legacy JWT key (an ``sb_secret_`` key is never sent as a bearer)."""
    headers = {"apikey": key}
    if key_format(key) == "legacy-jwt":
        headers["Authorization"] = "Bearer " + key
    return headers


def urllib_get(url: str, headers: Mapping[str, str]) -> int:
    request = urllib.request.Request(url, headers=dict(headers), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def main(
    argv: list[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    dotenv_path: Path | None = None,
    http_get: HttpGet | None = None,
) -> int:
    settings = load_settings(environ, dotenv_path)
    if settings.key is None:
        _report(loaded=False)
        return 1
    label = key_format(settings.key)
    if label == "unrecognized":
        # Not a service key; do not send it anywhere.
        _report(loaded=True, label=label)
        return 1
    try:
        status = (http_get or urllib_get)(
            settings.url.rstrip("/") + "/rest/v1/", auth_headers(settings.key)
        )
    except Exception:
        # The exception text is not trusted to be free of the key; drop it.
        status = None
    accepted = status is not None and 200 <= status < 300
    _report(loaded=True, label=label, accepted=accepted, status=status)
    return 0 if accepted else 1


def _report(
    *, loaded: bool, label: str | None = None, accepted: bool = False, status=None
) -> None:
    lines = [f"loaded: {'yes' if loaded else 'no'}"]
    if loaded:
        lines.append(f"format: {label}")
        lines.append(f"authenticated: {'yes' if accepted else 'no'}")
        lines.append(f"http status: {status if status is not None else 'none'}")
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
