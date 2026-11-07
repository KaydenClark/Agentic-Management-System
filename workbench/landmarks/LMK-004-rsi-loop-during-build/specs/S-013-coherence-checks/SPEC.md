# S-013 - Coherence checks

**Spec ID:** S-013
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator C (cloud, no secrets)
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Spec conformance, skill pins/sync, dev/main drift and independent review.
**Blockers:** none
**Confirmation:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-003.

## Intent and authority

[RSI Map source](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac); no execution release or reset of prior stops.

The owner asked that the system stay coherent and nothing fall behind, with one orchestrator checking that the project stays up to Spec, and that the distance between `dev` and `main` be measured so a long-unmerged trunk does not happen again. Orchestrator C runs in a cloud session, works only through GitHub, holds no secrets and writes no product code.

## Outcome

At any time a reader can see whether delivered work matches its Specs, whether every run used a pinned and current skills commit, and how far `dev` is ahead of `main`. Specs get a review from a context that did not build them.

## Why It Matters

An earlier Workbench let its development trunk run thousands of commits ahead of `main` and its records drift from its code. Catching drift early is cheaper than repairing it.

## Current Verified State

No criterion is checked off. Drift and up-to-Spec checks exist ([TK-001](tasks/TK-001/TASK.md), [TK-002](tasks/TK-002/TASK.md)); Board breach reporting waits on TK-005 and skills sync on S-006 rows. Independent review tooling exists ([TK-004](tasks/TK-004/TASK.md)) but is not in the native verdict gate. Secret-free execution has no recorded proof. RUNBOOK lacks coherence commands. See [history](../../../../wiki/history/S-013.md).

## Desired Behavior

- Compare each active Spec with delivered main/dev behavior and report evidenced gaps.
- Check every RSI row’s skills pin against current skills main; report missing/stale versions and failed installations. Measure dev-ahead-of-main commits/days and create a Grill Board item above threshold.
- A fresh-context reviewer evaluates the exact Spec candidate; changed content needs fresh review. Commit reports; never silently fix findings.
- Detect large shared-skill/AMS work bypassing Map/Plan or Prepare stops. Route the [known failure](../../../../feedback/REPORT-skills-workbench-bypass-2026-11-02.md) to S-000A and verify preparation before claiming improvement. This addition releases no implementation.

### Failure detection and use evidence

S-000B’s per-chat Python observer supplies request/loading/use/failure events. Skipping an explicit skill request (including chat invocation) is Critical and a failed requested use. Unknown observation stays unknown; file presence proves no use. This grants the secret-free C actor no credentials.

Detect/report mismatches before owner prompting; retain each recurrence occurrence and S-006 identity. Diagnose owning causes rather than inferring skill causation from involvement. Route to one active repair per skill; count successful eligible uses alongside failures.

Distinguish accepted source, installed bytes, actual loading and observed use. Report accidental stale loading separately from intentional baseline pins; never upgrade a frozen comparison silently. S-000B owns recovery, S-002 qualification/retention and S-011 authorized adoption. C remains secret-free.

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

Each Task is one fresh-session run in orchestrator C's cloud lane (GitHub only, no secrets), landed feature -> `main` through a checked PR. Stack: a read-only check script, Git and GitHub reads, a committed report, and tests on fixture repositories.

## Acceptance Criteria

- [ ] **Requested skill:** plant an explicit request that never loads or runs; record a Critical failed requested use with its request identity before owner intervention. Excluding it because it did not load fails.
- [ ] **Later version:** later work verifies the accepted loaded revision and detects recurrence; a stale version cannot prove the accepted repair failed or succeeded without that distinction.

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
