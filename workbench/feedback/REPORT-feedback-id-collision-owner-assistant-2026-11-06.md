# FAIL-161 collision evidence - owner-assistant

## Target and scope

Reporter: **owner-assistant**. Recorded: 2026-11-06 UTC.
Disposition: **diagnostic**; follow-up owner: the existing **S-003 feedback-log writer**.
Status: **unresolved; unfinished records-only checkpoint**.

This is supporting correction evidence for two existing, source-bound
`FAIL-161` receipts, not a new ID allocation or a replacement log. The
[recording rules](WORKBENCH_FEEDBACK.md#recording-rules) require stable IDs,
preserved failures and corrections linked by ID. Both underlying failures
already have intake rows. No third `FAIL-NNN` is invented or reserved here.

Method: read-only GitHub source inspection of committed logs, feedback directory
inventories and workflow files. No underlying failure was rerun. Evaluated
model: not-applicable to this structural comparison. The actors, model tiers,
actual models and harnesses responsible for the competing allocations are
unknown; the reporter is not assumed to be either actor. No skill causation
or model-quality conclusion follows.

## F-001 - One bare ID identifies two different occurrences

Severity: medium, a feedback traceability and future integration blocker.
Disposition: **diagnostic**; owner: **S-003 feedback-log writer**; evidence:
the two immutable log receipts below. A verified coordination channel to that
writer was unavailable at capture. No accepted repair Task is asserted.

1. **Promotion whitespace occurrence.**
   [Checkpoint 5fa75f6, log line 178](https://github.com/KaydenClark/Agentic-Management-System/blob/5fa75f6e18274a63db2d3b7c5253afb9a78a39f9/workbench/feedback/WORKBENCH_FEEDBACK.md#L178)
   assigns `FAIL-161` to PR142's promotion whitespace failure. Log blob:
   `bd12802d1648ba646c2092bb53a1a4f8009671a5`.
   Occurrence key:
   `PR142/259b7a905639cc6ab621220b160fc813c5bc43f1/run 42179393393/attempt 1/job 127765232219`.
   It records `site/app/tour/tour.module.css:45`, exit 2 and skipped later gates.
   Its original [supporting report](REPORT-promotion-ci-owner-assistant-2026-11-06.md)
   remains unchanged. This receipt does not identify the doctor occurrence.

2. **Doctor/TASKBOARD occurrence.**
   [PR178 head 98ad6597, log line 189](https://github.com/KaydenClark/Agentic-Management-System/blob/98ad6597faa931fb7be3330a9b37a49d28a190f0/workbench/feedback/WORKBENCH_FEEDBACK.md#L189)
   assigns `FAIL-161` to S-009/TK-0030's repository doctor failure at
   `d5b015fe135153c1e35747093750b81d9e21c24d`. Log blob:
   `df40b30e4a7b8a4f74b989532a5f006502c50418`.
   It records exit 1 because `TASKBOARD.page-002` was stale after Task
   creation/claim, and retains the separate correction `96f6848` and later
   selected-slice limits. This receipt does not identify PR142's CI job.

The ID strings are equal; activities, candidates, observations and evidence
are different. A bare `FAIL-161` link or deduplication key cannot distinguish
them. Neither receipt is a retry of the other. This is a demonstrated identity
collision across branches, not proof that either underlying failure vanished
or that an integrated canonical log already contains duplicate rows.

### Freshness and deduplication limits

At readback, S-003 had advanced to
`77a50aa6bbe73de724ce8a273948a946e8bbddd1`; its log blob
`ac92747c15e3e02fabcdf9c4651b650dfda02508` retains the doctor row byte-for-byte
and extends through FAIL-172. It contains no collision correction.
Dev `63870b54efba9b9028dc8c1ae194f3fef85138ae` still has log blob
`fdd3ac07fe17f6c9050d96fdd455a7591290d7ec`, ending at FAIL-148.
The promotion checkpoint remains a separate, unintegrated lane.

Inspected feedback inventories at those refs and the current S-005, S-006 and
S-009 refs contain no collision report. This records a newly identified
allocation correction within that inspected scope, not an exhaustive claim
about private or unpublished work. Later branch movement is not covered.

## Correct outcome and smallest next action

Before these records are combined, the existing serialized feedback writer
should coordinate a stable canonical identity for each occurrence, retain
both original source-bound receipts, and append an explicit mapping from any
superseded allocation to its canonical identity. Recheck links and prove that
neither occurrence was dropped or silently overwritten. Until that happens,
cite each occurrence by immutable source plus ID, never by bare `FAIL-161`.

No safe next numeric ID is claimed. The S-003 writer's current allocation
queue was not available, so choosing FAIL-173 merely from the latest visible
maximum would risk another collision. This report does not edit either log,
renumber historical rows, repair an implementation or assign another writer's
files. Existing S-003 scope and delivery gates remain in force.

## Publication and verification boundary

The checkpoint adds this report only, based on original checkpoint `5fa75f6`.
Both original receipts and the earlier promotion report remain byte-identical;
the active S-003 branch is not changed. No current main/dev update is implied.

The inspected `python-tests.yml` runs the full suite for every pull request
targeting main or dev without a path filter. Its only trigger is
`pull_request`; `site-build.yml` also has only that trigger. Therefore no PR is
opened or updated for this observation-only checkpoint, and no full suite is
requested. Source/readback and report whitespace checks are not project tests.

Remote checkpoint readback must verify the exact new report, its parent,
changed-file scope and preservation of the original feedback blobs before
publication is reported as verified. This is not independent Review, Human QA,
resolved allocation, source delivery to dev/main, merge, deployment or RSI
improvement evidence.
