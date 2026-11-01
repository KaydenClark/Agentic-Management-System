---
type: project
status: active
sensitivity: normal
knowledge_role: derived
provenance:
  - Kayden's shared CI VM instruction, 2026-11-01
source_paths:
  - .github/workflows/python-tests.yml
  - .github/workflows/site-build.yml
  - RUNBOOK.md
last_verified: 2026-11-01
---

# Shared CI

## Owner intent

On 2026-11-01, Kayden requested: "The AMS needs to be self hosting its CIs
on our CI VM that we use for all of our projects". This authorizes moving
AMS's existing CI checks onto the existing shared VM. It does not establish
Spec acceptance, Human QA or website deployment.

## Operation

The [Runbook](../../RUNBOOK.md#shared-ci-vm) owns operation and prerequisites.
The [Python workflow](../../.github/workflows/python-tests.yml) and
[site workflow](../../.github/workflows/site-build.yml) own job routing.
Both select `self-hosted`, `Linux`, `ARM64` and `servitor`; a dedicated AMS
runner service supplies that capacity. Public fork PRs require inspection
before their changes are brought onto an internal branch to execute on the VM.

## History

- 2026-11-01: Captured the owner's shared-VM requirement and routed its
  implementation and operating prerequisites to the workflows and Runbook.
