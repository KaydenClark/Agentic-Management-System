---
type: meta
status: active
sensitivity: normal
knowledge_role: canonical
provenance:
  - LLM Workbench template wiki
source_paths:
  - workbench/wiki/features
last_verified: 2026-11-01
---

# Feature Catalog

> Generated from LLM Workbench v3.2.2.

This is the Workbench's Feature catalog: maintained articles explaining what
capabilities do, why they matter, their history, progress, limits and sources.
Read the relevant existing article before updating the Wiki. Reconcile later
Specs, corrections and lessons into that article; preserve its identity and
History. A new Spec, chat or operation does not by itself need a new article.
Create an article only when no existing article owns the capability.

Completion is a capture point, not the end of maintenance. Several Specs may
contribute to one feature article; preserve each source and its actual limits.
The collection exists in every Workbench and may be empty.

## When An Article Is Written

A Spec is captured after it is `complete` and before any of its records are
retired or discarded. Capture is not a gate on `complete`: a Spec whose
capture has not happened, or failed, stays `complete` and uncaptured, and
`doctor` reports a Spec completed with recorded main verification and no
captured article as attention (`uncaptured-complete`). Retirement
(`spec-workbench.mjs retire-spec S-### --wiki <note>`) takes the captured
article as the Spec's durable owner, and Task records, including missed
attempts, are never discarded before their parent Spec is captured.

Maintaining the article is part of ordinary authorized work. Later changes
update that same article before the operation finishes.

## What Qualifies

Source-backed knowledge transformed into prose a cold reader can use. Keep
observed behavior, evolving understanding and unresolved gaps distinct. Explain
progress and history with dated sources and links to live owners. Not a pasted Spec, a Task list, evidence rows, a Taskboard
projection or a completed Task standing in for the capability. Copied delivery
state is refused by the validator (`copied-task-state`); link to the retired
Spec instead.

## Article Shape

```markdown
---
type: feature
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - features capture at the closure point, YYYY-MM-DD
source_paths:
  - workbench/specs/retired/S-###-slug/SPEC.md
  - path/to/source-or-test
last_verified: YYYY-MM-DD
---

# [Capability Name]

[What was delivered, in one paragraph.]

## What It Does

## Why It Matters

## Limits

## Evidence and Sources

## History
```

- `History` is a dated list of what created and changed the article and the
  operation that authorized each change; see `SCHEMA.md` Update.
- `type: feature` belongs in this collection only; a note here of any other
  type, or a feature article anywhere else, is invalid.
- `knowledge_role` is `canonical` or `curated` for the article to serve as the
  Spec's retirement owner.
- For each contributing completed Spec, `source_paths` names its retired route,
  `workbench/specs/retired/<spec directory>/SPEC.md`, which is the provenance
  retirement and discard read, plus the source and tests that prove it.
- Name the article for the capability it explains, not for the identifier of
  the Spec that delivered it. Where it names an identifier, it also names the
  artifact and what it is for.
- Route every article from `MEMORY.md` with a relative link and a one-line
  summary beside it, so a reader can choose the article without opening it.
  This collection keeps no index of its own.
- Design Concept and guidebook notes remain valid retirement owners for
  earlier Specs; a Task record's discard waits for a features article.
