// S-011 TK-003: the shared-skill repair round two is the current result on
// /rsi. Each skill's baseline and candidate Mid-tier runs are charted where a
// reader sees them without interaction, the High and Small arms read as
// non-gating comparisons, every disposition is stated as recorded, and the
// identities behind the charts sit in an on-page evidence section. The first
// attempt stays on the page as history.
import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement, Fragment } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { readPage, hiddenMarker } from './rsi-html.mjs';
import { quoteProblems } from './tour-helpers.mjs';
import { hygieneFindings } from './hygiene.mjs';

const { RoundTwoEvidence } = await import('../app/rsi/round-two.tsx');
const { roundTwo } = await import('../app/rsi/round-two-data.ts');
const { RepairEvidence } = await import('../app/rsi/repair.tsx');
const { RsiView } = await import('../app/rsi/view.tsx');
const { seriesViews } = await import('../app/rsi/data.ts');

const html = () => renderToStaticMarkup(createElement(RoundTwoEvidence));
const text = (h) => h.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ');
const skillBlock = (out, skill) => {
  const start = out.indexOf(`data-round-two-skill="${skill}"`);
  assert.ok(start >= 0, `no chart for ${skill}`);
  const end = out.indexOf('data-round-two-skill=', start + 1);
  return out.slice(start, end < 0 ? out.indexOf('data-round-two-dev') : end);
};

// The recorded safe summary, typed here independently of the data module.
const EXPECTED = {
  'setup-workbench': { baseline: ['Broken', '12/15', [false, false, false]], candidate: ['Excellent', '14/15', [true, true, true]], disposition: 'merged', commit: '8dc3b636e039a13434f0ddf5f4403f7402683982', candidateSha: '378658d1b2a7ba276202e4d0058a794a1a25185a' },
  orchestrate: { baseline: ['Broken', '26/27', [true, true, false]], candidate: ['Excellent', '27/27', [true, true, true]], disposition: 'merged', commit: '1e41c87', candidateSha: 'aebb3098f0f119e15b1ca773b7bf2a96aba54d6c' },
  handoff: { baseline: ['Broken', '3/18', [false, false, false]], candidate: ['Excellent', '18/18', [true, true, true]], disposition: 'merged', commit: '2c2dfef', candidateSha: '28749fb7793ac9dacb948dce72b634ba540a7bd1' },
  journey: { baseline: ['Excellent', '30/30', [true, true, true]], candidate: ['Excellent', '30/30', [true, true, true]], disposition: 'owner-merge', commit: '03fcdb2', candidateSha: '2567c74328cbe2eb9a8e9bfa9fde7b57c4dab315' },
  land: { baseline: ['Broken', '16/18', [false, true, false]], candidate: ['Broken', '16/18', [true, false, false]], disposition: 'returned', commit: null, candidateSha: '9eca0b3c81b8a6d0c5e649e5259a2a3cc648a8b7' },
};

test('round-two data holds the recorded Mid-tier results and dispositions for each skill', () => {
  assert.deepEqual(roundTwo.skills.map((s) => s.skill), Object.keys(EXPECTED));
  for (const s of roundTwo.skills) {
    const want = EXPECTED[s.skill];
    for (const role of ['baseline', 'candidate']) {
      const mid = s[role].mid;
      assert.equal(mid.model, 'claude-sonnet-5-5', `${s.skill} ${role} Mid model`);
      assert.deepEqual([mid.level, mid.pooled, mid.runs.map((r) => r.pass)], want[role], `${s.skill} ${role}`);
      assert.equal(s[role].high.model, 'claude-opus-5-5');
      assert.equal(s[role].small.model, 'claude-haiku-5-5');
    }
    assert.equal(s.disposition.kind, want.disposition, `${s.skill} disposition`);
    assert.equal(s.mainCommit, want.commit, `${s.skill} merge commit`);
    assert.equal(s.candidate.sha, want.candidateSha, `${s.skill} candidate`);
  }
});

