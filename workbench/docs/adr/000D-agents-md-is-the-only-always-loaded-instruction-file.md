---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - CLAUDE.md
---

# AGENTS.md is the only always-loaded instruction file

AGENTS.md is the only always-loaded instruction file. It holds only rules for every session that the code cannot tell an agent, plus pointers to procedures loaded on demand. Its size is measured over everything an agent is told to load. CLAUDE.md is `@AGENTS.md`.

Considered and rejected: several always-loaded files per host, which duplicate and drift.

Consequences: Host-specific files point at AGENTS.md instead of restating it.

Provenance: Owner decision review, 2026-11-01.
