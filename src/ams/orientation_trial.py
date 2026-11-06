"""Session-orientation trial: does a fresh session follow the RUNBOOK before answering (LMK-000B)?

Each run starts a read-only Claude Code or Codex session in a temporary detached
worktree at a chosen revision, sends one owner prompt and keeps the event stream.
Scoring reads only observable behavior: whether the session opened RUNBOOK.md
and whether its final reply opens with the RUNBOOK's Orientation note. It does
not judge answer quality; read the transcript for that.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CASES = Path(__file__).resolve().parents[2] / "evals" / "session-orientation" / "cases.json"
NOTE_WINDOW = 300
CLAUDE_TOOLS = ["Read", "Glob", "Grep", "Bash(git status:*)", "Bash(git log:*)", "Bash(git branch:*)",
                "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(sed -n:*)", "Bash(grep:*)",
                "Bash(wc:*)", "Bash(node workbench/tools/spec-workbench.mjs:*)"]


def load_cases(path=CASES):
    return json.loads(Path(path).read_text())["cases"]


def _events(stream):
    for line in stream.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _claude(stream):
    reads, answer, model = [], "", None
    for event in _events(stream):
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            model = event.get("model")
        elif kind == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    reads.append(json.dumps(block.get("input", {})))
        elif kind == "result":
            answer = event.get("result") or ""
    return reads, answer, model


def _codex(stream):
    reads, messages = [], []
    for event in _events(stream):
        item = event.get("item", {})
        if event.get("type") != "item.completed":
            continue
        if item.get("type") == "command_execution":
            reads.append(item.get("command", ""))
        elif item.get("type") == "agent_message":
            messages.append(item.get("text", ""))
    return reads, (messages[-1] if messages else ""), None


def score(provider, stream):
    reads, answer, model = (_claude if provider == "claude" else _codex)(stream)
    read_runbook = any("RUNBOOK.md" in read for read in reads)
    note = "orientation" in answer.lstrip()[:NOTE_WINDOW].lower()
    return {"provider": provider, "model": model, "toolCalls": len(reads),
            "readRunbook": read_runbook, "orientationNote": note,
            "passed": read_runbook and note, "finalAnswer": answer}


def command(provider, prompt, worktree, model=None):
    if provider == "claude":
        args = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
                "--no-session-persistence", "--permission-mode", "dontAsk",
                "--allowedTools", *CLAUDE_TOOLS]
        return args + (["--model", model] if model else [])
    args = ["codex", "exec", "--json", "-s", "read-only", "-C", str(worktree)]
    return args + (["-m", model] if model else []) + [prompt]


def run(provider, revision, case, out, *, overlay=(), model=None, repo=Path.cwd()):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{stamp}-{provider}-{case['id']}-{revision[:12]}{'-overlay' if overlay else ''}"
    base = Path(tempfile.mkdtemp(prefix="ams-orientation-"))
    worktree = base / "AMS"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "--detach", "-q", str(worktree), revision], check=True)
    try:
        for path in overlay:
            shutil.copyfile(repo / path, worktree / path)
        if overlay:
            subprocess.run(["git", "-C", str(worktree), "commit", "-qam", "Orientation trial overlay"], check=True)
        proc = subprocess.run(command(provider, case["prompt"], worktree, model), cwd=worktree,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1800)
    finally:
        subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(worktree)], check=False)
        shutil.rmtree(base, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{run_id}.jsonl").write_text(proc.stdout)
    result = score(provider, proc.stdout)
    result.update({"runId": run_id, "case": case["id"], "revision": revision, "overlay": list(overlay),
                   "requestedModel": model, "exitCode": proc.returncode})
    (out / f"{run_id}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ams-orientation", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    go = sub.add_parser("run", help="run one or more cases (makes model requests)")
    go.add_argument("--provider", choices=["claude", "codex"], required=True)
    go.add_argument("--revision", required=True, help="git revision the worker starts from")
    go.add_argument("--overlay", nargs="*", default=[], help="files copied from this checkout onto the revision")
    go.add_argument("--case", action="append", help="case id (default: all)")
    go.add_argument("--model", help="model override; default is the CLI's configured model")
    go.add_argument("--out", type=Path, default=Path(".local/orientation-trials"))
    again = sub.add_parser("score", help="re-score a saved event stream")
    again.add_argument("--provider", choices=["claude", "codex"], required=True)
    again.add_argument("stream", type=Path)
    args = parser.parse_args(argv)
    if args.cmd == "score":
        result = score(args.provider, args.stream.read_text())
        print(json.dumps({k: v for k, v in result.items() if k != "finalAnswer"}))
        return 0
    revision = subprocess.run(["git", "rev-parse", args.revision], capture_output=True, text=True, check=True).stdout.strip()
    cases = [c for c in load_cases() if not args.case or c["id"] in args.case]
    for case in cases:
        result = run(args.provider, revision, case, args.out, overlay=args.overlay, model=args.model)
        print(json.dumps({k: v for k, v in result.items() if k != "finalAnswer"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
