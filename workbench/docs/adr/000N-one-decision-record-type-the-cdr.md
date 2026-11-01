---
date: 2026-11-01
canonicalized_in:
  - GLOSSARY.md
  - ARCHITECTURE.md
---

# One decision-record type, the CDR

There is one decision-record type, the Consequential Decision Record (CDR). Each CDR has a kind: architecture (how the system is built) or destination (what the product must be, including owner answers from the Grill Board). Every CDR uses the same lifecycle and the same tool.

Considered and rejected: separate record types with separate rules for architecture and destination decisions.

Consequences: How the kind is stored is recorded in the CDR on the adr and ddr collections.

Provenance: Owner decision review, 2026-11-01.
