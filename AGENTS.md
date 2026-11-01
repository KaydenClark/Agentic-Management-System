# AMS - Agent Operating System

> Generated from LLM Workbench v3.2.2.

AMS uses and repairs the Workbench while building the agent-management system in [Blueprint](BLUEPRINT.md). Templates are shapes, not records.

## Dev environment tips

- Run `git status --short --branch`; read [RUNBOOK](RUNBOOK.md#get-oriented), [ARCHITECTURE](ARCHITECTURE.md#routes), [GLOSSARY](GLOSSARY.md), the [Wiki](workbench/wiki/MEMORY.md) and the assigned Spec/Task. Load the personal skill ([methods](workbench/docs/SKILLS.md)) before using it.
- Pre-repo planning (S-001/S-003, owner decisions, evidence) is in private GPT_OS branch `claude/ams-s003-map-20261031` under `AMS/`. Read its `AMS/CONTINUE.md` before planning; copy nothing here without owner go-ahead: this repository is public.
- The owner request governs scope; these rules and an assigned Spec bound it. Distinguish intent confirmation, execution approval, review, Human QA and publication. Reuse given authority; ask only for consequential unresolved choices. Delegate only when authorized.
- Scope: `src/`, `tests/`, `site/`, `grill-board/`, `evals/`, root controls and `workbench/` lanes as assigned; `workbench/tools/` only via setup-workbench. Author skills with author-skill; a project skill needs a distinct need.
- Before editing, verify repository, branch, remote, upstream and locks. Preserve decisions, corrections, unrelated edits and recovery material; one writer per shared record; never switch a checkout another writer uses.
- Ask before destructive actions, paid services, wider scope or unrequested external changes. License choice stays with the owner. Send no messages without authorization. Never commit secrets, host paths or private research.
- Jot sourced intent and corrections into their owner or a flat Wiki topic first.

## Testing instructions

- Run `node workbench/tools/spec-workbench.mjs doctor` and the [checks](RUNBOOK.md#test-and-build). Find causes before fixing; red/green/refactor. Never weaken checks; name unavailable ones.
- RSI keeps problem, baseline, hypothesis, controlled comparison, failures and disposition; a demo or static score proves no improvement. Website claims link to evidence at its scope.

## PR instructions

- Work on a short-lived branch named for the change; never commit to `main`. Started on `main`? Run `git switch -c BRANCH`; your changes come with you.
- Commit each coherent step before ending a turn, saying what and why; the [require-committed](.agents/hooks/require-committed.sh) Stop hook enforces this. Never stash, reset or discard to get a clean tree.
- Push and confirm the remote has the commit. Open a PR into `main`; once up to date with checks passing, merge it yourself with a merge commit; no owner approval is needed. A merge is not Spec acceptance, Human QA or deployment (none configured).
- Read back changed owners and the diff; report candidate, checks, limits and delivery. Record review only from an eligible reviewer and Human QA only from a human.
