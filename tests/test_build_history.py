"""Tests for the build-history importer (S-006 TK-004).

A fixture Git repository holds a Spec, a Task, a wiki note and a merged PR
branch; `gh` and the lifecycle tool are stubbed with JSON shaped like their
real output, and Supabase is a stub that applies the unique key the way
PostgREST's ``resolution=ignore-duplicates`` does. No test reaches GitHub or
Supabase.
"""

import json
import os
import random
import re
import string
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from ams import build_history as bh
from ams import writer

URL = "https://example-project.supabase.co"
_rng = random.Random(20261104)
_ALPHA = string.ascii_letters + string.digits
FAKE_SECRET = "sb_secret_" + "".join(_rng.choice(_ALPHA) for _ in range(40))
FAKE_PUBLISHABLE = "sb_publishable_" + "".join(_rng.choice(_ALPHA) for _ in range(30))
ENV = {"SUPABASE_URL": URL, "SUPABASE_SERVICE_ROLE_KEY": FAKE_SECRET,
       "SUPABASE_PUBLISHABLE_KEY": FAKE_PUBLISHABLE}

SPEC_PATH = "workbench/specs/S-001-demo/SPEC.md"
TASK_PATH = "workbench/specs/S-001-demo/tasks/TK-001/TASK.md"
WIKI_PATH = "workbench/wiki/context-demo.md"

SPEC_V1 = """# S-001 - Demo

**Spec ID:** S-001
**Status:** active

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-002 | Planned only in the table | ready | none | pending |

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA
"""

SPEC_V2 = SPEC_V1.replace("**Status:** active\n", "**Status:** active\n**Updated:** 2026-11-01\n").replace(
    "| Every criterion |\n",
    "| Every criterion |\n"
    "| 2026-11-01 | TK-001 | Task closed | PR #1 merged | RUNBOOK | none |\n"
    "| 2026-11-01 | TK-001 | Correction: check moved to `src/` | pytest | this Spec | none |\n",
)

TASK_V1 = """# TK-001 - Demo task

**Task ID:** TK-001
**Status:** ready

## Acceptance

- [ ] Something.
"""

TASK_V2 = TASK_V1.replace("ready", "in-progress") + "\n**Current claimant:** demo-agent\n"
TASK_V3 = TASK_V2.replace("in-progress", "done") + """
## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/demo | {head} | ahead 0 behind 0 | 0 | pytest 3 passed | RUNBOOK | none | abc123 |
"""

WIKI = """# Demo context

## 2026-10-31: Owner clarification

Kind: intent / correction. State: confirmed by the owner.

<!-- jot-entry -->
### JOT-11111111-2222-3333-4444-555555555555
Kind: correction
State: confirmed
Recorded: 2026-11-01T10:55:00.000Z
Author: Kayden
Source: Owner chat, 2026-11-01
Topic: demo
Supersedes: none

The board shows committed cards only.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-99999999-2222-3333-4444-555555555555
Kind: intent
State: confirmed
Recorded: 2026-11-01T10:56:00.000Z
Author: Kayden
Source: Owner chat, 2026-11-01
Topic: demo
Supersedes: none

Not a correction.
<!-- /jot-entry -->
"""


def _git(repo, *args, when=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True, env=env).stdout.strip()


def _write(repo, path, text):
    target = Path(repo, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


@pytest.fixture(scope="module")
def fixture_repo(tmp_path_factory):
    repo = tmp_path_factory.mktemp("history-repo")
    _git(repo, "init", "-q", "-b", "main")
    _write(repo, SPEC_PATH, SPEC_V1)
    _write(repo, TASK_PATH, TASK_V1)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "Map S-001 with TK-001", when="2026-11-01T10:00:00Z")
    _write(repo, TASK_PATH, TASK_V2)
    _git(repo, "commit", "-q", "-am", "Claim S-001 TK-001", when="2026-11-01T10:10:00Z")
    _git(repo, "switch", "-q", "-c", "feat/demo")
    _write(repo, "src/thing.py", "x = 1\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "Add thing", when="2026-11-01T10:20:00Z")
    _write(repo, "src/thing.py", "x = 2\n")
    _git(repo, "commit", "-q", "-am", "Fix the review finding", when="2026-11-01T10:30:00Z")
    fix = _git(repo, "rev-parse", "HEAD")
    _git(repo, "switch", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "feat/demo", "-m",
         "Merge pull request #1 from owner/feat/demo\n\nAdd thing", when="2026-11-01T10:40:00Z")
    merge = _git(repo, "rev-parse", "HEAD")
    _write(repo, SPEC_PATH, SPEC_V2)
    _write(repo, TASK_PATH, TASK_V3.format(head=fix))
    _write(repo, WIKI_PATH, WIKI)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "Close S-001 TK-001", when="2026-11-01T10:50:00Z")
    _git(repo, "branch", "dev", "main~1")
    _git(repo, "switch", "-q", "dev")
    _write(repo, "site/page.txt", "dev only\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "Dev-only page", when="2026-11-01T10:45:00Z")
    _git(repo, "switch", "-q", "main")
    shas = {name: _git(repo, "rev-parse", ref) for name, ref in
            [("map", "main~3"), ("claim", "main~2"), ("add", "feat/demo~1"),
             ("close", "main"), ("dev", "dev")]}
    shas.update(fix=fix, merge=merge)
    return repo, shas


def git_runner(repo):
    def git(args):
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                              text=True).stdout
    return git


