import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';

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
    assert.match(headerNav(page(name)), /href="\/start"[^>]*aria-current="page"[^>]*>About<\/a>/);
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
