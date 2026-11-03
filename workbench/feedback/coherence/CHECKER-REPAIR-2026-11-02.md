# Up-to-Spec evidence boundary repair

## Finding and candidate

A checked acceptance criterion with an `Evidence:` reference to an unrelated existing file was reported `met`. File presence or commit ancestry does not verify the behavior. The baseline module at `408e851e5ec621bd00f32e9a382df8d9a06b505e` had SHA-256 `7aa6c2efd6829d93e45ce5d3d099bfa451bcd143215372c13336396012ebc400`. Candidate `7735c553bbe2cde0e5c5d6a26a56e7468773961b` has module SHA-256 `2621bf52c450cfac9f83b34e4dcec16fef7e7455af2bcfefdad1dedace172c37`. It reports checked criteria as `unknown`, while retaining resolved references; unchecked criteria remain `not met`.

## Observations

The implementor reported 33 focused coherence and review tests passed. Deterministic `uv run python tests/coherence_replay.py` compared the baseline and candidate at fixture commit `ce9d9b71ef3709eddfc8fd615fe7280668e9f006`: three false `met` results, including an ancestor-only reference and a second unrelated existing file, became `unknown` with their references preserved. Missing and unmerged references remained `unknown`; an unchecked criterion remained `not met`. The second unrelated file demonstrates recurrence of the original pattern within the fixture, not later-use benefit.

The first attempted test had a fixture syntax error; the corrected test produced the expected red before repair. These are distinct observations. A fresh Luna context explicitly loaded the installed journey and carry skill bytes and ran the candidate on actual records without database, model or secret calls: S-001 returned 0 met, 6 not met and 2 unknown; S-003 returned 0 met, 8 not met and 0 unknown. These outputs describe the checker's conservative classifications, not proof that historical behavioral evidence is absent or that a Spec failed acceptance. Automatic skill discovery and other hosts remain unverified. The local personal catalog snapshot was `f2354fd037eddc3e02bf5766630bec8f039efaa7`, not a claim about published main.

## Limits and disposition

Full source suite and combined candidate checks were pending at this report. No independent assembled Review, owner Human QA, deployment, whole-Spec acceptance or benefit claim follows. The repair is a candidate awaiting assembly and review; the original false report remains historical evidence. Separately, the control-pruning work repeated an earlier ceiling-versus-goal failure and required root and owner intervention; see [failure report](../REPORT-runbook-target-failure-2026-11-02.md). This repair is not evidence of a fully autonomous end-to-end learning cycle.

Source: [draft PR 140](https://github.com/KaydenClark/Agentic-Management-System/pull/140), including implementor verification and pending checks; [S-013 TK-001V](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/tasks/TK-001V/TASK.md). Fresh-session observations were relayed by the coordinating orchestrator on 2026-11-02.

## Assembly update

The implementor's full source suite reported **809 passed, 5 skipped and 1 failed**. The failure was the inherited base's AGENTS length (3,215 characters), not a checker assertion; recovery candidate `49a0ef2` passed hygiene after that separate control change. This does not replace a full run on the final combined candidate. The root inspected the three-file checker diff and accepted the bounded conservative behavior for assembly. Source `7735c553bbe2cde0e5c5d6a26a56e7468773961b` is contained in assembly merge `e882efe9d905f074a0b36bff8976e49da03cc028`. The assembled candidate still requires final checks and independent Review; no whole-Spec acceptance or owner Human QA is implied.

## Reproduce fresh-record use

In a disposable checkout containing the source commit, the read-only invocations are:

```sh
git switch --detach 7735c553bbe2cde0e5c5d6a26a56e7468773961b
uv run python -m ams.coherence.up_to_spec S-001 --commit 7735c553bbe2cde0e5c5d6a26a56e7468773961b --json
uv run python -m ams.coherence.up_to_spec S-003 --commit 7735c553bbe2cde0e5c5d6a26a56e7468773961b --json
```

The fresh observer explicitly loaded journey SHA-256 `9b740599e8f694c8d662471b187c42d9124a02ed655bc7d28885b8ec134bf42a` and carry SHA-256 `5c6aed11058d392bedc4f1071e7942162d1b6cf52592e61c08b23d6a7a39d986` from the personal catalog snapshot named above. This is the coordinator's summary of an actual explicit load and use, not proof of automatic discovery. It does not establish the meaning or completeness of other historical evidence. The initial published snapshot remains at `e8450d2`; this maintained update records the later source-suite and assembly observations. Final assembled checks and independent Review are still pending.
