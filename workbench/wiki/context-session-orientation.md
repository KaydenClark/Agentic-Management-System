---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, AMS chat on agents ignoring project context, 2026-11-06
source_paths:
  - AGENTS.md
  - RUNBOOK.md
  - workbench/feedback/REPORT-context-recovery-before-answer-2026-11-06.md
last_verified: 2026-11-06
---

# Session orientation: agents recover intent before answering

## Owner direction

Source: Kayden, AMS chat, 2026-11-06, after [FAIL-132](../feedback/WORKBENCH_FEEDBACK.md)
and its [loop report](../feedback/REPORT-context-recovery-before-answer-2026-11-06.md).

- Agents recovering intent before answering is foundational: agents always do
  it, every session. "Foundational" describes the behavior, not a separate
  foundation file or record. AGENTS and the RUNBOOK make it an every-session
  step.
- These findings are new work. They do not belong to S-002, which builds the
  RSI loop rather than applying its repairs.
  [LMK-000B](../landmarks/LMK-000B-session-orientation/LANDMARK.md) owns them.
- Every session is work. "Work" in AGENTS meant every session; the trigger must
  not let an agent treat a question or a conversation as exempt.
- The RUNBOOK is the operating manual that trains each new agent. Agents read
  and follow it every session. Enforce recovery through the RUNBOOK, not by
  reading alone: when agents do not follow the manual, change how it trains
  them.
- The test is that agents read and follow the RUNBOOK every time. It must run
  on Anthropic and OpenAI models.
- S-002 being a Spec rather than a Landmark is an issue the owner raised; it is
  recorded here and not yet acted on. S-002 should close once the RSI loop is
  built.

## How it relates to Wiki memory

[LMK-000A](../landmarks/LMK-000A-wiki-memory/LANDMARK.md) makes established
knowledge recoverable: retrieval, freshness and consolidation. LMK-000B makes
every session actually use the RUNBOOK and recover that knowledge before its
first answer, across harnesses. Memory quality stays with LMK-000A.

## Open

- `align-concept` cannot be chosen by an agent (`disable-model-invocation`) and
  no AMS route names it (loop report F-2). Not yet decided.
