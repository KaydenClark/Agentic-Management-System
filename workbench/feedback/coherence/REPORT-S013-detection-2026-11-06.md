# S-013 detection implementation and retained failures

Scope: [TK-001D](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/tasks/TK-001D/TASK.md).
This is a bounded detection/reporting slice. [Operator replay and limits](../../wiki/guidebooks/coherence-observations.md)
explain the caller seam. The existing [release graph](../../wiki/guidebooks/rsi-task-release.md)
still owns ordering. No complete RSI loop, real native use, Human QA, production
database application, installation or deployment is established here.

## Ownership and evidence

Before implementation, current main/dev/PR ownership, local Task records,
worktrees and current local agent activities were inspected. TK-002O remained
with codex-s006-recovery on PR175; page-review, website and Wiki writers remained
untouched. TK-001D was unclaimed on main/dev, with no active detection worker
or S-013 feature branch. Its old preparation hold was reconciled with the owner's
later implementation launch. Native claim `544a163` was pushed before product
edits; complete starting snapshot binding `67196eb` followed committed originals.
Raw workspace inventories remain private, outside the observed checkout.

Expected TDD collection failure at `9bdc277` established the absent public seam.
The first implementation `fe06655` passed 56 focused coherence checks. Its full
suite then failed: **858 passed, 6 skipped, 1 failed in 301.68 seconds**; the failed
repository hygiene assertion found two literal fake host-path canaries in new
tests. That result remains failed. The attempted interruption found no matching
owned process because the run had already exited; no process was signaled.

## Failed evidence and corrections

- **FAIL-175 — replay path normalization.** Initial replay refused because the
  temporary directory traversed the host's temporary-path symlink. Canonicalize
  only the owned temporary root; do not relax report-path symlink rejection.
  The unchanged replay scenario subsequently passed with fresh-process recovery.
- **FAIL-176 — candidate hygiene.** Two test literals violated public hygiene.
  Preserve exactly the same runtime private-path canaries by constructing their
  strings, retaining rejection/no-body-export assertions. The same hygiene
  check subsequently reported zero findings. No allowlist or scanner was weakened.
- **FAIL-177 — independent Spec review failed at fe06655.** P1: a Prepare limit
  was enforced only when an assignment-scope path was exceeded. P2: a null host
  refused instead of retaining unknown. Fix phase enforcement independently of
  eventual product scope, allow only preparation-record edits during Prepare,
  retain unavailable host identity as unknown and exclude it from eligible uses.
- **FAIL-178 — independent Standards review failed at fe06655.** P2: a copied
  Markdown report could inflate occurrence counts. P2: a list-valued observed
  reason could raise TypeError. Bind report filenames and retained occurrence/use
  identities, validate scalar types before set membership, and refuse broken
  recurrence closure. Do not count corrupted evidence.
- **FAIL-179 — documentation budget attempts.** The initial Runbook addition
  reached 3,031 characters; local pruning assertions at 3,004 and 3,008 also failed
  before writing. Coherent wording pruning reached 2,998 while retaining scope,
  commit, local-handoff and delivery controls. These were documentation checks,
  not measured skill improvement attempts.
- **FAIL-180 — restricted network inspection.** Initial GitHub read and native
  next refresh could not resolve the remote in the restricted shell. Explicitly
  authorized network reads refreshed the required refs; cached next output was
  not used as a claim. No other owner's checkout or claim was changed.

All four independent review defects were reproduced together at `3123371`
as four expected red regressions before repair. A further expected red case
proved recovery must refuse a recurrence after its parent report is removed.
These expected controls do not consume or reset any candidate campaign slots.

Failure intake for these local issues was recorded after the first repairs;
that chronology is a recording gap, not a claim of prompt intake. The canonical
[failure log](../WORKBENCH_FEEDBACK.md) links this retained evidence. No new
trial/campaign, installed-skill claim or global RSI success counter is created.

## Verification frontier

The corrected candidate requires the final full suite on a fresh checkout,
refreshed independent review, native Task gate, exact-head shared CI and normal
publication. These are recorded in the Task as performed; this report does not
predeclare their outcomes. Existing unrelated doctor findings remain owned by
their original records. Reports run only when invoked by an orchestrator; there
is no continuous watcher. Native receipt authenticity, general semantic grading
and later real use retain the worker/evaluator/adoption owners.

## Subsequent verified result

Corrected product `c01c5136f834656001e023da259a6348949ddf2c` passed 62 focused coherence checks and the operator replay in 2.292 seconds. A fresh immutable checkout passed **865 tests, 6 skipped in 300.98 seconds**. Wiki, layout, ADR and whitespace checks passed; hygiene reported zero findings. Existing doctor findings remain unchanged (other Tasks/host setup), and local selection output grants no new claim.

Independent `standards_review` and `spec_review` contexts both returned PASS with zero unresolved findings for main `adde5f4` through exact product `c01c513`. Spec review explicitly limits its conclusion to TK-001D's bounded synthetic behavior. [Shared CI42195608915](https://github.com/KaydenClark/Agentic-Management-System/actions/runs/42195608915) succeeded on that exact head on the declared `servitor-ams` runner: full Python suite, hygiene, records/Taskboard and 375px Board steps all passed. Its workflow is unchanged from governing main.

The native lifecycle closed TK-001D using the 44-file tool closure verified byte-for-byte against governing main `adde5f4`. Closure records still need their final exact-head checks and normal non-site main delivery through [PR182](https://github.com/KaydenClark/Agentic-Management-System/pull/182); a native close or merge does not establish whole-Spec acceptance, real loop assembly, owner Human QA or website promotion.
