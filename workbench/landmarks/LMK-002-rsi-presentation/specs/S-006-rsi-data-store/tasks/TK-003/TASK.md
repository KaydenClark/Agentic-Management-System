# TK-003 - The writer records RSI result and run rows with full provenance, refusing a missing skills commit and a stale update

**Task ID:** TK-003
**Spec ID:** S-006
**Slice:** The writer records RSI result and run rows with full provenance, refusing a missing skills commit and a stale update
**Status:** in-progress
**Blockers:** TK-002
**Destination:** spec-acceptance: Schema and provenance; Conflict refusal
**Planned verification:** live tests for the missing-field and conflict refusals

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk003
**Current claimant:** claude-s006-tk003

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-000A, ADR-002J and DDR-000T, and the writer under `src/`.

Deliver: a migration for RSI result and run tables carrying every field the Spec's Desired Behavior names (task, split, arm, runtime, controls and skills commits, provider, model, effort, pass, cost, tokens, completed state, source), non-null where required; the writer's insert for them; and a stale-update refusal: an update against a row changed since it was read is refused.

Out of scope: seeding (TK-005 and S-002).

Hand back to S-006 with `close`.

## Acceptance

- [ ] Inserting a result row with no skills commit fails at the database.
- [ ] A complete row inserts and the publishable key reads it; client writes fail on both new tables.
- [ ] An update against a row changed since it was read is refused and the row is unchanged.
- [ ] `uv run pytest` passes.
