"""S-013 TK-002: fixture tests for the up-to-Spec report (ADR-001F).

A criterion is met only when its acceptance line carries evidence that resolves at
the checked commit (a commit SHA or a repository path). Checked without such
evidence is unknown; unchecked is not met.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from ams.coherence.up_to_spec import check_spec, render_report

SPEC_TEMPLATE = """# S-900 - Fixture

**Spec ID:** S-900
**Status:** active

## Acceptance Criteria

- [x] **Evidenced.** Works. *Evidence:* `{sha}`, [test](tests/test_thing.py).
- [x] **Unevidenced.** Claimed done with nothing linked.
- [x] **Bogus evidence.** *Evidence:* `deadbeefdeadbeef` and `tests/missing.py`.
- [ ] **Open.** Not done yet. *Check:* `tests/test_thing.py`.
- [x] **Sibling link.** *Evidence:* [result](evidence.md) and [up](../../../../../tests/test_thing.py).
- [x] **Side branch.** *Evidence:* `{side}`.

## RSI and website connection

none
"""

TASK = """# TK-001 - slice

**Task ID:** TK-001
**Spec ID:** S-900
**Status:** done
**Destination:** spec-acceptance: Evidenced; Open
**Proof:** fixture proof
"""


def _git(cwd, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def _fixture():
    d = tempfile.mkdtemp(prefix="uts-")
    _git(d, "init", "-q", "-b", "main")
    Path(d, "tests").mkdir()
    Path(d, "tests/test_thing.py").write_text("pass\n")
    _git(d, "add", ".")
    _git(d, "commit", "-q", "-m", "evidence")
    sha = _git(d, "rev-parse", "HEAD")
    # A commit that exists in the repository but only on an unmerged branch.
    _git(d, "checkout", "-q", "-b", "side")
    Path(d, "side.txt").write_text("side\n")
    _git(d, "add", ".")
    _git(d, "commit", "-q", "-m", "side")
    side = _git(d, "rev-parse", "HEAD")
    _git(d, "checkout", "-q", "main")
    spec_dir = Path(d, "workbench/landmarks/LMK-900-x/specs/S-900-fixture")
    (spec_dir / "tasks/TK-001").mkdir(parents=True)
    (spec_dir / "SPEC.md").write_text(SPEC_TEMPLATE.format(sha=sha[:12], side=side[:12]))
    (spec_dir / "evidence.md").write_text("result\n")
    (spec_dir / "tasks/TK-001/TASK.md").write_text(TASK)
    _git(d, "add", ".")
    _git(d, "commit", "-q", "-m", "spec")
    return d, _git(d, "rev-parse", "HEAD")


class UpToSpecTest(unittest.TestCase):
    def setUp(self):
        self.repo, self.commit = _fixture()
        self.report = check_spec("S-900", repo=self.repo, commit=self.commit)
        self.by_name = {c["name"]: c for c in self.report["criteria"]}

    def test_evidenced_is_met_unevidenced_is_unknown(self):
        self.assertEqual(self.by_name["Evidenced"]["status"], "met")
        self.assertEqual(self.by_name["Unevidenced"]["status"], "unknown")

    def test_unresolvable_evidence_is_not_met(self):
        self.assertEqual(self.by_name["Bogus evidence"]["status"], "unknown")
        self.assertEqual(self.by_name["Bogus evidence"]["evidence"], [])

    def test_markdown_links_resolve_relative_to_the_spec(self):
        c = self.by_name["Sibling link"]
        self.assertEqual(c["status"], "met")
        self.assertIn("workbench/landmarks/LMK-900-x/specs/S-900-fixture/evidence.md", c["evidence"])
        self.assertIn("tests/test_thing.py", c["evidence"])

    def test_commit_off_the_checked_history_is_not_evidence(self):
        # Codex review on PR #11: an unmerged commit must not make a line met.
        self.assertEqual(self.by_name["Side branch"]["status"], "unknown")

    def test_unchecked_is_not_met_and_check_text_is_not_evidence(self):
        self.assertEqual(self.by_name["Open"]["status"], "not met")
        self.assertEqual(self.by_name["Open"]["evidence"], [])

    def test_no_criterion_met_without_evidence(self):
        # Must-fail invariant from S-013 "Up to Spec": met implies resolved evidence.
        for c in self.report["criteria"]:
            if c["status"] == "met":
                self.assertTrue(c["evidence"], c["name"])

    def test_related_tasks_listed_by_destination(self):
        self.assertEqual([t["id"] for t in self.by_name["Open"]["tasks"]], ["TK-001"])
        self.assertEqual(self.by_name["Unevidenced"]["tasks"], [])

    def test_report_names_spec_and_commit_and_lists_unmet(self):
        md = render_report(self.report)
        self.assertIn(self.commit, md)
        self.assertIn("S-900", md)
        for name in ("Unevidenced", "Bogus evidence", "Open"):
            self.assertIn(name, md)
        self.assertEqual(self.report["summary"], {"met": 2, "not met": 1, "unknown": 3})


if __name__ == "__main__":
    unittest.main()
