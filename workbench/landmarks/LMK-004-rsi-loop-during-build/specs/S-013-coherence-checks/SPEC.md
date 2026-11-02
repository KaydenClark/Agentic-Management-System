# S-013 - Coherence checks

**Spec ID:** S-013
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator C (Coherence, cloud, no secrets)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** Checks that keep the AMS coherent: up to Spec, skills pinned and in sync, `dev` measured against `main`, and independent Spec review.
**Blockers:** none
**Confirmation:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-003.

## Intent and authority

The owner asked that the system stay coherent and nothing fall behind, with one orchestrator checking that the project stays up to Spec, and that the distance between `dev` and `main` be measured so a long-unmerged trunk does not happen again. Orchestrator C runs in a cloud session, works only through GitHub, holds no secrets and writes no product code.

## Outcome

At any time a reader can see whether delivered work matches its Specs, whether every run used a pinned and current skills commit, and how far `dev` is ahead of `main`. Specs get a review from a context that did not build them.

## Why It Matters

An earlier Workbench let its development trunk run thousands of commits ahead of `main` and its records drift from its code. Catching drift early is cheaper than repairing it.

## Current Verified State

No criterion is checked off.

- **Drift measured:** the drift check and report exist ([TK-001 receipt](tasks/TK-001/TASK.md#receipt)); the Grill Board item on breach is blocked ([TK-005](tasks/TK-005/TASK.md)).
- **Up to Spec:** the check and an S-004 report exist ([TK-002 receipt](tasks/TK-002/TASK.md#receipt)).
- **Skills in sync:** blocked on S-006 rows ([TK-003](tasks/TK-003/TASK.md)).
- **Independent review:** the procedure and checker exist ([TK-004 receipt](tasks/TK-004/TASK.md#receipt)); the checker is not in the native verdict gate.
- **No secrets:** no evidence recorded.
- `doctor` reports structural findings. `dev` exists on the remote. RUNBOOK does not name the coherence commands.

History: [S-013 history](../../../../wiki/history/S-013.md).

## Desired Behavior

- **Up to Spec.** For each active Spec, compare delivered behavior on `main` or `dev` with its acceptance criteria and report gaps.
- **Skills pinned and in sync.** Every RSI row names a skills commit; report rows whose commit is behind the current skills `main` and sessions that could not install skills.
- **`dev` ahead of `main`.** Report commits and days `dev` is ahead of `main`, with a threshold that raises a Grill Board item.
- **Independent Spec review.** A fresh-context reviewer passes or returns the exact assembled commit against the Spec's conditions; a changed commit needs a fresh review.
- Reports are committed records; findings are visible, never silently fixed.

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

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Drift measured.** The report gives commits and days `dev` is ahead of `main` at a named time, and a threshold breach creates a Grill Board item. *Must fail:* a breach with no item.
- [ ] **Up to Spec.** The report lists each unmet criterion of the checked Spec with evidence. *Must fail:* a criterion reported met with no evidence.
- [ ] **Skills in sync.** Rows without a skills commit, or behind the current skills `main`, are listed. *Must fail:* an unpinned row passing.
- [ ] **Independent review.** A review names its exact commit and comes from a context that did not build the Spec. *Must fail:* a review by the builder's own session, or one reused after the commit changed.
- [ ] **No secrets.** C's session configuration holds no Supabase or Vercel secret, and C never calls the Supabase or Vercel connectors shared with the other orchestrators (owner, 2026-11-01, [JOT-dfb739bc](../../../../wiki/context-owner-answers-coherence.md)). *Must fail:* a secret in C's environment, or a C call to either connector.

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
