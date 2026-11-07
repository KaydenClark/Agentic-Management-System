# TK-003I - An opted-in Codex hook records an explicit skill request

**Task ID:** TK-003I
**Landmark ID:** LMK-004
**Slice:** An opted-in Codex hook records an explicit skill request
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Optional participation
**Planned verification:** Exercise the supported hook JSON with public synthetic inputs and the exact observer candidate.
**Claimed by:** codex-rsi-host
**Current claimant:** codex-rsi-host

## Assignment

Use the checked TK-003E observer interface at ede79bbc. Implement the optional Codex adapter for explicit skill request and resumption capture from supported hook inputs. Document a project-local opt-in that preserves existing hooks. Reconcile the existing Stop hook. Keep only derived skill and stable identities in the observer, no prompt text, credentials or full transcript. Take completion and loaded/use evidence from a supported Workbench signal, never infer them from a hook event alone. Exercise local request/replay/disabled/ambiguous/malformed inputs. Keep the actual Servitor hook trust and native startup/worker proof in TK-003H.

## Acceptance

- [ ] Supported explicit input creates one observer request, replays safely and adds no record for an incidental mention or disabled project.
- [ ] A turn/session end does not mark the task completed or claim skill use. The optional setup preserves existing hooks.
- [ ] No live config changes, model calls, secret access or hosted writes are required to verify the adapter component.

Workspace baseline sha256:91cee65b7ee261d02fa9783472d3648b6876533c89d13ff6506761380f84423b

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/servitor-rsi-host | ce9ebed18e48ccf7a3bac05c3034d552ac7a73b3 | none | 0 | Product candidate ce9ebed: focused synthetic CLI tests passed 4/4, covering explicit request, immutable replay, resume no-op, privacy, disabled/ambiguous/malformed input, wrong project and outbox failure. Standalone full pytest without loopback permission stopped at first socket bind PermissionError after 363 passed and two skipped; rerun with scoped loopback access is in progress. | Added non-installed Codex hook example and optional project opt-in instructions; existing Stop hook and live configuration were not changed. | Native hook trust, actual host delivery and startup/worker proof remain for TK-003H; no model call, installed hook, hosted write, push or merge. Full Python suite remains pending. | a49e7ac5b4c0348fce78fc3cb2c516812890c366c32c28c98f68e5ce35bb148c |
