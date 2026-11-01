---
name: map
summary: Writes the finished result you want as a checkable destination, such as a Spec, so a reviewer can judge the work without having been in the conversation.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's To Spec](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/to-spec) and Kayden Clark's Workbench Map, MIT License, using the project's own destination records and authority instead of automatic tracker activation.
credit_license: MIT
---

## What it does

Map turns intent you have already settled into a written **destination**: a description of the finished result precise enough that someone else can later say whether the work reached it. It describes where you are going, never how to get there. The route belongs to [plan](/skills/plan).

A **Workbench** is the structured project folder, created by [setup-workbench](/skills/setup-workbench), that holds the project's records. A **Spec** is the record that owns one capability and its acceptance criteria. A **Task** is one assignment that carries out part of a Spec. Map writes or revises the destination owner at the right scale: a Spec, a **PRD** (what users or the product need), a **landmark** (a direction spanning several related capabilities), or the **Blueprint** (the project's audience, promised outcomes and boundaries, holding enduring direction rather than a list of current work).

The work runs in three moves.

1. **Recover, don't re-interview.** Map gathers what the conversation and sources already settled: problem, audience, outcome, scope, exclusions, and how far documentation or publication may go. It keeps corrections and earlier decisions. It also reads project instructions, glossary, decisions, code, tests and existing records, and keeps four things apart: verified current behavior, reports someone made, desired behavior, and unknowns. If it could not cover all the source, it says so.
2. **Pick the existing owner.** It reuses the record that already owns the capability, rather than spawning a Spec per file or verb, a parallel requirements list, or an oversized template.
3. **Write something auditable.** The result covers the problem and why it matters, evidence for current behavior, requirements and non-goals, accepted decisions and public contracts, checkable acceptance examples, dependencies, assumptions and open choices.

Two habits matter. Every requested requirement must land in acceptance or a named dependency; unfinished work may not quietly become an exclusion. And acceptance includes a plausible wrong result that must fail, so the check can tell success from near-success. Map prefers the highest practical public test seam, reuses approved testing decisions, and takes any materially new seam choice to the owner.

A new Spec starts with the template's sample Task rows removed, evidence only appended to, and its completion result left pending. Map never records tests or implementation that did not happen. If the code lacks something a newer accepted requirement asks for, that is an implementation gap, not a reason to weaken the destination.

## When to use it

Reach for Map when you need to write or revise a destination document and the intent is settled enough to write down. Invoking it is neither a confirmation nor an execution approval; if the project's controls lack either, Map does not supply it.

| What you have | Reach for |
|---|---|
| A fuzzy idea you want challenged first | [grilling](/skills/grilling) |
| Settled meaning you want restated for sign-off | [readback](/skills/readback) |
| A Spec that is ready and needs to become Tasks | [plan](/skills/plan) |
| Unclear or overloaded project terms | [domain-modeling](/skills/domain-modeling) |
| A decision that needs durable evidence behind it | [research](/skills/research) |

## Example request

> We've agreed the export feature should let people download their data as CSV, admins included, with no scheduled exports for now. Map that into a Spec. Update the existing exports Spec if there is one, and stop before planning.

Map would find the existing owner, write the outcome, the scheduling non-goal and acceptance examples including a wrong result that must fail, then return the path, status and gaps.

## What it requires

- A Workbench. Map first checks for the manifest and the Workbench tool; if either is missing it stops and tells you to run setup-workbench. It will not create records by hand or use another tracker.
- Settled intent and an agreed place to save or publish.
- For a new Spec, an ID proposed by the Workbench tool's read-only next-id command. A proposal does not claim the ID, so Map rechecks for concurrent allocation and saves through the project's authorized writer.
- Existing validators, run through that same writer, to check IDs, structure, links, status and fidelity to sources.

## What it does not authorize

- No Tasks. A new Spec is created as planned, with no owner claim, no Task and an empty tasks folder.
- No activation, claim or **Journey** (the run that takes one Task through implementation and checks). Starting build work needs separate authorization.
- No confirmation or execution approval the project hasn't given. Those stay distinct from each other and from review and **Human QA** (a person's hands-on quality check).
- No planning by implication. If both are authorized, the Map is preserved at its required publication boundary before Plan starts.
- A local file or a draft pull request is not proof the Spec arrived on the target branch. Map separates local work, review-branch publication and checked integration.

## Checking before it returns

Map compares the artifact against every applicable source and correction, and asks whether an independent reviewer could identify success, failure, boundaries and uncertainty without the conversation. It saves within the agreed endpoint and reads the saved owner back.

For publication it expects the committed tree to pass the Workbench's render and doctor (validation) commands, and the pull request record to count Specs, Tasks and empty tasks folders against the real target. Map fetches the target first, because doctor does not fetch, and validates the saved Map record with doctor before claiming checked publication.

It returns the path or link, status, covered acceptance, gaps, and the next authorized step: Plan if the Spec is ready, otherwise the specific decision still missing.

## FAQs

### Does Map decide how to build the thing?

No. It keeps settled technical decisions and public contracts, and may include a prototype shape taken from a real source, trimmed to the decision-rich parts, when that states a contract better than prose. It does not invent build steps, allocate Tasks or schedule anything.

### What if the conversation left a requirement unresolved?

Map names it as an open owner choice or a dependency. It does not drop it or rewrite it to match what the code does today.

### What if a Spec for this capability already exists?

Map revises the existing owner and keeps its decisions and history. It does not overwrite conflicting intent or fit the text to the code.

### Why did it stop and tell me to run setup-workbench?

The manifest or tool file was missing. Map refuses to improvise records, so set up the Workbench and run Map again.

### Review failed. What now?

The work returns to the still-open owner, and the revision keeps open choices, handoff dependencies and correction history.

## It's working when

- The destination can be read cold by a reviewer, who can tell success, failure, boundaries and unknowns apart.
- Each requested requirement shows up in acceptance or a named dependency.
- Current behavior, desired behavior and unknowns are labeled separately.
- Acceptance includes at least one plausible wrong result that must fail.
- A new Spec exists with zero Tasks and an empty tasks folder.
- Existing decisions and corrections survived the edit.
- The return message states path, status, gaps, the next authorized operation and the publication level reached.

## Where it fits in the workflow

Map is the first half of the **Prepare** stage (Map and Plan). It usually follows the Align stage, where [grilling](/skills/grilling) and [readback](/skills/readback) build and confirm shared understanding, and is also fed by [domain-modeling](/skills/domain-modeling) and [research](/skills/research) when needed. It hands a ready destination to [plan](/skills/plan), which breaks it into Tasks; if the destination is not ready, it hands back the specific missing decision instead.
