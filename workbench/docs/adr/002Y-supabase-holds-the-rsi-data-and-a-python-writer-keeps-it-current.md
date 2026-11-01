---
date: 2026-11-01
canonicalized_in:
  - supabase
---

# Supabase holds the RSI data and a Python writer keeps it current

Supabase holds the RSI data. A Python writer pushes results as they arrive, and the site updates from Supabase. Secrets live in Vercel and Supabase environment settings, never in the repository.

Considered and rejected: the site reading files from the repository at build time.

Consequences: The ledger writer is the only writer of RSI data.

Provenance: Owner answer, 2026-11-01 (round 3).
