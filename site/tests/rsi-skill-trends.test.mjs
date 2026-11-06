// S-007 TK-002J: "Is RSI improving each skill?" on /rsi. Each charted skill
// gets one point per recorded loop from the kept version's Alignment Score and
// fitness level, with the start point; attempts not kept and High/Small runs
// are secondary marks that never decide a point; a new test contract or model
// starts a new labeled line; regressions stay visible; and a skills-by-loops
// strip shows the fitness level per loop. The checks run on the recorded
// loops, on a labeled multi-loop fixture, and on planted faults to prove each
// check fails.
import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createElement, Fragment } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { readPage, hiddenMarker } from './rsi-html.mjs';
import { quoteProblems } from './tour-helpers.mjs';
import { hygieneFindings } from './hygiene.mjs';
import { siteDir } from './helpers.mjs';

const { SkillTrends } = await import('../app/rsi/skill-trends.tsx');
const { recordedLoops, skillTrends } = await import('../app/rsi/skill-loops.ts');
const { multiLoopFixture, FIXTURE_SKILL } = await import('../app/rsi/fixtures/skill-loops.ts');
const { RoundTwoEvidence } = await import('../app/rsi/round-two.tsx');
const { RsiView } = await import('../app/rsi/view.tsx');
const { seriesViews } = await import('../app/rsi/data.ts');

const render = (records) => renderToStaticMarkup(createElement(SkillTrends, { records }));
const text = (h) => h.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/\s+/g, ' ');
const TRACK = ['data-break-label', 'data-trend-skill', 'data-trend-line', 'data-trend-point', 'data-break', 'data-not-kept', 'data-secondary-mark', 'data-regression', 'data-regression-text', 'data-running-average', 'data-level-row', 'data-level-cell', 'data-trend-points', 'data-trend-provenance'];

// Each skill's cards, lines and points as the page draws them.
function read(html) {
  const tracked = readPage(`<main>${html}</main>`, TRACK);
  const cards = tracked.filter((r) => 'data-trend-skill' in r.attrs);
  const inside = (card, attr) => tracked.filter((r) => attr in r.attrs && r.ancestors.some((a) => a.attrs === card.attrs));
  return cards.map((card) => {
    const lines = inside(card, 'data-trend-line').map((line) => ({
      contract: line.attrs['data-contract'],
      model: line.attrs['data-model'],
      points: tracked
        .filter((r) => 'data-trend-point' in r.attrs && r.ancestors.some((a) => a.attrs === line.attrs))
        .map((p) => [p.attrs['data-trend-point'], Number(p.attrs['data-loop']), p.attrs['data-score'], p.attrs['data-level']]),
      average: tracked.some((r) => 'data-running-average' in r.attrs && r.ancestors.some((a) => a.attrs === line.attrs)),
    }));
    return {
      skill: card.attrs['data-trend-skill'],
      card,
      lines,
      breaks: inside(card, 'data-break').map((r, i) => ({ reasons: r.attrs['data-break'], label: inside(card, 'data-break-label')[i]?.text.trim() ?? '' })),
      notKept: inside(card, 'data-not-kept').map((r) => r.attrs['data-not-kept']),
      secondary: inside(card, 'data-secondary-mark').map((r) => [r.name, r.attrs['data-secondary-mark'], 'data-trend-point' in r.attrs]),
      notKeptAsPoint: inside(card, 'data-not-kept').filter((r) => 'data-trend-point' in r.attrs).length,
      regressions: inside(card, 'data-regression').length,
      regressionTexts: inside(card, 'data-regression-text').length,
      points: inside(card, 'data-trend-point').length,
      tracked,
    };
  });
}

