# Wiki memory: stopped candidate and bounded corrective restart

## Candidate and review boundary

Source candidate: `9419c9a2eec14bf5224fcbba4af1d3208c1a1466`; implementation comparison base: `28e4b122b7503348fcc119bfb98640dda2632a03`. [S-000D](../landmarks/LMK-000A-wiki-memory/specs/S-000D-memory-retrieval/SPEC.md) retains all five accepted improvements; [TK-002U](../landmarks/LMK-000A-wiki-memory/specs/S-000D-memory-retrieval/tasks/TK-002U/TASK.md) remains open with Receipt1 intact. The [Wiki Landmark](../landmarks/LMK-000A-wiki-memory/LANDMARK.md) is critical independent AMS memory, not RSI.

Source: direct root-thread handbacks, owner-local 2026-11-05 (UTC 2026-11-06). Independent fresh contexts `wiki_standards_review` and `wiki_spec_review` each ran High / OpenAI gpt-6.1-sol / Codex on the exact candidate/base above. They performed static code review only: no tests, edits, public actions or native verdict. These findings are supplemental review of an incomplete candidate, not assembled Spec PASS, Human QA or acceptance. Line references below identify the frozen candidate, not a claim that a future revision has the same lines.

## Stopped evidence

FAIL-118: first focused run12/13 failed because the fixture lacked a route; repaired run13passed. FAIL-119: baseline preflight rejected archive-placeholder scope mismatch. The worker then continued after the Runbook limit, encountered FAIL-120's unknown-query false hit (3/4development checks), repaired code and later reported16focused passes/4development checks. FAIL-121 already records that process breach; later passes do not erase it. Root STOP governed the stopped run; the owner later explicitly authorized the bounded continuation below. No post-STOP candidate tests or repair occurred in this records-only continuation.

The Task retains the actual baseline/candidate limits and artifact digests. Source-hit/proxy checks are not independently judged answer correctness, stale-answer prevention, transfer or owner correction effort. Real bindings, console entrypoint QA, operating docs, final checks and preservation proof remain incomplete. Native workspace inventory is still incomplete because pre-existing REBASE_HEAD residue remains; root reported no active rebase directories. Preserve that metadata and the explicit limitation.

## Supplemental static findings

**FAIL-122 — Baseline route body is read before privacy/path validation.** Standards reviewer: [capture_baseline.py](../../evals/wiki-memory/capture_baseline.py), line20, calls `(root / case['route']).read_text()` before containment, symlink, ignored-path or handling checks, then truncates the already-read text. A caller-selected route or unsuitable snapshot could therefore read/copy protected content. The script documents a prepared-public-snapshot precondition; no evidence shows the committed baseline exposed private data. The defect is the unchecked read boundary, not a claim of observed disclosure. Validate eligible source/route identity and handling before any body read; bound extraction and preserve refusal evidence. Static finding only; no exploit or rerun performed.

**FAIL-123 — Superseded context is silently and irrecoverably cut.** Spec reviewer: [memory.py](../../src/ams/memory.py), lines457–458, unconditionally slices each old correction's content to600characters without a truncation flag. If hits otherwise fit, line475 clears continuation. Increasing max-chars cannot recover the old context through this result. Preserve the full source and expose truncation plus a working continuation/read route; do not silently present a clipped correction as complete. Static code-path finding; no new runtime result claimed.

**FAIL-124 — Duplicate heading source selection disagrees with retrieval.** Spec reviewer: [memory.py](../../src/ams/memory.py), lines216–219, assigns a second repeated heading `purpose-1`; `_source_bytes`, line335, matches only the unsuffixed heading slug. A legitimate binding to the second section therefore reaches missing-source-anchor rather than change/restore detection. Align anchor semantics across retrieval and exact source selection, including section extent. Standards independently noted divergent duplicate-heading parsing; repository requirements govern, not a generic duplication heuristic. No currently demonstrated real binding is claimed affected. Static finding only.

The implementor associated with these source defects was High / OpenAI gpt-6.1-sol / Codex. Findings are accepted-open under the existing TK-002U acceptance; no new scope or Task is needed.

## Proposed bounded restart: TK-002U only

