---
date: 2026-11-01
canonicalized_in:
  - supabase
supersedes:
  - 002Y-supabase-holds-the-rsi-data-and-a-python-writer-keeps-it-current.md
---

# Supabase holds the RSI data and the service key stays local

Supabase holds the RSI data. A Python writer pushes results as they arrive, and the site updates from Supabase. The service role key lives only in the gitignored local environment file in the owner's main checkout (ADR-003C), never in the repository or in Vercel. The public site only reads, so Vercel holds only the project URL and publishable key.

Considered and rejected: the site reading files from the repository at build time; keeping the service key in Vercel settings, which a read-only site does not need.

Consequences: The ledger writer, run where the key lives, is the only writer of RSI data.

Provenance: Owner answer, 2026-11-01 (round 3) (ADR-002Y). Owner delegation, 2026-11-01: `workbench/wiki/context-owner-answers-coherence.md` (JOT-33cf0369-9c98-44ed-a480-a93e63b49a81).
