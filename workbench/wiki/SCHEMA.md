---
type: meta
status: active
sensitivity: normal
knowledge_role: canonical
provenance:
  - LLM Workbench template wiki
source_paths:
  - workbench/wiki
last_verified: 2026-11-01
---

# Wiki Schema and CRUD Contract

> Generated from LLM Workbench v3.2.2.

## Purpose And Ownership

The Wiki is the Workbench's persistent knowledge base. It preserves what we
know and think: evolving understanding, history, progress, lessons, rationale,
and unresolved context. Agents read the relevant articles when starting work
and reconcile changed knowledge into those same articles before finishing.
They preserve sources, uncertainty, and correction history. They create a new
article only when no existing article owns the subject. Authoritative rules,
live work records, and proof retain their owners and are linked from the Wiki.

This evolving synthesis is agent-written Markdown: summaries, entity pages,
concept pages, comparisons and an overview, plus small source-linked jots with
clearly labeled intent, findings, proposals and unresolved questions. A cold
start retrieves relevant context rather than loading the corpus. Progress
explanations link to live owners instead of copying Task rows or Spec evidence.
Legacy notepads remain readable sources and structured domain stores.

In Governance Plane terms a wiki page is Enduring Context, this schema is
Canon, and the wiki's raw sources are the claims that played the Actuality
role relative to the target in the operation just performed. Destination
Question Cards and landmark records keep the structured account with its
lineage and identifiers; the wiki is what they are summarized into, updated
whenever a card changes.

The wiki is not a Governance Plane and owns none. A note may document
Grounding or Enduring Context. A governing artifact may have a role as a whole
while its supporting claims remain distinct; a folder or role label grants no
instruction authority. Wiki content cannot
authorize a change to Actuality; only the current user request, `AGENTS.md`,
and the explicitly assigned spec instruct.

A recall/search index is derived from named sources and remains rebuildable;
it neither owns Wiki knowledge nor supplies authority. No recall database or
additional index service is required by this boundary.

## Profile And Collections

`workbench/manifest.json` declares the wiki profile:

- `project`: this room's `MEMORY.md` router, flat notes beside it, and the
  declared collections.
- `deployment`: the same, plus flat `[OWNER]/`, `Projects/`, and `Machine/`
  pointer collections for a multi-room deployment. One deployment has exactly
  one deployment-profile wiki.

Declared collections are `design-concepts/` (required to exist, may be empty),
`features/` (the maintained Feature catalog; capture at completion and update
the owning capability article as knowledge changes; additive, may be empty), `guidebooks/` (ordered procedures), and
`archive/` (historical, generated, superseded, and migration evidence). Every
collection is flat; only `archive/` may nest. `MEMORY.md` is the only router.

## Fresh Capture And Privacy

The `jot` skill owns small timely capture and bounded retrieval in an existing
topic page or a flat `context-TOPIC.md` note. Entry kind, state, source, author,
recorded time and linked supersession distinguish owner intent, observation,
inference, proposal, questions and verification. `confirmed` is sourced
knowledge or intent; it does not make a claim Canon or prove implementation.
Append corrections and retain the original claim and provenance.

New project context defaults to shared capture in its topic page, or a flat
`context-TOPIC.md` page linked from `MEMORY.md`. Publish those pages with the
authorized work so a fresh clone can recover the context and relevant owner.
Review sources before capture; keep private material out of shared pages.
Explicit private capture uses hidden `.jot-private-TOPIC.md` files, ignored and
untracked, with local retrieval opting in. Private pages stay out of shared
discovery, validation, generated bundles and public readers. A `sensitivity`
label alone does not enforce access. Preserve legacy originals; private-to-
tracked migration requires specific exposure approval. Shared migration proof
uses synthetic fixtures. The Board's structured private answers retain their
legacy domain schema and storage.

## Page Kinds

Five kinds of page, mapped onto the collections below. This is a first cut
and may be revised when something does not fit.

- **Overview**: `MEMORY.md`, the router, carrying a one-line summary beside
  every link so a reader can choose a page without opening it. Write a list
  entry as `- [Schema](SCHEMA.md) - what the page is for` (the link, a dash, an
  en or em dash or a colon, then at least two words), or give a table row a second cell that
  says what the page is for. `wiki.mjs validate` reports a routed Wiki page
  without one as attention (`unsummarized-route`), never as a failure.
