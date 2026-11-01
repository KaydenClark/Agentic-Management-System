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

Optional browser check at 375 px in both themes (needs Playwright with Chromium installed; not a site dependency):

```bash
npm run check:browser            # starts `next start` itself
node tests/browser-375.check.mjs --shots /tmp/shots   # also saves screenshots
```

## Shell

- `app/layout.tsx` wraps every route in `app/shell/Shell.tsx`: header with the theme toggle, reading-order sidebar, the page in `<main>`, and the commit footer. A page renders only its own content.
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