def lifecycle_stub(args):
    if list(args[:2]) == ["list", "--all"]:
        return json.dumps({"total": 1, "specs": [
            {"id": "S-001", "title": "Demo", "status": "active", "lifecycle": "current",
             "path": SPEC_PATH, "landmarkId": None}]})
    if args[0] == "show" and args[1] == "S-001":
        return json.dumps({"id": "S-001", "title": "Demo", "status": "active", "path": SPEC_PATH,
                           "tasks": [{"id": "TK-001", "slice": "Demo task", "status": "done",
                                      "blockers": "none", "proof": "PR #1"},
                                     {"id": "TK-002", "slice": "Planned only in the table",
                                      "status": "ready", "blockers": "none", "proof": "pending"}],
                           "retiredTasks": []})
    raise AssertionError(f"unexpected lifecycle call {args}")


def gh_stub(shas):
    repo_url = writer.REPO_URL
    prs = [
        {"number": 1, "title": "Add thing", "state": "MERGED", "url": f"{repo_url}/pull/1",
         "createdAt": "2026-11-01T10:15:00Z", "closedAt": "2026-11-01T10:40:01Z",
         "mergedAt": "2026-11-01T10:40:01Z", "mergeCommit": {"oid": shas["merge"]},
         "headRefName": "feat/demo", "baseRefName": "main",
         "commits": [{"oid": shas["add"], "committedDate": "2026-11-01T10:20:00Z"},
                     {"oid": shas["fix"], "committedDate": "2026-11-01T10:30:00Z"}],
         "reviews": [{"id": "PRR_1", "author": {"login": "reviewer"}, "state": "CHANGES_REQUESTED",
                      "submittedAt": "2026-11-01T10:24:00Z", "body": "Please fix the loader."},
                     {"id": "PRR_2", "author": {"login": "chatgpt-codex-connector"},
                      "state": "COMMENTED", "submittedAt": "2026-11-01T10:25:00Z", "body": "Codex Review"}]},
        {"number": 2, "title": "Abandoned idea", "state": "CLOSED", "url": f"{repo_url}/pull/2",
         "createdAt": "2026-11-01T10:16:00Z", "closedAt": "2026-11-01T10:35:00Z",
         "mergedAt": None, "mergeCommit": None, "headRefName": "feat/idea", "baseRefName": "main",
         "commits": [], "reviews": []},
    ]
    comments = [
        {"id": 100, "in_reply_to_id": None, "user": {"login": "chatgpt-codex-connector[bot]"},
         "created_at": "2026-11-01T10:25:00Z", "path": "src/thing.py",
         "html_url": f"{repo_url}/pull/1#discussion_r100",
         "pull_request_url": "https://api.github.com/repos/o/r/pulls/1",
         "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow)</sub></sub>  "
                 "Load cards from committed records only**\n\nDetails here."},
        {"id": 101, "in_reply_to_id": 100, "user": {"login": "owner"},
         "created_at": "2026-11-01T10:32:00Z", "path": "src/thing.py",
         "html_url": f"{repo_url}/pull/1#discussion_r101",
         "pull_request_url": "https://api.github.com/repos/o/r/pulls/1",
         "body": "Fixed in deadbee: cards are read from HEAD."},
        {"id": 103, "in_reply_to_id": 100, "user": {"login": "owner"},
         "created_at": "2026-11-01T10:33:00Z", "path": "src/thing.py",
         "html_url": f"{repo_url}/pull/1#discussion_r103",
         "pull_request_url": "https://api.github.com/repos/o/r/pulls/1",
         "body": f"Correction: the fix commit is {shas['fix'][:7]}, not deadbee.\n\n---\nfooter"},
        {"id": 102, "in_reply_to_id": None, "user": {"login": "owner"},
         "created_at": "2026-11-01T10:26:00Z", "path": "src/thing.py",
         "html_url": f"{repo_url}/pull/1#discussion_r102",
         "pull_request_url": "https://api.github.com/repos/o/r/pulls/1",
         "body": "A human note, not a finding."},
    ]
    threads = {"data": {"repository": {"pullRequests": {
        "pageInfo": {"hasNextPage": False},
        "nodes": [{"number": 1, "reviewThreads": {"nodes": [
            {"isResolved": True, "comments": {"nodes": [{"databaseId": 100}]}},
            {"isResolved": False, "comments": {"nodes": [{"databaseId": 102}]}}]}},
                  {"number": 2, "reviewThreads": {"nodes": []}}]}}}}
    calls = []

    def gh(args):
        calls.append(list(args))
        if args[:2] == ["pr", "list"]:
            assert "commits" not in args[args.index("--json") + 1]  # too costly for GraphQL
            return json.dumps([{k: v for k, v in pr.items() if k != "commits"} for pr in prs])
        if args[0] == "api" and re.search(r"/pulls/\d+/commits", " ".join(args)):
            number = int(re.search(r"/pulls/(\d+)/commits", " ".join(args)).group(1))
            pr = next(p for p in prs if p["number"] == number)
            return "".join(json.dumps(c) + "\n" for c in pr["commits"])
        if args[:2] == ["api", "graphql"]:
            return json.dumps(threads)
        if args[0] == "api" and "pulls/comments" in " ".join(args):
            return "\n".join(json.dumps(c) for c in comments) + "\n"
        raise AssertionError(f"unexpected gh call {args}")

    gh.calls = calls
    return gh


