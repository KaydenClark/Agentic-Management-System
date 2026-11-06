# TK-0033 - Readers navigate the skills wiki in the current shell

**Task ID:** TK-0033
**Spec ID:** S-008
**Slice:** Inspect and recover PR #111 navigation on the current website shell
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: S-008 index and article navigation
**Planned verification:** Built-site tests and browser navigation across the index and all 39 articles; keyboard, anchor clearance, themes, narrow and wide viewports, enlarged text and scripts disabled.
**Claimed by:** codex-s008-navigation
**Current claimant:** codex-s008-navigation
**Proof:** At ac276e13d21628ea118e4dfed5e8e58739dc8d74, fresh build, 303 site tests, focused navigation 328/328 and full browser 2745/2745 pass; source review passed. At 9fd4c59ecf163a00c69176856e906fe01cf83c9d identical site tree 9364ae7fa6215d7352ae88078a8437d867bf92f2 and required python/site CI passed. Prior failures and both stop receipts retained.

## Assignment

Authority: [JOT-54c3a590-89e6-4bf7-95ef-4c50771e7ac8](../../../../../../wiki/context-website-presentation.md#jot-54c3a590-89e6-4bf7-95ef-4c50771e7ac8).

Inspect PR #111 head 85c993f91c03ed68cfd9c19945fb889853ec7118 against current dev and recover justified navigation, article contents links and linked start-page skill chips. Fit the current sticky header, focus behavior and tokens; preserve current shell and other owners' changes. Carry the bounded candidate through checks, QA and handback to dev. Do not change article content, page inventory, shared top-level navigation, private skills source or owner approval records. Prior Task receipts and whole-Spec Human QA remain distinct.

Workspace baseline sha256:df3974973671558bf9a64c9e27eb27afff1558b3e6fcbced627d5331c1658c50

## Acceptance

- [x] Index and all 39 articles expose reachable navigation and mark the current page; each article's contents links match its actual headings.
- [x] Start-page skill chips reach their corresponding articles; anchors and keyboard focus remain visible below the sticky header.
- [x] Navigation works at 375, 1280 and 1440 pixels, in both themes, with enlarged text and with scripts disabled; negative controls detect missing or incorrect links.
- [x] Current-base tests and browser QA pass without weakening checks; exact candidate and remaining limits are reported for independent review and dev containment.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-008-skills-wiki | cbbda7ee8a86ff505d5c7c2c218afc51895e7501 | ahead 0 behind 0 | 0 | Current-base site build and 287 tests pass; focused navigation browser 328 checks pass. Full browser stopped: six /governance axe color-contrast results undecided; no suppression. Root pytest across a moving checkout: 840 pass, 5 skip, 1 record-budget failure; focused hygiene passes after condensation. | S-008 Spec and Task; scoped website authority Jot. | Full browser rerun after S-010 correction, exact-head CI, independent review, native close and dev containment remain. Prior CSS zoom and misconfigured script-mode observations retained in handoff; PR151 enlarged-text matrix and Human QA remain separate. | de407ad7f057c43210d91e4cadfc86aeb5164eacdb8b2381ac3c248a2eb3dd04 |
| 2 | Feature/S-008-skills-wiki | 3cc34f626dcacdb1f0fcbbdcb77fcaeafb8e912b | ahead 0 behind 0 | 0 | At 3cc34f626dcacdb1f0fcbbdcb77fcaeafb8e912b: clean install, build and 303 site tests pass; focused navigation 328 checks pass. Full browser 2739/2745: six start-toy no-request checks observed route and skill _rsc requests in the interaction window; cause unproven. Previously failing governance contrast passes six cases. | S-008 Task; original stop receipt retained. | Coordinated diagnosis and correction of no-request failures, current-base full browser, exact-head CI, independent review, native close and dev containment remain. Human QA and PR151 historical matrix remain separate. | badbf1016b7fd3c337ad64f4446a6018073ea4121fd1dd989ae18750d7d1d9c7 |
| 3 | Feature/S-008-skills-wiki | 49e6aa4df23e5c0654f9b551945344ac6c47a7a7 | ahead 3 behind 0 | 0 | At ac276e13d21628ea118e4dfed5e8e58739dc8d74: fresh build and 303 site tests pass; navigation matrix 328/328; full browser 2745/2745 including original request and focus controls; exact-head python and site CI pass. At 49e6aa4df23e5c0654f9b551945344ac6c47a7a7 the site tree is identical; dev merge changes evidence records only. | S-008 Task and preserved earlier receipts. | Independent assembled review and dev containment remain with orchestrator. Native workspace check incomplete: retained refs, ignored evidence and missing discovery route; private verified originals retained. PR151 historical matrix and Human QA remain separate. | 3964d957f0051155749302f60686c37711bb62fe03818557d7e9341bc04b4286 |
| 4 | Feature/S-008-skills-wiki | 9fd4c59ecf163a00c69176856e906fe01cf83c9d | ahead 0 behind 0 | 0 | At ac276e13d21628ea118e4dfed5e8e58739dc8d74, fresh build, 303 site tests, focused navigation 328/328 and full browser 2745/2745 pass; source review passed. At 9fd4c59ecf163a00c69176856e906fe01cf83c9d identical site tree 9364ae7fa6215d7352ae88078a8437d867bf92f2 and required python/site CI passed. Prior failures and both stop receipts retained. | S-008 Spec and Task; owner authority Jot and generated Taskboard. | Orchestrator review and dev containment; final close-record CI. Workspace closeout remains incomplete for retained refs, ignored evidence and discovery route; private originals retained. PR151 historical matrix, S-008 Human QA and owner dev-to-main promotion remain separate.; close attribution: {"agent":"codex-s008-navigation","claimant":"codex-s008-navigation","onBehalfOf":null} | 0bfd10ba9e2efa9d64d80a6886da70e7e107418ff8cc657109b80c321ddb1583 |
