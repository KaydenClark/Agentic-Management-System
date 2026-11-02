---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - workbench/specs/S-001-ams/SPEC.md
supersedes:
  - 002S-at-most-six-active-specs.md
---

# Limit active Landmarks, not Specs

At most six Landmarks are active at once. Use Landmark -> Spec -> Task. What was called a parent Spec is a Landmark; introduce no additional parent-Spec hierarchy. Specs consume no Landmark slots and never wait for another Spec to close to free one.

An unfinished capability can prevent final acceptance without preventing work on an independent Spec or Task. Block only work that actually needs its missing output. S-001 remains the cross-landmark yardstick under the Blueprint, not a parent of Landmarks; its existing ready checks and repairs can proceed now.

Considered and rejected: counting every Spec against six slots, which locked out S-001; placing Landmarks beneath S-001, which inverted the hierarchy; removing the limit entirely, which the owner rejected in favor of limiting the parent destinations.

Consequences: AGENTS counts Landmarks. S-001 separates readiness from acceptance. Retire the slot-transfer queue; keep real Task inputs, scoped execution authority, review, Human QA and publication gates. No outcome is accepted through this correction. Replaces ADR-002S, retained in history.

Provenance: Kayden's AMS chat corrections, 2026-11-01: "You cant have landmarks below a spec" and "Parent specs should be Landmarks". Captured as [JOT-abe54041-757d-443a-82f4-6bc011b3908f](../../wiki/context-active-spec-approvals.md).
