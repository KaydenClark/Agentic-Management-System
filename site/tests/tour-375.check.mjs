// Local browser check for the tour pages (S-003 TK-002), after npm run build.
// Starts `next start` on a free port, opens each page in the reading order in
// Chromium at 375 px in both themes and checks: no horizontal scroll, the
// page's back/forward links are visible, and every request stays on the site.
// Also checks the tour text is readable with scripts disabled. Needs
// Playwright with Chromium installed; not part of `npm test`.
// Usage: node tests/tour-375.check.mjs [--url http://host:port] [--shots DIR]
// Screenshots are named tour-<page>-<theme>-375.png.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { createServer } from 'node:net';
import { join } from 'node:path';
import { siteDir } from './helpers.mjs';
import { READING_ORDER } from './tour-helpers.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const WIDTH = 375;

let chromium;
try {
  ({ chromium } = createRequire(import.meta.url)('playwright'));
} catch {
  console.error('This check needs Playwright (require("playwright")) with Chromium installed.');
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
const slug = (href) => (href === '/' ? 'home' : href.slice(1));

const server = opt('--url') ? { url: opt('--url'), stop() {} } : await startServer();
const shots = opt('--shots');
const browser = await chromium.launch();
try {
  const origin = new URL(server.url).origin;
  for (const theme of ['light', 'dark']) {
    const context = await browser.newContext({ viewport: { width: WIDTH, height: 812 }, colorScheme: theme });
    const page = await context.newPage();
    const foreign = [];
    page.on('request', (r) => { if (new URL(r.url()).origin !== origin) foreign.push(r.url()); });
    for (const href of READING_ORDER) {
      await page.goto(server.url + href, { waitUntil: 'networkidle' });
      const s = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        order: [...document.querySelectorAll('nav[aria-label="Page order"] a')].filter((a) => a.getBoundingClientRect().width > 0).length,
      }));
      check(`${theme} ${href}: no horizontal scroll at ${WIDTH}px`, s.scrollWidth <= WIDTH, `scrollWidth ${s.scrollWidth}`);
      check(`${theme} ${href}: back/forward links visible`, s.order >= 1, `${s.order} link(s)`);
      if (shots) await page.screenshot({ path: join(shots, `tour-${slug(href)}-${theme}-375.png`), fullPage: true });
    }
    check(`${theme}: requests stay on the site`, foreign.length === 0, foreign.join(', '));
    await context.close();
  }
  const noJs = await browser.newContext({ viewport: { width: WIDTH, height: 812 }, javaScriptEnabled: false });
  const p = await noJs.newPage();
  for (const href of ['/start', '/how-it-works']) {
    await p.goto(server.url + href);
    const text = (await p.textContent('main')) ?? '';
    check(`scripts disabled: ${href} text readable`, text.split(/\s+/).length > 250);
  }
  await noJs.close();
} finally {
  await browser.close();
  server.stop();
}
const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} tour browser checks passed`);
process.exit(failed.length ? 1 : 0);
