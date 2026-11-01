---
date: 2026-11-01
canonicalized_in:
  - workbench/manifest.json
---

# One manifest names every path

One manifest names every path a tool or skill uses; no other code holds a path literal.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if in a fixture, renaming one declared path makes every consumer follow, and doctor fails on a hard-coded path. Refuted if consumers break, or the manifest carries fields nothing reads.

Considered and rejected: deriving paths by convention in each tool.

Consequences: The Python CLI resolves paths through one reader.

Provenance: Owner decision review, 2026-11-01.