@pytest.fixture(scope="module")
def rows(fixture_repo):
    repo, shas = fixture_repo
    sources = bh.Sources(git=git_runner(repo), gh=gh_stub(shas), lifecycle=lifecycle_stub,
                         refs=("main", "dev"))
    return bh.collect(sources)


def by_kind(rows, kind):
    return [r for r in rows if r["kind"] == kind]


# --- what the records yield --------------------------------------------------


def test_counts_match_the_records(rows, fixture_repo):
    _, shas = fixture_repo
    counts = {}
    for row in rows:
        counts[row["kind"]] = counts.get(row["kind"], 0) + 1
    assert counts == {
        "commit": 7,        # 6 on main (5 + the merge) and 1 dev-only
        "merge": 1,         # PR #1
        "pr_opened": 2,     # PRs #1 and #2
        "return": 2,        # PR #2 closed unmerged; PR #1 changes requested
        "correction": 5,    # Codex finding, its corrected reply, evidence-log correction, two wiki
        "correction_fix": 1,
        "spec": 1,
        "task": 2,         # a TASK.md and a Spec-table-only Task
        "spec_event": 2,    # Mapped, Task closed
        "task_receipt": 1,
        "task_claimed": 1,
    }


def test_every_row_names_its_source_and_strength(rows):
    for row in rows:
        bh.validate(row)  # raises on a row without a source
        assert row["strength"] == "recorded_fact"
        assert row["is_test"] is False
        assert row["source_ref"].strip()
        assert row["source_url"].startswith("https://")


def test_rows_are_in_the_order_events_occurred(rows):
    times = [bh.parse_time(r["occurred_at"]) for r in rows]
    assert times == sorted(times)
    order = [(r["kind"], r["source_ref"]) for r in rows]
    finding = next(i for i, r in enumerate(rows) if r["kind"] == "correction" and r["source_kind"] == "pr")
    fix = next(i for i, r in enumerate(rows) if r["kind"] == "correction_fix")
    merge = next(i for i, r in enumerate(rows) if r["kind"] == "merge")
    assert finding < fix < merge, order


def test_merge_row_is_the_writer_row(rows, fixture_repo):
    repo, shas = fixture_repo
    (merge,) = by_kind(rows, "merge")
    assert merge == writer.merge_event(shas["merge"], git=git_runner(repo))
    assert merge["detail"]["pr"] == 1


def test_commit_rows_name_their_sha_branch_and_pr(rows, fixture_repo):
    _, shas = fixture_repo
    commits = {r["source_ref"]: r for r in by_kind(rows, "commit")}
    assert set(commits) == {shas[k] for k in ("map", "claim", "add", "fix", "merge", "close", "dev")}
    fix = commits[shas["fix"]]
    assert fix["source_kind"] == "commit"
    assert fix["source_url"] == f"{writer.REPO_URL}/commit/{shas['fix']}"
    assert fix["summary"] == "Fix the review finding"
    assert fix["detail"]["prs"] == [1]
    assert fix["detail"]["refs"] == ["dev", "main"]
    assert commits[shas["close"]]["detail"]["refs"] == ["main"]
    assert commits[shas["dev"]]["detail"]["refs"] == ["dev"]
    assert commits[shas["map"]]["occurred_at"] == "2026-11-01T10:00:00Z"


def test_codex_finding_and_its_fix_are_corrections(rows, fixture_repo):
    _, shas = fixture_repo
    finding = next(r for r in rows if r["kind"] == "correction" and r["source_kind"] == "pr")
    assert finding["source_ref"] == "#1 comment 100"
    assert finding["source_url"].endswith("#discussion_r100")
    assert finding["summary"] == "Load cards from committed records only"
    assert finding["detail"]["priority"] == "P2"
    assert finding["detail"]["resolved"] is True
    assert finding["detail"]["fix_commit"] == shas["fix"]  # the corrected reply wins
    assert finding["detail"]["fix_reply_url"].endswith("#discussion_r103")
    assert finding["detail"]["fix_named_earlier"] == ["deadbee"]
    reply = next(r for r in rows if r["source_ref"] == "#1 comment 103")
    assert reply["kind"] == "correction"
    assert reply["summary"] == f"Correction: the fix commit is {shas['fix'][:7]}, not deadbee."
    (fix,) = by_kind(rows, "correction_fix")
    assert fix["source_kind"] == "commit" and fix["source_ref"] == shas["fix"]
    assert fix["occurred_at"] == "2026-11-01T10:30:00Z"
    assert fix["detail"]["findings"] == ["#1 comment 100"]
    # A human comment that is not a bot finding is not a correction.
    assert not any("comment 102" in r["source_ref"] for r in rows)


