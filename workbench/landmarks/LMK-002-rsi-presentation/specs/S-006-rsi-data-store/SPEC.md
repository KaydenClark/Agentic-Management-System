# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The Supabase schema and the local Python writer that push RSI results, build history, cost and tokens, read by the site under row-level security.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-004 claimed by claude-s006-tk004.
**Next gate:** Close TK-004 with verification and documentation proof.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the website updates from Supabase; anything the site shows, including build history, is written there. Token counts go with the RSI data. Secrets live only in Vercel and Supabase settings.

## Outcome

One Supabase project holds every row the site presents. A local Python writer keeps it current. The site reads with the publishable key and cannot write.

## Why It Matters

Charts can only be honest if each number has a row behind it with its provenance. Keeping writes local and reads public separates credentials from the public surface.

## Current Verified State

- `supabase/migrations/` holds a read-only baseline: clients cannot insert, update or delete, and every new public table starts with row-level security on.
- `build_events` (migration `20261101132456`) holds one real row, the merge of PR #15 (884d021); the publishable key reads it and is refused (401) on insert, update and delete. `ams-writer` writes it. No RSI result or run tables exist.

## Desired Behavior

- Tables for RSI trial results, build history and run metadata. Each result row names: task, held-out or dev, trial arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Every table has a SELECT policy for the site and no client write path.
- A Python writer, run locally with the service key, inserts rows and refuses a write that conflicts with a newer row.
- Seed rows come only from real sources: the site build, improvements after it, and what the skills repository already records about recent skill fixes. Each carries a strength label (for example: anecdote, single trial, repeated trials, held-out with interval).
- Synthetic or test rows are marked so the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events, imported from the real records (Spec and Task files, Git history, GitHub pull requests), returns and corrections included, so the site can show how the AMS built itself.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key never enters this repository or the site's environment. The writer reads it from `SUPABASE_SERVICE_ROLE_KEY` in its process environment, loaded from the gitignored local environment file. It accepts a new-style `sb_secret_` key as well as a legacy JWT service-role key.
- Never fabricate data. An empty table is a valid state.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- Supabase project `hqvtnpvwwppbeurponnn` ([ADR-003C](../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)); Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

Each Task is one fresh-session run by orchestrator B's lane (the only holder of the service key), landed feature -> `main` through a checked PR. Stack: a Supabase migration, the Python writer, Supabase, and pytest plus queries with the publishable key.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds.
- [ ] **No client writes.** With the publishable key, insert, update and delete fail on every table; select works. *Check:* a test using the publishable key. *Must fail:* any client write accepted.
- [ ] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file.
- [ ] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite.
- [ ] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real.
- [ ] **Key loads and authenticates.** A check reports only whether `SUPABASE_SERVICE_ROLE_KEY` loaded and whether Supabase accepted it, for `sb_secret_` and legacy keys. *Must fail:* any output, log or file containing the value.
- [ ] **Build history from real records.** Supabase holds build-history rows from this build's real Spec, Task, PR and commit records, each naming its source (path, PR number or commit SHA); returns and corrections are rows. Re-importing adds no duplicates. *Must fail:* a hand-typed row or a row with no source.
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
| 2026-11-01 | TK-001 | Task closed | PR #15 merged as 884d021: uv run pytest 37 passed (red run 36 failed first); env -u SUPABASE_SERVICE_ROLE_KEY uv run ams-keycheck printed loaded: no, exit 1; live uv run --directory <main checkout> ams-keycheck printed loaded: yes / format: sb_secret / authenticated: yes / http status: 200, exit 0, no key value; hygiene grep found no key in tracked files or diff; render no diff, doctor no blocking finding | RUNBOOK names uv run pytest and ams-keycheck; ARCHITECTURE names src/ams/keycheck.py | Legacy-JWT path proven only with fakes; the live key is sb_secret. Tables, inserts and the publishable-key read path remain for TK-002 onward; close attribution: {"agent":"claude-s006-tk001","claimant":"claude-s006-tk001","onBehalfOf":null} |
| 2026-11-01 | TK-002 | Task closed | PR #18 merged as d279ae1: migration 20261101132456_build_events applied to hqvtnpvwwppbeurponnn, security advisors no finding; uv run pytest 108 passed, 1 skipped (writer tests red first: import error, then 9 failing inconclusive-probe tests after Codex P2 finding 4435825468, fixed and resolved); live from main checkout: ams-writer record-merge 884d021 printed inserted: id=1 kind=merge subject=PR #15 strength=recorded_fact is_test=False, rerun printed already recorded; ams-writer readcheck with the publishable key printed rows: 1, insert/update/delete refused (http status 401), row unchanged: yes, exit 0; AMS_LIVE=1 live test passed; hygiene grep found no key in the diff; render no diff, doctor no blocking finding | RUNBOOK names ams-writer record-merge/readcheck and AMS_LIVE=1; ARCHITECTURE names ams-writer and the build_events migration; both at or under 3,000 chars | Only build_events exists, with one row; the is_test filter is proven by policy text and stubs, not by a live test row. RSI result and run tables, stale-update refusal (TK-003) and the full build-history import (TK-004) remain; legacy-JWT path still proven only with fakes; close attribution: {"agent":"claude-s006-tk002","claimant":"claude-s006-tk002","onBehalfOf":null} |

## Review and Human QA

Not applicable beyond Spec review; the data's presentation gets Human QA in S-007.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Supabase region defaults to the nearest US region unless the owner chooses otherwise.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files read at build time.
- Superseded by: none
