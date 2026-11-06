# TK-001 - A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes

**Task ID:** TK-001
**Spec ID:** S-005
**Slice:** A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Every page covered
**Planned verification:** pytest against a fixture page list and built pages in a temporary Git repository; live run against origin/dev


## Assignment

Target checked `main` via PR174; S-003 owns read-only site inputs. Preserve claimant, failures/receipts and unrelated work. [Full earlier assignment/checkpoint](https://github.com/KaydenClark/Agentic-Management-System/blob/7eedef9b76a3fa41f3cd0183492cef36cdebc914/workbench/landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/tasks/TK-001/TASK.md); S-005 links current confirmed authority.

Deliver `ams-pages generate`:

1. Freeze one trusted candidate SHA and export only its Git tree to owned temporary storage. Build/start through supported permissions; collect actual complete routes/served HTML. Historical `landed.commit` is provenance only. Injectable fixture evidence is labeled synthetic, not live proof.
2. Require explicit Spec/Task/landed ownership for every public surface, including all skill articles and visitor404. Distinguish internal global-error. Ref drift, missing/list-only owners and execution failure refuse before writes. Never invent provenance.
3. Candidate execution receives no private HOME context or service/provider/Git credentials. Own runtime cleanup through interruption; preserve unrelated files/processes.
4. SHA-256 canonical `<main id="main">`: exclude footer, script/style/comments and review-mark/exclude subtrees; retain decoded text and href/src/alt in source order; join/collapse ASCII whitespace. Preserve S-003 parity using README contract and `tests/fixtures/grill_board/pages/` vectors.
5. One current card per route/hash, `grill-board/pages/index.json` (path/title/landed/hash/card/candidate), and `grill-board/page-approvals.md` anchor `## Approvals`. Cards carry Topic, Priority/Value reasons, page/title/hash/candidate, landed provenance, Spec/Task/sources, recommendation and owner/write anchor. Only generated owners commit, through Board flock/CAS. Dirty/unsafe paths or conflicts leave no partial write; identical reruns make no commit.
6. Content edits create a new card and append dated stale/supersession without rewriting answered/history bytes. Footer-only edits do not invalidate content. Removed routes leave no actionable card; returning content gets a fresh occurrence. Stale cards leave the queue and refuse writes. Keep existing Board behavior and public privacy intact.

No site edits/live Board writes in another checkout. TK-002 approval readback/hardening, TK-003 criticism, TK-000K coverage CLI and TK-001E draft/review consumption remain separate. No Supabase approval rows, public review status or private criticism. Coordinate complete metadata with S-003. Close only after actual acceptance/checks/delivery.

## Acceptance

- [ ] Complete owned build produces correct cards/index/approval anchor in one commit; identical rerun is a no-op.
- [ ] Independent hash vectors, edit/footer staleness, immutable answered history and stale-write refusal pass.
- [ ] New/missing/removed routes, ref drift, dirty/unsafe paths and execution errors are handled without invented ownership, partial writes or unrelated changes.
- [ ] Actual runtime/interruption cleanup and private-context isolation are proved.
- [ ] Actual pinned build covers every skill article and visitor404 with cards and live Board readback.
- [ ] Required pytest/render/doctor and repository/current-candidate checks pass; unavailable checks named.

## Preservation and progress

Workspace baseline sha256:81dd8dfc83cf2aaa52dcbc6b763823137fe82ede9d053bb84a22225d4f2feb2d

Claim originals preceded the complete private inventory; separate binding preceded work. Local raw retention is not remote recovery.

Both failures remain below: missing CAS `--add`, then stale diagnostic masked by answered handling. Root inspected/released same-Task correction;119 focused checks passed. No attempt reset or new owner gate. At df2333b, frozen export/owner refusal/actual SIGINT cleanup fixtures pass3/3; sandbox ps refusal was resolved by approved observation. Container/live coverage, full checks, Review and Human QA remain; other Tasks unopened.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 1d4defb14d891e73ac0c3ef0200f3f56fbf71783 | none | 0 | STOPPED source 1d4defb. Before product edits: 115 Board tests passed after approved loopback rerun; initial sandbox run failed socket.bind (97 failed,18 passed). Expected missing-module red retained separately. Post-implementation tests/test_pages.py -xq first failed new-file CAS missing --add; corrected. Second run:1 passed,1 failed, stale answered-card refusal reported already answered instead of stale. No further correction/retry. | S-005 confirmed current-build and committed-only approval contracts; TK-001 stopped checkpoint; Board README and S-005 history. No site edits. | RUNBOOK verification stop: generator incomplete and not mergeable. Scoped release required before correction/retry. Automatic pinned-current-build collector, actual full route coverage, unrun new cases and post-change Board/full checks remain. TK-002/TK-003/coverage/feedback consumption unopened. No close, Human QA, public approval mirror or acceptance. | 32d09afc9162864eb71826644723aa9e03f0b72719fbdb6f92e4e52228567ab4 |
| 2 | Feature/S-005-page-review-cards | ce15fb2ab430c243cad23ae3c408451e4d0e2e21 | ahead 0 behind 0 | 1 | Source ce15fb2 product bytes: tests/test_pages.py plus existing test_grill_board.py/test_grill_board_answers.py/test_grill_board_ratings.py pass119/119 in86.85s with PYTHONPATH=src and approved loopback. git diff --check passes. Both prior failed runs and first receipt retained. Root inspected and authorized one early stale refusal under standing user scope; no campaign/attempt reset. | S-005 current-build contract and incomplete collector; TK-001 inspected correction; Board README. Prior failed Receipt unchanged. | TK001 incomplete: automatic pinned-current-build collection and live full inventory/card readback pending. Full repository/fresh candidate/shared CI/independent Review unperformed. Other S005 Tasks unopened. No new owner approval gate; next bounded assignment belongs to orchestrator. No Human QA or delivery acceptance. | af6254d52dafbd24a825e3bd5208a6a5d4561eebb4e7a5c2978db60c23c118b8 |
| 3 | Feature/S-005-page-review-cards | 39c0313d6e82e9d321d78eff84408aac4c351df5 | ahead 4 behind 0 | 0 | Source39c0313 collector suite:6 passed,1 failed. Real Docker fixture reached cleanup; os.killpg(server-client PID,0) raised EPERM. Approved process permissions used. Container SIGINT case unrun. No correction/retry after report. Owned-container readback empty. | Pinned collector/Docker fixture source; earlier receipts unchanged; Task compacted to6867 preserving receipt bytes. | Incomplete: host Docker-client cleanup observation unresolved; container lifecycle not qualified. CLI automatic path, actual Next build, complete S003 route metadata/cards and full checks remain. Parent inspects next correction; no new owner gate or attempt reset. | e95da87d1c8373faff8814266f53ed8a69629737caa8d12ad56ee59d62b1e55c |
