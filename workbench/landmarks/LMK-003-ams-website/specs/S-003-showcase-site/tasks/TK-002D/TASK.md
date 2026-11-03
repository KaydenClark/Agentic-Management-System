# TK-002D - Keyboard users fully see each focused navigation link

**Task ID:** TK-002D
**Spec ID:** S-003
**Slice:** Keyboard users fully see each focused navigation link
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Presentation, Route, Feedback
**Planned verification:** Reproduce and establish the recorded phone clipping cause; same80case matrix at375px/desktop,100/200-percent and both themes; affected browser checks, completed build and full site suite.
**Claimed by:** s003-frontend
**Current claimant:** s003-frontend
**Proof:** Source02a70b2fc3ed33444626293932ffb010ccd5b866: cause established from56baseline Tab observations with6clips persisting500ms; CSS-only experiment did not fix; explicit reveal fixed same nodes. Final handler scrolls only nav horizontally by measured delta. Completed build and217site tests pass;348affected browser checks including disabled-reveal negative control pass; same80navigation cases and56reverse-keyboard cases pass; console0. Root inspected final phone/dark200 and desktop/dark200 focused screenshots and scoped diff. Original failures remain preserved.

## Assignment

Kayden explicitly authorizes this focus correction only after PR148 stopped. Recover sourced929eeec1dd517132494797753a56abdd5f914a9, TK-001Q receipt and retained exact focus rectangles. Establish the root cause before choosing a repair. Distinguish source scrolling behavior from asynchronous observation; do not hide or relax the geometry requirement. Guarantee that every keyboard-focused menu link is fully visible in its scroll viewport, with visible focus and no sideways page movement, at normal/enlarged text in both themes.

Preserve the full-width sticky header, top-left Home icon, far-right theme control, current-page state, direct/clicked hash clearance, touch/no-script behavior, centered reading width and existing negative controls. No redesign, unrelated features, dependencies, palette work or shared-skill changes. s003-frontend owns site source/tests/docs; orchestrator owns all records. Complete one build before verification and freeze it during browser readers. Preserve all failed evidence. Return source commit, exact checks, screenshots, cause and both merge/completion answers before final PR148 current-head CI. Checked delivery is into dev only; never promote dev to main. This authorization does not waive a later three-strike stop.

## Acceptance

- [x] The recorded clipping cause is established with observable evidence; a focused link cannot remain partly outside its nav viewport.
- [x] Every keyboard link is fully visible at375px and desktop,100/200-percent, both themes; focus is visible and the page never scrolls sideways.
- [x] Existing header/Home/theme/sticky/hash/touch/no-script behavior and negative controls remain valid; build, full site suite and affected browser checks pass on the named candidate.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s003-navigation | 02a70b2fc3ed33444626293932ffb010ccd5b866 | ahead 0 behind 0 | 0 | Source02a70b2fc3ed33444626293932ffb010ccd5b866: cause established from56baseline Tab observations with6clips persisting500ms; CSS-only experiment did not fix; explicit reveal fixed same nodes. Final handler scrolls only nav horizontally by measured delta. Completed build and217site tests pass;348affected browser checks including disabled-reveal negative control pass; same80navigation cases and56reverse-keyboard cases pass; console0. Root inspected final phone/dark200 and desktop/dark200 focused screenshots and scoped diff. Original failures remain preserved. | ReadingNav focus handler, browser geometry detector/negative control and README; originalQ receipt remains; local diagnosis/final evidence retained | Local corrective acceptance met; exact-head CI and checked dev merge remain. OriginalQ incomplete run remains retained with later correction linked; native incomplete-run retirement unavailable. No Human QA, protected-deployment readback or production promotion claimed.; close attribution: {"agent":"s003-orchestrator","claimant":"s003-frontend","onBehalfOf":"s003-frontend"} | 10990440b63f0a403e81e81b5ff13526c21f471f4d4bf0d50c089922951ae320 |
