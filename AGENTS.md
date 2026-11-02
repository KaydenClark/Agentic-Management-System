# AMS - Agent Operating System

> Generated from LLM Workbench v3.2.2.

[Blueprint](BLUEPRINT.md) owns the destination: website, RSI and shared skill improvement. [S-001](workbench/specs/S-001-ams/SPEC.md) assesses the build.

## Start and scope

- Verify repo, branch, remote, locks and dirty state. Follow [RUNBOOK](RUNBOOK.md#get-oriented) and assigned Spec/Task; load the [personal skill](workbench/docs/SKILLS.md).
- For planning, read `AMS/CONTINUE.md` in private GPT_OS branch `claude/ams-s003-map-20261031`. This repo is public; copying needs owner go-ahead.
- Owner scope and assigned Spec govern. Distinguish confirmation, execution approval, review, Human QA and publication. Ask consequential choices; delegate only when authorized.
- At most six active Landmarks. Landmark -> Spec -> Task. Specs need no slots; only real inputs block Tasks (ADR-003J).
- Edit `workbench/tools/` only via setup-workbench; author skills with author-skill.
- Preserve decisions, corrections and others' edits; one writer per record; never switch another writer's checkout. Jot sourced intent/corrections in their owner first.
- Ask before destructive actions, paid services, scope expansion or unrequested external changes. Owner chooses license. No unauthorized messages or committed secrets, host paths or private research.
- Never combine untrusted input, credentials and outward actions in one session.

## Testing instructions

- Run `node workbench/tools/spec-workbench.mjs doctor` and [checks](RUNBOOK.md#test-and-build). Diagnose; red/green/refactor. Never weaken checks; name unavailable ones.
- Three strikes: run, failed test, second failed test; stop and report both attempts.
- RSI here: issue, baseline, hypothesis, before/after, failures, disposition; show the scoped log on the site. Improve skills; never install elsewhere. Static scores prove no benefit.

## Shared CI

Use `workbench-ci` and `workbench-runner-ams`; no GitHub-hosted fallback.
Forks skip; inspect before internal execution. No keys or `AMS_LIVE` in CI.
CI details: [Shared CI](workbench/wiki/context-shared-ci.md).

## Delivery and recovery

- Commit coherent steps (what/why) before exit; the [guard](.agents/hooks/require-committed.sh) checks dirty files. Never commit to `main`, stash, reset or discard to get clean.
- Merge current, checked non-site PRs into `main` yourself with a merge commit. Site: feature -> checked `dev`; only owner merges `dev` -> `main`. Merge is not acceptance, Human QA or deployment.
- After Test And Build, complete [Clean up](RUNBOOK.md#clean-up). Verify remote publication and target containment; leave no owned dirty work for cold start. Unfinished work stays on its Spec's Feature branch. Report blockers and retained items.
- Read back owners/diff; report candidate, target, checks and limits. Separate push/merge/deploy. Record only eligible review and actual human QA.
- Recover from Spec/Task and Wiki; adoption rollback: `workbench/sessions/recovery/adoption-recovery.json`.
