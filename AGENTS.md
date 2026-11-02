# AMS - Agent Operating System

> Generated from LLM Workbench v3.2.2.

AMS builds the system in [Blueprint](BLUEPRINT.md); [S-001](workbench/specs/S-001-ams/SPEC.md) is the yardstick. Templates are shapes, not records.

## Dev environment tips

- Run `git status --short --branch`; read [RUNBOOK](RUNBOOK.md#get-oriented), [GLOSSARY](GLOSSARY.md), the [Wiki](workbench/wiki/MEMORY.md) and the assigned Spec/Task. Load the personal skill ([methods](workbench/docs/SKILLS.md)) before using it.
- Pre-repo planning lives in private GPT_OS branch `claude/ams-s003-map-20261031` under `AMS/`; read its `AMS/CONTINUE.md` before planning. Copy nothing here without owner go-ahead: this repository is public.
- Owner scope governs; rules and the assigned Spec bound it. Distinguish confirmation, execution approval, review, Human QA and publication. Ask only consequential unresolved choices. Delegate only when authorized.
- At most six Landmarks are active. Hierarchy: Landmark -> Spec -> Task. Specs need no slots; only real inputs block Tasks (ADR-003J).
- Edit `workbench/tools/` only via setup-workbench; author skills with author-skill.
- Verify repository, branch, remote and locks before editing. Preserve decisions, corrections and others' edits; one writer per record; never switch a checkout another writer uses.
- Ask before destructive actions, paid services, wider scope or unrequested external changes. License choice stays with the owner. Send no messages without authorization. Never commit secrets, host paths or private research.
- One session never holds all three of untrusted input, credentials and outward actions.
- Jot sourced intent and corrections into their owner first.

## Testing instructions

- Run `node workbench/tools/spec-workbench.mjs doctor` and the [checks](RUNBOOK.md#test-and-build). Find causes before fixing; red/green/refactor. Never weaken checks; name unavailable ones.
- Three strikes: the run, a failed test, a second failed test; then stop and report both attempts.
- RSI keeps problem, baseline, hypothesis, controlled comparison, failures and disposition; a demo or static score proves no improvement. Site claims link evidence at its scope.

## PR instructions

- Work on a short-lived branch named for the change; never commit to `main`. Started on `main`? Run `git switch -c BRANCH`.
- Commit each coherent step before ending a turn, saying what and why; the [require-committed](.agents/hooks/require-committed.sh) Stop hook enforces this. Never stash, reset or discard to get a clean tree.
- Push and confirm the remote has the commit. Non-site work: PR into `main`; once current and checked, merge it yourself with a merge commit. Site work: feature -> `dev` -> `main`; agents merge into `dev` only, never `dev` -> `main`. A merge is not Spec acceptance, Human QA or deployment.
- Read back changed owners and the diff; report candidate, checks, limits and delivery. Record review only from an eligible reviewer and Human QA only from a human.
