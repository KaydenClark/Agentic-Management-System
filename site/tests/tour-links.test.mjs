// S-003 TK-002 acceptance: every page links forward and back in one reading
// order, over the built output. A page with no forward or back link fails, and
// so does a page that is outside the reading order. Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { builtPage, builtPages, siteDir } from './helpers.mjs';
import { READING_ORDER, builtName, mainOf, orderProblems } from './tour-helpers.mjs';

const nav = (links) => `<nav aria-label="Page order">${links}</nav>`;

test('the check catches dead ends and wrong links (self-test)', () => {
  const order = ['/a', '/b', '/c'];
  assert.deepEqual(orderProblems(nav('<a rel="prev" href="/a">A</a><a rel="next" href="/c">C</a>'), 1, order), []);
  assert.deepEqual(orderProblems(nav('<a rel="next" href="/b">B</a>'), 0, order), []);
  assert.deepEqual(orderProblems(nav('<a rel="prev" href="/b">B</a>'), 2, order), []);
  assert.ok(orderProblems('<main>no links</main>', 1, order).length, 'page with no forward/back links passes');
  assert.ok(orderProblems(nav('<a rel="prev" href="/a">A</a>'), 1, order).length, 'missing forward link passes');
  assert.ok(orderProblems(nav('<a rel="next" href="/c">C</a>'), 1, order).length, 'missing back link passes');
  assert.ok(orderProblems(nav('<a rel="prev" href="/c">C</a><a rel="next" href="/a">A</a>'), 1, order).length, 'swapped links pass');
  assert.ok(orderProblems(nav(''), 0, ['/only']).length, 'a lone page with no links passes');
});

test('nav.ts lists the reading order Home, Start here, How it works, RSI results', () => {
  const src = readFileSync(join(siteDir, 'app', 'nav.ts'), 'utf8');
  const hrefs = [...src.matchAll(/href:\s*"([^"]+)"/g)].map((m) => m[1]);
  assert.deepEqual(hrefs, READING_ORDER);
});

READING_ORDER.forEach((href, i) => {
  test(`${href} links back and forward in the reading order`, () => {
    assert.deepEqual(orderProblems(builtPage(builtName(href)).html, i), [], href);
  });
});

test('every built page is in the reading order (no orphan page)', () => {
  const inOrder = new Set(READING_ORDER.map(builtName));
  for (const { name } of builtPages()) {
    if (name.startsWith('_')) continue; // Next's own not-found and error pages
    assert.ok(inOrder.has(name), `${name} is built but not in the reading order`);
  }
});

test('internal links on tour pages resolve to a built page or an id on the page', () => {
  const built = new Set(builtPages().map((p) => p.name));
  for (const href of READING_ORDER) {
    const { html } = builtPage(builtName(href));
    for (const [, target] of mainOf(html).matchAll(/<a\b[^>]*href="([^"]+)"/gi)) {
      if (/^(https?:|mailto:)/.test(target)) continue;
      if (target.startsWith('#')) {
        assert.match(html, new RegExp(`\\sid="${target.slice(1)}"`), `${href}: ${target} has no target`);
        continue;
      }
      const path = target.split('#')[0];
      assert.ok(built.has(builtName(path === '' ? href : path)), `${href}: link ${target} has no built page`);
    }
  }
});
