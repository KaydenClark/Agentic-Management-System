# S-008 - Skills wiki

**Spec ID:** S-008
**Status:** active
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Site-written articles on the owner's skills, one page per skill grouped by Workbench stage, modeled on aihero.dev/skills.
**Blockers:** none
**Confirmation:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-001 claimed by Orchestrator (Claude Opus 5.5).
**Next gate:** Close TK-001 with verification and documentation proof.

## Intent and authority

The owner chose site-written articles on the owner's skills, modeled on https://www.aihero.dev/skills. The skills repository is private, so the site publishes articles written for it, not skill files.

On 2026-11-01, in chat, the owner:

- set the article template, giving the reference site's `/grilling` page as the model of depth and tone, then added an example request and a "does not authorize" section, each beside its partner;
- supplied the chart of skills by Workbench stage, committed as `skills-by-workbench-stage.svg` beside this Spec. The chart is the authority for each skill's stage. `/start` screen 3 draws it from `site/app/start/skills.mjs`, which reaches `dev` through PR #87 and is not yet on `main`;
- named the source as the owner's skills repository, `KaydenClark/skills` (private), covering every skill on the chart under its current name in that repository, so `grill-me` is `align-concept` and `grill-with-docs` is `align-docs`;
- chose stage grouping and an index plus one page per skill;
- ruled out "used to build this site" marks on the public site: that record belongs to the Supabase backend and GitHub, not the wiki;
- asked for this Spec to be finished and implementation not started.

## Outcome

A reader can browse the skills that operate the AMS by Workbench stage, open any one, and learn what it does, when to reach for it, what it needs and refuses, how to tell it is working and where it fits in the workflow.

## Why It Matters

The skills are how agents operate the AMS. Explaining them faithfully, without publishing private files, shows the method behind the results.

## Current Verified State

- No wiki pages exist.
- `KaydenClark/skills` is private; at commit `878241202bf7ec97c0952287f1633f6f0ddf1a6e` (2026-11-01) every skill on the chart is a top-level skill directory, with `grill-me` and `grill-with-docs` renamed `align-concept` and `align-docs`. Four top-level skills are not on the chart (`clean-my-ai-harness-codex`, `obsidian-vault`, `ponder`, `teach`). The repository has a `THIRD_PARTY_NOTICES.md` and no root `LICENSE`.
- The chart (`skills-by-workbench-stage.svg`) still shows the old names `grill-me` and `grill-with-docs`.

## Desired Behavior

- **Set.** One article for each skill on the chart, under its name in the skills repository at the pinned commit: 39 skills at commit `8782412` (Route 5, Align 12, Prepare 2, Journey 7, Judge 1, Complete 4, Improve 8). Skills not on the chart get no article.
- **Index (`/skills`).** The skills grouped by the chart's seven stages in order (Route, Align, Prepare, Journey, Judge, Complete, Improve), each stage with its gloss, main-flow skills first in their order, then the others. Each skill shows its name and a one-line summary and links its article.
- **Article (`/skills/<name>`).** Sections in this order:
  1. **What it does**: the mechanism in plain words, with its key terms defined.
  2. **When to use it**: how it is invoked or reached for and, where neighbours overlap, a "what you have / reach for" table pointing to the right skill.
  3. **Example request**: one realistic request that would bring the skill in.
  4. **What it requires**: the skills, records, tools or Workbench it depends on.
  5. **What it does not authorize**: what running it never grants (for example, merging, publishing or Human QA).
  6. **Skill-specific sections**: only where the skill needs them (for example, the round and frontier of `grilling`).
  7. **FAQs**: the questions readers actually ask, each with a direct answer, including known failure modes and their workaround.
  8. **It's working when**: observable signs, as a list, that a run is behaving as designed.
  9. **Where it fits in the workflow**: its stage on the chart, what calls it and what it hands to, linking those skills' articles.
