---
type: memory
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Owner chat instruction, 2026-11-02: map and plan; stop before implementation
source_paths:
  - BLUEPRINT.md
last_verified: 2026-11-02
---

# Feedback-to-improvement loop: current understanding and prepared route

## Current understanding

The RSI Loop turns failures from real agent work into demonstrated improvements to shared skills and the Workbench, then checks later use for recurrence and regression. [LMK-004 — RSI Loop](../landmarks/LMK-004-rsi-loop-during-build/LANDMARK.md) owns this whole destination; [its synthesis](design-concepts/landmark-rsi-loop.md) explains the capability relationships. S-002 owns evaluation/qualification, S-000B worker execution/recovery, S-006 durable data, S-007 presentation, S-013 detection, S-011 source delivery and S-000A catalog refocus. Follow the [continuation guide](guidebooks/rsi-loop-continuation.md) for actual owners and release conditions, not a copied queue here.

Failures enter [WORKBENCH_FEEDBACK.md](../feedback/WORKBENCH_FEEDBACK.md). Diagnosis identifies whether the cause belongs to a skill, tool, environment, control or coordination. Cases and comparisons declare an observable outcome and intended useful benefit before evaluating the candidate against the current version and applicable controls. Existing r1 Fitness/Alignment qualification, Stable/Excellent, useful benefit and no regression all matter; a higher static score alone does not prove improved work. Failed attempts and inconclusive results remain evidence. Adoption and later observed use are distinct from source publication.

Worker-written, commit-pinned cases/runs/candidates/comparisons/dispositions belong in Supabase; raw transcripts remain local/private and safe Git exports are recovery copies. The Python worker runs outside Supabase, initially locally. An available database proves no running worker. Available Codex/Claude subscription meters govern model work, Mid/Small by default and High when needed. Preserve initial attempt → retry → retry → stop, baseline excluded; repairs or renames reset no counter or stopped campaign.

## Confirmed preparation and execution boundary

