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

- `app/layout.tsx` wraps every route in `app/shell/Shell.tsx`: a top bar with the site title, the reading-order links and the theme toggle; the page in `<main>`; and the commit footer. Header, main and footer share one centred `.container` (`--container` in `app/theme/tokens.css`); a wide page adds `.container-wide` (`--container-wide`). A page renders only its own content.
- `app/nav.ts` is the one reading-order list; order is reading order. Add an entry only for a route that exists.
- `app/theme/tokens.css` is the only file with color, type and spacing values (Color system v2.2 from the owner's Grilling Board Redesign canvas). Everything else uses `var(--token)`; `tests/tokens.test.mjs` enforces it.
- Theme: follows the system; the toggle overrides it and is stored in `localStorage` (`ams-theme`); a first-party inline script in `<head>` reapplies the stored choice before first paint.
- Footer SHA: `next.config.ts` fixes it at build time from `VERCEL_GIT_COMMIT_SHA`, else `git rev-parse HEAD`, else `unknown`.
- Fonts (IBM Plex Sans, IBM Plex Mono, Zilla Slab) are self-hosted through `@fontsource`; the site makes no third-party requests.

## Theme token check

The theme block of `app/theme/tokens.css` (light, manual dark, the system-dark `@media` rule and the `.tone`/`.h-*` mixes) is generated from `../grill-board/theme/tokens.json`, the recorded Grill Board theme ([DDR-000Y](../workbench/docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md)), and sits between the `BEGIN theme tokens` and `END theme tokens` markers. To change a color, edit `tokens.json`, then run `npm run tokens:gen` (`node scripts/gen-tokens.mjs --write`; without `--write` it prints the block). `tests/tokens-json.test.mjs` fails `npm test` unless the block equals the generator's output byte for byte, each marker appears once, and nothing outside the markers declares a recorded token or holds a color-like value. Type and spacing tokens are hand-written after the block and are not in `tokens.json`, so they are not compared; `tests/tokens.test.mjs` still keeps every literal inside `tokens.css`. Vercel builds with root directory `site/`, so the check runs in the local `npm test` only.

## Tour pages (`/start`, `/how-it-works`)

- Start here (`app/start/`) and How it works (`app/how-it-works/`) are the first tour pages (S-003 TK-002). Each opens with a `<p data-opener>` plain-language summary; any term from the jargon list in `tests/tour-helpers.mjs` used there must be a `<dfn>` or link to an on-page id or the Glossary. Every claim links the committed record it comes from on GitHub (`blob/dev/...`).
- Owner quotes go in `<figure data-owner-quote>` with a `<blockquote>` and a `<figcaption>` holding the date and a link to the committed record; the test checks the words are verbatim in that file. Quote marks anywhere else in a page body fail the test, so paraphrase without them.
- `app/shell/PageOrder.tsx` puts back and forward links (`rel="prev"`/`rel="next"`) at the end of every page in `app/nav.ts`; a new page gets them by being added to `nav.ts`.
- Tests (`npm test`): `tests/tour-inventory.test.mjs` (pages exist, openers, placeholders, quotes, GitHub links name existing files) and `tests/tour-links.test.mjs` (reading order, back/forward links on every page, no orphan page, internal links resolve). Each runs planted-fault self-tests first.
- Browser check at 375 px, both themes, every page in the reading order: `node tests/tour-375.check.mjs [--shots DIR]` (needs Playwright with Chromium; screenshots are `tour-<page>-<theme>-375.png`).

## RSI charts (`/rsi`)

The chart page lives in `app/rsi/`. It renders from `seriesViews(rowsBySeries)` in `app/rsi/data.ts`; until S-006's result rows exist it is fed an empty array per series (`app/rsi/fixtures/empty.ts`), so every chart place shows its "no trials recorded yet" state and no number. Its render tests, including planted-fault cases, are `tests/rsi-empty.test.mjs` and run with `npm test`.
