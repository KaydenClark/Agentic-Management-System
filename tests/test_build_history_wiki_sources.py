"""Wiki relocation must preserve provable history, never waive comparison."""
import copy
import json

import pytest

from ams import build_history as bh
from test_build_history import _git, _write, git_runner, StubSupabase, URL, FAKE_PUBLISHABLE

PATHS = {sid: f"workbench/specs/{sid}-demo/SPEC.md" for sid in ("S-003", "S-007")}
PAGE = "workbench/wiki/context-website.md"


def lifecycle(args):
    specs = [{"id": sid, "path": path, "title": sid, "status": "active"}
             for sid, path in PATHS.items()]
    if args[0] == "list":
        return json.dumps({"specs": specs})
    return json.dumps({**next(s for s in specs if s["id"] == args[1]), "tasks": []})


def commit(repo, message, when="2026-11-01T11:00:00Z"):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message, when=when)
    return _git(repo, "rev-parse", "HEAD")


def page(sha):
    return "---\nsource_paths:\n" + "".join(f"  - {p}\n" for p in PATHS.values()) + \
        "---\n\n# Historical implementation reports and limits\n\n" + "\n".join(
            f"[previous {sid} at {sha[:7]}]({bh.REPO_URL}/blob/{sha[:7]}/{path})"
            for sid, path in PATHS.items())


