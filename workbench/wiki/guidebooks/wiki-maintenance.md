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

## Recover and check with ams-memory

```sh
uv run ams-memory query "Wiki memory independent Landmark owner correction" --json
uv run ams-memory query "AMS reusable workflows purpose" --limit 3 --max-chars 12000
uv run ams-memory check --json
```

Query reads MEMORY first, ranks up to three matching routes, then uses bounded fallback only when those routes yield no matching sections/entries. Eligible flat Wiki topics and declared article/history collections are searched; hidden/ignored/private/restricted pages and archive are excluded. Malformed handling, bindings or Jots exclude that page with a reason. A matched route may omit other relevant pages: follow the returned pointers. Ranking is deterministic keyword overlap, requiring two distinct terms for multiword queries; it is no semantic answer judge.

The default limit is6 and full JSON bound6400 characters; supported limits are1–20 and1000–48000 characters. Results retain title, heading, state, revision digest, route and source pointers. Clipped claim/correction text is labeled; read its named page/anchor or increase the bound to recover it. Old entries remain superseded context, never current hits. References are identities; query does not recursively ingest their bodies. There is no durable index or cache to maintain.

Claim bindings use one JSON object (`version: 1`, `claims: [...]`) in an HTML comment named `ams-memory-bindings`. Each claim has a stable `id`, explanation `anchor`, optional `supersedes` and `sources`. Each source declares its repository-relative `identity`, explicit `reviewed_public: true` and retained `observations` (`sha256`, inspected Git `revision`, `observed_at` date). Several claims/sources can share a page. The [Wiki topic](../context-wiki-maintenance.md) and [AMS purpose](../context-ams-purpose.md) contain inspected examples, including retained source supersession.

Fingerprint only reviewed, tracked public Markdown. Supported sources are eligible Wiki notes, named root controls and project docs/Spec/Landmark records; ignored/hidden/symlink/private/restricted paths and unsupported external bodies refuse. A Jot anchor fingerprints its exact retained block. Other heading anchors fingerprint that heading's subtree through the next equal/higher heading, with repeated headings suffixed `-1`, `-2`, matching retrieval anchors. Visible historical Jot headings still count in actual page anchors when maintained text is retrieved separately. Sources without anchors fingerprint the complete reviewed file. Inspect the actual source before recording metadata; metadata alone grants no exposure authority.

`check` reports each bound explanation as unchanged, possibly-stale, missing or unavailable; pages without bindings remain explicitly unbound. It writes nothing and never refreshes dates/confirmations. To distinguish returned bytes from an intervening edit, save a check result in ignored local recovery, then run `check --previous SAVED_JSON --json`; `SAVED_JSON` is the actual prior result path. Matching a prior historical observation is `restored-historical`, still requiring review. Restored bytes prove neither truth nor acceptance.

The [development evaluation](../../../evals/wiki-memory/README.md) compares pinned navigation/native-Jot context with candidate retrieval on identical sources and bounds. Independent answers, stale-answer repetition and owner effort remain unmeasured. Consolidation, function/detail bundles and fresh-agent evaluation retain their assigned Tasks; this reader supplies no execution authority.

## History

- 2026-11-04: S-000C repair connected existing schema/Jot rules to an operational intake, ingest, durable-query and semantic-correction path; no new mandatory framework or product change.