def test_returns_are_rows(rows):
    returns = {r["source_ref"]: r for r in by_kind(rows, "return")}
    assert set(returns) == {"#2", "#1 review PRR_1"}
    assert returns["#2"]["occurred_at"] == "2026-11-01T10:35:00Z"
    assert returns["#2"]["detail"]["reason"] == "closed unmerged"
    assert returns["#1 review PRR_1"]["detail"]["reason"] == "changes requested"


def test_spec_and_task_records(rows, fixture_repo):
    _, shas = fixture_repo
    (spec,) = by_kind(rows, "spec")
    assert spec["source_kind"] == "path" and spec["source_ref"] == SPEC_PATH
    assert spec["subject"] == "S-001" and spec["occurred_at"] == "2026-11-01T10:00:00Z"
    tasks = {r["subject"]: r for r in by_kind(rows, "task")}
    task = tasks["S-001 TK-001"]
    assert task["source_ref"] == "S-001/TK-001"  # one identity whichever record holds it
    assert task["detail"]["record"] == TASK_PATH
    assert task["source_url"].startswith(f"{writer.REPO_URL}/blob/{shas['map']}/{TASK_PATH}")
    assert task["detail"]["status"] == "done"
    planned = tasks["S-001 TK-002"]
    assert planned["source_ref"] == "S-001/TK-002"
    assert planned["detail"]["record"] == SPEC_PATH
    assert planned["occurred_at"] == "2026-11-01T10:00:00Z"
    assert planned["source_url"].startswith(f"{writer.REPO_URL}/blob/{shas['map']}/{SPEC_PATH}#L")
    (claimed,) = by_kind(rows, "task_claimed")
    assert claimed["source_ref"] == shas["claim"] and claimed["subject"] == "S-001 TK-001"
    events = {r["source_ref"]: r for r in by_kind(rows, "spec_event")}
    assert set(events) == {SPEC_PATH + "#evidence-1", SPEC_PATH + "#evidence-2"}
    closed = events[SPEC_PATH + "#evidence-2"]
    assert closed["summary"] == "Task closed" and closed["subject"] == "S-001 TK-001"
    assert closed["occurred_at"] == "2026-11-01T10:50:00Z"  # the commit that recorded it
    assert closed["source_url"].startswith(f"{writer.REPO_URL}/blob/{shas['close']}/{SPEC_PATH}#L")
    correction = next(r for r in rows if r["source_ref"] == SPEC_PATH + "#evidence-3")
    assert correction["kind"] == "correction"
    (receipt,) = by_kind(rows, "task_receipt")
    assert receipt["source_ref"] == TASK_PATH + "#receipt-1"
    assert receipt["detail"]["head_sha"] == shas["fix"]


def test_jot_correction_is_a_row_and_other_jots_are_not(rows):
    jots = [r for r in rows if r["source_kind"] == "jot"]
    assert [r["source_ref"] for r in jots] == ["JOT-11111111-2222-3333-4444-555555555555"]
    assert jots[0]["kind"] == "correction"
    assert jots[0]["occurred_at"] == "2026-11-01T10:55:00Z"
    assert jots[0]["source_url"].startswith(f"{writer.REPO_URL}/blob/")
    noted = next(r for r in rows if r["source_ref"] == WIKI_PATH + "#2026-10-31-owner-clarification")
    assert noted["kind"] == "correction" and noted["source_kind"] == "path"
    assert noted["occurred_at"] == "2026-11-01T10:50:00Z"  # when this repository recorded it


def test_collect_is_deterministic(fixture_repo, rows):
    repo, shas = fixture_repo
    again = bh.collect(bh.Sources(git=git_runner(repo), gh=gh_stub(shas),
                                  lifecycle=lifecycle_stub, refs=("main", "dev")))
    assert again == rows


def test_dirty_records_are_refused(tmp_path, fixture_repo):
    repo, shas = fixture_repo
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(repo), str(clone)], check=True)
    Path(clone, SPEC_PATH).write_text("edited but not committed\n")
    with pytest.raises(bh.RefusedError, match="uncommitted"):
        bh.collect(bh.Sources(git=git_runner(clone), gh=gh_stub(shas),
                              lifecycle=lifecycle_stub, refs=("main",)))


# --- validation --------------------------------------------------------------


GOOD = {"kind": "commit", "subject": "abc1234", "summary": "x", "occurred_at": "2026-11-01T10:00:00Z",
        "source_kind": "commit", "source_ref": "a" * 40, "source_url": "https://github.com/x",
        "strength": "recorded_fact", "is_test": False, "detail": {}}


@pytest.mark.parametrize("change", [{"source_ref": ""}, {"source_ref": "  "}, {"source_kind": None},
                                    {"source_kind": "chat"}, {"source_url": None},
                                    {"source_url": "http://x"}, {"strength": "anecdote"},
                                    {"occurred_at": "yesterday"}, {"kind": "Bad Kind"},
                                    {"summary": ""}])
def test_a_row_without_a_proper_source_is_refused(change):
    with pytest.raises(ValueError):
        bh.validate(dict(GOOD, **change))


def test_import_sends_nothing_when_any_row_lacks_a_source(capsys):
    store = StubSupabase()
    code = bh.import_rows([GOOD, dict(GOOD, source_ref="")], _settings(), store)
    assert code == 1
    assert store.calls == []
    assert "refused" in capsys.readouterr().out