// The recorded loop 1 (S-011 history, round two), typed here independently of
// the data modules: [kind, loop, pooled score, fitness level] per point.
const RECORDED = {
  'setup-workbench': { contract: 'v2', points: [['start', 0, '12/15', 'Broken'], ['loop', 1, '14/15', 'Excellent']], notKept: [] },
  orchestrate: { contract: 'v1', points: [['start', 0, '26/27', 'Broken'], ['loop', 1, '27/27', 'Excellent']], notKept: ['b61280d'] },
  handoff: { contract: 'v2', points: [['start', 0, '3/18', 'Broken'], ['loop', 1, '18/18', 'Excellent']], notKept: ['96b9460'] },
  journey: { contract: 'v1', points: [['start', 0, '30/30', 'Excellent'], ['loop', 1, '30/30', 'Excellent']], notKept: [] },
  land: { contract: 'v2', points: [['start', 0, '16/18', 'Broken'], ['loop', 1, '16/18', 'Broken']], notKept: ['5739c32', 'fc1a080', '9eca0b3'] },
};
const NOT_KEPT_SCORES = { b61280d: '27/27', '96b9460': '15/18', '5739c32': '13/18', fc1a080: '16/18', '9eca0b3': '16/18' };
const MID = 'claude-sonnet-5-5';

// The fixture, typed independently of its module: three lines (contract
// fx-v1, then a new contract fx-v2, then a new model), a rejected attempt at
// 20/20 in loop 2, High runs at 20/20 everywhere, a regression at loop 3 and a
// loop 5 that kept its start.
const FIXTURE = {
  [FIXTURE_SKILL]: {
    lines: [
      { contract: 'fx-v1', model: 'fixture-model-a', points: [['start', 0, '10/20', 'Broken'], ['loop', 1, '14/20', 'Functional'], ['loop', 2, '17/20', 'Stable'], ['loop', 3, '12/20', 'Broken']], average: true },
      { contract: 'fx-v2', model: 'fixture-model-a', points: [['start', 3, '8/20', 'Broken'], ['loop', 4, '15/20', 'Functional'], ['loop', 5, '15/20', 'Functional']], average: true },
      { contract: 'fx-v2', model: 'fixture-model-b', points: [['start', 5, '16/20', 'Stable'], ['loop', 6, '20/20', 'Excellent']], average: false },
    ],
    breaks: [{ reasons: 'contract', label: /new contract fx-v2/ }, { reasons: 'model', label: /new model/ }],
    notKept: ['fx0003r', 'fx0006r'],
    regressions: 1,
  },
};

const CHECKS = {
  'each skill shows one point per recorded loop from the kept version, with its start': (cards, want) => {
    assert.deepEqual(cards.map((c) => c.skill), Object.keys(want), 'charted skills');
    for (const c of cards) {
      const lines = want[c.skill].lines ?? [{ points: want[c.skill].points }];
      assert.deepEqual(c.lines.map((l) => l.points), lines.map((l) => l.points), `${c.skill} points`);
    }
  },
  'a test contract or model change starts a new labeled line, never a continuation': (cards, want) => {
    for (const c of cards) {
      const lines = want[c.skill].lines ?? [{ contract: want[c.skill].contract, model: MID }];
      assert.deepEqual(c.lines.map((l) => [l.contract, l.model]), lines.map((l) => [l.contract, l.model]), `${c.skill} lines`);
      for (let i = 1; i < c.lines.length; i++) {
        const [a, b] = [c.lines[i - 1], c.lines[i]];
        assert.ok(a.contract !== b.contract || a.model !== b.model, `${c.skill}: line ${i} continues line ${i - 1}`);
      }
      const breaks = want[c.skill].breaks ?? [];
      assert.equal(c.breaks.length, breaks.length, `${c.skill} break count`);
      breaks.forEach((b, i) => {
        assert.equal(c.breaks[i].reasons, b.reasons, `${c.skill} break ${i} reason`);
        assert.match(c.breaks[i].label, b.label, `${c.skill} break ${i} label`);
      });
    }
  },
  'attempts not kept and High or Small runs are secondary marks that never decide a point': (cards, want) => {
    for (const c of cards) {
      assert.deepEqual(c.notKept, want[c.skill].notKept, `${c.skill} attempts not kept`);
      assert.ok(c.secondary.length > 0, `${c.skill} shows no High or Small run`);
      for (const [name, tier, isPoint] of c.secondary) {
        assert.equal(name, tier === 'High' ? 'path' : 'rect', `${c.skill} ${tier} mark shape`);
        assert.equal(isPoint, false, `${c.skill}: a ${tier} run is drawn as a point`);
      }
      assert.equal(c.notKeptAsPoint, 0, `${c.skill}: an attempt not kept is drawn as a point`);
      const all = c.lines.flatMap((l) => l.points);
      assert.equal(c.points, all.length, `${c.skill}: a point sits outside its line`);
    }
  },
  'a regression stays visible on the chart and in words': (cards, want) => {
    for (const c of cards) {
      const n = want[c.skill].regressions ?? 0;
      assert.equal(c.regressions, n, `${c.skill} regression marks`);
      assert.equal(c.regressionTexts, n, `${c.skill} regression words`);
    }
  },
};

