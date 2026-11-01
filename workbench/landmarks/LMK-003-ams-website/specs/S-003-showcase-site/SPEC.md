# S-003 - Showcase site shell and orientation tour

**Spec ID:** S-003
**Status:** planned
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The Next.js site shell in `site/` and the orientation tour that explains the AMS to a reader who knows nothing about agents.
**Blockers:** none
**Latest event:** Ported from the pre-repository draft and rewritten from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning.

## Intent and authority

The owner asked for a public site that shows off the system, explains how to use it, why and its benefits, and keeps the owner's voice and intent alive; it should be no more than a presentation website. Confirmed 2026-11-01: Next.js on Vercel at a free `*.vercel.app` address, Python backends, Supabase, no FastAPI; site work goes feature -> `dev` -> `main`. Orchestrator A deploys only through Git pushes to `dev`, browses no web and holds no Supabase service key.

## Outcome

A blog-style site with a reading order. Each page opens with a plain-language summary a non-engineer can follow, then goes deeper, so a CTO finds the architecture, guarantees, limits and evidence. This Spec owns the shell every page uses and the tour pages; other pages are sibling Specs.

## Why It Matters

The site is the owner's public piece and the owner's way back into the system. Built with the AMS, it is evidence of the AMS only if its claims trace to records.

## Current Verified State

- `site/` holds a placeholder and a page template; no Next app. The `dev` branch exists. No Vercel deployment serves this repository yet.

## Desired Behavior

- **Shell.** Navigation with reading position, light and dark following the system with a manual toggle, the old Grill Board's theme tokens, the deployed commit SHA on every page.
- **Tour pages.** Start here (what the AMS is and refuses to do); Why; How it works (records, lifecycle, one real Spec and Task); a short quickstart; Limits; Glossary; About with a resume summary.
- **Links to siblings.** RSI charts (S-007), skills wiki (S-008), demo Grill Board (S-009), governance stack and flow charts (S-010).
- **Data.** Anything dynamic, such as build history, is read from Supabase with the publishable key.
- **Voice.** Agents draft every page from the records and the voice and taste record (S-005). Owner words appear verbatim only with their source. Each page shows a draft mark until the owner approves it on the Grill Board.

## Decisions And Contracts

- Presentation only: the site runs no agents and edits no records.
- No third-party scripts, fonts, trackers or cookies; requests go only to the site, Supabase and GitHub links.
- Colors are signals with one stated meaning each; the complete token list is recorded in a theme decision record before the token check runs.
- Core page text renders on the server, readable with scripts disabled.

## Non-Goals

- A CMS, comments, accounts, analytics or a newsletter.
- A custom domain; a development view on Vercel.
- Publishing private skill content (summaries only, S-008).

## Dependencies And Blockers

- A Vercel project with production from `main` and a protected `dev` deployment (owner action).
- S-005 for page approvals; until it exists, approvals happen in chat.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Next app in `site/` with shell, theme tokens, light/dark and SHA footer, deployed to `dev` | ready | none | pending |
| TK-002 | Start here and How it works pages with plain-language openers and reading order | ready | TK-001 | pending |
| TK-003 | Why, Limits, Glossary, quickstart and About pages | ready | TK-002 | pending |
| TK-004 | Draft marks driven by hash-bound approval records | ready | TK-001 | pending |
| TK-005 | Hygiene, accessibility, 375 px and third-party checks on the built output | ready | TK-001 | pending |

### TK-001 - Shell on dev

**Stance:** Builder

Proves the theme, SHA and responsive criteria.

### TK-002 - First tour pages

**Stance:** Builder

Proves the opener and reading-order criteria.

### TK-003 - Remaining tour pages

**Stance:** Builder

Completes the page inventory.

### TK-004 - Draft marks

**Stance:** Builder

Proves the draft-mark criterion.

### TK-005 - Quality checks

**Stance:** Builder

Proves the hygiene, accessibility and no-third-party criteria.

## Acceptance Criteria

- [ ] **Pages exist.** Every tour page exists with a plain-language opener. *Check:* page inventory test. *Must fail:* a placeholder page or an opener using an undefined term.
- [ ] **Reading order.** Every page links forward and back. *Must fail:* a dead end.
- [ ] **Theme tokens.** Every color, type and spacing value equals the recorded Grill Board token. *Check:* token comparison script. *Must fail:* a color not in the token list.
- [ ] **Responsive and accessible.** No horizontal scroll at 375 px; WCAG AA contrast; keyboard navigable; reduced motion respected; both themes at both widths. *Check:* browser screenshots of the `dev` deployment plus an automated accessibility pass.
- [ ] **SHA on every page.** The shown SHA equals the deployed commit and links to GitHub. *Must fail:* a page whose SHA differs from the deployment.
- [ ] **No third parties.** Network inspection shows requests only to the site, Supabase and GitHub links. *Must fail:* an external font or script.
- [ ] **Public hygiene.** The hygiene check passes on every candidate. *Must fail:* a host path or key in the built output.
- [ ] **Owner words.** Each quoted owner statement links its dated source. *Must fail:* a paraphrase presented as a quote.
- [ ] **Draft marks.** A page shows a draft mark until an approval bound to its content hash exists; editing restores it. *Must fail:* an approved mark on changed content.
- [ ] **Quickstart replays.** A test runs the quickstart's commands on a fresh clone and gets the shown output.

## RSI and website connection

The build of this site is the loop's first trial (S-002). Truthful claims link a decision record, criterion, Supabase row or sourced owner statement.

## Testing Seams

- The built output and the `dev` deployment, never the source tree: inventory, link, token, hygiene and draft-mark tests; browser checks.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-003
# site build and test commands named at Task planning
```

## Documentation Impact

- RUNBOOK names the site build and test commands; ARCHITECTURE adds `site/`.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Ported and rewritten from confirmed decisions | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner approves each page on the Grill Board and alone merges `dev` -> `main`.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Video walkthroughs remain an open owner choice.

## Supersession

- Supersedes: the pre-repository draft of S-003.
- Superseded by: none
