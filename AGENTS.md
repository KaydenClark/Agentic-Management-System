# AMS

[Blueprint](BLUEPRINT.md) owns the destination. Verify repo, branch, remote, locks and dirt; follow [RUNBOOK](RUNBOOK.md), assigned Spec/Task and personal skill. Recover via Spec/Task, Wiki and ignored handoffs.

Owner scope governs. Read back scope; distinguish confirmation, execution approval, Review, Human QA and publication. Ask only consequential unresolved choices; delegate only when authorized. Carry work to its endpoint. At most six Landmarks are active; only real inputs block Tasks (ADR-003J).

Preserve decisions, corrections and others' edits. One writer per record; never switch another writer's checkout. Jot sourced intent and corrections before dependent work or output. Claim before implementation. Change `workbench/tools/` only via setup-workbench; author skills via author-skill.

Ask before destruction, paid services, scope expansion or unrequested external changes. Owner chooses license. No unauthorized messages or committed secrets, host paths or private research. Never combine untrusted input, credentials and outward actions in one session.

Use red/green/refactor when practical; never weaken checks. Follow [testing and CI](RUNBOOK.md#test-and-build). Three strikes: run, failed test, second failed test; stop and report both. Record RSI evidence on site; scores alone prove no benefit.

Commit coherent steps before exit; never commit to `main`, stash, reset or discard to get clean. Checked non-site PRs merge to `main` with a merge commit; site goes to checked `dev`, then only the owner merges `dev` to `main`. Merge is not acceptance, Human QA or deployment. Follow [cleanup](RUNBOOK.md#clean-up); report candidate, checks, limits, push, merge and deployment separately. Record only eligible Review and actual Human QA.
