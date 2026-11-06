"""Replay TK-001D's synthetic escaped failure with fresh-process recovery.

Run from the project root: uv run python evals/coherence_observation_replay.py
Uses only owned temporary files, local Git and the current Python interpreter.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from ams.coherence.observe import observe, publish


def replay():
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="coherence-observation-") as directory:
        repo = Path(directory).resolve()
        # The observer's subprocesses have no provider/database environment.
        env = {"PATH": os.defpath, "GIT_AUTHOR_NAME": "Synthetic fixture", "GIT_COMMITTER_NAME": "Synthetic fixture",
               "GIT_AUTHOR_EMAIL": "fixture@example.invalid", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
               "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "TMPDIR": str(repo),
               "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")}

        def git(*args):
            return subprocess.check_output(["git", *args], cwd=repo, env=env, text=True).strip()

        def put(path, value):
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value)

        def commit():
            git("add", ".")
            git("commit", "-qm", "synthetic observation fixture")
            return git("rev-parse", "HEAD")

        git("init", "-q", "-b", "main")
        task_path = "workbench/specs/S-003-fixture/tasks/TK-003/TASK.md"
        put(task_path, "# Synthetic website Task\n\n**Task ID:** TK-003\n**Spec ID:** S-003\n**Status:** in-progress\n")
        put("site/page.html", "<main>Sample explanation</main>\n")
        contract = {
            "schema_version": 1, "synthetic": True, "family": "synthetic-page-explanation",
            "failure_id": "synthetic-page-miss", "spec_id": "S-003", "task_id": "TK-003", "phase": "acceptance",
            "probes": [{"id": "sample-explanation", "path": "site/page.html", "contains": "Sample explanation"}],
            "workflow": {"size": "small", "limit": "implement", "source_repository": "ams", "map": None,
                         "plan": None, "allowed_paths": ["site"]}, "skill": None,
        }
        put("evidence/contract.json", json.dumps(contract))
        source = commit()
        put("site/page.html", "<main>Incomplete page</main>\n")
        candidate = commit()
        # Deliberately green while failing the accepted page requirement.
        subprocess.run([sys.executable, "-c", "from pathlib import Path; assert '<main>' in Path('site/page.html').read_text()"],
                       cwd=repo, env=env, check=True)
        reports = repo / "workbench/feedback/coherence"
        first = observe(repo, source, candidate, "evidence/contract.json", "synthetic-page-use-1", "2026-11-06T09:00:00Z")
        assert len(first["findings"]) == 1 and first["findings"][0]["code"] == "acceptance-miss"
        assert publish(first, reports) == "created"
        assert publish(first, reports) == "unchanged"
        second = observe(repo, source, candidate, "evidence/contract.json", "synthetic-page-use-2",
                         "2026-11-06T09:00:01Z", previous=first)
        assert publish(second, reports) == "created"
        command = [sys.executable, "-m", "ams.coherence.observe", "recover", "--reports", str(reports),
                   "--spec", "S-003", "--task", "TK-003"]
        recovered = json.loads(subprocess.check_output(command, cwd=repo, env=env, text=True))
        assert len(recovered) == 2
        assert {r["occurrence_id"] for r in recovered} == {first["occurrence_id"], second["occurrence_id"]}
        assert second["findings"][0]["previous_finding"] == first["findings"][0]["id"]
        assert (repo / task_path).read_text().endswith("**Status:** in-progress\n")
        return {"synthetic": True, "source": source, "candidate": candidate, "component_check": "passed",
                "finding": first["findings"][0]["code"], "replay": "unchanged", "fresh_process_recovered": len(recovered),
                "recurrence_links_original": True, "responsible_owner": first["owner"],
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "limits": "Fixture detection and routing only; no native model use, database write or benefit claim."}


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
