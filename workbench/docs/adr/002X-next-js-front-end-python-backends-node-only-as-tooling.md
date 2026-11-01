---
date: 2026-11-01
canonicalized_in:
  - ARCHITECTURE.md
  - site
  - pyproject.toml
---

# Next.js front end, Python backends, Node only as tooling

The site front end is Next.js. The AMS runtime and every backend, including the Grill Board's and the site's data feed, are Python. FastAPI is not used. Node is allowed only as tooling: the Workbench lifecycle tools and the Next.js build.

Considered and rejected: FastAPI as a backend framework, and Node as an AMS runtime.

Consequences: New backend code is Python.

Provenance: Owner answer, 2026-11-01 (round 2). Owner answer, 2026-11-01 (round 3).
