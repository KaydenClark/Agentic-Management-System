# ADR Register

> Derived by `adr.mjs register`; do not edit by hand. The directory listing is the source; this table is a projection.

[Complete history](HISTORY.md). Only accepted active decisions follow.

| ADR | Title | Status | Date | Canonicalized in |
|---|---|---|---|---|
| [000A](000A-improvement-claims-need-held-out-ledger-evidence.md) | Improvement claims need held-out ledger evidence | accepted | 2026-11-01 | AGENTS.md, evals |
| [000B](000B-a-confirmed-grill-board-answer-goes-straight-to-its-owner.md) | A confirmed Grill Board answer goes straight to its owner | accepted | 2026-11-01 | grill-board |
| [000C](000C-the-authority-order-for-agents.md) | The authority order for agents | accepted | 2026-11-01 | AGENTS.md |
| [000D](000D-agents-md-is-the-only-always-loaded-instruction-file.md) | AGENTS.md is the only always-loaded instruction file | accepted | 2026-11-01 | AGENTS.md, CLAUDE.md |
| [000E](000E-an-always-loaded-line-must-change-the-next-action.md) | An always-loaded line must change the next action | accepted | 2026-11-01 | AGENTS.md, workbench/artifact-budgets.json |
| [000F](000F-agents-start-small-and-investigate-before-asking.md) | Agents start small and investigate before asking | accepted | 2026-11-01 | AGENTS.md |
| [000G](000G-a-rule-is-enforced-only-when-code-refuses-and-a-test-shows-it.md) | A rule is enforced only when code refuses and a test shows it | accepted | 2026-11-01 | AGENTS.md, tests |
| [000H](000H-a-check-never-blocks-its-own-repair.md) | A check never blocks its own repair | accepted | 2026-11-01 | AGENTS.md, workbench/tools |
| [000I](000I-a-required-step-must-produce-a-checkable-result.md) | A required step must produce a checkable result | accepted | 2026-11-01 | AGENTS.md, RUNBOOK.md |
| [000J](000J-check-a-host-before-relying-on-it.md) | Check a host before relying on it | accepted | 2026-11-01 | RUNBOOK.md |
| [000K](000K-a-stance-is-a-working-perspective-not-a-permission.md) | A stance is a working perspective, not a permission | accepted | 2026-11-01 | GLOSSARY.md, .agents/skills |
| [000L](000L-governance-planes-are-roles-a-claim-plays-in-one-operation.md) | Governance planes are roles a claim plays in one operation | accepted | 2026-11-01 | GLOSSARY.md |
| [000M](000M-a-directory-guide-holds-invariants-and-pointers-only.md) | A directory guide holds invariants and pointers only | accepted | 2026-11-01 | AGENTS.md |
| [000N](000N-one-decision-record-type-the-cdr.md) | One decision-record type, the CDR | accepted | 2026-11-01 | GLOSSARY.md, ARCHITECTURE.md |
| [000O](000O-cdrs-follow-standard-adr-practice.md) | CDRs follow standard ADR practice | accepted | 2026-11-01 | ARCHITECTURE.md |
| [000P](000P-a-capability-change-gets-one-short-spec.md) | A capability change gets one short Spec | accepted | 2026-11-01 | workbench/specs |
| [000Q](000Q-each-task-is-its-own-runnable-file.md) | Each Task is its own runnable file | accepted | 2026-11-01 | workbench/specs |
| [000R](000R-a-task-is-one-agent-run.md) | A Task is one agent run | accepted | 2026-11-01 | workbench/specs |
| [000S](000S-a-spec-is-accepted-against-its-conditions.md) | A Spec is accepted against its conditions | accepted | 2026-11-01 | workbench/specs |
| [000T](000T-scaffolding-is-deleted-at-close.md) | Scaffolding is deleted at close | accepted | 2026-11-01 | workbench/specs, ARCHITECTURE.md |
| [000U](000U-a-prototype-needs-no-spec.md) | A prototype needs no Spec | accepted | 2026-11-01 | workbench/specs |
| [000V](000V-the-taskboard-is-generated-and-shows-active-work.md) | The Taskboard is generated and shows active work | accepted | 2026-11-01 | TASKBOARD.md |
| [000W](000W-read-commands-use-the-same-words-for-every-kind.md) | Read commands use the same words for every kind | accepted | 2026-11-01 | RUNBOOK.md |
| [000X](000X-the-ams-runtime-is-a-small-python-cli.md) | The AMS runtime is a small Python CLI | accepted | 2026-11-01 | RUNBOOK.md, pyproject.toml |
| [000Y](000Y-one-manifest-names-every-path.md) | One manifest names every path | accepted | 2026-11-01 | workbench/manifest.json |
| [000Z](000Z-research-and-releases-have-their-own-folders.md) | Research and releases have their own folders | accepted | 2026-11-01 | ARCHITECTURE.md |
| [001A](001A-glossary-and-architecture-own-different-truths.md) | Glossary and Architecture own different truths | accepted | 2026-11-01 | GLOSSARY.md, ARCHITECTURE.md |
| [001B](001B-readme-orients-people-and-the-runbook-orients-agents.md) | README orients people and the Runbook orients agents | accepted | 2026-11-01 | README.md, RUNBOOK.md |
| [001C](001C-current-state-files-say-what-is-true-now.md) | Current-state files say what is true now | accepted | 2026-11-01 | ARCHITECTURE.md |
| [001D](001D-each-kind-of-truth-has-one-home.md) | Each kind of truth has one home | accepted | 2026-11-01 | ARCHITECTURE.md |
| [001E](001E-a-spec-needs-fresh-context-review-of-the-exact-commit.md) | A Spec needs fresh-context review of the exact commit | accepted | 2026-11-01 | AGENTS.md, workbench/specs |
| [001F](001F-no-pass-while-an-acceptance-line-lacks-evidence.md) | No pass while an acceptance line lacks evidence | accepted | 2026-11-01 | workbench/specs |
| [001G](001G-the-branch-policy-lives-in-one-config-file.md) | The branch policy lives in one config file | accepted | 2026-11-01 | workbench/manifest.json |
| [001H](001H-done-requires-a-pushed-read-back-commit.md) | Done requires a pushed, read-back commit | accepted | 2026-11-01 | AGENTS.md |
| [001I](001I-built-deployed-and-passing-claims-name-their-commit.md) | Built, deployed and passing claims name their commit | accepted | 2026-11-01 | AGENTS.md |
| [001J](001J-the-workflow-map.md) | The workflow map | accepted | 2026-11-01 | RUNBOOK.md, .agents/skills |
| [001K](001K-a-pr-merges-only-after-checks-on-the-combined-commit.md) | A PR merges only after checks on the combined commit | accepted | 2026-11-01 | AGENTS.md |
| [001L](001L-verify-runs-the-full-suite-on-one-commit.md) | Verify runs the full suite on one commit | accepted | 2026-11-01 | RUNBOOK.md |
| [001M](001M-a-claim-is-a-pushed-branch-and-a-draft-pr.md) | A claim is a pushed branch and a draft PR | accepted | 2026-11-01 | AGENTS.md, RUNBOOK.md |
| [001N](001N-the-wiki-is-a-small-linked-synthesis.md) | The Wiki is a small linked synthesis | accepted | 2026-11-01 | workbench/wiki |
| [001O](001O-links-and-grep-before-any-vector-index.md) | Links and grep before any vector index | accepted | 2026-11-01 | ARCHITECTURE.md |
