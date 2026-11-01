"""Import this repository's build history into ``build_events`` (S-006 TK-004).

Every row is derived, read-only, from a real record and names it:

- ``commit``: each commit reachable from the given refs (default
  ``origin/main`` and ``origin/dev``), from ``git log``; source the SHA.
- ``merge``: each merged pull request, built by ``ams.writer.merge_event`` so
  it shares its key with rows ``ams-writer record-merge`` already wrote.
- ``pr_opened``: each pull request's opening, from ``gh pr list``.
- ``return``: returned work: a pull request closed unmerged, a review that
  requested changes, or a Spec evidence-log row that reopens, returns or fails.
- ``correction``: a Codex review finding (``gh api .../pulls/comments``), a Spec
  evidence-log row that starts ``Correction``, or a Wiki entry whose ``Kind``
  names a correction.
- ``correction_fix``: the commit a reply names as the fix for a finding.
- ``spec``, ``task``: each Spec and Task record the lifecycle tool lists
  (``spec-workbench.mjs list --all --json`` and ``show S-### --json``), dated by
  the commit that added its file.
- ``spec_event``: each other Spec evidence-log row; ``task_receipt``: each Task
  Receipt row; ``task_claimed``: each ``Claim S-### TK-###`` commit. A table row
  is dated by the commit that recorded it (``git blame``).

Each row carries strength ``recorded_fact`` and a ``source_url``; a row without
a source is refused before anything is sent. Inserts use the table's unique key
``(kind, source_kind, source_ref)`` with ``resolution=ignore-duplicates``, so a
re-import adds no rows. Rows are sorted and inserted in the order the events
occurred. Records must be committed: uncommitted changes under ``workbench/``
are refused, because a row must link a source others can open.

Commands: ``ams-history import [--dry-run] [--ref REF ...] [--refresh-changed]``
writes with the service key and reports stored rows whose subject, summary, time
or link no longer match the records; ``--refresh-changed`` updates them, logging
each and keeping the old values in ``detail.refreshed``.
``ams-history readcheck [--ref SHA] [--dev-ref REF]`` reads the records in a
temporary worktree at SHA (default HEAD), keeps GitHub events up to SHA's commit
time, and compares every row the publishable key reads: it fails on a missing
row, an extra row (one no record derives, so a hand-typed row fails it), a
content mismatch, an unsourced row or rows out of order, naming up to 20 keys of
each. Rows after SHA that it does not derive count as newer than the ref.
Dev-only commits are expected only when ``--dev-ref`` names the dev branch.
No key is ever printed.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from ams import keycheck, source_rules, writer

REPO_ROOT = writer.REPO_ROOT
REPO_URL = writer.REPO_URL
REPO_SLUG = REPO_URL.removeprefix("https://github.com/")
STRENGTH = "recorded_fact"
SOURCE_KINDS = source_rules.SOURCE_KINDS
DEFAULT_REFS = ("origin/main", "origin/dev")
CONFLICT_KEY = "kind,source_kind,source_ref"
BATCH = 200
# `commits` is left out: in one GraphQL query it exceeds GitHub's node limit, so
# each PR's commits come from REST instead (`_pr_commits`).
PR_FIELDS = ("number,title,state,url,createdAt,closedAt,mergedAt,mergeCommit,"
             "headRefName,baseRefName,reviews")
EVIDENCE_HEADING = "## Append-Only Evidence And Execution Log"
RECEIPT_HEADING = "## Receipt"
READ_COLUMNS = "id,kind,source_kind,source_ref,occurred_at,source_url,strength,subject,summary"
# The fields readcheck compares with the re-derived records (review N1); detail is
# bookkeeping (refs, PR numbers, receipt cells) and is not compared.
CONTENT_FIELDS = ("subject", "summary", "occurred_at", "source_url")
SHOWN = 20  # keys printed per list before the rest are counted

Runner = Callable[[Sequence[str]], str]

_KIND = re.compile(r"^[a-z][a-z_]*$")
_CLAIM = re.compile(r"^Claim (S-[0-9A-Z]+) (TK-[0-9A-Z]+)\b")
# "Fixed in abc1234" or a later "Correction: the fix commit is abc1234"; the newest wins.
_FIX_NAMED = re.compile(r"\b(?:fixed in|fix commit is) `?([0-9a-f]{7,40})\b", re.IGNORECASE)
_PRIORITY = re.compile(r"!\[(P\d) Badge\]")
_CORRECTION_EVENT = re.compile(r"^correction\b", re.IGNORECASE)
_RETURN_EVENT = re.compile(r"^(return|returned|reopen|reopened|fail|failed|revert|reverted)\b",
                           re.IGNORECASE)
_JOT_HEADING = re.compile(r"^#{2,6}\s+(JOT-[0-9a-f-]+)\s*$")


class RefusedError(Exception):
    """The records cannot be imported as they stand; nothing was sent."""


@dataclass(frozen=True)
class Sources:
    git: Runner
    gh: Runner
    lifecycle: Runner
    refs: tuple[str, ...] = DEFAULT_REFS
    # A pinned readcheck keeps GitHub events (PRs, merges, review threads) that
    # occurred at or before this instant: the pinned ref's commit time.
    cutoff: datetime | None = None


# --- small helpers -----------------------------------------------------------


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"time without a zone: {value}")
    return parsed


def utc(value: str | datetime) -> str:
    moment = parse_time(value) if isinstance(value, str) else value
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _commit_url(sha: str) -> str:
    return f"{REPO_URL}/commit/{sha}"


def _blob_url(sha: str, path: str, line: int | None = None) -> str:
    return f"{REPO_URL}/blob/{sha}/{path}" + (f"#L{line}" if line else "")


def _row(kind, subject, summary, occurred_at, source_kind, source_ref, source_url, detail):
    return {"kind": kind, "subject": subject, "summary": summary, "occurred_at": occurred_at,
            "source_kind": source_kind, "source_ref": source_ref, "source_url": source_url,
            "strength": STRENGTH, "is_test": False, "detail": detail}


def _key(row: Mapping) -> tuple[str, str, str]:
    return (row["kind"], row["source_kind"], row["source_ref"])


def _field_name(header: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", header.strip().lower()).strip("_")


def _slug(heading: str) -> str:
    text = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"\s+", "-", text)


def validate(row: Mapping) -> None:
    """Raise ValueError unless the row names a real source and recorded_fact strength."""
    if not isinstance(row.get("kind"), str) or not _KIND.match(row["kind"]):
        raise ValueError(f"bad kind {row.get('kind')!r}")
    for name in ("subject", "summary"):
        if not isinstance(row.get(name), str) or not row[name].strip():
            raise ValueError(f"row without {name}: {row.get('kind')}")
    source_rules.check_source(row, table="build_events")  # the rule every site table shares (TK-005)
    if row.get("source_kind") not in SOURCE_KINDS:
        raise ValueError(f"row without a source kind: {row.get('kind')}")
    if not isinstance(row.get("source_ref"), str) or not row["source_ref"].strip():
        raise ValueError(f"row without a source: {row.get('kind')} {row.get('subject')}")
    url = row.get("source_url")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError(f"row without a source link: {row.get('kind')} {row['source_ref']}")
    if row.get("strength") != STRENGTH:
        raise ValueError(f"row not labelled {STRENGTH}: {row['source_ref']}")
    if row.get("is_test") is not False:
        raise ValueError(f"the importer writes no test rows: {row['source_ref']}")
    try:
        parse_time(row.get("occurred_at") or "")
    except (TypeError, ValueError):
        raise ValueError(f"row without a time: {row['source_ref']}") from None


# --- Git ---------------------------------------------------------------------


def _commits(git: Runner, refs: Sequence[str]) -> list[dict]:
    out = git(["log", "--format=%H%x1f%P%x1f%cI%x1f%an%x1f%s%x1e", *refs, "--"])
    membership = {ref: set(git(["rev-list", ref, "--"]).split()) for ref in refs}
    names = {ref: ref.removeprefix("origin/") for ref in refs}
    commits = []
    for record in out.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        sha, parents, committed, author, subject = record.split("\x1f")
        commits.append({"sha": sha, "parents": parents.split(), "time": committed,
                        "author": author, "subject": subject,
                        "refs": sorted(names[r] for r in refs if sha in membership[r])})
    return commits


def _first_commit(git: Runner, path: str) -> tuple[str, str] | None:
    out = git(["log", "--follow", "--diff-filter=A", "--format=%H%x1f%cI", "HEAD", "--", path])
    lines = [line for line in out.splitlines() if line.strip()]
    if not lines:
        return None
    sha, committed = lines[-1].split("\x1f")
    return sha, committed


def _blame(git: Runner, path: str) -> list[tuple[str, str, int, str, str]]:
    """(commit, utc time, line, text, path) for each line of path at HEAD.

    The line number and path are the ones the line had in that commit, so a
    link to the commit's blob shows the line even after lines above it moved
    or the file was renamed.
    """
    try:
        out = git(["blame", "--line-porcelain", "HEAD", "--", path])
    except subprocess.CalledProcessError:
        return []
    lines, sha, when, number, origin = [], None, None, 0, path
    for raw in out.splitlines():
        if raw.startswith("\t"):
            lines.append((sha, when, number, raw[1:], origin))
            continue
        head = raw.split(" ")
        if len(head) >= 3 and re.fullmatch(r"[0-9a-f]{40}", head[0]):
            sha, number = head[0], int(head[1])
        elif head[0] == "filename":
            origin = raw[len("filename "):]
        elif head[0] == "committer-time":
            when = utc(datetime.fromtimestamp(int(head[1]), tz=timezone.utc))
    return lines


def _table(lines, heading: str) -> list[tuple[dict, tuple[str, str, int, str]]]:
    """Rows of the first Markdown table under heading, each with its blame line."""
    start = next((i for i, line in enumerate(lines) if line[3].strip() == heading), None)
    if start is None:
        return []
    header, rows = None, []
    for line in lines[start + 1:]:
        text = line[3].strip()
        if text.startswith("#"):
            break
        if not text.startswith("|"):
            if header is not None:
                break
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", text)[1:-1]]
        if header is None:
            header = [_field_name(c) for c in cells]
        elif all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        else:
            rows.append((dict(zip(header, cells)), line))
    return rows


# --- rows from each record ---------------------------------------------------


def commit_rows(commits: Iterable[dict], prs_of: Mapping[str, list[int]]) -> list[dict]:
    rows = []
    for c in commits:
        rows.append(_row("commit", c["sha"][:7], c["subject"] or "(no subject)", utc(c["time"]),
                         "commit", c["sha"], _commit_url(c["sha"]),
                         {"author": c["author"], "parents": c["parents"], "refs": c["refs"],
                          "prs": sorted(prs_of.get(c["sha"], []))}))
        claim = _CLAIM.match(c["subject"])
        if claim:
            spec, task = claim.groups()
            rows.append(_row("task_claimed", f"{spec} {task}", c["subject"], utc(c["time"]),
                             "commit", c["sha"], _commit_url(c["sha"]),
                             {"spec": spec, "task": task}))
    return rows


def pr_rows(prs: Iterable[dict], git: Runner) -> list[dict]:
    rows = []
    for pr in prs:
        number, url = pr["number"], pr["url"]
        rows.append(_row("pr_opened", f"PR #{number}", pr["title"], utc(pr["createdAt"]), "pr",
                         f"#{number}", url,
                         {"pr": number, "base": pr["baseRefName"], "head": pr["headRefName"],
                          "state": pr["state"]}))
        merge = (pr.get("mergeCommit") or {}).get("oid")
        if pr["state"] == "MERGED" and merge:
            try:
                rows.append(writer.merge_event(merge, git=git))
            except (ValueError, subprocess.CalledProcessError):
                # Not a merge commit in local Git (squash or rebase merge): use GitHub's record.
                rows.append(_row("merge", f"PR #{number}", pr["title"], utc(pr["mergedAt"]),
                                 "commit", merge, _commit_url(merge),
                                 {"pr": number, "pr_url": url, "branch": pr["headRefName"]}))
        elif pr["state"] == "CLOSED" and pr.get("closedAt"):
            rows.append(_row("return", f"PR #{number}", f"Closed unmerged: {pr['title']}",
                             utc(pr["closedAt"]), "pr", f"#{number}", url,
                             {"pr": number, "reason": "closed unmerged"}))
        for review in pr.get("reviews") or []:
            if review.get("state") != "CHANGES_REQUESTED":
                continue
            login = (review.get("author") or {}).get("login", "unknown")
            rows.append(_row("return", f"PR #{number}", f"Changes requested by {login}",
                             utc(review["submittedAt"]), "pr", f"#{number} review {review['id']}",
                             url, {"pr": number, "reason": "changes requested",
                                   "reviewer": login}))
    return rows


def _is_codex(login: str) -> bool:
    return login.endswith("[bot]") and "codex" in login.lower()


def _finding_title(body: str) -> str:
    first = next((line for line in body.splitlines() if line.strip()), "")
    first = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", first)
    first = re.sub(r"</?sub>|\*\*", "", first)
    return first.strip() or "Codex review finding"


def review_rows(prs: Sequence[dict], comments: Sequence[dict], resolved: Mapping[int, bool],
                git: Runner) -> list[dict]:
    pr_commits = {c["oid"]: c for pr in prs for c in pr.get("commits") or []}
    replies: dict[int, list[dict]] = {}
    for comment in comments:
        if comment.get("in_reply_to_id"):
            replies.setdefault(comment["in_reply_to_id"], []).append(comment)
    rows, fixes = [], {}
    for comment in comments:
        login = (comment.get("user") or {}).get("login", "")
        if comment.get("in_reply_to_id") or not _is_codex(login):
            continue
        number = int(comment["pull_request_url"].rstrip("/").rsplit("/", 1)[1])
        ref, title = f"#{number} comment {comment['id']}", _finding_title(comment["body"])
        priority = _PRIORITY.search(comment["body"])
        fix_sha, fix_reply, named_earlier = None, None, []
        human = [r for r in replies.get(comment["id"], [])
                 if not _is_codex((r.get("user") or {}).get("login", ""))]
        for reply in sorted(human, key=lambda r: r["created_at"], reverse=True):
            named = _FIX_NAMED.search(reply["body"])
            if not named:
                continue
            if fix_reply is None:  # the newest naming reply decides, even if unresolvable
                fix_sha = _resolve_commit(named.group(1), pr_commits, git)
                fix_reply = reply["html_url"]
            else:
                named_earlier.insert(0, named.group(1))
        for reply in human:
            first = reply["body"].strip().splitlines()[0].strip() if reply["body"].strip() else ""
            if _CORRECTION_EVENT.match(first):
                rows.append(_row("correction", f"PR #{number}", first, utc(reply["created_at"]),
                                 "pr", f"#{number} comment {reply['id']}", reply["html_url"],
                                 {"pr": number, "author": reply["user"]["login"],
                                  "corrects": ref}))
        rows.append(_row("correction", f"PR #{number}", title, utc(comment["created_at"]), "pr",
                         ref, comment["html_url"],
                         {"pr": number, "reviewer": login, "priority": priority and priority.group(1),
                          "path": comment.get("path"), "resolved": resolved.get(comment["id"]),
                          "fix_commit": fix_sha and fix_sha[0], "fix_reply_url": fix_reply,
                          "fix_named_earlier": named_earlier}))
        if fix_sha:
            entry = fixes.setdefault(fix_sha[0], {"time": fix_sha[1], "findings": [], "titles": [],
                                                   "prs": set(), "replies": []})
            entry["findings"].append(ref)
            entry["titles"].append(title)
            entry["prs"].add(number)
            entry["replies"].append(fix_reply)
    for sha, entry in fixes.items():
        prs_named = sorted(entry["prs"])
        rows.append(_row("correction_fix", sha[:7],
                         "Fix for review finding: " + "; ".join(entry["titles"]),
                         utc(entry["time"]), "commit", sha, _commit_url(sha),
                         {"findings": entry["findings"], "prs": prs_named,
                          "reply_urls": entry["replies"]}))
    return rows


def _resolve_commit(prefix: str, pr_commits: Mapping[str, dict], git: Runner):
    matches = [oid for oid in pr_commits if oid.startswith(prefix)]
    if len(matches) == 1:
        return matches[0], pr_commits[matches[0]]["committedDate"]
    try:
        out = git(["show", "-s", "--format=%H%x1f%cI", prefix + "^{commit}", "--"]).strip()
    except subprocess.CalledProcessError:
        return None
    sha, committed = out.splitlines()[0].split("\x1f")
    return sha, committed


def record_rows(git: Runner, lifecycle: Runner) -> list[dict]:
    rows = []
    for listed in json.loads(lifecycle(["list", "--all", "--json"]))["specs"]:
        spec_id, path = listed["id"], listed["path"]
        shown = json.loads(lifecycle(["show", spec_id, "--json"]))
        created = _first_commit(git, path)
        if created is None:
            raise RefusedError(f"{path} is not committed")
        rows.append(_row("spec", spec_id, f"{spec_id} - {listed['title']}", utc(created[1]), "path",
                         path, _blob_url(created[0], path),
                         {"status": listed.get("status"), "landmark": listed.get("landmarkId"),
                          "created_commit": created[0]}))
        blame = _blame(git, path)
        for index, (cells, line) in enumerate(_table(blame, EVIDENCE_HEADING), start=1):
            event = cells.get("event", "").strip()
            task = cells.get("task", "").strip()
            kind = ("correction" if _CORRECTION_EVENT.match(event)
                    else "return" if _RETURN_EVENT.match(event) else "spec_event")
            subject = f"{spec_id} {task}" if task and task.lower() != "none" else spec_id
            rows.append(_row(kind, subject, event or "(no event)", line[1], "path",
                             f"{path}#evidence-{index}", _blob_url(line[0], line[4], line[2]),
                             dict(cells, spec=spec_id, recorded_commit=line[0])))
        for task in [*shown.get("tasks", []), *shown.get("retiredTasks", [])]:
            rows.extend(_task_rows(git, spec_id, path, task))
    return rows


def _task_rows(git: Runner, spec_id: str, spec_path: str, task: Mapping) -> list[dict]:
    task_id = task["id"]
    path = posixpath.join(posixpath.dirname(spec_path), "tasks", task_id, "TASK.md")
    created = _first_commit(git, path)
    subject = f"{spec_id} {task_id}"
    # One key per Task whichever record holds it (and wherever the Spec moves), so a
    # table-only Task that later gets its TASK.md is the same event, not a second row.
    identity = f"{spec_id}/{task_id}"
    if created is None:
        # A planned Task recorded only as a row of its Spec's slice table.
        line = next((line for line in _blame(git, spec_path)
                     if re.match(rf"^\|\s*{re.escape(task_id)}\s*\|", line[3])), None)
        if line is None:
            print(f"note: {subject} has no committed record; no task row", file=sys.stderr)
            return []
        return [_row("task", subject, task.get("slice") or task_id, line[1], "path",
                     identity, _blob_url(line[0], line[4], line[2]),
                     {"spec": spec_id, "task": task_id, "status": task.get("status"),
                      "recorded_commit": line[0], "record": spec_path})]
    rows = [_row("task", subject, task.get("slice") or task_id, utc(created[1]), "path", identity,
                 _blob_url(created[0], path),
                 {"spec": spec_id, "task": task_id, "status": task.get("status"),
                  "created_commit": created[0], "record": path})]
    for index, (cells, line) in enumerate(_table(_blame(git, path), RECEIPT_HEADING), start=1):
        rows.append(_row("task_receipt", subject,
                         f"Receipt run {cells.get('run', index)} on {cells.get('branch', 'unknown')}",
                         line[1], "path", f"{path}#receipt-{index}", _blob_url(line[0], line[4], line[2]),
                         dict(cells, spec=spec_id, task=task_id, recorded_commit=line[0])))
    return rows


def wiki_rows(git: Runner) -> list[dict]:
    """Wiki entries whose Kind names a correction; Jot entries keep their JOT id."""
    names = git(["ls-tree", "-r", "--name-only", "HEAD", "--", "workbench/wiki"]).split("\n")
    rows = []
    for path in sorted(n for n in names if n.endswith(".md") and "TEMPLATE" not in n):
        lines = _blame(git, path)
        heading = None
        for i, (sha, when, number, text, origin) in enumerate(lines):
            if text.startswith("#"):
                heading = (text, number, sha, origin)
                continue
            kind_line = re.match(r"^Kind:\s*(.*)$", text)
            if not kind_line or not re.search(r"\bcorrection\b", kind_line.group(1), re.I):
                continue
            if heading is None:
                continue
            jot = _JOT_HEADING.match(heading[0])
            fields, summary = _entry_fields(lines[i:])
            page = Path(path).stem
            if jot:
                recorded = fields.get("recorded")
                rows.append(_row("correction", page, summary or jot.group(1),
                                 utc(recorded) if recorded else when, "jot", jot.group(1),
                                 _blob_url(heading[2], heading[3], heading[1]),
                                 {"page": path, "kind": kind_line.group(1), "state": fields.get("state"),
                                  "author": fields.get("author"), "source": fields.get("source"),
                                  "recorded_commit": sha}))
            else:
                title = heading[0].lstrip("#").strip()
                rows.append(_row("correction", page, title, when, "path", f"{path}#{_slug(title)}",
                                 _blob_url(heading[2], heading[3], heading[1]),
                                 {"page": path, "kind": kind_line.group(1), "recorded_commit": sha}))
    return rows


def _entry_fields(lines) -> tuple[dict, str | None]:
    fields, summary = {}, None
    for _, _, _, text, _ in lines:
        if text.startswith("#") or text.startswith("<!--"):
            break
        field = re.match(r"^([A-Z][A-Za-z ]+):\s*(.*)$", text)
        if field and summary is None:
            fields[_field_name(field.group(1))] = field.group(2).strip()
        elif text.strip() and summary is None:
            summary = text.strip()[:280]
    return fields, summary


# --- collect -----------------------------------------------------------------


KIND_ORDER = {kind: i for i, kind in enumerate(
    ["spec", "task", "pr_opened", "commit", "task_claimed", "correction", "correction_fix",
     "return", "merge", "spec_event", "task_receipt"])}


def collect(sources: Sources) -> list[dict]:
    """Every build-history row the records hold, in the order the events occurred."""
    if sources.git(["status", "--porcelain", "--", "workbench"]).strip():
        raise RefusedError("uncommitted record changes under workbench/; commit them first")
    commits = _commits(sources.git, sources.refs)
    prs = json.loads(sources.gh(["pr", "list", "--repo", REPO_SLUG, "--state", "all",
                                 "--limit", "1000", "--json", PR_FIELDS]))
    prs_of: dict[str, list[int]] = {}
    for pr in prs:
        pr["commits"] = _pr_commits(sources.gh, pr["number"])
        for c in pr["commits"]:
            prs_of.setdefault(c["oid"], []).append(pr["number"])
    comments = [json.loads(line) for line in sources.gh(
        ["api", "--paginate", f"repos/{REPO_SLUG}/pulls/comments?per_page=100", "--jq", ".[]"]
    ).splitlines() if line.strip()]
    if sources.cutoff is not None:
        # Cut comments off first: a later reply can name an earlier fix commit, and
        # that fix row is dated by the commit, not the reply (Codex P2 on PR #65).
        comments = [c for c in comments if parse_time(c["created_at"]) <= sources.cutoff]
    github = [*pr_rows(prs, sources.git),
              *review_rows(prs, comments, _resolved_threads(sources.gh), sources.git)]
    if sources.cutoff is not None:
        github = [r for r in github if parse_time(r["occurred_at"]) <= sources.cutoff]
    rows = [*commit_rows(commits, prs_of), *github,
            *record_rows(sources.git, sources.lifecycle), *wiki_rows(sources.git)]
    seen = set()
    for row in rows:
        validate(row)
        if _key(row) in seen:
            raise RefusedError(f"two events share the key {_key(row)}")
        seen.add(_key(row))
    return sort_rows(rows)


def _pr_commits(gh: Runner, number: int) -> list[dict]:
    out = gh(["api", "--paginate", f"repos/{REPO_SLUG}/pulls/{number}/commits?per_page=100",
              "--jq", ".[] | {oid: .sha, committedDate: .commit.committer.date}"])
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def sort_rows(rows: Iterable[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (parse_time(r["occurred_at"]),
                                       KIND_ORDER.get(r["kind"], 99), r["source_ref"]))


_THREADS_QUERY = """query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes { number reviewThreads(first: 100) {
        pageInfo { hasNextPage }
        nodes { isResolved comments(first: 1) { nodes { databaseId } } } } }
    }
  }
}"""


def _resolved_threads(gh: Runner) -> dict[int, bool]:
    """Each review thread's first comment id -> resolved, over every page of PRs."""
    owner, name = REPO_SLUG.split("/")
    resolved, after = {}, None
    while True:
        args = ["api", "graphql", "-f", f"query={_THREADS_QUERY}",
                "-F", f"owner={owner}", "-F", f"name={name}"]
        if after:
            args += ["-f", f"after={after}"]
        pulls = json.loads(gh(args))["data"]["repository"]["pullRequests"]
        for pr in pulls["nodes"]:
            threads = pr["reviewThreads"]
            if (threads.get("pageInfo") or {}).get("hasNextPage"):
                raise RefusedError(f"PR #{pr['number']} has more than 100 review threads")
            for thread in threads["nodes"]:
                for comment in thread["comments"]["nodes"]:
                    resolved[comment["databaseId"]] = thread["isResolved"]
        if not pulls["pageInfo"]["hasNextPage"]:
            return resolved
        after = pulls["pageInfo"]["endCursor"]


