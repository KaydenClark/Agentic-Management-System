# TK-002F - The owner opens a current, answerable Grill Board without requesting preparation

**Task ID:** TK-002F
**Spec ID:** S-004
**Slice:** Restore the established LLM_Workbench owner-queue workflow in AMS
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Current owner queue
**Planned verification:** A disposable project with an actionable pending owner request and no prebuilt card must show the request; new/revised/resolved items update without owner preparation; preserve answers, revisions, refusal and privacy checks; execute applicable Runbook checks.
**Claimed by:** codex-s004-queue
**Current claimant:** codex-s004-queue

## Assignment

Kayden, AMS chat, 2026-11-03: things should automatically render into the Grill Board without asking for an update before use; make it like LLM_Workbench. See JOT-7c039b2f in the parent Spec's linked context. This replaces the assessment detour with the real queue gap and authorizes carrying a bounded correction through commit and PR to Feature/s004-owner-queue-gap.

Reference source: KaydenClark/LLM_Workbench at9d5e1f25b0d5870589ae1c5752f27f42acb796ef, tools/grill-board.mjs, tools/grill-board-project.mjs, tools/grill-board-deploy.mjs and workbench/grill-board/README.md. Reuse its stable question identity/revision, current queue reads, preserved owner answers and explicit answer-application workflow. Its agents add/revise items through the native tool; the reader does not infer all owner questions from Specs. Do not claim otherwise or re-ask settled holds as new decisions.

Resolved correction, 2026-11-03: Kayden directs Python, as already required by ADR-002X. The agent-created backend hold was unnecessary. Implement the established behavior in Python; no architecture choice remains. Preserve the existing board, answer history, other writers and the unborn dirty owner-queue worktree. No production deployment, paid service, synthetic owner answer, Spec acceptance or Human QA is authorized by this Task.

## Acceptance

- [ ] The board presents a real actionable owner request without owner-requested card preparation; the question contains the context, recommendation and source needed to answer it.
- [x] New, revised and resolved items stay current; repeated opening neither duplicates items nor loses answers or re-asks settled decisions.
- [x] An owner answer reaches its named durable owner with exact wording and revision; stale/concurrent writes refuse without data loss. Agent checks never become owner QA or a formal Spec approval.
- [x] The selected architecture and existing privacy, loopback, rating/flag and conflict contracts hold; checks and representative rendered QA support completion.
- [x] Commit/push, verify exact remote SHA and open a PR into Feature/s004-owner-queue-gap; report remaining integration and Human QA gates separately.

## Preparation evidence

- Existing AMS board reads only committed files under grill-board/cards; that directory contains only .gitkeep. Its core source/tests are byte-identical between S-004 featureeef0aa5 and mainbbc9ff7.
- At mainbbc9ff7 the full suite passed809with5skipped; this is baseline evidence, not proof of a queue repair.
- A separate S-004 baseline test invocation was interrupted after failures in the restricted environment. A direct socket-bind diagnostic reproduces PermissionError before product behavior can be exercised; localhost tests require permitted execution. No repair or final pass is claimed.
- Wiki validation, layout validation and diff whitespace pass; doctor has no global blocker and retains existing informational/slice findings.

Permitted baseline rerun: `uv run --offline pytest -q tests/test_grill_board.py tests/test_grill_board_answers.py tests/test_grill_board_ratings.py tests/test_grill_board_theme.py --maxfail=1` passed128/128 in86.17seconds on unchanged product code. This establishes existing card mechanics only. ADR validation and staged-file hygiene also pass. No automatic-queue repair has been implemented.

## Implementation evidence

Expected red: an explicit pending request in a Spec rendered the old empty-board message; after projection, both initial HTTP cases passed. The next expected red showed projected requests could not yet use the committed-card writer. Extending that writer initially exposed Git's missing --add option for a first response file; the transaction refused and rolled back. The correction passed the full focused suite:146tests, including128existing board tests and18queue regressions.

The first full suite passed827with6skipped. Browser checks passed8/8, covering both themes at375/1280, reachable controls, automatic reload, exact unsaved-note preservation and source unavailability; inspected phone/dark and desktop/light screenshots. Self-review then tightened non-decision revisions and unprepared owner-next-gate detection; the resulting20queue cases pass. A fresh-checkout full run will bind final verification. No owner answer was submitted to the real board.

## Final checked candidate and remaining boundary

Sourcec9a8aa06da488dfc30b9ca8af5a7fa1944497d2e, fresh detached checkout: full Python suite829passed/6skipped; separate Playwright run8passed;20focused queue cases pass. Render matches committed projection; doctor has no global blocker; layout, Wiki, ADR, whitespace and hygiene checks pass. Retained doctor findings are the pre-existing S-011 slice, stale S-002 claim, undeclared legibility and permission drift; detached HEAD is an inspection notice. Site code and managed Workbench tools are unchanged.

Readback of the actual project has zero authored requests and six visible source-preparation issues. No owner answer was submitted. Automatic approval review rejected publishing the proposed real usability request into S-004 and pushing it, classifying the new workflow item/payload as beyond implementation authorization. The rejected command did not run; no workaround or substitute publication was attempted. The exact question and proposed answer were presented to Kayden for optional approval; silence supplies none.

The Python implementation is committed/pushed on task/s004-automatic-owner-queue in PR156 into Feature/s004-owner-queue-gap. The PR remains draft and this Task remains in progress: the real-project presentation acceptance above is not checked. Code behavior is established through disposable records and owner-action fixtures, not a real owner decision. Current writer codex-s004-queue continues only the withheld posting if explicitly approved, or reconciles the endpoint if the owner chooses code-only delivery. Independent assembled Review, owner Human QA, target integration and publication remain separate. Existing CI workflows target main/dev, so no combined statuses are attached to this feature-target candidate; do not claim CI passed.

## Checked feature-branch delivery continuation, 2026-11-03

Kayden authorizes PR156 feature integration; acceptance, Human QA and DQC lifecycle remain open.

Review reproduced draft loss after withdrawal/completion. The repair preserves escaped words, never on another question. Independent re-review cleared it; a nonblocking duplication heuristic remains. See Receipt.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | task/s004-automatic-owner-queue | 98adbea1dc17e466c9fd5bfbf04a44fb499791dd | ahead 0 behind 0 | 2 | Repair runtime f9ef2b9: full suite 834 passed/6 skipped; queue 25 passed; final added browser regressions 2 passed at 375/1280. Independent Standards/Spec re-review: no blocking findings. | PR156; TK-002F repair evidence | Merge only to Feature/s004-owner-queue-gap under current owner direction; real-project acceptance, Human QA and DQC lifecycle remain open. One pre-existing Wiki edit is preserved. | 5a6e4e3155280fd9cd34aad8de96bcfb0b4a0b55ec9c5263e1747f968dce0298 |
