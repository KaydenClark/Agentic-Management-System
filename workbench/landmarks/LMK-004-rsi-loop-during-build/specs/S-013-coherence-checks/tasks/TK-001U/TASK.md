# TK-001U - Recover current controls and records on dev

**Task ID:** TK-001U
**Spec ID:** S-013
**Slice:** Assemble current main records and confirmed recovery corrections with the newer dev website
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Feedback loop connection
**Planned verification:** Inspect merge and retained site ancestry; validate records, links, rendering, doctor and hygiene; report limits.
**Claimed by:** codex-recovery
**Current claimant:** codex-recovery

## Assignment

Owner instruction, 2026-11-02: recover the Workbench meaning and current records, reconcile approved corrections, and prepare the combined result on dev for owner review. One writer owns the reconciliation and task projection. Preserve other claims, campaign stops and owner gates. This assembly does not complete the broader detection or learning cycle.

## Acceptance

- [ ] Current main records are assembled with newer dev site work and confirmed owner corrections, with conflicts explained.
- [ ] Recovery accounting identifies retained obligations, gaps and source limits without claiming behavioral proof.
- [ ] Focused checks and scoped QA are recorded; unverified work remains open.

## Work in progress and verification

The merge commit preserves dev's Start and How it Works pages, including its quickstart and RSI evidence, and combines both website context histories; the generated taskboard was rendered from merged records. Both original remote tips are ancestors. Owner correction commits were cherry-picked with their original messages. Controls and adoption accounting have been reconciled; broader detection and learning-cycle acceptance remain open.

`doctor` reports no global blocker, with S-011/TK-003's dependency, a stale S-002 claim, undeclared legibility and permission-scope drift still visible. Wiki validation, layout validation and `git diff --check` pass. Hygiene did not run: the first attempt could not access the uv cache; the second, with a temporary cache, could not create the worktree virtual environment. Stop after these two failed attempts; final assembly must resolve the environment and run remaining checks. Full Python and site checks, fresh-clone verification, independent review and owner Human QA are not claimed.
