"""Public hygiene and character limits over records, controls and the built site (S-001 TK-002).

Planted values are assembled at run time, so this file holds no key-, path- or
session-shaped literal of its own.
"""

import json
import subprocess
from pathlib import Path

import pytest

from ams import hygiene

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "site"
J = "".join

PLANTED = [
    ("host path", J(["/ho", "me/someone/project/notes.md"])),
    ("host path", J(["/Us", "ers/someone/Code/AMS"])),
    ("host path", J(["C:", "\\Users\\some", "one\\AMS"])),
    ("host path", J(["file:", "///C:/Us", "ers/someone/AMS"])),
    ("credential", J(["sb_", "secret_", "AbCdEf0123456789"])),
    ("credential", J(["sk-", "ant-", "a" * 30])),
    ("credential", J(["sk-", "b" * 32])),
    ("credential", J(["sk-", "proj-", "Ab_c-" * 20])),
    ("credential", J(["sk-", "svcacct-", "Ab_c-" * 20])),
    ("credential", J(["gh", "p_", "c" * 36])),
    ("credential", J(["github", "_pat_", "d" * 30])),
    ("credential", J(["xox", "b-", "1234567890-abcdef"])),
    ("credential", J(["AK", "IA", "ABCDEFGHIJKLMNOP"])),
    ("credential", J(["Bea", "rer ", "e" * 24])),
    ("credential", J(["-----BEGIN ", "RSA PRIVATE", " KEY-----"])),
    ("credential", J(["ey", "JhbGciOiJIUzI1NiJ9", ".", "eyJyb2xlIjoic2VydmljZV9yb2xlIn0", ".sig"])),
    ("private record ID", J(["claude.ai/code/", "session_", "01AbCdEfGhIjKlMnOpQrStUv"])),
    ("private record ID", J(["session", "_01", "AbCdEfGhIjKlMnOpQrStUv"])),
]


@pytest.mark.parametrize("label,value", PLANTED)
def test_each_planted_value_is_refused_by_class_and_line(label, value):
    hits = hygiene.text_findings(f"clean line\nsee {value} here\n")
    assert [(h.line, h.label) for h in hits] == [(2, label)]
    assert value not in " ".join(str(h) for h in hits)


def test_ordinary_prose_passes():
    text = "\n".join([
        "accepts `sb_secret_` and sb_publishable_AbCdEf0123 keys",
        "skills-installed-here; /homepage; the service role; `/home/` and `/Users/` dirs",
        "Bearer token in the header; a JWT without a role: "
        + J(["ey", "JhbGciOiJIUzI1NiJ9", ".", "eyJzdWIiOiJ4In0", ".sig"]),
        "session_id and session_01 short",
        "repo/root/file and ~/project",
    ])
    assert hygiene.text_findings(text) == []


def _limit(name, n, char="a"):
    return hygiene.limit_failure(name, char * n)


def test_record_limit_counts_code_points_not_bytes():
    assert _limit("workbench/specs/S-1/SPEC.md", 8000) is None
    assert _limit("workbench/specs/S-1/SPEC.md", 8001) is not None
    # 8,000 four-byte characters (32,000 bytes) are within the limit.
    assert _limit("workbench/landmarks/LMK-1/LANDMARK.md", 8000, "\U0001F600") is None
    assert _limit("workbench/landmarks/LMK-1/LANDMARK.md", 8001, "\U0001F600") is not None
    assert _limit("a/tasks/TK-1/TASK.md", 8001) == "a/tasks/TK-1/TASK.md: 8001 characters; maximum 8000"
    # CRLF counts as one character, as the Workbench budget tool counts it.
    assert hygiene.limit_failure("x/SPEC.md", "a\r\n" * 4000) is None


@pytest.mark.parametrize("control", hygiene.ROOT_CONTROLS)
def test_every_root_control_is_limited_to_3000(control):
    assert _limit(control, 3000) is None
    assert _limit(control, 3001) == f"{control}: 3001 characters; maximum 3000"


def test_limits_apply_by_place_not_by_any_name():
    assert _limit("workbench/wiki/AGENTS.md", 5000) is None  # not a root control
    assert _limit("notes.md", 20000) is None
    assert _limit("workbench/specs/SPEC-TEMPLATE.md", 9000) is None  # a template is not a record


