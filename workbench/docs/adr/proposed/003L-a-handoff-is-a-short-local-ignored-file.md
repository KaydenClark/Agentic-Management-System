---
date: 2026-11-03
canonicalized_in:
  - AGENTS.md
supersedes:
  - 001R-a-handoff-is-a-short-live-file.md
---

# A handoff is a short local ignored file

A handoff is a short file stating the endpoint, state, open question and next action. It lives only in the local ignored `workbench/sessions/handoffs/` lane: never committed, force-added or pushed, and never a root or CONTINUE-style file. Actionable continuation is published in the Spec and Task records, so recovery never depends on the handoff. Delete the handoff once its facts are in those records on the remote.

Considered and rejected: committing the handoff on the work branch while live (ADR-001R), which published session context to GitHub; long handoffs that restate the records.

Consequences: Replaces ADR-001R, retained in history. AGENTS.md already carries the rule; shared handoff skills follow this room control rather than overriding it.

Provenance: Kayden's 2026-11-02 instruction captured as [JOT-3ac3966d](../../wiki/context-owner-answers-coherence.md#jot-3ac3966d-b26f-4212-894f-011e5e2410ad): "Handoffs belong in the local ignored workbench/sessions lane and are never pushed to GitHub." ADR-001R's owner decision review, 2026-11-01.
