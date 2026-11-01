# AMS template research basis

## Scope and authority

Kayden's 2026-10-31 instruction authorizes the AMS-tuned template set and supplies the product intent preserved in [the context note](../wiki/context-ams-purpose.md) and [Blueprint](../../BLUEPRINT.md). The first RSI loop builds a website explaining and demonstrating AMS while real work informs Workbench repair and the system above it.

Research informs template design; historical instructions and proposed experiments do not become current authority by being cited. These are document formats, not a runner contract or measured improvement.

## Inspected research

AI_Research_Notes was read from the existing local checkout at commit `10b552f9d0cded150e584d7282421e745d0d353c`; the listed tracked files had no working-tree modifications. The unrelated untracked redesign document was not used. References below identify the owning repository and exact revision; access remains subject to that repository's permissions. No private raw transcripts were copied into AMS or the website.

| Source at inspected revision | Application to AMS templates | Read/evidence limit |
|---|---|---|
| [evaluating-llm-and-agent-changes.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/evaluating-llm-and-agent-changes.md) | Task/trial/grader distinctions, controlled repetitions, outcome grading, calibration, denominators and uncertainty. | Complete page; proposed minimal experiment is not adopted as a fixed sample-size rule. |
| [accountability-and-feedback.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/accountability-and-feedback.md) | Separate finding review, repair delivery and later-use benefit; record owner effort and recurrence. | Complete page; historical reports were not rerun. |
| [governance-stack.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/governance-stack.md) | Claim-relative roles, maintained owners, current authority versus historical context, and proportionate process. | Selected claim-role, authority, enforcement and limitations sections; historical lifecycle disagreements remain unresolved by this pass. |
| [ui-and-prototype-evidence.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/ui-and-prototype-evidence.md) | Visitor understanding, actual interactions, visible feedback and bounded screenshot/QA claims. | Complete page; historical UI observations not reproduced. |
| [knowledge-and-navigation.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/knowledge-and-navigation.md) | Flat routed knowledge, source-linked explanation, correction history and maintained owners. | Opening sections on access/navigation; no retrieval outcome measurement. |
| [skills-redesign-research.md](https://github.com/KaydenClark/AI_Research_Notes/blob/10b552f9d0cded150e584d7282421e745d0d353c/wiki/skills-redesign-research.md) | Controlled baseline/no-skill comparisons, full loaded-context cost and preservation of unadopted proposals. | Evidence, limits and baseline recommendations; no adoption of skill counts, gate counts or branch policy. |

The research pages cite their own primary sources and retain their coverage limits. This pass used the research notes as supplied evidence; it did not independently re-read external papers or rerun historical experiments. Numerical sample-size suggestions and old model results are not AMS guarantees.

## Workbench and authoring sources

- Inherited formats: LLM_Workbench `227d7c2a3ca009fc970900e9d18e4b72dc73c253`; exact original paths remain in the [inventory](template-inventory.md).
- Current GPT_OS instructions supplied by Kayden: scope, preservation, source-backed claims, useful verification and distinct delivery/acceptance states.
- Loaded GPT_OS `workbench/skills/writing-for-agents/SKILL.md` and `workbench/skills/to-docs/SKILL.md`: progressive disclosure, observable completion and maintained information owners.
- Loaded personal `jot/SKILL.md` and its Workbench reference: preserve source, speaker, correction, confirmation state and actual authorization.
- Loaded personal `author-skill/SKILL.md` and method/validation references: informs the inactive skill skeleton. A real capability still needs that authoring and separate-pruning workflow; none is authored or installed by this skeleton.

## Traceability

| Artifact family | Research/standard carried into the shape |
|---|---|
| Controls, Spec, Task, decisions | Product intent in Blueprint; scope and actual authority; one maintained owner; sourced decisions and evidence. |
| Evidence audit and feedback | Dated claim/evidence comparison, evidence availability separate from outcome, preserved reassessments, repair versus benefit. |
| RSI improvement | Real friction, causal hypothesis, baseline, controlled experiment, actual disposition, recurrence and next useful work. |
| Eval task/result/comparison | Frozen rubric, clean-state repetitions, model/host/skill identity, trace analysis, all attempts, comparability and uncertainty. |
| Wiki and research | Source-linked synthesis, claim status, read boundary, contradictory evidence and correction history. |
| Review and Human QA | Candidate-bound judgments, real reviewer involvement, actual human response and separate delivery authorization. |
| Website page | Useful explanation and exercised interactions, honest planned/observed states, safe public evidence and bounded claims. |
| Skill skeleton and handoff | Reuse personal ownership, concrete input/output and failure paths, truthful continuation and future behavioral validation. |

## Source fingerprints

SHA-256 identifies the bytes consulted even if a source later changes. Hashing is identity evidence, not behavioral validation.

| Local source | SHA-256 |
|---|---|
| AI_Research_Notes/wiki/evaluating-llm-and-agent-changes.md | `670be38eeaaa0c980bad499cfdb3af300ee238123675cc848622f1a91f65d62e` |
| AI_Research_Notes/wiki/accountability-and-feedback.md | `f052cb4ff02c94ceed998b15dbbe0434fd71d363541a912ade5e729487318ece` |
| AI_Research_Notes/wiki/governance-stack.md | `f952f5ea0c0c34cf644a06c79b9deddbdb772420e4dc0fcb6c1f2056d08ce623` |
| AI_Research_Notes/wiki/ui-and-prototype-evidence.md | `a2802ec85578a1699dcfc24c0dff54006147ed8fa3ebe384a063ad6dbf9421d5` |
| AI_Research_Notes/wiki/knowledge-and-navigation.md | `8368a8fd0531b55f73ed9cfc5e1eea861cc359204153d9ca4185969cce6368b0` |
| AI_Research_Notes/wiki/skills-redesign-research.md | `e6fff240b2e40c7be76ba7aa62d3cd06edc24325a0b25a45505202f6087bb438` |

## Verification limits

The AMS application suite, eval runner, generator, Wiki validator and deployment procedure are not installed. Template validation checks document structure, traceability, local routes, JSON compatibility and diff hygiene; it cannot prove agent outcomes or website behavior. Existing legacy JSON examples are preserved unchanged rather than presented as a new AMS runtime schema.

## Template verification — 2026-10-31

- Checked 35 Markdown files, 150 local links/anchors and the 15,000-character artifact budget; no failures after repairing the Wiki route and shortening Architecture.
- Parsed all four retained session JSON files; confirmed the schema and all three examples match the pre-edit bytes. A JSON Schema validator was unavailable, so no schema-validation pass is claimed.
- Confirmed CLAUDE.md and .gitignore match the pre-edit bytes. Existing unrelated work was preserved; the Git diff includes earlier edits and is not a clean-baseline measure of this pass alone.
- Checked diff whitespace and manually traced artifact routes for an unsupported website claim, an interrupted evaluation, a proposed improvement awaiting disposition, a changed review candidate and an absent human response. Each has a place to retain its limitation without recording a pass or approval. This is a document walkthrough, not an executed agent trial.
- No application suite, website/browser checks, independent review, Human QA or RSI trials ran. The templates support those future operations; they do not establish their results.
