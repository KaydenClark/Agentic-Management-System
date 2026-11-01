# TK-000R - JSONB numeric normalization cannot poison private assessment history

**Task ID:** TK-000R
**Spec ID:** S-006
**Slice:** JSONB numeric normalization cannot poison private assessment history
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Private assessment persistence
**Planned verification:** Red-first exponent/negative-zero JSONB transport normalization; exact payload text replay, duplicate/lost-response retries; live tagged normalization probe; focused/full/fresh checks and rereview.
**Claimed by:** codex-assessment-writer
**Current claimant:** codex-assessment-writer

## Assignment

Same approved private assessment persistence, successor correction after TK-000Q closed. One writer codex-assessment-writer on current PR #83 branch; no merge until corrected and checked. Independent assembled FAIL at `977ac08fed4a269182b67d6ada990042e2ceee88`, digest `cfc6d944ca5790364a2dedec20039979a70fa9ae28d83a8fd6fc579cc9562f8a`: Python hashes `1e+20`, JSONB reads the equivalent expanded integer, so immutable readback rejects its own row and blocks the namespace. Preserve exact canonical envelope text and hash it; JSONB remains a checked identity projection. Additive migration must not invent missing original text for existing rows. Preserve earlier migrations, failed verdict, Task receipts and scorer semantics. Raw data stays private; no trials, publication or qualification claims. Correct stale TRIAL-ROWS storage wording. Return immutable candidate for independent rereview.

## Acceptance

- [ ] Exponent, negative zero and nested numeric metadata survive JSONB normalization with exact original packet/result and stable digest.
- [ ] Changed text/projection/digest refuses; duplicate and lost-response retries remain idempotent; no corrupt namespace writes.
- [ ] Marked live normalization probes, tests and required checks pass; original failed review remains recorded.

## Native corrective provenance

The native failed verdict at reviewed `977ac08` generated this same Task ID at evidence row18. Its generic assignment and the already claimed bounded assignment describe the same numeric roundtrip correction; preserve the current claimant, detailed acceptance and original failed-review row. Native verdict source commit `ca447da043ad92ecfafc2ac370e7e717ff149fcc` is merged into this branch.
