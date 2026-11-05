---
type: memory
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - LLM Workbench template wiki: the glossary's Governance core grouping explained
  - Kayden's six-plane definitions, traversal order and Enduring Context correction, 2026-11-04
source_paths:
  - GLOSSARY.md
  - workbench/wiki/SCHEMA.md
last_verified: 2026-11-04
---

# Governance core: the vocabulary explained

These words explain AMS claim roles, what binds an agent, how disagreements
between governing claims and the running system resolve, and the Workbench's
lanes, collections and decision records.

The [glossary](../../GLOSSARY.md#governance-core) owns the stack definitions;
the [Wiki schema](SCHEMA.md#governance-stack) owns their use in Wiki operations.
This article explains the model and preserves the owner's corrections. It
authorizes nothing. Later sections retain other Workbench explanations;
their terms are not all entries in the current AMS glossary.

## Governance Plane

Planes classify claims relative to a target and operation, not whole artifacts.
One artifact may contain claims on several planes or only one. For example,
a Spec can contain desired outcomes, learned rationale, supporting test results
and governing acceptance criteria; those claims retain different roles.

Definition: [GLOSSARY.md, Governance core](../../GLOSSARY.md#governance-core).

## Governance Stack

Always display the complete stack downward in the order below, or upward in
its exact reverse, keeping the plane numbers attached. The numbers describe
how Kayden uses the stack, not a ranking for resolving contradictory claims.

| Plane | Meaning |
|---|---|
| 6. [Projection](#projection) | Snapshot summaries of each plane's claims at the last visit. |
| 5. [Intent](#intent) | What the owner wants. |
| 4. [Enduring Context](#enduring-context) | What we know about what exists, Canon, Grounding, Intent and what to do with it. |
| 3. [Grounding](#grounding) | Evidence and proofs establishing and supporting the source of truth. |
| 2. [Canon](#canon) | The authoritative source of truth. |
| 1. [Actuality](#actuality) | What exists and is being worked on. |

### Projection

A Projection summarizes each plane's claims as of the last time we were
there. A Wiki overview, Board card or work summary can present these snapshots.
Keep source revisions or observation times visible; reading a summary does not
refresh its underlying claims or prove that they still describe current state.

### Intent

Intent is what the owner wants, with reasons, boundaries, corrections and
confirmation status. A Projection helps the owner develop or revise Intent.
Recording whether that Intent was delivered does not rewrite what was wanted
or create a new owner confirmation, acceptance judgment or Human QA receipt.

### Enduring Context

Enduring Context is our knowledge: what we know about what exists; what the
source of truth and evidence say exists or should change; and what we know
about Intent and what to do with it. It includes rationale, uncertainty and
lessons, not just historical reference. The name remains Enduring Context.

### Grounding

Grounding is the evidence and proofs we use to establish and support the
authoritative source of truth. It informs justified changes to Canon and
Actuality. Record the candidate, source, actual result and limits; desired
results, summaries and recorded decisions do not by themselves supply proof.

### Canon

Canon is the authoritative source of truth for the target: what governs.
Knowledge and evidence inform changes to it within the authorized scope.
An implementation result can reveal a needed correction, but cannot silently
redefine Canon; a Canon claim alone does not prove that Actuality conforms.

### Actuality

Actuality is what exists and is being worked on. Inspect it directly when
current behavior matters. Change it using the authoritative source of truth,
what has been proven and what is known about the intended result.

### Downward And Upward Use

Downward, **6 → 5 → 4 → 3 → 2 → 1**: the owner views a Projection and creates
Intent; update Enduring Context with that Intent; use the knowledge to create
or review Grounding for changes; update Canon based on knowledge and proof;
then change Actuality based on Canon, Grounding and understood Intent.

Upward, **1 → 2 → 3 → 4 → 5 → 6**: inspect the changed Actuality; reconcile
Canon if needed; record the evidence and proofs from the work; update Enduring
Context with what now exists, what the source of truth says and what the new
evidence suggests; record Intent as delivered, partly delivered or not
delivered; then project the results with source times or revisions and gaps.

For example, a Wiki snapshot exposes an unclear definition. Kayden supplies
the intended meaning; the agent captures it, checks the affected sources,
updates the governing glossary/schema claims and repairs the existing Wiki.
Returning upward, it reconciles any further definition correction, records
validation results, updates the knowledge article, reports whether the
requested documentation was delivered, and summarizes the checked revisions.

This is a way to traverse the stack in either direction, not six mandatory
documents or approval gates. Each change stays within existing authority.

## Owner Correction And Sources

Kayden's [2026-11-04 instruction](#jot-687ce4ac-5a24-487f-8405-47872b0cce74)
corrects the earlier schema/article treatment of whole artifacts, supplies
the six definitions, fixes stack order and explains both directions of use.
It also retains Enduring Context after correcting the temporary alternate name.
The earlier [claim-role decision](../docs/adr/000L-governance-planes-are-roles-a-claim-plays-in-one-operation.md)
remains historical evidence; use the current glossary and schema for the
definitions and order. This documentation update does not establish a measured
RSI benefit or change the owner's release and acceptance boundaries.

## Workbench Contract

It is not a file; other root files are routed by intent, and no `CONTRACT.md` or other coequal root file exists.

## Instruction authority

An assigned spec cannot enlarge the request, platform safety, or `AGENTS.md` scope; an unassigned spec is evidence.

## State resolution

Neither "code always wins" nor "Canon proves implementation"; the touched owner is repaired rather than a universal precedence applied.

## No-governance-tax rule

Available mechanisms a change genuinely needs still apply; the line is availability, not ceremony.

## Diagnostic

The consuming command enforces the effect; no artifact chooses whether its own finding blocks.

## Support lane

A lane is a structural slot, not a plane.

## Skills lane

A skill this room adds under another name is room-owned and never replaced by the update; a personal skills catalog is never on this room's critical path.

## Collection

The full set: `docs/adr`, `wiki/design-concepts`, `wiki/guidebooks`, `wiki/archive`, `sessions/grilling`, `sessions/handoffs`, `sessions/checkpoints`, `sessions/notepads`, `sessions/notepads/templates`, `sessions/recovery`, and the additive `wiki/features` and `docs/ddr`.

Collection names are lowercase; local notepads may use nested type folders; a collection is never promoted to a lane because its contents differ in kind.

## ADR

Active accepted ADR decision claims are architectural Canon; rationale and history remain distinct; `canonicalized_in` names operational owners.

## Decision Record

Both are atomic, superseded whole and managed alike by one tool, `adr.mjs`, which creates, validates, registers, accepts, supersedes, deprecates and reads both. The test that chooses between them: would the choice still hold if the architecture were rebuilt differently? Yes is a DDR. One decision that needs both records links them rather than merging them.

## DDR

An active accepted DDR owns destination Canon beside the ADR; it serves a destination goal rather than an architecture choice. Lifecycle is its folder, as for an ADR: `proposed/`, the accepted top level, and the permanent `archive/`. `adr.mjs new --kind ddr` writes the next one into `proposed/`. A DDR that changes or contradicts the Blueprint names `BLUEPRINT.md` in `canonicalized_in`, which never names the Wiki; the Wiki cites it and keeps no page per DDR. It is not a Blueprint paragraph.

## Read words

Create, Read, Update and Delete remain the frame; what kind of each a tool needs differs. `capture` is Create, not a read. The decision-record tool answers all five for ADRs and DDRs; other tools gain them as they are revised, and existing command names keep working.

## Checkpoint

Preserve existing bytes and citations. New claims reconcile into their durable owners; operational recovery is separate.

## Operational recovery

Excluded from notepad discovery and durable provenance; existing historical recovery references remain valid.

## Design Concept article

It documents a design concept; it is not the Blueprint, an ADR, a procedure, or task state. Any agent creates or updates it in an authorized operation whose work touched it; the collection itself remains required.

## Wiki profile

A profile declares routing shape; it grants no authority and copies no live task state.

## Managed runtime tool

It is updated only by explicit update with backup and rollback; an application's root `tools/` is application-owned.

## Declared integration branch

A declaration, not a prose convention: tools and root files resolve it from the manifest, `doctor` reports it undeclared or missing without blocking selection, and only generation, adoption, and upgrade completion fail closed on it.

<!-- jot-entry -->
### JOT-687ce4ac-5a24-487f-8405-47872b0cce74
Kind: intent
State: confirmed
Recorded: 2026-11-05T03:39:59.913Z
Author: codex-wiki-governance
Source: Kayden, direct instructions and corrections in the Wiki governance-stack chat, 2026-11-04
Topic: vocabulary-governance-core
Supersedes: none

Kayden authorized updating the Wiki schema, glossary and related references. Claims within an artifact occupy planes; an artifact can contain claims from several planes or only one. Always present the numbered stack in ascending or descending order: 6 Projection, 5 Intent, 4 Enduring Context, 3 Grounding, 2 Canon, 1 Actuality. Enduring Context remains the name; the temporary wording Enduring Knowledge was corrected by Kayden. Canon is the authoritative source of truth. Grounding is the evidence and proofs used to establish and support that source of truth. Enduring Context is our knowledge about what exists, what Canon and evidence say exists or should change, and Intent and what to do with it. Projection is a snapshot summary of each plane’s claims as of the last time we were there. Downward use starts from a projection, develops Intent, updates knowledge, creates or reviews evidence, changes Canon based on knowledge and proof, and changes Actuality based on Canon, proof and understood Intent. Upward use starts from changed Actuality, reconciles Canon if needed, records proofs, updates knowledge, records Intent as delivered or not, and projects results. Stack traversal does not supply additional execution authority or owner acceptance. This supersedes the schema and vocabulary article passages assigning a plane to a whole artifact; historical evidence remains intact.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-0ad0d283-d165-4b0e-8cc9-9175c7c094f5
Kind: verification
State: current
Recorded: 2026-11-05T03:52:25.161Z
Author: codex-wiki-governance
Source: Codex local documentation readback and fresh-checkout checks, 2026-11-04; source candidate 3039e2220c99c0479ac43998edc4169beb952afa
Topic: vocabulary-governance-core
Supersedes: none

Local documentation now defines the six planes in 6-to-1 order, explains downward and upward use, treats planes as claim roles, preserves Enduring Context and makes Projection a dated/revisioned snapshot. All 22 original glossary terms remain; six new entries restore Governance Plane and the five previously missing plane definitions. The compact glossary retains intent development and DQC evolution within its 3000-character limit. Wiki, glossary, layout, decision-record, Taskboard and hygiene checks passed. A fresh checkout of source candidate 3039e22 passed 839 tests with 6 skipped after authorized localhost access; the sandboxed failure and rerun are retained in FAIL-104. Later edits only tighten glossary wording, order explanatory examples and record verification/publication limits. Doctor still reports unrelated existing claims, S-011 dependency, undeclared runtime surfaces and Claude permission drift; none establishes a stack-documentation defect. Publication was refused twice by automatic approval review (FAIL-102/103); the branch remains local with no PR or main merge. The requested documentation is implemented locally; checked public delivery awaits recognized owner approval, and no owner acceptance, browser QA or measured RSI benefit is claimed.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-14f25176-8c50-47f8-8089-2319e079f3a3
Kind: intent
State: confirmed
Recorded: 2026-11-05T04:13:00.328Z
Author: codex-wiki-governance
Source: Kayden direct approval in this Wiki governance-stack chat, 2026-11-04
Topic: vocabulary-governance-core
Supersedes: none

Kayden replied "I approve" directly to the request to publish codex/wiki-governance-stack to the public KaydenClark/Agentic-Management-System repository, open its PR into main, and merge after CI passes. This explicitly authorizes that bounded documentation delivery. The earlier failed publication attempts remain historical. The approval does not establish owner acceptance, Human QA, deployment or any broader release permission. Continue the checked non-site landing; retain all six definitions and the ordered stack unchanged.
<!-- /jot-entry -->
