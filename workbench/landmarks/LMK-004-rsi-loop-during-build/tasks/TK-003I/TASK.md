# TK-003I - An opted-in Codex hook records an explicit skill request

**Task ID:** TK-003I
**Landmark ID:** LMK-004
**Slice:** An opted-in Codex hook records an explicit skill request
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Optional participation
**Planned verification:** Exercise the supported hook JSON with public synthetic inputs and the exact observer candidate.

## Assignment

Use the checked TK-003E observer interface at ede79bbc. Implement the optional Codex adapter for explicit skill request and resumption capture from supported hook inputs. Document a project-local opt-in that preserves existing hooks. Reconcile the existing Stop hook. Keep only derived skill and stable identities in the observer, no prompt text, credentials or full transcript. Take completion and loaded/use evidence from a supported Workbench signal, never infer them from a hook event alone. Exercise local request/replay/disabled/ambiguous/malformed inputs. Keep the actual Servitor hook trust and native startup/worker proof in TK-003H.

## Acceptance

- [ ] Supported explicit input creates one observer request, replays safely and adds no record for an incidental mention or disabled project.
- [ ] A turn/session end does not mark the task completed or claim skill use. The optional setup preserves existing hooks.
- [ ] No live config changes, model calls, secret access or hosted writes are required to verify the adapter component.
