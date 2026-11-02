# TK-002 - Add a public hygiene and character-limit check over records, controls and the built site

**Task ID:** TK-002
**Spec ID:** S-001
**Slice:** Add a public hygiene and character-limit check over records, controls and the built site
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Limits; Hygiene.
**Claimed by:** claude-impl-s001-tk002
**Current claimant:** claude-impl-s001-tk002
**Proof:** ams-hygiene at 1c77317: planted/valid tests pass; built site 0 findings; real repo 12 findings fail; pytest 629 pass, 1 fail (real repo); site npm test 70 pass; render, doctor, validate, diff --check ok

## Assignment

Add a public hygiene and Unicode character-limit check over records, controls and the built site; wire it into the existing checks. Refuse host paths, credentials, private record IDs, split records and any Spec, Task or Landmark over 8,000 characters; root controls are limited to 3,000. Preserve existing rules and scope.

## Acceptance

- [ ] Real repository/site input is checked; violations are named and fail.
- [ ] Planted invalid inputs fail; valid inputs pass. Report existing violations without weakening the check.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s001-tk002-hygiene-check | 1c773172d7d9ec9c913ffe406ebae89fcd3cc93e | ahead 0 behind 0 | 0 | ams-hygiene at 1c77317: planted/valid tests pass; built site 0 findings; real repo 12 findings fail; pytest 629 pass, 1 fail (real repo); site npm test 70 pass; render, doctor, validate, diff --check ok | RUNBOOK Test And Build; ARCHITECTURE codemap; CI workflows | 12 real findings fail CI, owned outside TK-002: S-002, S-002 TK-002, S-006, S-008 over 8,000; GLOSSARY, README, TASKBOARD over 3,000; host paths and session IDs in orchestrator A/B handoffs; a host path in site/tests/hygiene.test.mjs. Not merged until fixed.; close attribution: {"agent":"claude-impl-s001-tk002","claimant":"claude-impl-s001-tk002","onBehalfOf":null} | c080bccf3f4584db73f00dd8542203429e9b21e4641df9c1509ccc246f827325 |
