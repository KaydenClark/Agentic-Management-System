# AMS artifact template inventory

Complete local template set for AMS: Kayden's agents, workflows, intent capture, skills and tools in one RSI loop, beginning with a website that explains and demonstrates the system. [Blueprint](../../BLUEPRINT.md) owns product direction; [research basis](template-research-basis.md) records sources and limits.

## How to use the set

Choose the smallest artifact that serves the work. Copy a record template to its owning location and replace placeholders with sourced facts. Keep unknown and pending fields explicit. Templates do not create assignments, approvals, findings, results or publication authority. Link related records instead of duplicating their state.

Root controls are AMS-specific working documents with unresolved implementation fields; reusable record templates remain blank. The active application, website and evaluators are future work. There is no requirement to instantiate every template in every loop.

## Inherited formats and first-pass provenance

Initial source: LLM_Workbench `227d7c2a3ca009fc970900e9d18e4b72dc73c253`, read from Git objects. The source checkout's unrelated edits were not used. This table preserves the original extraction history; the tuning below supersedes its first-pass-only descriptions and “not invented” limits.

| AMS artifact | Established source path at the revision above | Changes |
|---|---|---|
| [AGENTS.md](../../AGENTS.md) | `templates/AGENTS.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [BLUEPRINT.md](../../BLUEPRINT.md) | `templates/BLUEPRINT.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [README.md](../../README.md) | `templates/README.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [ARCHITECTURE.md](../../ARCHITECTURE.md) | `templates/ARCHITECTURE.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [RUNBOOK.md](../../RUNBOOK.md) | `templates/RUNBOOK.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [TASKBOARD.md](../../TASKBOARD.md) | `templates/TASKBOARD.md` | Preserved source sections; replaced source-only routes/commands and branch assumptions with agreed paths or explicit unfilled fields. README retains folder orientation; Taskboard has empty data rows. |
| [GLOSSARY.md](../../GLOSSARY.md) | `templates/GLOSSARY.md` | Retained source glossary introduction and project-term template. Upstream filled vocabulary is not silently accepted as AMS definitions. |
| [workbench/specs/SPEC-TEMPLATE.md](../../workbench/specs/SPEC-TEMPLATE.md) | `templates/SPEC.md` | Omitted source migration/landmark instructions and legacy inline Task seed; used agreed separate Task path. No Spec was created. |
| [workbench/specs/TASK-TEMPLATE.md](../../workbench/specs/TASK-TEMPLATE.md) | `workbench/tools/task-record.mjs#formatTaskRecord` | Extracted established Spec-parent serializer fields; omitted optional former-ID/landmark fields, used agreed T-NNN folder naming, and left values unfilled. No parser or lifecycle implemented. |
| [workbench/decisions/ADR-TEMPLATE.md](../../workbench/decisions/ADR-TEMPLATE.md) | `workbench/tools/adr.mjs#adrTemplate` | Extracted verbatim generator shape with date/title placeholders; both record variants share the agreed decisions folder. No accepted decision created. |
| [workbench/decisions/DDR-TEMPLATE.md](../../workbench/decisions/DDR-TEMPLATE.md) | `workbench/tools/adr.mjs#ddrTemplate` | Extracted verbatim generator shape with date/title placeholders; both record variants share the agreed decisions folder. No accepted decision created. |
| [workbench/feedback/REPORT_FORMAT.md](../../workbench/feedback/REPORT_FORMAT.md) | `templates/feedback/REPORT_FORMAT.md` | Location and relative links only. |
| [workbench/feedback/WORKBENCH_FEEDBACK.md](../../workbench/feedback/WORKBENCH_FEEDBACK.md) | `templates/WORKBENCH_FEEDBACK.md` | Retained source sections and log columns; replaced producer/upstream routing with AMS-local feedback and left status choices unfilled. |
| [workbench/research/RESEARCH-TEMPLATE.md](RESEARCH-TEMPLATE.md) | `tools/new-research-project.mjs` | Extracted the established generated document shape; substituted title/question/date parameters only. |
| [workbench/research/NOTES-TEMPLATE.md](NOTES-TEMPLATE.md) | `tools/new-research-project.mjs` | Extracted the established generated document shape; substituted title/question/date parameters only. |
| [workbench/wiki/MEMORY.md](../../workbench/wiki/MEMORY.md) | `templates/wiki/MEMORY.project.md` | Retained project-router sections; removed routes to uncreated collections, schema/tool claims and prefilled upstream vocabulary. Used placeholder provenance/status rather than fictitious installation metadata. |
| [workbench/wiki/DESIGN-CONCEPT-TEMPLATE.md](../../workbench/wiki/DESIGN-CONCEPT-TEMPLATE.md) | `templates/wiki/design-concepts/README.md#Article Shape` | Extracted existing article shape. Kept templates flat; replaced unconfigured retired-Spec route and unverified metadata with placeholders. |
| [workbench/wiki/FEATURE-TEMPLATE.md](../../workbench/wiki/FEATURE-TEMPLATE.md) | `templates/wiki/features/README.md#Article Shape` | Extracted existing article shape. Kept templates flat; replaced unconfigured retired-Spec route and unverified metadata with placeholders. |
| [workbench/sessions/HANDOFF-TEMPLATE.md](../../workbench/sessions/HANDOFF-TEMPLATE.md) | `templates/HANDOFF.md` | Source body unchanged; template-only filename/location. |
| [workbench/sessions/notepad.schema.json](../../workbench/sessions/notepad.schema.json) | `templates/sessions/notepads/templates/notepad.schema.json` | Copied unchanged established structured-session format. No active note or session tool created. |
| [workbench/sessions/work.example.json](../../workbench/sessions/work.example.json) | `templates/sessions/notepads/templates/work.example.json` | Copied unchanged established structured-session format. No active note or session tool created. |
| [workbench/sessions/handoff.example.json](../../workbench/sessions/handoff.example.json) | `templates/sessions/notepads/templates/handoff.example.json` | Copied unchanged established structured-session format. No active note or session tool created. |
| [workbench/sessions/grilling.example.json](../../workbench/sessions/grilling.example.json) | `templates/sessions/notepads/templates/grilling.example.json` | Copied unchanged established structured-session format. No active note or session tool created. |

