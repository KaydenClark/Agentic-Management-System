// Browser checks over the built site (npm run check:browser, after npm run
// build). Starts `next start` on a free port and opens every route the build
// produces (read from .next/app-path-routes-manifest.json, so new pages are
// covered without editing this file), plus the not-found page, in Chromium at
// 375 px and 1280 px in both themes. For each it checks:
//   - no horizontal scroll;
//   - an automated WCAG 2.x A/AA pass with axe-core (contrast included),
//     injected from node_modules, never a CDN;
//   - keyboard: Tab reaches every visible interactive element and each one
//     shows a focus indicator: a visible (non-transparent) outline,
//     box-shadow, border or background that differs from its unfocused look;
//   - reduced motion: with prefers-reduced-motion: reduce, nothing animates
//     or transitions and scrolling is not smooth;
//   - network: every request goes to the site, Supabase or GitHub. Requests
//     to any other host are recorded and aborted, so the check itself never
//     contacts a third party.
// Plus TK-001's home checks (theme follows the system, toggle overrides and
// persists, fonts self-hosted) and page text readable with scripts disabled.
// Before the real pass it plants each fault into a live page and requires the
// matching check to fail, so a check that cannot fail is reported.
// Needs Playwright with Chromium installed (not a site dependency) and the
// axe-core devDependency. Not part of `npm test`.
// Usage: node tests/browser.check.mjs [--url http://host:port] [--shots DIR]
import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { createServer } from 'node:net';
import { join } from 'node:path';
import { siteDir } from './helpers.mjs';
import { allowedHost } from './hygiene.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const WIDTHS = [375, 1280];
const HEIGHT = 812;
const THEMES = ['light', 'dark'];
const GROUND = { light: 'rgb(247, 247, 247)', dark: 'rgb(10, 10, 10)' };
const AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const NOT_FOUND_PATH = '/__qa-no-such-page__';

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.error('check:browser needs Playwright (require("playwright")) with Chromium installed.');
  process.exit(2);
}
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// Every page route the build produced. Next's own error fallback is not a
// page; the not-found page is visited at an address that does not exist.
function builtRoutes() {
  const manifest = JSON.parse(readFileSync(join(siteDir, '.next', 'app-path-routes-manifest.json'), 'utf8'));
  const prerendered = Object.keys(JSON.parse(readFileSync(join(siteDir, '.next', 'prerender-manifest.json'), 'utf8')).routes);
  const routes = [];
  for (const [entry, route] of Object.entries(manifest)) {
    if (!entry.endsWith('/page') || route === '/_global-error') continue;
    if (route === '/_not-found') { routes.push({ name: 'not-found', path: NOT_FOUND_PATH }); continue; }
    if (!route.includes('[')) { routes.push({ name: route === '/' ? 'home' : route.slice(1).replace(/\//g, '-'), path: route }); continue; }
    // A dynamic route is checked at each prerendered path; with none, it
    // cannot be checked and that is a failure, not a silent skip.
    const pattern = new RegExp(`^${route.replace(/\[\[?\.{0,3}[^\]]+\]\]?/g, '[^/]+(?:/[^/]+)*')}$`);
    const paths = prerendered.filter((p) => pattern.test(p));
    if (!paths.length) routes.push({ name: route, path: null });
    for (const p of paths) routes.push({ name: p.slice(1).replace(/\//g, '-'), path: p });
  }
  return routes;
}

const freePort = () => new Promise((resolve) => {
  const srv = createServer().listen(0, () => { const { port } = srv.address(); srv.close(() => resolve(port)); });
});

async function startServer() {
  const port = await freePort();
  const child = spawn(join(siteDir, 'node_modules', '.bin', 'next'), ['start', '-p', String(port)], { cwd: siteDir, stdio: ['ignore', 'pipe', 'inherit'] });
  await new Promise((resolve, reject) => {
    child.stdout.on('data', (d) => { if (/ready|started|Local:/i.test(String(d))) resolve(); });
    child.on('exit', (code) => reject(new Error(`next start exited with ${code}`)));
    setTimeout(() => reject(new Error('next start did not become ready in 30 s')), 30000);
  });
  return { url: `http://localhost:${port}`, stop: () => child.kill() };
}

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); console.log(`${ok ? 'ok    ' : 'FAIL  '} ${name}${detail ? ` (${detail})` : ''}`); };

// --- Detectors. Each returns a list of problems; empty means pass. ---

async function horizontalScroll(page) {
  const { scrollWidth, clientWidth } = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
  return scrollWidth > clientWidth ? [`scrollWidth ${scrollWidth} > ${clientWidth}`] : [];
}

async function axeProblems(page) {
  if (!(await page.evaluate(() => typeof window.axe === 'object'))) await page.addScriptTag({ content: axeSource });
  const res = await page.evaluate((tags) => window.axe.run(document, { runOnly: { type: 'tag', values: tags }, resultTypes: ['violations', 'incomplete'] }), AXE_TAGS);
  const describe = (r) => `${r.id}: ${r.nodes.slice(0, 3).map((n) => `${n.target.join(' ')}${n.any?.[0]?.message ? ` [${n.any[0].message}]` : ''}`).join('; ')}${r.nodes.length > 3 ? `; +${r.nodes.length - 3} more` : ''}`;
  // Contrast axe could not decide (e.g. text over an image) is treated as a
  // failure: AA must be shown, not assumed.
  return [
    ...res.violations.map(describe),
    ...res.incomplete.filter((r) => r.id === 'color-contrast').map((r) => `undecided ${describe(r)}`),
  ];
}

async function keyboardProblems(page) {
  await page.evaluate(() => { document.activeElement?.blur?.(); window.scrollTo(0, 0); });
  const total = await page.evaluate(() => {
    const native = 'a[href], area[href], button, input:not([type="hidden"]), select, textarea, summary, iframe, audio[controls], video[controls], [contenteditable=""], [contenteditable="true"]';
    const visible = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
    const els = [...document.querySelectorAll(`${native}, [tabindex]`)]
      .filter((el) => !el.disabled && !el.closest('[inert]') && visible(el))
      // tabindex="-1" on a non-interactive element (a skip-link target) is a
      // focus target, not a control.
      .filter((el) => el.matches(native) || el.tabIndex >= 0);
    els.forEach((el, i) => el.setAttribute('data-qa-i', String(i)));
    // The look of a control: what a focus indicator can change. Recorded for
    // every control now, while nothing is focused, as its baseline.
    window.__qaLook = (el) => {
      const s = getComputedStyle(el);
      const sides = ['Top', 'Right', 'Bottom', 'Left'];
      return {
        outline: { style: s.outlineStyle, width: parseFloat(s.outlineWidth) || 0, color: s.outlineColor },
        shadow: s.boxShadow,
        border: sides.map((d) => `${s[`border${d}Style`]} ${parseFloat(s[`border${d}Width`]) || 0} ${s[`border${d}Color`]}`),
        background: s.backgroundColor,
      };
    };
    window.__qaBaseline = Object.fromEntries(els.map((el, i) => [String(i), window.__qaLook(el)]));
    return els.length;
  });
  const reached = new Set();
  const noIndicator = [];
  for (let step = 0; step < total * 2 + 5; step += 1) {
    await page.keyboard.press('Tab');
    const f = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const i = el.getAttribute('data-qa-i');
      // Alpha of a computed color: 0 for transparent or a zero-alpha value.
      const alpha = (c) => {
        if (!c || c === 'transparent') return 0;
        const slash = c.match(/\/\s*([\d.]+)(%?)\s*\)\s*$/);
        if (slash) return parseFloat(slash[1]) / (slash[2] ? 100 : 1);
        const rgba = c.match(/^rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\s*\)$/);
        return rgba ? parseFloat(rgba[1]) : 1;
      };
      const colorsIn = (v) => v.match(/(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\([^)]*\)|transparent/g) ?? [];
      const now = window.__qaLook(el);
      const was = window.__qaBaseline[i] ?? { outline: { style: 'none', width: 0, color: '' }, shadow: 'none', border: [], background: '' };
      const outlineSeen = (o) => o.style !== 'none' && o.width > 0 && alpha(o.color) > 0;
      const shadowSeen = (v) => v !== 'none' && colorsIn(v).some((c) => alpha(c) > 0);
      const changes = [];
      if (outlineSeen(now.outline) && JSON.stringify(now.outline) !== JSON.stringify(was.outline)) changes.push('outline');
      if (shadowSeen(now.shadow) && now.shadow !== was.shadow) changes.push('box-shadow');
      if (now.border.some((b, k) => b !== was.border[k] && !b.startsWith('none') && parseFloat(b.split(' ')[1]) > 0 && alpha(b.split(' ').slice(2).join(' ')) > 0)) changes.push('border');
      if (now.background !== was.background && alpha(now.background) > 0) changes.push('background');
      return { i, label: `${el.tagName.toLowerCase()}${el.className ? `.${String(el.className).split(' ')[0]}` : ''} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30)}"`, indicator: changes.length > 0 };
    });
    if (!f) break;
    if (f.i !== null && reached.has(f.i)) break;
    if (f.i !== null) reached.add(f.i);
    if (!f.indicator) noIndicator.push(f.label);
  }
  const missed = await page.evaluate((got) => [...document.querySelectorAll('[data-qa-i]')]
    .filter((el) => !got.includes(el.getAttribute('data-qa-i')))
    .map((el) => `${el.tagName.toLowerCase()} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30)}"`), [...reached]);
  return [
    ...(total === 0 ? ['no interactive element found'] : []),
    ...missed.map((m) => `not reachable by Tab: ${m}`),
    ...noIndicator.map((m) => `no visible focus indicator: ${m}`),
  ];
}

async function motionProblems(page) {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const found = await page.evaluate(() => {
    const secs = (v) => Math.max(0, ...v.split(',').map((t) => (t.trim().endsWith('ms') ? parseFloat(t) / 1000 : parseFloat(t)) || 0));
    const out = [];
    if (getComputedStyle(document.documentElement).scrollBehavior === 'smooth') out.push('html: scroll-behavior smooth');
    for (const el of document.querySelectorAll('*')) {
      for (const pseudo of [null, '::before', '::after']) {
        const s = getComputedStyle(el, pseudo);
        const name = `${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? `.${el.className.split(' ')[0]}` : ''}${pseudo ?? ''}`;
        if (s.animationName !== 'none' && secs(s.animationDuration) > 0.01) out.push(`${name}: animation ${s.animationName} ${s.animationDuration}`);
        if (s.transitionProperty !== 'none' && secs(s.transitionDuration) > 0.01) out.push(`${name}: transition ${s.transitionProperty} ${s.transitionDuration}`);
      }
    }
    for (const a of document.getAnimations()) if (a.playState === 'running') out.push(`running animation ${a.animationName ?? a.id ?? ''}`);
    return out;
  });
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  return found;
}

// Records every request; lets the site, data: and blob: through, records and
// aborts anything else (allowed Supabase/GitHub loads are recorded as allowed
// and aborted too: this check browses nothing off the site).
function watchNetwork(page, origin, log) {
  return page.route('**/*', (route) => {
    const url = new URL(route.request().url());
    if (url.origin === origin || url.protocol === 'data:' || url.protocol === 'blob:') return route.continue();
    log.push({ url: url.href, allowed: allowedHost(url.hostname) });
    return route.abort('blockedbyclient');
  });
}
const foreign = (log) => log.filter((r) => !r.allowed).map((r) => r.url);

async function openPage(browser, url, { width, theme, origin }) {
  const context = await browser.newContext({ viewport: { width, height: HEIGHT }, colorScheme: theme });
  const page = await context.newPage();
  const log = [];
  await watchNetwork(page, origin, log);
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  return { context, page, log };
}

// --- Planted faults: each must make its detector fail. ---

async function selfTest(browser, server, origin) {
  const plants = [
    ['a low-contrast color', axeProblems, (p) => p.addStyleTag({ content: 'main p { color: #c4c4c4 !important; }' }), (x) => x.some((m) => m.startsWith('color-contrast'))],
    ['an element wider than the viewport', horizontalScroll, (p) => p.evaluate(() => { const d = document.createElement('div'); d.style.width = '600px'; d.style.height = '1px'; document.querySelector('main').append(d); })],
    ['focus outlines removed', keyboardProblems, (p) => p.addStyleTag({ content: '*:focus, *:focus-visible { outline: none !important; box-shadow: none !important; }' }), (x) => x.some((m) => m.startsWith('no visible focus'))],
    ['a transparent focus outline', keyboardProblems, (p) => p.addStyleTag({ content: '*:focus, *:focus-visible { outline-color: transparent !important; }' }), (x) => x.some((m) => m.startsWith('no visible focus'))],
    ['a decorative box-shadow that does not change on focus', keyboardProblems, (p) => p.addStyleTag({ content: '*:focus, *:focus-visible { outline: none !important; } a, button { box-shadow: 0 0 0 2px #000 !important; }' }), (x) => x.some((m) => m.startsWith('no visible focus'))],
    ['a control taken out of the tab order', keyboardProblems, (p) => p.evaluate(() => { const b = document.createElement('button'); b.textContent = 'Planted'; b.tabIndex = -1; document.querySelector('main').append(b); }), (x) => x.some((m) => m.startsWith('not reachable'))],
    ['a transition ignoring reduced motion', motionProblems, (p) => p.addStyleTag({ content: '.card, h1 { transition: transform 1s ease; }' })],
    ['an animation ignoring reduced motion', motionProblems, (p) => p.addStyleTag({ content: '@keyframes qa-spin { to { transform: rotate(1turn); } } h1 { animation: qa-spin 2s infinite; }' })],
  ];
  for (const [what, detector, plant, matches = (x) => x.length > 0] of plants) {
    const { context, page } = await openPage(browser, server.url, { width: 375, theme: 'light', origin });
    const before = await detector(page);
    await plant(page);
    const after = await detector(page);
    check(`self-test: planted ${what} is caught`, before.length === 0 && matches(after), after.slice(0, 2).join(' | ') || 'not caught');
    await context.close();
  }
  // An external font: the request must be seen and blocked.
  const { context, page, log } = await openPage(browser, server.url, { width: 375, theme: 'light', origin });
  const before = foreign(log).length;
  await page.addStyleTag({ content: '@font-face { font-family: "QA Planted"; src: url(https://fonts.gstatic.com/s/qa/planted.woff2) format("woff2"); } h1 { font-family: "QA Planted"; }' });
  await page.evaluate(() => document.fonts.load('16px "QA Planted"').catch(() => {}));
  await page.waitForTimeout(200);
  check('self-test: planted external font request is caught', before === 0 && foreign(log).length > 0, foreign(log).join(', ') || 'not caught');
  await context.close();
}

// --- The pass over every route. ---

const server = opt('--url') ? { url: opt('--url'), stop() {} } : await startServer();
const shots = opt('--shots');
const browser = await chromium.launch();
try {
  const origin = new URL(server.url).origin;
  await selfTest(browser, server, origin);

  const routes = builtRoutes();
  check('routes: every built route has a path to check', routes.every((r) => r.path), routes.map((r) => r.path ?? `${r.name} (dynamic, nothing prerendered)`).join(', '));
  for (const route of routes.filter((r) => r.path)) {
    for (const theme of THEMES) {
      for (const width of WIDTHS) {
        const tag = `${route.name} ${theme} ${width}px`;
        const { context, page, log } = await openPage(browser, `${server.url}${route.path}`, { width, theme, origin });
        const ground = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
        check(`${tag}: renders in the ${theme} theme`, ground === GROUND[theme], ground);
        let p = await horizontalScroll(page);
        check(`${tag}: no horizontal scroll`, !p.length, p.join('; '));
        p = await axeProblems(page);
        check(`${tag}: axe WCAG A/AA (contrast included)`, !p.length, p.join(' | '));
        p = await keyboardProblems(page);
        check(`${tag}: keyboard reaches every control with a visible focus`, !p.length, p.join(' | '));
        p = await motionProblems(page);
        check(`${tag}: reduced motion respected`, !p.length, p.join(' | '));
        if (shots) {
          await page.evaluate(() => { document.activeElement?.blur?.(); window.scrollTo(0, 0); });
          await page.screenshot({ path: join(shots, `qa-${route.name}-${theme}-${width}.png`), fullPage: true });
        }
        check(`${tag}: requests only to the site, Supabase or GitHub`, !foreign(log).length, foreign(log).join(', '));
        await context.close();
      }
    }
    const noJs = await browser.newContext({ viewport: { width: WIDTHS[0], height: HEIGHT }, javaScriptEnabled: false });
    const p = await noJs.newPage();
    await p.goto(`${server.url}${route.path}`);
    const text = (await p.textContent('main')) ?? '';
    check(`${route.name}: page text readable with scripts disabled`, text.trim().length > 40 && (route.name !== 'home' || /Agentic Management System/.test(text)), `${text.trim().length} chars`);
    await noJs.close();
  }

  // TK-001's home checks: system theme, toggle override and persistence,
  // self-hosted fonts.
  for (const scheme of THEMES) {
    const { context, page, log } = await openPage(browser, server.url, { width: WIDTHS[0], theme: scheme, origin });
    const state = () => page.evaluate(() => ({
      ground: getComputedStyle(document.body).backgroundColor,
      attr: document.documentElement.getAttribute('data-theme'),
      stored: localStorage.getItem('ams-theme'),
    }));
    let s = await state();
    check(`home ${scheme} system: follows system theme`, s.ground === GROUND[scheme] && s.attr === null, s.ground);
    const fonts = await page.evaluate(async () => { await document.fonts.ready; return ['IBM Plex Sans', 'IBM Plex Mono', 'Zilla Slab'].map((f) => [f, [...document.fonts].some((ff) => ff.family.replace(/["']/g, '') === f && ff.status === 'loaded')]); });
    check(`home ${scheme} system: self-hosted fonts loaded`, fonts.every(([, ok]) => ok), fonts.filter(([, ok]) => !ok).map(([f]) => f).join(', '));
    const other = scheme === 'light' ? 'dark' : 'light';
    await page.click('[data-theme-toggle]');
    s = await state();
    check(`home ${scheme} system: toggle overrides to ${other}`, s.ground === GROUND[other] && s.attr === other && s.stored === other, `${s.ground}, stored ${s.stored}`);
    let p = await horizontalScroll(page);
    check(`home ${other} (toggled): no horizontal scroll at ${WIDTHS[0]}px`, !p.length, p.join('; '));
    p = await axeProblems(page);
    check(`home ${other} (toggled): axe WCAG A/AA (contrast included)`, !p.length, p.join(' | '));
    await page.reload({ waitUntil: 'networkidle' });
    s = await state();
    check(`home ${scheme} system: ${other} choice persists after reload`, s.ground === GROUND[other] && s.attr === other, s.ground);
    check(`home ${scheme} system: requests only to the site, Supabase or GitHub`, !foreign(log).length, foreign(log).join(', '));
    await context.close();
  }
} finally {
  await browser.close();
  server.stop();
}
const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} browser checks passed`);
process.exit(failed.length ? 1 : 0);
