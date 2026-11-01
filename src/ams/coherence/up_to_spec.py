"""S-013 TK-002 (ADR-001F): up-to-Spec report for one Spec at one commit.

Read-only; needs only `git`. For each acceptance criterion:
  met      - line is checked AND its `Evidence:` clause names a commit SHA in the
             checked commit's history, or a path present at that commit
             (Markdown links resolve from the Spec's folder, code paths from root);
  unknown  - line is checked but no evidence resolves (a claim without proof);
  not met  - line is unchecked.
`Check:` and `Must fail:` text is planned verification, never evidence.
Done Tasks whose Destination names the criterion are listed as context only;
they do not make a criterion met (the line itself must link its evidence).

Run: uv run python -m ams.coherence.up_to_spec S-004 [--commit REF] [--write PATH]
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
import sys
from pathlib import Path

LINE = re.compile(r"^- \[(?P<mark>[ xX])\] \*\*(?P<name>.+?)\.?\*\*(?P<rest>.*)$")
EVIDENCE = re.compile(r"\*?Evidence:\*?(?P<text>.*?)(?=\*(?:Check|Must fail):|$)")
SHA = re.compile(r"\b[0-9a-f]{7,40}\b")
PATH = re.compile(r"\]\(([^)\s#]+)|`([^`\s]+/[^`\s]+|[^`\s]+\.[A-Za-z0-9]+)`")
FIELD = lambda name: re.compile(rf"^\*\*{name}:\*\*\s*(.*)$", re.M)


def _git(repo: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, check=check, capture_output=True, text=True)


def _show(repo: str, commit: str, path: str) -> str:
    return _git(repo, "show", f"{commit}:{path}").stdout


def _resolves_commit(repo: str, sha: str, commit: str) -> bool:
    # Evidence must be delivered: the SHA has to be in the checked commit's history,
    # not merely exist in the object store (e.g. on an unmerged branch).
    if _git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode:
        return False
    return _git(repo, "merge-base", "--is-ancestor", sha, commit, check=False).returncode == 0


def _resolves_path(repo: str, commit: str, path: str) -> bool:
    return _git(repo, "cat-file", "-e", f"{commit}:{path}", check=False).returncode == 0


def _normalize(path: str, base: str = "") -> str | None:
    """Repo-relative POSIX path, or None if it escapes the repository."""
    joined = posixpath.normpath(posixpath.join(base, path.lstrip("/") if not base else path))
    return None if joined.startswith("..") or joined == "." else joined


def _find_spec(files: list[str], spec_id: str) -> str:
    hits = [f for f in files if re.search(rf"(^|/){re.escape(spec_id)}-[^/]+/SPEC\.md$", f)]
    if len(hits) != 1:
        raise ValueError(f"{spec_id}: expected one SPEC.md, found {len(hits)}")
    return hits[0]


def _section(text: str, heading: str) -> list[str]:
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == f"## {heading}"
            continue
        if inside:
            out.append(line)
    return out


def _evidence(repo: str, commit: str, rest: str, spec_dir: str) -> list[str]:
    m = EVIDENCE.search(rest)
    if not m:
        return []
    text, found = m.group("text"), []
    for link, code in PATH.findall(text):
        if code and SHA.fullmatch(code):
            continue
        # Markdown links resolve relative to the Spec (as a renderer would);
        # backticked code paths are repository-root relative.
        path = _normalize(link, spec_dir) if link else _normalize(code)
        if path and _resolves_path(repo, commit, path):
            found.append(path)
    for sha in SHA.findall(text):
        if _resolves_commit(repo, sha, commit):
            found.append(sha)
    return found


def _tasks(repo: str, commit: str, files: list[str], spec_path: str) -> list[dict]:
    root = spec_path.rsplit("/", 1)[0] + "/tasks/"
    tasks = []
    for f in sorted(x for x in files if x.startswith(root) and x.endswith("/TASK.md")):
        body = _show(repo, commit, f)
        get = lambda n: (FIELD(n).search(body) or [None, ""])[1].strip()
        dest = get("Destination").removeprefix("spec-acceptance:").strip()
        tasks.append({"id": get("Task ID"), "status": get("Status"), "proof": get("Proof") or None,
                      "destinations": [d.strip().rstrip(".") for d in dest.split(";") if d.strip()]})
    return tasks


def check_spec(spec_id: str, repo: str = ".", commit: str = "HEAD") -> dict:
    sha = _git(repo, "rev-parse", f"{commit}^{{commit}}").stdout.strip()
    files = _git(repo, "ls-tree", "-r", "--name-only", sha).stdout.splitlines()
    spec_path = _find_spec(files, spec_id)
    tasks = _tasks(repo, sha, files, spec_path)
    criteria = []
    for line in _section(_show(repo, sha, spec_path), "Acceptance Criteria"):
        m = LINE.match(line.strip())
        if not m:
            continue
        name, checked = m.group("name").strip(), m.group("mark") != " "
        evidence = _evidence(repo, sha, m.group("rest"), posixpath.dirname(spec_path)) if checked else []
        status = "not met" if not checked else ("met" if evidence else "unknown")
        related = [{"id": t["id"], "status": t["status"], "proof": t["proof"]}
                   for t in tasks if name in t["destinations"]]
        criteria.append({"name": name, "checked": checked, "status": status,
                         "evidence": evidence, "tasks": related})
    summary = {k: sum(c["status"] == k for c in criteria) for k in ("met", "not met", "unknown")}
    return {"spec": spec_id, "path": spec_path, "commit": sha, "criteria": criteria, "summary": summary}


def render_report(r: dict) -> str:
    s = r["summary"]
    rows = []
    for c in r["criteria"]:
        ev = ", ".join(f"`{e}`" for e in c["evidence"]) or "none"
        tk = ", ".join(f"{t['id']} ({t['status']})" for t in c["tasks"]) or "none"
        rows.append(f"| {c['name']} | {c['status']} | {ev} | {tk} |")
    unmet = [c["name"] for c in r["criteria"] if c["status"] != "met"]
    return "\n".join([
        f"# Up-to-Spec report: {r['spec']}",
        "",
        f"- **Spec:** `{r['path']}`",
        f"- **Commit:** `{r['commit']}`",
        f"- **Summary:** {s['met']} met, {s['not met']} not met, {s['unknown']} unknown",
        f"- **Unmet or unknown:** {', '.join(unmet) or 'none'}",
        f"- **Check:** `uv run python -m ams.coherence.up_to_spec {r['spec']} --commit {r['commit'][:12]}` (S-013 TK-002, non-blocking)",
        "",
        "| Criterion | Status | Evidence resolved at commit | Related Tasks (context only) |",
        "|---|---|---|---|",
        *rows,
        "",
        "Met requires a checked line whose `Evidence:` clause names a SHA or path that resolves at the commit. "
        "Checked without resolvable evidence is unknown; unchecked is not met. Task status never makes a line met.",
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("spec")
    p.add_argument("--repo", default=".")
    p.add_argument("--commit", default="HEAD")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write")
    a = p.parse_args(argv)
    try:
        r = check_spec(a.spec, a.repo, a.commit)
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"up_to_spec: cannot check: {getattr(e, 'stderr', '') or e}", file=sys.stderr)
        return 2
    out = json.dumps(r, indent=2) + "\n" if a.json else render_report(r)
    if a.write:
        Path(a.write).parent.mkdir(parents=True, exist_ok=True)
        Path(a.write).write_text(out)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
