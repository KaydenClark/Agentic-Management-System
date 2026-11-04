# TK-002K - Tracker projections pass whitespace checks without changing owner text

**Task ID:** TK-002K
**Spec ID:** S-004
**Concept source:** [DQC-000A](../../../../../../landmark-tracker/destination-questions/DQC-000A.json)
**Slice:** Correct generated Markdown and deliver it through supported setup update
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Verified delivery
**Planned verification:** Regression with empty notes and exact owner whitespace; generated projection determinism and full-range git diff check; package checks, source Review/CI and supported AMS update/receipt verification.
**Claimed by:** codex-s004-projection
**Current claimant:** codex-s004-projection

Workspace baseline sha256:e42a3e97088c284f79cbb5354160944497a71f55ca1645c14b03a61a33e923d4

## Assignment

The owner authorized S-004 implementation, preservation, verification and delivery; see the parent Spec's confirmed intent and execution citation. Independent Standards/Spec review of d9178b0 found required `git diff --check BASE...HEAD` fails in generated TRACKER.md: empty notes produce trailing ': ' and the document has an extra blank final line. Source H is already closed; this is a later bounded corrective run, not erased evidence or a new concept.

High tier Codex source implementor owns the reusable setup-workbench generator/tests in the isolated skills source checkout and the supported AMS managed-tool update. Root is the record writer. Use actual native claim as codex-s004-projection on Feature/S-004-dqc-grilling-board, then source author-skill/setup procedures. Preserve installed personal catalog, original root recovery metadata, earlier package backups and Board I source. No manual edit of generated tracker or receipt hashes.

Fix generation so empty event notes and document separators produce clean Markdown. Preserve exact owner readbacks, notes and confirmation snapshots, including trailing spaces, tabs and newline variants; encode display whitespace safely where needed instead of stripping recorded content. Add regression proving both clean projection output and unchanged source bytes. Repair the inherited missing native-README help reference to the actual delivered procedure if reached. Keep the API and concept meaning unchanged; no new frontier rules or unrelated refactoring.

Publish and independently review the checked source correction, merge under existing authority, then update AMS through the authentic package route and rebuild. Coordinate Git writes and push ordering with codex-s004-board, who owns README/manifest-display corrections in another clone of the same Spec branch. Full baseline/source/current-target whitespace must pass, not merely an empty working-tree diff. Return exact source/AMS SHAs, executed checks, preserved files/backup/receipt identity, implementor QA, remaining limits and the two merge/completion answers before native closure. Root handles acceptance and whole-assembly Review; do not claim Human QA, personal installation or deployment.

## Acceptance

- [ ] Generated TRACKER.md passes full-range whitespace checks for empty notes and exact whitespace-bearing owner text; source readbacks/notes/confirmation snapshots remain unchanged and rebuild is deterministic.
- [ ] Required source checks and independent correction Review pass on the published candidate; source delivery and supported AMS update have verified containment, authentic receipts and retained recovery.
- [ ] The actual AMS full-range check passes without generated/manual or receipt edits; Board behavior and all unrelated/installed/private work remain preserved, with exact remaining gates reported.
