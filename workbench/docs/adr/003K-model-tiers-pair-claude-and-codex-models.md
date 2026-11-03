---
date: 2026-11-02
canonicalized_in:
  - RUNBOOK.md
supersedes:
  - 003A-implementors-run-on-opus-or-sonnet.md
---

# Model tiers pair Claude and Codex models

AMS names model roles by tier, never by one provider's model. Each agent runs a tier on its own harness's model:

| Tier | Claude | Codex |
|---|---|---|
| Frontier | Fable | Astra |
| High | Opus | Sol |
| Mid | Sonnet | Terra |
| Small | Haiku | Luna |

Frontier gives judgment and advice only, such as review, judging and recommendations; it never implements unless the owner authorizes that run. Orchestrators, Dispatchers and difficult work run High. Implementors run High or Mid. Specs, Tasks, trial contracts and briefs name the tier; evidence names the harness and exact model that actually ran. A tier its harness cannot run is recorded as unavailable, never silently filled by another provider's model. A comparison or qualification stays within one harness unless its contract declares a cross-harness arm.

Claude and Codex may work in AMS at the same time. Each claims through the Workbench with an agent name that starts with its harness (`claude-…` or `codex-…`), keeps to its own worktrees, and reads current claims before writing. Branch names stay free of harness and model prefixes. One writer per record applies across harnesses; a record another harness holds is reached through its claimant, not edited around.

Considered and rejected: naming one provider's models in records with the other's in parentheses, which reads as one provider standing in for the other; using one provider for every role, which would stop both harnesses sharing the system.

Consequences: Replaces ADR-003A, retained in history; its Opus/Sonnet implementor rule becomes High/Mid. Existing records that name exact models stay as evidence. Running agents use their own provider's model for each tier.

Provenance: Kayden's AMS chat, 2026-11-02 and 2026-11-03: the owner gave the Claude/Codex model pairing in the table, asked for a system both harnesses can share without stepping on each other or causing confusion, and ruled that Frontier models give judgment and advice only unless the owner authorizes implementation. ADR-003A's owner answers, 2026-11-01.
