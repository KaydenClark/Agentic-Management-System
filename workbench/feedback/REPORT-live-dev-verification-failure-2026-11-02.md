# Live dev verification failure

## Target And Scope

Owner: S-003 website orientation; related S-007 page-order correction.
Date: 2026-11-02 (America/Denver). Failed candidate preserved at
`5ad0bdb7b45152bbbd1f04c7e3244d75ec7f2fba` in draft PR #136.
Source: this chat's local test runs and Kayden's instruction to report the
failure and retry. Evaluated model and reviewer model: unknown;
host: Codex desktop on macOS. This is the implementor's incident report,
not independent review or owner Human QA.

## Evidence And Limitations

The RSI ordering test failed before implementation and passed afterward
(7/7 focused tests). Two later full site test attempts failed after successful
builds. The first found undefined terms in the new Why opener and a repository
link helper that recognized only moving dev links. The second found that the
new immutable-example assertion selected every S-003 source on the page,
including a contextual link outside the historical example. The first issues
were corrected before that second run; the last assertion remained failing.
The saved candidate is not merge-ready. The accompanying Python run passed
772 tests, with 4 skipped; that does not erase the site failure.

## Findings

### F-001 — Verification changes exceeded the intended assertion scope

Severity: medium. Disposition: diagnostic; owner: S-003.
Evidence: `site/tests/tour-inventory.test.mjs` at the saved candidate selects
links across the whole page by path. The requirement concerns the historical
example section. A correct contextual link therefore fails the new check.
The agent widened the checked population without testing that boundary first.
This caused an avoidable failed verification and another owner intervention.

Bounded correction: select the example section, require its three distinct
Spec/Task identities, verify immutable revisions and their actual Git objects,
and include a contextual moving link outside that section as a negative
control. Run that focused test before the full suite. Keep unrelated source
link checks intact. A passing correction proves this check's scope, not
future agent reliability.

### F-002 — Check prerequisites and copy contracts were read too late

Severity: low. Disposition: diagnostic; owner: S-003.
The agent initially ran site tests while a build was still generating the
files they consume, and later invoked a build from the repository root
instead of site/. Neither established a product defect. The new Why opener
also failed the existing glossary/definition contract. These were avoidable
ordering, directory and contract mistakes, not evidence of a broken harness.

Preventive procedure for the retry: read the relevant test contract, name the
working directory, await the build, then run built-output checks. Check new
copy against the opener vocabulary rules before the full suite. Expected TDD
red results remain distinct from failed candidate verification. Apply the
project's stop rule to real failed verification attempts and preserve output.

## Challenged Or Rejected Findings

No evidence establishes a defect in a shared skill, model quality, or general
harness reliability. Do not patch shared skills or claim measured improvement
from this report. The owner authorized another bounded attempt; the stopped
candidate and both failed attempts remain historical evidence.

## Next Action And Review Boundary

Repair the scoped assertion, implement the already requested MIT license and
skills-wiki refresh, verify the exact candidate, and publish through the
project's separate main and dev routes. Review/acceptance and demonstrated
later-use benefit remain unestablished. Update this report with actual retry
results rather than promising that recurrence is impossible.

## Retry evidence and recurrence

Kayden explicitly authorized a retry in this chat. Site candidate
`1d2b70d88ac699cbc922f8eb607283cdada23d75` changes the historical-example check
in `site/tests/tour-inventory.test.mjs` to select its section and verify all
three source identities. An outside moving link is accepted and an inside
moving link is rejected. Focused execution: 1 passed. F-001 disposition is now
**test** for that scoped assertion, with the saved candidate as evidence;
no general reliability claim follows.

F-002 recurred during this retry: the agent invoked built-article tests after
changing the catalog source pin and before rebuilding. Two assertions read the
old pin from generated HTML and failed. The first report did not prevent that
ordering mistake. After awaiting `npm run build` in site/, `npm test` passed
all 206 tests. This corrects the current verification result but leaves future
recurrence prevention unproven. F-002 remains **diagnostic**, rather than
repaired or an improvement claim. No shared harness code or installed skill
was changed to compensate for the agent's mistake.

The current published skills revision was checked against remote main;
39 articles were checked against a Git archive made at that revision, with
zero source-copy findings. These results and license application do not
qualify unfinished skill repairs, prove native activation or supply Human QA.
