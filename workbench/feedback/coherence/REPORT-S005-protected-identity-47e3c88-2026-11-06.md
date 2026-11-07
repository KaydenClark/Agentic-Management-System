# Protected HTML deployment identity compatibility

- Canonical occurrence: FAIL-191; owner S-005/TK-001, existing Servitor writer.
- Inspected source: `f0fc830b393c7ad08e36e179ae2d962a636e0941`, `protected_pages._Identity`.
- Actual captured source: `47e3c8804c6b9434a945588492d22c28ef9cb439`.
- Actual deployment: `dpl_8iTY4Lk2cmC9tbFixJZ1KJKZYf5j`, READY.
- Observation completed `2026-11-06T11:24:09Z`; capture-manifest SHA-256 `d24dc70eb443858bb9c62e627515a6bf066d0015a1365bb9b1bb2ca590f8784e`.
- Disposition: routed to existing writer; repair pending. No collector or card mutation was performed by this reporter.

## Actual finding

Authenticated HTTP capture contains all50 public surfaces:49 normal200 responses and one visitor404, including39 skill articles. Every full source footer and deployment marker matches the pins above. Exact raw-body hashes match the private capture manifest; total UTF-8 body length is2,215,684 bytes. The bodies and any access material remain private.

All50 actual Next16 HTML documents have the native identity shape `<html data-dpl-id="dpl_8iTY4Lk2cmC9tbFixJZ1KJKZYf5j">`. None supplies an asset `?dpl=` identity. Read-only execution of the exact inspected parser finds50 correct source footers and zero deployment identities. The current strict collector would therefore refuse this genuine capture. This is a producer/consumer compatibility finding, not missing deployment provenance or authority to bypass validation.

## Narrow existing-writer correction

Recognize the native html-root identity without an arbitrary-text or weak fallback. Retain trusted outer source, deployment and origin pins, exact public route/kind/status coverage, raw-body hashes and content identity. Reject missing, conflicting or mixed markers, including disagreement between native and legacy representations. Retest the corrected exact candidate against the trusted immutable artifact through the existing writer's procedure.

These derived observations are a handoff, not a self-authenticating protected manifest. There are no competing collector/card writes, fabricated approvals or wider rollout. The captured source47 is not proof for later dev, and no corrected S005 result is claimed.
