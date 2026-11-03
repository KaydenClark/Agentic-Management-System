# S-003 website verification — owner-assistant

## Target And Scope

Reporter: **owner-assistant**. Date: 2026-11-03 UTC.
Owner-authorized independent observation and recording only; no implementation,
acceptance, deployment or repair authority is implied.

Candidate: dev `ce39c6a89f92dffaebecb468b367c49ab6577bd8`.
Scope: `site/app/how-it-works/page.tsx`, `site/app/start/page.tsx`,
S-003's Route criterion, and the recent Start-copy correction.
Evidence type: source inspection. Evaluated model: not-applicable;
reviewer model: unknown; host: cloud Linux source inspection.

## Evidence And Limitations

Source was read at the fixed candidate using `git show` and `git log`.
No project code or browser test was executed for this report. This is not a
rendered-page review, a claim that a link currently returns 404, or a complete
S-003 acceptance audit. Build/test evidence from an older candidate does not
transfer to this candidate.

## Findings

### F-001 — Public example sources are mutable rather than revision-pinned

Severity: medium. Disposition: **diagnostic**; owner: **S-003**, Route criterion.
Diagnostic performed: source comparison described below; no persistent test added.

**Known open gap, not a newly discovered defect:** the [TK-002 receipt](https://github.com/KaydenClark/Agentic-Management-System/blob/ce39c6a89f92dffaebecb468b367c49ab6577bd8/workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/tasks/TK-002/TASK.md#L37)
already records this limitation. This report re-verifies that existing gap at
the named candidate and retains its original owner; it creates no duplicate Task.

[How It Works at the candidate](https://github.com/KaydenClark/Agentic-Management-System/blob/ce39c6a89f92dffaebecb468b367c49ab6577bd8/site/app/how-it-works/page.tsx#L14)
defines `REPO_BLOB` with `/blob/dev/`. Its real-work example uses that prefix
for S-003 and TK-001/TK-002 links. The paragraph following TK-002 explicitly
says those links will change when the Task files are deleted.

[S-003 at the same candidate](https://github.com/KaydenClark/Agentic-Management-System/blob/ce39c6a89f92dffaebecb468b367c49ab6577bd8/workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md#acceptance-criteria)
requires public revision-pinned Spec/Task sources that survive record moves.
A moving branch link does not satisfy that requirement: later edits can change
the evidence behind the displayed historical account, and deletion can remove
the linked path. This is an observed source/requirement mismatch, not a
demonstrated current HTTP failure.

Smallest next action for the existing builder: select the actual evidence
revision supporting each account, use immutable links to those records, and
verify they resolve. Update the contradictory explanation accordingly. Do not
blindly substitute an arbitrary or latest SHA. Retain this finding until the
changed candidate is checked; this report makes no fix.

## Challenged Or Rejected Findings

The earlier Start-page definition and empty-RSI wording discrepancies are
**not reopened** here. Candidate ce39c6a includes merged
[PR #134](https://github.com/KaydenClark/Agentic-Management-System/pull/134),
which reconciles that copy. Source correction is observed; rendered deployment
verification remains outside this report.

A READY deployment or passing build alone is not owner acceptance. Existing
unverified S-003 criteria and blocked assignment reconciliation are not
converted into new owner questions by this record.

## Next Action And Review Boundary

Keep F-001 with the existing S-003 website work; no new Task, approval gate or
scope is created. This documentation-only record does not mark S-003 complete,
claim Human QA, or prove improved agent reliability. A separate-context source reviewer confirmed this narrow mismatch and located
the pre-existing TK-002 limitation. That review covered the cited source and
requirement only, not the full site, rendered behavior or Human QA.
