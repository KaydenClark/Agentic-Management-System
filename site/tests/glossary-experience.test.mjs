import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';

// Public links and text equivalents survive a change in visual layout.
function relationshipProblems(html) {
  const main = mainOf(html);
  const ids = [...main.matchAll(/\sid="([^"]+)"/g)].map(match => match[1]);
  const problems = [];
  for (const match of main.matchAll(/\shref="#([^"]+)"/g)) {
    if (ids.filter(id => id === match[1]).length !== 1) problems.push(`unresolved or duplicate anchor ${match[1]}`);
  }
  for (const figure of main.matchAll(/<figure\b([^>]*)>([\s\S]*?)<\/figure>/g)) {
    const label = figure[1].match(/\saria-labelledby="([^"]+)"/)?.[1];
    const caption = figure[2].match(/<figcaption\b([^>]*)>([\s\S]*?)<\/figcaption>/);
    if (!label || !caption || !caption[1].includes(`id="${label}"`) || visibleText(caption[2]).length < 30) {
      problems.push('relationship lacks its readable caption');
    }
  }
  if (![...main.matchAll(/<figure\b/g)].length) problems.push('no relationships');
  return problems;
}

const example = '<main><figure aria-labelledby="meaning"><a href="#term">Term</a><figcaption id="meaning">A readable sentence explaining the connection between terms.</figcaption></figure><dt id="term">Term</dt></main>';

test('relationship detector rejects broken links and missing text equivalents', () => {
  assert.deepEqual(relationshipProblems(example), []);
  assert.ok(relationshipProblems(example.replace('id="term"', 'id="other"')).length);
  assert.ok(relationshipProblems(example.replace(/<figcaption[\s\S]*?<\/figcaption>/, '')).length);
  assert.ok(relationshipProblems(example.replace('aria-labelledby="meaning"', '')).length);
  assert.ok(relationshipProblems('<main>Only a list.</main>').length);
});

test('glossary relationships retain resolving term links and readable captions', () => {
  const html = builtPage('glossary.html').html;
  assert.deepEqual(relationshipProblems(html), []);
  const main = mainOf(html);
  const stableIds = ['group-ams', 'group-records', 'group-feedback-dispositions', 'ams', 'rsi-loop', 'alignment-assessment', 'alignment-score', 'fitness-level', 'improvement-attempt', 'workbench', 'intent', 'implementation-task', 'evaluation-task', 'evidence-audit', 'improvement-record', 'review-receipt', 'human-qa-receipt', 'diagnostic', 'test', 'repaired', 'declined', 'accepted-open'];
  for (const id of stableIds) assert.equal([...main.matchAll(/\sid="([^"]+)"/g)].filter(match => match[1] === id).length, 1, id);
  for (const href of ['/start#what-it-is', '/how-it-works#example', '/how-it-works#governance', '/rsi']) {
    assert.ok(main.includes(`href="${href}"`), `no return to explanation ${href}`);
  }
  const text = visibleText(main);
  assert.match(text, /Each attempt at the case is a trial/);
  assert.match(text, /agent checks cannot supply it/);
  assert.match(text, /different ways to handle a finding, not a sequence of required steps/);
});
