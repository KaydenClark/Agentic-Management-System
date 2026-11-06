# Collector cleanup can observe an exiting group before its leader is reapable

**Disposition:** bounded correction qualified locally; fresh checks, independent
review and delivery remain required. No owner QA or permission waiver.

Central intake: [FAIL-210 and diagnostic cases211–220](WORKBENCH_FEEDBACK.md).
These rows were added late after the repair; FAIL-221 retains that recording
failure rather than backdating compliance. Prior receipt/source bytes remain.

The fresh b8e2236 approval-continuation suite finished984 passed,6 skipped and
one failure in `test_poll_interruption_is_reraised_after_owned_cleanup`.
`owned_process.send(0)` raised EPERM. Collector bytes are identical to held
PR174 source800a67b; earlier successful CI/full runs remain historical evidence.
The PR was returned to draft and its existing exact-main permission request
does not make that source safe to merge with this unresolved finding.

## Reproduction and diagnosis

An isolated unchanged-case rerun passed; that did not clear the full-run failure.
Independent investigation invoked the unchanged original case100 times under
the approved host permissions with in-memory poll/group-signal observations:
90 passed and10 raised PermissionError. Every captured failure followed a
successful group SIGTERM, signal-zero EPERM, then immediate poll returning None.
The known leader became reapable with returncode-15 shortly afterward; targeted
post-run observations found neither owned process. An unrelated sentinel stayed
alive through all100 cases and was then terminated/reaped by its own handle.
An earlier sandboxed diagnostic could not run ps and is not used as OS evidence.

Apple's public [group-signal implementation](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_sig.c#L1549)
and [group iterator](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_proc.c#L4059)
can produce EPERM when no eligible member is found. Python's
[POSIX poll](https://github.com/python/cpython/blob/v3.14.5/Lib/subprocess.py#L1835)
uses nonblocking waitpid; a None result is not an exit barrier. The public XNU
revision was not established as an exact source match for this host kernel;
the recorded host observations establish this execution's race. Astra supplied
investigation and strategy only; it made no source or test edits.

## Bounded correction and controls

After successful TERM, an observation-only EPERM waits for the known direct
child within the existing cleanup deadline. Group signaling is not retried
while that exit is unknown. After reap, group observation is retried once:
ESRCH establishes absence; success keeps descendant cleanup active; continuing
EPERM remains an error. Initial live-leader SIGTERM denial still propagates
immediately. Interrupted polling remains recorded and re-raised after cleanup.

A deterministic red reproduced the delayed-exit failure before the correction.
Four controls now cover eventual absence, a surviving descendant requiring KILL,
persistent live-leader denial and continued denial after leader exit. Existing
genuine-denial controls remain. The actual adverse fixture also now waits for
the descendant's own acknowledgment that its TERM-ignore handler is installed.
This fixture correction accompanies the runtime correction, not a replacement
for race coverage.

The corrected runtime passes100 invocations of the unchanged original fixture,
with the unrelated sentinel preserved and then reaped. All17 collector tests
pass, including actual interruption and the enabled Docker/SIGINT pair. Private
diagnostics retain both original and corrected results. Fresh full verification
and independent review follow; approval/private-feedback completion, final
assembled-dev capture, public delivery and actual owner QA remain separate.

Fresh source5ef89a6 subsequently passes989 tests/6 skips, including the enabled
real Docker checks. Independent Spec review finds no runtime defect; Standards
review requires the central intake above. Its record correction/review and
exact-head shared CI remain before readiness. No protected-main retry occurred.

Exact source27291722b10f9db9cfef73237812bc9383960cf5 shared CI42232842207 subsequently passes987 Python tests/8 skips and10 browser tests. TK-002 native close retains the shorthand proof and original receipt bytes: source5ef89a6 is the989/6 local run; source272 is the987/8 plus10 browser CI run. Current record checks/CI, TK-003 implementation, main delivery and owner QA remain separate.
