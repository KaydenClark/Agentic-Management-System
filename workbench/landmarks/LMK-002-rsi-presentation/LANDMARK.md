# LMK-002 - Presentation of the RSI

**Landmark ID:** LMK-002
**Status:** planned
**Priority:** 2
**Owner:** Kayden
**Updated:** 2026-11-01
**Catalog description:** Website pages that chart skill and build improvement from real RSI data only, read from Supabase and labeled at the strength the data supports.
**Blockers:** none
**Latest event:** Landmark mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning for S-006.

## Direction

The public site shows what the RSI loop actually measured, including no change and regressions. A local Python writer pushes each RSI result, build event, cost and token count to Supabase as it happens. The site reads those rows with the publishable key under row-level security and never writes.

Chart places exist from the first deploy, empty until data arrives, so the owner can see where results will appear. The first data is the building of the site itself and the improvements made after it, plus what the skills repository already records about recent skill fixes. Nothing is invented to fill a chart.

## Why It Matters

The AMS premise, that a managed environment beats none, is a claim to test, not to assert. A presentation that only shows good news, or shows numbers it cannot trace, would undo the point of the site. Rows that carry their own provenance let every number link back to what produced it.

## What Success Looks Like

- [ ] The Supabase schema for RSI results, build history, cost and tokens exists as migrations in `supabase/migrations/`, with row-level security on every table (S-006).
- [ ] A Python writer, run locally with the service key, inserts rows; the site holds only the publishable key and cannot write (S-006).
- [ ] Every seeded row comes from a real, named source and carries a strength label (S-006).
- [ ] The RSI chart pages exist on the `dev` deployment with an honest empty state before any data arrives (S-007).
- [ ] Every number on those pages links to the rows that produced it, and a headline appears only from held-out tasks with an interval (S-007).

## Decision Records

The decision records under this landmark, one line each, linked to their record.

- [Supabase holds the RSI data and a Python writer keeps it current](../../docs/adr/archive/002Y-supabase-holds-the-rsi-data-and-a-python-writer-keeps-it-current.md)
- [The Supabase project and its read-only baseline](../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)
- [Charts start blank and data is never fabricated](../../docs/ddr/000T-charts-start-blank-and-data-is-never-fabricated.md)
- [Improvement claims need held-out ledger evidence](../../docs/adr/000A-improvement-claims-need-held-out-ledger-evidence.md)

## Child Specs

- [S-006 - RSI data store](specs/S-006-rsi-data-store/SPEC.md)
- [S-007 - RSI chart pages](specs/S-007-rsi-charts/SPEC.md)

## Direct Tasks

- none

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show LMK-002
node workbench/tools/spec-workbench.mjs show S-006
node workbench/tools/spec-workbench.mjs show S-007
node workbench/tools/spec-workbench.mjs doctor
```

Each reached check is confirmed against what has landed on `main` and, for pages, against the protected `dev` deployment.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Landmark mapped from confirmed owner decisions; child Specs S-006 and S-007 written as planned; a read-only Supabase baseline migration already exists | render and doctor on the mapping branch | this record | Task planning |

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
