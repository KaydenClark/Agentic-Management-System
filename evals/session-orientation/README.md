# Session-orientation trial

Owner: [LMK-000B](../../workbench/landmarks/LMK-000B-session-orientation/LANDMARK.md).
Question: does a fresh session follow the [RUNBOOK](../../RUNBOOK.md#get-oriented)
before its first answer, on both Anthropic and OpenAI models?

Each run starts a read-only session in a temporary detached worktree, sends one
owner prompt from [cases.json](cases.json), keeps the raw event stream and
scores two observable facts:

- `readRunbook`: the session opened `RUNBOOK.md` with a tool or shell command.
  Mentioning it in text does not count.
- `orientationNote`: the final reply opens (first 300 characters) with the
  RUNBOOK's Orientation note.

A run passes when both hold. The scorer does not judge whether the note is
accurate or the answer good; read the transcript for that.

```bash
uv run ams-orientation run --provider claude --revision BASE
uv run ams-orientation run --provider claude --revision BASE --overlay AGENTS.md RUNBOOK.md
uv run ams-orientation run --provider codex --revision BASE --case next-work
uv run ams-orientation run --provider codex --revision BASE --model MODEL
uv run ams-orientation score --provider claude .local/orientation-trials/RUN.jsonl
```

`--overlay` copies the named files from this checkout onto the revision, so a
candidate can test changed controls without later records that describe the
expected answer. Results and transcripts go to `.local/orientation-trials/`
(ignored by git).

Every `run` makes real model requests on the CLI's own sign-in. Claude runs use
`dontAsk` with read-only tools allowed; Codex runs use its `read-only` sandbox.
User-level settings, skills and hooks still load, as in a normal session.
