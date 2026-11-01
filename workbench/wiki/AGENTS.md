---
type: meta
status: active
sensitivity: normal
knowledge_role: canonical
provenance:
  - LLM Workbench template wiki
source_paths:
  - workbench/wiki
last_verified: 2026-11-01
---

# workbench-adopt Wiki Agent Instructions

> Generated from LLM Workbench v3.2.2.

This Wiki follows root `AGENTS.md`; this file bounds Wiki maintenance.

## Cold Start And Navigation

1. Start each operation at `MEMORY.md`.
2. Read relevant articles for understanding, history and progress.
3. Follow their sources to current rules, assignments and proof; recheck live
   state before acting.
4. When a topic route lacks needed continuation context, use bounded
   `jot search --query TOPIC`; include private jots only with explicit
   `--include-private` within unchanged local access. Read relevant omitted
   entries explicitly. Keep private filenames out of the shared router.
5. Retrieve focused knowledge; compare claim kind, state, sources and corrections with live owners.

## Authority And Scope

- The wiki owns durable documentary knowledge and navigation, not a
  Governance Plane and not authorization.
- Verified runtime and the root controls outrank wiki notes; maintained active
  notes outrank `archive/` and platform auto-memory.
- Raw sources stay read-only during wiki maintenance unless the user also
  requests project or source work.
- Do not read or reproduce `restricted` context unless the task requires it.

## CRUD

- Follow `SCHEMA.md` for properties, provenance, sensitivity, and freshness.
- Reconcile changed knowledge into its existing article before finishing each
  operation. Preserve sources, uncertainty and correction history; create an
  article only when no existing article owns the subject.
- Keep collections flat; never copy live task state.
- Jot useful discoveries and actual owner confirmations, approvals and corrections
  when they arrive, before the next dependent action. Preserve source, scope,
  status and correction history; confirmation and approval are distinct from proof.
- New project context is shared by default, linked from its relevant Wiki route
  and included in authorized integration publication. Explicit private jots stay
  hidden, ignored and untracked; private-to-tracked transfer needs specific
  exposure approval. Preserve originals and check completeness at closeout.
- Any agent creates or updates a Design Concept article its operation touched;
  record the authorizing operation in `authorized_by` and `History`. Repair
  from direct proof or mark stale; see `SCHEMA.md` Create and Update.
- Reading and updating the Wiki is part of every use: ingest follows `SCHEMA.md`
  Update, and the lint of touched pages and of the whole Wiki follows `SCHEMA.md`
  Lint.
- Run `node workbench/tools/wiki.mjs validate` after maintained-note changes.

## Documentation

Update changed durable truth in its owner during this task; otherwise report
`Docs checked; no update needed` and why.
