// Focused live controls for the native keyboard detector. Build first; pass
// the isolated built site's URL. Faults remain installed throughout detection.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { keyboardProblems } from './keyboard-helpers.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:3188';
const browser = await chromium.launch();
const results = [];
const check = (name, pass, detail) => {
  results.push({ name, pass, detail });
  console.log(`${pass ? 'ok' : 'FAIL'} ${name}: ${JSON.stringify(detail)}`);
};
async function fixture(width = 375, theme = 'light') {
  const context = await browser.newContext({ viewport: { width, height: 812 }, colorScheme: theme });
  const page = await context.newPage();
  await page.goto(`${base}/start`, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: 'html { font-size: 200% !important; }' });
  return { context, page };
}
try {
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await context.newPage();
    await page.goto(`${base}/skills/grilling`, { waitUntil: 'networkidle' });
    const details = page.locator('nav[aria-label="Skills wiki"] details').first();
    const link = details.locator('a').first();
    const hidden = await link.evaluate(el => !el.checkVisibility({ visibilityProperty: true }));
    const closed = await keyboardProblems(page);
    const omitted = await link.evaluate(el => !el.hasAttribute('data-qa-i'));
    check('native closed-details links omitted', hidden && omitted && !closed.length, closed);
    // Derived geometry counterexample; not a claim about native hidden rects.
    await link.evaluate(el => { el.getClientRects = () => [new DOMRect(0, 0, 1, 1)]; });
    const derived = await keyboardProblems(page);
    const stillOmitted = await link.evaluate(el => el.getClientRects().length === 1 && !el.hasAttribute('data-qa-i'));
    check('derived rect-only visibility counterexample', !derived.length && stillOmitted, derived);
    await link.evaluate(el => { delete el.getClientRects; });
    await details.evaluate(el => { el.open = true; });
    const opened = await keyboardProblems(page);
    const visible = await link.evaluate(el => el.checkVisibility({ visibilityProperty: true }) && el.hasAttribute('data-qa-i'));
    await link.evaluate(el => { el.tabIndex = -1; el.textContent = 'QA opened unreachable'; window.__qaOpenedFault = true; });
    const broken = await keyboardProblems(page);
    const retained = await link.evaluate(el => el.tabIndex === -1 && window.__qaOpenedFault === true);
    check('native opened links checked and visible unreachable caught', visible && !opened.length && broken.some(x => x.includes('not reachable by Tab: a "QA opened unreachable"')) && retained, { opened, broken, retained });
    await context.close();
  }
  for (const width of [375, 1280]) for (const theme of ['light', 'dark']) {
    const { context, page } = await fixture(width, theme);
    const source = page.getByText('Source identities', { exact: true }).first();
    await source.click();
    const focusedMiddle = await source.evaluate(el => document.activeElement === el);
    const errors = await keyboardProblems(page);
    check(`document start after middle focus ${width}/${theme}`, focusedMiddle && !errors.length, errors);
    await context.close();
  }
  const controls = [
    ['visible unreachable', async page => page.evaluate(() => {
      const button = document.createElement('button');
      button.textContent = 'QA visible unreachable'; button.tabIndex = -1;
      button.dataset.qaFault = 'unreachable'; document.querySelector('main').append(button);
    }), errors => errors.some(x => x.includes('not reachable by Tab: button "QA visible unreachable"')), '[data-qa-fault="unreachable"]'],
    ['invisible focus', page => page.addStyleTag({ content: '*:focus, *:focus-visible { outline: none !important; box-shadow: none !important; }' }).then(style => style.evaluate(el => { el.dataset.qaFault = 'focus'; })), errors => errors.some(x => x.startsWith('no visible focus')), '[data-qa-fault="focus"]'],
    ['early traversal termination', page => page.evaluate(() => {
      const first = document.querySelector('a[href]');
      first.dataset.qaFault = 'early-stop';
      first.addEventListener('focus', () => first.blur());
    }), errors => errors.some(x => x.startsWith('not reachable by Tab')), '[data-qa-fault="early-stop"]'],
  ];
  for (const [name, plant, matches, marker] of controls) {
    const { context, page } = await fixture();
    const before = await keyboardProblems(page);
    await page.evaluate(() => { window.__qaDocument = 'faults must survive'; });
    await plant(page);
    const errors = await keyboardProblems(page);
    const retained = await page.evaluate(selector => window.__qaDocument === 'faults must survive' && !!document.querySelector(selector), marker);
    check(`negative: ${name}`, !before.length && matches(errors) && retained, { before, errors, retained });
    await context.close();
  }
  // The real shell must reveal links natively without relying on hydration.
  for (const route of ['/rsi', '/start']) for (const javaScriptEnabled of [false, true]) {
    for (const width of [375, 1280]) for (const theme of ['light', 'dark']) {
      const context = await browser.newContext({ viewport: { width, height: 812 }, colorScheme: theme, javaScriptEnabled });
      const page = await context.newPage();
      await page.goto(`${base}${route}`, { waitUntil: 'networkidle' });
      const errors = await keyboardProblems(page);
      const text = (await page.textContent('main')) ?? '';
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
      check(`real shell ${route} JS=${javaScriptEnabled} ${width}/${theme}`, !errors.length && !overflow && text.trim().length > 40, { errors, overflow });
      await context.close();
    }
  }
} finally {
  await browser.close();
}
assert.ok(results.every(x => x.pass), `${results.filter(x => !x.pass).length}/${results.length} keyboard controls failed`);
console.log(`${results.length}/${results.length} keyboard controls passed`);
