# Handoff — Orchestrator A (website, cloud)

STATUS: in progress · 11/01/2026 ~08:40 MST · by orchestrator A (Claude cloud session)

Plain-language continuation instructions. Verify live state first (`git fetch origin`; list open PRs into `dev`). This handoff carries context, not authority.

## The job

Orchestrator A builds the AMS website: LMK-003 (S-003, S-008, S-009, S-010) and the pages of LMK-002 (S-007). It's a Next.js site in `site/`, delivered feature -> `dev` -> `main`. Agents merge into `dev`; only the owner merges `dev` -> `main`.

## Authorized endpoint

The owner approved the full build on 11/01/2026. A merges a site PR into `dev` once `site builds` CI is green (ADR-003I, RUNBOOK). A green Vercel preview is no longer needed, and previews no longer exist for working branches. Never merge `dev` -> `main`.

Demo freeze: no merges into `dev` or `main` from 07:00 to 09:00 MST on 11/02/2026. The demo is at 08:00 MST.

## Verified state

- `dev` = b551cf3 (PR #63: owner layout fix, centered container, nav in the top bar, metadataBase https://www.workbenchsystem.app; Vercel `dpl_51JpYcagSTCwvzvShrKQg5zvyWDM` READY). Before that, e0317ae (PR #47 demo batch). Its Vercel deployment `dpl_P21PisbATrNQUX7yLzY7hJ5PYzTB` is READY. Its contents can't be fetched from the cloud, so verify on the owner's machine.
- Live pages on `dev`: `/` (shell), `/start` and `/how-it-works` (TK-002), and `/rsi` (empty-state chart places, S-007 TK-001).
- Checks on `dev`: TK-005 quality checks (`npm test` hygiene; `npm run check:browser` axe, keyboard, reduced motion, 375 px, third parties) and the TK-007 token check (generated theme block, `npm run tokens:gen` from `grill-board/theme/tokens.json`).
- Closed Tasks: S-003 TK-001, TK-002, TK-005, TK-007 and S-007 TK-001. Each Task record lists its proof and gaps.
- `site/page-list.json` holds `/`, `/rsi`, `/start` and `/how-it-works`. A is its only writer, and B builds S-005 review cards from it. Keep each `path` stable.
- Vercel is on Pro now. It deploys only `main` and `dev`. Production domain: https://www.workbenchsystem.app (public, serves `main`; the apex redirects to www).

## In flight (Dispatchers started in the old chat; they do NOT merge)

1. **Done:** `site/s003-shell-topnav` merged as PR #63 (b551cf3). The phone nav wraps instead of collapsing, and "n of N" now sits beside Back/Next.
2. **Branch `site/s003-start-toy` (no PR yet at 08:45 MST), owner feedback (11/01):** rebuild `/start` as the Blueprint elevator pitch with flow charts and an interactive toy that walks one piece of work through the lifecycle, and remove the owner quote. The PR will carry the report. Merge it after #1, once green.

## Built, gated (branches pushed, no PR)

- `site/s007-tk002-rsi-live` (187061f): `/rsi` reads `rsi_runs` and `rsi_results`, matching B's `detail.variant` / `disposition` / `stop_rule` contract. Gate: S-006 accepted. S-006 failed reviews 1 and 2, and a third review is running.
- `site/s003-tk006-under-the-hood` (171cce2): `/under-the-hood` built from 463 `build_events` rows. Same gate as above.
- `site/s009-demo-grill-board` (cc34492): `/grill-board-demo`, which passes every check. Gate: S-009 active. Six Specs are active, so S-009 needs S-006 to close or the owner to swap S-002 to the backlog.
- Before merging any of these three: merge `origin/dev` in, adapt to the top-bar nav, mark live regions with `data-review-exclude` (B's S-005 hash rule), close the Task with `--task`, and add the page to `page-list.json`.
- Reading order: Home, Start here, How it works, Grill Board demo, Under the hood, RSI results.
- Stale PRs to close as superseded once their work lands: #14 is merged; **#20** (prototype) gets superseded by `site/s009-demo-grill-board`.

## Demo plan (11/02/2026)

- Vercel deploys only `dev` and `main`. Production is https://www.workbenchsystem.app (canonical, public) and changes only when the owner merges `dev` -> `main`.
- Freeze: no merges into `dev` or `main` from 07:00 to 09:00 MST. The demo is at 08:00 MST.
- Fallback: the last READY `dev` deployment (now b551cf3, `dpl_51JpYcagSTCwvzvShrKQg5zvyWDM`; before it, e0317ae).

## Resume point

Single next action: find the PR from `site/s003-start-toy` (Start here toy). Merge `origin/dev` into it if it is behind, and merge it into `dev` once `site builds` and Codex are green. Recreate a pre-freeze check for 06:30 MST on 11/02.

## Open work

- S-003 TK-003: the rest of the tour (Why, Limits, Glossary, quickstart, About).
- S-003 TK-004: draft marks. It reads B's `page_approvals` table, which doesn't exist yet, and must match S-005 TK-001's hash vectors.
- S-003 TK-006: see gated above.
- S-007 TK-002 and TK-003: gated on S-006.
- S-008: skills wiki. S-010: governance and flow charts. Both are planned, with no Tasks.
- **Fresh-context Spec reviews by orchestrator C:** none requested yet for S-003 or S-007.
- Owner action: extend the Vercel connector's access to the `agentic-management-system-site` project and team, so cloud agents can fetch `dev` pages.

## Boundaries

- No secrets. No web browsing; orchestrator C does research.
- At most six active Specs (ADR-002S).
- One writer per file. A owns `site/page-list.json`.
- Never `dev` -> `main`.
- The claim tool picks TK-004 by default, so always pass `--task`.
- The hygiene check rejects Claude-Session links in served pages, so strip them at render.

## Sources to load

AGENTS.md, RUNBOOK.md, ADR-003I, DDR-000Y, and the LMK-003 and LMK-002 landmarks with their Specs and Tasks, all on `origin/dev`.

## Peers

- Coordinator (owner's machine): session_01UmLJaYpvFNgdMtECMorgKY. Send it messages with the session service's send_message tool.
- Orchestrator B (owner's machine): session_01UmLJaZDjSkp781nt5p2jr1.
- Vercel: project prj_AW53nWMo9WMHfLujOjUOjMH51frE, team team_xTKOSRO3aHZzt794rxYLiODN.

## Suggested skills

None installed on the cloud host; the personal skill catalog is unavailable there, so `doctor` reports `personal-catalog-unavailable`.