test('each skill charts baseline against candidate at the Mid tier with every run marked pass or fail', () => {
  const out = html();
  for (const [skill, want] of Object.entries(EXPECTED)) {
    const block = skillBlock(out, skill);
    for (const role of ['baseline', 'candidate']) {
      const [level, pooled, runs] = want[role];
      const [passed, of] = pooled.split('/');
      const row = block.match(new RegExp(`data-arm-row="${role}"[\\s\\S]*?</li>`))?.[0] ?? '';
      assert.match(text(row), new RegExp(`${passed} of ${of}`), `${skill} ${role} pooled`);
      assert.match(text(row), new RegExp(level), `${skill} ${role} level`);
      const marks = [...row.matchAll(/data-run-result="(pass|fail)"/g)].map((m) => m[1] === 'pass');
      assert.deepEqual(marks, runs, `${skill} ${role} per-run marks`);
    }
    assert.match(block, /data-round-two-bar=/, `${skill} draws no bar`);
  }
});

test('charts are visible without interaction: nothing collapsed or hidden around them', () => {
  const tracked = readPage(`<main>${html()}</main>`, ['data-round-two-chart', 'data-round-two-skill', 'data-round-two-dev', 'data-round-two-evidence']);
  assert.ok(tracked.some((r) => 'data-round-two-chart' in r.attrs), 'no summary chart');
  assert.equal(tracked.filter((r) => 'data-round-two-skill' in r.attrs).length, 5);
  for (const record of tracked) {
    const found = [record, ...record.ancestors].map(hiddenMarker).filter(Boolean);
    assert.deepEqual(found, [], `${Object.keys(record.attrs).find((a) => a.startsWith('data-round-two'))} is hidden by ${found.join(', ')}`);
  }
});

test('High and Small arms are shown as non-gating comparisons with their exact models', () => {
  const out = html();
  for (const skill of Object.keys(EXPECTED)) {
    const block = skillBlock(out, skill);
    const arms = block.match(/data-comparison-arms=""[\s\S]*?<\/div>/)?.[0] ?? '';
    assert.match(text(arms), /not gating/i, `${skill} comparison arms not labeled non-gating`);
    assert.match(arms, /High[\s\S]*claude-opus-5-5/);
    assert.match(arms, /Small[\s\S]*claude-haiku-5-5/);
  }
  // An ungraded run is shown as ungraded, never as a number.
  assert.match(text(skillBlock(out, 'setup-workbench')), /ungraded/);
  assert.match(text(skillBlock(out, 'setup-workbench')), /0 of 5/);
  assert.match(text(skillBlock(out, 'land')), /0 of 6/);
});

test('dispositions are stated as recorded, including the owner decision and the returned repair', () => {
  const out = html();
  for (const skill of ['setup-workbench', 'orchestrate', 'handoff']) assert.match(text(skillBlock(out, skill)), /Merged/);
  const journey = text(skillBlock(out, 'journey'));
  assert.match(journey, /owner decision/i);
  assert.match(journey, /no regression/i);
  assert.match(journey, /not reproduce/i);
  assert.match(journey, /not a proven fix/i);
  const land = text(skillBlock(out, 'land'));
  assert.match(land, /Not merged/);
  assert.match(land, /returned to the owner after three attempts/i);
  assert.match(land, /equal to the baseline/i);
});

