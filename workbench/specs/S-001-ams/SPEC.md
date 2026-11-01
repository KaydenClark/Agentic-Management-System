# S-001 - The AMS: yardstick for the whole system

**Spec ID:** S-001
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The single "Are we there yet?" check for the AMS across its four landmarks, its room and governance, its skills, its Python runtime and the owner's gates.
**Blockers:** none
**Latest event:** Ported from the pre-repository plan and rewritten from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Claim TK-001 or TK-002; at most six Specs are active at once.

## Intent and authority

The owner asked for one Spec to point at and ask "Are we there yet?", with a yes or no and the remaining steps. Ported 2026-11-01 and rewritten from the confirmed decisions, which win over the earlier draft. This Spec owns only cross-landmark checks; child Specs of the landmarks own the capabilities.

## Outcome

The AMS is the management system Claude Code and Codex use to align and deliver the owner's ideas: a Workbench room operated by the owner's skills, with a local Grill Board and an RSI loop that measures the work. Its first outside product is the presentation website.

## Why It Matters

Agent management must be auditable while it is built, and the owner wants to stand behind every site claim; that needs one place saying what is done and what is not.

## Current Verified State

- The repository is adopted as a Workbench (v3.2.2): root controls, `workbench/` lanes, Node lifecycle tools, a generated Taskboard.
- Six child Specs are active with Tasks (2026-11-01): S-003 and S-007 (orchestrator A), S-004, S-006 and S-002 (B), S-013 (C). The rest wait in the backlog below.
- `site/` holds only a placeholder; a read-only Supabase baseline migration exists; a `dev` branch exists.

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
- At most six active Specs; the rest wait in the backlog.
- No public claim of improved outcomes without held-out rows, controls, the prior version and an interval.
- Secrets live only in Vercel and Supabase settings. Private evidence and traces stay out of this public repository.
- License: MIT, copyright Kayden Clark (the license file is the owner's to add).

## Backlog order

Planned Specs, activated in this order as active ones close (at most six active): S-005 page review cards; S-011 land skill events; S-010 governance flow charts; S-008 skills wiki; S-009 demo Grill Board; S-012 Python lifecycle CLI. The owner may reorder.

## Non-Goals

- Building any capability here; child Specs own them.
- GitHub Issues as claim records; claims use pushed branches and draft pull requests.
- A FastAPI service or a development view on Vercel.

## Dependencies And Blockers

- Every child Spec of LMK-001 to LMK-004, plus Vercel and Supabase projects on free tiers.

## Vertical Implementation Slices

Each slice is a cross-landmark check; capability work belongs to child Specs.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Run the "Are we there yet?" check at a named commit and record the answer in this Spec's log | ready | none | pending |
| TK-002 | Add a public hygiene and character-limit check over records, controls and the built site | ready | none | pending |
| TK-003 | Cold-start trial: a fresh session given only the repository URL names the AMS, its active Specs and next Task | ready | TK-002 | pending |

### TK-001 - Are we there yet?

**Stance:** Builder

Run every acceptance check below and every landmark's success checks at one commit; record met, not met or unknown with evidence.

### TK-002 - Hygiene and size check

**Stance:** Builder

A script that fails on host paths, credentials, private record IDs and any Spec, Task or Landmark over 8,000 characters; wired into the checks.

### TK-003 - Cold-start trial

**Stance:** Builder

One recorded trial in a separate session, never simulated in the building session.

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

## Review and Human QA

None yet. Independent review needs a fresh-context reviewer at the exact commit; Human QA comes only from the owner.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Current answer: **No** (2026-11-01). Every landmark is planned.

## Supersession

- Supersedes: the pre-repository draft of S-001.
- Superseded by: none
