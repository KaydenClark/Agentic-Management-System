---
date: 2026-11-01
canonicalized_in:
  - ARCHITECTURE.md
  - workbench/manifest.json
---

# The adr and ddr collections are the CDR's two kinds

The installed tool keeps CDRs in two collections, `adr` and `ddr`. These are the two kinds of the one CDR type: `adr` for architecture, how the system is built, and `ddr` for destination, what the product must be, including owner answers. The collection is the kind field. Both share one tool, one template shape and one lifecycle, and the prefix keeps every ID unique.

Considered and rejected: one folder with a frontmatter kind field, which the installed tool does not support.

Consequences: Use `adr.mjs new --kind adr|ddr`; folder location within a collection is lifecycle only.

Provenance: Owner decision review, 2026-11-01.
