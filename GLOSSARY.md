# AMS Glossary

> Generated from LLM Workbench v3.2.2.

Shared AMS terms; [Blueprint](BLUEPRINT.md) owns the destination.

## Language

### AMS

**AMS**:
A reusable system of workflows, rules, skills and tools through which people capture, develop and record intent with AI, and agents carry that intent into verified outcomes. Its methods can be packaged for anyone to reuse; this project adds RSI to improve them through actual work.

**RSI loop**:
Recursive self-improvement through actual work: observe friction, propose a bounded change, compare outcomes, decide its disposition and examine later use. A loop record proves no improvement.

**Alignment assessment**:
Application of approved Alignment Check r1 to a named candidate and scope over three assessment runs.

**Alignment Score**:
The percentage of passed applicable checks pooled across the three assessment runs; distinct from fitness level and acceptance.

**Fitness level**:
The r1 classification: Excellent at three passing runs, Stable at two, Functional at one and Broken at none; any Critical failure overrides the count to Broken.

**Improvement attempt**:
One assessed version of an improvement candidate; each candidate gets at most three, excluding baseline.

**Workbench**:
The environment where AMS operates, bringing together people, agents, project records, working artifacts and tools.

**Intent**:
What the owner wants, with reasons, boundaries and corrections. Retain whether confirmed or unresolved.

### Records

**Implementation Task**:
A bounded assigned slice under a Spec, owning execution state and proof.

**Evaluation task**:
A repeatable test case; one attempt at it is a trial. Neither is an implementation assignment.

**Evidence audit**:
A maintained assessment of claims against dated, candidate-specific evidence, keeping reassessment history.

**Improvement record**:
The link from an observed problem through hypothesis and comparison to an actual disposition and later-use check.

**Review receipt**:
An actual assessment of a named candidate and scope, recording reviewer involvement, findings and limits.

**Human QA receipt**:
Sourced human judgment of the named experience or candidate. Agent checks cannot supply it.

### Feedback dispositions

A disposition describes how a finding was handled and grants no execution or release authority; without an established one, keep it pending and name the missing owner or evidence.

**diagnostic**:
Names the diagnostic that makes the condition visible and whether it is implemented or proposed.

**test**:
Names the test that detects the condition, with its actual result or implementation gap.

**repaired**:
Names the implementing revision and its verification. Later-use benefit remains a separate claim.

**declined**:
Names the actual decision source and reason for declining the proposed action.

**accepted-open**:
Names the actual acceptance of follow-up work and its owning Spec; the problem remains open.
