# Vercel adapter artifact layout blocks protected review coverage

**Disposition:** accepted-open, existing S-003 ownership; no new owner preference.
**Source:** dev `40acb3a491a55599e5b1f00fd92a27315739a4a9`, after PR178.
**Deployment:** `dpl_3U2SoEgLBFPcTaduX2u4Qnr2DX3k`, immutable origin `https://agentic-management-system-site-ctewgjcvo.vercel.app`.
**Observed state:** ERROR, `BUILD_UTILS_SPAWN_1`, build step.

## Observations

Authenticated deployment metadata and build events identify that exact source.
Next16.4.3 compiles and generates51 static outputs, then runs Vercel's
`onBuildComplete` hook. The subsequent npm postbuild inventory fails with
`Page inventory: route manifest/artifact coverage differs` in `readBuild`.
Source CI is green; it did not exercise this deployed artifact layout.

The unchanged source independently builds through S-005's credential-free
isolated Docker collector:50 public routes including39 skill articles and
visitor404, only internal global-error excluded, owned cleanup verified.
That ordinary-layout build cannot supply protected deployment evidence.

## Reproduction and diagnosis

A separate diagnostic fixture used the frozen40ac product files plus a named
no-op CommonJS adapter outside the product sources. The only activation was
`NEXT_ADAPTER_PATH` pointing to that fixture. It used the same approved immutable
Node image, no credentials/public service configuration, public package
acquisition followed by disconnected build networking, and owned cleanup.
This is a diagnostic build, not a claim of a successful40ac deployment.

Next logs the diagnostic adapter hook and the unchanged inventory reproduces
the same postbuild refusal. Observed HTML counts:

| Build layout | HTML artifacts |
|---|---:|
| `server/app` | 0 |
| `server/route-cache/APP_PAGE` | 51 |

The scoped tree includes logical root, RSI, skills and visitor404 plus the
internal global-error. Its filenames are bound to route-source hashes and
normalized pathnames. Raw build output, manifests and relative artifact lists
remain private diagnostic evidence; no actual owner action or Board write ran.

Independent Astra investigation supplied primary-source diagnosis only, with
no implementation. Next16.4.3 enables scoped build artifacts for adapter builds
and writes HTML using the route cache key:
[writer](https://github.com/vercel/next.js/blob/v16.4.3/packages/next/src/export/worker.ts),
[key](https://github.com/vercel/next.js/blob/v16.4.3/packages/next/src/server/lib/route-cache-key.ts),
[adapter resolver](https://github.com/vercel/next.js/blob/v16.4.3/packages/next/src/build/adapter/build-complete.ts).
The deployed directory listing itself was not exposed by the Git-deployment API;
the isolated adapter reproduction establishes the relevant layout mismatch.

## Existing owner and bounded correction

S-003/TK-002Z, claimant `codex-s003-inventory`, owns the reader and build wiring on
`Feature/S-003-website-shell-and-ams-orientation`. Preserve its existing closure,
receipts, seven original metadata objects and all provenance/history. Coordinate
the resulting flat inventory with S-005; no competing site implementation was
made by this report's writer.

Resolve both supported artifact layouts from actual manifest-backed route and
source identities. Keep exact coverage and refuse missing, extra or ambiguous
artifacts; visitor404 remains public and only global-error is internal. Keep
explicit current ownership and truthful pending/null provenance. Do not disable
postbuild validation or accept a stale checked-in inventory to pass deployment.
Add scoped-layout adverse fixtures and an actual adapter-enabled build check,
then review, check and deliver through the existing dev route.

Only after the matching protected deployment is READY should S-005 capture
every route, verify source/deployment pins and generate final review cards.
No complete protected coverage, Task completion, Human QA or main promotion is
claimed here.

## Dependency review limits

Separate read-only Standards and Spec reviews of `517184e...e1d8930` found no
material defect in the bounded ordinary-layout inventory/preservation contract.
The Spec reviewer passed10 inventory fixture cases, then stopped executable
review after two archive-harness setup failures: an exclusion pattern retained
an unavailable real-build assertion, then a hash-test archive lacked its helper.
These are retained review harness failures, not evidence of product failure.
Neither review supplied deployed audit or owner QA; the later adapter failure
is a distinct uncovered execution boundary.
