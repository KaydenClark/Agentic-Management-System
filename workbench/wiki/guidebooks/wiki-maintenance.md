---
type: guidebook
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - S-000C maintained Wiki repair, 2026-11-04
source_paths:
  - workbench/wiki/SCHEMA.md
  - workbench/wiki/design-concepts/README.md
  - workbench/wiki/features/README.md
  - workbench/docs/SKILLS.md
last_verified: 2026-11-04
---

# Maintain useful Wiki understanding

Use this procedure during ordinary authorized work, after a material source change or when a query produces durable understanding. It makes [the existing schema](../SCHEMA.md#update) concrete; it adds no execution gate or service. Begin at [MEMORY](../MEMORY.md), then read the relevant explanation and its governing sources. Native `jot read` returns entries, not the surrounding explanation: read both when the question needs both. [SKILLS](../../docs/SKILLS.md#wiki-maintenance) routes this procedure from the working instructions.

## Intake a source safely

Find the smallest existing topic/capability owner first. Record who produced the source, its date, what was inspected, an immutable commit/revision or an authorized snapshot with digest, exposure classification and uncertainty. Use repository-relative paths plus commit-pinned links for public project material; retain a live owner link for future changes. A moving URL or a copied claim that a revision exists is not verification of its contents. Distinguish direct inspection from a named upstream report and name access limits. Do not fetch private sources merely to fill a public explanation, copy raw transcripts, or publish local attachment/recovery paths. If a source is unavailable, limit the affected claim; do not invent its content.

For fresh captures use the actual native interface, reading its returned revision before a write:

```sh
node workbench/tools/jot.mjs read --page workbench/wiki/context-TOPIC.md --limit 8 --max-chars 6000
node workbench/tools/jot.mjs add --page workbench/wiki/context-TOPIC.md --visibility shared --revision ACTUAL_REVISION --kind observation --state current --source SAFE_SOURCE --author ACTUAL_AUTHOR --content "Sourced finding, limits and affected owners"
```

The uppercase values are placeholders, not runnable source identities. Refusal saves nothing: reread and reconcile before retrying. An observation is not owner confirmation. Exact owner readbacks, reasons and confirmation text retain their own owners and bytes.

## Ingest into understanding

Read the current explanation against the new source and its corrections. Reconcile the meaningful change into that same explanation: what it means, why, what is established, what remains unresolved and how it relates to other concepts. A jot alone does not finish ingest. Preserve historical observations with their dates/candidates; explain supersession above or alongside them rather than silently rewriting them as current. Update the affected Landmark synthesis, incoming/outgoing crosslinks and MEMORY's one-line summary in the same change. If no claim changed, record that conclusion and why the source adds no new understanding rather than adding duplicate prose.

Create a topic only when no sufficient owner exists. A new Task is not a new topic. Ordinary topic capture may reuse a sufficient current owner without filling the Feature catalog. Spec-completion capture and retirement retain the separate requirements in [the Feature contract](../features/README.md#when-an-article-is-written) and [schema Create](../SCHEMA.md#create); this procedure grants no exception to them. [Landmark articles](../design-concepts/README.md#landmark-synthesis-pages) summarize confirmed card answers, distinguish unconfirmed/inferred material and cite every affected DQC by ID and title. When a Landmark has no cards, say so; do not manufacture answers. Link live Specs/Tasks and their proof instead of copying execution rows. Lifecycle history stays in native history pages.

## File a durable query answer

Answer from the routed current explanation and the smallest necessary source set. When the answer would save another reader reconstruction, file it in the existing owner as explanation or comparison, with evidence and limits. Reconcile affected Landmark/routes just as for ingest. For example, “Does delivered DQC lifecycle mean the redesign is complete?” belongs in [Grill Board](../context-grilling-board.md#established-behavior-and-remaining-gap): lifecycle delivery and later working-control requirements are different claims. Its [Landmark synthesis](../design-concepts/landmark-grill-board.md#open-and-unresolved) and MEMORY summary must expose the same gap. A transient answer needs no new page.

## Correct and check the affected meaning

For a native entry correction, use `jot correct` with the actual latest `--revision` and `--supersedes ENTRY_ID`; retain the original entry and source. Update the current explanation, affected summaries and links as well. Do not mark agent/synthetic material as human-confirmed. A pending owner-intent change cannot supersede an exact confirmed readback without the owner's actual revised confirmation.

Before finishing, read touched explanations and their affected routes against the governing sources. Check for contradictory current claims, old certainty resurfacing, missing source coverage, broken/orphan links, misleading summaries and accidental copied work state. Trace a representative question from MEMORY and state the answer and limits using that route. Run `node workbench/tools/wiki.mjs validate`, relevant native diagnostics and the Runbook checks for the candidate. Structural green proves shape, not faithful meaning. Broaden semantic inspection only along relationships the change affects.

For a correction exercise, copy only the needed public source pages into an isolated disposable fixture outside the working checkout. Label all planted claims and corrections synthetic. Introduce a contradiction between source, current explanation and an affected route; read and detect it before repair. Apply the correction to the actual explanation, relevant summary/link and retained history. Read the answer again through the corrected route and prove the earlier source bytes remain. A successful exercise establishes that bounded maintenance path, not clean-baseline improvement, generalization or owner acceptance. Record its real result and limitations in the assigned work owner.

## History

- 2026-11-04: S-000C repair connected existing schema/Jot rules to an operational intake, ingest, durable-query and semantic-correction path; no new mandatory framework or product change.
