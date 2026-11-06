# TK-002 - Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden

**Task ID:** TK-002
**Spec ID:** S-007
**Slice:** Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Every number links; Provenance and series; Not only up; No test rows
**Planned verification:** link-coverage, model-change, regression and test-row render tests

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** ams-records-site
**Current claimant:** ams-records-site

Read `AGENTS.md`, the S-006 Spec (`workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md`) and its result and run tables under `supabase/migrations/` on `origin/main`, and the chart route on `origin/dev`.

Deliver: the page reads result rows with the publishable key and renders them per task and per version, with provider, model, effort and system version on each series. A model change starts a new series. Regressions, variants, removed versions and fired stop rules are marked. Every number links to the rows behind it and shows each row's strength label. Test rows never render. Render tests use labeled fixtures for each case.

Out of scope: headlines (TK-003); statistics computed differently from the loop's.

Hand back to S-007 with `close`.

## Acceptance

- [x] A link-coverage test fails on any rendered number without a row link.
- [x] A model-change fixture renders two series, never one line.
- [x] A regression fixture shows the regression marked as such.
- [x] A marked test row in the fixture never renders.
- [ ] Build and tests pass; the `dev` deployment reads live rows or shows the empty state.

## Dependency readback and resumed assignment

The S-006 input is its delivered `rsi_runs`/`rsi_results` migration and public writer/source contract, available on main at `b059a6a08db8876e17c426764f8e6acbbca0632c`; whole-Spec acceptance is not a content dependency (ADR-003J). TK-001 is done. The owner-authorized shared-skill RSI display and coordinating assignment resume this unclaimed retained reader branch. One writer: AMS records/site implementor. Preserve earlier source history; incorporate current dev and finish the existing reader rather than introduce a competing architecture.

Add the safe published S-011 development evidence separately from behavioral trial rows: actual predicate counts and documentation failures with source links; candidate audit, installation/use and benefit remain pending. No private packets, skill text, fabricated score or dev-to-main promotion.

## Local verification and remaining gate

Retained reader fixtures passed14 tests before repair. Red/green checks then exposed and repaired failed reads claiming emptiness, null metrics becoming partial totals, malformed rows appearing empty, and absent successful-read timestamps. Safe evidence render tests cover baseline/candidate predicates, separate incomplete audits, retained provisional tallies, goal misses and private-source exclusion. A built-site suite passed203 tests before the latest trace totals; current focused reader/evidence checks pass21. Full build/suite and exact-head CI will be rerun for delivery.

Phone browser inspection found the new full commit link overflowed (scroll width423 at viewport375); wrapping was repaired and awaits the final built readback. Local browser also observed the existing favicon404 and CSS-preload warnings. No live Supabase read or protected dev readback, whole-Spec acceptance or Human QA is claimed yet. The source-injected skill evidence is incomplete/unqualified and authorizes no skills merge or installation.

Final local readback at source1f87d39: production build passed; all203 site tests passed; built-site hygiene zero. Phone recheck after wrapping: viewport375, document scroll width375, actual screenshot retained locally; earlier overflow remains above as history. Repo hygiene found two pre-existing dev gaps already repaired on main (missing TASKBOARD max budget and a literal host path in a planted test string). Applying those exact main fixes and native render returned zero findings; no managed runtime or check was weakened. Current-head shared CI and protected dev readback remain the delivery gate.

## Resumption inventory — 2026-11-06

Workspace baseline sha256:210dc486dbab702cce0215b23b78c86d28b43fb504336d4195a9338eafa36fc3

Native complete resumption snapshot at committed dev 517184e46a4b3ba0ebda36a54a6744e1b7c3b606, recorded owner ams-records-site; actual observer/closing delegate codex-s007-reader-readback (gpt-6.1-sol, harness Codex, tier unknown). Existing claimant and history remain unchanged. This newly observed snapshot binds this resumed run only; it cannot reconstruct the abandoned original run. Original committed records remain reachable; raw inventory is retained privately outside the observed checkout. Parent verified the old claimant has no active worker and delegated bounded continuation. No competing open Spec PR or newer remote head was observed before switching this isolated checkout.

## Resumed Check and QA — 2026-11-06