# --- Supabase ----------------------------------------------------------------


def _counts(rows: Iterable[Mapping]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["kind"]] = counts.get(row["kind"], 0) + 1
    return dict(sorted(counts.items()))


def _send(http, method: str, url: str, headers: Mapping[str, str], payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    try:
        status, raw = http(method, url, headers, body)
    except Exception:
        return None, None
    try:
        return status, json.loads(raw) if raw else None
    except ValueError:
        return status, None


def _differences(have: Mapping, want: Mapping) -> list[str]:
    """The compared fields whose stored value differs from the re-derived record."""
    changed = []
    for field in CONTENT_FIELDS:
        if field == "occurred_at":
            try:
                same = parse_time(have.get(field) or "") == parse_time(want[field])
            except ValueError:
                same = False
        else:
            same = have.get(field) == want[field]
        if not same:
            changed.append(field)
    return changed


def _named(label: str, items: Sequence[str]) -> None:
    for item in items[:SHOWN]:
        print(f"{label}: {item}")
    if len(items) > SHOWN:
        print(f"{label}: ... and {len(items) - SHOWN} more")


def _read_all(http, url: str, key: str, columns: str, page: int = 1000):
    headers = writer._headers(key)
    rows, offset = [], 0
    while True:
        query = (f"{writer._rest(url)}?select={columns}&is_test=eq.false"
                 f"&order=occurred_at.asc,id.asc&limit={page}&offset={offset}")
        status, body = _send(http, "GET", query, headers)
        if status != 200 or not isinstance(body, list):
            print(f"select failed: http status {status if status is not None else 'none'}")
            return None
        rows.extend(body)
        if len(body) < page:
            return rows
        offset += page


def import_rows(rows: Sequence[dict], settings: keycheck.Settings, http: writer.Http,
                refresh_changed: bool = False) -> int:
    if settings.key is None:
        print("loaded: no")
        return 1
    if keycheck.key_format(settings.key) == "unrecognized":
        print("loaded: yes\nformat: unrecognized")
        return 1
    try:
        for row in rows:
            validate(row)
    except ValueError as error:
        print(f"refused: {error}; nothing sent")
        return 1
    ordered = sort_rows(rows)
    headers = writer._headers(settings.key)
    headers["Prefer"] = "return=representation,resolution=ignore-duplicates"
    endpoint = f"{writer._rest(settings.url)}?on_conflict={CONFLICT_KEY}"
    inserted: list[dict] = []
    for start in range(0, len(ordered), BATCH):
        status, body = _send(http, "POST", endpoint, headers, ordered[start:start + BATCH])
        if status not in (200, 201) or not isinstance(body, list):
            print(f"insert failed: http status {status if status is not None else 'none'} "
                  f"after {len(inserted)} inserted")
            return 1
        inserted.extend(body)
    made = _counts(inserted)
    for kind, count in _counts(ordered).items():
        print(f"{kind}: records {count}, inserted {made.get(kind, 0)}")
    print(f"inserted: {len(inserted)}\nalready recorded: {len(ordered) - len(inserted)}")
    return _refresh(ordered, settings, http, refresh_changed)


def _refresh(rows: Sequence[dict], settings: keycheck.Settings, http, apply: bool) -> int:
    """Find stored rows whose compared fields differ from the records; update them only
    when asked, logging each one and keeping the old values in detail.refreshed."""
    stored = _read_all(http, settings.url, settings.key, "id,detail," + READ_COLUMNS)
    if stored is None:
        return 1
    want = {_key(r): r for r in rows}
    changed = [(r, want[_key(r)], _differences(r, want[_key(r)]))
               for r in stored if _key(r) in want]
    changed = [c for c in changed if c[2]]
    if not apply:
        print(f"changed: {len(changed)} (not updated; run with --refresh-changed)")
        _named("changed", [f"{' '.join(_key(r))}: {', '.join(f)}" for r, _, f in changed])
        return 0
    headers = writer._headers(settings.key)
    at = utc(datetime.now(timezone.utc))
    for row, record, fields in changed:
        patch = {f: record[f] for f in fields}
        # Append to the stored refresh history; never drop an earlier refresh's values.
        history = (row.get("detail") or {}).get("refreshed") or []
        if isinstance(history, dict):
            history = [history]
        patch["detail"] = dict(record["detail"], refreshed=[
            *history, {"at": at, "previous": {f: row.get(f) for f in fields}}])
        status, _ = _send(http, "PATCH", f"{writer._rest(settings.url)}?id=eq.{row['id']}",
                          headers, patch)
        if status not in (200, 204):
            print(f"refresh failed: http status {status if status is not None else 'none'} "
                  f"at {' '.join(_key(row))}")
            return 1
        print(f"refreshed: {' '.join(_key(row))}: {', '.join(fields)}")
    print(f"refreshed: {len(changed)}")
    return 0


def readcheck(rows: Sequence[dict], url: str, key: str, http: writer.Http, page: int = 1000,
              cutoff: datetime | None = None) -> int:
    """Compare every row the site key reads with the records re-derived at one ref.

    Fails on a record without a row (missing), a row before the ref that no record
    derives (extra), a compared field that differs (content mismatch), an unsourced
    row or rows out of time order. A row after ``cutoff`` that the ref does not
    derive is counted as newer than the ref, not as extra.
    """
    if keycheck.key_format(key) != "unrecognized" or not key.startswith("sb_publishable_"):
        print("refused: the publishable slot holds a key that is not a publishable key")
        return 1
    visible = _read_all(http, url, key, READ_COLUMNS, page)
    if visible is None:
        return 1
    have = {_key(r): r for r in visible}
    want = {_key(r): r for r in rows}
    missing = sorted(want.keys() - have.keys())
    unexpected = sorted(have.keys() - want.keys())
    newer = {k for k in unexpected
             if cutoff is not None and parse_time(have[k]["occurred_at"]) > cutoff}
    extra = [k for k in unexpected if k not in newer]
    mismatches = [(k, _differences(have[k], want[k])) for k in sorted(want.keys() & have.keys())]
    mismatches = [(k, f) for k, f in mismatches if f]
    unsourced = [r for r in visible if not (r.get("source_ref") or "").strip()
                 or not (r.get("source_url") or "").startswith("https://")
                 or r.get("strength") != STRENGTH]
    times = [parse_time(r["occurred_at"]) for r in visible]
    print(f"rows: {len(visible)}")
    seen = _counts(r for r in visible if _key(r) in want)
    for kind, count in _counts(rows).items():
        print(f"{kind}: records {count}, rows {seen.get(kind, 0)}")
    print(f"missing: {len(missing)}\nextra: {len(extra)}\nnewer than ref: {len(newer)}")
    print(f"content mismatches: {len(mismatches)}\nunsourced: {len(unsourced)}")
    print(f"in time order: {'yes' if times == sorted(times) else 'no'}")
    _named("missing", [" ".join(k) for k in missing])
    _named("extra", [" ".join(k) for k in extra])  # hand-typed, fabricated or stale rows
    _named("mismatch", [f"{' '.join(k)}: {', '.join(f)}" for k, f in mismatches])
    for row in visible:
        if row["kind"] in ("return", "correction", "correction_fix"):
            print(f"{row['kind']}: {row['occurred_at']} {row['source_ref']} {row.get('summary', '')}")
    ok = not (missing or extra or mismatches or unsourced) and times == sorted(times)
    return 0 if ok else 1


# --- command line ------------------------------------------------------------


def _runner(prefix: Sequence[str], cwd: Path = REPO_ROOT) -> Runner:
    def run(args: Sequence[str]) -> str:
        return subprocess.run([*prefix, *args], cwd=cwd, check=True, capture_output=True,
                              text=True).stdout
    return run


@contextlib.contextmanager
def _checkout_at(sha: str):
    """A detached temporary worktree at sha, so records are read as they stood there."""
    folder = tempfile.mkdtemp(prefix="ams-history-")
    subprocess.run(["git", "-C", str(REPO_ROOT), "worktree", "add", "-q", "--detach", folder, sha],
                   check=True, capture_output=True)
    try:
        yield Path(folder)
    finally:
        subprocess.run(["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", folder],
                       capture_output=True)


def main(
    argv: list[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    dotenv_path: Path | None = None,
    http: writer.Http | None = None,
    git: Runner | None = None,
    gh: Runner | None = None,
    lifecycle: Runner | None = None,
) -> int:
    parser = argparse.ArgumentParser(prog="ams-history", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    imp = sub.add_parser("import", help="derive build-history rows and insert the new ones")
    imp.add_argument("--ref", action="append", default=[],
                     help="Git ref whose commits are history (default: origin/main, origin/dev)")
    imp.add_argument("--dry-run", action="store_true", help="print counts; send nothing")
    imp.add_argument("--refresh-changed", action="store_true",
                     help="update stored rows whose subject, summary, time or link differ "
                          "from the records, logging each and keeping the old values")
    check = sub.add_parser("readcheck",
                           help="read every row with the publishable key; compare to the records at one ref")
    check.add_argument("--ref", default="HEAD", help="commit the records are read at (default HEAD)")
    check.add_argument("--dev-ref", help="also expect the commits of this ref (the dev branch)")
    args = parser.parse_args(argv)
    git_here = git or _runner(["git", "-C", str(REPO_ROOT)])
    gh = gh or _runner(["gh"])
    environ = os.environ if environ is None else environ
    dotenv_path = keycheck.DOTENV_PATH if dotenv_path is None else dotenv_path
    http = http or writer.urllib_http
    try:
        if args.command == "readcheck":
            return _pinned_readcheck(args, git, git_here, gh, lifecycle, environ, dotenv_path, http)
        rows = collect(Sources(git=git_here, gh=gh,
                               lifecycle=lifecycle or _runner(["node", "workbench/tools/spec-workbench.mjs"]),
                               refs=tuple(args.ref) or DEFAULT_REFS))
    except RefusedError as error:
        print(f"refused: {error}")
        return 1
    except subprocess.CalledProcessError as error:
        print(f"refused: {Path(str(error.cmd[0])).name} failed (exit {error.returncode})")
        return 1
    if args.dry_run:
        for kind, count in _counts(rows).items():
            print(f"{kind}: {count}")
        print(f"total: {len(rows)}")
        return 0
    return import_rows(rows, keycheck.load_settings(environ, dotenv_path), http,
                       refresh_changed=args.refresh_changed)


def _pinned_readcheck(args, git, git_here, gh, lifecycle, environ, dotenv_path, http) -> int:
    sha = git_here(["rev-parse", "--verify", f"{args.ref}^{{commit}}"]).strip()
    dev = git_here(["rev-parse", "--verify", f"{args.dev_ref}^{{commit}}"]).strip() if args.dev_ref else None
    cutoff = parse_time(git_here(["show", "-s", "--format=%cI", sha, "--"]).strip())
    print(f"ref: {sha}\nref time: {utc(cutoff)}")
    print(f"dev ref: {dev}" if dev else "dev ref: none (dev-only rows read as extra)")
    refs = (sha, dev) if dev else (sha,)

    def check(git_at: Runner, lifecycle_at: Runner) -> int:
        rows = collect(Sources(git=git_at, gh=gh, lifecycle=lifecycle_at, refs=refs, cutoff=cutoff))
        settings = keycheck.load_settings(environ, dotenv_path)
        return readcheck(rows, settings.url, writer.publishable_key(environ, dotenv_path), http,
                         cutoff=cutoff)

    if git is not None:  # injected runners (tests) already read the records at the ref
        return check(git, lifecycle)
    with _checkout_at(sha) as folder:
        return check(_runner(["git", "-C", str(folder)], folder),
                     _runner(["node", "workbench/tools/spec-workbench.mjs"], folder))


if __name__ == "__main__":
    sys.exit(main())
