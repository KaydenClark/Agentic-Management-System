---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, S-003 repair chat and owner corrections, 2026-11-01
  - Existing S-003 and S-007 execution reports at 97bfcaa
source_paths:
  - workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md
  - workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md
last_verified: 2026-11-01
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

## Effect on existing assignments

The new S-003 destination supersedes TK-003's resume-summary and fresh-clone command-replay instructions. About explains AMS and Quickstart is a reading route. TK-006's dedicated build-history page is withdrawn; S-007 owns the build-evidence explanation. Reconcile those assignments before any implementation resumes, preserving their receipts. The specification repair creates no Tasks and claims no implementation completion.

## Historical implementation reports and limits

The [previous S-003 at 97bfcaa](https://github.com/KaydenClark/Agentic-Management-System/blob/97bfcaa/workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) retains the original reports, counts, candidates and limitations. They describe work performed against an older destination, not acceptance of the revised one.

The shell report (PR #13) records local build/browser checks and READY deployment metadata, but says the deployed footer SHA and text were not fetched. The first tour pages (PR #23) report local content/link checks; their moving dev source links were identified as a risk when Task records are retired. The local quality checks (PR #25) report accessibility and network checks, with limits on focus measurement and no deployed screenshots. Theme integration (PR #32) checks shared color tokens; the report explicitly lacks type/spacing source coverage. Later PRs #63 and #67 changed layout and Start here. Follow the existing S-003 Task receipts for their exact scope rather than treating a closed Task as Spec acceptance.

The [previous S-007 at 97bfcaa](https://github.com/KaydenClark/Agentic-Management-System/blob/97bfcaa/workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) records the initial empty-chart implementation (PR #14). Local tests and deployment metadata did not establish a live Supabase reader or rendered deployed-page verification. These are dated reports; current behavior requires candidate-specific inspection.

## History

- 2026-11-01: created during owner-authorized S-003 specification repair. Preserved the opening brief, subsequent corrections and source-linked execution history; moved historical explanations out of the two affected Specs. No website implementation, Human QA or outcome acceptance performed.
