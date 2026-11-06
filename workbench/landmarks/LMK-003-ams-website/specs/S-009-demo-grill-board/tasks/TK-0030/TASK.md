# TK-0030 - A visitor explores sample Grill Board decisions locally

**Task ID:** TK-0030
**Spec ID:** S-009
**Slice:** Recover the existing demo as a usable visitor experience with accurate current Board context
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: S-009 Acceptance Criteria
**Planned verification:** Built-site tests and browser interaction, storage and network checks at 375px and desktop in both themes; inspect script-disabled content and current S-004 behavior.
**Claimed by:** codex-s009-demo
**Current claimant:** codex-s009-demo
Workspace baseline sha256:4106561b4e83a48bea8672f3a5cf2bc2060c8dc44e40957a807543b68ddd3d15

The snapshot was captured at claim commit 3523bff before product work and its digest bound in e793ba6. The native-compatible literal above was corrected later in c023ef0; it was not present in that earlier binding commit.

## Assignment

Recover the existing S-009 prototype and preserve its source history. Deliver labeled everyday sample cards with Priority and Value reasons, rating and Too taxing, using S-004 signal colors. Interactions stay in memory and send or store no answers. Explain the current real Board lifecycle accurately. The S-003 writer owns shared navigation, tour, glossary and page inventory integration; return the route and source metadata for integration. Do not use real owner queue data.

## Acceptance

- [x] Visitors can inspect and interact with clearly labeled everyday samples; each card shows the required signals and reasons.
- [x] Demo interactions send and store nothing, and reloading clears them; existing site theme preference is separate.
- [x] The explanation distinguishes real current Board behavior from the local simulation and does not imply execution or application.
- [x] The page is usable at 375px and desktop in both themes, with readable core content when scripts are disabled.
- [x] The checked candidate and route metadata are handed back for S-003 integration and page review.

## Checked delivery and limits

Product candidate d5b015fe135153c1e35747093750b81d9e21c24d passed the site build, 275 site tests and 2461 browser checks. Its demo interactions and privacy checks also passed at the two complementary theme/viewport combinations, and phone-light and desktop-dark screenshots were inspected. The built d5b015f demo was additionally exercised for reload: sample rating, flag and note reset. The loopback-capable Python run passed 841 tests with 5 skipped; the restricted-sandbox failure remains in the canonical feedback log. Current dev retains the identical demo source files.

PR177 merged at 63870b54efba9b9028dc8c1ae194f3fef85138ae. PR178 delivered the page inventory at 40acb3a491a55599e5b1f00fd92a27315739a4a9 with S-009/TK-0030 and PR177's actual containment provenance. Both are contained in dev. This is the Task's metadata handback, not Human QA, Spec acceptance or protected-page verification. The dev deployment reported ERROR; platform-layout repair remains separate. Legacy TK-001/TK-002 and their proof remain for later reconciliation.

The original workspace snapshot and late literal correction above remain preserved. Its native preservation check reported accounted=false, remoteRecoverable=false and complete=false, with missing discovery route, retained refs not remotely verified and unselected ignored evidence. The workspace is retained; no release or full remote-recovery claim is made.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-009-demo-grill-board-page | 40acb3a491a55599e5b1f00fd92a27315739a4a9 | ahead 76 behind 0 | 1 | d5b015f site build; 275 site tests; 2461 browser checks and 2 complementary interaction/privacy checks; Python 841 passed 5 skipped with loopback; targeted built-demo reload reset passed. Current dev retains demo source bytes; PR177 and PR178 containment verified. | Task acceptance and delivery provenance; native snapshot and late binding preserved. | Spec acceptance, legacy Task reconciliation, independent Review, Human QA, protected deployment verification and owner-only main promotion remain. Dev deployment ERROR; platform repair separate. Workspace preservation check incomplete; workspace retained. | a97b46321ddb21e97e3ec225d141b315c4acdf90abf2ffa2475a3f55cecc7d02 |
