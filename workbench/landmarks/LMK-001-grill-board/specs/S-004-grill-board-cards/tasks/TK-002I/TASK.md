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

- [x] Current DQCs render as complete readback-shaped cards; confirm/correct/feedback use the native lifecycle with exact owner words and visible history.
- [x] New/revised/resolved DQCs and round changes appear without manual preparation, preserving unsaved typing, unanswered/dependent frontier and clear reconciliation/next action.
- [x] Existing committed card data, answers and flags survive; no duplicate competing question store, unsafe path/origin, stale overwrite or partial save.
- [x] Focused and full product checks plus dark/light 375px browser QA pass on the exact candidate; source/usage docs match actual behavior and no Human QA is fabricated.

## Workspace preservation

Workspace baseline sha256:bfc58b1c0c4fd948b8522e7c742347d34ee20e34099c6344c9328dafdf8f40f2

The implementation begins in a fresh isolated clone at published `1553bc6`, after native claim `0da727f`. The complete starting snapshot is retained privately. The original-checkout prelude snapshot was incomplete because historical REBASE_HEAD remains; it and its exact bytes are retained without removal. This new workspace baseline does not retroactively replace that limitation. No product edits preceded this binding.

## Verified handback

High-tier Codex implementor gpt-6.1-sol delivered product d9178b0, then guide/manifest/CI corrections 2e50b2b. The director inspected dark375/light1280 screenshots and the safe semantic-heading correction. Exact owner source remains stored unchanged; rendered sections escape prose. Native transactions remain the sole DQC writer.

- [HTTP/native regressions](../../../../../../../tests/test_grill_board_dqcs.py) cover full readback, exact confirmation and retry, web/CLI history parity, corrections/quality, source/dirty/stale failures, concurrent writers, failed commit and unrelated staging, dependency holds, context/history, legacy preservation, origin checks, cross-topic links and malformed manifests. Unknown receipts retain the original submission; actual browser POST bytes (including CRLF) match saved/replayed words.
- [Rendered checks](../../../../../../../tests/test_grill_board_dqc_browser.py) and [desktop screenshot](../../../../../../../grill-board/qa/dqc-light-1280.png) cover 375/1280 dark/light, reachable controls, escaped complete semantic sections, refresh/draft retention and unknown-outcome retry. All 10 browser checks passed, including three existing legacy checks. The round walkthrough performs web input, finish, actual disposable Wiki commit, sourced native reconciliation and a next proposal visible through refresh.
- [Exact assembled CI d760635](https://github.com/KaydenClark/Agentic-Management-System/actions/runs/41776062954) passed: 839 tests, 6 skips; browser 10 passed; full PR-range whitespace, hygiene zero, layout/ADR/render passed. Prior local full run834/6 and affected checks are supporting evidence, not a substitute for this fresh candidate.
- Both independent axes revalidated guide/manifest corrections; source K fixes the generated whitespace check through the package. Real-project read-only load preserves A confirmed and B/C/D non-actionable context, zero source issues. No synthetic owner actions, personal-catalog update or website deployment.
- Original root prelude snapshot remains explicitly incomplete due retained historical REBASE_HEAD. Product edits began only after a genuine complete snapshot in the isolated implementation clone, bound separately in 8845720. Private baseline/dispositions are retained; full inventory accounting awaits integration and generated-cache cleanup rather than a fabricated preintegration pass.

Merge answer: code is eligible under checked non-site delivery, pending final assembled record/review gates. Completion answer: scoped implementation acceptance is met; native closure follows director acceptance. Actual owner Human QA and Spec acceptance remain unperformed.
