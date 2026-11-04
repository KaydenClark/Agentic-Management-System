# TK-002I - The owner answers current DQCs and continues a Board round

**Task ID:** TK-002I
**Spec ID:** S-004
**Concept source:** [DQC-000A](../../../../../../landmark-tracker/destination-questions/DQC-000A.json) — confirmed Grilling Board lifecycle.
**Slice:** The owner answers current DQCs and continues a Board round
**Status:** in-progress
**Blockers:** TK-002H
**Destination:** spec-acceptance: DQC lifecycle acceptance
**Planned verification:** Native CLI/setup and disposable Git/HTTP/browser cases described below; applicable Runbook checks and exact-candidate delivery verification.
**Claimed by:** codex-s004-board
**Current claimant:** codex-s004-board

## Assignment

Implement the local Python DQC Board against TK-002H’s published native lifecycle API; do not independently mutate DQC JSON or duplicate confirmation semantics. High tier Codex, one writer for src/ams/grill_board, product tests, grill-board/README and browser QA artifacts. Read the confirmed parent intent and current source before editing. The director owns Spec, Task acceptance/projections and Wiki synthesis; use native claim/close with your own claimant and coordinate record writes.

Deliver full DQC readback cards with question, why, suggested answer, source, revision and exact Confirm/Correction flow; separate Priority/Value reasons, ratings, Too taxing, visible preserved history and returned owner words. Surface pending/confirmed/deferred/superseded/delivered context honestly. DQCs are initial concept owners. Preserve existing legacy cards and responses; prevent duplicate actionable question owners and never silently migrate private answers. Reuse applicable safe transaction and refresh/draft recovery behavior from preserved PR156 e575ea44 on Feature/s004-owner-queue-gap, but do not import its independent request-fence model or unrelated dirty records.

End-to-end round processing must expose all changed DQCs including quality feedback, preserve unanswered/dependent frontier, and support actual Wiki/docs reconciliation or authorized preparation/next-round references, through native operations without inventing agent judgments. Do not claim that a round count dispatches implementation or establishes Human QA. Keep Board and terminal consistent and root TRACKER.md current. UI should reflect new/revised/resolved records without manual owner preparation, preserve unsaved typing and show source/refusal errors.

Verify HTTP and rendered interactions at 375px and desktop in dark/light; exact displayed confirmation and corrections, same history as terminal, stale/concurrent/retry/restart behavior, round feedback and continuation, legacy answers/flags, escaping and origin/loopback protections. Run focused checks then applicable Runbook checks; do not weaken existing tests. All owner actions must use disposable fixtures, never real synthetic owner answers. No site deployment, catalog installation, unrelated candidate/worktree changes or unauthorized documentation edits.

Return exact SHA, tests, screenshots/implementor QA against parent acceptance, limits, PR and the two merge/completion answers. Include usage docs for supported agent capture/round reconciliation. Publish/close truthful native receipts and leave a clean tree; assembly Review and actual owner Human QA remain separate.

## Acceptance

- [ ] Current DQCs render as complete readback-shaped cards; confirm/correct/feedback use the native lifecycle with exact owner words and visible history.
- [ ] New/revised/resolved DQCs and round changes appear without manual preparation, preserving unsaved typing, unanswered/dependent frontier and clear reconciliation/next action.
- [ ] Existing committed card data, answers and flags survive; no duplicate competing question store, unsafe path/origin, stale overwrite or partial save.
- [ ] Focused and full product checks plus dark/light 375px browser QA pass on the exact candidate; source/usage docs match actual behavior and no Human QA is fabricated.

## Workspace preservation

Workspace baseline sha256:bfc58b1c0c4fd948b8522e7c742347d34ee20e34099c6344c9328dafdf8f40f2

The implementation begins in a fresh isolated clone at published `1553bc6`, after native claim `0da727f`. The complete starting snapshot is retained privately. The original-checkout prelude snapshot was incomplete because historical REBASE_HEAD remains; it and its exact bytes are retained without removal. This new workspace baseline does not retroactively replace that limitation. No product edits preceded this binding.
