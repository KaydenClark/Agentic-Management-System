---
date: 2026-11-01
canonicalized_in:
  - ARCHITECTURE.md
---

# CDRs follow standard ADR practice

CDRs follow standard industry ADR practice: one decision per record. An edit may bring a record's text closer to what was meant. A change that goes against the decision needs a new CDR that supersedes the old one.

Considered and rejected: one record per artifact that collects many decisions, and editing a record to say something it did not decide.

Consequences: Supersession uses the tool's supersede command; prior text stays in Git.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
