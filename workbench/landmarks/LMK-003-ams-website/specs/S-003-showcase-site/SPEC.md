# S-003 - Showcase site shell and orientation tour

**Spec ID:** S-003
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The Next.js site shell in `site/` and the orientation tour that explains the AMS to a reader who knows nothing about agents.
**Blockers:** none
**Confirmation:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-007 closed with proof.
**Next gate:** Complete TK-002.

## Intent and authority

The owner asked for a public site that shows off the system, explains how and why to use it, keeps the owner's voice, and is no more than a presentation website. Confirmed 2026-11-01: Next.js on Vercel at a free `*.vercel.app` address, Python backends, Supabase, no FastAPI; site work goes feature -> `dev` -> `main`. Orchestrator A deploys only through Git pushes to `dev`, browses no web and holds no Supabase service key.

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
- **Data.** Anything dynamic is read from Supabase with the publishable key.
- **Under the hood.** A page rendered from S-006's build-history rows shows how the AMS built this site: Specs, Tasks, PRs and commits in order, returns and corrections included. No history is hand-written, so the page is the site's proof it was made with the system.
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
- S-006 for build-history rows (TK-006).
- Open owner choice `grill-board-theme-tokens`: the old Grill Board's token values are outside this public repository; the owner supplies them or approves copying them before TK-007. Until then the shell keeps every value in one token file.

## Vertical Implementation Slices

Every Task targets `dev`: branch from `origin/dev` (it holds the Next scaffold in `site/`), PR into `dev`, and only the owner merges `dev` -> `main`. Stack: Next.js pages in `site/`, Supabase reads, the build, tests on the built output and the protected `dev` deployment.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

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
- [ ] **Under the hood from rows.** The page renders S-006 build-history rows in time order, returns and corrections included, each linking its source. *Check:* render against a fixture and against Supabase. *Must fail:* history text not from a row, or a hidden correction row.
- [ ] **Quickstart replays.** A test runs the quickstart's commands on a fresh clone and gets the shown output.

## RSI and website connection

Building this site is the loop's first trial (S-002). Claims link a decision record, criterion, Supabase row or sourced owner statement.

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
| 2026-11-01 | TK-001 | Task closed | PR #13 merged into dev as c529821; npm ci && npm run build && npm test 14/14 pass from a fresh clone (red 10/14 at 90559c8 first); check:browser 15/15 at 375px both themes, toggle overrides system and persists, self-hosted fonts, no off-site requests, home text without JS; Vercel dev deployment dpl_71NzXZ7rd77HgFsxAbgA1oVu7qsd READY at c529821; Codex code and security review no findings at 1fd680b | site/README.md documents npm ci, build, test, check:browser; tokens.css header cites the owner design canvas Color system v2.2 | Deployed footer SHA and home text not fetched from the dev deployment: the Vercel connector's web_fetch refuses this project (owner to extend connector access); contrast, keyboard and automated a11y pass belong to TK-005; tokens unverified against B's theme CDR until TK-007; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A-dispatcher-S003","onBehalfOf":"orchestrator-A-dispatcher-S003"} |
| 2026-11-01 | TK-007 | Task closed | PR #32 (9c37ebf) merged into demo batch site/demo-batch-20261102 for one dev merge; scripts/gen-tokens.mjs generates the tokens.css theme block from grill-board/theme/tokens.json (DDR-000Y); tests/tokens-json.test.mjs requires the block byte-equal to the generator, markers once at stylesheet top level, nothing recorded or color-like outside; red/green per Codex finding; Codex code and security clean at 9c37ebf; batch npm test 59/59, check:browser 149/149 | site/README.md Theme token check; npm run tokens:gen | Type and spacing tokens not in tokens.json so not compared; five mix meanings supplied by the generator until S-004 TK-003 records them; check runs in npm test and CI, not in the Vercel build; dev deployment content to be verified on the owner's machine; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A","onBehalfOf":"orchestrator-A"} |

## Review and Human QA

The owner approves each page on the Grill Board and alone merges `dev` -> `main`.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Video walkthroughs remain an open owner choice.

## Supersession

- Supersedes: the pre-repository draft of S-003.
- Superseded by: none