const realCards = () => read(render(recordedLoops()));
const fixtureCards = () => read(render(multiLoopFixture));

for (const [name, check] of Object.entries(CHECKS)) {
  test(`recorded loops: ${name}`, () => check(realCards(), RECORDED));
  test(`labeled fixture: ${name}`, () => check(fixtureCards(), FIXTURE));
}

test('the recorded seam derives loop 1 from round two and the S-011 attempts, inventing nothing', () => {
  const records = recordedLoops();
  assert.deepEqual(records.map((r) => r.skill), Object.keys(RECORDED));
  for (const r of records) {
    const want = RECORDED[r.skill];
    assert.equal(r.loop, 1);
    assert.equal(r.contract, want.contract);
    assert.deepEqual([r.tier, r.model], ['Mid', MID]);
    assert.deepEqual([`${r.start.passed}/${r.start.checks}`, r.start.level], want.points[0].slice(2));
    assert.deepEqual([`${r.kept.passed}/${r.kept.checks}`, r.kept.level], want.points[1].slice(2));
    assert.deepEqual(r.notKept.map((a) => a.version), want.notKept);
    for (const a of r.notKept) assert.equal(`${a.passed}/${a.checks}`, NOT_KEPT_SCORES[a.version], `${r.skill} ${a.version}`);
    assert.match(r.source, /S-011 history/);
    assert.equal(r.evidence, `#round-two-evidence-${r.skill}`);
  }
  assert.equal(records.find((r) => r.skill === 'land').kept.keptStart, true, 'land kept no attempt');
});

test('the seam refuses a loop recorded twice', () => {
  assert.throws(() => skillTrends([multiLoopFixture[0], multiLoopFixture[0]]), /recorded twice/);
});

test('the fixture loop that kept no attempt keeps its start score and says so', () => {
  const out = text(render(multiLoopFixture));
  assert.match(out, /Loop 5, no attempt kept, so the start version fx0005 stands: 15 of 20 checks \(75%\), Functional\./);
  assert.match(out, /Restart after loop 3 \(new test contract\), version fx0004 measured again: 8 of 20 checks \(40%\)/);
  assert.match(out, /Restart after loop 5 \(new model\)/);
});

