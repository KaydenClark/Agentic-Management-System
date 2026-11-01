# Handoff — Orchestrator A (website, cloud)

STATUS: stopped by owner · 11/01/2026 · by orchestrator A (Claude cloud session)

Continuation notes only, not authority. Verify live state first (`git fetch origin`; open PRs into `dev`).

## Owner stop and correction (11/01/2026)

- Owner: "STOP YOU ARE BUILDING THE WRONG THING". A stays stopped until the owner says resume.
- Owner, relayed by the coordinator: "instead of an orientation guide and skills wiki I have agents asking me what kind of demo I want and adding the RSI info off of the website because it would interfer with the demo".
- The earlier "demo" framing is **withdrawn**. That covers the demo batch, the cutoff and freeze times, the demo priorities, and holding RSI back. There is no demo to design, and the owner is not to be asked what demo they want.
- RSI information stays on the site. Nothing comes off the site to protect a showing.

## The job

Build the owner's confirmed site to the Specs and CDRs. LMK-003 covers:
- S-003: shell, orientation tour, under the hood
- S-008: skills wiki, written as site summaries in the style of aihero.dev/skills
- S-009: the demo Grill Board page, one page with sample non-engineering cards
- S-010: the governance stack and flow charts

LMK-002 covers S-007, the RSI pages: charts plus RSI information. Real data appears as soon as its source is accepted. Until then the pages explain the RSI and show the honest empty state.

## Rules that hold

- Site work goes feature -> `dev` -> `main`. Agents merge into `dev` once the `site builds` CI check passes (ADR-003I). Only the owner merges `dev` -> `main`.
- Vercel deploys only `main` and `dev`.
- Production is https://www.workbenchsystem.app, which is public and canonical, and changes only when the owner merges.
- `dev` stays on its protected vercel.app URLs.
- At most six active Landmarks ([ADR-003J](../docs/adr/003J-limit-active-landmarks-not-specs.md)); Landmark -> Spec -> Task. Specs need no slots. The owner stop above still holds.
- One writer per file. A is the only writer of `site/page-list.json`.
- The claim tool picks TK-004 by default, so always pass `--task`.
- The hygiene check rejects Claude-Session links in served pages.

## Verified state

- **`dev` = 992a5f8.** Its pages:
  - shell, with a centred container and the reading order in the top bar (PR #63, owner layout feedback, b551cf3)
  - Start here, rebuilt as short screens, flow charts and a lifecycle toy with the owner quote removed (PR #67, 992a5f8). The owner said STOP right after this merged; whether it stays is the owner's call.
  - How it works
  - `/rsi`, showing the empty-state chart places and the RSI explanation
- **Checks on `dev`:**
  - TK-005: hygiene, axe, keyboard, reduced motion, 375 px, third-party requests
  - TK-007: the token check, with the theme block generated from `grill-board/theme/tokens.json` by `npm run tokens:gen`
- **Closed:** S-003 TK-001, TK-002, TK-005 and TK-007; S-007 TK-001.
- **`site/page-list.json`:** `/`, `/rsi`, `/start` and `/how-it-works`. The `/start` entry still names PR #23's commit and needs updating to 992a5f8.
- **Records:** the S-003 Spec is over its 8,000-character limit and needs pruning. Branch `records/a-correction-dev` logs the stop and correction; it is pushed and unmerged.

## Built, pushed, not merged (no PR)

| Branch | Page | Waits on |
|---|---|---|
| `site/s007-tk002-rsi-live` (187061f) | `/rsi` reads `rsi_runs` and `rsi_results` | S-006 accepted (it failed reviews 1 and 2) |
| `site/s003-tk006-under-the-hood` (171cce2) | `/under-the-hood` from `build_events` | S-006 accepted |
| `site/s009-demo-grill-board` (cc34492) | `/grill-board-demo` | S-009 active |

- Draft PR #20 (the old Grill Board prototype) is superseded by that branch.
- Before merging any of these three:
  - merge `origin/dev` in and adapt to the top-bar nav;
  - mark live regions `data-review-exclude` (S-005 hash rule);
  - close the Task with `--task`;
  - add the page to `page-list.json`.

## Open work

- S-003 TK-003 (rest of the tour), TK-004 (draft marks from B's `page_approvals`, once it exists) and TK-006.
- S-007 TK-002 and TK-003.
- S-008 skills wiki and S-010 governance stack and flow charts: planned, no Tasks yet.
- Fresh-context Spec reviews by orchestrator C: none requested yet.
- Owner gates:
  - extend the Vercel connector's access to the `agentic-management-system-site` project and team;
  - resume and authorize S-009's scoped work; no Spec slot is needed.

## Resume point

Wait for the owner's next instruction. When the owner says resume, ask nothing about demos. Find out what the owner meant by "the wrong thing" before building further.

## Peers

- Coordinator (owner's machine): session_01UmLJaYpvFNgdMtECMorgKY
- Orchestrator B: session_01UmLJaZDjSkp781nt5p2jr1
- Vercel: project prj_AW53nWMo9WMHfLujOjUOjMH51frE, team team_xTKOSRO3aHZzt794rxYLiODN