# --- writing and reading back ------------------------------------------------


class StubSupabase:
    """build_events with its unique key; honours on_conflict + ignore-duplicates."""

    def __init__(self, rows=()):
        self.rows = [dict(r, id=i + 1) for i, r in enumerate(rows)]
        self.calls = []

    def key(self, row):
        return (row["kind"], row["source_kind"], row["source_ref"])

    def __call__(self, method, url, headers, body):
        self.calls.append((method, url, dict(headers), body))
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if method == "POST":
            assert headers["apikey"] == FAKE_SECRET
            assert query["on_conflict"] == ["kind,source_kind,source_ref"]
            assert "resolution=ignore-duplicates" in headers["Prefer"]
            existing = {self.key(r) for r in self.rows}
            inserted = []
            for row in json.loads(body):
                if self.key(row) in existing:
                    continue
                saved = dict(row, id=len(self.rows) + 1)
                self.rows.append(saved)
                existing.add(self.key(row))
                inserted.append(saved)
            return 201, json.dumps(inserted).encode()
        if method == "PATCH":
            assert headers["apikey"] == FAKE_SECRET
            target = int(query["id"][0].removeprefix("eq."))
            row = next(r for r in self.rows if r["id"] == target)
            for field, (value,) in query.items():
                if field != "id" and str(row.get(field)) != value.removeprefix("eq."):
                    return 200, b"[]"  # the conditional update matched no row
            row.update(json.loads(body))
            return 200, json.dumps([row]).encode()
        if method == "GET":
            assert headers["apikey"] in (FAKE_PUBLISHABLE, FAKE_SECRET)
            visible = [r for r in self.rows if not r.get("is_test")]
            visible.sort(key=lambda r: (bh.parse_time(r["occurred_at"]), r["id"]))
            offset = int(query.get("offset", ["0"])[0])
            limit = int(query.get("limit", ["1000"])[0])
            cols = query["select"][0].split(",")
            page = [{c: r.get(c) for c in cols} for r in visible[offset:offset + limit]]
            return 200, json.dumps(page).encode()
        return 405, b""


def _settings(key=FAKE_SECRET):
    from ams import keycheck
    return keycheck.Settings(url=URL, key=key)


def test_import_twice_adds_no_rows(rows, capsys):
    store = StubSupabase()
    assert bh.import_rows(rows, _settings(), store) == 0
    first = capsys.readouterr().out
    assert len(store.rows) == len(rows)
    assert f"inserted: {len(rows)}" in first
    assert bh.import_rows(rows, _settings(), store) == 0
    second = capsys.readouterr().out
    assert len(store.rows) == len(rows)
    assert "inserted: 0" in second and f"already recorded: {len(rows)}" in second
    for out in (first, second):
        assert FAKE_SECRET not in out


def test_import_skips_the_existing_writer_row(rows, fixture_repo, capsys):
    (merge,) = by_kind(rows, "merge")
    store = StubSupabase([merge])  # the row ams-writer record-merge already wrote
    assert bh.import_rows(rows, _settings(), store) == 0
    assert len(store.rows) == len(rows)
    assert sum(1 for r in store.rows if r["kind"] == "merge") == 1


def test_import_inserts_in_time_order(rows):
    store = StubSupabase()
    bh.import_rows(list(reversed(rows)), _settings(), store)
    times = [bh.parse_time(r["occurred_at"]) for r in store.rows]
    assert times == sorted(times)


def test_import_without_service_key_sends_nothing(rows, capsys):
    store = StubSupabase()
    assert bh.import_rows(rows, _settings(key=None), store) == 1
    assert store.calls == []
    assert "loaded: no" in capsys.readouterr().out


def test_import_failure_exits_nonzero_without_echoing(rows, capsys):
    def failing(method, url, headers, body):
        return 500, json.dumps({"message": "boom " + FAKE_SECRET}).encode()
    assert bh.import_rows(rows, _settings(), failing) == 1
    out = capsys.readouterr().out
    assert "http status 500" in out and FAKE_SECRET not in out


def test_readcheck_matches_every_record_with_the_publishable_key(rows, capsys):
    store = StubSupabase(rows)
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, page=5) == 0
    out = capsys.readouterr().out
    assert f"rows: {len(rows)}" in out and "missing: 0" in out
    assert "commit: records 7, rows 7" in out
    assert all(c[0] == "GET" for c in store.calls)


def test_readcheck_fails_when_a_record_has_no_row(rows, capsys):
    store = StubSupabase(rows[1:])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 1
    assert "missing: 1" in capsys.readouterr().out


def test_readcheck_fails_on_a_hand_typed_row_no_record_derives(rows, capsys):
    # The criterion's must-fail case: a well-formed row (commit kind, a made-up
    # SHA, recorded_fact, an https link) that no record produces.
    fake_sha = "".join(_rng.choice("0123456789abcdef") for _ in range(40))
    planted = {"kind": "commit", "subject": "Hand-typed commit", "summary": "never happened",
               "occurred_at": rows[-1]["occurred_at"], "source_kind": "commit",
               "source_ref": fake_sha, "source_url": bh._commit_url(fake_sha),
               "strength": bh.STRENGTH, "detail": {}}
    store = StubSupabase([*rows, planted])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 1
    out = capsys.readouterr().out
    assert "missing: 0" in out and "extra: 1" in out
    assert f"extra: commit commit {fake_sha}" in out


