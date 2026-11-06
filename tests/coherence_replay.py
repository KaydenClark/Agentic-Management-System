"""Replay the current checker and its frozen predecessor on one fixture.

Run from the repository root: uv run python tests/coherence_replay.py
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = "408e851e5ec621bd00f32e9a382df8d9a06b505e"
ROOT = Path(__file__).resolve().parents[1]
MODULE = "src/ams/coherence/up_to_spec.py"
ENV = {**os.environ, "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
       "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
       "GIT_AUTHOR_DATE": "2020-01-01T00:00:00+0000", "GIT_COMMITTER_DATE": "2020-01-01T00:00:00+0000",
       "GIT_CONFIG_NOSYSTEM": "1"}


def git(repo, *args):
    return subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=repo, env=ENV,
                          check=True, capture_output=True, text=True).stdout.strip()


def run(module, repo, commit):
    result = subprocess.run([sys.executable, str(module), "S-900", "--repo", str(repo),
                             "--commit", commit, "--json"], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix="coherence-replay-") as temp:
        repo = Path(temp) / "fixture"
        repo.mkdir()
        git(repo, "init", "-q", "-b", "main")
        (repo / "README.md").write_text("Fixture document.\n")
        (repo / "other.txt").write_text("Second fixture document.\n")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "documents")
        ancestor = git(repo, "rev-parse", "HEAD")
        git(repo, "checkout", "-q", "-b", "side")
        (repo / "side.txt").write_text("Side branch.\n")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "side")
        side = git(repo, "rev-parse", "HEAD")
        git(repo, "checkout", "-q", "main")
        spec = repo / "workbench/specs/S-900-fixture/SPEC.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(f"""# S-900 - Fixture

## Acceptance Criteria

- [x] **Alpha.** Behavior A. *Evidence:* `README.md`.
- [x] **Beta.** Behavior B. *Evidence:* `{ancestor}`.
- [x] **Gamma.** Behavior C. *Evidence:* `{side}`.
- [x] **Delta.** Behavior D. *Evidence:* `missing.txt`.
- [ ] **Epsilon.** Behavior E. *Evidence:* `other.txt`.
- [x] **Zeta.** Behavior F. *Evidence:* `other.txt`.
""")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "spec")
        fixture = git(repo, "rev-parse", "HEAD")
        old = Path(temp) / "old.py"
        old.write_text(subprocess.run(["git", "show", f"{BASE}:{MODULE}"], cwd=ROOT,
                                      check=True, capture_output=True, text=True).stdout)
        candidate = ROOT / MODULE
        before, after = run(old, repo, fixture), run(candidate, repo, fixture)
        rows = lambda report: {c["name"]: {"status": c["status"], "evidence": c["evidence"]}
                               for c in report["criteria"]}
        old_rows, new_rows = rows(before), rows(after)
        for name in ("Alpha", "Beta", "Zeta"):
            assert old_rows[name]["status"] == "met" and new_rows[name]["status"] == "unknown"
            assert old_rows[name]["evidence"] == new_rows[name]["evidence"] and new_rows[name]["evidence"]
        for name in ("Gamma", "Delta"):
            assert old_rows[name] == new_rows[name] == {"status": "unknown", "evidence": []}
        assert old_rows["Epsilon"] == new_rows["Epsilon"] == {"status": "not met", "evidence": []}
        digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        print(json.dumps({"fixture_commit": fixture, "ancestor_commit": ancestor, "side_commit": side,
                          "baseline_commit": BASE, "baseline_module_sha256": digest(old),
                          "candidate_commit": git(ROOT, "rev-parse", "HEAD"),
                          "candidate_module_sha256": digest(candidate),
                          "before": old_rows, "after": new_rows}, indent=2))


if __name__ == "__main__":
    main()
