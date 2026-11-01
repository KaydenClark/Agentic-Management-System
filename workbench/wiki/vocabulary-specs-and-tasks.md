---
type: memory
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - LLM Workbench template wiki: the glossary's Specs and Tasks grouping explained
source_paths:
  - GLOSSARY.md
last_verified: 2026-11-01
---

# Specs and Tasks: the vocabulary explained

These words name the units of planned work, the reviews that judge them and the places their records go when the work is done.

The [glossary](../../GLOSSARY.md#specs-and-tasks) owns each definition; this article explains how each word differs from its neighbours. It authorizes nothing.

## Spec

The Spec owns the continuing outcome across implementor runs. The orchestrator
compares each hand-back with Spec acceptance and reconciles the candidate,
evidence and remaining gaps before dispatching another run.

A Spec has many Tasks and Chats. Tasks reach its destination; useful knowledge moves to maintained durable owners after verified delivery. TASK.md owns each active Task state and proof; the Spec holds capability state and gates. Record-backed Tasks live under `tasks/`; table-backed compatibility and completed tables remain readable history. See AGENTS review/closure and Runbook lifecycle.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Task

A Task covers one implementor run, including verification and hand-back. A later
run receives a fresh bounded assignment after reconciliation into the Spec;
independent assignments may run in parallel with isolated writers. Runtime
status, Receipt and dependency guards still apply until explicit migration is
delivered. Reconcile knowledge and live references before replacing or
discarding completed-run scaffolding.

**Earlier wording, scoped by the 25 October 2026 single-run correction.** The
following continuation means check/fix loops within the current run, rather than
a standing assignment across later implementor runs.

One Task is intended for one useful context and one Chat.

It is temporary execution structure. When a check finds a miss and the fix is more of the same work, the same Task continues with an adjusted handoff; a new Task opens only when the fix changes the Task enough that it has to be rewritten. A later gap against delivered work becomes a new Spec under its landmark or the Blueprint, never a revived Spec and never a correction anchored to a Wiki claim. Small direct Blueprint Tasks remain accepted destination design with no delivered home; a Task's parent is its Spec or, directly, its landmark, and a `wiki-claim` destination serves only a Task whose own destination is producing that Wiki page. AGENTS carries the room's actual branch route and any accepted exception.

The alias listed under _Avoid_. Historical `TK-###` identifiers stay readable exactly as written in append-only evidence and are never rewritten; `TK` is the Task identifier prefix, so newly allocated slices keep the `TK-###` form.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Packet

Required material remains executable from tracked owners; optional local untracked context neither authorizes work nor proves claims. Traverse the owning Spec or Wiki rather than copying its body into the Packet. The Wiki is evidence for a Spec's direction and plan, never the destination a Packet carries.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Assembled-Spec review

Worker self-check is not independent approval. After a failed assembled review,
the orchestrator reconciles the finding into the still-open Spec and dispatches
a fresh single-run Task, preserving earlier IDs, records and proof. The next
assembled candidate needs fresh review. Follow the
[review and correction procedure](../docs/SKILLS.md).

**Legacy review wording, retained as migration evidence.** The following wording
predates the single-run correction and does not authorize reopening a completed
assignment for a later implementor run.

Worker self-check is not independent approval. A failed review is corrected under the still-open Spec: each finding continues its Task with an adjusted handoff, or opens a new Task only when the fix rewrites it, keeping earlier Task proof as written; the fresh assembled candidate needs review. [AGENTS](../docs/SKILLS.md) owns the obligation.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Human QA

Version cadence is a default, not the sole trigger. Actual per-Spec content-bound approval is distinct from monitoring or a green suite; only the owner promotes integration to main. Failure returns to Align and delivery at the implicated scope, without assuming every defect changes design.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Retired

Its useful content reaches durable owners; discard requires closure/capture, verified main containment, clean current-reference checks and recovery identity. Task progress remains distinct from folder lifecycle.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Archive

It is never cleared by transient Spec/Task cleanup; each decision-record register routes active decisions and its history routes retained alternatives.

Definition: [GLOSSARY.md, Specs and Tasks](../../GLOSSARY.md#specs-and-tasks).

## Priority and value

The glossary's Priority and value grouping classifies planned work and the questions about it. This section holds the full table the two glossary entries summarize.

**Priority** describes when to attend. **Value** describes return versus
investment. They are separate classifications, never a summed score.

| Priority: when to attend | Value: return versus investment |
|---|---|
| **P1 — Interrupt:** stop normal work | **V1 — Quick Win:** high return, low investment |
| **P2 — Committed:** current expected work | **V2 — Strategic Value:** high return, high investment |
| **P3 — Secondary:** when committed work allows | **V3 — Fill-In:** low return, low investment |
| **P4 — Backlog:** retained without current expectation | **V4 — Defer / Eliminate:** low return, high investment |

P1 remains visible regardless of Value. Value informs choices within an
attention lane; quick wins must not continually crowd out strategic work.

Definition: [GLOSSARY.md, Priority and value](../../GLOSSARY.md#priority-and-value).
