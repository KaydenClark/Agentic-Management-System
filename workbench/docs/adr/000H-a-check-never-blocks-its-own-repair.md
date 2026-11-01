---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - workbench/tools
---

# A check never blocks its own repair

A check blocks only the change it judges. It never blocks the repair that would fix it.

Considered and rejected: global gates that refuse every change while any finding is open.

Consequences: Blocking checks scope their refusal to the judged change.

Provenance: Owner decision review, 2026-11-01.
