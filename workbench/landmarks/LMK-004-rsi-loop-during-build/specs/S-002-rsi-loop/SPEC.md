# S-002 - RSI loop with safeguards

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The measured self-improvement loop: the site build as the first trial, then rounds that start from failed results, under safeguards that keep the numbers honest.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** Activated 2026-11-01 under the owner's six-active-Spec approval; four Tasks planned, seeding first.
**Next gate:** S-006 rows for TK-001; the owner's standing campaign approval before TK-002.

## Intent and authority

The owner's aim is to build the whole thing and then loop. The first trial is the whole build; then the loop repeats until the owner's token meter is spent or a stop rule fires. The owner confirmed building the safeguards in from the start.

## Outcome

Each change to a runtime, control or skill is tested on fixed tasks against the current version and against controls, and ends in rows plus a disposition. The site shows the result either way.

## Why It Matters

Outside research does not settle whether shaping an agent's environment improves results. Without controls, noise and grader independence, a loop can report improvement that is not there.

## Current Verified State

- The loop runner and fixed eval task set are not implemented. S-006 has the RSI writer and live tables, but the 2026-11-01 read-only check found 0 non-test runs/results. The owner's reported completed baseline has not yet been located; no baseline score is inferred.
- Loop #1 now includes fitness level, Alignment Score, Stable/Excellent-only acceptance, an initial attempt plus at most two retries, Supabase results and visibility on the Vercel dev site. The exact owner wording, recovered sources, proposed scoring/counter interpretation and unanswered questions are in [the existing RSI context](../../../../wiki/context-ams-purpose.md#loop-1-preparation-recovered-design-and-open-decisions). Preparation is authorized; no paid-campaign limit or assessment result is supplied by this record.

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

- S-006 for rows; sandboxed run hosts.
- Open owner choice `rsi-campaign-approval`: the one standing campaign approval (budget and stop condition) before any paid trial run. The build readback approval of 2026-11-01 authorizes building the loop, not its spend.
- Seed sources are real only: this build's own history (S-006 build-history rows) and the before/after notes the owner's skills repository records. That repository is private, so a row carries a summary and a commit pointer, never its text.

## Vertical Implementation Slices

Each Task is one fresh-session run in orchestrator B's local lane, landed feature -> `main` through a checked PR. Stack: task set and graders under `evals/`, a Python runner in a sandbox, the S-006 writer, Supabase rows, and queries over them.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Real, labeled seeds.** Every seed row names a real source (a build-history row, or a skills-repository commit) and the strength it supports; the build alone is one uncontrolled trial. *Must fail:* a seed row with no source, or a before/after note shown as measured improvement.
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
| 2026-11-01 | none | Owner requested Loop #1 preparation and the first improvement wave, with fitness/alignment results, Stable/Excellent-only acceptance and a three-attempt stop. Captured source and interview frontier in the linked RSI context. | Read-only Supabase counts; dev source and READY deployment metadata inspected | Current Verified State; existing RSI context | Baseline artifact/findings; campaign scoring/counter answers; paid budget if needed; Supabase-to-site reader and actual trials |

## Review and Human QA

Each retained change gets independent review; the owner judges whether a manual round is worth automating.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- The retro improvement loop needs its own improvement before it is used in force.

## Supersession

- Supersedes: none
- Superseded by: none
