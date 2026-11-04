# S-004 - Grill Board cards and answers

**Spec ID:** S-004
**Status:** active
**Priority:** 1
**Owner:** Kayden; codex-s004-director
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Local Grill Board cards with Priority, Value, a rating and a "too taxing" flag, whose confirmed answers are written straight into their owning records.
**Blockers:** none
**Confirmation:** [JOT-285d9127-f10b-4928-b302-23131f2f42fe](../../../../wiki/context-grilling-board.md)
**Execution approval:** [JOT-285d9127-f10b-4928-b302-23131f2f42fe](../../../../wiki/context-grilling-board.md)
**Next gate:** TK-002H native tracker/setup, then TK-002I Python Board; independent assembled Review and owner Human QA remain separate.

## Intent and authority

The owner originally confirmed card rules on 2026-11-01. The [exact confirmed DQC lifecycle readback](../../../../wiki/context-grilling-board.md#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba) and [JOT-285d9127-f10b-4928-b302-23131f2f42fe](../../../../wiki/context-grilling-board.md) now authorize the connected concept/execution lanes, full-readback cards, TRACKER.md, reusable setup-workbench support, verification and checked non-site delivery. Preserve original decisions and historical proof except where this confirmed correction supersedes them. No paid services, public website deployment or replacement of the installed personal catalog is authorized.

## Outcome

One local Python Board presents current DQCs as complete readback questions. Board and terminal actions update the same stable concept records, while TRACKER.md follows intent through execution records that remain owned by Landmarks, Specs and Tasks.

## Why It Matters

Priority and Value are how the owner decides what needs attention. Costly questions waste the scarcest input, so the owner can flag them for rewrite.

## Current Verified State

- Historical committed-card criteria were verified at their linked evidence (TK-001 to TK-000J); this does not prove the expanded DQC lifecycle.
- The automatic-queue candidate in PR156 is preserved on its feature target, not main. Its separate dirty worktree is outside this writer’s scope.
- Current native tracker is bundled but undeclared in AMS; no root TRACKER.md exists. New DQC acceptance below is unverified.
- Review: passed at `4d49bfc` (Orchestrator C); proof in [S-004 history](../../../../wiki/history/S-004.md).
- Not met: owner approval and Human QA.

History: [S-004 history](../../../../wiki/history/S-004.md).

## Desired Behavior

- A local Python server reads durable records and is never the record.
- Agents post only items needing an answer (owner gates, open choices, page approvals, decision texts), never routine content or drafts.
- Each card shows Priority and Value with one-line reasons, a 1-5 rating and a one-click "too taxing" flag; a flagged card is rewritten before it is re-asked.
- A confirmed answer goes straight into its owning record, with no re-confirmation.
- Flags, ratings and comments are committed records the loop reads.
- A write refuses a target changed since it was read; nothing is deleted or renumbered.
- Each color is a signal with one stated meaning.
- It matches the owner's "Grilling Board Redesign" artifact, dark and light, loading nothing from other hosts.

## Decisions And Contracts

- Board decisions are tracked apart from delivery (Specs, Tasks).
- The board is local only; Vercel never serves it.
- Complete DQC question readbacks are allowed and must be inspectable before confirmation. This supersedes the 1,000-character/no-heading restriction for DQC cards; the Board still offers no routine page drafting editor. Preserve legacy card data and history.
- DQCs are the initial owners of questions, evolving concepts and exact confirmed readbacks. Board cards and TRACKER.md project those records. TASKBOARD.md projects execution. Stable DQC IDs connect both lanes; execution records retain execution truth.
- Persist changes through one native validated operation contract for terminal and Python Board, with serialized writes, revision/commit conflict refusal, idempotent retries and rollback on commit failure.
- Preserve history, source, scope and owner words; pending revisions cannot inherit previous confirmation. Confirmation, authorization, reconciliation, implementation and Human QA remain distinct.
- Round review includes all changed answers and feedback, carries unanswered/dependent questions, and records confirmed Wiki/document reconciliation, authorized preparation or the next frontier. Completion alone dispatches no unauthorized work.
- Reusable native tools and setup changes belong in KaydenClark/skills through author-skill; AMS consumes the supported package/update route with recovery inventory and authentic tool receipts. Never mutate installed personal skills or forge managed hashes.
- An owning record is a `.md` file under `workbench/` `specs/`, `landmarks/`, `docs/adr/`, `docs/ddr/` or `wiki/`, or `grill-board/page-approvals.md`; any other path is refused (TK-000G).
- The theme follows the artifact; tokens live in `grill-board/theme/tokens.json` ([DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md)).

## Non-Goals

- Page review cards (S-005) and the public demo (S-009).
- Accounts, a hosted board or a drafting editor.

## Dependencies And Blockers

- Python 3.14.5 pinned with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

TK-002H delivers the reusable native tracker/setup path and supported AMS update. TK-002I consumes that exact API and delivers the Python Board path. Serialize these writers on Feature/S-004-dqc-grilling-board; preserve prior candidate branches. Source catalog delivery uses its isolated checkout and independent PR. Both Tasks include repair, checks and implementor QA, followed by assembled Review.

Each Task is one bounded run; whole-Spec checked delivery targets `main`.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [x] **Signals on every card.** Every card shows Priority and Value with a one-line reason each. *Check:* render a fixture card set. *Must fail:* a card with a grade and no reason. *Evidence:* [board] (TK-001, PR #16).
- [x] **Answer lands in its owner.** Confirming an answer changes the owning record and needs no second confirmation. *Check:* test against a fixture record. *Must fail:* an answer that only changes board state. *Evidence:* [answers] (TK-000G, 3e557c0).
- [x] **Conflict refusal.** A write against a record changed since it was read is refused and nothing is written. *Must fail:* a silent overwrite. *Evidence:* [answers] (TK-002).
- [x] **Rating and flag.** A 1-5 rating and a "too taxing" flag are each one click and saved as committed records. A flagged card cannot be re-asked unchanged. *Must fail:* a flagged card re-posted with the same text. *Evidence:* [ratings] (TK-003; TK-000H, 0356d08).
- [x] **Not a drafting surface.** The board offers no editor for pages or routine content. *Must fail:* a page draft posted as a card. *Evidence:* [ratings] (TK-000I, a06d530).
- [x] **Colors mean one thing.** Each color has one documented meaning used consistently. *Must fail:* one color used for two meanings. *Evidence:* [theme] (TK-004, PR #24).
- [x] **Local only.** The board starts with one documented local command and no Vercel deployment serves it. *Evidence:* [board].
- [x] **Looks like the artifact.** Layout, formatting and colors match the artifact, dark and light. *Check:* served tokens equal `grill-board/theme/tokens.json`; side-by-side screenshots in `grill-board/qa/`; no third-party request; 375px holds. *Must fail:* a drifted token or a third-party resource. *Evidence:* [theme], [qa shots], [375px] (TK-000J, 00b0aa0).

[board]: ../../../../../tests/test_grill_board.py
[answers]: ../../../../../tests/test_grill_board_answers.py
[ratings]: ../../../../../tests/test_grill_board_ratings.py
[theme]: ../../../../../tests/test_grill_board_theme.py
[qa shots]: ../../../../../grill-board/qa/
[375px]: ../../../../../tests/test_grill_board_phone.py

### DQC lifecycle acceptance

- [ ] **Initial concept capture and tracker.** Supported setup creates/enables a tracker and root TRACKER.md; capture main branches before interviewing, retain stable IDs and deterministic current/history views. Must fail: bundled tool exists but fresh setup has no usable tracker.
- [ ] **Complete readback card.** Each DQC card shows its full question, why, proposed answer/readback, source, revision, separate Priority/Value reasons and state. Confirm binds exactly that displayed readback; correction/feedback records owner words without invented confirmation.
- [ ] **One safe lifecycle.** CLI and web actions use the same owning operations and preserve exact prior confirmed versions, source/scope, corrections, ratings and flags across retry/restart. Stale, competing or failed writes cannot silently overwrite or partially save records/projections; pending text cannot inherit old confirmation.
- [ ] **Round continuation.** Ending a round exposes every changed DQC and quality event; reconciliation receipts link actual Wiki/docs revisions or authorized preparation/next frontier. Unanswered questions and dependencies remain visible. A bookkeeping count alone fails.
- [ ] **Two connected lanes.** DQCs relate by stable ID to Landmarks, Specs and qualified Tasks; those execution records reference DQC IDs. Concept traceability includes deferral, supersession, delivery evidence and affected reopening without copying execution status into a competing authority.
- [ ] **Current usable Board.** New/revised/resolved DQCs refresh without manual preparation; preserve unsaved owner typing and readable returned notes/history. Local-only origin/escaping protections and reachable controls at 375px hold in dark/light. Existing card/history data and protected worktrees remain intact.
- [ ] **Reusable setup and delivery.** Source candidate proves Create, Adopt and explicit Update availability, compatibility, refusal/preservation and recovery; AMS update uses supported package tooling and valid receipts. Catalog/source checks, applicable qualification and independent assembled Review are recorded on exact revisions. Installed personal catalog remains unchanged; Human QA stays unperformed unless actually sourced.

## RSI and website connection

A low-rated or flagged question is a failed result the loop may study (S-002). The demo (S-009) shows the board with sample cards.

## Testing Seams

- The server's HTTP interface on fixture records in a temporary Git repository.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-004
uv run pytest
uv run --with playwright pytest tests/test_grill_board_phone.py
```

## Documentation Impact

- RUNBOOK, ARCHITECTURE, Wiki and grill-board/README.md: tracker ownership, supported capture/actions/round continuation, Python Board operation and exact source/update identity. Reusable setup package references/templates explain fresh and existing project support without assuming the Board is hosted.

## Review and Human QA

Independent assembled Review covers the new immutable candidate after implementor QA. Human QA is the owner using the board on real items; it is not supplied by agent browser checks.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- S-005 adds page review cards on this board.

## Supersession

- Supersedes: none
- Superseded by: none
