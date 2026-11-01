# AMS site

The public presentation site for the AMS (Spec S-003), a Next.js app deployed on Vercel. Site work goes feature branch -> `dev` -> `main`; only the owner merges `dev` -> `main`.

## Build and test

Node.js 20 or later builds the site; `npm test` needs Node 21 or later (Node 22 is what the checks ran on). From `site/`:

```bash
npm ci
npm run build
npm test
```

`npm test` runs `node --test "tests/**/*.test.mjs"` (Node's built-in runner; the glob is quoted so Node expands it, which needs Node 21 or later). The tests read the prerendered HTML in `.next/server/app/`, so run `npm run build` first and rebuild after each commit: the footer test compares the built SHA with the current commit.

`npm test` is browser-free and takes well under a second. Besides the page tests it runs `tests/hygiene.test.mjs` over every file the site serves (prerendered HTML and RSC in `.next/server/app/`, client JS and CSS in `.next/static/`): no host path (`/home/`, `/Users/`, `C:\Users\`, `file:///` with a drive or host directory), Supabase secret or service-role key, JWT, API token, private key block, email address, reference to the private GPT_OS repository or agent session link; and no HTML or CSS resource (script, `<link>`, image, CSS `url()` or `@import`) loaded from a host other than Supabase or GitHub. The patterns live in `tests/hygiene.mjs`; its planted-fault cases plant into a copy of a built page.

Browser checks (needs Playwright with Chromium installed, resolved with `require("playwright")`; not a site dependency. axe-core is a devDependency and is injected from `node_modules`, never a CDN):

```bash
npm run check:browser                                  # starts `next start` itself
node tests/browser.check.mjs --shots DIR               # also saves qa-<route>-<theme>-<width>.png
node tests/browser.check.mjs --url http://host:port    # check a running server instead
```

`tests/browser.check.mjs` reads every route from the build manifests (plus the not-found page), so a new page is covered without editing the check. Each route is opened at 375 px and 1280 px in light and dark and checked for: no horizontal scroll; an axe-core WCAG 2.x A/AA pass, contrast included (contrast axe cannot decide counts as a failure); Tab reaching every visible control, each with a visible focus indicator; nothing animating, transitioning or smooth-scrolling under `prefers-reduced-motion: reduce`; and every request going to the site, Supabase or GitHub. Requests to other hosts are recorded and aborted, so the check contacts no third party. It also keeps TK-001's home checks (theme follows the system, the toggle overrides and persists, fonts self-hosted) and checks each page's text with scripts disabled. Before the real pass it plants each fault into a live page (low contrast, a too-wide element, focus outlines removed, a control taken out of the tab order, a transition and an animation ignoring reduced motion, an external font) and fails if any check misses its fault. It exits non-zero on any failure.

## Shell

- `app/layout.tsx` wraps every route in `app/shell/Shell.tsx`: header with the theme toggle, reading-order sidebar, the page in `<main>`, and the commit footer. A page renders only its own content.
- `app/nav.ts` is the one reading-order list; order is reading order. Add an entry only for a route that exists.
- `app/theme/tokens.css` is the only file with color, type and spacing values (Color system v2.2 from the owner's Grilling Board Redesign canvas). Everything else uses `var(--token)`; `tests/tokens.test.mjs` enforces it.
- Theme: follows the system; the toggle overrides it and is stored in `localStorage` (`ams-theme`); a first-party inline script in `<head>` reapplies the stored choice before first paint.
- Footer SHA: `next.config.ts` fixes it at build time from `VERCEL_GIT_COMMIT_SHA`, else `git rev-parse HEAD`, else `unknown`.
- Fonts (IBM Plex Sans, IBM Plex Mono, Zilla Slab) are self-hosted through `@fontsource`; the site makes no third-party requests.

## RSI charts (`/rsi`)

The chart page lives in `app/rsi/`. It renders from `seriesViews(rowsBySeries)` in `app/rsi/data.ts`; until S-006's result rows exist it is fed an empty array per series (`app/rsi/fixtures/empty.ts`), so every chart place shows its "no trials recorded yet" state and no number. Its render tests, including planted-fault cases, are `tests/rsi-empty.test.mjs` and run with `npm test`.
