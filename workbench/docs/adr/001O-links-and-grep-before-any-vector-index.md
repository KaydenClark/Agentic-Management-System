---
date: 2026-11-01
canonicalized_in:
  - ARCHITECTURE.md
---

# Links and grep before any vector index

Agents follow links and use grep. No vector index is built until a fixed known-answer question set shows retrieval misses.

Considered and rejected: a vector index on speculation.

Consequences: A retrieval eval comes before any index.

Provenance: Owner decision review, 2026-11-01.
