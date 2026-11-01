# TK-002 - Add a public hygiene and character-limit check over records, controls and the built site

**Task ID:** TK-002
**Spec ID:** S-001
**Slice:** Add a public hygiene and character-limit check over records, controls and the built site
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Limits; Hygiene.

## Assignment

Add a public hygiene and Unicode character-limit check over records, controls and the built site; wire it into the existing checks. Refuse host paths, credentials, private record IDs, split records and any Spec, Task or Landmark over 8,000 characters; root controls are limited to 3,000. Preserve existing rules and scope.

## Acceptance

- [ ] Real repository/site input is checked; violations are named and fail.
- [ ] Planted invalid inputs fail; valid inputs pass. Report existing violations without weakening the check.
