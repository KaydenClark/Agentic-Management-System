// Local browser check for TK-001 (npm run check:browser, after npm run build).
// Starts `next start` on a free port, opens it in Chromium at 375 px and checks,
// in both themes: no horizontal scroll, the theme follows the system, the
// toggle overrides it and the choice persists across reloads, fonts are
// self-hosted, every request stays on the site, and the home text is there
// with scripts disabled. Needs Playwright with Chromium installed; it is not
// part of `npm test` and not a site dependency.
// Usage: node tests/browser-375.check.mjs [--url http://host:port] [--shots DIR]
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { createServer } from 'node:net';
import { join } from 'node:path';
import { siteDir } from './helpers.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const WIDTH = 375;
const GROUND = { light: 'rgb(247, 247, 247)', dark: 'rgb(10, 10, 10)' };

let chromium;
try {
  ({ chromium } = createRequire(import.meta.url)('playwright'));
} catch {
  console.error('check:browser needs Playwright (require("playwright")) with Chromium installed.');
  process.exit(2);
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

const server = opt('--url') ? { url: opt('--url'), stop() {} } : await startServer();
const shots = opt('--shots');
const browser = await chromium.launch();
try {
  const origin = new URL(server.url).origin;
  for (const scheme of ['light', 'dark']) {
    const context = await browser.newContext({ viewport: { width: WIDTH, height: 812 }, colorScheme: scheme });
    const page = await context.newPage();
    const foreign = [];
    page.on('request', (r) => { if (new URL(r.url()).origin !== origin) foreign.push(r.url()); });
    await page.goto(server.url, { waitUntil: 'networkidle' });
    const state = () => page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      ground: getComputedStyle(document.body).backgroundColor,
      attr: document.documentElement.getAttribute('data-theme'),
      stored: localStorage.getItem('ams-theme'),
    }));
    let s = await state();
    check(`${scheme} system: follows system theme`, s.ground === GROUND[scheme] && s.attr === null, `${s.ground}`);
    check(`${scheme} system: no horizontal scroll at ${WIDTH}px`, s.scrollWidth <= WIDTH, `scrollWidth ${s.scrollWidth}`);
    const fonts = await page.evaluate(async () => { await document.fonts.ready; return ['IBM Plex Sans', 'IBM Plex Mono', 'Zilla Slab'].map((f) => [f, [...document.fonts].some((ff) => ff.family.replace(/["']/g, '') === f && ff.status === 'loaded')]); });
    check(`${scheme} system: self-hosted fonts loaded`, fonts.every(([, ok]) => ok), fonts.filter(([, ok]) => !ok).map(([f]) => f).join(', '));
    if (shots) await page.screenshot({ path: join(shots, `home-375-${scheme}.png`), fullPage: true });

    const other = scheme === 'light' ? 'dark' : 'light';
    await page.click('[data-theme-toggle]');
    s = await state();
    check(`${scheme} system: toggle overrides to ${other}`, s.ground === GROUND[other] && s.attr === other && s.stored === other, `${s.ground}, stored ${s.stored}`);
    check(`${other} (toggled): no horizontal scroll at ${WIDTH}px`, s.scrollWidth <= WIDTH, `scrollWidth ${s.scrollWidth}`);
    if (shots) await page.screenshot({ path: join(shots, `home-375-${other}-toggled.png`), fullPage: true });
    await page.reload({ waitUntil: 'networkidle' });
    s = await state();
    check(`${scheme} system: ${other} choice persists after reload`, s.ground === GROUND[other] && s.attr === other, `${s.ground}`);
    check(`${scheme} system: requests stay on the site`, foreign.length === 0, foreign.join(', '));
    await context.close();
  }
  const noJs = await browser.newContext({ viewport: { width: WIDTH, height: 812 }, javaScriptEnabled: false });
  const p = await noJs.newPage();
  await p.goto(server.url);
  const text = await p.textContent('main');
  check('scripts disabled: home text readable', /Agentic Management System/.test(text ?? '') && /agents/.test(text ?? ''));
  await noJs.close();
} finally {
  await browser.close();
  server.stop();
}
const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} browser checks passed`);
process.exit(failed.length ? 1 : 0);
