---
type: project
status: active
sensitivity: normal
knowledge_role: derived
provenance:
  - Kayden's ruling in AMS chat, 2026-11-02
source_paths:
  - workbench/docs/adr/002V-artifacts-have-character-limits.md
  - workbench/artifact-budgets.json
  - src/ams/build_history.py
last_verified: 2026-11-02
---

# Spec history lives outside Specs

Specs, Tasks and Landmarks have an 8,000-character limit ([ADR-002V](../docs/adr/002V-artifacts-have-character-limits.md)). Several active Specs exceed it mainly through their append-only evidence logs. The owner ruled where that history belongs.

## Current state

The native lifecycle tools (`close`, `verdict`, `complete` and related commands in `workbench/tools/`, shipped by setup-workbench) append evidence rows to each `SPEC.md`. `src/ams/build_history.py` imports those rows into Supabase keyed by table position. Until that design changes, Specs keep gaining history. The entries below record the intent and its open work.

<!-- jot-entry -->
### JOT-5ee25ca7-6874-4266-a54c-567024e2be50
Kind: intent
State: confirmed
Recorded: 2026-11-02T14:28:11.945Z
Author: Kayden
Source: Kayden, AMS chat (Claude Code orchestration session), 2026-11-02, answering whether append-only evidence logs count toward the 8,000-character Spec limit
Topic: spec-history
Supersedes: none

Kayden ruled: "Specs should not have any history on them, that goes into the wiki, or to supabase so we can show it on the RSI Tracker". Meaning: a Spec holds current destination, contracts, acceptance and state, not its event history; history (evidence-log rows, closes, verdicts, corrections) belongs in the Wiki or in Supabase build history, which the RSI Tracker reads. This answers the evidence-log question for S-006, S-008 and S-013 (over 8,000 mainly through their logs). It does not by itself authorize changing the native lifecycle tools (setup-workbench owns workbench/tools/), changing Supabase row identity, or a live import; those routes remain to be chosen and approved. ADR-002V's limit is unchanged.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-60427aea-2242-4a67-b929-21cac8c92a9a
Kind: intent
State: confirmed
Recorded: 2026-11-02T14:29:21.801Z
Author: Kayden
Source: Kayden, AMS chat (Claude Code orchestration session), 2026-11-02, follow-up to JOT-5ee25ca7
Topic: spec-history
Supersedes: none

Kayden gave the reason: "SPECs describe a destination. History about how we got to that destination does not belong in the description of it. It does not help us verify we reached the destination." A Spec keeps only what verifies arrival: destination, contracts, acceptance criteria with their checks, and current state and next gate. Event history (closes, verdict rows, corrections, intermediate proof) lives in the Wiki or Supabase build history.
<!-- /jot-entry -->