# --- pinned readcheck (review N1, N2 at d6d4a6d) ------------------------------


def _later_merge():
    sha = "".join(_rng.choice("0123456789abcdef") for _ in range(40))
    return {"kind": "merge", "subject": "PR #9", "summary": "Merged after the candidate",
            "occurred_at": "2026-11-02T09:00:00Z", "source_kind": "commit", "source_ref": sha,
            "source_url": bh._commit_url(sha), "strength": bh.STRENGTH, "is_test": False,
            "detail": {}}


CUTOFF = bh.parse_time("2026-11-01T23:00:00Z")


def test_a_pinned_readcheck_is_not_failed_by_a_merge_after_the_ref(rows, capsys):
    store = StubSupabase([*rows, _later_merge()])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 0
    out = capsys.readouterr().out
    assert "missing: 0" in out and "extra: 0" in out and "newer than ref: 1" in out
    assert "content mismatches: 0" in out


def test_a_pinned_readcheck_fails_on_a_missing_pre_ref_row_and_names_it(rows, capsys):
    gone = next(r for r in rows if r["kind"] == "spec_event")
    store = StubSupabase([r for r in rows if r is not gone])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 1
    out = capsys.readouterr().out
    assert "missing: 1" in out
    assert f"missing: spec_event path {gone['source_ref']}" in out


def test_a_row_before_the_ref_that_no_record_derives_is_extra_not_newer(rows, capsys):
    early = dict(_later_merge(), occurred_at="2026-11-01T10:05:00Z")
    store = StubSupabase([*rows, early])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 1
    out = capsys.readouterr().out
    assert "extra: 1" in out and "newer than ref: 0" in out


def test_readcheck_names_at_most_twenty_keys_then_counts_the_rest(rows, capsys):
    store = StubSupabase()
    assert bh.readcheck(rows * 1, URL, FAKE_PUBLISHABLE, store) == 1
    out = capsys.readouterr().out
    named = [line for line in out.splitlines()
             if line.startswith("missing: ") and " " in line[9:] and "... and" not in line]
    assert len(named) == min(20, len(rows))
    if len(rows) > 20:
        assert f"missing: ... and {len(rows) - 20} more" in out


def test_a_service_key_edit_to_a_real_row_fails_readcheck_and_is_named(rows, capsys):
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "commit")
    victim["summary"] = "Rewritten by hand"
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 1
    out = capsys.readouterr().out
    assert "content mismatches: 1" in out
    assert f"mismatch: commit commit {victim['source_ref']}: summary" in out


@pytest.mark.parametrize("field,value", [("subject", "other"),
                                         ("source_url", "https://example.com/elsewhere"),
                                         ("occurred_at", "2026-11-01T00:00:01Z")])
def test_each_compared_field_is_checked(rows, capsys, field, value):
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "task")
    victim[field] = value
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 1
    assert f": {field}" in capsys.readouterr().out


def test_times_are_compared_as_instants_not_spellings(rows, capsys):
    store = StubSupabase(rows)
    for row in store.rows:
        row["occurred_at"] = row["occurred_at"].replace("Z", "+00:00")
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 0
    assert "content mismatches: 0" in capsys.readouterr().out


def test_import_reports_a_changed_row_and_leaves_it_without_the_flag(rows, capsys):
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "spec_event")
    victim["summary"] = "Older wording"
    assert bh.import_rows(rows, _settings(), store) == 0
    out = capsys.readouterr().out
    assert "changed: 1 (not updated; run with --refresh-changed)" in out
    assert victim["summary"] == "Older wording"
    assert not any(c[0] == "PATCH" for c in store.calls)


def test_refresh_changed_updates_each_changed_row_and_logs_its_old_values(rows, capsys):
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "spec_event")
    victim["summary"] = "Older wording"
    want = next(r for r in rows if bh._key(r) == bh._key(victim))
    assert bh.import_rows(rows, _settings(), store, refresh_changed=True) == 0
    out = capsys.readouterr().out
    assert f"refreshed: spec_event path {victim['source_ref']}: summary" in out
    assert "refreshed: 1" in out
    assert victim["summary"] == want["summary"]
    assert victim["detail"]["refreshed"][-1]["previous"] == {"summary": "Older wording"}
    patches = [c for c in store.calls if c[0] == "PATCH"]
    assert len(patches) == 1 and f"id=eq.{victim['id']}" in patches[0][1]
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store) == 0
    capsys.readouterr()
    assert bh.import_rows(rows, _settings(), store, refresh_changed=True) == 0
    assert "refreshed: 0" in capsys.readouterr().out


