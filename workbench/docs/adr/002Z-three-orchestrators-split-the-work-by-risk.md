---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - RUNBOOK.md
---

# Three orchestrators split the work by risk

Three orchestrators, all Claude, split the work. A, Website, builds the site and RSI presentation; deploys reach Vercel only through pushes to `dev`, and it does no web browsing. B, Grill Board and RSI loop, runs the local board, the Python backend and the Supabase keys on the owner's Mac mini, and never deploys. C, Coherence, checks the project stays up to Spec, syncs skills, watches `dev`/`main` drift, gives independent Spec review and does web research; it holds no secrets and writes no product code. A and C run in Claude cloud sessions.

Considered and rejected: one orchestrator holding untrusted input, secrets and outward actions together.

Consequences: Each orchestrator holds at most two of the three risks.

Provenance: Owner decision review, 2026-11-01, with the owner's correction. Based on Meta's Rule of Two.
