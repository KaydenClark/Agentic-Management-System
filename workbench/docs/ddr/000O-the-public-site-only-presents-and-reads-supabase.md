---
date: 2026-11-01
supersedes:
canonicalized_in:
  - BLUEPRINT.md
  - site
---

# The public site only presents and reads Supabase

The public site is presentation only. It reads ledger rows and records from Supabase and writes nothing. It is never a second dashboard, and Vercel hosts no development view.

Considered and rejected: a site with its own backend state or an owner dashboard on Vercel.

Consequences: Data the site needs is written to Supabase by the Python writer.

Provenance: Owner decision review, 2026-11-01. Owner answer, 2026-11-01 (round 2).
