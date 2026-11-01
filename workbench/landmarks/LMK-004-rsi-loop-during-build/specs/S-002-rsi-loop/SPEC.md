# S-002 - RSI loop with safeguards

**Spec ID:** S-002
**Status:** planned
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The measured self-improvement loop: the site build as the first trial, then rounds that start from failed results, under safeguards that keep the numbers honest.
**Blockers:** none
**Latest event:** Mapped from the earlier loop proposal and the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning; the owner's one standing campaign approval before paid trial runs.

## Intent and authority

The owner's aim is to build the whole thing and then loop. The first trial is the whole build; then the loop repeats until the owner's token meter is spent or a stop rule fires. The owner confirmed building the safeguards in from the start.

## Outcome

Each change to a runtime, control or skill is tested on fixed tasks against the current version and against controls, and ends in rows plus a disposition. The site shows the result either way.

## Why It Matters

Outside research does not settle whether shaping an agent's environment improves results. Without controls, noise and grader independence, a loop can report improvement that is not there.

## Current Verified State

- No loop, tasks, graders or rows exist in this repository. The data store is S-006.

## Desired Behavior

One round: select the failing tasks; analyze the failed runs and name the earliest gap and its single owner; propose one change with its expected movement; implement it (skills through the skills repository's own process); rerun the same tasks against the current version; dispose as retain, revise (variant) or remove; write rows and the disposition to Supabase.

Safeguards, each required:

1. **Start from failure.** A round starts only from a failed result. Retro findings are for the owner and do not start rounds yet.
2. **Noise floor.** A version is run against itself before any change is trusted.
3. **Control arms.** No-AMS and plain-instruction arms run alongside the AMS arm.
4. **Paired statistics** per task, with intervals.
5. **Full rows.** Cost, tokens and completed state on every row.
6. **Independent graders** taken from the accepted version, never the candidate's.
7. **Sandboxed trials**, never with permission checks skipped.
8. **Held-out before public.** More than two held-out tasks before any public number.
9. **Retire studied held-out tasks** once their failures have been studied.
10. **One standing campaign approval** from the owner instead of a spend approval each round.
11. **Skills pinned per run.** Each run records the skills commit it used.
12. **Three strikes.** A run, a failed test, a second failed test, then stop and report.
13. **Repeat failures.** A failure seen twice is first checked for an earlier fix that did not work.

## Decisions And Contracts

- One improvement procedure; one change per version.
- Same provider, model and effort within a comparison.
- No automated proposer until a trusted grader, a measured cost per trial and an owner-judged manual round exist.

## Non-Goals

- Changing model weights.
- Presenting results (S-007).

## Dependencies And Blockers

- S-006 for rows; the standing campaign approval; sandboxed run hosts.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Register the site build as the first trial and write its rows with skills pin, cost and tokens | ready | none | pending |
| TK-002 | Noise-floor run of one version against itself on a small task set | ready | TK-001 | pending |
| TK-003 | Control arms and paired per-task statistics on the same tasks | ready | TK-002 | pending |
| TK-004 | One full round from a failed result to a recorded disposition | ready | TK-003 | pending |

### TK-001 - First trial rows

**Stance:** Builder

Proves the full-rows and pin criteria.

### TK-002 - Noise floor

**Stance:** Builder

Proves the noise-floor criterion.

### TK-003 - Controls

**Stance:** Builder

Proves the control and statistics criteria.

### TK-004 - First round

**Stance:** Builder

Proves the round and disposition criteria.

## Acceptance Criteria

- [ ] **Full rows.** Every row has cost, tokens, completed state, arm, version and skills commit. *Must fail:* a row missing its skills pin.
- [ ] **Noise floor first.** A comparison is reported only after a same-version run sets the noise floor. *Must fail:* a lift smaller than the floor shown as improvement.
- [ ] **Controls run.** Each round has no-AMS and plain-instruction rows on the same tasks. *Must fail:* a round with only the AMS arm.
- [ ] **Graders independent.** The grader commit differs from the candidate and equals the accepted version's. *Must fail:* a candidate graded by its own changed grader.
- [ ] **Sandboxed.** Trials run without skipped permission checks. *Must fail:* a trial log showing them skipped.
- [ ] **Public numbers gated.** No public number until more than two held-out tasks have rows. *Must fail:* a headline from two tasks.
- [ ] **Starts from failure.** Every round names the failed row it started from. *Must fail:* a round started from a retro idea.
- [ ] **Stops.** After two failed fixes for one event the loop stops and reports. *Must fail:* a fourth attempt.

## RSI and website connection

This is the loop. S-006 stores its rows and S-007 presents them.

## Testing Seams

- The round runner on a fixture task with a known pass and fail; queries over the written rows.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-002
# runner and test commands named at Task planning
```

## Documentation Impact

- RUNBOOK names the run, inspect and measure commands the graders call.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion; campaign approval |

## Review and Human QA

Each retained change gets independent review; the owner judges whether a manual round is worth automating.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- The retro improvement loop needs its own improvement before it is used in force.

## Supersession

- Supersedes: none
- Superseded by: none
