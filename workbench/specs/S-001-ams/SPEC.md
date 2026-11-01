# S-001 - The AMS: yardstick for the whole system

**Spec ID:** S-001
**Status:** active
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** One "Are we there yet?" check across landmarks, room, skills, runtime and owner gates.
**Blockers:** none
**Confirmation:** [JOT-abe54041-757d-443a-82f4-6bc011b3908f](../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-abe54041-757d-443a-82f4-6bc011b3908f](../../wiki/context-active-spec-approvals.md)
**Latest event:** Owner set the cap to six active Landmarks; S-001 activated without waiting for another Spec to close.
**Next gate:** Run TK-001 now; unfinished assessed capabilities are findings, not a start gate.

## Intent and authority

The owner wants one "Are we there yet?" Spec, with yes/no and remaining steps. S-001 sits under the Blueprint and assesses the four landmarks; it does not parent them. Their Specs own capabilities. The linked owner correction authorizes S-001 work while those capabilities remain unfinished.

## Outcome

Claude Code and Codex deliver the owner's ideas through a Workbench, personal skills, a local Grill Board and a measured RSI loop. Its first outside product is the presentation website.

## Why It Matters

The owner needs one auditable account of what is done and what remains.

## Current Verified State

- Workbench v3.2.2 is adopted: controls, lanes, Node lifecycle and generated Taskboard.
- Six capability Specs were active before this correction. Specs consume no Landmark slots; A/B product work remains stopped.
- Site code, Supabase migrations and `dev` exist; see child Specs for scoped proof.

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
- At most six active Landmarks; the hierarchy is Landmark -> Spec -> Task ([ADR-003J](../../docs/adr/proposed/003J-limit-active-landmarks-not-specs.md)). Specs need no slots; only actual required inputs block their Tasks.
- No public claim of improved outcomes without held-out rows, controls, the prior version and an interval.
- Secrets live only in Vercel and Supabase settings. Private evidence and traces stay out of this public repository.
- License: MIT, copyright Kayden Clark (the license file is the owner's to add).

## Related scope and priorities

Landmarks parent capability Specs; S-001 assesses their outcomes across the build. Related unfinished work does not prevent S-001 from assessing it or repairing its own scope. Final acceptance remains unchanged.

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
- [ ] **Limits.** Every Spec, Task and Landmark is at most 8,000 characters and none is split into parts. *Check:* TK-002. *Must fail:* a `.part-` file or a record over the limit.
- [ ] **Hygiene.** No host path, credential, private record ID or private trace is in the repository or built site. *Check:* TK-002 on every candidate. *Must fail:* a committed key.
- [ ] **Skills pinned.** Every RSI run names the skills commit it used. *Must fail:* a run row with no skills pin.
- [ ] **Runtime baseline.** S-012 reports Python CLI results against the Node baseline on the same tasks. *Must fail:* the Node tools removed before that comparison exists.
- [ ] **Cold start.** TK-003 passes in a separate session. *Must fail:* a trial run in the building session.
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

- README and RUNBOOK point here as the yardstick.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Ported and rewritten; the Workbench adoption of 2026-11-01 recorded as this Spec's first room evidence | render, doctor | this Spec; adoption Wiki page | Every criterion |
| 2026-11-01 | none | Owner unblocked S-001; the limit applies to Landmarks, above Specs | Linked confirmed owner correction; activation/readiness verification in the delivery PR | Landmark cap and start/acceptance distinction | Acceptance remains open; A/B work stays stopped |

## Review and Human QA

None yet. Independent review needs a fresh-context reviewer at the exact commit; Human QA comes only from the owner.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Current answer: **No** (2026-11-01). Every landmark is planned.

## Supersession

- Supersedes: the pre-repository draft of S-001.
- Superseded by: none