At dev source `517184e46a4b3ba0ebda36a54a6744e1b7c3b606`, authenticated Vercel connector listing identified READY deployment `dpl_Hg4ZUAF5ZbwVNKLf3pZ2FsSdgS7N`. Exact deployment `/rsi` fetch returned HTTP 200 and `data-commit-sha` equal to that full SHA. Last successful read was `2026-11-06T10:21:12.288Z`. Result row 41 rendered at both `dev-per-task-row-41` and `dev-per-version-row-41`, with actual row links and provenance; no unavailable message rendered. This is a real populated read, not inferred emptiness. Safe summary only: raw protected HTML, access URLs/tokens and row contents remain private. Footer identifies the deployment; these records-only follow-ups are separate candidates and are not claimed deployed.

QA inspected the rendered read state, task/version traceability and provenance against TK-002, and read the existing model-change/regression/test-row fixtures and publishable-read/RLS source contract. It does not establish held-out headlines, the later private-lineage projection, whole-Spec acceptance, independent Review or owner Human QA. Earlier failed reads, null/partial-total and phone-overflow findings above, and all TK-002L/TK-0031 receipts, remain preserved.

Fresh Wiki and layout validation, native render, whitespace and source hygiene passed. Doctor returned pre-existing unrelated blocked slices/stale claims, legibility and Claude permission-scope diagnostics; no selected S-007 blocker. No repair of those other lanes was attempted. Sandbox fetch and uv-cache access required an alternate approved boundary; escalated fetch and the existing Python environment's source hygiene succeeded. A basic network-disabled Docker Node version check passed, but site bind-mount invocations stalled before creating a container and were canceled after checking their uncertain state. No local install/build/test success is claimed; required production build before tests and complete Python coverage use the existing shared CI workflows on the pushed candidate. Actual model gpt-6.1-sol, harness Codex, tier unknown.

### Current-base recovery limits

The narrow clone refspec initially left origin/dev stale despite a fetch of dev into FETCH_HEAD. PR conflict inspection exposed this; explicit tracking-ref fetch recovered current dev `40acb3a491a55599e5b1f00fd92a27315739a4a9`. Its normal merge preserved both complete website Wiki captures; resulting candidate `a00990a7121abf1ef6244e7f2029ea1e9744b68d` is mergeable. Fresh independent candidate layout/Wiki/hygiene/whitespace checks pass. Shared Python run 42204219727 and site run 42204222133 target that exact head; results were pending at this capture.

Read-only Vercel inspection found dev40acb3a deployment `dpl_3U2SoEgLBFPcTaduX2u4Qnr2DX3k` in ERROR: Next generation completed, then `postbuild` page-inventory generation failed with `Page inventory: route manifest/artifact coverage differs`. This belongs to the current S-003 inventory owner and was reported to the coordinator before repair; no foreign source, deployment settings or manual deployment was changed. The successful protected reader observation above remains pinned to dev517; current40acb3a is not claimed deployed or read back.

Native workspace-closeout first rejected an abbreviated baseline commit; the full-SHA invocation then reported missing-discovery-route because its pushed-pending route requires this exact candidate/ref in the integration (main) Spec. This website Task targets dev and does not authorize main publication. No managed tool or governance record was changed to bypass that mismatch; native accounted/remoteRecoverable/complete are not claimed. Generated hygiene bytecode was retained privately outside the checkout after the checker identified it as unselected ignored evidence. All originals remain committed; the genuine resumption snapshot and failed check outputs remain private. Native closure and acceptance stay pending required exact-head checks and truthful current deployment evidence.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-007-rsi-chart-pages | a00990a7121abf1ef6244e7f2029ea1e9744b68d | ahead 0 behind 0 | 1 | Independent protected dev517 HTTP200/exact footer/linked row41/readAt 2026-11-06T10:21:12.288Z PASS; fresh structural/Wiki/hygiene/whitespace PASS; exact-head a00990a shared CI pending; local bind-mount build unavailable | site/README.md protected readback; website Wiki, Landmark synthesis and MEMORY; TK-002 resumption evidence | Current dev40acb3a inventory postbuild deployment failed; S003 owner notified. Native preservation check main discovery-route mismatch; no complete closeout claimed. Required CI and native close remain pending; no owner QA or whole-Spec acceptance. | 2c7fb7dadc8f3a0fbb30143cff47167eef1d8588c1c8e65a73e8e4ff7bd20931 |
