# S-013 - Coherence checks

**Spec ID:** S-013
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator C (Coherence, cloud, no secrets)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Checks that keep the AMS coherent: up to Spec, skills pinned and in sync, `dev` measured against `main`, and independent Spec review.
**Blockers:** none
**Confirmation:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-7d1aa896-f169-4621-9f7c-b4f538591df8](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-002 closed with proof.
**Next gate:** Complete TK-003.

## Intent and authority

The owner asked that the system stay coherent and nothing fall behind, with one orchestrator checking that the project stays up to Spec, and that the distance between `dev` and `main` be measured so a long-unmerged trunk does not happen again. Orchestrator C runs in a cloud session, works only through GitHub, holds no secrets and writes no product code.

## Outcome

At any time a reader can see whether delivered work matches its Specs, whether every run used a pinned and current skills commit, and how far `dev` is ahead of `main`. Specs get a review from a context that did not build them.

## Why It Matters

An earlier Workbench let its development trunk run thousands of commits ahead of `main` and its records drift from its code. Catching drift early is cheaper than repairing it.

## Current Verified State

- `doctor` reports structural findings. No up-to-Spec, skills-sync or `dev`-ahead check exists. `dev` exists on the remote.

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

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | node --test workbench/tools/coherence-drift.test.mjs: 4 pass at 6848b75; clean-clone run with only git; report workbench/feedback/coherence/DRIFT-2026-11-01.md (main 0a7d04e, dev b06d7db, 3 ahead, 0 behind) | workbench/feedback/coherence/DRIFT-2026-11-01.md; RUNBOOK not updated (at 2,996 of 3,000 chars, finding COH-005) | Grill Board item on breach (TK-005); thresholds 20 commits / 7 days are C's default pending owner choice; close attribution: {"agent":"orchestrator-C","claimant":"orchestrator-C","onBehalfOf":null} |
| 2026-11-01 | TK-001 | Correction: check moved from `workbench/tools/` (managed runtime refused unreceipted files, `tools-receipt-missing`) to `src/ams/coherence/drift.py` on pinned Python 3.14; same fixture | `PYTHONPATH=src python3.14 -m unittest discover -s tests`: 4 pass; report regenerated (main 0a7d04e, dev 87a3576, 5 ahead, 0 behind) | workbench/feedback/coherence/DRIFT-2026-11-01.md | Receipt row 1 cites the removed Node path; superseded by this row |
| 2026-11-01 | TK-002 | Task closed | uv run pytest: 47 pass at 206fa51 (6 up-to-Spec fixture tests incl. must-fail invariant; mutation forcing met-without-evidence fails 4 tests); report workbench/feedback/coherence/UP-TO-SPEC-S-004-2026-11-01.md for S-004 at main 8b70874 (0 met, 7 not met) | workbench/feedback/coherence/UP-TO-SPEC-S-004-2026-11-01.md; RUNBOOK line blocked by COH-003 | Specs do not yet use an Evidence: clause on acceptance lines; checked lines without one report unknown by design; close attribution: {"agent":"orchestrator-C","claimant":"orchestrator-C","onBehalfOf":null} |
| 2026-11-01 | none | Owner answers to COH-005, COH-006 and COH-016 recorded; No secrets line reworded per COH-016 (connectors stay attached, C never uses them); ADR-003F/003G/003H supersede 002O/002F/002Y | `adr.mjs validate` ok | [owner answers](../../../../wiki/context-owner-answers-coherence.md), [sweep](../../../../feedback/coherence/COHERENCE-2026-11-01.md) | No secrets still needs evidence |

## Review and Human QA

C's own reports are reviewed by the owner on the Grill Board when they raise items.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