def test_a_second_refresh_keeps_the_first_refreshs_old_values(rows, capsys):
    # Codex P2 on PR #65: refresh history is appended, never replaced.
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "spec_event")
    victim["summary"] = "Original wording"
    assert bh.import_rows(rows, _settings(), store, refresh_changed=True) == 0
    victim["summary"] = "Intermediate wording"
    assert bh.import_rows(rows, _settings(), store, refresh_changed=True) == 0
    capsys.readouterr()
    history = victim["detail"]["refreshed"]
    assert [h["previous"]["summary"] for h in history] == ["Original wording",
                                                           "Intermediate wording"]


def test_a_refresh_refuses_a_row_changed_after_it_was_read(rows, capsys):
    # Codex P2 on PR #65: the update is conditional on the values it read.
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "spec_event")
    victim["summary"] = "Older wording"

    def racing(method, url, headers, body):
        if method == "PATCH":
            victim["summary"] = "Written by someone else meanwhile"
        return store(method, url, headers, body)
    assert bh.import_rows(rows, _settings(), racing, refresh_changed=True) == 1
    out = capsys.readouterr().out
    assert f"refused: spec_event path {victim['source_ref']} changed since it was read" in out
    assert victim["summary"] == "Written by someone else meanwhile"
    assert "refreshed" not in victim["detail"]


