# Handoff: Orchestrator B (Grill Board, RSI data, RSI loop)

**Written:** 2026-11-01 by Orchestrator B, at the owner's wrap-up instruction. **For:** a fresh orchestrator starting cold. Delete this file once its next action is done and the state below is reflected in the owning records.

## Endpoint

The owner's stop point is the full site on the protected `dev` deployment with a Grill Board review card for every page. After that, the RSI loop runs until the token meter is spent or three strikes stop it. B owns LMK-001 (Grill Board), the Supabase data store (S-006), and LMK-004's loop (S-002). A owns the site and C owns coherence and independent review.

## State

- **S-004 Grill Board** (active). Every Task is merged: board, theme, answers, rating, too-taxing flag, review fixes ([PR #58](https://github.com/KaydenClark/Agentic-Management-System/pull/58)). C's review #1 failed at `dd52f70`; review #2 **passed** at `4d49bfc` with digest `3e475711fb57`. **Waiting on the owner**: approval (`spec-workbench.mjs approve`) and Human QA, then `complete`. Don't edit S-004's reviewed sections (criteria, decisions, prose, Completion Result) before completing: that changes the digest and voids the pass. Only header gate fields and evidence-row cells are outside the digest.
- **S-005 page review cards** (planned, inactive). Four Tasks are ready ([PR #54](https://github.com/KaydenClark/Agentic-Management-System/pull/54)): TK-001 generator, TK-002 approvals to Supabase `page_approvals`, TK-003 voice record, TK-000K coverage check. **Slot plan:** S-005 takes S-004's slot when S-004 completes. TK-001 must commit exact canonical-content hash vectors (whitespace, sorted attributes, NFC and entities, void elements, `data-review-exclude` and `data-review-mark` subtrees removed) so A's site computes identical hashes. Tell A when `page_approvals` exists (S-003 TK-004 waits on it).
- **S-006 data store** (active). Tables `build_events`, `rsi_runs` and `rsi_results` are live with RLS: the site key reads non-test rows only, every client write is refused, and a single source and strength rule applies. Two independent reviews failed: `c87bf4e` (fixed by TK-000E, [PR #49](https://github.com/KaydenClark/Agentic-Management-System/pull/49)/[#53](https://github.com/KaydenClark/Agentic-Management-System/pull/53)) and `d6d4a6d` (history readcheck compares against moving refs and keys only; the legacy-key tick overclaimed). **Strike 2 of 3 is used (ADR-002W).** The strike-2 correction is in the "S-006 correction" section below. The S-006 SPEC is over its 8,000-character limit on `main` and needs pruning by its author, in evidence-row cells or before the next review.
- **S-002 RSI loop** (active, no Tasks run). TK-001 (seeding) waits on S-006 complete. TK-002 (noise floor) waits on the **owner's standing campaign approval, given by the owner directly**: auto mode refused to record it when relayed by another session. Field contract agreed with A for `rsi_runs.detail`: `disposition` is retain, revise or remove; `variant` is a boolean; `version`; a fired stop sets `state='stopped'` plus `stop_rule` (three_strikes, paid_plan_requested, meter_spent or owner_stop) and `stop_note`. S-002's first Task records it in the Spec.
- **Slot plan:** S-004's slot goes to S-005; S-006's slot goes to A's S-009 (demo Grill Board). The cap is 6 active Specs.
- **Infra:**
  - Vercel deploys only `main` and `dev` (ADR-003I). The team is on Pro.
  - Production is public at `www.workbenchsystem.app`, with the apex redirecting there (DDR-000Z). It shows 404 until the owner merges `dev` to `main`.
  - CI: `site builds` (site PRs) and `python tests` (pytest, record checks and the 375px board check on every PR).

## S-006 correction

PENDING: filled in when the strike-2 correction implementor reports.

## Open owner gates

- S-004: approval and Human QA, then complete.
- S-002: the standing RSI campaign approval, given directly by the owner.
- `.claude/settings.json` Edit allow rules for the workbench lanes. Without them `doctor` keeps reporting `permission-scope-drift`, which blocks nothing.
- Optional: make `python tests` a required GitHub check on `main`.
- `README.md` is over the 3,000-character root-control limit and needs a prune.

## Local-only facts (a cloud agent can't see these)

- The Supabase secret key lives only in the gitignored env file at the root of the owner's main checkout on Servitor (`/Users/kayden/GPT_OS/AMS`). It is never printed or committed. A hook blocks shell commands that name that file; the `ams-*` commands read it themselves.
- Live commands must run there: `uv run --directory /Users/kayden/GPT_OS/AMS <cmd>`, after `git -C … pull --ff-only origin main` while that checkout is clean and on `main`. The commands are `ams-keycheck`, `ams-writer`, `ams-history import|readcheck`, `ams-rsi livecheck` and `ams-sources livecheck`.
- The Grill Board runs locally on Servitor: `uv run ams-board` serves 127.0.0.1:8765. It is never deployed.
- The owner's artifact copy for the QA screenshots is not in the repo. It is the "Grilling Board Redesign" artifact, version 1793538932-43c3.

## Next action

PENDING: set when the S-006 correction reports.
