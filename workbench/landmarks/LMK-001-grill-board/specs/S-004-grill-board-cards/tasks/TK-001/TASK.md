# TK-001 - The owner starts the board with one command and sees every committed card with Priority and Value and a reason for each

**Task ID:** TK-001
**Spec ID:** S-004
**Slice:** The owner starts the board with one command and sees every committed card with Priority and Value and a reason for each
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Signals on every card; Local only
**Planned verification:** pytest over a fixture card set through the HTTP interface

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s004-tk001
**Current claimant:** claude-s004-tk001

Start from a clean clone of `https://github.com/KaydenClark/Agentic-Management-System`. Read `AGENTS.md`, `RUNBOOK.md`, this Task, the parent Spec (`../../SPEC.md`), [ADR-003D](../../../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md) and the card decisions it cites: DDR-000K (Priority and Value grades), DDR-000L (one local page) and DDR-000P (local Python server) under `workbench/docs/ddr/`.

Deliver the thinnest whole board: a card file format under `grill-board/`, a Python server (standard library or a small dependency added through `uv`) that reads committed card files and serves one local page listing every card with Priority and Value and a one-line reason for each, sorted by those signals, and one documented start command. Write the tests first.

In scope: card format, server, page, tests, the RUNBOOK start command and an ARCHITECTURE line for `grill-board/`. Out of scope: answering, ratings, flags and colors (TK-002 to TK-004), page review cards (S-005), any hosted deployment.

Hand back to S-004 with `close`: candidate commit, the test command and its output, docs touched and any gap.

## Acceptance

- [ ] `uv run` starts the board with the one command RUNBOOK names; it serves on localhost only and no Vercel configuration references it.
- [ ] Every card in a fixture set renders with Priority, Value and a one-line reason for each.
- [ ] A fixture card with a grade and no reason is refused or reported, never rendered silently. The test fails if it renders.
- [ ] `uv run pytest` passes on Python 3.14.5 from a clean clone.
