# Coherence sweep, 2026-11-01

**Owner:** S-013, orchestrator C (cloud, no secrets). **Targets:** `main` `0a7d04e`, `dev` `87a3576`, measured 2026-11-01 13:18 UTC.
**Method:** `spec-workbench.mjs doctor|list|render`, a character count of root controls and every Spec/Task/Landmark, the drift check (`ams.coherence.drift`), and a full read of all 107 CDRs by a separate read-only subagent. C spot-checked COH-005 and COH-006 in the source text. **Limits:** C cannot see the owner's 81-item list, which lives in the private GPT_OS repository, so COH-004 compares CDRs with each other and with their provenance lines, not with that list.

## Checks that pass

| Check | Result |
|---|---|
| Active Specs at most 6 (ADR-002S) | 6 active: S-002, S-003, S-004, S-006, S-007, S-013. The other 7 are planned. At the cap. |
| Specs, Tasks and Landmarks at most 8,000 characters (ADR-002V) | All within the limit. Largest: S-001 at 7,975, S-003 at 7,431, S-002 at 6,775. |
| `dev` ahead of `main` (ADR-002T) | 5 commits, 0 days, 0 behind. Within threshold: [DRIFT-2026-11-01](DRIFT-2026-11-01.md). |
| RSI rows pin a skills commit (ADR-002R) | No RSI runs or rows exist yet. Nothing to check. |
| Three-strikes stops (ADR-002W) | The rule is in AGENTS.md. No stop has been reported yet. |
| `canonicalized_in` targets exist | All exist. |
| Independent reviews due | None. No Spec has been assembled. |

## Findings