@pytest.fixture
def relocated(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-qb", "main")
    for sid, count in (("S-003", 6), ("S-007", 2)):
        _write(repo, PATHS[sid], f"# {sid}\n\n**Spec ID:** {sid}\n\n" + bh.EVIDENCE_HEADING +
               "\n\n| Date | Task | Event | Verification |\n|---|---|---|---|\n" +
               "".join(f"| 2026-11-01 | none | Real event {n} | check {n} |\n"
                       for n in range(count)))
    archive = commit(repo, "Original reports", "2026-11-01T10:00:00Z")
    original = bh.record_rows(git_runner(repo), lifecycle)
    for sid, path in PATHS.items():
        _write(repo, path, f"# {sid}\n\n**Spec ID:** {sid}\n\nCurrent destination; history is in the Wiki.\n")
    _write(repo, "workbench/wiki/MEMORY.md", "# Router\n\n[Website](context-website.md)\n")
    _write(repo, PAGE, page(archive))
    commit(repo, "Move history to the Wiki")
    return repo, archive, original


def test_relocated_eight_events_are_derived_with_exact_original_fields(relocated, capsys):
    repo, _, original = relocated
    current = bh.record_rows(git_runner(repo), lifecycle)
    retained = [r for r in current if "#evidence-" in r["source_ref"]]
    assert len(retained) == 8
    assert retained == [r for r in original if "#evidence-" in r["source_ref"]]
    assert bh.readcheck(current, URL, FAKE_PUBLISHABLE, StubSupabase(original)) == 0
    assert "extra: 0" in capsys.readouterr().out


@pytest.mark.parametrize("mutation", ["missing", "tampered", "unprovable"])
def test_relocation_does_not_hide_bad_database_rows(relocated, mutation, capsys):
    repo, _, original = relocated
    actual = copy.deepcopy(original)
    if mutation == "missing":
        actual.pop()
    elif mutation == "tampered":
        actual[-1]["source_url"] = bh.REPO_URL + "/blob/" + "f" * 40 + "/fake.md"
    else:
        planted = copy.deepcopy(actual[-1])
        planted["source_ref"] += "-unprovable"
        actual.append(planted)
    assert bh.readcheck(bh.record_rows(git_runner(repo), lifecycle), URL,
                        FAKE_PUBLISHABLE, StubSupabase(actual)) == 1
    assert ("missing: 1" if mutation == "missing" else
            "content mismatches: 1" if mutation == "tampered" else "extra: 1") in capsys.readouterr().out


@pytest.mark.parametrize("change", ["external", "symbolic", "query", "fragment", "path", "label", "source_paths"])
def test_unsupported_declarations_refuse_without_external_operations(relocated, change):
    repo, archive, _ = relocated
    text = page(archive)
    if change == "external":
        text = text.replace(bh.REPO_URL, "https://external.invalid/repo")
    elif change == "symbolic":
        text = text.replace(f"/blob/{archive[:7]}/", "/blob/main/")
    elif change in ("query", "fragment"):
        text = text.replace("SPEC.md)", "SPEC.md" + ("?token=not-a-credential" if change == "query" else "#L1") + ")")
    elif change == "path":
        text = text.replace("/blob/" + archive[:7] + "/workbench", "/blob/" + archive[:7] + "/../workbench")
    elif change == "label":
        text = text.replace("previous S-003", "previous S-999")
    else:
        text = text.replace("source_paths:", "unrelated_paths:")
    _write(repo, PAGE, text)
    commit(repo, "Unsupported declaration")
    calls = []
    real_git = git_runner(repo)
    def local_git(args):
        calls.append(args)
        assert not any(a in ("fetch", "remote", "push", "clone") for a in args)
        return real_git(args)
    with pytest.raises(bh.RefusedError, match="unsupported historical"):
        bh.record_rows(local_git, lifecycle)
    archive_commands = [c for c in calls if c[0] == "--no-replace-objects"]
    assert archive_commands and all("--no-lazy-fetch" in c for c in archive_commands)


@pytest.mark.parametrize("hidden", ["orphan", "comment", "fence", "inline", "router-code"])
def test_orphan_or_nonvisible_declarations_cannot_authorize_retained_rows(relocated, hidden, capsys):
    repo, archive, original = relocated
    text = page(archive)
    if hidden == "orphan":
        _write(repo, "workbench/wiki/MEMORY.md", "# No route\n")
    elif hidden == "router-code":
        _write(repo, "workbench/wiki/MEMORY.md", "`[Website](context-website.md)`\n")
    else:
        wrapped = {"comment": "<!--\n{}\n-->", "fence": "```markdown\n{}\n```", "inline": "`{}`"}[hidden]
        if hidden == "inline":
            text = "\n".join(wrapped.format(line) for line in text.splitlines())
        else:
            text = wrapped.format(text)
        _write(repo, PAGE, text)
    commit(repo, "Not an active source route")
    assert bh.readcheck(bh.record_rows(git_runner(repo), lifecycle), URL,
                        FAKE_PUBLISHABLE, StubSupabase(original)) == 1
    assert "extra: 8" in capsys.readouterr().out


def test_repeated_identical_routes_do_not_duplicate_events(relocated):
    repo, archive, _ = relocated
    _write(repo, PAGE, page(archive) + "\n" + page(archive).split("# Historical")[1])
    commit(repo, "Repeated source links")
    rows = bh.record_rows(git_runner(repo), lifecycle)
    assert len([r for r in rows if "#evidence-" in r["source_ref"]]) == 8


def test_conflicting_current_event_cannot_override_declared_history(relocated):
    repo, archive, _ = relocated
    old = _git(repo, "show", f"{archive}:{PATHS['S-003']}")
    _write(repo, PATHS["S-003"], old.replace("Real event 0", "Different event 0"))
    commit(repo, "Conflicting event key")
    with pytest.raises(bh.RefusedError, match="conflicting historical Spec event"):
        bh.record_rows(git_runner(repo), lifecycle)


@pytest.mark.parametrize("source", ["future", "orphan", "unavailable", "identity", "no-table"])
def test_archive_must_be_available_ancestor_with_expected_identity_and_past_time(relocated, source):
    repo, archive, _ = relocated
    if source == "unavailable":
        invalid = "f" * 40
    else:
        if source == "orphan":
            _git(repo, "switch", "-q", "--orphan", "unrelated")
        else:
            _git(repo, "switch", "-q", "-c", "alternate", archive)
        old = _git(repo, "show", f"{archive}:{PATHS['S-003']}")
        if source == "identity":
            old = old.replace("**Spec ID:** S-003", "**Spec ID:** S-999")
        elif source == "no-table":
            old = old.split(bh.EVIDENCE_HEADING)[0]
        _write(repo, PATHS["S-003"], old + "\nAlternate source\n")
        invalid = commit(repo, "Alternate archive", "2026-11-03T00:00:00Z" if source == "future" else "2026-11-01T10:30:00Z")
        _git(repo, "switch", "-q", "main")
        if source != "orphan":
            _git(repo, "merge", "-q", "-s", "ours", "alternate", "-m", "Known ancestor without changing destination", when="2026-11-01T11:30:00Z")
    text = page(archive).replace(f"previous S-003 at {archive[:7]}", f"previous S-003 at {invalid[:7]}")
    text = text.replace(f"/blob/{archive[:7]}/{PATHS['S-003']}", f"/blob/{invalid[:7]}/{PATHS['S-003']}")
    _write(repo, PAGE, text)
    commit(repo, "Declare invalid archive", "2026-11-01T12:00:00Z")
    with pytest.raises(bh.RefusedError, match="future|non-ancestor|unavailable|identity differs|no evidence"):
        bh.record_rows(git_runner(repo), lifecycle)
