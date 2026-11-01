# TK-000S - Changed exact assessment artifacts cannot masquerade as retries

**Task ID:** TK-000S
**Spec ID:** S-006
**Slice:** Changed exact assessment artifacts cannot masquerade as retries
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Private assessment persistence
**Planned verification:** Red-first remote/local identity, prefix, replay and frozen-metadata fixtures; no-write refusal and exact retries; full/fresh checks and marked live conflict/cleanup.
**Claimed by:** codex-assessment-writer
**Current claimant:** codex-assessment-writer

## Assignment

Correct unmet existing S-006 immutable idempotence/conflict and S-002 frozen-metadata requirements under the standing approved outcome; S-006 remains active and has not received formal acceptance. Base `110bb7af107b83b8eaf07a0bc871276b3a21ac26`; codex-assessment-writer owns one feature branch into checked main. Public-seam synthetic reproduction on that exact source independently confirms changed metadata true-to1 succeeds through remote prefix/duplicate and local duplicate/frozen/result replay comparisons despite different canonical bytes. The original remote evidence is retained, but changed evidence is silently accepted as its retry. [Late bot finding](https://github.com/KaydenClark/Agentic-Management-System/pull/83#discussion_r4437152745) is provenance, not the sole proof.

Use exact canonical artifact comparisons at remote prefix/duplicate and local immutable packet/frozen/result seams. No scoring formula, rubric contents, qualification, database schema, site or publication change. Preserve prior candidate-bound PASS/FAIL and closed receipts. Do not resolve approval-blocked external threads. Return immutable candidate for fresh independent review.

## Acceptance

- [ ] Valid scalar type/spelling changes (true-to1, exponent-float-to-integer,1.0-to1 and negative-zero sign) refuse at immutable remote/local identity and frozen/result boundaries with original evidence retained.
- [ ] Exact retries remain idempotent and rejected changes leave remote history unmodified; all relevant comparisons use canonical artifacts without changing scoring rules.
- [ ] Focused/full/fresh verification and marked live duplicate/conflict probes pass with cleanup0; prior review/receipt history remains intact.

## Red/green proof

Synthetic public-seam reproduction against delivered110bb7a independently observed changed canonical evidence accepted by remote prefix/duplicate, local duplicate, typed saved-result replay and frozen metadata. Twelve new pytest fixtures initially failed (DID NOT RAISE); schema true/1.0 protocol fixtures separately failed before the explicit exact-identifier repair. A shared canonical identity helper now guards only immutable packet/result/frozen/approved-protocol comparisons; remote prefix/duplicate compare preserved canonical TEXT. Scoring formulas, check classes, qualification and database schema are unchanged. Independent frozen-type fixtures cover the same comparisons separately. Full/live/fresh verification and independent review remain pending.

## Same-run historical-source correction

Independent scoped review of a95f629 found the same equality issue in retained historical source facts. Four valid Quality-finding observation fixtures (true/int, exponent/int, float/int and negative-zero sign) were observed red before applying the same canonical helper there. Source-run/candidate/observation fact strings keep their existing meaning. Audit of remaining equality sites distinguishes validated scalar IDs/classes and typed attempt counters from artifact identity; JSONB projection comparison intentionally remains type-aware semantic comparison because JSONB normalizes number spelling.
