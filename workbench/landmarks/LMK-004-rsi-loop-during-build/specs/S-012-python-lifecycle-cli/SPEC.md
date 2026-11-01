# S-012 - Python lifecycle CLI

**Spec ID:** S-012
**Status:** planned
**Priority:** 4
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** A small Python CLI for the AMS lifecycle, measured against the current Node lifecycle tools as the baseline before it replaces anything.
**Blockers:** S-002
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning once the loop (S-002) can compare versions.

## Intent and authority

The owner decided the AMS runtime and backends are Python, and confirmed that the current Node lifecycle tools run this build and serve as the baseline; the Python CLI is its own Spec, measured against them. Node remains allowed as tooling.

## Outcome

A Python CLI where each command does one action and records stay plain readable files. It replaces a Node lifecycle command only where it does at least as well on the same tasks.

## Why It Matters

Rewriting a working runtime on preference alone is the kind of change the loop exists to test. Measuring against the baseline keeps the switch honest.

## Current Verified State

- The Node lifecycle tools in `workbench/tools/` run the room (`render`, `doctor`, `next`, `show`, `claim`, `close`). No Python CLI exists. The system Python is older than current; Python 3.14.5 is pinned with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Desired Behavior

- A pinned current Python version in the repository: Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).
- A command exists only where it prevents a repeated agent mistake or does deterministic work.
- Read commands use the same words for every kind: `list`, `show`, `search`, `history`, `inspect`.
- Lifecycle behavior equals the baseline's on the same records: refused operations write nothing, the Taskboard regenerates byte-identically, `doctor` fails on a hand-edited board.
- Comparison trials run Python and Node on the same tasks under S-002's safeguards.

## Decisions And Contracts

- No Node command is removed until the comparison shows the Python one is at least as good.
- Records keep their current formats, so either runtime reads them.

## Non-Goals

- Rewriting the site's Next.js tooling.
- New lifecycle features beyond the baseline.

## Dependencies And Blockers

- S-002 (comparison procedure).

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Pin Python and add a `show` command that reads the same records as the Node tool | ready | none | pending |
| TK-002 | `render` with byte-identical Taskboard output and a parity test against Node | ready | TK-001 | pending |
| TK-003 | Comparison trials on the same tasks, rows in Supabase | ready | TK-002 | pending |

### TK-001 - Pinned Python and show

**Stance:** Builder

Proves the pin and read-parity criteria.

### TK-002 - Render parity

**Stance:** Builder

Proves the Taskboard criterion.

### TK-003 - Comparison

**Stance:** Builder

Proves the baseline criterion.

## Acceptance Criteria

- [ ] **Pinned Python.** The repository pins a current Python version and the CLI refuses to run on an older one. *Must fail:* the CLI running on the system 3.9.
- [ ] **Read parity.** `show` gives the same facts as the Node `show` for every record. *Must fail:* a field one reads and the other drops.
- [ ] **Render parity.** Python and Node render byte-identical Taskboards from the same tree. *Must fail:* any byte difference.
- [ ] **Refusals write nothing.** A refused operation leaves the tree unchanged. *Must fail:* a partial write.
- [ ] **Measured against baseline.** Comparison rows exist for both runtimes on the same tasks before any Node command is retired. *Must fail:* a retirement with no rows.

## RSI and website connection

The comparison is a loop round; its rows appear on the charts (S-007).

## Testing Seams

- The CLI run in disposable directories; a parity test running both runtimes on one tree.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-012
node workbench/tools/spec-workbench.mjs render
# Python parity test command named at Task planning
```

## Documentation Impact

- RUNBOOK lists each Python command only once it exists.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

Independent review at the exact commit before any Node command is retired.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: the earlier draft's runtime criteria based on a prototype's verbs and a zero-dependency rule.
- Superseded by: none
