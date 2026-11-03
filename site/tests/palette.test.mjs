import {test} from 'node:test';
import assert from 'node:assert/strict';
import {builtPage} from './helpers.mjs';
import {readPage, hiddenMarker} from './rsi-html.mjs';

function signalProblems(html, kind, meaning) {
  const signals = readPage(html, ['data-signal']).filter(node => node.attrs['data-signal'] === kind);
  if (!signals.length) return [`missing ${kind} signal`];
  return signals.flatMap(node => [
    ...(!new RegExp(`(?:^|\\s)h-${kind}(?:\\s|$)`).test(node.attrs.class ?? '') ? ['wrong hue'] : []),
    ...(!meaning.test(node.text) ? ['no readable meaning'] : []),
    ...([node, ...node.ancestors].some(hiddenMarker) ? ['hidden meaning'] : []),
  ]);
}

test('palette checks reject absent, mismatched and unexplained signals', () => {
  const good = '<div data-signal="agent" class="tone h-agent"><p>Agents carry the work.</p></div>';
  assert.deepEqual(signalProblems(good, 'agent', /Agents carry/), []);
  for (const bad of ['', good.replace('h-agent', 'h-owner'), good.replace('Agents carry the work.', 'Decoration.'), good.replace('<div ', '<div hidden ')]) {
    assert.ok(signalProblems(bad, 'agent', /Agents carry/).length);
  }
});

test('shared palette signals retain readable agent, answer-worth and rework meanings', () => {
  assert.deepEqual(signalProblems(builtPage('index.html').html, 'agent', /agents/i), []);
  const how = builtPage('how-it-works.html').html;
  assert.deepEqual(signalProblems(how, 'worth', /answers shape the work/i), []);
  assert.deepEqual(signalProblems(how, 'returned', /return for correction/i), []);
  assert.deepEqual(signalProblems(builtPage('glossary.html').html, 'agent', /Work with agents/), []);
});

test('failed RSI reads carry trouble while successful empty reads remain neutral', async () => {
  await import('./tsx-register.mjs');
  const {createElement} = await import('react');
  const {renderToStaticMarkup} = await import('react-dom/server');
  const {RsiView} = await import('../app/rsi/view.tsx');
  const {emptyData, seriesViews} = await import('../app/rsi/data.ts');
  const render = unavailable => renderToStaticMarkup(createElement(RsiView, {views: seriesViews(emptyData), unavailable}));
  assert.deepEqual(signalProblems(render(true), 'heat', /could not be loaded.*unknown/s), []);
  assert.equal(readPage(render(false), ['data-signal']).length, 0, 'successful empty data must not signal trouble');
});
