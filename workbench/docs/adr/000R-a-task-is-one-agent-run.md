---
date: 2026-11-01
canonicalized_in:
  - workbench/specs
---

# A Task is one agent run

A Task is one agent run. Further work becomes a new Task. At the end, results and gaps go into the Spec and the Task file can go. Anything the site shows, such as build history and RSI results, is written to Supabase first.

Considered and rejected: long-lived Tasks that accumulate several runs.

Consequences: Deleting a finished Task loses nothing the site needs.

Provenance: Owner decision review, 2026-11-01.
