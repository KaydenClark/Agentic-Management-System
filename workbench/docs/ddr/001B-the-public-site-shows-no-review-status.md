---
date: 2026-11-02
supersedes:
canonicalized_in:
  - workbench/landmarks/LMK-003-ams-website/LANDMARK.md
  - workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md
  - workbench/landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/SPEC.md
---

# The public site shows no review status

No page of the public website shows a draft, approval or review banner, mark or status. A public site does not tell visitors whether its owner reviewed a page. The owner's page review on the Grill Board, with approval bound to the page's content hash, stays an owner-facing record and never changes what visitors see.

Considered and rejected: a draft mark on every page until an approval bound to its content hash exists, restored when the content changes, the earlier rule in LMK-003, S-003 and S-005, which the owner withdrew.

Consequences: LMK-003, S-003 and S-005 drop the draft mark. S-005 keeps hash-bound approvals for the owner and agents; a content change makes an approval stale on the board only. Existing draft notices on `dev` pages are site work.

Provenance: Owner decision in chat, 2026-11-02, relayed by the coordinating session; paraphrased in `workbench/wiki/context-website-presentation.md` (JOT-76ddc50f).
