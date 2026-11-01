# TK-000O - Historical finding ID collisions cannot bypass Regression acceptance

**Task ID:** TK-000O
**Spec ID:** S-002
**Slice:** Historical finding ID collisions cannot bypass Regression acceptance
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Scoring; Stops
**Planned verification:** Red/green collision fixture at score/record seams; independent review; final-head CI.

## Assignment

Same authorized S-002 delivery, codex-s002 writer, `codex/s002-assessment-loop` -> `main`, PR #78. [Automated finding](https://github.com/KaydenClark/Agentic-Management-System/pull/78#discussion_r4436884504) at `d8fc717` proved a historical Quality finding could collide with the generated ID of a currently failing Regression check, leaving Stable accepted. Reject incompatible check/class collisions before writing or retain a distinct current-class finding; preserve previous evidence and original classes. No storage, trial or rubric expansion.

## Acceptance

- [ ] A historical Quality finding cannot hide a current Regression failure through an ID collision; incompatible check IDs/classes cannot reuse the current finding identity.
- [ ] Refused collisions leave stored history unchanged, and normal repeat findings, enrichment, retests and recurrence still work.
- [ ] Focused tests, independent review and required CI pass before merge; native proof/closure retained.
