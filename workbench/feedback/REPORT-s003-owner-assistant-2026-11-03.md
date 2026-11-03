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

## F-002 — RSI page should show whole-AMS improvement over time

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

### Owner clarification — supersedes the narrower adoption framing

Recorded: 2026-11-03 06:09 UTC. Reporter: **owner-assistant**.
Source: owner's subsequent message in the assistant conversation, verbatim:

"Exactly, I want it to show the real thing. pass and fail. But I want it to give real info. Not just individual run results. The page is supposed to display the improvements of the whole AMS over time, not the results of runs"

This clarification is the current meaning of F-002. The earlier installation
question remains historical context, not the full destination. The owner wants
the page to show the whole AMS's improvement over time, retaining both pass and
fail and providing meaningful information rather than a display of individual
run results. This is not a request to hide failures or turn failed runs into
positive claims.

The next action is to reconcile this exact intent through the existing S-007
owner/builder workflow. This report does not define an aggregation method,
metric, statistical claim, baseline, chart design or new test campaign.
The earlier source observations remain valid within their bounded scope;
they do not establish a whole-system trend. Missing evidence remains missing.
No product code, Spec acceptance criteria, decisions or Tasks were changed by
this clarification. This sourced owner wording is internal project feedback,
not copy for the public website.


### Candidate progress and existing review findings — 2026-11-03 16:16 UTC

Reporter: **owner-assistant**. Evidence: source inspection and GitHub state
readback; evaluated model: not-applicable; reviewer model: unknown.
F-002 remains open. This observation is not a new implementation defect or
a claim that an unfinished PR should already satisfy whole-Spec acceptance.

