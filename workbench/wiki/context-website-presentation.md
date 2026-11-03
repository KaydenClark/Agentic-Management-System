---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, S-003 repair chat and owner corrections, 2026-11-01
  - Existing S-003 and S-007 execution reports at 97bfcaa
  - Owner decisions in chat, 2026-11-02 (paraphrased; entries below)
  - Kayden, RSI proof and skill-improvement scope correction, 2026-11-02
source_paths:
  - BLUEPRINT.md
  - workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md
  - workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md
  - workbench/landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/SPEC.md
last_verified: 2026-11-02
---

# Website presentation: intent, corrections and history

The website explains and demonstrates AMS. Visitors come for understanding; it is not a live control panel. [S-003](../landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) owns the shell and orientation. [S-007](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) owns RSI evidence presentation. These Specs own their destinations; this article preserves context and grants no implementation or release authority.

For RSI, the [approved correction](#jot-cf0db5e8-89b7-4766-85d7-1f101bfc3aaa) requires visible real-evidence charts and useful supporting information on the website. Omit irrelevant material and GitHub exits; retain source identity, failures and evidence limits. Implementation is authorized for this correction; other website feedback and production promotion retain their own boundaries.

## RSI proof during website development

Confirmed by Kayden in chat, 2026-11-02; the [sourced correction](#jot-052e2b9a-85fc-4813-bad1-6039aa017f9c) preserves the intent. This AMS project develops and proves shared skill improvements through the website build. Workflow and process issues found during that work feed the RSI loop: record the issue and baseline, repair the owning skills, compare before and after here, log the evidence and disposition, and display the RSI log on the website. Retain failures, regressions and unknowns; an issue report or merged repair alone proves no improvement.

For each issue, ask how the skill correction prevents recurrence in any project. This project is the proving ground for improving the whole workflow and system. Shared methods live in `KaydenClark/skills`; the [later owner instruction](#jot-8c178984-eede-44cc-8c58-33f137a551c6) authorizes installing qualifying repairs in this machine's personal catalog. Installing them into other projects remains outside scope and is not an additional proof gate. [Blueprint](../../BLUEPRINT.md) owns this purpose, [S-002](../landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) owns comparisons, S-006 owns stored results, and S-007 owns their presentation.

## Owner brief and corrections, 2026-11-01

Later catalog direction: [S-000A](../landmarks/LMK-004-rsi-loop-during-build/specs/S-000A-skills-refocus/SPEC.md) prepares distinct jobs/methods, Primitive/Compound composition, actual Setup Workbench prerequisites and retained adaptation credit. S-008's next accepted source pin must explain these faithfully. This changes the documentation destination; no rewritten skill, trial, public article update or deployment is established by preparation.

Kind: intent. State: confirmed. Source: Kayden's opening brief and subsequent answers in the S-003 repair chat.

The original brief requires the full first build, not a reduced website demo: local Python Grill Board; real-data RSI presentation with initially empty chart spaces; the Next.js website with tour, skills wiki, demo board, governance and flow charts; and the safeguarded RSI loop. Python writes results to Supabase and the site reads them. The later secret-location decision remains authoritative: ADR-003H keeps the service key local; the site uses only read access.

The owner requested deeper page briefs and a proper, auditable destination. Visitors come for understanding. Content requirements must state what the explanation achieves; CI is not proof that visitors understand it. Missing incidental details must not become owner gates. Existing facts are discoverable work; ask about consequential uncertainty rather than invent requirements.

About explains the AMS project: what it is, who made it and why. Kayden explicitly rejected a CV/resume requirement after an agent treated ambiguous wording as a blocker. The quickstart serves understanding rather than installation.

There is no page titled “Under the hood.” Kayden explained that the RSI page and skills wiki already serve that purpose and that the website presents the system as a floor model. S-007 therefore explains build activity and measured results, while S-008 explains skills. Readable prose may connect sourced events; requiring each sentence to originate in a database row was excessive.

The owner directed: “History goes in the wiki, not on the SPEC.” Specifications state destinations; this article retains the earlier account with source links. This rewrite authorizes documentation only, not website implementation or new acceptance.

## Owner corrections, 2026-11-02

Kind: intent. State: confirmed. Source: the owner in chat, 2026-11-02, paraphrased in the entries below ([JOT-90878239](#jot-90878239-ede0-41d9-bc5a-aea988e679b2), [JOT-76ddc50f](#jot-76ddc50f-c446-4fc9-8c50-f5fd8515ad78), [JOT-ab257a24](#jot-ab257a24-3630-4184-ac69-4f9fa3d9fb38)).

- The site shows no owner quotations and uses none of the owner's actual instructions to agents as examples; it paraphrases and links the source. The earlier verbatim-with-source rule is withdrawn ([DDR-001A](../docs/ddr/001A-the-public-site-shows-no-owner-quotations.md)).
- The site shows no draft, approval or review banner, mark or status. Owner review on the Grill Board, bound to the content hash, stays an internal record and never changes what visitors see ([DDR-001B](../docs/ddr/001B-the-public-site-shows-no-review-status.md)).
- Quickstart folds into Start here at `/start`, which tells readers to use the `setup-workbench` skill to set up a Workbench; no `/quickstart` page and no command replay.

S-003, S-005 and LMK-003 state the new destination. S-003 TK-003 and TK-004 and S-005 TK-002 still carry the withdrawn instructions and need reconciling before they run; the site's quote convention, quote tests and existing draft notices on `dev` are site work.

## Effect on existing assignments

The new S-003 destination supersedes TK-003's resume-summary and fresh-clone command-replay instructions. About explains AMS and Quickstart is a reading route. TK-006's dedicated build-history page is withdrawn; S-007 owns the build-evidence explanation. Reconcile those assignments before any implementation resumes, preserving their receipts. The specification repair creates no Tasks and claims no implementation completion.

## Historical implementation reports and limits

The [previous S-003 at 97bfcaa](https://github.com/KaydenClark/Agentic-Management-System/blob/97bfcaa/workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) retains the original reports, counts, candidates and limitations. They describe work performed against an older destination, not acceptance of the revised one.

The shell report (PR #13) records local build/browser checks and READY deployment metadata, but says the deployed footer SHA and text were not fetched. The first tour pages (PR #23) report local content/link checks; their moving dev source links were identified as a risk when Task records are retired. The local quality checks (PR #25) report accessibility and network checks, with limits on focus measurement and no deployed screenshots. Theme integration (PR #32) checks shared color tokens; the report explicitly lacks type/spacing source coverage. Later PRs #63 and #67 changed layout and Start here. Follow the existing S-003 Task receipts for their exact scope rather than treating a closed Task as Spec acceptance.

The [previous S-007 at 97bfcaa](https://github.com/KaydenClark/Agentic-Management-System/blob/97bfcaa/workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) records the initial empty-chart implementation (PR #14). Local tests and deployment metadata did not establish a live Supabase reader or rendered deployed-page verification. These are dated reports; current behavior requires candidate-specific inspection.

## History

- 2026-11-01: created during owner-authorized S-003 specification repair. Preserved the opening brief, subsequent corrections and source-linked execution history; moved historical explanations out of the two affected Specs. No website implementation, Human QA or outcome acceptance performed.
- 2026-11-02: recorded the owner's corrections on owner quotations, review banners and the Quickstart page; records only, no site change.
- 2026-11-02: clarified that website development proves shared skill improvements here, records before/after in RSI and displays the log; installation into other projects is outside this project.

<!-- jot-entry -->
### JOT-90878239-ede0-41d9-bc5a-aea988e679b2
Kind: intent
State: confirmed
Recorded: 2026-11-02T15:42:34.223Z
Author: Kayden
Source: Owner (Kayden), in chat, 2026-11-02, relayed by the coordinating session; paraphrased
Topic: website-presentation
Supersedes: none

Paraphrased owner decision: the public website never shows the owner's quotations and never uses the owner's actual instructions or commands to agents as examples. Where a page relies on what the owner decided, it paraphrases and links the source record. This withdraws the earlier rule that owner words may appear on the site verbatim with their source (S-003 Data and approvals; S-005 Decisions And Contracts). Internal records may still hold sourced owner wording; this governs only what visitors see. Effect: S-003, S-005 and LMK-003 restate the rule; the site's owner-quote figure convention and verbatim-quote test are site work for orchestrator A on dev.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-76ddc50f-c446-4fc9-8c50-f5fd8515ad78
Kind: intent
State: confirmed
Recorded: 2026-11-02T15:42:34.389Z
Author: Kayden
Source: Owner (Kayden), in chat, 2026-11-02, relayed by the coordinating session; paraphrased
Topic: website-presentation
Supersedes: none

Paraphrased owner decision: the public website shows no draft, approval or review banner, mark or status on any page. A public site does not tell visitors whether its owner reviewed a page. Owner review of pages through S-005 page cards, with approval bound to the page content hash on the Grill Board, may stay as an owner-facing internal record, but it never changes what visitors see. This withdraws the draft-until-approved mark in S-003 and LMK-003 and the restored-draft-mark behavior in S-005. Effect: S-003 TK-004 (draft marks) loses its destination and needs reconciling; existing draft notices on dev pages (for example /start and the skills articles) are site work for orchestrator A.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-ab257a24-3630-4184-ac69-4f9fa3d9fb38
Kind: intent
State: confirmed
Recorded: 2026-11-02T15:42:34.556Z
Author: Kayden
Source: Owner (Kayden), in chat, 2026-11-02, relayed by the coordinating session; paraphrased
Topic: website-presentation
Supersedes: none

Paraphrased owner decision: Quickstart is folded into Start here as one page at /start; there is no separate /quickstart page. That page tells readers to use the setup-workbench skill to set up a Workbench. The reading route through the tour stays; the page does not replay setup commands or become an installation guide. Effect: S-003 Orientation content and the Route criterion restate this; S-003 TK-003's quickstart page and fresh-clone replay need reconciling before implementation resumes.
<!-- /jot-entry -->

## Start-page correction — 2026-11-02

Kayden requested reconciliation of main's reusable intent-to-outcome definition
into dev, preserving newer site work, and correction of the claim that RSI is
empty. The correction retains dev's skills diagram and integrated Quickstart,
uses owner roles, and describes the existing RSI repair checks, failures and gaps
as development evidence that does not establish demonstrated improvement.
This correction does not establish measured benefit, deployed-page verification
or owner Human QA.

## Live dev follow-up — 2026-11-02

Owner-authorized browser inspection of dev ce39c6a confirmed the Start wording
and working toy advance. Home, Why and the generated glossary still used the
older personal-system framing. The correction carries main's Home/glossary
meaning into dev, aligns Why, and updates How it works to acknowledge RSI repair
evidence without claiming improvement. The real Spec/Task example is pinned to
ce39c6a, which contains the described records and receipts; later record moves
must not rewrite that historical account. This also repairs the mutable-example
source mismatch recorded by the owner-assistant's source inspection.

The RSI title now precedes its repair evidence and trial charts. These are site
corrections, not Spec acceptance, owner Human QA or demonstrated benefit.
Kayden subsequently authorized both license application and a current-source
refresh of the skills wiki; the retry below records that work.

## Authorized retry — 2026-11-02

The immutable-source check now selects only the historical example and requires
its distinct Spec and two Task links. Its negative controls accept a contextual
moving link outside the example and reject one inside. The focused check passes.
The MIT file is populated under the recorded decision and explicit owner request;
About describes that file. Non-site license/report delivery uses PR #137 to main;
site changes use PR #136 to dev.

The 39 skills articles now name published catalog commit
`fb7ad23c963e183b930b23bc5fdf4d309dff292a`, checked against remote main. The source
comparison included referenced methods and setup assets, not just SKILL.md.
Affected articles describe Spec history on the Wiki history page. The handoff
article distinguishes the unchanged published method from AMS's local-only note
rule; unfinished repair candidates remain unfinished. A Git archive made from
that exact commit supplied the source-copy check: 39 articles, zero findings;
the checker itself skipped Git HEAD comparison because the archive has no .git.
This is source inspection and documentation checking, not skill activation or
behavioral benefit evidence.

One stale-output failure recurred during the retry: built-article tests were
invoked after the source pin changed but before rebuilding. After a completed
build, all 206 site tests passed. The incident report must retain that recurrence;
recording preventive steps did not itself prevent it. No owner Human QA claimed.

<!-- jot-entry -->
### JOT-052e2b9a-85fc-4813-bad1-6039aa017f9c
Kind: intent
State: confirmed
Recorded: 2026-11-02T17:09:39.584Z
Author: Kayden
Source: Kayden, AMS documentation correction and installation-scope clarification in chat, 2026-11-02
Topic: website-presentation
Supersedes: none

Kayden confirms that this AMS project is where shared skill improvements are developed and proved through actual website work. Find workflow and process issues while building, record each issue, repair the owning skills, compare before and after here, record the evidence and disposition in the RSI log, and display that log on the website. Recurring failures are inputs to improving the whole workflow and system for use in any project. The question of preventing recurrence in any project governs how the shared skills are repaired; proving the repair belongs to this project. This project improves the skills and does not install them into other projects. Cross-project installation or rollout is not this project's work or proof gate. This corrects the agent's proposed portfolio rollout and separate proof-project framing. The requested action is documentation correction; this entry claims no skill repair, measured result, database write, website implementation or deployment.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-8c178984-eede-44cc-8c58-33f137a551c6
Kind: intent
State: confirmed
Recorded: 2026-11-02T20:40:20.003Z
Author: Kayden
Source: Kayden, shared-skill repair instruction in AMS chat, 2026-11-02
Topic: website-presentation
Supersedes: none

The shared handoff, branch and cleanup repairs must be logged and displayed with their actual RSI test and audit results on dev. Terra 6.1 tests and audits govern the requested Stable or Excellent skill merge gate. The owner explicitly authorizes updating this machine personal skills folder after a qualifying repair. The earlier exclusion of installation into other projects remains: personal-catalog installation is a different action. Keep handoffs local and ignored; publish Tasks and safe evidence summaries, never the private source text or raw evaluation material. A measured audit score is separate from demonstrated behavioral benefit and whole-AMS fitness.
<!-- /jot-entry -->

## Verification failure and owner-authorized retry — 2026-11-02

Kayden requested a failure report and another attempt after the website
correction stopped on two failed verification runs. The
[incident report](../feedback/REPORT-live-dev-verification-failure-2026-11-02.md)
retains both attempts and the narrower-check and sequential-build corrections.
Kayden also explicitly requested applying the recorded MIT license and
updating the public skills wiki. This authorizes those corrections, not
installing skills, promoting unfinished catalog candidates, owner Human QA
or dev-to-main site promotion. Recording the failure proves no prevention
benefit; the retry must supply its actual results.

<!-- jot-entry -->
### JOT-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458
Kind: intent
State: confirmed
Recorded: 2026-11-03T01:29:33.714Z
Author: Kayden
Source: Kayden, website feedback and explicit approval of five-item readback in AMS chat, 2026-11-02
Topic: website-presentation
Supersedes: none

The owner approved five website changes for task preparation: consolidate the overlapping Home, Start Here, Why and How It Works presentation, treating Start Here as About; use a conventional full-width persistent navigation header with the home icon at top left and light/dark toggle at far right; redesign the glossary as a fun visual explanation of definitions; enlarge site text and improve readability; visibly use the Grill Board palette across both themes. Exact page consolidation and glossary design remain implementation choices within those outcomes. This approval authorizes recording tasks for the next agent, not implementing the site, claiming Human QA, deployment or dev-to-main promotion. This supersedes the requirement for separately presented Start Here/About orientation, while preserving the required explanatory subjects.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-78d8b232-f2c6-4697-ab8c-9e25f60760ba
Kind: intent
State: unresolved
Recorded: 2026-11-03T01:29:43.808Z
Author: Kayden
Source: Kayden, additional website feedback in AMS chat, 2026-11-02; individual readback pending
Topic: website-presentation
Supersedes: none

Additional owner direction: website examples and showcase links should stay on the website rather than sending visitors to GitHub. If material belongs on the website, present it there; otherwise omit it as an example. The agent will read back this requirement before creating its task, as requested for each feedback item. Existing requirements for GitHub-linked sources and deployed SHA need reconciliation after that readback is approved; no exception for those links has been agreed. This pending readback is not task or implementation approval.
<!-- /jot-entry -->

## Feedback task preparation verification — 2026-11-02

Five approved feedback Tasks were prepared under S-003 (TK-001P through TK-001T); website-only example links remain pending readback. Record/layout validation and diff whitespace checks passed. The hygiene check failed twice because the modified S-003 exceeded its 8,000-character budget: 9,934 characters on the first attempt, 8,782 after shortening. Work stopped under the project three-strike rule; do not merge this candidate until an authorized retry repairs the size failure and checks pass. No site implementation, deployment or Human QA is claimed.

### Owner-authorized size repair and publication retry

Kayden explicitly authorized pushing `docs/website-feedback-tasks`, opening its PR, repairing the size issue and merging after checks pass. The Spec was shortened to 7,997 characters without dropping its required subjects or changing the 8,000-character budget. Hygiene, layout, decision-record and whitespace checks pass. The earlier failures remain historical evidence; merge still requires passing checks on the candidate. The website-only link readback remains pending and has no Task; this publication approval does not confirm that readback or implement the website.


## Checker evidence presentation — 2026-11-02

S-007/TK-001W presents the bounded checker repair, observations and remaining limits on `/rsi`, linked to the immutable safe report. Site source `77ed4478ee8294f3f4cbd38e270c1514245ed170` was assembled at `1b07f1e72cc4419ad017af3fe0f76fc7f1e8fc9e`. The worker reported a passing build, 209 tests including 10 focused checks, and desktop inspection. Root inspected the actual build at 375px with a 360px document and no horizontal overflow; the console showed a favicon 404 and stylesheet preload warnings. An earlier page-hash link regression failed and was repaired. These observations do not prove owner Human QA, deployment, behavioral benefit or the complete learning cycle. See the [Task](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/tasks/TK-001W/TASK.md) and [PR 141](https://github.com/KaydenClark/Agentic-Management-System/pull/141).

<!-- jot-entry -->
### JOT-9203891f-d937-480d-8d08-83bcf77eddd8
Kind: intent
State: confirmed
Recorded: 2026-11-03T05:27:28.327Z
Author: Kayden
Source: Kayden, RSI Results feedback and scope answer in AMS chat, 2026-11-02
Topic: website-presentation
Supersedes: none

The RSI Results page must visibly chart relevant real results and present the useful explanation and supporting evidence on the website. Material that is not relevant enough to present there should be omitted; readers must not be sent to GitHub. This settles the RSI-page portion of the earlier website-only feedback without treating other pages as approved work. Kayden explicitly chose: Read back and prepare the task, rather than implement the page correction now. Prepare one bounded S-007 task covering chart visibility, on-site evidence and removal of GitHub exits from the RSI reader experience, including shared chrome where it supplies those exits. Preserve provenance, honest empty/unavailable states and the distinction between audits, development observations and demonstrated improvement. No website implementation, task claim, campaign, deployment or dev-to-main promotion is authorized by this preparation.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-d795477b-63fe-4264-8ca9-7ba15e5d4470
Kind: intent
State: confirmed
Recorded: 2026-11-03T05:28:10.350Z
Author: Kayden
Source: Kayden, explicit readback-before-plan correction in AMS chat, 2026-11-02
Topic: website-presentation
Supersedes: JOT-9203891f-d937-480d-8d08-83bcf77eddd8

Kayden explicitly requires the readback before planning. Stop at the proposed readback; no Task or Spec change until it is reviewed. The preceding entry records the RSI feedback and intended preparation scope, not approval of an agent-written readback, task breakdown or shared-footer design. No Task, implementation or deployment has been performed.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-cf0db5e8-89b7-4766-85d7-1f101bfc3aaa
Kind: intent
State: confirmed
Recorded: 2026-11-03T05:33:14.467Z
Author: Kayden
Source: Kayden, approval of RSI readback and website implementation in AMS chat, 2026-11-02
Topic: website-presentation
Supersedes: JOT-d795477b-63fe-4264-8ca9-7ba15e5d4470

Kayden confirmed the readback and explicitly authorized fixing the website now. Implement visible charts of real RSI evidence, keep relevant explanation and supporting information on the website, omit irrelevant material, and remove GitHub links from the RSI reader experience. The readback-only hold is released for this correction. Preserve honest empty/unavailable states, source identity and the distinction between development observations, audit scores and demonstrated improvement. This does not authorize new trial campaigns, skill installation or owner-only dev-to-main site promotion.
<!-- /jot-entry -->
