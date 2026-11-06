---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, owner instruction approved 2026-11-01, relayed by the AMS foundation coordinator
  - setup-workbench v3.2.2 Adoption run, 2026-11-01
source_paths:
  - workbench/manifest.json
  - workbench/tools/.workbench-tools.json
  - workbench/research/template-inventory.md
last_verified: 2026-11-02
---

# Workbench adoption

Owner approved setup-workbench Adopt on 2026-11-01. The [original record](https://github.com/KaydenClark/Agentic-Management-System/blob/b7efbaba15baa354eafbc92b91a352ae54d94c71/workbench/wiki/context-workbench-adoption.md) retains original details and verification.

The scaffold lacked a manifest, stamp and tools. Adoption used setup-workbench v3.2.2 SHA-256 `99080edd8e061ba6b1b142e27088338914b591cee27a7c5725383d405af7ceb2`, lineage `9d5e1f25b0d5`; Node 26.3.0 and Git 2.54.0. Recovery: published main `49d4999`; rollback: ignored `workbench/sessions/recovery/adoption-recovery.json`. Manifest default/integration: main; no dev deploy field.

Controls and ignore rules were folded; glossary feedback terms and notepad examples ported; old ADR/DDR and Wiki templates archived; current templates and commit hook kept. Pre-adoption architecture remains at `49d4999`. Original checks: stable render, no blocking doctor, null next, valid layout/tools/skills, clean whitespace; disposable Jot/claim/close/refusals. No current host-activation proof.

Open gaps: Spec Adoption evidence owed; doctor permission-scope drift; ten template lines dropped/six changed (personal-skill-first, carry, claim, pre-edit readback, Task review, closeout), fidelity unproved. Old Task template: `T-NNN`; tools: `TK-###`; run/journey/measure bracketed. Receipt matches 41 managed files; its source SHA `95d3c0c1cb98a0d1746fab9278a70bc719d9ea2af115bd38eac45db46c7d2f77` differs from the package SHA above; 11 hashes differ. Authorized update `0b58148359ae43ec9c15300414b4230c9dcc9b5a` added spec-history. Sessions explicitly loaded orchestrate/carry/journey/plan/jot; automatic discovery and other hosts unverified.

## Pinned recovery inventory — 2026-11-02

Scope: [capability overview](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/wiki/workbench-capabilities.md) at `9d5e1f25b0d5870589ae1c5752f27f42acb796ef`: linked setup, map/plan, Wiki, review, Dashboard, core operations, reusable skills, producer utilities, retained-capture indices; `features/README.md`; ADR/DDR `REGISTER.md`/`HISTORY.md`, including ADR page 001. The 51 captures, 52 operations, 33 core skills, seven maintainers and 18 utilities overlap, not 161 distinct features. The core article lists 23; the pinned manifest supplies 33 required names. Later snapshots `d4ff0fbc`/`afc68e62` prove no runtime/AMS parity at the pin. Decision directories are canonical; registers/history project them. No code audit.

**Reading the matrix:** Rows identify legacy items, owner, disposition and evidence limits. “Adapted” means a related principle, not equivalence. S-001 must compare every “Unknown” source/owner/behavior before retain/adapt/missing decisions; absence does not mean retirement. Proposed/superseded/deprecated history is not canon.

### Feature captures: 51 named positions

At AMS `b7efbaba15baa354eafbc92b91a352ae54d94c71`, `git ls-tree -r --name-only workbench/wiki/features` returned no files despite its declared collection. Disposition: **capture layer unported**, not absent/retired behavior. S-001 and each Spec/Wiki/SKILLS/manifest/receipt/control/executable owner must classify each item against evidence; untested parity is unknown. Pinned retained-capture names:

adoption-preflight-and-legacy-classification; adoption-when-git-writes-are-unavailable; assigned-work-portable-stances-and-delivery-boundaries; assignment-ownership-and-coordination-records; blueprint-active-adrs-and-the-context-map; bounded-team-coordination; canonical-evaluator-invocation; checkpoint-retirement-and-direct-promotion; configured-host-capabilities; consistent-bootstrap-ownership-guidance; control-fidelity-without-forced-uniformity; copyable-workbench-template-reference-room; core-skill-ownership-and-compatibility; declared-integration-and-recoverable-completion; dependency-safe-direct-claiming; diagnostics-ordered-by-consequence; evidence-bounded-upgrade-claims; evidence-gated-harness-feedback; feedback-and-migration-integrity; fresh-template-to-independent-project-proof; genesis-from-blueprint-decisions-and-active-adrs; governance-planes-adr-decisions-and-scoped-diagnostics; held-out-path-safety-evaluation; historical-v3-1-release-proof-packet; import-safe-feedback-helper-entry; installed-runtime-integrity; installed-skill-identity-and-inspection; installed-state-reporting-and-repair; json-notepad-foundation; lexicon-freshness-repair; line-ending-aware-records; linked-follow-up-reconciliation; manifest-schema-2-lanes-and-managed-runtime; mechanical-permission-scope-and-declared-lanes; named-template-upgrade-release-gate; operable-genesis-readiness; portable-verification-boundaries; portable-wiki-knowledge-and-collections; portable-workbench-installation-adoption-and-upgrade; project-evidence-preparation-for-blueprint-grilling; recorded-baseline-availability; release-candidate-proof-and-historical-disposition; reproducible-adoption-provenance; skill-presence-and-repair-routes; source-checked-finding-disposition; spec-centered-progressive-disclosure; upgrade-layout-without-replacing-skills; verified-automation-run-outcomes; visible-workbench-identifiers; wiki-routing-version-stamps-and-safe-source-reads; workflow-composition-and-cold-continuation.

### Operation families: 52 named positions

| Legacy catalog rows | Owner; disposition/evidence |
|---|---|
| Evidence preparation for Blueprint questions; Architecture and destination decision records; Destination Question Cards and Tracker projections; LANDMARK.md delivery artifacts; Landmark article checking; Exact-commit GitHub coordination inspection | Blueprint, ADR/DDR and Landmark/Spec records adapt destination and hierarchy; documented by current controls. Question Cards/Tracker and article/coordination checker equivalence **unknown**: S-001 inspects CLI/tests. |
| Manifest and room initialization; Room identity, source receipts and legibility; Lifecycle classification, adoption and upgrade; Managed runtime and room skill lanes; Control fidelity and permission-scope checks; Host minimum and optional Task requirements; Configured-host probes; Glossary, Architecture and explanatory dictionary; Preservation-aware Lexicon migration; Shared startup continuation; Maintained workflow reference; Cross-platform managed line endings | Manifest, receipt, setup-workbench, controls and SKILLS **adapted** identity and routing; Receipt proves bytes, not activation. Probes, upgrade and line endings **unknown**; S-001/setup test. |
| Standalone Task packets and receipts; Safe work selection and claims; Typed identifiers and supported widening; Scoped diagnostics and gate checks; Current hot Taskboard and retained Spec catalog; Six-lane JSON board preview; Lane Sweep; Map count evidence; Claimant-attributed Task closure | Spec/Task, TASKBOARD and `spec-workbench.mjs` **adapted** hierarchy/claim/close. Widening, preview, sweep and map-count **unknown**; S-001 compares CLI/tests. |
| Wiki validation, repair and safe moves; Feature capture and synthesis maintenance; JSON objective notepads; Direct promotion, scans and frozen checkpoint history; Optional private session transport; Draft skill Wiki prototype; Wiki Jot capture and focused retrieval; Legacy note continuity without unintended exposure | Wiki, sessions, jot and reconcile **adapted** knowledge and local handoffs. Captures unported; notepad, checkpoint, transport and prototype **unknown**, S-001/Wiki inspect. |
| Assembled Spec or landmark reports; Candidate-bound review and corrective return; Owner approval and verified completion; Reference-safe record moves and reparenting; Capture, retirement and bounded discard; Confirmed readback fidelity; Checked acceptance evidence gate; Observed integration landing and continuation | AGENTS, RUNBOOK, SKILLS and Spec/Task records **adapted** approval, review, QA and delivery; merge is not acceptance. Report/move/discard/landing **unknown**, S-001 compares. |
| Five-section local Workbench Dashboard; Focused draft review and exact confirmation; Answer metadata, concurrency and historical fidelity; Owner round feedback and promotion hand-back; Board maintenance and durable decision application; Optional receipt-backed project Grill Board; Named local Board entry; Optional macOS Dashboard login service; Review-presentation experiment feedback | S-004/S-005 own local Board; S-003/S-008 own presentation. Surfaces **adapted**; Dashboard, service, metadata and concurrency parity **unknown**, S-001/Specs assess. Website is not private review proof. |

### Skills and producer tools

| Legacy entries | Owner; disposition/evidence |
|---|---|
| Core same-name: carry, code-review, grilling, orchestrate, jot, domain-modeling, pr | Manifest and SKILLS **required/routed**. Names prove neither bytes nor activation. |
| Core successors: implement → journey; to-spec → map; to-tasks → plan; reconciler → reconcile; improve-harness → improve-workbench; auditor → audit-workbench | SKILLS **adapted routing**; method parity and host activation **unknown**, S-001 to compare actual methods and host runs. setup-workbench and author-skill are current policy additions. |
| Remaining core: adoption, checkpoint, genesis, to-docs, tracer-bullet, update-harness, notepad, save, promote, handoff, grill-me, workbench-runtime, writing-for-agents, retro, director, dispatcher, spec-planner, spec-manager, builder, reviewer | SKILLS and S-001: **unmapped/unknown** in required routing, not retired. Compare each operation and evidence. `writing-for-agents` was explicitly loaded this run; optional presence/use does not make it a required room skill. |
| Maintainers: workbench-release, workbench-room-checks, workbench-evaluation, implement-spec, promote-decision, readback, grill-with-docs | Not required room skills; **parity unknown**, not retired. S-001 compares setup/author/evaluate/audit/journey/carry. |
| Utilities: Static workbench scoring; Guardrail audit; Controlled outcome trials and held-out evaluation; Feedback discovery and automated disposition; Self-drift receipts; Carrier line landing and append-only history; Composed lifecycle and portability proof; Derive a fresh independent room; Bounded optional team run; Context prompt packing; Research folder scaffolding; Optional Foundry socket contracts; Personal skill catalog publication; One parallel verification command; Clean immutable-candidate verification; Conservative change-aware hosted CI; Staged-byte pre-commit checks; Validated Task PR merge train | S-001/S-002/S-006/S-012/S-013, evals, feedback, CI and personal methods own candidates. Behavior **unknown** without proof; S-001 assigns capability owners; producer status is not retirement. |

### Decision ledger

Pinned history indexes list 82 ADRs (64 accepted, six superseded, 12 proposed) and 57 DDRs (49 accepted, three superseded, one deprecated, four proposed). AMS projections differ; do not inherit legacy totals. Owners: A=[AGENTS](../../AGENTS.md), B=[Blueprint](../../BLUEPRINT.md), R=[Runbook](../../RUNBOOK.md), C=[Architecture](../../ARCHITECTURE.md), G=[Glossary](../../GLOSSARY.md), K=[SKILLS](../docs/SKILLS.md), W=[Wiki](MEMORY.md). Adapted rows cite documentary controls; S-001 compares source records and implementation. IDs belong to pinned collections.

| Legacy ADR IDs and subject | Owner; disposition/evidence |
|---|---|
| 000F, 001N, 0039 branch/candidate | A/K: **adapted** checked branch routes; not acceptance or deployment. |
| 000G, 000H, 000N, 000U hierarchy | B/C/G/A: **adapted** destination, owner and Task structure. |
| 000J, 0020, 0023, 0034, 0035, 0036, 0044 evidence/judgment | A/R/C/B: **adapted** distinct evidence, Review and Human QA. |
| 000R, 0018, 0043, 0054 continuity/knowledge | C/W/A: **adapted** Wiki and record routes. |
| 001B, 001F, 001M, 0045, 0046 skill ownership | K/A: **adapted** personal source and managed tools. |
| 0028, 0051 local continuity; 0031, 0052 managed runtime | A/R/W and K/R: **adapted** local boundaries and receipt; private transport/runtime parity **unknown**. |
| 0001, 0003, 0005, 000A–000D, 000I, 000K, 000L, 000O, 000P, 000S, 000T, 000V, 000W, 000X, 000Y, 000Z, 0015, 001O, 0026, 0027, 0029, 0030, 0032, 0037, 0038, 0040–0042, 0047, 0048, 0049, 0050, 0053, 0055 | **Unknown**; S-001 compares source/owner/proof. Ranges are consecutive. |
| Superseded 0002, 000M, 0013, 0017, 0025, 0033; proposed 000E, 000Q, 001A, 001C, 001D, 001E, 001G, 001H, 001I, 001J, 001K, 001L | **Historical/proposed**, not canon; S-001 checks successors. |

| Legacy DDR IDs and subject | Owner; disposition/evidence |
|---|---|
| 000A recursive destination | B: **adapted** destination; recursive behavior unproved. |
| 000B, 000C, 000O, 002D, 002E owner scope | B/A/C: **adapted** owner and destination. |
| 000F, 000G, 000K, 001A, 001E, 001N, 001X continuity/ownership | A/R/C/G/W: **adapted** routes. |
| 001M Wiki history | W: **adapted** history route; adoption evidence row remains owed. |
| 000R, 000S, 001K source rights/setup | B/K/A: **adapted** setup and source policy. |
| 001B, 002B, 002C Task/review/branch | A/C/G/K: **adapted** bounded execution and distinct review. |
| 000T system identity | B/G: **adapted**; pinned DDR 000T and [owner correction](context-owner-answers-coherence.md#jot-aba91085-29c1-4777-88a7-e8bc1da63060) support current Glossary meaning, not workflow proof. |
| 000D, 000E, 000H–000J, 000L–000N, 000P, 000U–000Z, 001C, 001G–001J, 001L, 001O–001Q, 001T–001W | **Unknown**; S-001 compares source/owner/proof. |
| Superseded 000Q, 001D, 001R; deprecated 001F; proposed 001S, 001Y, 001Z, 002A | **Historical/proposed**, not canon; S-001 checks successors. |

No row proves equivalence, learning, Review or acceptance. TK-001X owns accounting; S-001 owns unresolved capability comparisons.

## Later owner correction

<!-- jot-entry -->
### JOT-9abd9e46-08ae-4283-a950-a96e6095759f
Kind: intent
State: current
Recorded: 2026-11-03T19:41:00.470Z
Author: Kayden
Source: Kayden, AMS chat, 2026-11-03
Topic: workbench-adoption
Supersedes: none

Owner correction: AGENTS.md still contains material that belongs elsewhere, specifically the three-strike rule. Authorized repair: keep core authority, safety and collaboration rules in AGENTS; route testing, CI, scheduling, RSI and delivery procedures to their existing owning documents. Relocation preserves the existing policies; this request does not retire the three-strike stop or authorize deployment.
<!-- /jot-entry -->
