# S-010 - Governance stack and flow charts

**Spec ID:** S-010
**Status:** active
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Site pages explaining the governance stack and drawing the AMS workflows as diagrams that match the code they depict.
**Blockers:** S-003 site shell content exists at checked dev commit `259b7a905639cc6ab621220b160fc813c5bc43f1`; whole-Spec completion remains separate.
**Confirmation:** [JOT-8634622a-512b-44d9-9b99-0f973c450356](../../../../wiki/context-website-presentation.md)
**Execution approval:** [JOT-8634622a-512b-44d9-9b99-0f973c450356](../../../../wiki/context-website-presentation.md)
**Next gate:** Complete TK-002.

## Intent and authority

The owner's confirmed site scope includes the governance stack and the flow charts. Pictures must show the real thing: a diagram that disagrees with the code misleads.

## Outcome

A reader understands who decides what, what a check may block, and how work moves from an idea to a delivered result, from diagrams that stay true as the code changes.

## Why It Matters

The governance stack is what makes the AMS auditable rather than a set of prompts. Diagrams that drift from the code would undercut the site's main claim.

## Current Verified State

- TK-001 delivered the Task lifecycle chart on the Spec branch; TK-002 through TK-004 and assembled acceptance remain open.
- At assembled candidate `987c3314b26764772b7331d500e30c1c3b8a3ebc` (including checked `dev` `6cdb647d2d415a8400d1d26cad2614b492c03926`), site build and 282 site tests passed; the RSI browser integration check passed. The Task chart and audited runtime sources are byte-identical to `d774b5113d0e19bc3e35a7467ce03a321a9eb948`, where shared CI passed Python and site jobs and earlier browser and Python checks apply to that unchanged scope. This does not establish independent Review, Human QA or delivery.

History: [S-010 history](../../../../wiki/history/S-010.md).

## Desired Behavior

- **Governance stack page.** In plain words with one worked example each: the authority order (platform safety, the owner's current request, `AGENTS.md`, the assigned Spec or Task); confirmation versus approval; a check blocks only what it evaluates; the planes as roles a claim plays in one operation, never folders.
- **Flow charts.** The Spec lifecycle, the Task lifecycle, idea to delivered (Explore, Promote, Prepare, Journey, Judge, Complete), the review-and-return loop, the branch model (feature -> `main`; site via `dev`), the three orchestrators and the RSI round.
- Lifecycle diagrams are generated from, or tested against, the status sets and transitions in the code at the build commit.

## Decisions And Contracts

- A diagram showing a status the code does not have is a defect.
- The planes are claim roles, never directories.

## Non-Goals

- Interactive editing of records from a diagram.
- Third-party diagram services.

## Dependencies And Blockers

- S-003 (site shell). The diagrams follow whichever runtime is current: today the Node lifecycle tools; later the Python CLI if S-012 replaces them.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

### TK-001 - First generated diagram

**Stance:** Builder

Proves the match-the-code criterion on one lifecycle.

### TK-002 - Remaining lifecycles

**Stance:** Builder

Extends the drift test.

### TK-003 - Governance page

**Stance:** Builder

Proves the planes and authority criteria.

### TK-004 - Process diagrams

**Stance:** Builder

Completes the chart inventory.

## Acceptance Criteria

- [ ] **Diagrams match the code.** A test compares each lifecycle diagram's states and transitions with the code at the build commit. *Must fail:* a diagram showing a status the code lacks, or missing one it has.
- [ ] **Planes as roles.** The governance diagram shows one claim moving between roles in one operation. *Must fail:* boxes labeled as folders.
- [ ] **Worked examples.** Each governance idea has a plain-language opener and one example. *Must fail:* a definition that uses an undefined term.
- [ ] **Chart inventory.** Every chart listed above exists. *Must fail:* a missing chart or a placeholder.
- [ ] **Readable everywhere.** Diagrams are legible at 375 px and in both themes. *Check:* browser screenshots.

## RSI and website connection

The RSI round diagram matches the loop specified in S-002.

## Testing Seams

- A drift test reading the lifecycle status sets from the code; rendered output in a browser.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-010
# site test command named at Task planning
```

## Documentation Impact

- The glossary links the governance page for each governance term.

## Review and Human QA

The owner reviews the pages through their Grill Board cards (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
