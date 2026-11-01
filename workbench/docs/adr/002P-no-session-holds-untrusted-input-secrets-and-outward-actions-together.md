---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
---

# No session holds untrusted input, secrets and outward actions together

An autonomous session holds at most two of: untrusted input, private data or credentials, and outward actions.

Considered and rejected: one session doing web research, holding Supabase and Vercel credentials, and deploying.

Consequences: Work is split across orchestrators so each holds at most two.

Provenance: Owner decision review, 2026-11-01. Based on Meta's Rule of Two.
