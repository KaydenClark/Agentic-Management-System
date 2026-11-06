import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, visibleText } from './helpers.mjs';
import { aboutNavigationProblems, childProblems, mainOf } from './tour-helpers.mjs';

const page = name => builtPage(`${name}.html`).html;
const headerNav = html => html.match(/<nav[^>]*aria-label="Reading order"[\s\S]*?<\/nav>/)?.[0] ?? '';

test('the orientation has one About entry and its older routes share the same introduction', () => {
  for (const name of ['index', 'start', 'about', 'why', 'how-it-works']) {
    const nav = headerNav(page(name));
    assert.match(nav, /href="\/start"[^>]*>About<\/a>/);
    assert.doesNotMatch(nav, /href="\/about"/);
  }
  assert.equal(visibleText(mainOf(page('start'))), visibleText(mainOf(page('about'))));
  for (const name of ['start', 'about']) {
    assert.deepEqual(aboutNavigationProblems(page(name)), []);
    for (const id of ['what-it-is','problem','flow','try','who','refuses','today','quickstart','holds','license','status','built']) {
      assert.match(page(name), new RegExp(`\\sid="${id}"`), `${name} loses old entry #${id}`);
    }
  }
});

test('Home guides visitors to the introduction, real example, methods, evidence and limits', () => {
  const main = mainOf(page('index'));
  for (const path of ['/start', '/how-it-works#example', '/skills', '/rsi', '/start#refuses']) {
    assert.ok(main.includes(`href="${path}"`), `Home has no route to ${path}`);
  }
  assert.doesNotMatch(visibleText(main), /footer[\s\S]{0,100}linked to[\s\S]{0,30}GitHub/i);
});

test('the orientation explains limits, human decisions and the everyday purpose of the Grill Board on-site', () => {
  const about = visibleText(mainOf(page('start')));
  const how = mainOf(page('how-it-works'));
  assert.match(about, /Kayden Clark/);
  assert.match(about, /MIT License/);
  assert.match(about, /runs no agents/);
  assert.doesNotMatch(about, /all Claude|architecture record marks itself partial/i);
  for (const id of ['governance', 'grill-board']) assert.match(how, new RegExp(`\\sid="${id}"`));
  assert.match(visibleText(how), /Human QA/);
  assert.match(visibleText(how), /does not.*approval|not.*approval/);
  assert.match(visibleText(how), /picnic|weekend|dinner/);
  assert.ok(how.includes('href="/start#refuses"'));
});

test('About alias accepts every valid attribute order and rejects wrong links or state', () => {
  const orders = [
    ['href="/start"', 'aria-current="page"', 'class="navlink"'],
    ['href="/start"', 'class="navlink"', 'aria-current="page"'],
    ['aria-current="page"', 'href="/start"', 'class="navlink"'],
    ['aria-current="page"', 'class="navlink"', 'href="/start"'],
    ['class="navlink"', 'href="/start"', 'aria-current="page"'],
    ['class="navlink"', 'aria-current="page"', 'href="/start"'],
  ];
  const render = attrs => `<nav aria-label="Reading order"><a ${attrs.join(' ')}>About</a></nav><main>Same introduction.</main>`;
  for (const attrs of orders) {
    const html = render(attrs);
    const parents = new Map([['/start', html]]);
    assert.deepEqual(aboutNavigationProblems(html), [], attrs.join(' '));
    assert.deepEqual(childProblems('/about', html, parents), []);
    for (const changed of [
      html.replace('href="/start"', 'href="/why"'),
      html.replace('aria-current="page"', ''),
      html.replace('aria-current="page"', 'aria-current="false"'),
      html.replace('>About</a>', '>Different</a>'),
    ]) assert.ok(aboutNavigationProblems(changed).length, changed);
    assert.ok(childProblems('/about', html.replace('Same introduction.', 'Other introduction.'), parents).length);
  }
  assert.ok(aboutNavigationProblems('<nav aria-label="Reading order"><a aria-current="page" href="/start">About</a><a aria-current="page" href="/why">Why</a></nav>').length);
});
