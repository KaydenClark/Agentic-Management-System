# Context recovery before answering: improve-workbench loop, pass 1

Failure entry: [FAIL-132](WORKBENCH_FEEDBACK.md). Recurring class: FAIL-008,
FAIL-009, FAIL-017, FAIL-034, FAIL-131; adjacent FAIL-014 and FAIL-018.

## Target And Scope

- Target: AMS room at `1e139b2` on `Feature/S-000D-wiki-memory`, the room's
  own controls (AGENTS, RUNBOOK, `workbench/docs/SKILLS.md`) plus the
  personal-catalog skills they route to. Room-owned and catalog-owned parts
  are named per finding.
- Question: the owner has written down orientation, intent capture, one
  writer per record and correction-in-owner rules. Why do agents still answer
  or propose before recovering them?
- Method: improve-workbench steps 1–3 (read-only). No control was changed.
- Owning Spec: pending. No current Spec owns "agents recover owner intent
  before answering". Candidates are S-002 (RSI loop) and S-000A (skills
  refocus); the owner chooses.

### Job contract

| Field | Value |
|---|---|
| Job | A fresh session receives an owner question about the project, not an assigned Task. Reproduction input: the opening owner message of the FAIL-132 session (why agents ignore project context and how to fix it). |
| Accepted outcome | The first substantive reply recovers and cites the AMS records relevant to the question (controls, settled answers, failure history), names contradictions, and proposes nothing that duplicates an existing record without saying so. |
| Evidence of outcome | The first reply's transcript: which records it cites and whether the owner has to correct it. |
| Worker | claude-opus-5-5, Claude Code desktop, default AMS controls, personal skill catalog as installed. |
| Authority | The owner said "Log it and start": log the failure and run the read-only loop steps. Changing a control, running fresh workers and paid trials each need further owner scope. |
| Outside state | None material; the job reads only local records. |
| Suspected gap | The orientation trigger does not fire for questions or conversation, and nothing makes recovered context visible before a proposal. |

## Evidence And Limitations

### Baseline: this session's first reply (observed)

- Loaded automatically: CLAUDE.md → AGENTS.md (21 lines), the agent's own
  memory index, and a SessionStart git save-guard message.
- Read before answering: file and word counts across `workbench/`, the first
  60 lines of `workbench/wiki/MEMORY.md`, one stopped report's first 30 lines,
  and commit-date counts.
- Not read: RUNBOOK "Get oriented", SKILLS, ARCHITECTURE, GLOSSARY, the
  trackers and the failure log, even though AGENTS says "Before work, follow
  RUNBOOK…".
- Result: recommended five generic practices that AMS already defines, then
  proposed a new intent page and AGENTS rule. The owner had to say that all
  five exist. Outcome not reached; one owner correction round.
- Worker self-report (uncorroborated): it treated the message as a general
  question rather than "work", so it did not apply the orientation rule.

### Historical recurrences (recorded evidence, not reruns)

