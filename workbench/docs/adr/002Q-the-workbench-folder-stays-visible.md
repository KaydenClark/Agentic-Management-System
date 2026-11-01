---
date: 2026-11-01
canonicalized_in:
  - ARCHITECTURE.md
---

# The workbench folder stays visible

The AMS keeps a visible `workbench/` folder.

Considered and rejected: a hidden dot-folder, which tools treat as private and Codex skips; and flattening into the root, which collides with application folders.

Consequences: Lanes stay under `workbench/`.

Provenance: Owner decision review, 2026-11-01.
