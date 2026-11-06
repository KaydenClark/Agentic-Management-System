# Vercel adapter artifact layout blocks protected review coverage

**Disposition:** inventory layout repaired; later source reconciliation below resolves the historical ledger and separate hash-reader findings. Final protected capture remains. No new owner preference.
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

## Delivered inventory repair and remaining utility gap

PR186 delivered source3104402 into dev47e3c88. Both shared workflows passed;
the exact deployment was READY. An independent adapter-enabled build produced
50 public inventory entries from51 scoped HTML artifacts, with all50 canonical
hashes equal to its ordinary-layout build and owned cleanup verified. S-005
then authenticated all50 protected responses at47e3c88 and validated their
source/deployment identities, including populated RSI. These observations
resolve the deployed inventory failure above, not whole-site acceptance.

The separate directory reader remains incomplete. The report at
[PR142's hash-reader review](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4491854021)
was independently reproduced on47e3c88: a synthetic adapter fixture containing
one manifest-bound scoped page returns1 inventory entry but0 pages through
`readBuiltPages` in `site/scripts/page-hash.mjs`. The reader and its printer are
unchanged at devb699f10f4e08a0ea72f2915e0c14c0744385cbcd. Existing S-003
ownership should reconcile artifact enumeration without weakening coverage or
altering canonical content identity. No competing site correction was made.

S-005 hashes actual served bodies directly and does not call that directory
reader. All50 protected47 bodies independently match the site's pure
`contentHash` function and the committed card index. This protects the existing
capture's identities; it does not qualify the separate directory utility.

The independent Standards finding in source310's failure ledger also remains:
nine-column failure rows189/190 follow a three-column alias-table header,
hiding six fields in rendered Markdown. Preserve row/alias bytes and restore
the complete failure-table header through its existing owner.

Dev has advanced after the47 capture. The final owner queue must be regenerated
and read back against one exact assembled READY dev revision, including later
navigation/governance changes. Neither the47 snapshot nor this report claims
that final queue, owner QA, private-feedback completion or main promotion.

## Later source reconciliation

At independently fetched dev `f17dabdc8b82de487f322a9a268e532fe85ad1d2`,
`readBuiltPages` delegates to the shared strict `readPageArtifacts` reader.
The website owner reports delivery through PR195 and closure PR197. The
nine-column failure-table header is also present in the later ledger; the
earlier malformed-header observation is historical. These are source
readbacks, not a new execution claim. Preserve the failed receipts above.
Final capture still requires one exact assembled READY deployment; no owner
QA or main promotion is supplied by these repairs.
