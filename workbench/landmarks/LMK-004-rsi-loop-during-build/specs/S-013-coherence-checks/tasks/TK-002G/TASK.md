# TK-002G - Put operating instructions in their owning documents

**Task ID:** TK-002G
**Spec ID:** S-013
**Slice:** Repair AGENTS document ownership
**Status:** in-progress
**Blockers:** none
**Destination:** wiki-claim: Workbench control ownership
**Planned verification:** policy and link inspection; Runbook checks; checked PR into main
**Proof:** Local full suite 810 passed, 4 skipped; fresh-checkout documentation checks passed. Earlier public pushes were rejected. The owner has now explicitly authorized public publication; current PR checks and landing remain pending.
**Claimed by:** codex-agents-ownership
**Current claimant:** codex-agents-ownership

## Authorized slice

Kayden's AMS chat, 2026-11-03: fix AGENTS.md because it contains material that belongs elsewhere, including the three-strike rule. [Captured correction](../../../../../../wiki/context-workbench-adoption.md#jot-9abd9e46-08ae-4283-a950-a96e6095759f). Move procedures to RUNBOOK and SKILLS, preserving policies, source history and unrelated edits. Documentation only; feature branch into main. No deployment or broader Spec acceptance.

## Verification and hand-back

AGENTS now holds core rules and routes. RUNBOOK owns testing (including the three-strike stop), scheduling, CI and delivery; SKILLS owns method routing, delivery reporting and RSI. Local links and character limits pass. The Receipt retains the initial sandbox failures and successful rerun.

Next action: push this documentation and its required records, open a PR into main, wait for required CI and merge under the existing non-site policy. [Standing authorization](../../../../../../wiki/context-grilling-board.md#jot-d24d46bd-7ca5-44e0-854e-0411e4fbff30) resolves the earlier public-disclosure hold. Local verification clone is retained pending delivery; original checkout and unrelated ignored material remain untouched. This is no Spec acceptance, Human QA or deployment.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/agents-document-ownership | ea007f82b05653fbb0130c8e0336d0265832c9cb | ahead 1 behind 0 | 1 | Local full suite: 810 passed, 4 skipped with loopback permitted. Initial sandbox run: 704 passed, 4 skipped, 97 failed and 9 errors when socket.bind was denied. Fresh checkout: hygiene tests 36 passed, 1 skipped; hygiene 0 findings; Wiki and layout valid; render no diff. Edited links resolve; whitespace clean; AGENTS 1369 and RUNBOOK 2969 characters. Doctor retains pre-existing findings, none globally blocking. | AGENTS.md, RUNBOOK.md, SKILLS.md; Architecture RSI route; Wiki ownership and continuation; S-013 TK-002G and generated Taskboard | Implemented locally. Automatic approval review rejected public branch push twice: explicit user approval to disclose this documentation and its associated records to the public AMS repository is required. No push, PR, CI, merge or deployment occurred. Retain feature branch and verification clone pending approval. | 429979792bd9c437f2e14b37a731cf9ac59fe0339206a43061cf1f5da96aabef |
