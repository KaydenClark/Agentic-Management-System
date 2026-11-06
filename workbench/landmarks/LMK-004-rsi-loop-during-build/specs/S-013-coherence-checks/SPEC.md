# S-013 - Coherence checks

**Spec ID:** S-013
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator C (Coherence, cloud, no secrets)
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Coherence checks: Spec fidelity, pinned/current skills, dev/main drift and independent review.
**Blockers:** none
**Confirmation:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-003.

## Intent and authority

The [owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-55876e5d-6957-4a4e-917b-8ba7245adee2) authorizes Map/Plan preparation; implementation and trial holds remain.

Owner requires Spec fidelity and measured dev/main distance to prevent another long-unmerged trunk. Orchestrator C works in the cloud through GitHub only, holds no secrets and writes no product code.

## Outcome

Readers see Spec fidelity, pinned/current skills per run and dev/main distance. An independent context reviews each Spec.

## Why It Matters

An earlier Workbench accumulated thousands of unmerged commits and stale records. Catch drift before recovery becomes costly.

## Current Verified State

No criterion is verified. Legacy Review returned `b7efbaba15baa354eafbc92b91a352ae54d94c71` for incomplete accounting/control routes; [TK-001X](tasks/TK-001X/TASK.md) owns correction. [TK-001U](tasks/TK-001U/TASK.md) retains dev-recovery evidence, not complete detection/learning. [TK-001D](tasks/TK-001D/TASK.md#receipt) now records bounded synthetic detection/replay; real native loading/use and whole-Spec acceptance remain open.

Drift/report: [TK-001](tasks/TK-001/TASK.md#receipt); breach card waits on [TK-005](tasks/TK-005/TASK.md). Up-to-Spec/S-004: [TK-002](tasks/TK-002/TASK.md#receipt). Skills sync [TK-003](tasks/TK-003/TASK.md) waits on S-006. Review tooling [TK-004](tasks/TK-004/TASK.md#receipt) remains outside the native verdict gate. Secret-free execution is unproved. Doctor remains structural; dev exists. RUNBOOK now routes to the detection procedure.

History: [S-013 history](../../../../wiki/history/S-013.md).

## Desired Behavior

- **Up to Spec.** For each active Spec, compare delivered behavior on `main` or `dev` with its acceptance criteria and report gaps.
- **Skills pinned and in sync.** Every RSI row names a skills commit; report rows whose commit is behind the current skills `main` and sessions that could not install skills.
- **`dev` ahead of `main`.** Report commits and days `dev` is ahead of `main`, with a threshold that raises a Grill Board item.
- **Independent Spec review.** A fresh-context reviewer passes or returns the exact assembled commit against the Spec's conditions; a changed commit needs a fresh review.
- Reports are committed records; findings are visible, never silently fixed.
- **Preparation routing.** Detect a large shared-skill or other AMS change proceeding without its Map/Plan or past a Prepare stop. Route the [recorded failure](../../../../feedback/REPORT-skills-workbench-bypass-2026-11-02.md) and recurrence to [S-000A](../S-000A-skills-refocus/SPEC.md) for source repair; check preparation before claiming a reliability improvement. This addition is preparation only.

### Failure detection and use evidence

Detect and route observed mismatches before owner prompting, preserving a separate occurrence for each recurrence. Link detection to the existing failure intake and S-006 safe identities; classify suspected cause without asserting skill causation from involvement alone. Count eligible successful uses alongside failures for later recurrence measurement.

Distinguish accepted source version, installed bytes, actual host loading and observed use. A deliberately pinned baseline is not an accidental stale installation; report the condition rather than silently upgrading a comparison. S-000B owns recovery; S-002 qualification/retention. Installation needs separate authority; C stays secret-free.

## Decisions And Contracts

- C holds no secrets and writes no product code; it reads through GitHub and writes reports.
- A check blocks only what it evaluates and never blocks its own repair.
- A new check starts non-blocking and blocks only after it has proven stable.

## Non-Goals

- Merging `dev` -> `main`; that is the owner's.
- Fixing product code.

## Dependencies And Blockers

- None to start. The skills-row check needs S-006 rows (read with the publishable key, which is not a secret); the Grill Board item needs S-004's card format.
- Reports live in `workbench/feedback/coherence/`.

## Vertical Implementation Slices

Each Task uses C's fresh cloud context (GitHub only, no secrets), targeting checked feature -> main. Stack: read-only check, Git/GitHub reads, committed report and fixture-repository tests.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Feedback loop connection:** Detection closes the reporting gap: an orchestrator exercises acceptance beyond green checks, records an unreported mismatch with source/candidate identity, assigns its existing owner and next action, and preserves recurrence. A planted failure that reaches completion without a finding must fail.
- [ ] **Prepare boundary:** TK-001D detects and routes a planted missing-Map/Plan or Prepare-stop bypass, including cross-repository skill work, before owner intervention. A document reminder alone fails.

- [ ] **Drift measured.** The report gives commits and days `dev` is ahead of `main` at a named time, and a threshold breach creates a Grill Board item. *Must fail:* a breach with no item.
- [ ] **Up to Spec.** The report lists each unmet criterion of the checked Spec with evidence. *Must fail:* a criterion reported met with no evidence.
- [ ] **Skills in sync.** Rows without a skills commit, or behind the current skills `main`, are listed. *Must fail:* an unpinned row passing.
- [ ] **Independent review.** A review names its exact commit and comes from a context that did not build the Spec. *Must fail:* a review by the builder's own session, or one reused after the commit changed.
- [ ] **No secrets.** C's session configuration holds no Supabase or Vercel secret, and C never calls the Supabase or Vercel connectors shared with the other orchestrators (owner, 2026-11-01, [JOT-dfb739bc](../../../../wiki/context-owner-answers-coherence.md)). *Must fail:* a secret in C's environment, or a C call to either connector.

- [ ] **Recurrence and loading:** detect a planted recurrence and a stale loaded skill without owner intervention; link the occurrence and actual version. A source merge treated as proof of host use fails; an intentional baseline silently upgraded fails.

## RSI and website connection

Drift and sync findings can be failed results that start loop rounds (S-002).

## Testing Seams

- Fixture Git repositories with known drift; fixture rows; GitHub read-only queries.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-013
node workbench/tools/spec-workbench.mjs doctor
```

## Documentation Impact

- RUNBOOK names the coherence commands; reports get a home in the Workbench.

## Review and Human QA

C's own reports are reviewed by the owner on the Grill Board when they raise items.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none

## Feedback-loop planning boundary

The 2026-11-02 preparation request granted no implementation authority. TK-001D's later scoped release is recorded in [its Task](tasks/TK-001D/TASK.md); other holds, stopped experiments and failed evidence retain their scope. See [plan](../../../../wiki/context-feedback-improvement-loop-plan.md).


Detection replay and limits: [procedure](../../../../wiki/guidebooks/coherence-observations.md).