def test_limits_agree_with_the_budget_file():
    budgets = json.loads((REPO_ROOT / "workbench/artifact-budgets.json").read_text())["artifacts"]
    assert budgets["SPEC.md"]["maxCharacters"] == hygiene.RECORD_LIMIT
    assert budgets["TASK.md"]["maxCharacters"] == hygiene.RECORD_LIMIT
    assert budgets["LANDMARK.md"]["maxCharacters"] == hygiene.RECORD_LIMIT
    for control in ("AGENTS.md", "BLUEPRINT.md", "ARCHITECTURE.md", "RUNBOOK.md"):
        assert budgets[control]["maxCharacters"] == hygiene.CONTROL_LIMIT


def test_a_split_record_is_refused():
    assert hygiene.is_split("workbench/specs/S-1/SPEC.md.part-1." + "a" * 64 + ".md")
    assert hygiene.is_split("x/TASK.part-2.md")
    assert not hygiene.is_split("workbench/specs/S-1/SPEC.md")
    assert not hygiene.is_split("docs/department-list.md")


def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def test_the_repository_check_reads_tracked_files_and_names_only_the_place(tmp_path):
    _git(tmp_path, "init", "-q")
    secret = J(["sb_", "secret_", "AbCdEf0123456789"])
    (tmp_path / "AGENTS.md").write_text("a" * 3001)
    (tmp_path / "leak.md").write_text(f"\nKEY={secret}\n")
    (tmp_path / "workbench/specs/S-1").mkdir(parents=True)
    (tmp_path / "workbench/specs/S-1/SPEC.md").write_text("ok\n")
    (tmp_path / "workbench/specs/S-1/SPEC.md.part-1.md").write_text("ok\n")
    (tmp_path / "untracked.md").write_text(secret)
    _git(tmp_path, "add", "AGENTS.md", "leak.md", "workbench")
    found = hygiene.check_repository(tmp_path)
    assert found == [
        "AGENTS.md: 3001 characters; maximum 3000",
        "leak.md:2: credential",
        "workbench/specs/S-1/SPEC.md.part-1.md: split record",
    ]
    assert secret not in " ".join(found)


def _built_site(root, page_text):
    app = root / ".next" / "server" / "app"
    static = root / ".next" / "static" / "chunks"
    app.mkdir(parents=True)
    static.mkdir(parents=True)
    (app / "index.html").write_text(page_text)
    (static / "main.js").write_text("console.log(1)")
    cache = root / ".next" / "cache"
    cache.mkdir()
    (cache / "trace.json").write_text(J(["/Us", "ers/someone/build"]))  # not served
    return root


def test_the_site_check_reads_served_build_output_only(tmp_path):
    site = _built_site(tmp_path, "<main>ok</main>")
    assert hygiene.check_site(site) == []
    (site / ".next/server/app/index.html").write_text(
        "<main>" + J(["/ho", "me/someone/x"]) + "</main>")
    assert hygiene.check_site(site) == ["site/.next/server/app/index.html:1: host path"]


def test_the_site_check_refuses_a_missing_build(tmp_path):
    with pytest.raises(hygiene.NoBuild):
        hygiene.check_site(tmp_path)


def test_the_cli_exits_nonzero_and_names_findings(tmp_path, capsys):
    _git(tmp_path, "init", "-q")
    (tmp_path / "RUNBOOK.md").write_text("ok\n")
    _git(tmp_path, "add", "RUNBOOK.md")
    assert hygiene.main(["--root", str(tmp_path)]) == 0
    site = _built_site(tmp_path / "site", "<main>" + J(["gh", "p_", "c" * 36]) + "</main>")
    (tmp_path / "RUNBOOK.md").write_text("a" * 3001)  # a repository finding the site run ignores
    capsys.readouterr()
    assert hygiene.main(["--site", str(site)]) == 1
    out = capsys.readouterr().out
    assert "site/.next/server/app/index.html:1: credential" in out
    assert "RUNBOOK.md" not in out and "c" * 36 not in out
    assert hygiene.main(["--site", str(tmp_path / "unbuilt")]) == 2


# The real repository on every candidate. Findings fail here; the check is
# never narrowed to make them pass (S-001 Limits and Hygiene).
def test_the_repository_is_clean():
    found = hygiene.check_repository(REPO_ROOT)
    assert found == [], "hygiene and limit findings:\n" + "\n".join(found)


@pytest.mark.skipif(not (SITE_DIR / ".next" / "server" / "app").is_dir(),
                    reason="no site build here; site CI runs `ams-hygiene --site site` after `npm run build`")
def test_the_built_site_is_clean():
    assert hygiene.check_site(SITE_DIR) == []
