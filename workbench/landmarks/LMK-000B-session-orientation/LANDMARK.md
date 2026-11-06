# LMK-000B - Session orientation: agents recover intent before answering

**Landmark ID:** LMK-000B
**Status:** active
**Priority:** 1
**Owner:** Kayden
**Updated:** 2026-11-06
**Catalog description:** Every session follows the RUNBOOK and shows the recovered intent before its first answer or action.
**Blockers:** none
**Next gate:** Owner review of the first orientation trial results in the [loop report](../../feedback/REPORT-context-recovery-before-answer-2026-11-06.md).

## Direction

[The owner's direction](../../wiki/context-session-orientation.md#owner-direction)
makes this foundational: agents always do it. Every session is work.
Before its first answer or action, an agent follows the [RUNBOOK](../../../RUNBOOK.md#get-oriented),
the operating manual that trains each new agent. It recovers what already
exists, the owner's settled answers and corrections, and recorded failures, and
it shows them before it proposes anything. When agents do not follow the
manual, the manual changes how it trains them.

## Why It Matters

The same failure is logged across Anthropic and OpenAI workers (FAIL-008, 009,
017, 034, 131, 132). Agents answered or redesigned without recovering recorded
intent, the owner had to restate settled decisions, and new sessions produced
competing versions. Recording intent does no good if sessions do not recover it.

## What Success Looks Like

- [ ] Fresh Anthropic and OpenAI sessions read the RUNBOOK before their first
      answer, for questions and discussion as well as Tasks.
- [ ] Their first reply opens with the RUNBOOK's orientation note: records read,
      what already exists for the topic, settled owner answers, and
      contradictions found.
- [ ] A repeatable trial measures both, on both providers, with a baseline
      and a candidate under the same prompts.
- [ ] Owner corrections that govern operation live in the RUNBOOK or its
      routed owners, not only in one harness's private memory.

## Decision Records

[Owner direction, 2026-11-06](../../wiki/context-session-orientation.md#owner-direction).
No ADR yet.

## Child Specs

None yet. Findings F-1 to F-4 in the loop report are pending dispositions under
this Landmark.

## Boundaries

Memory retrieval, freshness and consolidation stay with
[LMK-000A](../LMK-000A-wiki-memory/LANDMARK.md). RSI loop construction stays
with S-002. Trials are read-only sessions; they make no edits, pushes or
outward actions. No shared-skill installation without the owner.

## Verification Procedure

Run the [orientation trial](../../../evals/session-orientation/README.md) on
the baseline and candidate revisions for each provider. Read each transcript;
the scorer's counts are evidence of reading and of the note's presence, not of
answer quality.

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
