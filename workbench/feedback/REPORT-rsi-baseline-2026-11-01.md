# Loop #1 baseline: merged AMS main

## Target And Scope

Assessment `AMS-RSI-L1-BASELINE-20261101`, November 1, 2026. Whole AMS at
[`a3d014e`](https://github.com/KaydenClark/Agentic-Management-System/commit/a3d014e18f3f447d887a85fe6b6f16471781d509),
merged by owner direction in [PR #70](https://github.com/KaydenClark/Agentic-Management-System/pull/70).
This is baseline/attempt 0 and consumes no improvement strike. No source repair
was made during assessment. The supplied pre-build readback remains historical
proposed context; current owner answers and later decisions govern.

**Result: Broken. Provisional Alignment Score: 4/138 checks passed, approximately
2.90%. Acceptance: not accepted. Evidence: incomplete. Evaluators: unqualified.**
Exact percentage is `200/69%`; approximate display sets no rounding contract.
All three runs fail because required Critical evidence is missing. The score
measures available full-scope passing evidence. It is not an estimate of defective
code, operational reliability or demonstrated improvement.

## Evidence And Limitations

- Frozen inventory: all 446 tracked objects at tree
  `b161312f6d0b41a7d711915b73acb9ff890ca645`. Reconstruct with
  `git ls-tree -r a3d014e18f3f447d887a85fe6b6f16471781d509`.
  Inventory SHA-256 is in the linked assessment metadata.
- Approved r1, check version 1, source SHA-256
  `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`.
  All 47 core IDs retain their original 14 Critical/33 Quality classes. No
  Regression class is inferred without baseline pass evidence. A07-04 alone is
  N/A: AMS is not Audit_Workbench assessing its own adoption. The unclaimed
  v3.2.3 connected-Board expansion is outside this core inventory.
- Three separate assessor contexts reviewed the same pinned source and evidence.
  These are **read-only evidence-review runs, not behavioral worker trials or
  cold native-entry proofs**. Each was supplied the exact repository and assignment.
  Native skill use, cloud execution, recovery and comparative benefit remain
  unproven. All 40 managed tool hashes matched their receipt, a bounded identity
  check that cannot certify personal skills or native activation.
- Checked candidate `7993fe9eccfcb8913b420a477d7713f5a4fd0bc1` has exactly the
  same tracked tree as assessed main. Python: **368 passed, 4 skipped**. Site:
  **build passed, 70 tests passed**. Both GitHub checks on PR #70 succeeded.
  Layout/ADR validation passed; regenerated Taskboard matches. Doctor retains
  two nonblocking findings: legibility-undeclared and permission-scope-drift.
- Separate-context merge-preservation review found no lost branch changes or
  findings within that scope. It supplies neither Human QA nor product acceptance.
- Vercel reports production deployment `dpl_3Wiqgkc2ZvNcUxHjePsmQLM98UDk`
  READY at assessed main. This is deployment metadata, not rendered-site QA.
- Exact assessor model IDs are not exposed and remain unknown. No semantic
  evaluator qualification or protected behavioral-grader campaign is claimed.
  Missing proof stays No in its original class and denominator. Execution uses
  the subscription meter; unavailable per-run costs/tokens are not invented zeros.
- Original assessor outputs remain preserved locally. Published exports remove
  one host-local input locator without changing a verdict, reason or count.

[Assessment metadata](../../evals/rsi-loop-1/baseline-20261101/assessment.json)
and independent ledgers: [run 1](../../evals/rsi-loop-1/baseline-20261101/run-1.json),
[run 2](../../evals/rsi-loop-1/baseline-20261101/run-2.json),
[run 3](../../evals/rsi-loop-1/baseline-20261101/run-3.json).

| Run | Yes | No | N/A | Passing run |
|---|---:|---:|---:|---|
| 1 | 1 | 45 | 1 | No |
| 2 | 1 | 45 | 1 | No |
| 3 | 2 | 44 | 1 | No |

## Findings

**F-001 — RSI execution and results path is incomplete (high).**
Canon: S-002/S-006/S-007 and the owner's Loop #1 request. Actuality: `evals/`
has templates but no runner or fixed task set; `site/app/rsi/page.tsx` imports
`emptyRows`, and `data.ts` has no Supabase reader. The earlier live query found
zero real runs/results. Impact: the promised assessment/record/display loop
cannot operate yet. This does not show the existing writer is broken.
Recommendation: one end-to-end assessment/attempt slice, retaining failures,
measurement availability and writer-to-Supabase-to-dev readback.
Disposition: accepted-open; owner: S-002, S-006 storage and S-007 presentation;
evidence: their current Specs and the pinned source paths above.

**F-002 — Current consumers retain superseded meaning (high).**
S-001 says secrets live only in Vercel/Supabase settings, conflicting with
ADR-003H and the owner's local-writer-key decision. S-002 TK-002 and
ADR-003F/003G retain older campaign gates despite the current meter correction.
S-001/S-003 say no website exists although four routes build. Mechanism: a fresh
agent can recover the wrong operation from disagreeing current consumers.
Recommendation: reconcile current consumers, preserve history, then retest cold
pickup against the owner's exact corrections. No secret exposure was observed.
Disposition: accepted-open; owner: S-013/S-002; evidence: owner-answer Wiki,
`coherence/COHERENCE-2026-11-01.md` and the run ledgers.

**F-003 — Document size contracts are violated (medium).**
Unicode counts: S-003 11,344, S-004 8,218 and S-006 8,183 against 8,000;
README 4,245 and GLOSSARY 3,055 against the 3,000 root-control rule. The latter
includes this chat's glossary additions. TASKBOARD is 3,737, with its generated
view limit already disputed in COH-002. That ambiguity does not excuse the
undisputed excesses. Recommendation: prune in place, preserve obligations and
evidence, and check budgets in delivery. Changed reviewed Specs need their
required fresh review; do not silently rewrite their reviewed candidate.
Disposition: accepted-open; owner: S-001 TK-002 and affected Spec authors;
evidence: artifact-budgets.json, ADR-002V and per-run source counts.

**F-004 — Whole-AMS behavioral proof is insufficient (high).**
Full-scope intent/result mapping, fresh discovery/continuation, authority and
visibility preservation, upgrade/recovery and real comparison proofs are missing
or partial. Product fixtures establish only their named behaviors. Recommendation:
freeze valid/adverse/resume workloads and known-failure controls, qualify grading
as applicable, and collect actual evidence with exact configurations.
Disposition: accepted-open; owner: S-002 evaluation and S-001 cold-start work;
evidence: S-001/S-002 and all run ledgers. Missing proof does not mean each
mechanism was executed and failed.

**F-005 — Owner-reported scope drift remains unresolved (high).**
The earlier demo-framing failure and this chat's lost grilling flow require
explicit original-case and regression retests. A merged record or omission
cannot close them. Cause remains provisional: agent behavior does not prove the
skill text caused it. Recommendation: use these real failures as evaluation
inputs and retest fresh use before retaining a lesson.
Disposition: accepted-open; owner: S-002/S-013; evidence:
`REPORT-demo-framing-failure-2026-11-01.md` and the current RSI Wiki.

## Complete Check Ledger

Reasons, source paths and evidence states remain in the linked run exports.
Run 3 accepts A06-04's static visibility of incomplete proof; runs 1/2 require
wider evidence. This disagreement is preserved rather than replaced by a
favorable consensus.

| Check | Class | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| A01-01 | Critical | No | No | No |
| A01-02 | Critical | No | No | No |
| A01-03 | Critical | No | No | No |
| A01-04 | Quality | No | No | No |
| A01-05 | Critical | No | No | No |
| A01-06 | Critical | No | No | No |
| A01-07 | Critical | No | No | No |
| A02-01 | Quality | No | No | No |
| A02-02 | Quality | No | No | No |
| A02-03 | Quality | No | No | No |
| A02-04 | Quality | No | No | No |
| A02-05 | Quality | No | No | No |
| A02-06 | Quality | No | No | No |
| A03-01 | Quality | No | No | No |
| A03-02 | Quality | No | No | No |
| A03-03 | Quality | No | No | No |
| A03-04 | Quality | No | No | No |
| A04-01 | Quality | No | No | No |
| A04-02 | Quality | No | No | No |
| A04-03 | Critical | No | No | No |
| A04-04 | Critical | No | No | No |
| A04-05 | Critical | No | No | No |
| A04-06 | Critical | No | No | No |
| A04-07 | Quality | No | No | No |
| A05-01 | Quality | No | No | No |
| A05-02 | Quality | No | No | No |
| A05-03 | Quality | No | No | No |
| A05-04 | Quality | No | No | No |
| A06-01 | Quality | No | No | No |
| A06-02 | Critical | No | No | No |
| A06-03 | Critical | No | No | No |
| A06-04 | Quality | No | No | Yes |
| A06-05 | Critical | No | No | No |
| A07-01 | Quality | Yes | Yes | Yes |
| A07-02 | Quality | No | No | No |
| A07-03 | Quality | No | No | No |
| A07-04 | Quality | N/A | N/A | N/A |
| A08-01 | Quality | No | No | No |
| A08-02 | Quality | No | No | No |
| A08-03 | Quality | No | No | No |
| A09-01 | Quality | No | No | No |
| A09-02 | Critical | No | No | No |
| A09-03 | Quality | No | No | No |
| A09-04 | Quality | No | No | No |
| A10-01 | Quality | No | No | No |
| A10-02 | Quality | No | No | No |
| A10-03 | Quality | No | No | No |

## Challenged Or Rejected Findings

- Green product checks prove neither whole-AMS reliability nor full intent
  satisfaction; their narrow successes also do not justify calling those tested
  components broken.
- Integration resolved the dual-branch baseline. It did not complete the site,
  perform owner QA or close S-006/S-004 review obligations.
- Low evidence coverage is not an observed failure rate. No effect size,
  uplift, control comparison or accepted fitness claim is supplied.
- The earlier proposed readback does not supersede later hosting/key decisions.
  No credential was found in this assessment.

## Next Action And Open Questions

The next interview choice is bounded r1 scopes plus affected regressions for
individual improvements, while keeping whole-AMS fitness separate. A candidate
pass must not confer a whole-system pass. No improvement strike was consumed.
Existing repair histories, including S-006's two used reviews, remain; renaming
does not reset their counters.

The assessment-to-Supabase-to-dev path remains to be designed and implemented.
Current trial tables require numeric cost/token fields; do not invent values or
mislabel these evidence reviews as controlled trials. The first implementation
should establish that path and the behavioral proof needed for a qualified gate.

## Review Boundary

Three separate read-only assessor contexts supplied unqualified judgments.
The separate integration reviewer assessed merge preservation only. The reporting
context assembled the merge and owns its documentation; no independent full-report
approval or owner QA is invented. Later report commits do not rewrite the pinned
baseline.
