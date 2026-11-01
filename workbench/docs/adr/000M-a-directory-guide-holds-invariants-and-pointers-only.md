---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
---

# A directory guide holds invariants and pointers only

A directory guide holds only that directory's invariants and pointers, never a procedure.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if per host, an agent editing in that directory applies an invariant stated only in the guide without being told. Refuted if a host never loads it; then the invariant moves to AGENTS.md or a code check.

Considered and rejected: procedures in directory guides, which duplicate skills.

Consequences: Each host is tested separately.

Provenance: Owner decision review, 2026-11-01.
