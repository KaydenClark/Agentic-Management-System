# S-011 - Land skill catches every event

**Spec ID:** S-011
**Status:** planned
**Priority:** 3
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Improve the land skill so agents landing work no longer miss an event, measured as one RSI round from a failed result.
**Blockers:** S-002
**Latest event:** Mapped from the owner's example Spec of 2026-11-01.
**Next gate:** Task planning once the loop (S-002) can run a round.

## Intent and authority

The owner gave "improve the land skill so agents no longer miss an event" as an example Spec. The land skill lives in the owner's skills repository; changes to it go through that repository's own process.

## Outcome

An agent landing work through the land skill notices and handles each event in the landing path, such as a moved candidate, a failed check or unpushed work, instead of reporting success past it.

## Why It Matters

A missed landing event turns into lost or unverified work that looks done. It is also a clean first RSI case: a concrete failure, one owner, and a rerun that shows whether the fix worked.

## Current Verified State

- No recorded failing case exists in this repository yet; the first Task records one.

## Desired Behavior

- A failing case is recorded: the event, the run that missed it and the skills commit.
- One change is proposed to the land skill, made through the skills repository's process.
- The same case, and the regression set, are rerun at the new skills commit.
- The result is a disposition: retain, revise or remove.

## Decisions And Contracts

- This Spec runs under S-002's safeguards.
- A failure seen twice is first checked for an earlier fix that did not work.

## Non-Goals

- Editing the skill inside this repository.
- Other skills.

## Dependencies And Blockers

- S-002 (round procedure); the skills repository's review of the change.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Record a failing landing case as an evaluation task with its skills commit | ready | none | pending |
| TK-002 | Propose and land one land-skill change through the skills repository | ready | TK-001 | pending |
| TK-003 | Rerun the case and regression set at the new pin and record the disposition | ready | TK-002 | pending |

### TK-001 - Failing case

**Stance:** Builder

Proves the failing-case criterion.

### TK-002 - Skill change

**Stance:** Builder

Proves the process criterion.

### TK-003 - Rerun

**Stance:** Builder

Proves the rerun and disposition criteria.

## Acceptance Criteria

- [ ] **Failing case recorded.** The case fails at the old skills commit. *Must fail:* a case that passes before any change.
- [ ] **Changed through its owner.** The skill change is a merged change in the skills repository. *Must fail:* a copy of the skill edited in this repository.
- [ ] **Rerun at new pin.** The case and regression set rerun at the new skills commit, with rows in Supabase. *Must fail:* a claim of improvement with no rerun rows.
- [ ] **Disposition recorded.** Retain, revise or remove is recorded with its reason. *Must fail:* a retained change that broke a regression task.

## RSI and website connection

Its rows are among the first improvement data the charts show (S-007).

## Testing Seams

- The evaluation task fixture and its grader.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-011
```

## Documentation Impact

- The skills wiki entry for land is updated at the new pin (S-008).

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

The skill change is reviewed in the skills repository.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
