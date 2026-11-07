# S-004 - Grill Board cards and answers

**Spec ID:** S-004
**Concept source:** [DQC-000A](../../../../landmark-tracker/destination-questions/DQC-000A.json) — confirmed Grilling Board lifecycle.
**Status:** active
**Priority:** 1
**Owner:** Kayden; codex-s004-director
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Local DQC readback cards and TRACKER.md, with shared actions and stable execution links.
**Blockers:** none
**Confirmation:** [JOT-285d9127-f10b-4928-b302-23131f2f42fe](../../../../wiki/context-grilling-board.md)
**Execution approval:** [JOT-285d9127-f10b-4928-b302-23131f2f42fe](../../../../wiki/context-grilling-board.md)
**Next gate:** Build confirmed DQC-000E Dashboard sections; then owner Human QA.

## Intent and authority

The [confirmed readback](../../../../wiki/context-grilling-board.md#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba) and cited execution instruction authorize both lanes, full-readback cards, TRACKER.md, reusable setup support and checked delivery. Preserve earlier proof and decisions except where explicitly superseded. No paid services, website deployment or installed personal-catalog replacement.

## Outcome

One local Python Board presents current DQCs as complete readback questions. Board and terminal actions update the same stable concept records, while TRACKER.md follows intent through execution records that remain owned by Landmarks, Specs and Tasks.

## Why It Matters

Owner attention is scarce. Exact intent, separate Priority/Value and quality feedback keep questions usable and connected to outcomes.

## Current Verified State

[H](tasks/TK-002H/TASK.md) proves tracker/setup and exact initial DQCs; [I](tasks/TK-002I/TASK.md) proves the Python Board; [K](tasks/TK-002K/TASK.md) proves the source-generator correction. CI d760635 passes839/6skip and10browser checks. [History](../../../../wiki/history/S-004.md) owns actual reviews/receipts; owner Human QA remains unperformed. Prior candidates/recovery stay preserved.

## Desired Behavior And Contracts

The acceptance and confirmed readback own behavior. DQCs own concepts; execution records own work. Full DQC readbacks supersede the old context limit; no page editor. Preserve legacy data and [DDR-000Y theme](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md). Reusable source belongs in KaydenClark/skills; supported updates own managed bytes/receipts. No installed-skill changes or authority inferred from round completion.

## Non-Goals

- Page review cards (S-005) and the public demo (S-009).
- Accounts, a hosted board or a drafting editor.

## Dependencies And Blockers

- Python 3.14.5 pinned with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

TK-002K repairs the review-found generated whitespace through the source package before assembly delivery.

TK-002H delivers native tracker/setup and AMS update; TK-002I consumes its API for the Python Board. Serialize writers on Feature/S-004-dqc-grilling-board. Catalog source uses an isolated checkout and independent PR. Both include checks/QA; assembled Review follows.

Checked Task delivery targets `main`.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

Historical committed-card evidence remains valid for that candidate, not the new DQC lifecycle:

- [x] **Signals on every card.** Separate Priority/Value grades and reasons; missing reasons refuse. Evidence: [board], TK-001.
- [x] **Answer lands in its owner.** Confirm writes the exact answer with no second confirmation. Evidence: [answers], TK-000G.
- [x] **Conflict refusal.** Stale writes refuse without changing files. Evidence: [answers], TK-002.
- [x] **Rating and flag.** Committed 1-5 ratings and Too taxing; unchanged flagged questions cannot return. Evidence: [ratings], TK-003/TK-000H.
- [x] **Not a drafting surface.** No routine page editor; legacy page-shaped cards refuse. Complete DQC readbacks are now explicitly allowed. Evidence: [ratings], TK-000I; new behavior remains below.
- [x] **Colors mean one thing.** Token values and meaning are consistent. Evidence: [theme], TK-004.
- [x] **Local only.** One local Python command, no hosted Board. Evidence: [board].
- [x] **Looks like the artifact.** Dark/light, local assets and 375px controls. Evidence: [theme], [qa shots], [375px], TK-000J.

[board]: ../../../../../tests/test_grill_board.py
[answers]: ../../../../../tests/test_grill_board_answers.py
[ratings]: ../../../../../tests/test_grill_board_ratings.py
[theme]: ../../../../../tests/test_grill_board_theme.py
[qa shots]: ../../../../../grill-board/qa/
[375px]: ../../../../../tests/test_grill_board_phone.py

### DQC lifecycle acceptance

- [x] **Initial capture and setup.** Create/Adopt/explicit Update yields usable DQCs and deterministic root TRACKER.md. Initial interview branches have stable IDs; existing schema/declarations remain readable. A bundled-but-unusable tool fails. Evidence: [TK-002H](tasks/TK-002H/TASK.md).
- [x] **Complete readback.** Cards show question, why, full proposal, source, revision, separate Priority/Value reasons and state. Confirm binds displayed bytes; corrections/quality feedback preserve owner words without invented confirmation. Evidence: [I](tasks/TK-002I/TASK.md).
- [x] **One safe lifecycle.** CLI/web preserve exact confirmed versions, source/scope, corrections, ratings and flags across retry/restart. Stale/concurrent/failed writes cannot overwrite or partially save; pending wording never inherits confirmation. Evidence: [I](tasks/TK-002I/TASK.md).
- [x] **Round continuation.** Review every changed DQC and quality event; retain unanswered/dependent questions. Reconciliation links actual Wiki/docs revisions, authorized preparation or next frontier. A count without continuation fails. Evidence: [I](tasks/TK-002I/TASK.md).
- [x] **Connected lanes.** DQCs and execution owners reference stable IDs in both directions, including qualified Tasks. Show deferral, supersession, outcome evidence and affected reopening without duplicating execution authority. Evidence: [TK-002H](tasks/TK-002H/TASK.md).
- [x] **Usable current Board.** Refresh new/revised/resolved DQCs without manual preparation; preserve typing, returned notes and history. Origin/escaping/local-only protections and 375px dark/light controls hold. Legacy records and protected worktrees remain intact. Evidence: [I](tasks/TK-002I/TASK.md).
- [x] **Verified delivery.** Source setup/update compatibility, preservation and recovery pass; AMS consumes authentic package receipts. Applicable source gates identify exact candidates. Personal catalog is unchanged; agent checks supply no Human QA. Evidence: [I](tasks/TK-002I/TASK.md). [K](tasks/TK-002K/TASK.md).

## Verification And Documentation

Use disposable Git projects at native CLI, Python HTTP and browser seams. Run RUNBOOK checks, supported setup Create/Adopt/Update/recovery and package/receipt verification. Exercise complete readbacks, round feedback, stable references, retry/stale/concurrent failure, refresh/restart, preserved data and 375px dark/light UI. Bind evidence to exact revisions; include a fresh candidate checkout.

Maintain RUNBOOK, ARCHITECTURE, Wiki and grill-board/README with actual tracker ownership/commands and update identity. Package references/templates cover fresh/existing projects. Quality feedback remains RSI input; S-005 owns page-review features, S-009 the public demo.

## Review and Human QA

Independent assembled Review covers the new immutable candidate after implementor QA. Human QA is the owner using the board on real items; it is not supplied by agent browser checks.

## Completion Result

Implementation and source publication are verified in H/I/K; History owns delivery receipts. Owner Human QA and Spec acceptance remain unperformed.

## Supersession

- Supersedes: none
- Superseded by: none
