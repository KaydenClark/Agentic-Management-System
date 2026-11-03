# S-001 - Assessment of the current AMS build

**Spec ID:** S-001
**Status:** active
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** One "Are we there yet?" check across landmarks, room, skills, runtime and owner gates.
**Blockers:** none
**Confirmation:** [JOT-abe54041-757d-443a-82f4-6bc011b3908f](../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-abe54041-757d-443a-82f4-6bc011b3908f](../../wiki/context-active-spec-approvals.md)
**Next gate:** Confirm acceptance criteria and completion result.

## Intent and authority

The Blueprint owns the final project destination. S-001 provides one "Are we there yet?" assessment of the current build, with yes/no and remaining steps against this Spec's criteria. It assesses the four landmarks without parenting them; their Specs own capabilities. The linked owner correction authorizes S-001 work while those capabilities remain unfinished.

## Outcome

An auditable assessment of the room, shared skills, local Grill Board, RSI loop and presentation website against this Spec's criteria. The website explains AMS and presents verified results; the room improves shared skills already used across projects.

## Why It Matters

The owner needs one auditable account of what is done and what remains.

## Current Verified State

- Answer: **No** ([TK-001 assessment at 325b422](tasks/TK-001/TASK.md#assessment-at-325b422-2026-11-02), updated at `9655f3c`).
- Met: Room; Limits (`uv run ams-hygiene` reports 0 findings at `9655f3c`, [TK-002](tasks/TK-002/TASK.md)); Cold start ([TK-003 trial](tasks/TK-003/TASK.md#trial-at-9655f3c-2026-11-02), with a shallow-clone claim caveat).
- Not met: Landmarks, Runtime baseline, Owner gates; Hygiene (the tree and built site are clean at `9655f3c`, but git history still holds the host path and session IDs PR #103 removed).
- Unknown: Skills pinned.
- Workbench v3.2.2 is adopted: controls, lanes, Node lifecycle and generated Taskboard.
- Site code, Supabase migrations and `dev` exist; see child Specs for scoped proof.

History: [S-001 history](../../wiki/history/S-001.md).

## Desired Behavior

- **Landmarks.** LMK-001 Grill Board, LMK-002 Presentation of the RSI, LMK-003 AMS website and LMK-004 RSI loop during the build each reach their success checks.
- **Room and governance.** Root controls stay small and single-purpose within their character limits; decision records hold rationale, one decision each; records stay in visible folders; `TASKBOARD.md` is generated.
- **Skills.** The owner's skills operate the AMS from the owner's skills repository, pinned per run; room-owned skills never shadow a personal skill name.
- **Runtime.** The current Node lifecycle tools run this build and are the baseline. A Python lifecycle CLI is its own Spec (S-012), measured against that baseline before it replaces anything.
- **Orchestration.** Three Claude orchestrators: A (Website, cloud), B (Grill Board and RSI loop, local, holds the Supabase keys, never deploys) and C (Coherence, cloud, no secrets, writes no product code). Each orchestrator decides its Dispatchers; each Dispatcher decides its implementors.

## Decisions And Contracts

- Non-site work goes feature -> `main`, merged by agents once current and checked. Site work goes feature -> `dev` -> `main`; only the owner approves `dev` -> `main`.
- Specs, Tasks and Landmarks are at most 8,000 characters; root controls at most 3,000. Over the limit means prune and revise, never split or truncate.
- Three strikes: a run, a failed test, a second failed test, then stop and report.
- At most six active Landmarks; the hierarchy is Landmark -> Spec -> Task ([ADR-003J](../../docs/adr/003J-limit-active-landmarks-not-specs.md)). Specs need no slots; only actual required inputs block their Tasks.
- No public claim of improved outcomes without held-out rows, controls, the prior version and an interval.
- Secrets live only in Vercel and Supabase settings. Private evidence and traces stay out of this public repository.
- License: MIT, copyright Kayden Clark (the license file is the owner's to add).

## Related scope and priorities

See Intent and authority, and Dependencies And Blockers.

## Non-Goals

- Building any capability here; child Specs own them.
- GitHub Issues as claim records; claims use pushed branches and draft pull requests.
- A FastAPI service or a development view on Vercel.

## Dependencies And Blockers

- Final acceptance needs the landmark child outcomes and Vercel/Supabase projects. Missing capabilities are findings, not start gates.
- TK-001/TK-002 need no prerequisite Spec; TK-003 needs TK-002. Block only a Task missing an input required to start.

## Vertical Implementation Slices

Task records under `tasks/` own these checks; capability work belongs to the landmark Specs.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Landmarks reached.** Each of LMK-001 to LMK-004 is `reached` with every success check ticked against `main`. *Check:* `show LMK-00N`. *Must fail:* a landmark marked reached while a child Spec's acceptance is unmet.
- [ ] **Room.** `render` twice is byte-identical; `doctor` has no blocking finding; `CLAUDE.md` is exactly `@AGENTS.md`. *Must fail:* a hand-edited Taskboard.
- [x] **Limits.** Every Spec, Task and Landmark is at most 8,000 characters and none is split into parts. *Check:* TK-002. *Must fail:* a `.part-` file or a record over the limit.
- [ ] **Hygiene.** No host path, credential, private record ID or private trace is in the repository or built site. *Check:* TK-002 on every candidate. *Must fail:* a committed key.
- [ ] **Skills pinned.** Every RSI run names the skills commit it used. *Must fail:* a run row with no skills pin.
- [ ] **Runtime baseline.** S-012 reports Python CLI results against the Node baseline on the same tasks. *Must fail:* the Node tools removed before that comparison exists.
- [x] **Cold start.** TK-003 passes in a separate session. *Must fail:* a trial run in the building session.
- [ ] **Owner gates.** The owner's Grill Board approval of every page and the owner's `dev` -> `main` merge are recorded, bound to commits. Never supplied by an agent.

## RSI and website connection

LMK-004 measures the build this Spec tracks; LMK-002 presents those rows. The site may show this Spec's answer.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs show S-001
```

To answer "Are we there yet?": name the commit; run each check; report met, not met or unknown with evidence. Answer yes only when all are met, owner gates included. An unknown never counts as met.

## Documentation Impact

- The Blueprint owns product direction; README and AGENTS link this Spec for the current-build assessment.

## Review and Human QA

None yet. Independent review needs a fresh-context reviewer at the exact commit; Human QA comes only from the owner.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Agent-workable: S-002, S-006, S-007 and S-013 Tasks as their inputs land; make `next` warn when a shallow clone hides claim branches (setup-workbench).
- Owner gates: approve S-005, S-009 to S-012; S-003 TK-003; S-004/S-008 QA and approvals; `dev` -> `main`; any history rewrite for strings PR #103 removed.

## Supersession

- Supersedes: the pre-repository draft of S-001.
- Superseded by: none