Each finding has one disposition, as defined in the [Glossary](../../../GLOSSARY.md#feedback-dispositions). In this report, `diagnostic` means this sweep is the diagnostic. It is manual unless a check is named. **Return to** names who acts.

| ID | Sev | Finding | Disposition | Return to |
|---|---|---|---|---|
| COH-001 | med | `README.md` is 4,245 characters, over the 3,000 root-control limit. `artifact-budgets.json` does not list README, GLOSSARY or TASKBOARD, so no tool enforces their limit. | diagnostic | B: prune README, don't split it. Add the three files to the budget file. |
| COH-002 | low | `TASKBOARD.md` is 4,364 characters. It is generated (ADR-000V), so it is unclear whether the root limit applies to it. | diagnostic | Owner: decide whether a generated view counts. |
| COH-003 | med | AGENTS is 2,992 characters, ARCHITECTURE 2,998 and RUNBOOK 2,996. All are within the limit but about twice the 900 to 1,500 target, with fewer than 10 characters of headroom. S-013 must document its commands in RUNBOOK and cannot do so without pruning. | accepted-open (S-013 Documentation Impact) | B: prune RUNBOOK; C then adds the coherence line. |
| COH-004 | high | There are 107 CDRs (83 ADR, 24 DDR) but 81 owner items. No mapping from items to CDRs exists. Of the 107, 15 cite only answers given after the review: ADR-002X, 002Y, 003A, 003B, 003C, 003D and DDR-000P to 000X. ADR-003B, 003C and 003D say they were "given after the decision review", so they are probably not among the 81. | diagnostic | **B: please add a mapping from owner item to CDR IDs**, flagging any CDR with no owner item. |
| COH-005 | high | Contradiction: ADR-002O says the owner "still approves each merge". DDR-000H and AGENTS say agents merge feature to `main` and the owner's "only merge gate is `dev` -> `main`". ADR-002F also counts the merge as an owner gate. | diagnostic | Owner: confirm which holds. B then supersedes the other. |
| COH-006 | high | Contradiction: ADR-002Y says "Secrets live in Vercel and Supabase environment settings". ADR-003C says the service role key is kept "only in a gitignored local environment file". | diagnostic | Owner, or B, from the owner's answer. |
| COH-007 | med | These CDRs hold more than one decision (one decision per CDR is required by ADR-000N/O). ADR-000D, 000E, 000R, 000X, 001G, 001K, 001S, 001T, 001W, 001Y, 002B, 002F, 002I, 002J, 002R, 002X, 002Z, 003B, 003C. Several also restate a decision recorded elsewhere: 001G and 001I; 001K and DDR-000H; 000R and 000T; 001T and 002J; 002R and 002Z. | diagnostic | B: split each into its own decisions, or merge the restatement into the existing record, against the COH-004 mapping. |
| COH-008 | med | Duplicate pairs: ADR-002H and DDR-000C (control arms); ADR-002P and 002Z (Rule of Two); ADR-000N and 003E (the two CDR kinds); ADR-000T and 001Q/001R (deleting notes and handoffs). | diagnostic | B, with COH-004. |
| COH-009 | med | Details that may be unsourced: "about 30" (ADR-001N); "pass^3" (002I); the per-trial cap (002J); the "voice guide" and rewrite-before-re-ask (DDR-000J); "drafted by agents" (DDR-000U); the Confirmed/Refuted thresholds in all 12 hypothesis CDRs. The owner may have confirmed these; C cannot see that. | diagnostic | B: cite the owner source, or mark them as proposed. |
| COH-010 | low | Minor tensions. ADR-000E counts tokens and says limits "never split", while ADR-002V counts characters. DDR-000G names Map, Plan and Build, which are not steps in the ADR-001J workflow map. DDR-000L ("never the record") sits against the Grill Board treated as a record store (DDR-000P, ADR-002U). DDR-000O ("no development view" on Vercel) sits against the owner-only dev deployments in ADR-003B. | diagnostic | B. |
| COH-011 | low | Bare IDs collide: 000A to 000X exist in both `adr/` and `ddr/`. They are unique only with the `ADR-`/`DDR-` prefix. The subagent also saw tools citing `DDR-000Y`, `DDR-001C` and `DDR-001E`, which do not exist. C has not verified whether these are fixtures. | diagnostic | B: confirm whether those tool citations are fixtures. |
| COH-012 | low | `TASK-TEMPLATE.md` uses `T-NNN` while the tooling uses `TK-###`. This is already logged in [WORKBENCH_FEEDBACK](../WORKBENCH_FEEDBACK.md). | diagnostic | Owner decides; B aligns the template. |
| COH-013 | med | A Task can be blocked only by a whole Spec. For example, S-013 TK-003 waits on all of S-006 when it needs only the result-table migration, and TK-005 waits on all of S-004 when it needs only the card format. | diagnostic | B: log it in the feedback lane, or block on a Task ID. |
| COH-014 | low | `doctor` reports `permission-scope-drift` in `.claude/settings.json`. Only the owner can fix it, and it is already logged. C recorded it and changed nothing. | diagnostic | Owner. |
| COH-015 | med | In C's cloud session, `doctor` reports `personal-catalog-unavailable` as blocking: the 16 required skills cannot be installed here, and ADR-001S expects them to be. Despite this, `claim` succeeded. Either the finding does not block claims or `claim` does not consult it. This is also the S-013 signal for a session that could not install skills. | diagnostic | B or owner: make the skills catalog available to cloud sessions, and make doctor and claim agree. |
| COH-016 | high | **No secrets** (S-013 acceptance): C's environment has no Supabase or Vercel secret variables. However, this session has account-level Supabase and Vercel connectors attached, which could read project settings and keys. C has not used them. The acceptance line cannot pass while they are attached. | accepted-open (S-013 No secrets) | Owner: detach both connectors from C's environment. |
| COH-017 | low | S-013 tasks say to put checks "beside the room tools", but the managed `workbench/tools/` runtime refuses unreceipted files (`tools-receipt-missing`), which blocked the next claim. The check moved to `src/ams/coherence/` in `d242334`. | repaired (`d242334`) | B: reword the S-013 Task text if it is re-planned. |
| COH-018 | low | `pyproject.toml` pins Python 3.14, but the cloud image ships 3.13. C installed 3.14 with `uv python install 3.14`. | diagnostic | B: name the install step in the RUNBOOK fresh-clone check. |

## Requests

- **B:** the COH-004 mapping first; then COH-001, COH-003 and COH-007 to COH-011.
- **Owner:** COH-005, COH-006, COH-016, then COH-002.
- **C** reruns this sweep as work lands, and reviews each Spec once it is assembled.

## Owner answers, 2026-11-01

Recorded in [owner answers](../../wiki/context-owner-answers-coherence.md). Each disposition below replaces the one in the table above.

| ID | Answer | Disposition |
|---|---|---|
| COH-005 | The owner does not approve every merge. Agents merge non-site work into `main`; the owner approves only the site's `dev` -> `main`. DDR-000H and AGENTS were already right; ADR-002O and ADR-002F were wrong. | repaired: ADR-003F and ADR-003G supersede ADR-002O and ADR-002F |
| COH-006 | The owner delegated the call. The service role key stays only in the gitignored local env file (ADR-003C); Vercel holds only the URL and publishable key, because the site only reads. | repaired: ADR-003H supersedes ADR-002Y |
| COH-016 | The connectors stay attached, because they are shared with the other orchestrators. C never uses them. | declined (detaching); S-013 No secrets now requires that C never calls them |

## Later findings, 2026-11-01

| ID | Sev | Finding | Disposition | Return to |
|---|---|---|---|---|
| COH-019 | high | The Vercel free plan's limit of 100 deployments per day was hit at 13:48 UTC. Vercel reported `api-deployments-free-per-day` on PR #30 at `a1b3d8d`. Every push to a PR branch creates a Vercel deployment, including non-site PRs where `site/vercel.json`'s `ignoreCommand` cancels the build. With three orchestrators pushing, the daily limit runs out, and site previews on `dev` are blocked for about 24 hours. Non-site PRs show a red Vercel status that is not about their content. | diagnostic | A or B, with the owner's go-ahead: stop deployments for branches that need none, for example with `git.deploymentEnabled` in `site/vercel.json` limited to `dev` and `main`, so ignored builds stop counting. |

| ID | Update | Disposition |
|---|---|---|
| COH-019 | PR #46 (`3affa38`) set `git.deploymentEnabled` in `site/vercel.json` to `main` and `dev` only, recorded as ADR-003I. Other branches no longer create Vercel deployments. | repaired (`3affa38`) |

## Wrap-up sweep, 2026-11-01 15:43 UTC (`main` `b0fd71f`, `dev` `e0317ae`)

| ID | Sev | Finding | Disposition | Return to |
|---|---|---|---|---|
| COH-020 | low | C's `up_to_spec` checker does not resolve Markdown reference-style links (`[board]: path`). It reported 4 evidenced S-004 lines as unknown. | accepted-open (S-013 Up to Spec) | C: resolve reference links, with a fixture test |
| COH-021 | high | `dev` is 84 commits ahead of `main` and 62 behind, which breaches the 20-commit threshold. See [DRIFT-2026-11-01-wrap](DRIFT-2026-11-01-wrap.md). | diagnostic (`ams.coherence.drift`) | Owner: merge `dev` -> `main`, the site gate. C raises no Grill Board item until S-013 TK-005 lands. |
| COH-022 | med | Recording a review verdict pushes Specs over 8,000 characters: S-004 is at 8,218 and S-006 at 8,183. Both were near the limit before review. | diagnostic | B: prune both. The process needs room for verdict rows. |
| COH-023 | low | S-013 TK-004 still shows `blocked` by TK-002, which is done. | diagnostic | The next C session updates the blocker when it claims TK-004. |

Status of the earlier findings at this commit:
- COH-001 (README at 4,245 characters) is still open.
- COH-003 (RUNBOOK at 2,986 characters) is still open, so there is still no room for the coherence commands.
- COH-004, COH-007 to COH-011 and COH-013 still have their original dispositions. C has not verified any change.
- COH-005, 006, 016 and 019 are repaired or declined, as recorded above.
