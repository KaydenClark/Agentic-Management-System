# RUNBOOK target displaced by ceiling compliance

## Target And Scope

S-011 documentation work on 2026-11-02, preserved at `14d3480c28bcccb4d05b22b7ab7acc137e9b68cb` and `94c8191d48a5f8049712ad81d713055d764ecb53`. This is an observed execution failure, separate from the frozen three-pair shared-skills comparison. Evaluated/reviewer model: unknown; host: Codex on macOS. No skill fitness score is assigned here.

## Evidence And Limitations

The actual [budget](../artifact-budgets.json) already gives RUNBOOK a 900–1,500-character target and a 3,000 ceiling. [ADR-002V](../docs/adr/002V-artifacts-have-character-limits.md) requires pruning/revision, never splitting or truncation. `artifact-budgets.mjs` counts complete source in Unicode codepoints after LF normalization. Hygiene enforces the ceiling, not the target. [ADR-001B](../docs/adr/001B-readme-orients-people-and-the-runbook-orients-agents.md) retains the implemented command surface; brevity cannot erase it.

| Observation | Actual outcome |
|---|---|
| Initial hygiene | AGENTS 3017 and RUNBOOK 3336 exceeded 3000 |
| First reduction | AGENTS 2995 passed; RUNBOOK 3116 still failed |
| Owner explicitly resumed focused repair | RUNBOOK attempts at 3036 and 3025 still failed; repeated stop preserved |
| Owner corrected the objective and units | Near 900 characters was the goal; the ceiling was not the goal |
| Owner required source homework | Existing target, counting, no-split and command-coverage rules were recovered before the new draft |
| Reconciled local draft | RUNBOOK 1193 Unicode codepoints; all 11 declared AMS entrypoints, actual check commands and the literal board command retained; no extraction |

The owner intervened to resume, correct the objective, clarify characters rather than words, and require checking all rules. These interventions are cost evidence, not proof of a general skill cause. The final draft remains above 900 because the real command surface must stay readable. Local focused verification passed 38 tests, including hygiene and the board command with socket permission. Earlier full-suite sandbox failures remain in TK-001; no passing full suite is claimed by this report.

## Findings

**F-001 — Goal replaced with ceiling.** The implementor repeatedly optimized a failing cap check instead of recovering the stated target and producing a coherent small artifact. The policy was present; missing routing during execution cannot be described as a missing size rule. **Disposition: diagnostic**; owner: S-011/TK-001; evidence: the preserved counts and [owner correction](../wiki/context-owner-answers-coherence.md#jot-08cbbb7a-b88b-4ecc-962e-88d1578bce53). The current local correction does not establish future reliability.

**F-002 — Contradictory diagnostic remedy.** `workbench/tools/artifact-budgets.mjs` suggests splitting or condensing an over-limit artifact, while ADR-002V and S-001 prohibit splitting records. **Disposition: diagnostic**; owner: the setup-workbench package; evidence: source inspection of `budgetFailure`, not an executed split. No managed tool changed in this repair.

## Challenged Or Rejected Findings

No causal claim that shared skills alone caused the failed reductions is established. A green cap check cannot prove the owner's goal, behavioral improvement or a whole-AMS fitness level. The new failure cannot be inserted retroactively into the frozen comparison or reset its attempts.

## Next Action And Review Boundary

Publish the checked small RUNBOOK with S-011 records, then display this separate failure in the safe RSI log. The earlier [prune-artifact proposal](../wiki/context-owner-answers-coherence.md#jot-8a72da2b-8f02-45c8-8df5-4ae2a339df45) now has [owner implementation approval](../wiki/context-owner-answers-coherence.md#jot-1d568dd6-5ffd-43f5-a6e3-8f58568c92bf); its separate test suite and qualifying result remain pending. Root inspected the 1193-character draft; this is not a skill audit, Human QA or benefit verdict.
