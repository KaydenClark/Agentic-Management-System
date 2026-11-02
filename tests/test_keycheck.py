"""Tests for the Supabase service-key check (S-006 TK-001).

Every key here is fake and generated in this file. The HTTP layer is stubbed,
so no test reaches Supabase.
"""

import base64
import json
import logging
import random
import string

import pytest

from ams import keycheck

URL = "https://example-project.supabase.co"

_rng = random.Random(20261101)
_ALPHABET = string.ascii_letters + string.digits


def _random(n):
    return "".join(_rng.choice(_ALPHABET) for _ in range(n))


def _b64(obj):
    raw = json.dumps(obj, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


FAKE_SECRET = "sb_secret_" + _random(40)
FAKE_JWT = ".".join(
    [
        _b64({"alg": "HS256", "typ": "JWT"}),
        _b64({"iss": "supabase", "ref": _random(20), "role": "service_role"}),
        _random(43),
    ]
)
FAKE_KEYS = {"sb_secret": FAKE_SECRET, "legacy-jwt": FAKE_JWT}


class StubHttp:
    """Records each request and answers with a fixed status."""

    def __init__(self, status):
        self.status = status
        self.calls = []

    def __call__(self, url, headers):
        self.calls.append((url, dict(headers)))
        if isinstance(self.status, Exception):
            raise self.status
        return self.status


def _prefix(key):
    for prefix in ("sb_secret_", "eyJ"):
        if key.startswith(prefix):
            return prefix
    return ""


def assert_no_leak(key, *texts):
    """Fail if any text holds the key or a piece of it longer than its prefix."""
    size = len(_prefix(key)) + 1
    pieces = {key[i : i + size] for i in range(len(key) - size + 1)}
    for text in texts:
        assert key not in text
        leaked = sorted(p for p in pieces if p in text)
        assert not leaked, f"key fragment(s) leaked: {len(leaked)}"


def run(capsys, caplog, *, environ, dotenv_path, http):
    caplog.set_level(logging.DEBUG)
    code = keycheck.main(environ=environ, dotenv_path=dotenv_path, http_get=http)
    out, err = capsys.readouterr()
    return code, out, err, caplog.text


# --- format recognition -----------------------------------------------------


@pytest.mark.parametrize("label,key", FAKE_KEYS.items(), ids=list(FAKE_KEYS))
def test_format_is_recognized(label, key):
    assert keycheck.key_format(key) == label


def test_other_strings_are_unrecognized():
    assert keycheck.key_format("sb_publishable_" + _random(20)) == "unrecognized"
    assert keycheck.key_format("not-a-key") == "unrecognized"


# --- loading ----------------------------------------------------------------


def test_unset_reports_loaded_no_and_exits_nonzero(capsys, caplog, tmp_path):
    http = StubHttp(200)
    code, out, err, logs = run(
        capsys, caplog, environ={}, dotenv_path=tmp_path / "absent", http=http
    )
    assert code != 0
    assert "loaded: no" in out
    assert http.calls == []


def test_empty_value_counts_as_unset(capsys, caplog, tmp_path):
    code, out, *_ = run(
        capsys,
        caplog,
        environ={"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": "  "},
        dotenv_path=tmp_path / "absent",
        http=StubHttp(200),
    )
    assert code != 0
    assert "loaded: no" in out


def test_dotenv_file_is_read_when_environment_is_unset(capsys, caplog, tmp_path):
    dotenv = tmp_path / "local-env"
    dotenv.write_text(
        "# local secrets\n"
        f"export SUPABASE_URL='{URL}'\n"
        f'SUPABASE_SERVICE_ROLE_KEY="{FAKE_SECRET}"\n'
        "OTHER=ignored\n"
    )
    http = StubHttp(200)
    code, out, err, logs = run(
        capsys, caplog, environ={}, dotenv_path=dotenv, http=http
    )
    assert code == 0
    assert "loaded: yes" in out
    assert http.calls[0][1]["apikey"] == FAKE_SECRET
    assert_no_leak(FAKE_SECRET, out, err, logs)


def test_environment_wins_over_dotenv(tmp_path):
    dotenv = tmp_path / "local-env"
    dotenv.write_text(f"SUPABASE_SERVICE_ROLE_KEY={FAKE_JWT}\nSUPABASE_URL={URL}\n")
    settings = keycheck.load_settings(
        environ={"SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET}, dotenv_path=dotenv
    )
    assert settings.key == FAKE_SECRET
    assert settings.url == URL


def test_url_defaults_to_the_recorded_project(tmp_path):
    settings = keycheck.load_settings(
        environ={"SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET},
        dotenv_path=tmp_path / "absent",
    )
    assert settings.url == "https://hqvtnpvwwppbeurponnn.supabase.co"


# --- the request ------------------------------------------------------------


@pytest.mark.parametrize("label,key", FAKE_KEYS.items(), ids=list(FAKE_KEYS))
def test_key_goes_in_apikey_header_of_rest_root(capsys, caplog, tmp_path, label, key):
    http = StubHttp(200)
    code, out, err, logs = run(
        capsys,
        caplog,
        environ={"SUPABASE_URL": URL + "/", "SUPABASE_SERVICE_ROLE_KEY": key},
        dotenv_path=tmp_path / "absent",
        http=http,
    )
    assert code == 0
    [(url, headers)] = http.calls
    assert url == URL + "/rest/v1/"
    assert headers["apikey"] == key
    # Review N6 at d6d4a6d: the check authenticates the way the writers do, so a
    # legacy JWT is also sent as a bearer token and a pass means the writers work.
    if label == "legacy-jwt":
        assert headers["Authorization"] == "Bearer " + key
    else:
        assert "Authorization" not in headers
    from ams import writer
    sent = {k: v for k, v in writer._headers(key).items() if k in ("apikey", "Authorization")}
    assert headers == sent
    assert f"format: {label}" in out
    assert "authenticated: yes" in out
    assert "http status: 200" in out


@pytest.mark.parametrize("status", [401, 403])
@pytest.mark.parametrize("label,key", FAKE_KEYS.items(), ids=list(FAKE_KEYS))
def test_refusal_reports_authenticated_no(capsys, caplog, tmp_path, label, key, status):
    code, out, err, logs = run(
        capsys,
        caplog,
        environ={"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": key},
        dotenv_path=tmp_path / "absent",
        http=StubHttp(status),
    )
    assert code != 0
    assert "loaded: yes" in out
    assert f"format: {label}" in out
    assert "authenticated: no" in out
    assert f"http status: {status}" in out


def test_network_failure_reports_authenticated_no(capsys, caplog, tmp_path):
    error = OSError(f"connection failed while sending {FAKE_SECRET}")
    code, out, err, logs = run(
        capsys,
        caplog,
        environ={"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET},
        dotenv_path=tmp_path / "absent",
        http=StubHttp(error),
    )
    assert code != 0
    assert "authenticated: no" in out
    assert "http status: none" in out
    assert_no_leak(FAKE_SECRET, out, err, logs)


def test_unrecognized_key_is_not_sent(capsys, caplog, tmp_path):
    key = "sb_publishable_" + _random(30)
    http = StubHttp(200)
    code, out, err, logs = run(
        capsys,
        caplog,
        environ={"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": key},
        dotenv_path=tmp_path / "absent",
        http=http,
    )
    assert code != 0
    assert "format: unrecognized" in out
    assert "authenticated: no" in out
    assert http.calls == []
    assert key not in out + err + logs


# --- no leak on any path ----------------------------------------------------

PATHS = {
    "accepted": 200,
    "refused-401": 401,
    "refused-403": 403,
    "server-error": 500,
    "network": OSError("boom"),
}


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("label,key", FAKE_KEYS.items(), ids=list(FAKE_KEYS))
@pytest.mark.parametrize("source", ["environ", "dotenv"])
def test_no_path_leaks_the_key(capsys, caplog, tmp_path, path, label, key, source):
    dotenv = tmp_path / "local-env"
    environ = {}
    if source == "environ":
        environ = {"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": key}
    else:
        dotenv.write_text(f"SUPABASE_URL={URL}\nSUPABASE_SERVICE_ROLE_KEY={key}\n")
    before = sorted(p.name for p in tmp_path.iterdir())
    code, out, err, logs = run(
        capsys, caplog, environ=environ, dotenv_path=dotenv, http=StubHttp(PATHS[path])
    )
    assert out.strip(), "the check always reports"
    assert_no_leak(key, out, err, logs)
    assert sorted(p.name for p in tmp_path.iterdir()) == before, "no file written"


def test_leak_detector_catches_a_fragment():
    with pytest.raises(AssertionError):
        assert_no_leak(FAKE_SECRET, "prefix " + FAKE_SECRET[:11])
    with pytest.raises(AssertionError):
        assert_no_leak(FAKE_JWT, FAKE_JWT[10:14])
    assert_no_leak(FAKE_SECRET, "format: sb_secret, prefix sb_secret_")
