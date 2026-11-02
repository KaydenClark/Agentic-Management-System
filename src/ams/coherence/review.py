"""S-013 TK-004 (ADR-001E): independent Spec review, checked outside the managed runtime.

The native `spec-workbench.mjs verdict` already binds a verdict to a real
candidate commit and to the Spec's content digest. It lacks two things ADR-001E
needs, added here without editing `workbench/tools/`:

  context    A review names its reviewing context: a 12-hex hash of the session
             id (never the id itself). Building sessions name theirs in an
             `AMS-Context:` commit trailer.
  record     Refuses a review whose context or agent built the Spec (Task
             claimants and closers, and trailer contexts, read from the Spec's
             Git history so deleted Task scaffolding still counts), then
             records it through the native `verdict` with agent and context
             in the reviewer cell.
  status     Reports each verdict at a commit: current, stale (the assembled
             commit or the Spec's content changed since review), refused (by a
             builder) or unbound (names no context). Non-blocking.

Run: uv run python -m ams.coherence.review context|builders|record|status ...
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

from ams.coherence.up_to_spec import _find_spec, _git, _section, _show

NATIVE = ["node", "workbench/tools/spec-workbench.mjs"]
CONTEXT = re.compile(r"^[0-9a-f]{12}$")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
TRAILER = re.compile(r"^AMS-Context:\s*([0-9a-f]{12})\s*$", re.M)
CLAIM = re.compile(r"\*\*(?:Claimed by|Current claimant):\*\*\s*(.+)$")
ATTRIBUTION = re.compile(r'"(?:agent|claimant|onBehalfOf)"\s*:\s*"([^"]+)"')
VERDICT = re.compile(r"^Review verdict: (pass|fail) at (\S+) \[([0-9a-f]{12})\] #(\d+)$")
CELL_AGENT = re.compile(r"\bagent:\s*([^;]+)")
CELL_CONTEXT = re.compile(r"\bcontext:\s*([0-9a-f]{12})\b")
NOT_A_NAME = {"", "none", "null", "unclaimed", "n-a"}
REVIEW_ROW = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*review\s*\|\s*Review verdict: ")
REVIEW_HEADER = re.compile(r"^\*\*(?:Updated|Latest event|Next gate):\*\*")
PART_BLOCK = re.compile(r"<!-- workbench-record-section.*?<!-- /workbench-record-section -->", re.S)


class Refused(Exception):
    """A review the procedure will not record."""


def context_id(session: str) -> str:
    return hashlib.sha256(session.encode()).hexdigest()[:12]


def current_context() -> str | None:
    session = os.environ.get("AMS_SESSION_ID") or os.environ.get("CLAUDE_CODE_SESSION_ID")
    return context_id(session) if session else None


def agent_key(name: str) -> str:
    """`Orchestrator C (cloud)`, `orchestrator-C` and `orchestrator c` are one agent."""
    name = re.sub(r"\(.*?\)|`", "", name)
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _spec_paths(spec_id: str) -> str:
    # Matches the Spec's folder wherever it has lived (moves between landmarks).
    return f":(glob)**/{spec_id}-*/**"


def _review_line(line: str) -> bool:
    return bool(REVIEW_ROW.match(line) or REVIEW_HEADER.match(line))


def _review_only(repo: str, spec_id: str, sha: str) -> bool:
    """A commit that only records a review: verdict rows, the header fields `verdict`
    rewrites, a fail verdict's corrective Task records, TASKBOARD and review reports.
    Merges and anything else count as building."""
    if len(_git(repo, "rev-list", "--parents", "-n1", sha).stdout.split()) > 2:
        return False
    folder = re.compile(rf"(^|/){re.escape(spec_id)}-[^/]+/")
    changes = _git(repo, "diff-tree", "--no-commit-id", "-r", "--root", "--name-status", sha).stdout
    for entry in changes.splitlines():
        state, path = entry.split("\t")[0], entry.split("\t")[-1]
        if _report_path(path):
            continue
        if not folder.search(path):
            return False
        if state == "A" and re.search(r"/tasks/[^/]+/TASK\.md$", path):
            body = _show(repo, sha, path)
            if re.search(r"^\*\*Planned verification:\*\* Answers evidence row \d+ \(fail verdict", body, re.M):
                continue
            return False
        if not path.endswith("/SPEC.md") or state != "M":
            return False
        diff = _git(repo, "show", "--no-color", "--format=", "-U0", sha, "--", path).stdout
        lines = [l[1:] for l in diff.splitlines()
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        if not all(_review_line(l) for l in lines):
            return False
    return True


def builders(spec_id: str, repo: str = ".", commit: str = "HEAD") -> dict:
    """Agents and contexts that built the Spec, from its whole history up to `commit`."""
    paths = _spec_paths(spec_id)
    # Session contexts: trailers on commits that touched the Spec folder or name the Spec,
    # except commits that only record a review (a reviewer's own bookkeeping).
    fmt = "--format=%H%x1f%B%x1e"
    log = _git(repo, "log", fmt, commit, "--", paths).stdout + _git(
        repo, "log", "-E", f"--grep={re.escape(spec_id)}([^0-9]|$)", fmt, commit).stdout
    contexts: set[str] = set()
    seen: set[str] = set()
    for entry in filter(str.strip, log.split("\x1e")):
        sha, _, body = entry.strip().partition("\x1f")
        found = set(TRAILER.findall(body))
        if sha in seen or not found:
            continue
        seen.add(sha)
        if not _review_only(repo, spec_id, sha):
            contexts |= found
    patch = _git(repo, "log", "-p", "--no-color", "--format=", commit, "--", paths).stdout
    agents: set[str] = set()
    for line in patch.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        names = ATTRIBUTION.findall(line)
        claim = CLAIM.search(line)
        if claim:
            names += re.split(r",|;|\band\b", claim.group(1))
        agents |= {agent_key(n) for n in names} - NOT_A_NAME
    return {"agents": agents, "contexts": contexts}


def _builder_reasons(agent: str | None, context: str | None, built: dict) -> list[str]:
    reasons = []
    if context and context in built["contexts"]:
        reasons.append(f"context {context} built the Spec (AMS-Context trailer)")
    if agent and agent_key(agent) in built["agents"]:
        reasons.append(f"agent {agent.strip()} built the Spec (claimed or closed a Task)")
    return reasons


def _native(repo: str, argv: list[str]) -> str:
    return subprocess.run([*NATIVE, *argv], cwd=repo, check=True, capture_output=True, text=True).stdout


def record(spec_id: str, candidate: str, result: str, findings: str, reviewer: str, agent: str,
           context: str | None = None, digest: str | None = None, repo: str = ".",
           run_verdict: Callable[[list[str]], object] | None = None):
    """Refuse a non-independent review; otherwise record it with the native verdict."""
    context = current_context() if context is None else context.strip()
    if not context or not CONTEXT.match(context):
        raise Refused(f"the review names no reviewing context ({context or 'none'}); pass --context "
                      "from `review context` in the reviewing session, or --session")
    if not agent or not agent.strip():
        raise Refused("the review names no reviewing agent (--agent)")
    # Bind the exact commit: a ref such as HEAD would re-resolve later and hide staleness.
    resolved = _git(repo, "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}", check=False)
    if resolved.returncode:
        raise Refused(f"candidate {candidate} is not a commit in this repository")
    candidate = resolved.stdout.strip()
    built = builders(spec_id, repo, candidate)
    head = builders(spec_id, repo, "HEAD")
    built = {k: built[k] | head[k] for k in built}
    reasons = _builder_reasons(agent, context, built)
    if reasons:
        raise Refused(f"{spec_id} review refused: {'; '.join(reasons)}. ADR-001E: a Spec is reviewed "
                      "by a context that did not build it; another agent name in the same session "
                      "is not independence.")
    cell = f"{reviewer.strip()}; agent: {agent.strip()}; context: {context}"
    argv = ["verdict", spec_id, "--candidate", candidate, "--result", result,
            "--findings", findings, "--reviewer", cell]
    if digest:
        argv += ["--digest", digest]
    return (run_verdict or (lambda a: _native(repo, a)))(argv)


def native_digest(repo: str, spec_id: str) -> Callable[[str], str]:
    def at(commit: str) -> str:
        report = json.loads(_native(repo, ["report", spec_id, "--candidate", commit, "--json"]))
        binding = report["candidate"]
        if binding.get("contentError") or not binding.get("contentDigest"):
            raise ValueError(f"no Spec digest at {commit}: {binding.get('contentError')}")
        return binding["contentDigest"]
    return at


def _verdicts(spec_text: str) -> list[dict]:
    rows = []
    for line in _section(spec_text, "Append-Only Evidence And Execution Log"):
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) < 6 or cells[1] != "review":
            continue
        m = VERDICT.match(cells[2])
        if not m:
            continue
        agent, context = CELL_AGENT.search(cells[4]), CELL_CONTEXT.search(cells[4])
        rows.append({"date": cells[0], "result": m.group(1), "candidate": m.group(2),
                     "digest": m.group(3), "ordinal": int(m.group(4)), "reviewer": cells[4],
                     "agent": agent.group(1).strip() if agent else None,
                     "context": context.group(1) if context else None})
    return rows


def _report_path(path: str) -> bool:
    """Generated projection and review reports: records that never alter the assembly."""
    return path == "TASKBOARD.md" or path.startswith("workbench/feedback/coherence/REVIEW-")


def _digest_records(repo: str, spec_id: str, commit: str) -> set[str]:
    """Paths the native content digest covers: SPEC.md, each tasks/[retired/]ID/TASK.md
    and their linked record parts. Their substantive changes move the digest."""
    folder_re = re.compile(rf"(^|/){re.escape(spec_id)}-[^/]+/")
    files = [f for f in _git(repo, "ls-tree", "-r", "--name-only", commit).stdout.splitlines()
             if folder_re.search(f)]
    specs = [f for f in files if re.search(rf"(^|/){re.escape(spec_id)}-[^/]+/SPEC\.md$", f)]
    if len(specs) != 1:
        return set()
    folder = posixpath.dirname(specs[0])
    records = {specs[0]} | {f for f in files
                            if re.fullmatch(re.escape(folder) + r"/tasks/(?:retired/)?[^/]+/TASK\.md", f)}
    parts = set()
    for record in records:
        for block in PART_BLOCK.findall(_show(repo, commit, record)):
            for link in re.findall(r"\]\(([^)\s]+)\)", block):
                parts.add(posixpath.normpath(posixpath.join(posixpath.dirname(record), link)))
    return records | (parts & set(files))


def status(spec_id: str, repo: str = ".", commit: str = "HEAD",
           digest_at: Callable[[str], str] | None = None) -> dict:
    sha = _git(repo, "rev-parse", f"{commit}^{{commit}}").stdout.strip()
    files = _git(repo, "ls-tree", "-r", "--name-only", sha).stdout.splitlines()
    spec_path = _find_spec(files, spec_id)
    built = builders(spec_id, repo, sha)
    digest_at = digest_at or native_digest(repo, spec_id)
    current_digest: str | None = None
    out = []
    for v in _verdicts(_show(repo, sha, spec_path)):
        refused = _builder_reasons(v["agent"], v["context"], built)
        stale = []
        if not FULL_SHA.match(v["candidate"]):
            stale.append(f"reviewed candidate {v['candidate']} is not a full commit SHA, so it names no exact commit")
        elif _git(repo, "cat-file", "-e", f"{v['candidate']}^{{commit}}", check=False).returncode:
            stale.append(f"reviewed commit {v['candidate']} is not in this repository")
        else:
            covered = _digest_records(repo, spec_id, v["candidate"]) | _digest_records(repo, spec_id, sha)
            changed = [p for p in _git(repo, "diff", "--name-only", v["candidate"], sha).stdout.splitlines()
                       if not (_report_path(p) or p in covered)]
            if changed:
                shown = ", ".join(changed[:5]) + (f" and {len(changed) - 5} more" if len(changed) > 5 else "")
                stale.append(f"commit changed since review: {len(changed)} path(s) differ ({shown})")
        if current_digest is None:
            current_digest = digest_at(sha)
        if current_digest[:12] != v["digest"]:
            stale.append(f"Spec content changed: reviewed digest {v['digest']}, now {current_digest[:12]}")
        unbound = [] if v["context"] else ["names no reviewing context"]
        state = ("refused" if refused else "unbound" if unbound else "stale" if stale else "current")
        out.append({**v, "status": state, "reasons": refused + unbound + stale})
    current = [v for v in out if v["status"] == "current"]
    return {"spec": spec_id, "path": spec_path, "commit": sha,
            "builders": {k: sorted(built[k]) for k in built}, "verdicts": out,
            "current": current[-1] if current else None}


def render_report(r: dict) -> str:
    rows = [f"| #{v['ordinal']} | {v['result']} | `{v['candidate'][:12]}` | {v['agent'] or 'none'} | "
            f"{v['context'] or 'none'} | **{v['status']}** | {'; '.join(v['reasons']) or 'none'} |"
            for v in r["verdicts"]]
    cur = r["current"]
    return "\n".join([
        f"# Review status: {r['spec']}",
        "",
        f"- **Spec:** `{r['path']}`",
        f"- **Commit:** `{r['commit']}`",
        f"- **Current independent verdict:** "
        + (f"#{cur['ordinal']} {cur['result']} at `{cur['candidate'][:12]}`" if cur else "none"),
        f"- **Building agents:** {', '.join(r['builders']['agents']) or 'none'}; "
        f"**contexts:** {', '.join(r['builders']['contexts']) or 'none'}",
        f"- **Check:** `uv run python -m ams.coherence.review status {r['spec']} --commit {r['commit'][:12]}` "
        "(S-013 TK-004, non-blocking)",
        "",
        "| Verdict | Result | Reviewed commit | Agent | Context | Status | Reasons |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
        "Current means the verdict's context did not build the Spec and neither the assembled commit "
        "(outside digest-covered Spec records, TASKBOARD and review reports) nor the Spec's content "
        "digest has changed since review.",
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("context", help="print this session's reviewing-context id")
    c.add_argument("--session")
    b = sub.add_parser("builders")
    b.add_argument("spec")
    b.add_argument("--commit", default="HEAD")
    r = sub.add_parser("record")
    r.add_argument("spec")
    for name in ("candidate", "result", "findings", "reviewer", "agent"):
        r.add_argument(f"--{name}", required=True)
    r.add_argument("--context")
    r.add_argument("--session")
    r.add_argument("--digest")
    s = sub.add_parser("status")
    s.add_argument("spec")
    s.add_argument("--commit", default="HEAD")
    s.add_argument("--json", action="store_true")
    s.add_argument("--write")
    a = p.parse_args(argv)
    try:
        if a.command == "context":
            ctx = context_id(a.session) if a.session else current_context()
            if not ctx:
                print("review: no session id; pass --session", file=sys.stderr)
                return 2
            print(ctx)
        elif a.command == "builders":
            found = builders(a.spec, a.repo, a.commit)
            print(json.dumps({k: sorted(v) for k, v in found.items()}, indent=2))
        elif a.command == "record":
            ctx = context_id(a.session) if a.session else a.context
            sys.stdout.write(record(a.spec, a.candidate, a.result, a.findings, a.reviewer, a.agent,
                                    context=ctx, digest=a.digest, repo=a.repo) or "")
        else:
            rep = status(a.spec, a.repo, a.commit)
            out = json.dumps(rep, indent=2) + "\n" if a.json else render_report(rep)
            if a.write:
                Path(a.write).parent.mkdir(parents=True, exist_ok=True)
                Path(a.write).write_text(out)
            sys.stdout.write(out)
    except Refused as e:
        print(f"review: refused: {e}", file=sys.stderr)
        return 1
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"review: cannot check: {getattr(e, 'stderr', '') or e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
