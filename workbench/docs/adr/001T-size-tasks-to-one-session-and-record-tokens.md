---
date: 2026-11-01
canonicalized_in:
  - workbench/specs
  - supabase
---

# Size Tasks to one session and record tokens

Each Task is sized to finish in one fresh session. Tokens per run are recorded with the RSI data in Supabase.

Considered and rejected: Tasks that span sessions, or unmeasured cost.

Consequences: The ledger writer records tokens on every run.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