The owner launched Stage A and explicitly confirmed the [exact four-section readback](guidebooks/rsi-loop-readback-2026-11-04.md), sourced by [the confirmation entry](#jot-6a1d5383-d939-47b2-bd45-51e702c12550). Its body SHA-256 remains `427c3f0d3c109b3ce05011433920b2f74b7044b068c41a6e8d58b08a93d9e853`. Stage A delivered the [case contract](guidebooks/rsi-case-contract.md), [worker contract](guidebooks/rsi-worker-contract.md) and [bounded release graph](guidebooks/rsi-task-release.md). [The later delivery observation](#jot-9280ecbd-819b-4559-bf34-6f342a7402a9) records PR169's merge at `3e3078810753035f289f20e5f9bc268a61e0fbd3`: the earlier publication refusal is resolved, with both refusals preserved as history.

Earlier statements that the assembled readback was unconfirmed or publication blocked refer to earlier stages; they are not the current frontier. Confirmation covers meaning and Stage A executable preparation. A separate Stage B launch is still required. This Wiki repair starts no model trials, database writes, automation, skill installation, deployment or stopped campaigns, and does not select a catalog pilot. The [live release owners](guidebooks/rsi-loop-continuation.md) govern any future action. Merge, installation, observed loading, Human QA and website promotion retain separate authority.

## Relationships and unresolved proof

The [AMS purpose](context-ams-purpose.md) explains why the website build is the first application. The [Grill Board](context-grilling-board.md) supplies sourced owner corrections and quality feedback; [RSI presentation](design-concepts/landmark-rsi-presentation.md) displays evidence at its supported strength. [Wiki maintenance](guidebooks/wiki-maintenance.md) makes the resulting knowledge retrievable, but a successful local correction exercise is not broad RSI benefit.

The [preparation-bypass failure](../feedback/REPORT-skills-workbench-bypass-2026-11-02.md) remains a recurrence case, not an implemented systemic repair by this page. End-to-end autonomous improvement, later-use benefit and unfamiliar-work generalization still need their actual evidence. The existing schema and contracts explain how to collect it; their existence supplies none of those outcomes.

## Evidence and sources

- [LMK-004 source at the intake revision](https://github.com/KaydenClark/Agentic-Management-System/blob/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/landmarks/LMK-004-rsi-loop-during-build/LANDMARK.md) and the linked live owner distinguish destination and current authority.
- [Pinned confirmed readback](https://github.com/KaydenClark/Agentic-Management-System/blob/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/wiki/guidebooks/rsi-loop-readback-2026-11-04.md) retains exact meaning; [Landmark history](history/LMK-004.md) owns lifecycle chronology.
- Research links in earlier source revisions are design hypotheses, not demonstrated local benefit. This repair relies on inspected AMS owners and preserves their sources rather than reasserting unverified research conclusions.

## History

- 2026-11-04: S-000C repair reconciled the confirmed Stage A readback, delivered preparation and resolved PR169 publication hold with unchanged Stage B/campaign stops. Original entries remain byte-preserved below; a historical unresolved entry cannot reopen subsequently confirmed meaning.

<!-- jot-entry -->
### JOT-9179f5d2-dd33-42ed-b679-5bf49c79c078
Kind: intent
State: unresolved
Recorded: 2026-11-04T06:42:19.816Z
Author: Claude Opus 5.5 (align-concept)
Source: Kayden's AMS chat, 2026-11-03, /align-concept on the RSI loop
Topic: feedback-improvement-loop-plan
Supersedes: none

Owner-proposed RSI loop direction, pending interview and readback confirmation. Failures from real agent work should become demonstrated improvements to individual skills and the Workbench across capture, diagnosis, testing, repair, regression checks, adoption and later-use observation. WORKBENCH_FEEDBACK.md stays the canonical failure intake; each skill gets a traceable view of its failures and improvement evidence; relevant LLM_Workbench failures may expand coverage. Proposed architecture: Supabase Free for durable records and website data, a Python worker executing and coordinating the loop outside Supabase; local execution is recommended, hosting not approved. Why: repeated owner intervention and no shared agent understanding of the loop; inspected execution path is manually advanced and too narrow for real Workbench behaviors; Supabase stores results without the full lifecycle. More documentation, higher audit scores or familiar-case passes alone do not establish improvement. Intended loop: reproducible cases with observable success criteria; cause attributed to skill, tool, environment, instructions or coordination; candidate vs current and, where applicable, no-skill baseline; failed attempts preserved; regression and qualification enforced; adoption distinct from source publication; later skill version verified and recurrence detected; authorized work continues without the owner starting each step. Visuals show lifecycle progress, candidate comparisons, regressions, uncertainty, owner interventions and recurrence per eligible use; historical coverage and unfamiliar-work performance stay separate. Existing installation, publication, budget and stopped-campaign boundaries remain. Open interview frontier: owning record (revise S-002 vs new Spec), eligible improvement targets, canonical store per record kind, inference harness/provider and budget, autonomy gates, success-criterion form. No execution authority granted.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-f2ce313b-5c73-4043-942f-a97e00aeef6a
Kind: intent
State: unresolved
Recorded: 2026-11-04T06:50:23.373Z
Author: Claude Opus 5.5 (align-concept)
Source: Kayden's AMS chat, 2026-11-03, /align-concept round 1 answers
Topic: feedback-improvement-loop-plan
Supersedes: none

Owner answers to round 1 (settle interview choices; assembled intent still unconfirmed). A1: the Wiki records the full alignment so a later chat can update the Specs from it; both Wiki and Specs carry the destination. B1: the loop improves shared skills and AMS Workbench controls, tools and instructions alike ('RSI is RSI'). C1 confirmed: failures canonical in WORKBENCH_FEEDBACK.md; cases, runs, candidates, comparisons and dispositions canonical in Supabase, worker-written and commit-pinned; raw transcripts local and private with only derived fields in Supabase; a Git-committed export of Supabase rows. D1: Mid and Small tier models by default, High only when needed; Codex and Claude both allowed while the owner's metered plan has capacity. Correction: the owner pays no per-token API cost, so the cap is a number of attempts, not dollars. D2: a skill change may be merged once it is Stable or Excellent and has not regressed. E1 (owner correction, FAIL-034): a case passes when it passes the existing Fitness and Alignment checks AMS already uses; the agent should have recovered this from S-002 r1 rather than proposing a new criterion. Pending clarifications: target Spec for the later update, attempt-cap value, High-tier escalation trigger, meter-exhaustion behavior, who merges and whether installation stays an owner command, and how r1 applies to per-case runs.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-d07bee36-7b4a-4029-8124-1a4120e97ccd
Kind: intent
State: confirmed
Recorded: 2026-11-04T06:59:35.737Z
Author: Kayden (captured by Codex)
Source: Kayden's AMS chat, 2026-11-03, explicit attempt-limit confirmation and map request
Topic: feedback-improvement-loop-plan
Supersedes: none

Owner confirmation and Map authorization, 2026-11-03. Kayden explicitly retains the existing attempt limit and confirms that useful-benefit requirements remain alongside Fitness and Alignment qualification. He requests this agent to map the destination now, not hand it off to Claude. A1/B1/C1/D1/D2/E1 answers in JOT-f2ce313b remain settled: Wiki explains intent and Specs own requirements; shared skills and Workbench controls/tools/instructions are RSI targets; Markdown owns failure intake; Supabase owns worker-written commit-pinned cases/runs/candidates/comparisons/dispositions; raw transcripts remain local/private, with safe derived fields and a Git-committed export. Codex/Claude run on available subscription meters, Mid/Small by default and High when needed; no API-dollar cap. Initial attempt -> retry -> retry -> stop, baseline excluded; repair/rename does not reset attempts. Qualified Stable/Excellent skills without regression may merge under existing checks and useful-benefit requirements; this does not grant installation, restart stopped campaigns or replace their frozen model conditions. Existing attempts are not an unresolved choice. S-002 remains lifecycle owner, S-006 data, S-007 presentation, S-013 detection, S-011 shared-skill delivery. This request authorizes Map and its normal documentation delivery only: no new Tasks, claims, model trials, backend changes, installation or deployment. The earlier assembled readback remains proposed; these sourced answers and the explicit mapping request supply the scope of this map.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-0968ba30-e2b1-4784-8df4-b887f76949f0
Kind: intent
State: confirmed
Recorded: 2026-11-04T07:05:12.012Z
Author: Kayden (captured by Codex)
Source: Kayden's AMS chat, 2026-11-04, separation-of-concerns and RSI Landmark corrections
Topic: feedback-improvement-loop-plan
Supersedes: none

The owner permits more than one Spec for separation of concerns and identifies the RSI Loop as a LANDMARK. This supersedes the mapping interpretation that S-002 owns the whole lifecycle. Reuse LMK-004 as RSI Loop; S-002 owns evaluation/qualification, new planned S-000B worker execution/recovery, S-006 persistence, S-007 presentation, S-013 detection and S-011 source delivery. Cross-landmark links preserve existing placements and evidence. Mapping only, zero new Tasks; attempt and acceptance requirements remain unchanged.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-ceab17ab-3842-4b20-992a-4f0ad562eb65
Kind: intent
State: confirmed
Recorded: 2026-11-04T07:16:39.699Z
Author: Kayden (captured by Codex)
Source: Kayden's AMS chat, 2026-11-04, RSI Landmark correction and explicit merge approval
Topic: feedback-improvement-loop-plan
Supersedes: JOT-d07bee36-7b4a-4029-8124-1a4120e97ccd

The owner identifies the RSI Loop as a Landmark and permits capability-specific Specs. LMK-004 owns the whole destination; S-002 evaluation/qualification; S-000B execution/recovery; S-006 persistence; S-007 presentation; S-013 detection; S-011 shared-source delivery. This corrects only the earlier S-002 whole-lifecycle ownership interpretation. All other confirmed terms in the superseded entry remain: unchanged three-attempt limit with baseline excluded, metered Mid/Small Codex/Claude and High when needed, no API-dollar cap, existing Fitness/Alignment and Stable/Excellent/no-regression/useful-benefit gates, Markdown intake, canonical Supabase records with safe Git exports, local/private raw transcripts, and separate installation authority. Mapping creates one planned worker Spec and zero Tasks. The owner now explicitly approves merging this mapping into main; implementation and stopped trials remain unauthorized by this map.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-55876e5d-6957-4a4e-917b-8ba7245adee2
Kind: intent
State: confirmed
Recorded: 2026-11-04T07:28:56.703Z
Author: Kayden (captured by Codex)
Source: Kayden's AMS chat, 2026-11-04, RSI loop Map and Plan preparation request
Topic: feedback-improvement-loop-plan
Supersedes: none

The owner wants the RSI Loop to finish pointing in the mapped direction and requests orchestration of Map and Plan for the unrecorded remainder. Prepare a recoverable next chat to finish loop design and executable preparation, followed by a separate later chat to implement the prepared loop. This instruction authorizes current documentation and preparation, not implementation, model trials, database writes, automation, installation, or deployment. The earlier assembled readback is not confirmed wholesale by this request; the design stage must confirm the exact assembled readback and resolve genuinely open choices before affected implementation. Existing confirmed answers, attempts, stopped campaigns and separate release authorities remain in force.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-df911047-15f2-444b-84c8-35e347675c36
Kind: intent
State: confirmed
Recorded: 2026-11-04T07:39:57.714Z
Author: Kayden (captured by Codex)
Source: Kayden direct approval in AMS chat, 2026-11-04, publication question reply
Topic: feedback-improvement-loop-plan
Supersedes: none

Kayden explicitly answered "Approve push, PR, and checked merge" to publication of the 19 documentation-only RSI Map/Plan files to public KaydenClark/Agentic-Management-System, opening a PR and merging into main after shared CI passes. This approval addresses the automatic approval-review publication refusals; it authorizes no implementation, model trials, installation or deployment. Existing design confirmation, stopped campaigns, attempts and separate authorities remain unchanged.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-af4af602-47bf-4669-b131-65694f17ca37
Kind: intent
State: confirmed
Recorded: 2026-11-04T07:57:47.544Z
Author: Kayden (captured by Codex)
Source: chat:stage-a-launch-20261104
Topic: feedback-improvement-loop-plan
Supersedes: none

On 2026-11-04 Kayden instructed: “Launch Stage A: finish design, confirm the readback, and deliver executable preparation.” This releases owner:rsi-design-launch for LMK-004/TK-002M only. Activate that design assignment; preserve all child implementation holds. The assembled readback still requires actual confirmation. No software implementation, actual model trials, database writes, automation, personal installation, deployment, stopped-campaign resumption or wider catalog work is authorized. Both S-000A pilots and all prior attempt, qualification and separate release gates remain unchanged.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-6a1d5383-d939-47b2-bd45-51e702c12550
Kind: intent
State: confirmed
Recorded: 2026-11-04T08:05:56.881Z
Author: Kayden (captured by Codex)
Source: chat:stage-a-readback-confirmation-20261104
Topic: feedback-improvement-loop-plan
Supersedes: none

Kayden explicitly replied “Confirm the readback as written.” to the exact assembled four-section readback presented in the AMS chat on 2026-11-04. The exact body is preserved in guidebooks/rsi-loop-readback-2026-11-04.md, SHA-256 427c3f0d3c109b3ce05011433920b2f74b7044b068c41a6e8d58b08a93d9e853 (UTF-8, from Summary heading through final newline). This confirms meaning and Stage A documentation/executable preparation only. It does not authorize Stage B software implementation, model trials, database writes, automation, personal installation or deployment; prior attempt limits, stopped campaigns and both catalog pilots retain their scope and holds. The linked exact body supersedes earlier unconfirmed assembled wording only; sourced prior answers remain settled.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-8529e8c1-690d-42b2-a501-dcc1dcce4a06
Kind: verification
State: current
Recorded: 2026-11-04T08:23:25.859Z
Author: Codex Stage A record writer
Source: chat:stage-a-publication-refusal-20261104
Topic: feedback-improvement-loop-plan
Supersedes: none

Root reports final Stage A candidate 5cd3b976d7909d2ce4973cfb3d6ceebb90bd3054 passed both fresh independent Standards and Spec delta reviews with zero findings, and shared CI run 41798333987 passed 839 tests/6 skipped plus 10 browser checks. Draft PR169 targets main. Automatic approval review rejected its merge twice before execution: first, trusted user authorization for the asserted owner-only default-branch merge was absent despite green CI; second, after root supplied exact scoped non-site payload and pinned-policy evidence through the same connector action, trusted user content still lacked explicit promotion authority and repository policy claims could not supply it. No merge occurred, no alternate route was attempted. Main remains cfc0bc4c7f2cd167cea2972016edee076b479b73. These are publication approval refusals FAIL-079/080, not model trials or RSI candidate strikes. Record the concrete final PR/head and obtain explicit user merge approval; changed metadata still requires final delta review/CI. Readback and preparation are complete, checked default-branch delivery is blocked; Stage B, model campaigns, DB writes, automation, installation and deployment remain held.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-9280ecbd-819b-4559-bf34-6f342a7402a9
Kind: verification
State: current
Recorded: 2026-11-04T15:21:31.453Z
Author: Codex
Source: chat:automatic-merge-authority-20261104
Topic: feedback-improvement-loop-plan
Supersedes: JOT-8529e8c1-690d-42b2-a501-dcc1dcce4a06

Kayden challenged the repeated merge-approval requests in the direct AMS chat on 2026-11-04: "I don't know how many times we need to fix this so you can commit, PR, and merge things automatically". This continuation treated that instruction as authorization for routine checked delivery within the existing AMS scope. The original FAIL-079/080 denials explicitly distinguished trusted user authorization from permission quoted in repository policy. After verifying the unchanged non-site candidate 7dbcc98829627ea2152c616cc99035bcc26b31f2, passed independent metadata reviews and successful shared CI run 41799304048, the same GitHub connector merged PR169 into main at 3e3078810753035f289f20e5f9bc268a61e0fbd3. Fresh clone of main verified the merge and its candidate parent. The former publication hold is resolved for PR169; both refusals remain historical evidence. No approval setting or reviewer policy changed, and one successful merge does not establish that standing authorization will be recognized in every future session. Stage B implementation, campaigns, database writes, automation, installation, Human QA and website dev-to-main promotion retain their existing authority boundaries.
<!-- /jot-entry -->