The same class appears in rows from both providers: FAIL-008 (coordination),
FAIL-009 and FAIL-034 (grilling), FAIL-017 (proposal "despite reading
routes"), FAIL-131 (dashboard interview, OpenAI). FAIL-034 (Anthropic) also
recommended a new criterion "despite having read" the existing contract. Most
are conversational or planning activities rather than Task implementation.

### Measures before any change

`node workbench/tools/spec-workbench.mjs doctor` after `git fetch`: ok, no
blocking finding. Attention findings include three stale claims (S-002, S-006,
S-011) and `permission-scope-drift`: `.claude/settings.json` has no Edit allow
rule for the docs, specs, wiki, sessions or feedback lanes. Inference, not
tested: Claude agents meet a permission prompt when they try to capture intent
in exactly the lanes that hold it.

### Limits

One observed run plus historical rows. No fresh rerun has happened. The
worker's account of why it skipped orientation is self-report. No
worker-limitation conclusion is drawn.

## Findings

### F-1 — Orientation is triggered by "work", and questions are not treated as work

- Severity: high. Kind: context (trigger never fires). Owner: AMS `AGENTS.md`.
- Location: AGENTS "Start and scope": "Before work, follow RUNBOOK…".
- Claim: the always-loaded rule is a pointer whose trigger is "work". In
  FAIL-132 the worker classified an owner question as not-work and never
  reached RUNBOOK's seven-document reading list. No hook or tool enforces
  orientation; the project's only hook is the Stop commit guard. The rules
  that agents reliably obey are the tool-enforced ones (commit guard, push and
  merge approval review: FAIL-044, 069, 079, 114).
- Smallest next action: see Intervention.
- Disposition: pending (owning Spec not chosen).

### F-2 — The intent-capturing alignment skill is unreachable in ordinary conversation

- Severity: high. Kind: ownership and capability discovery. Owners: AMS
  `workbench/docs/SKILLS.md` (route) and the personal catalog's
  `align-concept` (invocation).
- Claim: `align-concept` is the skill that interviews, saves the confirmed
  readback and resumes without re-asking. It has
  `disable-model-invocation: true`, so an agent cannot choose it, and AGENTS,
  RUNBOOK, SKILLS and GLOSSARY never name it. The SKILLS operation map has no
  row for discussing or aligning owner intent. A conversation therefore routes
  to nothing, or to `grilling`, which says to "create no notes, Wiki, glossary
  or project docs automatically". The interview stays in chat, the session
  ends and the next session cannot recover it. This fits the owner's report
  that agents did not write down what the owner wanted. Inference from source,
  not yet rerun.
- Smallest next action: add an alignment row to the SKILLS operation map.
  Separately, decide whether `align-concept` should allow model invocation
  (a catalog change through author-skill; the owner installs it).
- Disposition: pending.

### F-3 — An owner correction lives only in one harness's private memory and contradicts RUNBOOK

- Severity: medium. Kind: ownership (competing representations). Owner:
  `RUNBOOK.md`.
- Claim: RUNBOOK line 8 tells planners to read `AMS/CONTINUE.md` on a private
  branch. The owner's correction against CONTINUE-style handoff files and
  pointers exists only in Claude Code's per-user memory, not in any AMS
  record. Claude agents see both and must pick one; Codex agents see only
  RUNBOOK. This breaks AGENTS' rule to capture corrections in their owner.
- Smallest next action: with the owner's confirmation, record the correction
  in the owning Wiki topic and remove the RUNBOOK pointer. This corrects a
  wrong control rather than claiming an improvement.
- Disposition: pending.

### F-4 — Failure repairs add prose, and nothing checks whether a class recurs

- Severity: medium. Kind: feedback. Owner: the failure log's recording rules
  and the RSI loop Spec.
- Claim: the FAIL-017 repair was a SKILLS paragraph that states it is "not
  proof that the systemic failure is fixed". The same class recurred at
  FAIL-034, FAIL-131 and FAIL-132. The log links each row's repair but has no
  way to see that one class has recurred across rows, so each recurrence gets
  another local repair.
- Smallest next action: none in this pass; record as an input to the owning
  Spec's loop design.
- Disposition: pending.

## Intervention (step 3; not applied)

```text
Change: replace AGENTS "Before work, follow RUNBOOK#get-oriented, the assigned
  Spec/Task and SKILLS." with one sentence of the same length that also covers
  owner questions and makes recovery visible, for example: "Before answering
  about this project or starting work, recover the relevant records, settled
  answers and failures (RUNBOOK#get-oriented, assigned Spec/Task, SKILLS), cite
  them first and name contradictions."
Prediction: the same worker, given the FAIL-132 opening message in a fresh
  worktree, will cite AGENTS/RUNBOOK/SKILLS and the failure log in its first
  reply and diagnose why existing rules are not followed instead of listing
  generic practices, because the always-loaded trigger now covers questions and
  the citation requirement makes skipped recovery visible to the owner at once.
Would support it: first reply cites at least the existing orientation and
  intent-capture controls and the recurring FAIL rows; no owner correction is
  needed to reach the diagnosis.
Would weaken it: the reply still answers generically, or cites files but
  still proposes a parallel artifact (reading without using, as in FAIL-017
  and FAIL-034); or the run-without-change control also succeeds.
Carrying cost: one sentence in an always-loaded file, kept by the owner/root.
  It adds reading to short questions.
```

F-2 and F-3 are separate interventions. Keeping them out of this pass keeps
the prediction readable.

## Pass 1 change and trial results (2026-11-06)

Owner direction after step 3 ([context](../wiki/context-session-orientation.md#owner-direction)):
the findings belong to new Landmark LMK-000B, not S-002; every session is work;
enforce recovery through the RUNBOOK; test on Anthropic and OpenAI models.
Applied: the AGENTS line now covers every session including questions, and
RUNBOOK "Get oriented" requires a first-reply **Orientation** note that
overrides answer-first style, with the CONTINUE pointer removed. Both stay
within the 3,000-character control budget.

Trial: `ams-orientation` ([README](../../evals/session-orientation/README.md)),
3 prompts, read-only sessions in temporary worktrees at `1e139b2`. Candidate =
`1e139b2` plus the changed AGENTS.md and RUNBOOK.md only, so FAIL-132 and this
report were not visible to workers. One run per prompt and condition.

| Provider / model | Condition | Read RUNBOOK | Orientation note |
|---|---|---|---|
| Anthropic claude-opus-5-5, Claude Code `-p` | baseline | 3/3 | 0/3 |
| Anthropic claude-opus-5-5 | candidate, final RUNBOOK | 3/3 | 3/3 |
| OpenAI gpt-6.1-sol (configured default), Codex exec | baseline | 3/3 | 0/3 |
| OpenAI gpt-6.1-sol | candidate, final RUNBOOK | 3/3 | 0/3 |

An earlier, longer candidate RUNBOOK gave the same split (Claude 3/3 notes,
Codex 0/3).

Observations from reading the transcripts:

- Headless sessions on both providers read RUNBOOK even at baseline. This
  differs from FAIL-132's interactive desktop session, which did not. The
  trial does not reproduce the desktop condition; that gap stays open.
- Codex reads every listed record and its answers use recorded owner
  decisions (for example, the next-work answer recovers the settled dashboard
  readback). It skips only the visible note. The owner's user-level Codex
  instructions say "Lead with the answer" and "Do not force responses into
  rigid templates", and they outweigh the RUNBOOK's override line. Inference
  from instructions and outputs; not isolated by a run without that file.
- One Claude candidate run cited the overlay commit's title, "Orientation
  trial overlay", which hinted at the change. The harness now uses a neutral
  commit message. Results above are not rerun for that.

Decision: retain the AGENTS and RUNBOOK change provisionally for Anthropic.
For OpenAI the prediction failed; the next owner choice is whether the
user-level Codex instructions should defer to a project's RUNBOOK
orientation. Reconsider if Claude notes stop appearing in desktop sessions or
repeated runs. One run per cell supports this job only, not a general claim.

## Challenged Or Rejected Findings

- "Record volume alone causes the failure": weakened. FAIL-017 and FAIL-034
  read the relevant routes and still overrode them, so loading more or less
  text is not sufficient by itself.
- "Worker limitation": not concluded. The class spans Anthropic and OpenAI
  workers, which points toward the environment, but one run cannot separate
  the two.

## Next Action And Open Questions

1. Owner chooses the owning Spec for these findings (S-002, S-000A or a new
   one through map).
2. Owner authorizes the F-1 control change (step 4).
3. Owner authorizes two fresh runs (step 5), same worker and prompt: one at
   `1e139b2` plus only the AGENTS change, and one at `1e139b2` unchanged as the
   run without the change. Both candidates must exclude FAIL-132 and this
   report, because these records name the expected answer and would confound
   the rerun.
4. Decide F-2 (alignment route and invocation) and F-3 (CONTINUE correction).

## Review Boundary

Self-authored by the failed actor. Not independently reviewed. A
separate-context reviewer should challenge F-1 and F-2 before any repair is
retained.

## Models And Evidence States

- evaluated_model: claude-opus-5-5, Claude Code desktop (FAIL-132); historical
  rows as recorded. reviewer_model: none.
- Evidence states: F-1 is observed use (one run) plus source inspection. F-2
  and F-3 are source inspection. F-4 is recorded history. No behavioral test
  or repeated outcome trial has been run.
- Skill copies read: the installed Claude Code personal-catalog copies of
  `align-concept`, `grilling` and `improve-workbench` (source commit not
  checked).
