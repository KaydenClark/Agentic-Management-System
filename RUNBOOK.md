# AMS Runbook

## Get oriented

Read [AGENTS](AGENTS.md), then the [Architecture routes](ARCHITECTURE.md#routes), [Glossary](GLOSSARY.md), relevant [Wiki context](workbench/wiki/MEMORY.md) and assigned Spec/Task. Inspect live Git state before editing. Recover established answers and proceed to the authorized endpoint.

## Workflows

1. Capture the request, reasons, corrections and allowed endpoint in the existing owner. Use a [Wiki note](workbench/wiki/NOTE-TEMPLATE.md) when context has no owner; requirements belong in the Spec.
2. For a capability, use the [Spec](workbench/specs/SPEC-TEMPLATE.md) and bounded [Tasks](workbench/specs/TASK-TEMPLATE.md). Define observable acceptance before implementation. Small ordinary edits need no manufactured project hierarchy.
3. Apply the relevant existing personal skill; load its actual SKILL.md. Verify availability rather than invoking missing operation mappings. Keep one writer for shared records.
4. Check the requested outcome. Preserve actual proof, failures and limits. When required, obtain the appropriate [review](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) and record actual [Human QA](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md).
5. Deliver only through the authorized and verified route. Update durable owners and leave a [handoff](workbench/sessions/HANDOFF-TEMPLATE.md) if useful work remains.

### RSI during website work

Use actual site-building work to expose friction. Capture a [feedback report](workbench/feedback/REPORT_FORMAT.md) or maintain an [evidence audit](workbench/research/EVIDENCE-AUDIT-TEMPLATE.md), then use an [improvement record](workbench/research/IMPROVEMENT-TEMPLATE.md) for a bounded hypothesis and experiment. Define [eval tasks](evals/EVAL-TASK-TEMPLATE.md), retain each [result](evals/EVAL-RESULT-TEMPLATE.md), and assess a [comparison](evals/EVAL-COMPARISON-TEMPLATE.md). Keep the actual adoption decision distinct from the recommendation.

Use the [website-page template](site/PAGE-TEMPLATE.md) to explain verified behavior, intended behavior and limits. Recheck later use to determine whether the repair helped; feed supported learning into the next loop.

## Preserve knowledge as it happens

Use existing topic owners; grow flat Wiki notes through [MEMORY](workbench/wiki/MEMORY.md). Record source, speaker, date, claim status, reasons and correction history. Promote accepted requirements or rules to their maintained owner and link back. Templates do not need to be filled for every operation.

## Test And Build

AMS has no installed application test/build suite, evaluation runner or Workbench doctor. Do not run placeholder commands. For this Markdown scaffold, inspect content against the source research and request, check local links and JSON syntax, and run `git diff --check`. Record these as document checks, not runtime or agent-outcome tests.

When code is introduced, fill verified setup, focused-test, full-suite and build commands here from actual implementation. Then use those checks for relevant changes. Evaluation definitions remain independent of the eventual runner.

## Version control and publication

`main` is the only long-lived branch. For each change:

1. Branch from current `main` with a name for the change.
2. Commit each coherent step; never stash. The Stop hook refuses to end a turn with uncommitted work.
3. Push the branch and confirm the remote has the commit.
4. Open a PR into `main` (draft while unfinished). Once it is up to date with `main` and any required checks pass, merge it yourself with a merge commit, then confirm `main` contains it.
5. Delete the merged branch.

No deployment route is configured yet. Keep local, committed, pushed, merged and deployed states distinct when reporting.

## Recovery

Reopen the owning Spec/Task and relevant Wiki correction history; verify live state before resuming. Keep actual sessions ignored. Legacy JSON examples remain compatible reference material, not an active capture service.
