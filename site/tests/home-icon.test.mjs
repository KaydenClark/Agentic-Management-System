import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPages } from './helpers.mjs';

function homeIconProblems(html) {
  const header = html.match(/<header\b[\s\S]*?<\/header>/i)?.[0] ?? '';
  const links = [...header.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/gi)].map(match => match[0]);
  const home = links.filter(link => /\saria-label="Home"(?:\s|>)/.test(link));
  if (home.length !== 1) return ['exactly one named Home icon is required'];
  const problems = [];
  if (!/\shref="\/"(?:\s|>)/.test(home[0])) problems.push('Home icon has the wrong destination');
  if (!/<svg\b[^>]*\saria-hidden="true"/.test(home[0])) problems.push('Home has no decorative icon');
  return problems;
}

test('the Home icon check rejects a missing name, destination or icon', () => {
  const html = '<header><a href="/" aria-label="Home"><svg aria-hidden="true"></svg></a></header>';
  assert.deepEqual(homeIconProblems(html), []);
  for (const changed of [html.replace('aria-label="Home"',''), html.replace('href="/"','href="/start"'),html.replace(/<svg[\s\S]*?<\/svg>/,'')]) assert.ok(homeIconProblems(changed).length);
});

test('every built page has an accessible icon linking to Home', () => {
  for (const {name,html} of builtPages()) assert.deepEqual(homeIconProblems(html), [], name);
});
