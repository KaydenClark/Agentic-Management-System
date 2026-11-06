"""Escaped acceptance misses, preparation boundaries and native use evidence."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

import pytest

from ams.coherence.observe import Refused, observe, publish, recover


def git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
           "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
    return subprocess.check_output(["git", *args], cwd=repo, env=env, text=True).strip()


def put(repo, path, value):
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value)


def commit(repo):
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "synthetic observation")
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def case(tmp_path):
    git(tmp_path, "init", "-q", "-b", "main")
    spec = "workbench/specs/S-003-website/SPEC.md"
    task = "workbench/specs/S-003-website/tasks/TK-003/TASK.md"
    put(tmp_path, spec, "# Website\n\n**Spec ID:** S-003\n\n## Acceptance Criteria\n\n- [ ] The page explains the sample.\n")
    put(tmp_path, task, "# Website task\n\n**Task ID:** TK-003\n**Spec ID:** S-003\n**Status:** in-progress\n")
    put(tmp_path, "site/page.html", "<main>Sample explanation</main>\n")
    put(tmp_path, "workbench/map.md", "Confirmed website destination.\n")
    put(tmp_path, "workbench/plan.md", "Bounded website Task.\n")
    contract = {
        "schema_version": 1, "synthetic": True, "family": "website-explanation", "failure_id": "FAIL-017",
        "spec_id": "S-003", "task_id": "TK-003", "phase": "acceptance",
        "probes": [{"id": "sample-explanation", "path": "site/page.html", "contains": "Sample explanation"}],
        "workflow": {"size": "small", "limit": "implement", "source_repository": "ams",
                     "map": None, "plan": None, "allowed_paths": ["site", "evidence"]},
        "skill": None,
    }
    put(tmp_path, "evidence/contract.json", json.dumps(contract))
    source = commit(tmp_path)
    return tmp_path, source, contract


def check(case, occurrence="fixture-use-1", previous=None):
    repo, source, _ = case
    return observe(repo, source, git(repo, "rev-parse", "HEAD"), "evidence/contract.json", occurrence,
                   "2026-11-06T09:00:00Z", previous=previous)


def recut(case, contract):
    repo, _, _ = case
    put(repo, "evidence/contract.json", json.dumps(contract))
    return repo, commit(repo), contract


def codes(report):
    return [f["code"] for f in report["findings"]]


def test_green_unit_check_does_not_hide_actual_acceptance_miss(case):
    repo, _, _ = case
    put(repo, "site/page.html", "<main>Incomplete page</main>\n")
    candidate = commit(repo)
    # A green component check is deliberately weaker than the accepted behavior.
    subprocess.run(["python3", "-c", "assert 2 + 2 == 4"], check=True)
    report = check(case)
    assert codes(report) == ["acceptance-miss"]
    finding = report["findings"][0]
    assert finding["owner"] == {"spec_id": "S-003", "task_id": "TK-003"}
    assert finding["observed"] == "required-text-absent"
    assert report["candidate"] == candidate
    assert report["eligible_uses"] == 0


def test_replay_fresh_recovery_and_recurrence_preserve_occurrences(case):
    repo, _, _ = case
    put(repo, "site/page.html", "<main>Incomplete page</main>\n")
    commit(repo)
    first = check(case)
    directory = repo / "workbench/feedback/coherence"
    assert publish(first, directory) == "created"
    assert publish(check(case), directory) == "unchanged"
    assert recover(directory, "S-003", "TK-003") == [first]
    later = check(case, "fixture-use-2", previous=first)
    assert later["previous_occurrence"] == first["occurrence_id"]
    assert later["findings"][0]["previous_finding"] == first["findings"][0]["id"]
    assert publish(later, directory) == "created"
    assert len(recover(directory, "S-003", "TK-003")) == 2
    changed = copy.deepcopy(first)
    changed["candidate"] = "a" * 40
    with pytest.raises(Refused):
        publish(changed, directory)


@pytest.mark.parametrize("source_repository", ["ams", "KaydenClark/skills"])
def test_large_cross_repository_work_requires_frozen_map_and_plan(case, source_repository):
    contract = copy.deepcopy(case[2])
    contract["workflow"].update(size="large", source_repository=source_repository)
    case = recut(case, contract)
    report = check(case)
    assert codes(report) == ["missing-map", "missing-plan"]
    assert all(f["owner"]["spec_id"] == "S-000A" for f in report["findings"])
    assert all(f["failure_id"] == "FAIL-017" for f in report["findings"])


def test_valid_existing_preparation_is_reused_and_small_edit_needs_none(case):
    assert codes(check(case)) == []
    contract = copy.deepcopy(case[2])
    contract["workflow"]["size"] = "large"
    for key in ("map", "plan"):
        path = f"workbench/{key}.md"
        contract["workflow"][key] = {"path": path, "sha256": hashlib.sha256((case[0] / path).read_bytes()).hexdigest()}
    assert codes(check(recut(case, contract))) == []


def test_prepare_stop_and_overbroad_assignment_are_detected(case):
    contract = copy.deepcopy(case[2])
    contract["workflow"].update(limit="prepare", allowed_paths=["workbench", "evidence"])
    case = recut(case, contract)
    put(case[0], "site/page.html", "<main>Sample explanation changed</main>\n")
    commit(case[0])
    assert codes(check(case)) == ["prepare-stop-bypass"]
    contract["workflow"]["limit"] = "implement"
    case = recut(case, contract)
    put(case[0], "outside.txt", "unrequested\n")
    commit(case[0])
    assert codes(check(case)) == ["assignment-scope"]


def native_case(case, intentional=False):
    contract = copy.deepcopy(case[2])
    contract["skill"] = {"accepted_commit": "a" * 40, "expected_commit": "b" * 40 if intentional else "a" * 40,
                         "expected_digest": "c" * 64, "intentional_baseline": intentional,
                         "receipt_path": "evidence/native-use.json"}
    case = recut(case, contract)
    receipt = {"kind": "native-loaded-use", "host": "codex", "use_id": "fixture-native-use-1",
               "source_commit": contract["skill"]["expected_commit"], "installed_digest": "c" * 64,
               "loaded_digest": "c" * 64, "use_observed": True}
    put(case[0], "evidence/native-use.json", json.dumps(receipt))
    commit(case[0])
    return case, receipt


def test_actual_loaded_identity_differs_from_source_merge_and_install(case):
    case, receipt = native_case(case)
    receipt["loaded_digest"] = "d" * 64
    put(case[0], "evidence/native-use.json", json.dumps(receipt))
    commit(case[0])
    r = check(case)
    assert codes(r) == ["stale-loaded-skill"]
    assert r["eligible_uses"] == 0
    assert r["skill_use"]["loaded_digest"] == "d" * 64


def test_intentional_baseline_is_reported_without_upgrade(case):
    case, _ = native_case(case, intentional=True)
    r = check(case)
    assert codes(r) == []
    assert r["skill_use"]["condition"] == "intentional-baseline"
    assert r["skill_use"]["source_commit"] == "b" * 40
    assert r["eligible_uses"] == 1


def test_unknown_loading_is_unknown_not_a_success(case):
    case, receipt = native_case(case)
    receipt["loaded_digest"] = None
    put(case[0], "evidence/native-use.json", json.dumps(receipt))
    commit(case[0])
    r = check(case)
    assert codes(r) == ["unknown-loaded-skill"]
    assert r["eligible_uses"] == 0


def test_expected_red_is_separate_from_escaped_failure(case):
    contract = copy.deepcopy(case[2])
    contract["phase"] = "expected-red"
    case = recut(case, contract)
    put(case[0], "site/page.html", "<main>Incomplete page</main>\n")
    commit(case[0])
    r = check(case)
    assert codes(r) == []
    assert r["expected_red_count"] == 1
    assert r["eligible_uses"] == 0


def test_private_artifact_bytes_never_enter_report_and_extra_fields_refuse(case):
    repo, _, contract = case
    put(repo, "site/page.html", "PRIVATE CANARY /" + "Users/test/.env secret contents\n")
    commit(repo)
    assert "PRIVATE CANARY" not in json.dumps(check(case))
    contract = copy.deepcopy(contract)
    contract["private_prompt"] = "do not export"
    with pytest.raises(Refused):
        check(recut(case, contract))


@pytest.mark.parametrize("path", ["../outside", "/" + "Users/private", ".env", "workbench/sessions/private.md"])
def test_unsafe_probe_paths_refuse(case, path):
    contract = copy.deepcopy(case[2])
    contract["probes"][0]["path"] = path
    with pytest.raises(Refused):
        check(recut(case, contract))


def test_no_unpinned_candidate_and_no_changed_same_occurrence(case):
    with pytest.raises(Refused):
        observe(case[0], case[1], "HEAD", "evidence/contract.json", "fixture-use-1", "2026-11-06T09:00:00Z")
    r = check(case)
    with pytest.raises(Refused):
        check(case, previous=r)


def test_symlink_report_destination_refuses(case, tmp_path):
    destination = case[0] / "linked"
    destination.symlink_to(case[0] / "outside", target_is_directory=True)
    with pytest.raises(Refused):
        publish(check(case), destination)


def test_tampered_candidate_contract_cannot_change_frozen_expectation(case):
    repo, _, original = case
    contract = copy.deepcopy(original)
    contract["probes"][0]["contains"] = "Incomplete"
    put(repo, "evidence/contract.json", json.dumps(contract))
    put(repo, "site/page.html", "Incomplete")
    commit(repo)
    assert codes(check(case)) == ["acceptance-miss"]


def test_publishing_raw_or_unknown_nested_fields_refuses(case):
    r = check(case)
    r["probes"][0]["private_body"] = "private canary"
    with pytest.raises(Refused):
        publish(r, case[0] / "reports")


def test_same_native_use_cannot_be_recounted_by_renaming_occurrence(case):
    case, _ = native_case(case)
    directory = case[0] / "reports"
    first = check(case)
    publish(first, directory)
    with pytest.raises(Refused):
        publish(check(case, "renamed-use", previous=first), directory)


def test_prepare_stop_is_independent_of_eventual_assignment_scope(case):
    contract = copy.deepcopy(case[2])
    contract["workflow"]["limit"] = "prepare"
    case = recut(case, contract)
    put(case[0], "site/page.html", "<main>Sample explanation implemented</main>\n")
    commit(case[0])
    assert codes(check(case)) == ["prepare-stop-bypass"]


def test_unavailable_host_identity_stays_unknown(case):
    case, receipt = native_case(case)
    receipt["host"] = None
    put(case[0], "evidence/native-use.json", json.dumps(receipt))
    commit(case[0])
    r = check(case)
    assert codes(r) == ["unknown-loaded-skill"]
    assert r["skill_use"]["host"] is None
    assert r["eligible_uses"] == 0


def test_copied_report_cannot_duplicate_an_occurrence_on_recovery(case):
    directory = case[0] / "reports"
    publish(check(case), directory)
    original = next(directory.glob("OBS-*.md"))
    (directory / "OBS-copy.md").write_bytes(original.read_bytes())
    with pytest.raises(Refused):
        recover(directory)


def test_malformed_observed_field_refuses_without_typeerror(case):
    put(case[0], "site/page.html", "Incomplete")
    commit(case[0])
    r = check(case)
    r["findings"][0]["observed"] = []
    with pytest.raises(Refused):
        publish(r, case[0] / "reports")


def test_prepare_can_update_records_without_implementation_release(case):
    contract = copy.deepcopy(case[2])
    contract["workflow"].update(limit="prepare", allowed_paths=["site", "workbench"])
    case = recut(case, contract)
    put(case[0], "workbench/wiki/design.md", "Planned behavior, without implementation.\n")
    commit(case[0])
    assert codes(check(case)) == []


def test_recovery_refuses_a_recurrence_with_its_parent_removed(case):
    directory = case[0] / "reports"
    first = check(case)
    publish(first, directory)
    second = check(case, "fixture-use-2", previous=first)
    publish(second, directory)
    original = directory / ("OBS-" + hashlib.sha256(first["occurrence_id"].encode()).hexdigest()[:32] + ".md")
    original.unlink()
    with pytest.raises(Refused):
        recover(directory)


@pytest.mark.parametrize("move", ["outside-to-allowed", "product-to-record", "within-allowed"])
def test_move_checks_both_endpoints(case, move):
    repo, _, contract = case
    contract = copy.deepcopy(contract)
    if move == "outside-to-allowed":
        old, new, expected = "outside.txt", "site/moved.txt", ["assignment-scope"]
    elif move == "product-to-record":
        old, new, expected = "site/product.txt", "workbench/wiki/moved.md", ["prepare-stop-bypass"]
        contract["workflow"].update(limit="prepare", allowed_paths=["site", "workbench"])
    else:
        old, new, expected = "site/old.txt", "site/new.txt", []
    put(repo, old, "Distinct unchanged bytes that Git recognizes as a complete rename.\n")
    case = recut(case, contract)
    (repo / new).parent.mkdir(parents=True, exist_ok=True)
    git(repo, "mv", old, new)
    commit(repo)
    assert codes(check(case)) == expected


# Spawn fresh interpreters, not threads or inherited flock descriptors. The
# first writer pauses after fsync but before link; the contender must finish
# with a controlled refusal while that first writer still owns its operation.
PUBLISH_WORKER = r'''
import json, os, sys
from ams.coherence import observe as o
report = json.loads(sys.stdin.readline())
if sys.argv[2] == 'pause':
    link = o.os.link
    def paused(*args, **kwargs):
        print('ready', flush=True)
        sys.stdin.readline()
        return link(*args, **kwargs)
    o.os.link = paused
try:
    print(o.publish(report, sys.argv[1]), flush=True)
except o.Refused:
    print('refused', flush=True)
    sys.exit(2)
'''


def start_publisher(report, directory, pause=False):
    import sys
    process = subprocess.Popen([sys.executable, "-c", PUBLISH_WORKER, str(directory), "pause" if pause else "run"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.stdin.write(json.dumps(report) + "\n")
    process.stdin.flush()
    return process


def fresh_recover(directory):
    import sys
    result = subprocess.run([sys.executable, "-m", "ams.coherence.observe", "recover", "--reports", str(directory)],
                            capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_competing_processes_preserve_native_use_and_other_owner(case):
    case, _ = native_case(case)
    directory = case[0] / "reports"
    other = check(case, "other-owner")
    other["owner"] = {"spec_id": "S-004", "task_id": "TK-004"}
    other["task_path"] = "workbench/specs/S-004-other/tasks/TK-004/TASK.md"
    other["skill_use"]["use_id"] = "other-native-use"
    assert publish(other, directory) == "created"
    original = {p.name: p.read_bytes() for p in directory.glob("OBS-*.md")}
    first = check(case, "first-contender")
    second = check(case, "second-contender")
    winner = start_publisher(first, directory, pause=True)
    try:
        assert winner.stdout.readline().strip() == "ready"
        loser = start_publisher(second, directory)
        output, error = loser.communicate(timeout=10)
        assert (loser.returncode, output.strip()) == (2, "refused"), error
    finally:
        output, error = winner.communicate("continue\n", timeout=10)
    assert (winner.returncode, output.strip()) == (0, "created"), error
    assert {r["occurrence_id"] for r in fresh_recover(directory)} == {"other-owner", "first-contender"}
    assert publish(first, directory) == "unchanged"
    with pytest.raises(Refused):
        publish(second, directory)
    assert all((directory / name).read_bytes() == raw for name, raw in original.items())


def test_interrupted_publisher_releases_lock_and_retains_temporary(case):
    directory = case[0] / "reports"
    retained = check(case, "retained-owner")
    publish(retained, directory)
    originals = {p.name: p.read_bytes() for p in directory.glob("OBS-*.md")}
    process = start_publisher(check(case, "interrupted"), directory, pause=True)
    try:
        assert process.stdout.readline().strip() == "ready"
        temporary = {p.name: p.read_bytes() for p in directory.glob(".observation-*")}
        assert len(temporary) == 1
        assert fresh_recover(directory) == [retained]
    finally:
        process.kill()
        process.communicate(timeout=10)
    successor = start_publisher(check(case, "successor"), directory)
    output, error = successor.communicate(timeout=10)
    assert (successor.returncode, output.strip()) == (0, "created"), error
    assert {r["occurrence_id"] for r in fresh_recover(directory)} == {"retained-owner", "successor"}
    assert all((directory / name).read_bytes() == raw for name, raw in {**temporary, **originals}.items())


def test_unavailable_directory_lock_refuses_without_publication(case, monkeypatch):
    import fcntl
    def unavailable(*args):
        raise OSError("synthetic unsupported locking")
    monkeypatch.setattr(fcntl, "flock", unavailable)
    directory = case[0] / "reports"
    with pytest.raises(Refused, match="locking unavailable"):
        publish(check(case), directory)
    assert list(directory.iterdir()) == []


def test_corrupted_directory_is_preserved_and_refuses_new_reports(case):
    directory = case[0] / "reports"
    publish(check(case), directory)
    original = next(directory.glob("OBS-*.md"))
    duplicate = directory / "OBS-copy.md"
    duplicate.write_bytes(original.read_bytes())
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    with pytest.raises(Refused):
        publish(check(case, "later"), directory)
    with pytest.raises(Refused):
        recover(directory)
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before