The owner subsequently authorized bounded continuation. This plan changes neither the Runbook stop limit nor prior results.

1. Recover exact9419c9a, Receipt1, source snapshot/case identities, all failures and the three findings. Use journey/TDD; serialize one High-tier source writer. Preserve existing evidence, private boundaries and managed runtime.
2. Repair only FAIL-122–124: validated baseline read boundary, explicit/recoverable correction truncation, consistent duplicate-heading source selection. After authorization, use TDD one public behavior at a time: intentional red, minimal fix, green; then the next defect. Do not batch absent-module reds into wholesale implementation. Cover safe refusal, bounds/continuation and source change/restore.
3. Complete the already-assigned real claim/source bindings on at least two routed topics, including Wiki's separate Landmark correction; retain observed revisions/digests/dates and supersession. Preflight snapshot, case and metadata eligibility before baseline evaluation; make source identity strict and retain blocked native-search evidence. No new questions or tuned cases may masquerade as untouched evaluation.
4. Complete/exercise the declared CLI entrypoint and concise operating docs. Run appropriate focused checks, scoped native checks and owned-path/source/confirmation preservation only after authorized restart. Report incomplete workspace inventory honestly; do not clear REBASE_HEAD or invent a full closeout.
5. Hand back a fresh committed candidate with exact checks, remaining gaps and immutable evidence. Root independently inspects it before deciding native closure or releasing TK-002V. TK-002V/W retain their existing artifact dependencies; all five improvements remain required.

## Original stopped approval boundaries

- **Corrective restart:** permission to resume only the bounded TK-002U work above after the Runbook STOP. Until an actual answer arrives: no source/test/evaluation edits, candidate retests, native close or further implementation.
- **Public export and delivery:** direct permission to push the Wiki Landmark/records and scoped implementation to KaydenClark/Agentic-Management-System and perform the checked non-site main merge. Automatic approval review rejected two push attempts (FAIL-114/115), including the exact-payload retry after remote/payload checks. No third attempt or alternate export route. Await the owner's answer; local restart approval alone would not release publication.

Records-only continuation captures findings and the proposed restart; it authorizes neither pending action. No push, PR, merge, deployment, installation, source repair or Human QA is recorded here.

## Authorized local continuation

The owner directly answered the exact bounded restart question: “Authorize bounded continuation”. [Native source capture](../wiki/context-wiki-maintenance.md#jot-4a2097ca-5bd6-456f-83c9-3bdbe7a79a29) retains the complete question and answer. TK-002U resumes locally; the earlier pending-restart paragraphs above describe the stopped boundary. Public export approval remains pending. Actual repair/check results belong to the Task and subsequent evidence; this authorization is no completion or acceptance claim.

## Corrective-run evidence

The High / OpenAI gpt-6.1-sol / Codex implementor repaired FAIL-122–124 in one focused red/green cycle each: restricted baseline-body guard failed then passed; long superseded context silently cut600 characters then recovered in full at larger bound with explicit small-bound truncation; duplicate heading source was unavailable then matched the retrieval anchor and passed subtree change/restore. Empty evaluation and source-manifest preflight each had their own intentional red/green control. Aggregate focused suite:25passed. These intentional detecting reds are not unexpected verification failures.

Real console query/check and the frozen four-case same-source development evaluation pass. Four claims across Wiki-memory/AMS-purpose bind six inspected sources at revision19778a2, observed2026-11-06; source correction lineage is retained. Disposable copies of those real sources passed exactly-affected-claim change, restoration, missing and unavailable checks; real owner/source bytes were not mutated. All87 earlier Jot blocks,18 history files,228 managed/shared-skill files and Receipt1 remain byte-identical. Hardened baseline capture reproduces the original committed baseline byte for byte. Private local recovery retains actual output JSON and preservation manifests; the Task binds final evidence.

FAIL-125 retains a pre-write system-Python import diagnostic, corrected by using project Python; root clarified that this is not a failed test. Unexpected verification failures in the corrective run:0. Focused Wiki/layout/hygiene checks pass. Doctor retains previously identified unrelated S-011/stale-claim/legibility/permission findings. Full fresh assembled tests, independent Review and remaining Tasks belong to root/later work; no Human QA or publication is claimed.
