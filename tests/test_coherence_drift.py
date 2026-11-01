"""S-013 TK-001: fixture test for the dev-vs-main drift check.

Builds a throwaway Git repository with known drift and fixed dates, then checks
that the report gives the exact ahead/behind counts, days and threshold result.
"""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from ams.coherence.drift import measure_drift, render_report

NOW = "2026-11-01T00:00:00Z"


def _git(cwd, *args, date=None):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True)


def _commit(cwd, name, date):
    Path(cwd, name).write_text(name)
    _git(cwd, "add", name)
    _git(cwd, "commit", "-q", "-m", name, date=date)


def _fixture():
    """Base 10/01; dev adds 3 commits from 10/10; main adds 1 commit on 10/20."""
    d = tempfile.mkdtemp(prefix="drift-")
    _git(d, "init", "-q", "-b", "main")
    _commit(d, "base", "2026-10-01T00:00:00Z")
    _git(d, "checkout", "-q", "-b", "dev")
    _commit(d, "d1", "2026-10-10T00:00:00Z")
    _commit(d, "d2", "2026-10-12T00:00:00Z")
    _commit(d, "d3", "2026-10-15T00:00:00Z")
    _git(d, "checkout", "-q", "main")
    _commit(d, "m1", "2026-10-20T00:00:00Z")
    return d


def _measure(repo, head="dev", days=14):
    return measure_drift(repo=repo, base="main", head=head, fetch=False, now=NOW,
                         threshold_commits=20, threshold_days=days)


class DriftTest(unittest.TestCase):
    def setUp(self):
        self.repo = _fixture()

    def test_known_ahead_and_behind_counts_and_days(self):
        r = _measure(self.repo)
        self.assertEqual(r["ahead"]["commits"], 3)
        self.assertEqual(r["behind"]["commits"], 1)
        self.assertEqual(r["ahead"]["days"], 22)   # oldest dev-only commit 10/10 -> 11/01
        self.assertEqual(r["behind"]["days"], 12)  # oldest main-only commit 10/20 -> 11/01
        self.assertEqual(r["measured_at"], NOW)
        self.assertRegex(r["base_sha"], r"^[0-9a-f]{40}$")
        self.assertRegex(r["head_sha"], r"^[0-9a-f]{40}$")
        self.assertTrue(r["threshold"]["breached"])
        self.assertEqual(r["threshold"]["reasons"], ["days"])

    def test_no_breach_under_both_thresholds(self):
        r = _measure(self.repo, days=30)
        self.assertFalse(r["threshold"]["breached"])
        self.assertEqual(r["threshold"]["reasons"], [])

    def test_zero_drift_reports_zero_days(self):
        r = _measure(self.repo, head="main")
        self.assertEqual((r["ahead"]["commits"], r["ahead"]["days"]), (0, 0))
        self.assertFalse(r["threshold"]["breached"])

    def test_report_names_time_both_shas_and_counts(self):
        r = _measure(self.repo)
        md = render_report(r)
        for needle in (NOW, r["base_sha"], r["head_sha"], "BREACH"):
            self.assertIn(needle, md)
        self.assertTrue(re.search(r"ahead of `main` \| 3 \| 22", md))


if __name__ == "__main__":
    unittest.main()
