# TK-0033 - Readers navigate the skills wiki in the current shell

**Task ID:** TK-0033
**Spec ID:** S-008
**Slice:** Inspect and recover PR #111 navigation on the current website shell
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: S-008 index and article navigation
**Planned verification:** Built-site tests and browser navigation across the index and all 39 articles; keyboard, anchor clearance, themes, narrow and wide viewports, enlarged text and scripts disabled.
**Claimed by:** codex-s008-navigation
**Current claimant:** codex-s008-navigation

## Assignment

Authority: [JOT-54c3a590-89e6-4bf7-95ef-4c50771e7ac8](../../../../../../wiki/context-website-presentation.md#jot-54c3a590-89e6-4bf7-95ef-4c50771e7ac8).

Inspect PR #111 head 85c993f91c03ed68cfd9c19945fb889853ec7118 against current dev and recover justified navigation, article contents links and linked start-page skill chips. Fit the current sticky header, focus behavior and tokens; preserve current shell and other owners' changes. Carry the bounded candidate through checks, QA and handback to dev. Do not change article content, page inventory, shared top-level navigation, private skills source or owner approval records. Prior Task receipts and whole-Spec Human QA remain distinct.

Workspace baseline sha256:df3974973671558bf9a64c9e27eb27afff1558b3e6fcbced627d5331c1658c50

## Acceptance

- [ ] Index and all 39 articles expose reachable navigation and mark the current page; each article's contents links match its actual headings.
- [ ] Start-page skill chips reach their corresponding articles; anchors and keyboard focus remain visible below the sticky header.
- [ ] Navigation works at 375, 1280 and 1440 pixels, in both themes, with enlarged text and with scripts disabled; negative controls detect missing or incorrect links.
- [ ] Current-base tests and browser QA pass without weakening checks; exact candidate and remaining limits are reported for independent review and dev containment.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-008-skills-wiki | cbbda7ee8a86ff505d5c7c2c218afc51895e7501 | ahead 0 behind 0 | 0 | Current-base site build and 287 tests pass; focused navigation browser 328 checks pass. Full browser stopped: six /governance axe color-contrast results undecided; no suppression. Root pytest across a moving checkout: 840 pass, 5 skip, 1 record-budget failure; focused hygiene passes after condensation. | S-008 Spec and Task; scoped website authority Jot. | Full browser rerun after S-010 correction, exact-head CI, independent review, native close and dev containment remain. Prior CSS zoom and misconfigured script-mode observations retained in handoff; PR151 enlarged-text matrix and Human QA remain separate. | de407ad7f057c43210d91e4cadfc86aeb5164eacdb8b2381ac3c248a2eb3dd04 |
