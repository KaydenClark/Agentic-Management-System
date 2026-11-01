---
date: 2026-11-01
canonicalized_in:
  - supabase
  - grill-board
---

# Writes to shared stores refuse on conflict

Writes to shared stores, the ledger and the Grill Board, refuse on conflict instead of overwriting.

Considered and rejected: last-writer-wins, which silently loses records.

Consequences: Writers check the version they read before writing.

Provenance: Owner decision review, 2026-11-01.