test('the page shows no invented loop: only the recorded loops render, and no fixture is imported', () => {
  const out = render(recordedLoops());
  const loops = [...out.matchAll(/data-trend-point="(?:start|loop)" data-loop="(\d+)"/g)].map((m) => Number(m[1]));
  assert.equal(loops.length, 10, 'two points for each of five skills');
  assert.deepEqual([...new Set(loops)].sort(), [0, 1]);
  assert.doesNotMatch(out, /fixture|fx-v|fx0/i);
  for (const file of ['page.tsx', 'skill-trends.tsx', 'skill-loops.ts', 'view.tsx']) {
    assert.doesNotMatch(fs.readFileSync(path.join(siteDir, 'app/rsi', file), 'utf8'), /from ["'][^"']*fixtures/, `${file} imports a fixture`);
  }
  const html = fs.readFileSync(path.join(siteDir, '.next/server/app/rsi.html'), 'utf8');
  assert.equal((html.match(/data-trend-point="(?:start|loop)"/g) ?? []).length, 10, 'built page points');
  assert.doesNotMatch(html, /fixture-skill|fx-v1/);
});

test('each skill states its test contract, deciding tier and model, and outcome', () => {
  const out = render(recordedLoops());
  for (const [skill, want] of Object.entries(RECORDED)) {
    const start = out.indexOf(`data-trend-skill="${skill}"`);
    const t = text(out.slice(start, out.indexOf('data-trend-skill=', start + 1))).replace(/ ,/g, ',');
    assert.match(t, new RegExp(`Test contract ${want.contract}, deciding tier Mid, ${MID}`), `${skill} provenance`);
  }
  const t = text(out);
  for (const outcome of ['Merged: Broken 80% at the start, Excellent 93% after loop 1', 'Merged on owner decision: Excellent 100% at the start, Excellent 100% after loop 1', 'Not merged: Broken 89% at the start, Broken 89% after loop 1']) {
    assert.ok(t.includes(outcome), `missing outcome: ${outcome}`);
  }
});

test('the fitness level per loop strip shows every charted skill by loop, colored and named', () => {
  const tracked = readPage(`<main>${render(recordedLoops())}</main>`, ['data-level-per-loop', 'data-level-row', 'data-level-cell']);
  const rows = tracked.filter((r) => 'data-level-row' in r.attrs);
  assert.deepEqual(rows.map((r) => r.attrs['data-level-row']), Object.keys(RECORDED));
  for (const row of rows) {
    const cells = tracked.filter((r) => 'data-level-cell' in r.attrs && r.ancestors.some((a) => a.attrs === row.attrs));
    const want = RECORDED[row.attrs['data-level-row']].points.map((p) => p[3]);
    assert.deepEqual(cells.map((c) => c.attrs['data-level-cell']), want, `${row.attrs['data-level-row']} cells`);
    for (const c of cells) {
      assert.match(c.attrs.class, new RegExp(`level${c.attrs['data-level-cell']}`), 'cell color follows its level');
      assert.match(c.text, new RegExp(c.attrs['data-level-cell']), 'cell names its level');
      assert.match(c.text, /\d+%/, 'cell gives its score');
    }
  }
  const fixture = readPage(`<main>${render(multiLoopFixture)}</main>`, ['data-level-cell']);
  assert.deepEqual(fixture.map((c) => c.attrs['data-level-cell']), ['Broken', 'Functional', 'Stable', 'Broken', 'Functional', 'Functional', 'Excellent']);
  assert.deepEqual(fixture.filter((c) => c.attrs['data-break']).map((c) => [c.attrs['data-loop'], c.attrs['data-break']]), [['4', 'contract'], ['6', 'model']]);
});

test('the page explains a loop, the point, the level and High/Small, and states every color meaning', () => {
  const out = render(recordedLoops());
  const t = text(out);
  for (const term of ['One loop', 'The plotted point', 'Fitness level', 'High and Small']) assert.ok(t.includes(term), `no explanation of ${term}`);
  assert.match(t, /Alignment Score: checks passed, pooled over the three deciding runs/);
  for (const [level, hue] of [['Excellent', 'green'], ['Stable', 'blue'], ['Functional', 'amber'], ['Broken', 'orange-red, trouble']]) {
    assert.ok(t.includes(`${level} (${hue})`), `legend lacks ${level} (${hue})`);
  }
  assert.match(t, /orange-red means trouble everywhere here/);
  assert.match(t, /never decide a point/);
  assert.match(t, /not a statistical test/);
});

// S-007: no improved-outcome claim without held-out rows, controls, the prior
// version and an interval. A rising Alignment Score is a recorded score only.
test('a climbing score is never called improvement; the claim is reserved for held-out evidence', () => {
  for (const records of [recordedLoops(), multiLoopFixture]) {
    const t = text(render(records));
    assert.doesNotMatch(t, /\b(is|are) improving (that|the|this|each) skill\b|means the loop is improving/i, 'a score trend is presented as improvement');
    assert.match(t, /does not show that RSI improved the skill/);
    assert.match(t, /held-out trials with control arms, the prior version and an interval/);
  }
  assert.match(render(recordedLoops()), /href="#held-out-method"/);
});

test('not-charted skills are stated briefly and carry no score', () => {
  const out = render(recordedLoops());
  const note = text(out.match(/data-not-charted=""[\s\S]*?<\/p>/)?.[0] ?? '');
  assert.match(note, /prune-artifact and writing-for-agents are measured by document length, not an Alignment Score/);
  assert.match(note, /author-skill is on hold/);
  assert.ok(out.includes('href="#round-two-pruning"'));
});

test('skill trends lead the page ahead of the round-two evidence, stay on-site and hide nothing', () => {
  const out = renderToStaticMarkup(createElement(RsiView, { views: seriesViews({ runs: [], results: [] }), unavailable: false },
    createElement(Fragment, null, createElement(SkillTrends, { records: recordedLoops() }), createElement(RoundTwoEvidence))));
  const trends = out.indexOf('id="skill-trends-title"');
  assert.ok(trends > out.indexOf('<h1>RSI results</h1>') && trends < out.indexOf('id="round-two-title"'), 'skill trends must lead the evidence');
  assert.ok(out.indexOf('id="round-two-title"') < out.indexOf('data-split="held-out"'), 'empty trial places follow the results');
  const ids = new Set([...out.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
  for (const [, href] of out.matchAll(/href="([^"]+)"/g)) {
    assert.ok(href.startsWith('#'), `outbound link: ${href}`);
    assert.ok(ids.has(href.slice(1)), `missing on-page target: ${href}`);
  }
  const tracked = readPage(out, ['data-skill-trends', 'data-trend-skill', 'data-level-per-loop', 'data-trend-legend']);
  for (const record of tracked) assert.deepEqual([record, ...record.ancestors].map(hiddenMarker).filter(Boolean), [], `${record.name} is hidden`);
  const trendsOnly = render(recordedLoops());
  assert.deepEqual(quoteProblems(`<main>${trendsOnly}</main>`), []);
  assert.deepEqual(hygieneFindings(trendsOnly), []);
  assert.doesNotMatch(trendsOnly, /github\.com/i);
});

// Must-fail proof: each fault, planted once in the rendered markup, makes the
// named check fail. A fault that no longer applies fails here too.
const [C_POINTS, C_LINES, C_SECONDARY, C_REGRESSION] = Object.keys(CHECKS);
const FIXTURE_FAULTS = [
  ['a contract change joined into one line', C_LINES, (h) => h.replace(/<g data-break="contract">[\s\S]*?<\/g>/, '').replace(/<span[^>]*data-break-label="contract"[^>]*>[^<]*<\/span>/, '').replace('data-trend-line="1" data-contract="fx-v2"', 'data-trend-line="1" data-contract="fx-v1"')],
  ['a model change joined into one line', C_LINES, (h) => h.replace(/<g data-break="model">[\s\S]*?<\/g>/, '').replace(/<span[^>]*data-break-label="model"[^>]*>[^<]*<\/span>/, '').replace('data-contract="fx-v2" data-model="fixture-model-b"', 'data-contract="fx-v2" data-model="fixture-model-a"')],
  ['a point taken from the rejected attempt', C_POINTS, (h) => h.replace('data-loop="2" data-score="17/20"', 'data-loop="2" data-score="20/20"')],
  ['a point taken from a High run', C_POINTS, (h) => h.replace('data-loop="1" data-score="14/20"', 'data-loop="1" data-score="20/20"')],
  ['a High run drawn as a point', C_SECONDARY, (h) => h.replace('data-secondary-mark="High"', 'data-trend-point="loop" data-secondary-mark="High"')],
  ['an attempt not kept left off the chart', C_SECONDARY, (h) => h.replace(/<circle data-not-kept="fx0003r"[\s\S]*?<\/circle>/, '')],
  ['a hidden regression', C_REGRESSION, (h) => h.replace(/<circle data-regression=""[^>]*>(?:<\/circle>)?/, '')],
];
const REAL_FAULTS = [
  ['an invented loop on the page', C_POINTS, (h) => h.replace(/(<circle data-trend-point="loop" data-loop="1"[^>]*>)/, '$1</circle><circle data-trend-point="loop" data-loop="2" data-score="15/15" data-level="Excellent">')],
  ['the land point taken from its last attempt', C_POINTS, (h) => h.replace(/(data-trend-skill="land"[\s\S]*?data-trend-point="loop" data-loop="1" data-score=")16\/18/, '$113/18')],
];

test('each planted fault makes its check fail', async (t) => {
  for (const [faults, html, want] of [[FIXTURE_FAULTS, render(multiLoopFixture), FIXTURE], [REAL_FAULTS, render(recordedLoops()), RECORDED]]) {
    for (const [fault, name, plant] of faults) {
      await t.test(`${fault} fails "${name}"`, () => {
        const planted = plant(html);
        assert.notEqual(planted, html, `the fault "${fault}" no longer applies to the markup`);
        assert.throws(() => CHECKS[name](read(planted), want), assert.AssertionError);
      });
    }
  }
});

// The fitness-level colors (tokens.css site block): Excellent is green, the
// four fills are distinct in each theme, and the text on each fill meets WCAG
// AA contrast (4.5:1) in light and dark.
test('fitness-level tokens: Excellent green, four distinct fills, AA text in both themes', () => {
  const css = fs.readFileSync(path.join(siteDir, 'app/theme/tokens.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
  const rule = (from, sel) => {
    const at = css.indexOf(sel, from);
    assert.ok(at >= 0, `no rule ${sel}`);
    const body = css.slice(css.indexOf('{', at) + 1, css.indexOf('}', at));
    return Object.fromEntries([...body.matchAll(/(--[\w-]+)\s*:\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
  };
  const site = css.indexOf('--level-excellent');
  const siteStart = css.lastIndexOf(':root', site);
  const themes = {
    light: { ...rule(0, ':root,'), ...rule(siteStart, ':root,') },
    dark: { ...rule(0, '[data-theme="dark"]'), ...rule(siteStart, '[data-theme="dark"]') },
  };
  const lum = (hex) => {
    const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  for (const [theme, t] of Object.entries(themes)) {
    const value = (name) => { const v = t[name]; assert.ok(v, `${theme} ${name} missing`); const ref = v.match(/^var\((--[\w-]+)\)$/); return ref ? value(ref[1]) : v; };
    const fills = ['excellent', 'stable', 'functional', 'broken'].map((l) => value(`--level-${l}`).toUpperCase());
    assert.equal(new Set(fills).size, 4, `${theme}: fitness-level fills must differ`);
    const [r, g, b] = [1, 3, 5].map((i) => parseInt(fills[0].slice(i, i + 2), 16));
    assert.ok(g > r * 1.3 && g > b * 1.2, `${theme}: Excellent ${fills[0]} is not green`);
    assert.equal(value('--level-broken'), value('--heat'), `${theme}: Broken must be the trouble hue`);
    for (const l of ['excellent', 'stable', 'functional', 'broken']) {
      const c = ratio(value(`--level-${l}`), value(`--level-${l}-on`));
      assert.ok(c >= 4.5, `${theme} ${l}: text contrast ${c.toFixed(2)} is below 4.5`);
    }
    assert.notEqual(fills[0], value('--agent').toUpperCase(), `${theme}: Excellent must not reuse the agent hue`);
  }
});
