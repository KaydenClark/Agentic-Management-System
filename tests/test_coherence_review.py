"""S-013 TK-004 (ADR-001E): independent Spec review procedure.

A review names the exact assembled commit and the reviewing context. It is
refused when that context built the Spec, and it is stale once the commit or
the Spec's content changes after the review.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from ams.coherence.review import (
    Refused,
    builders,
    context_id,
    record,
    status,
)

BUILD_CTX = context_id("session-that-built")
REVIEW_CTX = context_id("fresh-review-session")
PRODUCT_CTX = context_id("session-that-wrote-product-code")

SPEC = """# S-900 - Fixture

**Spec ID:** S-900
**Status:** active

## Acceptance Criteria

- [ ] **Works.** It works.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped | doctor | this Spec | all |
"""

TASK = """# TK-001 - slice

**Task ID:** TK-001
**Spec ID:** S-900
**Status:** in-progress
**Claimed by:** impl-a
**Current claimant:** impl-a
"""

SPEC_DIR = "workbench/landmarks/LMK-900-x/specs/S-900-fixture"


def _git(cwd, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _verdict_row(candidate, reviewer, digest="a" * 12, n=1, result="pass"):
    return (f"| 2026-11-02 | review | Review verdict: {result} at {candidate} [{digest}] #{n} "
            f"| none | {reviewer} | none |\n")


def _fixture():
    """Spec claimed and built by `impl-a` in the session BUILD_CTX names."""
    repo = tempfile.mkdtemp(prefix="review-")
    _git(repo, "init", "-q", "-b", "main")
    Path(repo, "src").mkdir()
    Path(repo, "src/thing.py").write_text("v = 1\n")
    spec = Path(repo, SPEC_DIR)
    (spec / "tasks/TK-001").mkdir(parents=True)
    (spec / "SPEC.md").write_text(SPEC)
    (spec / "tasks/TK-001/TASK.md").write_text(TASK)
    _commit(repo, f"Claim S-900 TK-001\n\nAMS-Context: {BUILD_CTX}")
    # A product-code commit outside the Spec folder still names its Spec.
    Path(repo, "src/thing.py").write_text("v = 1  # built\n")
    _commit(repo, f"Build the S-900 slice\n\nAMS-Context: {PRODUCT_CTX}")
    Path(repo, "src/other.py").write_text("x = 1\n")
    _commit(repo, f"Unrelated S-9001 work\n\nAMS-Context: {REVIEW_CTX}")
    # Task scaffolding is deleted at close (ADR-000T); its claimant must still count.
    (spec / "tasks/TK-001/TASK.md").unlink()
    with (spec / "SPEC.md").open("a") as f:
        f.write('| 2026-11-01 | TK-001 | Task closed | pytest | none | '
                'close attribution: {"agent":"closer-a","claimant":"impl-a","onBehalfOf":null} |\n')
    candidate = _commit(repo, "Close S-900 TK-001")
    return repo, candidate


class BuilderContextsTest(unittest.TestCase):
    def setUp(self):
        self.repo, self.candidate = _fixture()

    def test_builders_come_from_claims_closes_and_commit_trailers(self):
        found = builders("S-900", repo=self.repo, commit=self.candidate)
        self.assertEqual(found["agents"], {"impl-a", "closer-a"})
        self.assertEqual(found["contexts"], {BUILD_CTX, PRODUCT_CTX})

    def test_context_id_hashes_the_session_and_never_stores_it(self):
        self.assertRegex(BUILD_CTX, r"^[0-9a-f]{12}$")
        self.assertNotEqual(BUILD_CTX, REVIEW_CTX)
        self.assertEqual(context_id("session-that-built"), BUILD_CTX)


class RecordRefusesBuilderTest(unittest.TestCase):
    """Acceptance 1: a review recorded by the building session is refused."""

    def setUp(self):
        self.repo, self.candidate = _fixture()
        self.calls = []

    def _record(self, **kw):
        args = dict(spec_id="S-900", candidate=self.candidate, result="pass", findings="none",
                    reviewer="model fresh", repo=self.repo, run_verdict=self.calls.append)
        args.update(kw)
        return record(**args)

    def test_building_session_under_another_agent_name_is_refused(self):
        # ADR-001E: a different agent name in the same session is not independence.
        with self.assertRaises(Refused) as caught:
            self._record(agent="reviewer-b", context=BUILD_CTX)
        self.assertIn("built", str(caught.exception))
        self.assertEqual(self.calls, [])

    def test_building_agent_in_a_new_session_is_refused(self):
        with self.assertRaises(Refused):
            self._record(agent="impl-a", context=REVIEW_CTX)
        with self.assertRaises(Refused):
            self._record(agent="Closer A", context=REVIEW_CTX)
        self.assertEqual(self.calls, [])

    def test_review_naming_no_context_is_refused(self):
        with self.assertRaises(Refused):
            self._record(agent="reviewer-b", context="")
        self.assertEqual(self.calls, [])

    def test_independent_review_is_passed_to_the_native_verdict(self):
        self._record(agent="reviewer-b", context=REVIEW_CTX)
        self.assertEqual(len(self.calls), 1)
        argv = self.calls[0]
        self.assertEqual(argv[:2], ["verdict", "S-900"])
        self.assertIn(self.candidate, argv)
        reviewer = argv[argv.index("--reviewer") + 1]
        self.assertIn("agent: reviewer-b", reviewer)
        self.assertIn(f"context: {REVIEW_CTX}", reviewer)


class StatusTest(unittest.TestCase):
    """Acceptance 2: a review reused after the commit changed is reported stale."""

    def setUp(self):
        self.repo, self.candidate = _fixture()
        self.digest = lambda commit: "a" * 64

    def _append_verdict(self, reviewer, digest="a" * 12, n=1, trailer=""):
        with Path(self.repo, SPEC_DIR, "SPEC.md").open("a") as f:
            f.write(_verdict_row(self.candidate, reviewer, digest, n))
        return _commit(self.repo, "Record S-900 review verdict" + (f"\n\nAMS-Context: {trailer}" if trailer else ""))

    def _status(self, commit):
        return status("S-900", repo=self.repo, commit=commit, digest_at=self.digest)["verdicts"]

    def test_independent_review_is_current_while_only_its_records_change(self):
        head = self._append_verdict(f"model fresh; agent: reviewer-b; context: {REVIEW_CTX}")
        Path(self.repo, "TASKBOARD.md").write_text("regenerated\n")
        head = _commit(self.repo, "Render")
        [v] = self._status(head)
        self.assertEqual(v["status"], "current", v)

    def test_review_reused_after_the_commit_changed_is_stale(self):
        self._append_verdict(f"model fresh; agent: reviewer-b; context: {REVIEW_CTX}")
        Path(self.repo, "src/thing.py").write_text("v = 2\n")
        head = _commit(self.repo, "Change delivered code after review")
        [v] = self._status(head)
        self.assertEqual(v["status"], "stale", v)
        self.assertIn("src/thing.py", " ".join(v["reasons"]))

    def test_review_reused_after_spec_content_changed_is_stale(self):
        head = self._append_verdict(f"model fresh; agent: reviewer-b; context: {REVIEW_CTX}")
        self.digest = lambda commit: "b" * 64
        [v] = self._status(head)
        self.assertEqual(v["status"], "stale", v)
        self.assertIn("content", " ".join(v["reasons"]))

    def test_reviewers_own_verdict_commit_does_not_make_it_a_builder(self):
        # Codex P2 on PR #97: review bookkeeping is not building.
        head = self._append_verdict(f"model fresh; agent: reviewer-b; context: {REVIEW_CTX}",
                                    trailer=REVIEW_CTX)
        self.assertNotIn(REVIEW_CTX, builders("S-900", repo=self.repo, commit=head)["contexts"])
        [v] = self._status(head)
        self.assertEqual(v["status"], "current", v)
        record("S-900", head, "pass", "none", "model fresh", "reviewer-b", context=REVIEW_CTX,
               repo=self.repo, run_verdict=lambda argv: None)

    def test_a_verdict_commit_that_also_changes_code_is_building(self):
        with Path(self.repo, SPEC_DIR, "SPEC.md").open("a") as f:
            f.write(_verdict_row(self.candidate, f"m; agent: reviewer-b; context: {REVIEW_CTX}"))
        Path(self.repo, "src/thing.py").write_text("v = 3\n")
        head = _commit(self.repo, f"Record S-900 verdict and patch code\n\nAMS-Context: {REVIEW_CTX}")
        self.assertIn(REVIEW_CTX, builders("S-900", repo=self.repo, commit=head)["contexts"])

    def test_supplementary_spec_artifact_changed_after_review_is_stale(self):
        # Codex P2 on PR #97: only digest-covered records are exempt.
        self._append_verdict(f"model fresh; agent: reviewer-b; context: {REVIEW_CTX}")
        Path(self.repo, SPEC_DIR, "diagram.svg").write_text("<svg/>\n")
        head = _commit(self.repo, "Add a Spec diagram after review")
        [v] = self._status(head)
        self.assertEqual(v["status"], "stale", v)
        self.assertIn("diagram.svg", " ".join(v["reasons"]))

    def test_review_recorded_at_a_symbolic_ref_goes_stale_after_a_code_commit(self):
        # Codex P2 on PR #97: `--candidate HEAD` must bind the commit, not the ref.
        def native(argv):
            candidate = argv[argv.index("--candidate") + 1]
            reviewer = argv[argv.index("--reviewer") + 1]
            with Path(self.repo, SPEC_DIR, "SPEC.md").open("a") as f:
                f.write(_verdict_row(candidate, reviewer).replace(self.candidate, candidate))
        record("S-900", "HEAD", "pass", "none", "model fresh", "reviewer-b", context=REVIEW_CTX,
               repo=self.repo, run_verdict=native)
        _commit(self.repo, "Record S-900 review verdict")
        Path(self.repo, "src/thing.py").write_text("v = 4\n")
        head = _commit(self.repo, "Change delivered code after review")
        [v] = self._status(head)
        self.assertRegex(v["candidate"], r"^[0-9a-f]{40}$")
        self.assertEqual(v["status"], "stale", v)

    def test_verdict_by_the_building_session_is_reported_refused(self):
        head = self._append_verdict(f"model; agent: reviewer-b; context: {BUILD_CTX}")
        [v] = self._status(head)
        self.assertEqual(v["status"], "refused", v)

    def test_verdict_naming_no_context_is_unbound(self):
        head = self._append_verdict("Orchestrator C (cloud)")
        [v] = self._status(head)
        self.assertEqual(v["status"], "unbound", v)


if __name__ == "__main__":
    unittest.main()
