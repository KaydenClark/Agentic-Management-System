"""Repository hygiene: no Supabase service key in any tracked file (S-006 review M3).

The scan reads every file ``git ls-files`` lists and flags the two real secret
shapes: ``sb_secret_`` followed by 8 or more key characters, and a three-part
JWT whose payload decodes to JSON with a ``role`` claim (the legacy service and
anon keys). The bare documented prefix ``sb_secret_`` is allowed. Test fakes are
built at runtime, so no tracked file holds one. A hit names only the file and
line, never the value.
"""

import base64
import json
import random
import re
import string
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SB_SECRET = re.compile(r"sb_secret_[A-Za-z0-9_-]{8,}")
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]+\.([A-Za-z0-9_-]+)\.[A-Za-z0-9_-]+")


def _has_role(segment: str) -> bool:
    try:
        payload = json.loads(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(payload, dict) and "role" in payload


def secret_hits(text: str) -> list[int]:
    """Line numbers holding a real secret shape."""
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        if SB_SECRET.search(line) or any(_has_role(m.group(1)) for m in JWT.finditer(line)):
            hits.append(number)
    return hits


def scan(root: Path) -> list[str]:
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True,
                            capture_output=True).stdout.decode().split("\0")
    found = []
    for name in filter(None, listed):
        path = root / name
        if not path.is_file():
            continue
        text = path.read_bytes().decode("utf-8", errors="ignore")
        found.extend(f"{name}:{line}" for line in secret_hits(text))
    return found


_rng = random.Random()
_ALPHA = string.ascii_letters + string.digits


def _b64(obj) -> str:
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()


def fake_secret() -> str:
    return "sb" + "_secret_" + "".join(_rng.choice(_ALPHA) for _ in range(40))


def fake_jwt(role="service_role") -> str:
    return ".".join([_b64({"alg": "HS256", "typ": "JWT"}),
                     _b64({"iss": "supabase", "role": role}),
                     "".join(_rng.choice(_ALPHA) for _ in range(43))])


def test_no_tracked_file_holds_a_service_key():
    found = scan(REPO_ROOT)
    assert found == [], "secret shapes in tracked files (values not shown): " + ", ".join(found)


@pytest.mark.parametrize("planted", [fake_secret, fake_jwt, lambda: fake_jwt("anon")])
def test_the_scan_fails_on_a_planted_fake(planted):
    assert secret_hits(f"ok line\nKEY={planted()}\n") == [2]


def test_the_bare_prefix_and_non_key_jwts_are_allowed():
    text = ("accepts `sb_secret_` and legacy JWT keys\n"
            "prefix sb_secret_ only\n"
            "sb_secret_abc\n"
            + ".".join(["eyJhbGciOiJIUzI1NiJ9", _b64({"sub": "no role"}), "sig"]) + "\n")
    assert secret_hits(text) == []


def test_the_scan_reads_tracked_files_and_names_only_the_line(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    key = fake_secret()
    (tmp_path / "clean.md").write_text("accepts `sb_secret_` keys\n")
    (tmp_path / "leak.txt").write_text(f"\nSUPABASE_SERVICE_ROLE_KEY={key}\n")
    (tmp_path / "untracked.txt").write_text(key)
    subprocess.run(["git", "-C", str(tmp_path), "add", "clean.md", "leak.txt"], check=True)
    found = scan(tmp_path)
    assert found == ["leak.txt:2"]
    assert key not in " ".join(found)
