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

This article owns CI operation and prerequisites; the [Runbook](../../RUNBOOK.md#shared-ci-vm) routes here.
The [Python workflow](../../.github/workflows/python-tests.yml) and
[site workflow](../../.github/workflows/site-build.yml) own job routing.
Both select `self-hosted`, `Linux`, `ARM64` and `servitor`; a dedicated AMS
runner service supplies that capacity. Public fork PRs require inspection
before their changes are brought onto an internal branch to execute on the VM.

The AMS account shares neither credentials nor workspaces with other projects.
Its systemd service `workbench-runner-ams` starts with the VM and restarts after
failure. An unavailable VM queues jobs; there is no GitHub-hosted fallback.

The runner cannot use sudo. An administrator provisions Chromium system packages
with `playwright install-deps chromium` when installing/updating Playwright;
the workflow downloads Chromium as the runner account. Keep Supabase keys and
`AMS_LIVE` out of CI. Inspect service state with
`systemctl status workbench-runner-ams` inside the VM. Verify the actual runner
and tested commit in GitHub job details.

## History

- 2026-11-01: Captured the owner's shared-VM requirement and routed its
  implementation and operating prerequisites to the workflows and Runbook.

- 2026-11-01: Preserved operating details here while pruning the Runbook for its 3,000-character limit.
