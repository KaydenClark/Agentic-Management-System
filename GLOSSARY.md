# AMS Glossary

> Generated from LLM Workbench v3.2.2.

AMS manages Kayden's agents, workflows, intent capture, skills and AI tools in one RSI loop; these are its shared terms. Definitions follow Kayden's 2026-10-31 instruction and the [research basis](workbench/research/template-research-basis.md).

## Language

### AMS

**AMS**:
Kayden's system for managing agents, workflows, intent capture, skills and AI tools in one RSI loop. It is built on and operates the Workbench while repairing it.

**RSI loop**:
Recursive self-improvement through actual work: observe friction, propose a bounded change, compare outcomes, decide its disposition and examine later use. A loop record does not prove improvement.

**Alignment assessment**:
Application of approved Alignment Check r1 to a named candidate and scope over three assessment runs.

**Alignment Score**:
The percentage of passed applicable checks pooled across all three assessment runs; distinct from fitness level and acceptance.

**Fitness level**:
The r1 classification: Excellent at three passing runs, Stable at two, Functional at one and Broken at none; any Critical failure overrides the count to Broken.

**Improvement attempt**:
One assessed version of an improvement candidate; each candidate has at most three attempts, excluding baseline.

**Workbench**:
The working foundation AMS uses and repairs. AMS also encompasses the system and tool belt that operates above it.

**Intent**:
What the owner wants, with reasons, boundaries and corrections. Retain whether it is confirmed or unresolved.

### Records

**Implementation Task**:
A bounded assigned slice under a Spec, owning execution state and proof.

**Evaluation task**:
A repeatable test case; one attempt at it is a trial. Neither is an implementation assignment.

**Evidence audit**:
A maintained assessment of claims against dated, candidate-specific evidence, preserving reassessment history.

**Improvement record**:
The connection from an observed problem through a hypothesis and comparison to an actual disposition and later-use check.

**Review receipt**:
An actual assessment of a named candidate and scope, recording reviewer involvement, findings and limits.

**Human QA receipt**:
Sourced human judgment of the named experience or candidate. Agent checks cannot supply it.

### Feedback dispositions

A disposition describes how a finding was handled and grants no execution or release authority; without an established one, keep it pending and name the missing owner or evidence.

**diagnostic**:
Names the diagnostic that makes the condition visible, and whether it is implemented or proposed.

**test**:
Names the test that detects the condition, with its actual result or implementation gap.

**repaired**:
Names the implementing revision and its verification. Later-use benefit remains a separate claim.

**declined**:
Names the actual decision source and reason for declining the proposed action.

**accepted-open**:
Names the actual acceptance of follow-up work and its owning Spec. The problem remains open.
