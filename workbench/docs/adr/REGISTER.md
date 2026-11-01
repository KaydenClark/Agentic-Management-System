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
| [001P](001P-continuity-is-proven-by-a-fresh-recipient-trial.md) | Continuity is proven by a fresh-recipient trial | accepted | 2026-11-01 | AGENTS.md, evals |
| [001Q](001Q-temporary-notes-are-reconciled-and-deleted.md) | Temporary notes are reconciled and deleted | accepted | 2026-11-01 | AGENTS.md |
| [001R](001R-a-handoff-is-a-short-live-file.md) | A handoff is a short live file | accepted | 2026-11-01 | RUNBOOK.md |
| [001S](001S-everything-a-session-needs-is-committed.md) | Everything a session needs is committed | accepted | 2026-11-01 | AGENTS.md, .agents/skills |
| [001T](001T-size-tasks-to-one-session-and-record-tokens.md) | Size Tasks to one session and record tokens | accepted | 2026-11-01 | workbench/specs, supabase |
| [001U](001U-capture-a-decision-before-the-output-that-depends-on-it.md) | Capture a decision before the output that depends on it | accepted | 2026-11-01 | AGENTS.md |
| [001V](001V-the-layout-is-judged-by-a-cold-start-eval.md) | The layout is judged by a cold-start eval | accepted | 2026-11-01 | evals |
| [001W](001W-the-owner-s-orchestration-model-is-the-default.md) | The owner's orchestration model is the default | accepted | 2026-11-01 | AGENTS.md, RUNBOOK.md |
| [001X](001X-room-skills-live-beside-the-owner-s-personal-skills.md) | Room skills live beside the owner's personal skills | accepted | 2026-11-01 | .agents/skills |
| [001Y](001Y-each-behavior-has-one-owning-skill.md) | Each behavior has one owning skill | accepted | 2026-11-01 | .agents/skills |
| [001Z](001Z-cross-skill-calls-are-explicit-skill-tool-calls.md) | Cross-skill calls are explicit Skill-tool calls | accepted | 2026-11-01 | .agents/skills |
| [002A](002A-one-improvement-procedure-starting-from-failed-results.md) | One improvement procedure, starting from failed results | accepted | 2026-11-01 | evals, workbench/feedback |
| [002B](002B-a-repeated-failure-first-checks-the-earlier-fix.md) | A repeated failure first checks the earlier fix | accepted | 2026-11-01 | evals, workbench/tools |
| [002C](002C-reports-say-what-happened.md) | Reports say what happened | accepted | 2026-11-01 | AGENTS.md |
| [002D](002D-every-finding-has-one-disposition.md) | Every finding has one disposition | accepted | 2026-11-01 | workbench/feedback |
| [002E](002E-runbook-commands-are-the-commands-graders-call.md) | Runbook commands are the commands graders call | accepted | 2026-11-01 | RUNBOOK.md, evals |
| [002G](002G-measure-the-noise-floor-before-trusting-a-change.md) | Measure the noise floor before trusting a change | accepted | 2026-11-01 | evals |
| [002H](002H-every-round-runs-two-control-arms.md) | Every round runs two control arms | accepted | 2026-11-01 | evals |
| [002I](002I-comparisons-use-paired-per-task-statistics.md) | Comparisons use paired per-task statistics | accepted | 2026-11-01 | evals |
| [002J](002J-every-ledger-row-records-cost-and-run-state.md) | Every ledger row records cost and run state | accepted | 2026-11-01 | evals, supabase |
| [002K](002K-graders-come-from-the-accepted-version.md) | Graders come from the accepted version | accepted | 2026-11-01 | evals |
| [002L](002L-trials-run-in-a-sandbox.md) | Trials run in a sandbox | accepted | 2026-11-01 | evals |
| [002M](002M-more-than-two-held-out-tasks-before-a-public-number.md) | More than two held-out tasks before a public number | accepted | 2026-11-01 | evals, site |
| [002N](002N-studied-held-out-tasks-retire-to-the-dev-set.md) | Studied held-out tasks retire to the dev set | accepted | 2026-11-01 | evals |
| [002P](002P-no-session-holds-untrusted-input-secrets-and-outward-actions-together.md) | No session holds untrusted input, secrets and outward actions together | accepted | 2026-11-01 | AGENTS.md |
| [002Q](002Q-the-workbench-folder-stays-visible.md) | The workbench folder stays visible | accepted | 2026-11-01 | ARCHITECTURE.md |
| [002R](002R-each-rsi-run-pins-the-skills-commit.md) | Each RSI run pins the skills commit | accepted | 2026-11-01 | evals, .agents/skills |
| [002S](002S-at-most-six-active-specs.md) | At most six active Specs | accepted | 2026-11-01 | workbench/specs |
| [002T](002T-measure-how-far-dev-runs-ahead-of-main.md) | Measure how far dev runs ahead of main | accepted | 2026-11-01 | RUNBOOK.md |
| [002U](002U-writes-to-shared-stores-refuse-on-conflict.md) | Writes to shared stores refuse on conflict | accepted | 2026-11-01 | supabase, grill-board |
| [002V](002V-artifacts-have-character-limits.md) | Artifacts have character limits | accepted | 2026-11-01 | workbench/artifact-budgets.json |
| [002W](002W-three-strikes-then-stop.md) | Three strikes, then stop | accepted | 2026-11-01 | AGENTS.md |
| [002X](002X-next-js-front-end-python-backends-node-only-as-tooling.md) | Next.js front end, Python backends, Node only as tooling | accepted | 2026-11-01 | ARCHITECTURE.md, site, pyproject.toml |
| [002Y](002Y-supabase-holds-the-rsi-data-and-a-python-writer-keeps-it-current.md) | Supabase holds the RSI data and a Python writer keeps it current | accepted | 2026-11-01 | supabase |
| [002Z](002Z-three-orchestrators-split-the-work-by-risk.md) | Three orchestrators split the work by risk | accepted | 2026-11-01 | AGENTS.md, RUNBOOK.md |
| [003A](003A-implementors-run-on-opus-or-sonnet.md) | Implementors run on Opus or Sonnet | accepted | 2026-11-01 | AGENTS.md |
| [003B](003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md) | The dev site is visible only to the owner, Claude and Codex | accepted | 2026-11-01 | site |
| [003C](003C-the-supabase-project-and-its-read-only-baseline.md) | The Supabase project and its read-only baseline | accepted | 2026-11-01 | supabase |
| [003D](003D-python-3-14-5-pinned-with-uv.md) | Python 3.14.5 pinned with uv | accepted | 2026-11-01 | .python-version, pyproject.toml |
| [003E](003E-the-adr-and-ddr-collections-are-the-cdr-s-two-kinds.md) | The adr and ddr collections are the CDR's two kinds | accepted | 2026-11-01 | ARCHITECTURE.md, workbench/manifest.json |
| [003F](003F-one-standing-campaign-approval-and-no-per-merge-gate.md) | One standing campaign approval and no per-merge gate | accepted | 2026-11-01 | evals, grill-board |
| [003G](003G-the-rsi-loop-design-with-one-owner-gate.md) | The RSI loop design with one owner gate | accepted | 2026-11-01 | evals, supabase |
| [003H](003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md) | Supabase holds the RSI data and the service key stays local | accepted | 2026-11-01 | supabase |
