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

Authorized retry launched hygiene after the sandbox failures. It found AGENTS at 3,215 characters against the 3,000 limit; a shortening attempt yielded 3,085 and the second check failed. Stopped under the three-strike rule. The control is still over budget; an explicitly authorized retry must finish it before readiness.

### Owner-authorized retry and fidelity review

Owner identified the ceiling-focused proposals as a recurrence and authorized repair; see [failure report](../../../../../../feedback/REPORT-runbook-target-failure-2026-11-02.md) and [correction](../../../../../../wiki/context-owner-answers-coherence.md#jot-7f1423d9-1f8a-4b06-8334-de686807f172). Draft AGENTS is 1,767 characters and RUNBOOK 1,525, above their 900–1,500 targets. Hygiene passes the ceiling, not the goal. An automatic review rejected a subsequent proposed pruning action because it would weaken explicit strike and RSI duties; it did not execute. Further edits require a safe, independently reviewed route.

Fidelity inspection: owner-only dev-to-main, review/QA distinctions, capture before dependent work, one writer, safety and three-strike rules remain explicit. Cold-start routes include architecture, glossary, Wiki, taskboard, Spec/Task and skill. Remaining gaps: AGENTS mentions Wiki without its path (Wiki validator reports `room-brain-unrouted`); shortened controls must be checked against shared CI, scoped RSI evidence and authorized-install boundaries before readiness. RUNBOOK retains the command surface, fresh checkout and render/doctor expectations. This is self-review, not independent Review or owner Human QA.

### Fidelity map for alternate control repair

| Existing duty | Retained owner / route |
|---|---|
| Scope, readback, authority, questions, delegation, carry | Universal AGENTS instructions |
| Repo/branch/remote/locks/dirt and cold-start context | AGENTS and RUNBOOK Get oriented -> architecture, glossary, Wiki, taskboard, assigned Spec/Task and skills |
| Six active Landmarks and real-input blockers | AGENTS; ADR-003J |
| One writer, preserve edits/decisions, no checkout switching | AGENTS |
| Capture sourced intent/corrections before dependent work | AGENTS; jot method via SKILLS |
| Claim and managed-tool/skill authorship boundaries | AGENTS; lifecycle and method routes in SKILLS |
| Destruction, paid services, external changes, license, messages, private data and three-way session boundary | AGENTS |
| Red/green, checks and three-strike stop | AGENTS; RUNBOOK Test And Build |
| RSI site evidence, full issue/baseline/hypothesis/comparison/failures/disposition, skill-source repair, installation authority and no cross-project rollout | Universal site-evidence sentence in AGENTS; RSI operation in SKILLS |
| Runner, fork inspection, no fallback, keys and live-test CI boundary | RUNBOOK Test And Build -> shared CI operation |
| Commit, no destructive cleanup, checked branch routes and owner-only dev-to-main | AGENTS; RUNBOOK cleanup and land |
| Review, Human QA, merge, deployment and delivery evidence distinctions | AGENTS; SKILLS delivery |
| Runtime commands, fresh checkout, rendering, doctor and rollback | RUNBOOK Test And Build and cleanup |

This map is the intended route for the alternate; actual edits and verification must be inspected separately. It does not establish full Workbench equivalence, independent Review or Human QA.

The alternate retains the three-strike and site RSI sentences verbatim, routes the full RSI operation and personal-install/no-rollout boundary to SKILLS, and routes CI policy to its Wiki owner. Wiki validation and hygiene pass; doctor has no global blockers but retains the S-011 slice, stale claim, legibility and permission findings. `git diff --check` passes. AGENTS is 1,861 characters and RUNBOOK 1,579, above their 900–1,500 targets; these are not accepted as complete. The exact alternate and fidelity map require independent inspection and further meaning-preserving pruning.

The revised candidate routes full RSI procedure to SKILLS and CI operation to its existing Wiki owner. The protected strike and site RSI sentences remain verbatim. Current controls measure AGENTS 1,494 and RUNBOOK 1,396 Unicode codepoints. The RUNBOOK retains all eleven AMS entrypoints and routes orientation to architecture, glossary, Wiki, Taskboard, assignment and skill; the duplicated workflow list remains in SKILLS. A focused fidelity check covered the target, protected sentences, Wiki/skill routes, Landmark and blocker rules, owner-only promotion, safety, managed tools, CI and entrypoints. Wiki and layout validation, hygiene and whitespace checks pass. Doctor has no global blocker; its existing slice and informational findings remain. These checks and this self-review do not constitute independent Review or owner Human QA. Final assembled checks and review remain open.
