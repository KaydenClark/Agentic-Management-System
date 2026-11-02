"""Public hygiene and character limits over records, controls and the built site (S-001 TK-002).

Usage: ``ams-hygiene [--root DIR]`` checks the repository; ``ams-hygiene --site
SITE_DIR`` checks the built site instead. Exit 0 when clean, 1 on any finding,
2 when ``--site`` has no build output.

The repository check reads every file ``git ls-files`` lists. It refuses:

- a host path: a home directory on Linux, macOS or Windows, the root home, or a
  ``file://`` URL naming a drive, home or temp directory;
- a credential: a Supabase secret key, a JWT whose payload carries a ``role``
  claim (Supabase's legacy keys), a private key block, an Anthropic/OpenAI/
  GitHub/Slack/AWS token shape or a bearer token;
- a private record ID: an agent session ID or session link, which names a
  private transcript (the site check, TK-005, refuses the same shapes). The
  private repository's name alone is a pointer AGENTS.md publishes, not an ID;
- a split record: any ``.part-`` file (ADR-002V: never split);
- a Spec, Task or Landmark record over 8,000 characters, or one of the eight
  root controls over 3,000 (S-001 Decisions; ``workbench/artifact-budgets.json``).

Characters are Unicode code points after CRLF/CR become LF, as the Workbench
budget tool counts them. ``--site`` scans what the built site serves
(``.next/server/app`` pages and ``.next/static`` JS/CSS). A finding names its
file, line and class, never the matched value.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

RECORD_LIMIT = 8000
CONTROL_LIMIT = 3000
RECORDS = frozenset({"SPEC.md", "TASK.md", "TASKS.md", "LANDMARK.md"})
# The eight root controls (workbench/tools/workbench-layout.mjs `controls`).
ROOT_CONTROLS = ("AGENTS.md", "BLUEPRINT.md", "GLOSSARY.md", "ARCHITECTURE.md",
                 "RUNBOOK.md", "TASKBOARD.md", "CLAUDE.md", "README.md")

SB_SECRET = re.compile(r"sb_secret_[A-Za-z0-9_-]{8,}")
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]+\.([A-Za-z0-9_-]+)\.[A-Za-z0-9_-]+")

_NOT_PATH_START = r"(?<![\w.~-])"
PATTERNS = (
    ("host path", re.compile(
        _NOT_PATH_START + r"(?:/home/|/Users/|/root/)[A-Za-z0-9._-]+"
        r"|\b[A-Za-z]:[\\/]{1,2}Users[\\/]{1,2}[A-Za-z0-9._-]+"
        r"|file:///(?:[A-Za-z]:|home/|Users/|root/|tmp/|var/|private/|opt/)")),
    ("credential", SB_SECRET),
    ("credential", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("credential", re.compile(
        r"\b(?:sk-ant-[A-Za-z0-9_-]{20,}|sk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}|(?:sk|pk)-[A-Za-z0-9_]{20,}|gh[oprsu]_[A-Za-z0-9]{20,}"
        r"|github_pat_[A-Za-z0-9_]{20,}|xox[abpr]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b")),
    ("credential", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("private record ID", re.compile(r"claude\.ai/code/session_[A-Za-z0-9]+|\bsession_0[A-Za-z0-9]{20,}")),
)


class NoBuild(Exception):
    """The site directory holds no build output to check."""


@dataclass(frozen=True)
class Finding:
    line: int
    label: str

    def __str__(self) -> str:
        return f"{self.line}: {self.label}"


def has_role_claim(segment: str) -> bool:
    """True when a JWT payload segment decodes to JSON with a ``role`` claim."""
    try:
        payload = json.loads(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(payload, dict) and "role" in payload


def text_findings(text: str) -> list[Finding]:
    """One finding per line and class; the matched value is never kept."""
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        labels = {label for label, pattern in PATTERNS if pattern.search(line)}
        if any(has_role_claim(m.group(1)) for m in JWT.finditer(line)):
            labels.add("credential")
        found.extend(Finding(number, label) for label in sorted(labels))
    return found


def character_count(text: str) -> int:
    return len(text.replace("\r\n", "\n").replace("\r", "\n"))


def limit_failure(name: str, text: str) -> str | None:
    """The limit message for a record or root control over its limit, else None."""
    path = Path(name)
    if path.name in RECORDS:
        limit = RECORD_LIMIT
    elif len(path.parts) == 1 and path.name in ROOT_CONTROLS:
        limit = CONTROL_LIMIT
    else:
        return None
    count = character_count(text)
    return f"{name}: {count} characters; maximum {limit}" if count > limit else None


def is_split(name: str) -> bool:
    return ".part-" in Path(name).name


def _file_findings(name: str, text: str) -> list[str]:
    return [f"{name}:{f}" for f in text_findings(text)]


def check_repository(root: Path) -> list[str]:
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True,
                            capture_output=True).stdout.decode().split("\0")
    found = []
    for name in filter(None, listed):
        if is_split(name):
            found.append(f"{name}: split record")
        path = Path(root) / name
        if path.is_symlink() or not path.is_file():
            continue
        text = path.read_bytes().decode("utf-8", errors="ignore")
        found.extend(_file_findings(name, text))
        if (failure := limit_failure(name, text)) is not None:
            found.append(failure)
    return sorted(found)


SERVED = ((".next/server/app", (".html", ".rsc", ".meta")), (".next/static", (".js", ".css")))


def check_site(site: Path) -> list[str]:
    """Hygiene over every text file the built site serves (as site/tests/helpers.mjs)."""
    site = Path(site)
    if not (site / SERVED[0][0]).is_dir():
        raise NoBuild(f"no build output under {SERVED[0][0]}; run `npm run build` in site/ first")
    found = []
    for folder, suffixes in SERVED:
        base = site / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in suffixes:
                name = "site/" + path.relative_to(site).as_posix()
                found.extend(_file_findings(name, path.read_bytes().decode("utf-8", errors="ignore")))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ams-hygiene", description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: here)")
    parser.add_argument("--site", type=Path, help="check this built site directory instead")
    args = parser.parse_args(argv)
    if args.site is None:
        found = check_repository(args.root)
    else:
        try:
            found = check_site(args.site)
        except NoBuild as error:
            print(f"ams-hygiene: {error}", file=sys.stderr)
            return 2
    for line in found:
        print(line)
    print(f"hygiene: {len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