## AMS tuning of inherited artifacts

| Artifact group | Current adaptation |
|---|---|
| AGENTS / RUNBOOK | Concrete scope, evidence, template-selection and RSI routes; missing runtime and publication policy stated explicitly. Personal skills retain independent ownership. |
| BLUEPRINT / README / GLOSSARY | Owner-supplied AMS purpose and first website loop; record distinctions and feedback dispositions; unimplemented setup remains explicit. |
| ARCHITECTURE / TASKBOARD | Maintained-owner routes, flat Wiki and new evidence routes; Taskboard remains a projection with no fabricated generator. |
| Spec / Task | Intent/source and authorized endpoint, observed outcome, RSI/website links, candidate proof and separate review/Human QA. |
| ADR / DDR | Explicit decision status/source because no lifecycle tool exists; target and evidence without invented acceptance. |
| Feedback / research | Defined dispositions, source registers, research limits, supported implications and RSI follow-through. |
| Wiki router / feature / design concept | Flat routes, current sourced context, correction history and intended-versus-observed limits. |
| Handoff | Current scope, confirmed state and continuation of unfinished RSI work. |
| Legacy notepad schema and three JSON examples | Preserved byte-for-byte for compatibility; no new runtime or active note. |

## Added AMS formats

These are AMS-authored adaptations grounded in the research basis, not falsely attributed upstream templates.

| Template | Use and filled-record location |
|---|---|
| [Evidence audit](EVIDENCE-AUDIT-TEMPLATE.md) | Maintain a claim/evidence assessment and its history in workbench/research/. |
| [Improvement record](IMPROVEMENT-TEMPLATE.md) | Connect friction, hypothesis, trial comparison, actual disposition and later use in workbench/research/. |
| [Eval task](../../evals/EVAL-TASK-TEMPLATE.md) | Define versioned cases under evals/; separate from implementation Tasks. |
| [Eval result](../../evals/EVAL-RESULT-TEMPLATE.md) | Record each attempt under evals/ with exact candidate and evidence. |
| [Eval comparison](../../evals/EVAL-COMPARISON-TEMPLATE.md) | Assess comparable runs under evals/, preserving failures and uncertainty. |
| [Wiki note](../wiki/NOTE-TEMPLATE.md) | Flat source-linked topic in workbench/wiki/; captures intent with status and corrections. |
| [Wiki guidebook](../wiki/GUIDEBOOK-TEMPLATE.md) | Flat extended procedure/explanation linked from the Runbook when applicable. |
| [Wiki comparison](../wiki/COMPARISON-TEMPLATE.md) | Flat qualitative comparison; measured trials remain in evals/. |
| [Review receipt](../specs/REVIEW-RECEIPT-TEMPLATE.md) | Candidate-bound assessment in the owning Spec's evidence location. |
| [Human QA receipt](../specs/HUMAN-QA-RECEIPT-TEMPLATE.md) | Actual human experience/judgment in the owning Spec's evidence location. |
| [Website page](../../site/PAGE-TEMPLATE.md) | Explanation, claim/evidence mapping and demo design under site/. |
| [Skill skeleton](SKILL-TEMPLATE.md) | Inactive authoring reference; only a validated, authorized capability becomes .agents/skills/<name>/SKILL.md. |

## Related maintained context

- [AMS purpose](../wiki/context-ams-purpose.md): direct owner clarification and assignment boundary.
- [Research basis](template-research-basis.md): pinned sources, rationale, coverage limits and source hashes.

## Remaining choices and limits

LICENSE stays unfilled until the owner selects it. CLAUDE.md and its discovery symlink retain their established forms. Application stack, tests, website implementation, Vercel/Supabase configuration, Grilling Board implementation, branch/merge policy and deployment remain unconfigured. No code, secrets or deployment configuration is invented to fill those choices.

Actual sessions, recovery, .local and .worktrees remain ignored. No evaluation run, actual review verdict or Human QA acceptance was created. This template work is local; publication and deployment are separate endpoints.

## History

- Initial inventory: copied/extracted established source formats; named five unresolved artifact families and deferred skill authoring.
- 2026-10-31: owner explicitly requested complete AMS-tuned templates; added the missing families plus qualitative Wiki comparison, website page and inactive skill skeleton. Preserved inherited provenance and legacy session compatibility.
