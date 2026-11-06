---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, AMS chat on agents ignoring project context, 2026-11-06
source_paths:
  - AGENTS.md
  - RUNBOOK.md
  - workbench/landmarks/LMK-000B-session-orientation/LANDMARK.md
  - workbench/feedback/REPORT-context-recovery-before-answer-2026-11-06.md
  - evals/session-orientation/README.md
last_verified: 2026-11-06
---

# Session orientation: agents recover intent before answering

Live state: [LMK-000B](../landmarks/LMK-000B-session-orientation/LANDMARK.md)
and its ready Task [TK-002Y](../landmarks/LMK-000B-session-orientation/tasks/TK-002Y/TASK.md).
Full evidence: the [loop report](../feedback/REPORT-context-recovery-before-answer-2026-11-06.md).

## Owner direction

Current correction (Kayden, direct AMS chat, 2026-11-06): read and follow the
RUNBOOK silently on every single start. Do not announce routine orientation.
This supersedes the earlier requirement to open replies with an Orientation
note; mandatory context recovery remains. AGENTS and RUNBOOK carry this rule.
The note-based trial criteria and results below are historical evidence for
the earlier requirement, not the current success criterion.

Source: Kayden, AMS chat, 2026-11-06, after [FAIL-132](../feedback/WORKBENCH_FEEDBACK.md).

- Agents recovering intent before answering is foundational: agents always do
  it, every session. "Foundational" describes the behavior, not a separate
  foundation file or record. AGENTS and the RUNBOOK make it an every-session
  step.
- These findings are new work. They do not belong to S-002, which builds the
  RSI loop rather than applying its repairs. LMK-000B owns them.
- Every session is work. "Work" in AGENTS meant every session; a question or a
  conversation is not exempt.
- The RUNBOOK is the operating manual that trains each new agent. Agents read
  and follow it every session. Enforce recovery through the RUNBOOK, not by
  reading alone: when agents do not follow the manual, change how it trains
  them.
- The test is that agents read and follow the RUNBOOK every time, on
  Anthropic and OpenAI models.
- Codex sessions fix the remaining Codex gap using the RUNBOOK (TK-002Y).
- S-002 being a Spec rather than a Landmark is an issue the owner raised. Not
  acted on. S-002 should close once the RSI loop is built.

## What was wrong

AMS already wrote down orientation, intent capture, one writer per record and
correction in the owning record. Agents still answered first. The same failure
class recurs on both providers: FAIL-008, 009, 017, 034, 131, 132. The causes
found:

1. The orientation rule said "Before work", and agents did not count a
   question or discussion as work. Nothing enforced it; the only tool-enforced
   rules were commits and push/merge approvals, and those were obeyed.
2. Reading was not using. FAIL-017 and FAIL-034 read the right records and
   still overrode them, because nothing made an agent show what it had found
   before proposing.
3. `align-concept`, the skill that saves confirmed intent, cannot be chosen by
   an agent (`disable-model-invocation`) and no AMS route names it, while
   `grilling` says to create no notes. Still open.
4. Each failure got a prose repair and nothing tracked recurrence of the class.
   Still open.
5. RUNBOOK pointed planners at a CONTINUE file the owner had ruled out; the
   correction lived only in one harness's private memory. Fixed.

## Earlier changes (before the silent-orientation correction)

- AGENTS: "Every session is work, including questions and discussion. Before
  your first answer or action, follow RUNBOOK, the operating manual, and open
  your first reply with its orientation note."
- RUNBOOK "Get oriented": applies to every session; read the listed records
  plus the topic's own records and failures; open the reply with
  **Orientation** (records read, what exists, owner answers, contradictions);
  this overrides answer-first style; no CONTINUE files. RUNBOOK and BLUEPRINT
  stay within the 3,000-character control limit.
- New Landmark LMK-000B owns the findings. New `ams-orientation` trial tool.

## Historical test procedure

`uv run ams-orientation run --provider claude|codex --revision REV [--overlay FILES] [--case ID] [--model M]`
([README](../../evals/session-orientation/README.md), code `src/ams/orientation_trial.py`,
tests `tests/test_orientation_trial.py`, prompts `evals/session-orientation/cases.json`).

- Each run makes a temporary detached worktree at REV, sends one owner prompt to
  a fresh read-only session, and removes the worktree.
- Claude runs: `claude -p`, `dontAsk`, read-only tools allowed. Codex runs:
  `codex exec --json -s read-only`.
- Baseline = REV. Candidate = REV plus `--overlay` of only the changed control
  files, so later records (this page, FAIL-132, the report) cannot leak the
  expected answer. Use `1e139b2` as REV to compare with the first results.
- Scoring: `readRunbook` (RUNBOOK.md opened by a tool or shell command; a
  mention in text does not count) and `orientationNote` (the final reply's
  first 300 characters contain "Orientation"). Pass needs both.
- Output: `.local/orientation-trials/` (ignored by git), one `.jsonl`
  transcript and one `.json` score per run. Read the transcripts; the score
  does not judge accuracy.
- Every run makes real model requests on the CLI's own sign-in.

## Results so far (one run per prompt)

| Model | Baseline | Candidate |
|---|---|---|
| Claude Opus 5.5 | read RUNBOOK 3/3, note 0/3 | read 3/3, note 3/3 |
| Codex gpt-6.1-sol | read 3/3, note 0/3 | read 3/3, note 0/3 ([FAIL-133](../feedback/WORKBENCH_FEEDBACK.md)) |

Claude's notes named real records and pending work. Codex reads everything and
uses recorded decisions but skips the note. Likely cause, not yet isolated:
the owner's user-level Codex instructions say to lead with the answer and avoid
rigid templates. TK-002Y tests and fixes this.

## Open

- TK-002Y's note requirement is superseded by the owner's silent-orientation
  correction; its trial criterion needs reconciliation before further use.
- Headless runs read RUNBOOK even at baseline, unlike the FAIL-132 desktop
  session. The trial does not yet cover interactive desktop sessions.
- Cause 3 (`align-concept` reachability) and cause 4 (recurrence tracking).
- Owner's S-002 Spec-versus-Landmark question.

<!-- jot-entry -->
### JOT-af08ae99-9f14-4460-9e36-0a86602052ad
Kind: intent
State: confirmed
Recorded: 2026-11-06T21:31:55.914Z
Author: Kayden
Source: Kayden, direct AMS chat instruction, 2026-11-06
Topic: session-orientation
Supersedes: none

I need you to read the runbook silently. You do it on every single start, You do not need to announce it
<!-- /jot-entry -->