def test_a_pinned_readcheck_reads_a_refreshed_row_as_it_stood_at_the_ref(rows, capsys):
    # Codex P2 on PR #65: a refresh after the ref does not fail a readcheck pinned before it.
    store = StubSupabase(rows)
    victim = next(r for r in store.rows if r["kind"] == "spec_event")
    pinned_summary = victim["summary"]
    victim["summary"] = "Condensed later"
    victim["detail"] = dict(victim["detail"], refreshed=[
        {"at": "2026-11-02T08:00:00Z", "previous": {"summary": pinned_summary}}])
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 0
    assert "content mismatches: 0" in capsys.readouterr().out
    victim["detail"]["refreshed"][0]["at"] = "2026-11-01T22:00:00Z"  # refreshed before the ref
    assert bh.readcheck(rows, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 1
    assert ": summary" in capsys.readouterr().out


def test_a_reply_after_the_cutoff_cannot_add_an_earlier_fix(fixture_repo):
    # Codex P2 on PR #65: a fix named in a later reply is dated by its commit,
    # so comments are cut off before review events are derived.
    repo, shas = fixture_repo
    cutoff = bh.parse_time("2026-11-01T10:31:00Z")  # after the fix commit, before the replies
    pinned = bh.collect(bh.Sources(git=git_runner(repo), gh=gh_stub(shas),
                                   lifecycle=lifecycle_stub, refs=("main",), cutoff=cutoff))
    assert not [r for r in pinned if r["kind"] == "correction_fix"]
    finding = next(r for r in pinned if r["source_ref"] == "#1 comment 100")
    assert finding["detail"]["fix_commit"] is None


def test_collect_at_a_cutoff_drops_github_events_after_it(fixture_repo):
    repo, shas = fixture_repo
    cutoff = bh.parse_time("2026-11-01T10:20:00Z")
    pinned = bh.collect(bh.Sources(git=git_runner(repo), gh=gh_stub(shas),
                                   lifecycle=lifecycle_stub, refs=("main",), cutoff=cutoff))
    github = [r for r in pinned if r["kind"] in ("pr_opened", "merge", "correction_fix")
              or (r["kind"] in ("return", "correction") and r["source_kind"] == "pr")]
    assert github and all(bh.parse_time(r["occurred_at"]) <= cutoff for r in github)
    assert {r["source_ref"] for r in pinned if r["kind"] == "pr_opened"} == {"#1", "#2"}
    assert not [r for r in pinned if r["kind"] == "merge"]


def test_dev_only_rows_are_extra_unless_the_dev_ref_is_named(fixture_repo, rows, capsys):
    repo, shas = fixture_repo
    main_only = bh.collect(bh.Sources(git=git_runner(repo), gh=gh_stub(shas),
                                      lifecycle=lifecycle_stub, refs=("main",), cutoff=CUTOFF))
    store = StubSupabase(rows)  # imported from main and dev
    assert bh.readcheck(main_only, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 1
    assert f"extra: commit commit {shas['dev']}" in capsys.readouterr().out
    with_dev = bh.collect(bh.Sources(git=git_runner(repo), gh=gh_stub(shas),
                                     lifecycle=lifecycle_stub, refs=("main", "dev"),
                                     cutoff=CUTOFF))
    assert bh.readcheck(with_dev, URL, FAKE_PUBLISHABLE, store, cutoff=CUTOFF) == 0


def test_main_readcheck_pins_to_ref_and_dev_ref(fixture_repo, rows, capsys):
    repo, shas = fixture_repo
    store = StubSupabase([*rows, _later_merge()])
    code = bh.main(["readcheck", "--ref", shas["close"], "--dev-ref", shas["dev"]], environ=ENV,
                   dotenv_path=Path("/nonexistent/ams-test-dotenv"), http=store,
                   git=git_runner(repo), gh=gh_stub(shas), lifecycle=lifecycle_stub)
    out = capsys.readouterr().out
    assert code == 0, out
    assert f"ref: {shas['close']}" in out and f"dev ref: {shas['dev']}" in out
    assert "newer than ref: 1" in out


def test_resolved_threads_page_past_one_hundred_pull_requests():
    pages = [{"data": {"repository": {"pullRequests": {
                 "pageInfo": {"hasNextPage": True, "endCursor": "C1"},
                 "nodes": [{"number": n, "reviewThreads": {"pageInfo": {"hasNextPage": False},
                            "nodes": [{"isResolved": True,
                                       "comments": {"nodes": [{"databaseId": n}]}}]}}
                           for n in range(1, 101)]}}}},
             {"data": {"repository": {"pullRequests": {
                 "pageInfo": {"hasNextPage": False, "endCursor": None},
                 "nodes": [{"number": 101, "reviewThreads": {"pageInfo": {"hasNextPage": False},
                            "nodes": [{"isResolved": False,
                                       "comments": {"nodes": [{"databaseId": 101}]}}]}}]}}}}]
    calls = []

    def gh(args):
        calls.append(list(args))
        return json.dumps(pages[len(calls) - 1])
    resolved = bh._resolved_threads(gh)
    assert len(resolved) == 101 and resolved[1] is True and resolved[101] is False
    assert any("after=C1" in a for a in calls[1])
    assert not any(a.startswith("after=") for a in calls[0])


def test_readcheck_refuses_a_secret_key(rows, capsys):
    store = StubSupabase(rows)
    assert bh.readcheck(rows, URL, FAKE_SECRET, store) == 1
    assert store.calls == []


def test_main_dry_run_prints_counts_and_writes_nothing(fixture_repo, capsys):
    repo, shas = fixture_repo
    store = StubSupabase()
    code = bh.main(["import", "--dry-run", "--ref", "main", "--ref", "dev"], environ=ENV,
                   dotenv_path=Path("/nonexistent/ams-test-dotenv"), http=store,
                   git=git_runner(repo), gh=gh_stub(shas), lifecycle=lifecycle_stub)
    assert code == 0
    assert store.calls == []
    out = capsys.readouterr().out
    assert "commit: 7" in out and "correction: 5" in out


def test_parse_time_handles_offsets():
    assert bh.parse_time("2026-11-01T06:20:13-07:00") == bh.parse_time("2026-11-01T13:20:13Z")
    assert isinstance(bh.parse_time("2026-11-01T10:55:00.000Z"), datetime)


def test_entry_point_is_registered():
    text = Path(writer.REPO_ROOT, "pyproject.toml").read_text()
    assert 'ams-history = "ams.build_history:main"' in text


def test_every_line_link_shows_its_row_in_the_linked_commit(rows, fixture_repo):
    # Codex P2 on PR #31: a line added above an older row must not shift its link.
    repo, _ = fixture_repo
    linked = [r for r in rows if "/blob/" in r["source_url"] and "#L" in r["source_url"]]
    assert any(r["source_ref"] == SPEC_PATH + "#evidence-1" for r in linked)
    for row in linked:
        tail = row["source_url"].split("/blob/", 1)[1]
        sha, rest = tail.split("/", 1)
        path, line = rest.rsplit("#L", 1)
        text = _git(repo, "show", f"{sha}:{path}").splitlines()[int(line) - 1]
        if "#evidence-" in row["source_ref"] or "#receipt-" in row["source_ref"]:
            assert text.startswith("| 2026-11-01") or text.startswith("| 1 |"), (row["source_ref"], text)
        if row["kind"] == "task":
            assert text.startswith("| " + row["subject"].split()[1]), text
        if row["source_kind"] == "jot":
            assert row["source_ref"] in text


def test_a_table_only_task_keeps_its_key_when_its_task_md_arrives(tmp_path, fixture_repo, rows):
    # Codex P2 on PR #31: materialising TASK.md must not create a second task row.
    repo, shas = fixture_repo
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "-b", "main", str(repo), str(clone)], check=True)
    _write(clone, "workbench/specs/S-001-demo/tasks/TK-002/TASK.md", "# TK-002 - Planned\n")
    _git(clone, "add", "-A")
    _git(clone, "commit", "-q", "-m", "Materialise TK-002", when="2026-11-01T11:00:00Z")
    later = bh.collect(bh.Sources(git=git_runner(clone), gh=gh_stub(shas),
                                  lifecycle=lifecycle_stub, refs=("main",)))
    before = {bh._key(r) for r in rows if r["kind"] == "task"}
    after = {bh._key(r) for r in later if r["kind"] == "task"}
    assert before == after


@pytest.mark.parametrize("subject,ids", [("Claim S-004 TK-000A", ("S-004", "TK-000A")),
                                         ("Claim S-006 TK-004", ("S-006", "TK-004")),
                                         ("Claim S-003Z TK-008G", ("S-003Z", "TK-008G")),
                                         ("Claimed nothing", None)])
def test_claim_commits_with_widened_ids_are_task_claims(subject, ids):
    # The real history holds "Claim S-004 TK-000A"; widened IDs end in letters.
    commit = {"sha": "b" * 40, "parents": ["c" * 40], "time": "2026-11-01T10:00:00Z",
              "author": "x", "subject": subject, "refs": ["main"]}
    claims = [r for r in bh.commit_rows([commit], {}) if r["kind"] == "task_claimed"]
    assert [(r["detail"]["spec"], r["detail"]["task"]) for r in claims] == ([ids] if ids else [])
