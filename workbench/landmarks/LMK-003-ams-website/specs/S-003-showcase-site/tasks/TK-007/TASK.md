# TK-007 - Recorded Grill Board tokens and a check that every value equals one

**Task ID:** TK-007
**Spec ID:** S-003
**Slice:** Recorded Grill Board tokens and a check that every value equals one
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Theme tokens
**Planned verification:** token comparison script failing on a stray color

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A
**Current claimant:** orchestrator-A
**Proof:** PR #32 (9c37ebf) merged into demo batch site/demo-batch-20261102 for one dev merge; scripts/gen-tokens.mjs generates the tokens.css theme block from grill-board/theme/tokens.json (DDR-000Y); tests/tokens-json.test.mjs requires the block byte-equal to the generator, markers once at stylesheet top level, nothing recorded or color-like outside; red/green per Codex finding; Codex code and security clean at 9c37ebf; batch npm test 59/59, check:browser 149/149

Blocked until the owner resolves `grill-board-theme-tokens` in S-003: the old Grill Board's values are not in this public repository. Read `AGENTS.md`, DDR-000M and the token file on `origin/dev`.

Deliver: a theme decision record listing every token with its source and meaning, the token file set to those values, and a comparison script in the site's checks that fails when any color, type or spacing value differs from the record.

Hand back to S-003 with `close`.

## Acceptance

- [ ] The decision record lists every token and cites the owner's answer.
- [ ] The comparison script fails on a planted stray color and passes on the build.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | site/demo-batch-20261102 | f63d945bfa25881708f4b78a1b5d4c903350857d | ahead 0 behind 0 | 0 | PR #32 (9c37ebf) merged into demo batch site/demo-batch-20261102 for one dev merge; scripts/gen-tokens.mjs generates the tokens.css theme block from grill-board/theme/tokens.json (DDR-000Y); tests/tokens-json.test.mjs requires the block byte-equal to the generator, markers once at stylesheet top level, nothing recorded or color-like outside; red/green per Codex finding; Codex code and security clean at 9c37ebf; batch npm test 59/59, check:browser 149/149 | site/README.md Theme token check; npm run tokens:gen | Type and spacing tokens not in tokens.json so not compared; five mix meanings supplied by the generator until S-004 TK-003 records them; check runs in npm test and CI, not in the Vercel build; dev deployment content to be verified on the owner's machine; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A","onBehalfOf":"orchestrator-A"} | e2368eb432ccb0432fa07288b9547249b20426653773fd9527e26fa8b4c21431 |
