# S-006 - RSI data store

**Spec ID:** S-006
**Status:** planned
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The Supabase schema and the local Python writer that push RSI results, build history, cost and tokens, read by the site under row-level security.
**Blockers:** none
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01; a read-only baseline migration already exists.
**Next gate:** Task planning.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the website updates from Supabase; anything the site shows, including build history, is written there. Token counts go with the RSI data. Secrets live only in Vercel and Supabase settings.

## Outcome

One Supabase project holds every row the site presents. A local Python writer keeps it current. The site reads with the publishable key and cannot write.

## Why It Matters

Charts can only be honest if each number has a row behind it with its provenance. Keeping writes local and reads public separates credentials from the public surface.

## Current Verified State

- `supabase/migrations/` holds a read-only baseline: clients cannot insert, update or delete, and every new public table starts with row-level security on.
- No RSI tables, writer or rows exist.

## Desired Behavior

- Tables for RSI trial results, build history and run metadata. Each result row names: task, held-out or dev, trial arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Every table has a SELECT policy for the site and no client write path.
- A Python writer, run locally with the service key, inserts rows and refuses a write that conflicts with a newer row.
- Seed rows come only from real sources: the site build, improvements after it, and what the skills repository already records about recent skill fixes. Each carries a strength label (for example: anecdote, single trial, repeated trials, held-out with interval).
- Synthetic or test rows are marked so the site never shows them.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key never enters this repository or the site's environment.
- Never fabricate data. An empty table is a valid state.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- A Supabase project on the free tier (owner action); a pinned Python version.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Migration for the result, build history and run tables with read policies | ready | none | pending |
| TK-002 | Python writer inserts one real build event end to end and the site's key reads it | ready | TK-001 | pending |
| TK-003 | Seed rows from named real sources with strength labels; test rows marked | ready | TK-002 | pending |

### TK-001 - Schema

**Stance:** Builder

Proves the schema and no-client-write criteria.

### TK-002 - Writer

**Stance:** Builder

Proves the end-to-end and conflict criteria.

### TK-003 - Honest seed

**Stance:** Builder

Proves the provenance criterion.

## Acceptance Criteria

- [ ] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds.
- [ ] **No client writes.** With the publishable key, insert, update and delete fail on every table; select works. *Check:* a test using the publishable key. *Must fail:* any client write accepted.
- [ ] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file.
- [ ] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite.
- [ ] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real.
- [ ] **No secrets in Git.** The hygiene check finds no service key in the repository. *Must fail:* a committed key.

## RSI and website connection

S-002 writes its rows here; S-007 reads them.

## Testing Seams

- Migrations applied to a local or branch database; the writer's insert interface; queries with the publishable key.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-006
# migration and Python test commands named at Task planning
```

## Documentation Impact

- RUNBOOK names the writer command; ARCHITECTURE names the data path.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned; baseline migration noted | render, doctor | this Spec | Every criterion |

## Review and Human QA

Not applicable beyond Spec review; the data's presentation gets Human QA in S-007.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Supabase region defaults to the nearest US region unless the owner chooses otherwise.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files read at build time.
- Superseded by: none
