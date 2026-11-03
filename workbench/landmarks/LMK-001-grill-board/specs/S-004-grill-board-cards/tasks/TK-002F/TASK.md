# TK-002F - The owner opens a current, answerable Grill Board without requesting preparation

**Task ID:** TK-002F
**Spec ID:** S-004
**Slice:** Restore the established LLM_Workbench owner-queue workflow in AMS
**Status:** blocked
**Blockers:** owner:grill-board-backend-selection
**Destination:** spec-acceptance: Current owner queue
**Planned verification:** A disposable project with an actionable pending owner request and no prebuilt card must show the request; new/revised/resolved items update without owner preparation; preserve answers, revisions, refusal and privacy checks; execute applicable Runbook checks.

## Assignment

Kayden, AMS chat, 2026-11-03: things should automatically render into the Grill Board without asking for an update before use; make it like LLM_Workbench. See JOT-7c039b2f in the parent Spec's linked context. This replaces the assessment detour with the real queue gap and authorizes carrying a bounded correction through commit and PR to Feature/s004-owner-queue-gap.

Reference source: KaydenClark/LLM_Workbench at9d5e1f25b0d5870589ae1c5752f27f42acb796ef, tools/grill-board.mjs, tools/grill-board-project.mjs, tools/grill-board-deploy.mjs and workbench/grill-board/README.md. Reuse its stable question identity/revision, current queue reads, preserved owner answers and explicit answer-application workflow. Its agents add/revise items through the native tool; the reader does not infer all owner questions from Specs. Do not claim otherwise or re-ask settled holds as new decisions.

Pending consequential choice: the reusable component is Node-backed, whereas ADR-002X requires Python for all AMS backends. The owner has been asked whether to reuse that component or reproduce its workflow in Python. Do not implement the dependent architecture choice until answered. Preserve the existing board, answer history, other writers and the unborn dirty owner-queue worktree. No production deployment, paid service, synthetic owner answer, Spec acceptance or Human QA is authorized by this Task.

## Acceptance

- [ ] The board presents a real actionable owner request without owner-requested card preparation; the question contains the context, recommendation and source needed to answer it.
- [ ] New, revised and resolved items stay current; repeated opening neither duplicates items nor loses answers or re-asks settled decisions.
- [ ] An owner answer reaches its named durable owner with exact wording and revision; stale/concurrent writes refuse without data loss. Agent checks never become owner QA or a formal Spec approval.
- [ ] The selected architecture and existing privacy, loopback, rating/flag and conflict contracts hold; checks and representative rendered QA support completion.
- [ ] Commit/push, verify exact remote SHA and open a PR into Feature/s004-owner-queue-gap; report remaining integration and Human QA gates separately.

## Preparation evidence

- Existing AMS board reads only committed files under grill-board/cards; that directory contains only .gitkeep. Its core source/tests are byte-identical between S-004 featureeef0aa5 and mainbbc9ff7.
- At mainbbc9ff7 the full suite passed809with5skipped; this is baseline evidence, not proof of a queue repair.
- A separate S-004 baseline test invocation was interrupted after failures in the restricted environment. A direct socket-bind diagnostic reproduces PermissionError before product behavior can be exercised; localhost tests require permitted execution. No repair or final pass is claimed.
- Wiki validation, layout validation and diff whitespace pass; doctor has no global blocker and retains existing informational/slice findings.
