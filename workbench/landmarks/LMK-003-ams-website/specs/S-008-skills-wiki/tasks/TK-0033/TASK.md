# TK-0033 - Readers navigate the skills wiki in the current shell

**Task ID:** TK-0033
**Spec ID:** S-008
**Slice:** Inspect and recover PR #111 navigation on the current website shell
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: S-008 index and article navigation
**Planned verification:** Built-site tests and browser navigation across the index and all 39 articles; keyboard, anchor clearance, themes, narrow and wide viewports, enlarged text and scripts disabled.

## Assignment

Inspect PR #111 head 85c993f91c03ed68cfd9c19945fb889853ec7118 against current dev and recover justified navigation, article contents links and linked start-page skill chips. Fit the current sticky header, focus behavior and tokens; preserve current shell and other owners' changes. Carry the bounded candidate through checks, QA and handback to dev. Do not change article content, page inventory, shared top-level navigation, private skills source or owner approval records. Prior Task receipts and whole-Spec Human QA remain distinct.

## Acceptance

- [ ] Index and all 39 articles expose reachable navigation and mark the current page; each article's contents links match its actual headings.
- [ ] Start-page skill chips reach their corresponding articles; anchors and keyboard focus remain visible below the sticky header.
- [ ] Navigation works at 375, 1280 and 1440 pixels, in both themes, with enlarged text and with scripts disabled; negative controls detect missing or incorrect links.
- [ ] Current-base tests and browser QA pass without weakening checks; exact candidate and remaining limits are reported for independent review and dev containment.
