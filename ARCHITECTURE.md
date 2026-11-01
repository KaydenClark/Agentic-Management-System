# AMS Architecture

AMS uses and repairs the Workbench while operating Kayden's agents, workflows, intent capture, skills and tools in one RSI loop. [Blueprint](BLUEPRINT.md) owns the destination. This map routes information; AGENTS owns instruction authority.

Adapted from LLM_Workbench `templates/ARCHITECTURE.md` at `227d7c2a3ca0`; AMS routing updated 2026-10-31. Runtime and delivery configuration remain unimplemented.

## Codemap

| Path | What lives there |
|---|---|
| `src/` | AMS runtime software |
| `tests/` | Software correctness tests |
| `site/` | Public showcase website; planned Vercel hosting and Supabase backend |
| `grill-board/` | Separate locally hosted question-and-answer tool for development; not part of the public website |
| `evals/` | RSI trials, graders and measured results |
| `.agents/skills/` | Project-owned skills; personal catalog stays independent |
| `.claude/skills` | Discovery symlink to ../.agents/skills |
| Root files | `AGENTS.md`, `BLUEPRINT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, `RUNBOOK.md`, `README.md`, `TASKBOARD.md` and the `CLAUDE.md` host adapter; their jobs are in [Ownership](#ownership). |
| `workbench/` | Specs and Tasks, the Wiki, decision records, research, sessions and feedback; software lives in `src/` and skills in `.agents/skills/`. |

## Ownership

An artifact is an identifiable document, record, source file or output. Its owner is the maintained location of a kind of truth; its maintainer is the person or assigned agent keeping it current. Information ownership grants no permission to act.

| Job | Definition and owned content | Agent question | Maintained owner / route |
|---|---|---|---|
| **Authority** | Establish who may authorize an action and which instructions apply. | Who can authorize this? | Current user request -> [AGENTS](AGENTS.md#enter-and-scope-the-work); the assigned Spec delegates only its bounded capability. |
| **Boundaries** | Limit the authorized action: scope, protected resources, prohibitions, approvals, privacy and external effects. | May I change or expose this? | [AGENTS](AGENTS.md); the current request and assigned Spec may narrow the task. |
| **Destination** | Describe the desired finished product, its people, purpose, experience, outcomes, qualities and non-goals. | What are we trying to build, and why? | [Blueprint](BLUEPRINT.md). |
| **Requirements** | Define the behavior, interfaces, constraints and exclusions of one capability. | What must this capability do? | Assigned stable `SPEC.md` -> Desired Behavior, Decisions And Contracts, Non-Goals. Cross-cutting qualities stay in the Blueprint. |
| **Decisions** | Preserve an accepted choice, its rationale, alternatives, consequences and supersession. | What was decided, and why this choice? | `workbench/decisions/` -> the relevant decision record; capability-local choices stay in the owning Spec. |
| **Language** | Define shared terms, aliases and distinctions precisely. | What does this word mean here? | [Glossary](GLOSSARY.md) -> the term; its Wiki explanation goes deeper. Capability-only terms remain in their Spec until shared. |
| **Knowledge** | Explain durable concepts and source-backed context that help a reader understand the project. | What do I need to understand about this? | [Wiki MEMORY](workbench/wiki/MEMORY.md) -> relevant note or Design Concept article -> governing sources. |
| **Navigation** | Connect a question to its smallest relevant information owner. | Where should I look? | This file's [Routes](#routes); Wiki MEMORY routes inside the Wiki; the agreed layout supplies locations. |
| **Work state** | Record assignment, priority, progress, dependencies, blockers, latest event and next gate. | What is happening, who owns it, and what is next? | Owning `SPEC.md` and its Tasks; [Taskboard](TASKBOARD.md) displays their current view; no generator is installed. |
| **Acceptance** | Specify the observable conditions and required proof for declaring an outcome complete. | What would count as done? | Assigned Spec -> Acceptance Criteria and Verification Procedure; AGENTS owns project-wide verification and review obligations. |
| **Evidence** | Record the candidate, method, observer or producer, result, limits and source needed to assess a claim. | What was actually checked, and what does it prove? | Spec evidence log -> named test, review, report or result artifact. Evaluation records own their observations; the Spec links the proof relevant to its acceptance. |
| **Operations** | Govern how authorized work moves through selection, execution, verification, maintenance and delivery. | What operation applies, and what are its entry and exit conditions? | [AGENTS](AGENTS.md) owns lifecycle obligations; the Runbook workflow routes to the skill each operation follows, which points to where each operation's prerequisites and expected results live. |
| **Procedures** | Describe the repeatable steps, inputs, commands, failure handling and checks for a particular operation. | How do I perform this operation here? | [Runbook workflow route](RUNBOOK.md#workflows) -> the named skill's procedure and tool; a workflow's steps are its [Runbook entry](RUNBOOK.md#workflows). A linked Wiki guidebook may hold an extended procedure without copying its governing rules. |
| **Reusable behavior** | Define a method for a recurring kind of work and the posture of a stance. | Which method or stance should I apply? | Load the relevant existing personal skill by its actual discovery route; use the inactive authoring skeleton only for a separately authorized AMS-owned capability. A skill inherits scope. |
| **Execution** | Carry out the authorized operation in a concrete environment and produce an observable result. | What runs, where does it run, and what happened? | Named source/tool and actual host configuration own the mechanism; Runbook explains invocation; Spec records the resulting state and evidence. A procedure is not a run. |
| **Configuration** | Declare paths, identity, dependencies, installed components and host settings. | What is configured here? | [AMS configuration remains unfilled; manifest and receipt mechanisms are deferred.] Runbook routes setup and inspection. |
| **Capability** | Establish which operations the configured environment can actually perform and under what limitations. | Can this environment do the requested operation? | Checks of the actual configured host -> actual host/tool and its result. A manifest declaration or installed file alone is insufficient. |
| **Working context** | Preserve unfinished reasoning, corrections, source references and unresolved questions for one objective. | What would otherwise be lost with this conversation? | Relevant topic Wiki page through `jot`, with source, claim kind/status and linked corrections; new project context is shared by default and explicit private capture stays ignored. Settled requirements, definitions and decisions retain their existing owners. Old JSON formats remain available as compatibility examples; no reader is installed here. |
| **Recovery** | Restore a verified, usable state after interruption or failure and establish a safe continuation point. | What survived, and how can I resume or roll back? | [Runbook recovery](RUNBOOK.md#recovery) -> existing root files, Spec, source, relevant Wiki context or legacy note, and any recovery receipt or backup. Recheck live state before acting. |
| **Handoff** | Communicate a delegated job, completion report or update to a specified recipient in another context, as a readable map to the context the records already hold. | What should this receiving agent do, and where is the context it needs? | Local Markdown instructions and selected context from accessible owners and relevant notes; it does not replace them. Delegation follows the current AGENTS authorization boundary. |
| **Feedback** | Preserve observed failures, friction, impact, uncertainties and proposed corrections. | What went wrong, and what should be investigated? | `workbench/feedback/` -> occurrence/report -> source evidence. An authorized repair and its disposition belong in the owning Spec. |
| **Evaluation** | Define comparisons and assess whether a change improves outcomes, including costs and uncertainty. | Does this Workbench help agents complete better work? | [RSI workflow](RUNBOOK.md#rsi-during-website-work) -> named evaluation task, result and comparison records; the relevant Spec owns acceptance. Structural checks do not establish agent outcomes. |
| **Provenance and history** | Preserve origins, revisions, producers, corrections and superseded claims without presenting them as current. | Where did this claim or component come from? | The owning artifact's provenance/evidence, Git history, ADR history or component receipt. Retired checkpoints remain history. |
| **Delivery and release** | Establish the verified candidate, integration containment, published version and installed consumer state separately. | Is this change delivered here, or only prepared? | AGENTS owns approval/review boundaries; [Runbook publication](RUNBOOK.md#version-control-and-publication) names the unresolved delivery configuration; the delivery Spec owns proof linked to actual Git, release and installation records. |
| **Human orientation** | Explain what the project is, who it is for, and how a person starts using it. | How do I get started? | [README](README.md), linking operational detail to the Runbook. |

## Routes

Start at [Runbook](RUNBOOK.md#get-oriented). Follow the smallest owner needed for the request.

| Need | Read |
|---|---|
| Scope and authority | [AGENTS](AGENTS.md) and the current owner request |
| Product purpose and first website loop | [Blueprint](BLUEPRINT.md) and [owner clarification](workbench/wiki/context-ams-purpose.md) |
| Shared vocabulary | [Glossary](GLOSSARY.md) |
| Implementation and acceptance | Assigned Spec and its Task records under workbench/specs/ |
| Durable knowledge | [Wiki router](workbench/wiki/MEMORY.md), then flat topic/feature/design-concept/guidebook articles |
| Decision rationale | ADR or DDR in workbench/decisions/, linked to the governing owner |
| Artifact selection and provenance | [Template inventory](workbench/research/template-inventory.md) and [research basis](workbench/research/template-research-basis.md) |
| Claim support | [Evidence audit](workbench/research/EVIDENCE-AUDIT-TEMPLATE.md) and its sources |
| Improvement hypothesis and disposition | [RSI record](workbench/research/IMPROVEMENT-TEMPLATE.md) |
| Repeatable outcomes | [Eval task](evals/EVAL-TASK-TEMPLATE.md), [result](evals/EVAL-RESULT-TEMPLATE.md), [comparison](evals/EVAL-COMPARISON-TEMPLATE.md) |
| Candidate review / actual human judgment | [Review receipt](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) / [Human QA receipt](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md) |
| Public explanation and demonstration | [Website page](site/PAGE-TEMPLATE.md) linked to safe evidence |
| Operations, checks and recovery | [Runbook](RUNBOOK.md) -> actual relevant skill/tool |

## Invariants and boundaries

- Requirements, state, evidence, explanation and authority have distinct jobs even when one artifact carries several claims. Governance roles are relative to the target and operation, not fixed by filenames.
- Maintain each claim in its owner and link consumers to it. Wiki and website explanations do not duplicate Task state or acceptance. The Taskboard displays state; it cannot establish it.
- Correct changing knowledge while preserving consequential reasons, evidence and correction history. Resolve disagreement by inspecting the applicable requirement and actual candidate, not a universal file precedence list.
- Personal skills retain their own lifecycle. A room-specific extension needs an authorized capability and actual validation; a host adapter changes discovery, not authority.
- A manifest declares, a receipt records, a template supplies a starting shape, and executing code produces behavior. None substitutes for proof of the others.
- A Spec owns capability intent and acceptance; Tasks own execution state and proof. Review and Human QA are recorded only when performed against identified content.
- The website explains and demonstrates maintained claims. Publish only safe evidence with appropriate authority; retain the difference between planned behavior, observed behavior and repeated outcomes.
- Flat Wiki articles grow through MEMORY.md. Create collections only when actual content warrants them. No additional registry, generator, manifest or lifecycle runtime is implied by these templates.
