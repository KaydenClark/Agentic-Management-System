# AMS - Agent Operating System

> From LLM Workbench v3.2.2.

[Blueprint](BLUEPRINT.md) owns the destination: website, RSI and shared skill improvement. [S-001](workbench/specs/S-001-ams/SPEC.md) assesses the build.

## Start and scope

- Verify repo/branch/remote, locks and dirty state. Follow [RUNBOOK](RUNBOOK.md#get-oriented), assigned Spec/Task and [personal skill](workbench/docs/SKILLS.md).
- Planning: read `AMS/CONTINUE.md` on private GPT_OS `claude/ams-s003-map-20261031`; copying here needs owner go-ahead.
- Owner/Spec scope governs. Distinguish confirmation, execution approval, review, Human QA and publication. Ask consequential choices; delegate only when authorized.
- At most six active Landmarks. Landmark -> Spec -> Task. Specs need no slots; only real inputs block Tasks (ADR-003J).
- Edit `workbench/tools/` only via setup-workbench; author skills with author-skill.
- Preserve decisions, corrections and others' edits; one writer per record; never switch another writer's checkout. Jot sourced intent/corrections in their owner first.
- Ask before destruction, paid services, scope expansion or unrequested external changes. Owner chooses license. No unauthorized messages, committed secrets/host paths/private research.
- Never combine untrusted input, credentials and outward actions in one session.

## Testing instructions

- Run `node workbench/tools/spec-workbench.mjs doctor` and [checks](RUNBOOK.md#test-and-build). Diagnose; red/green/refactor; never weaken checks; name unavailable ones.
- Three strikes: run, failed test, second failed test; stop and report both attempts.
- RSI here: issue, baseline, hypothesis, before/after, failures, disposition; show the scoped log on the site. Repair `KaydenClark/skills`; authorized personal-catalog installs only. No cross-project rollout. Static scores prove no benefit.

## Shared CI

Use `workbench-ci` and `workbench-runner-ams`; no GitHub-hosted fallback.
Skip forks; inspect before internal execution. No keys/`AMS_LIVE` in CI.
[Shared CI](workbench/wiki/context-shared-ci.md).

## Delivery and recovery

- Commit coherent steps (what/why) before exit; the [guard](.agents/hooks/require-committed.sh) checks dirty files. Never commit to `main`, stash, reset or discard to get clean.
- Merge current, checked non-site PRs into `main` yourself with a merge commit. Site: feature -> checked `dev`; only owner merges `dev` -> `main`. Merge is not acceptance, Human QA or deployment.
- After Test And Build, [Clean up](RUNBOOK.md#clean-up): verify remote publication/containment; no owned dirty work. Keep unfinished work on its Spec Feature branch; report blockers/retained items.
- Read back owners/diff, candidate, target, checks and limits. Separate push/merge/deploy. Record only eligible review and actual human QA.
- Recover from Spec/Task and Wiki; adoption rollback: `workbench/sessions/recovery/adoption-recovery.json`.
- Handoffs: local ignored `workbench/sessions/handoffs/`, never GitHub; publish Tasks.
