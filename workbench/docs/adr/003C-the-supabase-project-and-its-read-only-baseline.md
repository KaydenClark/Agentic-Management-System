---
date: 2026-11-01
canonicalized_in:
  - supabase
---

# The Supabase project and its read-only baseline

The AMS uses Supabase project `hqvtnpvwwppbeurponnn` in us-east-1 on the free tier. Its first migration is a read-only baseline. The service role key is kept only in a gitignored local environment file in the owner's main checkout.

Considered and rejected: committing keys, or a paid tier before it is needed.

Consequences: Write access comes in later migrations.

Provenance: Owner answer, 2026-11-01, given after the decision review.