[PR #154](https://github.com/KaydenClark/Agentic-Management-System/pull/154)
at `088acb924e443aca7b4e20f67607c100f3b58c79` adds round-two per-skill
comparisons before the preserved first attempt. The
[new page section](https://github.com/KaydenClark/Agentic-Management-System/blob/088acb924e443aca7b4e20f67607c100f3b58c79/site/app/rsi/round-two.tsx)
and [data](https://github.com/KaydenClark/Agentic-Management-System/blob/088acb924e443aca7b4e20f67607c100f3b58c79/site/app/rsi/round-two-data.ts)
distinguish three qualified repairs, journey's owner-directed no-regression
merge, land's failed qualification, pruning development observations and an
unmeasured skill on hold. The whole page retains separate behavioral-trial
sections and explicit missing-evidence states. It does not establish a
whole-AMS trend: the new section explicitly excludes broader benefit, native
discovery and later use, with personal installation still pending.

The [merged round-two record](https://github.com/KaydenClark/Agentic-Management-System/blob/bbc9ff7f52988cb60a5800fca232297475437f3b/workbench/wiki/history/S-011.md#resumed-per-pr-rsi-round-two)
and direct skills PR state readback confirm four merges. This replaces the
earlier zero-merge endpoint for current context, without rewriting that failed
attempt. Three bounded qualification outcomes and one no-regression merge must
not be pooled into an overall improvement claim. The reused RUNBOOK case
remains development evidence, not a fresh held-out qualification.

Both exact-head CI jobs passed. The builder reports a completed build,
232 site tests and a 375px inspection; this watch did not rerun those checks.
At observation, PR #154 was open against dev, dev remained
`7441e9e351fe75397448431b25e6e994e2cac29d`, and deployed-page readback,
Human QA and production promotion were not established.

Three actionable issues already have owners in PR #154's unresolved review:
[unsupported native entry kinds](https://github.com/KaydenClark/Agentic-Management-System/pull/154#discussion_r4457357204),
[a missing entry boundary](https://github.com/KaydenClark/Agentic-Management-System/pull/154#discussion_r4457357219),
and [candidate-bar contrast overridden by CSS](https://github.com/KaydenClark/Agentic-Management-System/pull/154#discussion_r4457357231).
Source inspection corroborates the invalid metadata, missing delimiters and
equal-specificity CSS ordering; runtime effects were not independently
executed here. The unsupported metadata also exists in the named main
snapshot, so reconciliation should account for both main and the dev
candidate. These references preserve the existing review identities rather
than create duplicate findings or Tasks.

Next action: the existing builder/reviewer workflow resolves those findings
and verifies the resulting candidate and delivery. Keep F-002's whole-AMS
over-time purpose open for the existing S-007 review, while preserving honest
bounded evidence and missing proof. No replacement design, metric, test
campaign, acceptance or release permission is supplied by this observation.


#### Delivery reconciliation — 2026-11-03 16:17 UTC

A subsequent canonical GitHub readback supersedes the earlier open-PR state:
[PR #154](https://github.com/KaydenClark/Agentic-Management-System/pull/154)
merged at 16:14:57 UTC into dev
`0d8a8fbd8478194dbf92706b292e40330d075094`, containing candidate
`088acb924e443aca7b4e20f67607c100f3b58c79`. The three linked review findings
were posted at 16:15:09 UTC, after the merge, and were still unresolved and
not outdated at this readback. The merge therefore did not wait for that
review outcome. No newer corrective source was present on dev.

The round-two charts are now integrated source, not an unmerged candidate.
The existing parser/provenance/CSS findings also remain in that integrated
source; passing CI and the merge do not resolve them. Follow their existing
review identities through a checked correction and verify the resulting
delivery. The unsupported metadata in main needs its own target-aware
reconciliation as well. No deployment readback, owner QA, production
promotion or whole-system improvement is established by this merge.


## Additional linked review observation — 2026-11-03 16:49 UTC

Reporter: **owner-assistant**. Disposition: **diagnostic**.
Existing finding identity:
[PR #142 review, dynamic freshness included in the content hash](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4457543895).
Owning surfaces: S-007 RSI page and S-005 page-review hash contract.
This is a newly reported issue on unchanged site source, not a regression
introduced by records-only PR #155. No duplicate Task is created.

At dev `0fdd1e147a9d6143a16e0b3eba2d561a70bc8392`, source inspection
corroborates the review:

- [The loader](https://github.com/KaydenClark/Agentic-Management-System/blob/0fdd1e147a9d6143a16e0b3eba2d561a70bc8392/site/app/rsi/supabase.ts#L106)
  generates a fresh read timestamp for each successful data read.
- [The page](https://github.com/KaydenClark/Agentic-Management-System/blob/0fdd1e147a9d6143a16e0b3eba2d561a70bc8392/site/app/rsi/view.tsx#L278)
  renders that changing text without the review-exclusion marker.
- [The hashing implementation](https://github.com/KaydenClark/Agentic-Management-System/blob/0fdd1e147a9d6143a16e0b3eba2d561a70bc8392/site/scripts/page-hash.mjs)
  includes main-region text unless explicitly excluded. The
  [S-005 contract](https://github.com/KaydenClark/Agentic-Management-System/blob/0fdd1e147a9d6143a16e0b3eba2d561a70bc8392/workbench/landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/SPEC.md#decisions-and-contracts)
  binds review to that content hash.

Consequently, when live reads succeed, the hash can change solely because the
displayed freshness time changes, despite unchanged result rows. This is a
source-supported conditional mismatch, not an observed invalidation of an
actual owner's approval in this watch. No app, build or test suite ran.
Evaluated model: not-applicable; reviewer model: unknown.

Next action: follow the existing review finding through the owning workflow,
retain visible freshness, and verify that timestamp-only changes leave the
review identity stable while actual content changes still change it. This
record supplies no fix, design acceptance or release permission.

### Delivery evidence reconciliation

[PR #155](https://github.com/KaydenClark/Agentic-Management-System/pull/155)
merged four documentation changes, with no site-code change. Its
[new S-011 history entry](https://github.com/KaydenClark/Agentic-Management-System/blob/0fdd1e147a9d6143a16e0b3eba2d561a70bc8392/workbench/wiki/history/S-011.md#rsi-page-shows-round-two-on-dev-tk-003-evidence)
reports the builder's deployed-page browser readback: round-two charts rendered
and 41 links included no GitHub exits. GitHub also records a successful Vercel
deployment for dev `0fdd1e1` at 16:27:29 UTC. This adds builder-reported
rendering evidence; it is not this watch's independent browser verification or
a closure of the three earlier review findings. Human QA, personal
installation and production promotion remain open.
