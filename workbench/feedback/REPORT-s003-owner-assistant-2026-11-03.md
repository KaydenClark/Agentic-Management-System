# S-003 website verification — owner-assistant

## Current Disposition — 2026-11-03 01:07 UTC

**F-001 is repaired at source on dev `07a7ae4404ad018c3763edef65ebdb5ef1607f0f`**,
through [PR #136](https://github.com/KaydenClark/Agentic-Management-System/pull/136)
(candidate `1d2b70d88ac699cbc922f8eb607283cdada23d75`).
The original observation below is historical, not a current request to fix it.

Independent readback of [How It Works at repaired dev](https://github.com/KaydenClark/Agentic-Management-System/blob/07a7ae4404ad018c3763edef65ebdb5ef1607f0f/site/app/how-it-works/page.tsx)
confirmed that all three historical example links now use the full evidence SHA
`ce39c6a89f92dffaebecb468b367c49ab6577bd8`, and the copy explains that record
moves/deletion do not change these references. `git cat-file -e SHA:path`
independently confirmed the Spec and both Task objects exist at that revision.
The [new regression assertion](https://github.com/KaydenClark/Agentic-Management-System/blob/07a7ae4404ad018c3763edef65ebdb5ef1607f0f/site/tests/tour-inventory.test.mjs)
requires the three distinct sources, immutable revisions and existing objects.
Its code was inspected, not executed by this verification.

PR #136 reports 206/206 site tests and authenticated live readback of the three
pinned links with deployment footer `07a7ae4`. Those are builder-reported
results, not an independently repeated browser run. This source-level closure
does not establish full site acceptance, Human QA or later-use improvement.

## Original Target And Scope

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

Historical severity: medium. Current disposition: **repaired**; owner: **S-003**, Route criterion.
Implementing candidate and verification are recorded above. The original disposition was diagnostic;
its source comparison is preserved below. No product fix was made by owner-assistant.

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

Historical recommendation (now addressed at source by PR #136): select the actual evidence
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

Keep F-001 as repaired source history under S-003; no further fix is requested by
this record. No new Task, approval gate or scope is created. This documentation-only record does not mark S-003 complete,
claim Human QA, or prove improved agent reliability. A separate-context source reviewer confirmed this narrow mismatch and located
the pre-existing TK-002 limitation. That review covered the cited source and
requirement only, not the full site, rendered behavior or Human QA.

## F-002 — RSI comparison does not answer the owner's adoption question

Recorded: 2026-11-03 06:05 UTC. Reporter: **owner-assistant**.
Disposition: **open owner feedback for S-007**, not a demonstrated numerical
defect, accepted design change, new Task, or implementation authorization.

The owner asked in the assistant conversation: "So what is the point of this
visual if its not telling me if the AMS is making things better or worse?
Why would I look at this and want to install the AMS skills"

This preserves the owner's concern about the visual's purpose and usefulness.
It does not establish that AMS as a whole makes outcomes worse. This wording is
feedback provenance, not public-site copy; the no-owner-quotations site rule
remains unchanged.

### Verified evidence and meaning

Source inspected at dev `76b9c564692a1e979cffbebbe30063b73588efb6`:

- [Chart and explanation](https://github.com/KaydenClark/Agentic-Management-System/blob/76b9c564692a1e979cffbebbe30063b73588efb6/site/app/rsi/repair.tsx#L4-L49)
  explicitly present the first workflow attempt as recorded development evidence.
- [Source data](https://github.com/KaydenClark/Agentic-Management-System/blob/76b9c564692a1e979cffbebbe30063b73588efb6/site/app/rsi/repair-data.ts#L30-L43)
  give baseline 9/11, 10/11, 10/11 and candidate 9/11, 8/11, 7/11:
  totals 29/33 and 24/33, respectively. Those totals summarize repeated
  deterministic checks, not independent outcome probabilities or an Alignment Score.
- Both arms use skill versions: baseline `fb7ad23c963e183b930b23bc5fdf4d309dff292a`
  and candidate `6f84573de47cbc7675876777e22e903ecd4783d1`.
  This is not an AMS-versus-no-AMS comparison. The candidate passed fewer checks
  in two runs, but this alone establishes neither source causation nor the
  value of installing AMS.
- The page already states that counts establish neither cause nor useful benefit,
  identifies source-injected skills rather than proven native activation,
  and keeps this first attempt distinct from later work. Those safeguards
  should not be misreported as missing.
- [S-007](https://github.com/KaydenClark/Agentic-Management-System/blob/76b9c564692a1e979cffbebbe30063b73588efb6/workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md)
  requires visible failures/regressions and traceable evidence, and forbids
  improvement claims without held-out rows, controls, a prior version and an
  interval. [Current presentation intent](https://github.com/KaydenClark/Agentic-Management-System/blob/76b9c564692a1e979cffbebbe30063b73588efb6/workbench/wiki/context-website-presentation.md)
  authorizes showing relevant real evidence on-site, not hiding failed attempts.

### Next action and boundary

Reconcile this owner feedback in the existing S-007 presentation review:
identify what useful question this visual answers for a visitor and make clear
what adoption or benefit conclusion remains unsupported. Preserve the failed
attempt and its limits. The exact presentation response remains for the existing
owner/builder process; this record does not prescribe a replacement chart,
approve a new baseline or test campaign, or change acceptance criteria.

The reviewed S-007, presentation Wiki and existing owner-assistant report already
track evidence limits, but not this exact owner concern about the visual's value
as a reason to install. This entry records that additional feedback without
creating a duplicate implementation Task. Review was source-only; no rendered
deployment, visitor comprehension, full acceptance or Human QA was verified.
