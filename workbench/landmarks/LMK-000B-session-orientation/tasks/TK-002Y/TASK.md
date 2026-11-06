# TK-002Y - Make Codex sessions open with the RUNBOOK Orientation note

**Task ID:** TK-002Y
**Landmark ID:** LMK-000B
**Slice:** Make Codex sessions open with the RUNBOOK Orientation note
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: LMK-000B What Success Looks Like
**Planned verification:** `ams-orientation` baseline and candidate runs on Codex for all three cases, plus a Claude regression run; read every transcript.

## Authorized slice

Owner: Kayden, 2026-11-06. Codex sessions are to fix the remaining
orientation failure using the RUNBOOK. Background, method and earlier results
are in [Session orientation](../../../../wiki/context-session-orientation.md)
and the [loop report](../../../../feedback/REPORT-context-recovery-before-answer-2026-11-06.md).

The failure is [FAIL-133](../../../../feedback/WORKBENCH_FEEDBACK.md): in 3/3
candidate runs Codex read RUNBOOK and used recorded decisions, but its reply
did not open with the **Orientation** note that RUNBOOK "Get oriented"
requires. Claude passed 3/3 under the same RUNBOOK.

Method: `improve-workbench`, one change at a time, each with a written
prediction and a fresh `ams-orientation` rerun.

1. Diagnose first. Run Codex once with user-level instructions withheld (for
   example, a separate `CODEX_HOME` that keeps only sign-in) to test whether
   the owner's user-level "Lead with the answer" and "Do not force responses
   into rigid templates" rules cause the miss. Record the result either way.
2. Prefer a room-owned fix: AGENTS.md or RUNBOOK.md wording that Codex
   follows. Both must stay within the 3,000-character limit
   (`uv run ams-hygiene`).
3. If only a user-level Codex instruction change works, show the owner the
   exact proposed text and evidence first. That file governs every project,
   so it changes only with the owner's explicit approval in that session.

Exclusions: no change to Claude-side behavior unless the Claude regression
fails; no shared-skill or catalog installation; no other projects.

## Verification and hand-back

Acceptance:

- [ ] Codex candidate: 3/3 cases read RUNBOOK and open with the Orientation
      note, and the notes name real records (read the transcripts).
- [ ] Claude candidate under the same controls still passes 3/3.
- [ ] The diagnosis in step 1 is recorded, including a negative result.
- [ ] Results, the decision and FAIL-133's outcome are appended to the loop
      report and the failure log; the Wiki topic is updated.

Run commands from the repository root. Candidates overlay only changed control
files onto the baseline so later records cannot leak the expected answer:

```bash
uv run ams-orientation run --provider codex --revision 1e139b2
uv run ams-orientation run --provider codex --revision 1e139b2 --overlay AGENTS.md RUNBOOK.md
uv run ams-orientation run --provider claude --revision 1e139b2 --overlay AGENTS.md RUNBOOK.md
```
