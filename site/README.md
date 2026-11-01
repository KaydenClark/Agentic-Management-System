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

## RSI charts (`/rsi`)

The chart page lives in `app/rsi/`. It renders from `seriesViews(rowsBySeries)` in `app/rsi/data.ts`; until S-006's result rows exist it is fed an empty array per series (`app/rsi/fixtures/empty.ts`), so every chart place shows its "no trials recorded yet" state and no number. Its render tests, including planted-fault cases, are `tests/rsi-empty.test.mjs` and run with `npm test`.