- **Credit.** Each article ends with a credit line: original to the owner, or adapted from a named source with its license, as the skill file and `THIRD_PARTY_NOTICES.md` state at the pin.
- **Pin.** Each article is derived from that skill's file at the pinned commit and names the commit. A later pin updates the affected articles.
- Layout follows the reference site's format; exact elements are confirmed against that page at Task planning.

## Decisions And Contracts

- Articles are written for the site; skill files are not copied.
- An adapted skill is credited to its source, never labeled original.
- The nine-section article above is the owner's (2026-11-01); it replaces the earlier five-part entry (does, when, does not authorize, example request, provenance).
- Stage membership comes from the chart; skill names come from the skills repository at the pin. Where they differ, the repository name is used and the chart is not edited by this Spec.
- No "used to build this site" marks: which skills built which work is recorded in the Supabase backend and on GitHub, not in the wiki (owner, 2026-11-01).

## Non-Goals

- Publishing the skills repository or any skill file.
- Editing skills; skill changes go through the skills repository's own process.
- Articles for skills not on the chart.
- Marking which skills were used to build the site.

## Dependencies And Blockers

- S-003 (site shell): satisfied for this Spec; the shell, theme and site tests are on `dev` (checked at `2a89fe4`, 2026-11-01). The owner's go-ahead is JOT-ba986c8a.
- Read access to `KaydenClark/skills` at the pinned commit for the authoring session.
- PR #87 (`skills.mjs` and `/start` screen 3) for the shared stage data: merged into `dev` 2026-11-01.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

### TK-001 - Index and first article

**Stance:** Builder

Proves the index, the article shape, credit and pin criteria on one skill.

### TK-002 - Full set

**Stance:** Builder

Proves the coverage criterion.

## Acceptance Criteria

- [ ] **Article shape.** Every article has sections 1-5 and 7-9 in order (skill-specific sections optional, between What it does not authorize and FAQs), a credit line, and names its skills commit. *Check:* a content test over the built articles. *Must fail:* an article with no FAQs, no "It's working when" or no "What it does not authorize", or with sections out of order.
- [ ] **Faithful.** Each described behavior, requirement and refusal appears in the pinned skill file. *Check:* a reviewer compares articles with the pinned files. *Must fail:* a behavior the skill does not have.
- [ ] **Coverage.** Every chart skill has an article under its repository name at the pin, and every stage names at least one skill. *Must fail:* a missing chart skill, an article named `grill-me`, an article for a skill not on the chart, or an orphan stage.
- [ ] **Index.** `/skills` lists every article under its chart stage, main-flow skills first in order, each linking its `/skills/<name>` page. *Must fail:* a skill under the wrong stage or an article with no index link.
- [ ] **Credit.** An adapted skill names its source and license. *Must fail:* an adapted skill labeled original.
- [ ] **No used marks.** No page marks a skill as used to build the site. *Must fail:* a "used" badge or list on any wiki page.
- [ ] **No private files.** The hygiene check finds no copied skill file content beyond short quoted lines. *Must fail:* a skill file reproduced on the site.

## RSI and website connection

Skill changes measured by the loop (S-002, S-011) update the affected articles at the new pin.

## Testing Seams

- Content tests over the built index and articles; a pin comparison against the skills commit; the existing site hygiene and browser checks.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-008
# site test command named at Task planning
```

## Documentation Impact

- The glossary links the wiki for skill names.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |
| 2026-11-01 | none | Entry shape revised to the owner's seven-section template; open choices listed | render, doctor | this Spec | Every criterion; open owner choices |
| 2026-11-01 | none | Owner settled the open choices: nine sections, stage grouping, chart skills at pin `8782412` under repository names, index plus page per skill, used marks dropped (TK-003 removed); implementation not started | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner reviews the wiki pages through their Grill Board cards (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- The chart image keeps the old names `grill-me` and `grill-with-docs` until the owner updates it.

## Supersession

- Supersedes: none
- Superseded by: none
