# TK-003 - Cold-start trial: a fresh session given only the repository URL names the AMS, its active Specs and next Task

**Task ID:** TK-003
**Spec ID:** S-001
**Slice:** Cold-start trial: a fresh session given only the repository URL names the AMS, its active Specs and next Task
**Status:** in-progress
**Blockers:** TK-002
**Destination:** spec-acceptance: Cold start.
**Claimed by:** claude-orch-s001-tk003
**Current claimant:** claude-orch-s001-tk003

## Assignment

After TK-002, record a cold-start trial in a separate session given only the repository URL. The session must name the AMS, its active Specs and its next Task. Never simulate this in the building session.

## Acceptance

- [x] The separate session, candidate, supplied input and actual result are recorded ([trial](#trial-at-9655f3c-2026-11-02)).
- [x] Its answer names the AMS, active Specs and next Task accurately, with the claim-visibility caveat below ([trial](#trial-at-9655f3c-2026-11-02)).

## Trial at 9655f3c (2026-11-02)

- **Separate session:** headless `claude -p` (Claude Code 2.1.310), session `f080acae-5bc8-40a3-a257-30d90337f16c`, started 16:07:29Z and finished 16:08:39Z, 14 turns, $0.57. It ran in a new empty folder, not in this repository, with no project instructions loaded. Its tools were limited to git, node, ls, cat, Read, Grep and Glob. The orchestrating session claimed this Task and recorded the result; it did not answer the questions.
- **Supplied input:** only the repository URL and three questions: what the project is, which Specs are active, and what the next Task is, citing sources.
- **Candidate:** the session cloned `main` at `9655f3c467f28c2e9daba1a19380d008fc3e65e3`, which is PR #98's merge with TK-002 done.
- **Ground truth at the candidate:** the Taskboard lists 8 active Specs: S-001, S-002, S-003, S-004, S-006, S-007, S-008 and S-013. `next --json --local` returns S-002 TK-000Y (ready, priority 1). In a full clone, `next --json` skips TK-000Y because it is claimed on `origin/feature/s002-structured-judge`, and returns no unclaimed Task.

### Actual result

| Question | Answer | Judgment |
|---|---|---|
| Project | AMS (Agentic Management System), Kayden's agent operating system. An RSI loop on an LLM Workbench, organized Landmark -> Spec -> Task, with S-001 as the yardstick and the website as the first loop. Cited README, AGENTS and TASKBOARD. | Accurate |
| Active Specs | The 8 above, each with its current slice. Cited `spec-workbench.mjs list` and both Taskboard pages. | Accurate |
| Next Task | S-002 TK-000Y, "A judge requests the fixed JSON schema through a bounded serialization-only transport" (ready, priority 1). Cited `next --json` and S-002's Next gate. | Accurate for the records on `main`; see the caveat |

**Caveat (finding):** the session made a shallow, single-branch clone (`--depth 1`), so `next` saw no claim branches. It reported "no remote claims" and named a Task that another writer holds. Given the same clone, the orchestrator reproduced this answer; a full clone gives a different one. Claim coordination therefore depends on how the reader cloned, and `next` gives no warning. That code lives in `workbench/tools/` (owned by setup-workbench) and is not changed here.

The session also noticed that this Task's record on `main` still says `blocked` while the Taskboard says `ready`. That is true at the candidate, because the claim exists only on this Task's branch.

