---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, S-003 repair chat and owner corrections, 2026-11-01
  - Existing S-003 and S-007 execution reports at 97bfcaa
  - Owner decisions in chat, 2026-11-02 (paraphrased; entries below)
source_paths:
  - workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md
  - workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md
  - workbench/landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/SPEC.md
last_verified: 2026-11-02
---

# Website presentation: intent, corrections and history

The website explains and demonstrates AMS. Visitors come for understanding; it is not a live control panel. [S-003](../landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) owns the shell and orientation. [S-007](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) owns RSI evidence presentation. These Specs own their destinations; this article preserves context and grants no implementation or release authority.

## Owner brief and corrections, 2026-11-01

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