- **Synthesis**: one evolving page per landmark, in `design-concepts/`,
  summarizing that landmark's question cards and what they add up to.
- **Entity pages**: one page per capability (`features/`), and per skill,
  role, stance and tool (flat notes beside the router).
- **Concept pages**: durable cross-cutting models, in `design-concepts/`,
  and lexicon articles explaining glossary terms beyond their `GLOSSARY.md`
  definitions (see Lexicon Articles below).
- **Comparisons**: filed back as a flat note when answering a question
  produced one worth keeping.

## Lexicon Articles

A lexicon article explains terms whose canonical definition is a `**Term**:`
entry in the room's root `GLOSSARY.md`: the fuller meaning, how each term
differs from its neighbours and the sources that own it. It is never a link
stub, and it links `GLOSSARY.md`. The glossary owns the definition; the
article explains it and authorizes nothing.

The room ships with one grouped vocabulary article per glossary grouping,
flat beside the router as `vocabulary-<grouping>.md`, each term a section
headed exactly as its glossary entry, plus `ai-coding-reference.md` for
general AI coding words that need no glossary entry. `MEMORY.md` routes them
under Vocabulary. Extend the owning section when a shared word gains
explanation. A term of this project that needs more than a section gets its
own flat `dictionary-<term>.md` article, which declares the term in its
frontmatter, spelled exactly as the glossary entry, and links `GLOSSARY.md`:

```yaml
glossary_term: Landmark
```

`wiki.mjs validate` refuses (`invalid-note`) an article whose declared term is
not a glossary entry, one that does not link the root `GLOSSARY.md`, and one in
a room that has no `GLOSSARY.md`. A grouped vocabulary article and a general
reference page declare no term and need no single glossary entry.

An ordinary installed `GLOSSARY.md` also passes the complete pinned format
parser, even when no article declares a term. Duplicate entries, missing
definitions, extra sections and definitions beyond the sentence limit
produce `invalid-note` findings in Wiki validation and `doctor`. A legacy
room without a glossary remains valid unless an article declares a term.
Confirmed glossary promotion validates the proposed file against existing
Wiki term declarations before writing, so removing or renaming a referenced
term leaves the current glossary and promotion source unchanged.

## Required Properties

Every active note uses YAML frontmatter with:

```yaml
type: memory | project | person | machine | guidebook | design-concept | feature | meta
status: active | partial | stale | archived
sensitivity: normal | private | restricted
knowledge_role: canonical | curated | derived | historical
provenance:
  - who or what produced the note and when
source_paths:
  - repository/relative/path
last_verified: YYYY-MM-DD
```

- `knowledge_role` says how this note relates to other knowledge: `canonical`
  owns its knowledge class, `curated` is a maintained synthesis, `derived`
  is generated output that never outranks its inputs, `historical` is cold
  evidence retained for provenance. It is not a Governance Plane and grants
  no authority.
- `provenance` is attribution: the people, sessions, decisions, or imports the
  note came from. Keep it separate from `knowledge_role`.
- `sensitivity` is handling metadata only. It is not encryption and not an
  access control: `normal` notes may travel with the repository, `private`
  and `restricted` notes stay out of any generated bundle or external upload
  unless the owner opts in to a specific one. Credentials, tokens, keys,
  health, financial, and account material never enter the wiki at any
  sensitivity.
- `source_paths` are repository-relative and portable. Absolute paths belong
  only in explicitly local, ignored state.

## Create

- Create a note only when no existing active note owns the fact.
- Keep every collection flat; do not add category indexes.
- Do not create notes for temporary status or tasks. A chat answer that
  produced a durable summary, comparison or synthesis is filed as a page;
  a passing answer is not.
- Any agent, in any authorized operation, creates or updates the pages that
  operation touched. The operation's own authority covers its wiki update;
  no per-page approval exists. Only this schema needs the owner's explicit
  say. Record the authorizing operation in a Design Concept article's
  `authorized_by` and `History`; see `design-concepts/README.md`.