test('the evidence section carries contracts, baseline pin, candidates, merges, reviews and judge limits', () => {
  const out = html();
  const start = out.indexOf('id="round-two-evidence"');
  assert.ok(start >= 0, 'no on-page evidence section');
  const ev = text(out.slice(start));
  for (const id of [
    '197858fec1e23882857684d67e847a20566a38232f662412621ebe68d382ec8d',
    'bf493e93b4e9e0426a2cf1af2c9867215bf3ac73be4ebc498c9f740868267e3b',
    'fb7ad23c963e183b930b23bc5fdf4d309dff292a',
    ...Object.values(EXPECTED).flatMap((s) => [s.candidateSha, s.commit].filter(Boolean)),
    'HO-07', 'PR-08', 'HO2-05', 'SW2-05',
  ]) assert.ok(ev.includes(id), `evidence lacks ${id}`);
  assert.equal((ev.match(/PASS WITH NOTES/g) ?? []).length >= 5, true, 'review verdicts missing');
  for (const [tier, model] of [['Frontier', 'claude-fable-5-1'], ['High', 'claude-opus-5-5'], ['Mid', 'claude-sonnet-5-5'], ['Small', 'claude-haiku-5-5']]) {
    assert.match(ev, new RegExp(`${tier}[^|]*?${model}`), `${tier} tier not shown with ${model}`);
  }
  for (const skill of Object.keys(EXPECTED)) assert.ok(out.includes(`id="round-two-evidence-${skill}"`), `no evidence rows for ${skill}`);
});

test('the first contract is shown as non-qualifying with the reason the tests were rebuilt', () => {
  const t = text(html());
  assert.match(t, /non-qualifying/i);
  assert.match(t, /seven of eight/i);
  assert.match(t, /owner-found failures/i);
});

test('pruning results are development observations, not held-out, and author-skill has no result', () => {
  const out = html();
  const start = out.indexOf('data-round-two-dev');
  assert.ok(start >= 0, 'no development observation chart');
  const dev = text(out.slice(start, out.indexOf('id="round-two-evidence"')));
  assert.match(dev, /development observation/i);
  assert.match(dev, /not a held-out result/i);
  assert.match(dev, /returned to the owner unmerged/i);
  for (const n of [2978, 2985, 2999, 1204, 1338, 1491, 1236, 1256, 1235, 1269, 1399, 1299, 1466, 3116, 3119]) {
    assert.ok(dev.includes(String(n)), `missing ${n}`);
  }
  assert.match(dev, /900–1500/);
  assert.match(dev, /3000/);
  const lengths = [...out.matchAll(/data-dev-length="(\d+)"/g)].map((m) => Number(m[1]));
  assert.deepEqual(lengths, [2978, 2985, 2999, 1204, 1338, 1491, 1236, 1256, 1235, 1269, 1399, 1299, 1466]);
  const author = out.match(/data-round-two-hold="author-skill"[\s\S]*?<\/p>/)?.[0] ?? '';
  assert.match(text(author), /on hold/i);
  assert.match(text(author), /no result/i);
  assert.doesNotMatch(text(author).replace(/author-skill/, ''), /\d/, 'author-skill must carry no number');
});

test('round two is current, precedes the first attempt, and the first attempt remains as history', () => {
  const out = renderToStaticMarkup(createElement(RsiView, { views: seriesViews({ runs: [], results: [] }), unavailable: false },
    createElement(Fragment, null, createElement(RoundTwoEvidence), createElement(RepairEvidence))));
  const title = out.indexOf('<h1>RSI results</h1>');
  const round = out.indexOf('id="round-two-title"');
  const first = out.indexOf('id="repair-title"');
  assert.ok(title >= 0 && round > title && first > round, 'round two must sit between the title and the first attempt');
  assert.match(out, /data-evidence-chart="workflow"/);
  assert.match(out, /id="candidate-evidence"/);
  assert.match(text(out.slice(round, first)), /current result/i);
});

test('round two stays on-site, quotes no one, carries no banner and no private material', () => {
  const out = html();
  for (const [, href] of out.matchAll(/href="([^"]+)"/g)) {
    assert.ok(href.startsWith('#'), `outbound link: ${href}`);
    assert.ok(out.includes(`id="${href.slice(1)}"`), `missing on-page target: ${href}`);
  }
  assert.deepEqual(quoteProblems(`<main>${out}</main>`), []);
  assert.deepEqual(hygieneFindings(out), []);
  assert.doesNotMatch(text(out), /\b(draft|approved|reviewed by|awaiting approval)\b/i);
  assert.doesNotMatch(out, /github\.com/i);
  assert.match(text(out), /Private prompts, transcripts, fixture contents and skill text are excluded/);
  assert.match(text(out), /not a held-out headline/i);
});
