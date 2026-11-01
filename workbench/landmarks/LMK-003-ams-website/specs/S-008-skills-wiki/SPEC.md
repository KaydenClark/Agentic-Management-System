# S-008 - Skills wiki

**Spec ID:** S-008
**Status:** planned
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Site-written summaries of the owner's skills, one entry per skill, modeled on the format of aihero.dev/skills.
**Blockers:** S-003
**Latest event:** Entry shape revised to the owner's article template (2026-11-01).
**Next gate:** Task planning after the site shell (S-003) exists.

## Intent and authority

The owner chose site-written summaries of the owner's skills, modeled on https://www.aihero.dev/skills. The skills repository is private, so the site publishes summaries, not skill files.

On 2026-11-01 the owner set the article template (below) in chat, giving the reference site's `/grilling` page as the model of depth and tone, and supplied the chart of skills by Workbench stage, committed as `skills-by-workbench-stage.svg` beside this Spec. The chart is the authority for each skill's stage. `/start` screen 3 draws it from `site/app/start/skills.mjs`, which reaches `dev` through PR #87 and is not yet on `main`.

## Outcome

A reader can browse the skills that operate the AMS, see what each does, when to use it and what it does not authorize, and see which ones were actually used to build the site.

## Why It Matters

The skills are how agents operate the AMS. Explaining them faithfully, without publishing private files, shows the method behind the results.

## Current Verified State

- No wiki pages exist. The skills live in the owner's skills repository, outside this one.

## Desired Behavior

- An index of the owner's skills, grouped by workflow stage, and one entry per skill.
- Each entry is an article with these sections, in this order (the owner's template):
  1. **What it does**: the mechanism in plain words, with its key terms defined.
  2. **When to use it**: how it is invoked or reached for, and, where neighbours overlap, a table of "what you have / reach for" pointing to the right skill.
  3. **What it requires**: the skills, records, tools or Workbench it depends on.
  4. **Skill-specific sections**: only where the skill needs them (for example, the round and frontier of `grilling`).
  5. **FAQs**: the questions readers actually ask, each with a direct answer, including known failure modes and their workaround.
  6. **It's working when**: observable signs, as a list, that a run is behaving as designed.
  7. **Where it fits in the workflow**: its stage on the skills-by-stage chart, what calls it and what it hands to, linking those skills' entries.
- Each entry also carries a credit line: original, or adapted from a named source with its license.
- Each entry is derived from that skill's file at a pinned skills commit, and names the commit.
- "Used to build this site" appears only where a record links the skill to a Task or review.
- Layout follows the reference site's format; the exact elements are confirmed against that page at Task planning.

## Decisions And Contracts

- Summaries are written for the site; skill files are not copied.
- An adapted skill is credited to its source, never labeled original.
- The article template above is the owner's (2026-11-01); it replaces the earlier five-part entry (does, when, does not authorize, example request, provenance).

## Non-Goals

- Publishing the skills repository or any skill file.
- Editing skills; skill changes go through the skills repository's own process.

## Open Owner Choices

- Whether "what it does not authorize" and an example request stay, as lines inside the template's sections; the template does not list them.
- Whether the index groups entries by the seven stages of the skills-by-stage chart (Route, Align, Prepare, Journey, Judge, Complete, Improve), and whether the chart's skills are the owner's set.
- Which skills repository and path the authoring session reads at a pinned commit.
- Whether TK-001 may start on the site shell already on `dev` before S-003 completes.
- One index page plus one page per skill (`/skills/<name>`), as on the reference site.
- Whether TK-003's "used to build this site" marks stay in this Spec.

## Dependencies And Blockers

- S-003 (site shell); a pinned skills commit readable by the authoring session.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Skills index page and one complete entry from a pinned skill, deployed to `dev` | ready | none | pending |
| TK-002 | Entries for every skill in the owner's set, grouped by stage | ready | TK-001 | pending |
| TK-003 | "Used to build this site" marks driven by Task and review records | ready | TK-002 | pending |

### TK-001 - First entry

**Stance:** Builder

Proves the entry-shape and pin criteria on one skill.

### TK-002 - Full set

**Stance:** Builder

Proves the coverage criterion.

### TK-003 - Used marks

**Stance:** Builder

Proves the "used" criterion.

## Acceptance Criteria

- [ ] **Entry shape.** Every entry has the template's six required sections in order (skill-specific sections optional, placed after What it requires), a credit line, and names its skills commit. *Check:* a content test over entries. *Must fail:* an entry with no FAQs or no "It's working when" section, or with sections out of order.
- [ ] **Faithful.** Each described behavior appears in the pinned skill file. *Check:* a reviewer compares entries with the pinned files. *Must fail:* a behavior the skill does not have.
- [ ] **Coverage.** Every skill in the owner's set has an entry and every stage names at least one skill. *Must fail:* an orphan stage.
- [ ] **Used means recorded.** A "used" mark links the Task or review record. *Must fail:* a mark with no record.
- [ ] **No private files.** The hygiene check finds no copied skill file content beyond short quoted lines. *Must fail:* a skill file reproduced on the site.

## RSI and website connection

Skill changes measured by the loop (S-002, S-011) update the affected entries at the new pin.

## Testing Seams

- Content tests over the built entries; a pin comparison against the skills commit.

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

## Review and Human QA

The owner reviews the wiki pages through their Grill Board cards (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
