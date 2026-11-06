# TK-002Z - Every built public page supplies truthful review ownership automatically

**Task ID:** TK-002Z
**Spec ID:** S-003
**Slice:** Every built public page supplies truthful review ownership automatically
**Status:** in-progress
**Blockers:** TK-002X
**Destination:** spec-acceptance: Route, Trust, Owner presentation
**Planned verification:** Real Next build versus inventory, automatic new-route fixture, missing/ambiguous-owner and classification controls, idempotence, source provenance and affected repository/site checks.
**Claimed by:** codex-s003-inventory
**Current claimant:** codex-s003-inventory

## Assignment

Owner's twelve-outcome request of2026-11-05, confirmed without another checkpoint: "Reconcile the built route inventory with page-review coverage, including every skill article." The current source is the checked baseline delivered by PR176 into dev259b7a905639cc6ab621220b160fc813c5bc43f1. TK-002X is natively closed and preserves its evidence.

One frontend writer owns site/page-list.json, build-time inventory scripts, package scripts, focused inventory tests and documentation. Stack: committed owner declarations and frozen public Workbench records -> actual Next route/prerender manifests and HTML -> deterministic page-list projection -> S-005's existing collector. No Git or host configuration is available inside that collector's container. Generate from those frozen inputs, never private source or guessed history.

Preserve all seven existing page-list rows exactly. Discover the skills index and every actual built article through declarative patterns, not39 hand-maintained card rows. Existing additional pages use verified current S-008 owners from their records and actual dev259b7a9/PR176 containment, explicitly not original introduction. The framework visitor404 is a public review surface; only _global-error is classified as internal fallback and excluded. Missing/ambiguous current Spec/Task ownership refuses before writes.

Root-approved provenance: historical-landing remains the default for unchanged legacy rows; verified-containment names an actual containing revision; new unintegrated routes use explicit pending-candidate with landed:null. The collector supplies its immutable expected candidate SHA for cards/index; never commit a self-referential candidate hash or invent a landing PR. New declared pages must join the normal build/collection path automatically. Preserve metadata writer ownership, public-page privacy and content-hash rules.

S-005 owns Python collector/Board/cards. Coordinate the flat pages output and postbuild read order with its writer; do not edit their code. S-009 owns its new-page/nav/tour/glossary integration, including /grill-board-demo under its actual TK-0030 once available; do not claim it landed in259b7a9. RSI hash exclusions, keyboard correction, demo authoring and governance diagrams are outside this Task unless root explicitly assigns a bounded correction. No deployment, Human QA, personal installation, model campaign or main promotion.

## Acceptance

- [ ] One real build produces exact public artifact/page-list coverage, including all actual skills articles and visitor404; internal error exclusion is explicit.
- [ ] Existing seven rows remain byte-equivalent as objects; additional entries have real owner records and honest provenance, with unknown original introduction left unknown.
- [ ] Adding one declared fixture page/article automatically yields its inventory entry; no manual card row is required. Missing/ambiguous ownership, unsupported classification and stale coverage fail.
- [ ] Generation is deterministic/idempotent and runs from Git-free frozen inputs; pending candidates contain no invented landing or self-referential hash.
- [ ] S-005 can consume the generated flat inventory before requests/Board writes. Affected checks and scoped QA pass; exact source and limits are returned for checked dev delivery.

## Starting inventory

Workspace baseline sha256:2ea064d22681213beb226e4a9eca397b64ba656035b3f7a780c272f89b80c3fc. Original claim/projection committed first; prior generated public build/manifests copied and verified privately outside the checkout before this complete snapshot. No product changes preceded the separate digest binding.