- At Spec completion, reconcile its useful knowledge into the existing Feature
  catalog article, creating one only for a capability with no owner. Later work
  updates that article; see `features/README.md`.

## Read

- Start at `MEMORY.md` and follow the smallest relevant link. Traverse first;
  search only when a route is missing, stale, or under explicit maintenance.
- Current work requires the live controls or verified runtime, never a note.
- Read `archive/` only for a targeted historical or provenance need.
- Restricted notes are opt-in and must be relevant to the user's request.

## Update

- Ingest at the exit of every operation. When a grilling session ends, a
  Task closes, a Spec completes, a decision is accepted or material is
  promoted, update every page that operation touched: the entity or concept
  page, the landmark synthesis, the overview line. One ingest usually
  touches several pages; expect that, not one.
- Identifiers are welcome: they are how agents link and find artifacts. No
  page references an identifier without the artifact's name or title and a
  little context about what it is for.
- Update the owning note rather than appending a second version elsewhere.
- Refresh `last_verified` only for facts actually checked in the current task.
- Label inferred claims with `Inference:` and dated claims with their date.
- Preserve unresolved contradictions explicitly until a higher-authority
  source is verified.
- Never copy live task rows, spec evidence, or generated Taskboard state into
  a note; link to the owner instead.

## Lint

At the end of a Wiki update, read touched pages and their affected routes for
contradictions, source coverage and accurate router summaries. At assembled
Spec review, run whole-Wiki structural validation and review the affected
pages against the changed controls. Broaden semantic review only where the
change reaches further pages; ordinary wording does not require rereading
all articles. Keep necessary corrections in the current Task; a new outcome
needs scope authority. A green validator is not semantic proof.

## Concurrency

The wiki is tracked in Git and updated on the agent's own branch like every
other owned document; Git reconciles. There is no writer lane, revision
stamp or lock. A same-paragraph collision between two lanes surfaces as a
merge conflict that the lane landing second resolves by reading both.

## Stale Handling

Mark a note `status: stale` when its sources moved, were superseded, or now
contradict it and no direct proof supports a repair. Staleness is visible and
nonblocking: an unrelated stale note never stops current work. Repair from
direct proof, record the change in the note's history, and clear the mark.

## Delete And Archive

- Delete only material proven duplicated, reproducible, or superseded.
- Move provenance-worthy source summaries into `archive/`.
- Git records ordinary revisions; `archive/` is for useful content, not every
  old file version.

## Links

- Markdown links are the portable syntax for control and source routes; they
  survive outside any editor.
- Obsidian `[[wikilinks]]` are optional between wiki-native notes. Obsidian is
  supported, never required; nothing in the wiki depends on a vault
  configuration existing.
- Note basenames must be unique across the wiki so shortest-form links resolve.

## Verification

```bash
node workbench/tools/wiki.mjs validate
node workbench/tools/wiki.mjs normalize
```

The validator checks the router, the declared collections, required
properties and enums, relative source paths, the Design Concept and features
article shapes, the absence of copied live task state and secret-like material,
and reports stale notes as attention. `validate` never writes.

`validate` reports wiki facts only. Two findings it used to carry are not wiki
facts and no longer come from here: `stale-seed`, for a seeded lane document
whose recorded generation is behind the manifest, and `unverified-provenance`,
for a manifest whose recorded source identity is a placeholder or disagrees with
`workbenchVersion`. `doctor` emits both, from the installed-state hook beside
its managed-runtime check; the checks themselves live in
`workbench/tools/workbench-layout.mjs` and are repaired by its `seed-documents`
and `record-source` commands. The `setup-workbench` skill's
check and repair states document them. Neither blocks.

`normalize` is the explicit repair for a note missing required properties. It
inserts only what is absent, never edits a body or overwrites a declared value,
and lists every note it changed. It fills the least-claiming values the schema
allows - `status: partial`, `knowledge_role: derived`, a `provenance` line
naming the normalization, the note's own path as `source_paths`, and
`last_verified` set to the day it ran - and infers `type` from the note's
location. Correct those values by hand afterwards; a Design Concept article
still needs its `authorized_by`, `parent`, and sections, and a
features article still needs its sections.
