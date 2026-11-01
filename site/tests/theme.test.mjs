// TK-001: light and dark follow the system and a manual toggle overrides it,
// persisted in localStorage. The browser check (npm run check:browser)
// exercises the toggle; these tests pin the pieces it relies on.
// Theme source: the owner's design canvas "Grilling Board Redesign",
// Color system v2.2 (token names kept exactly as the canvas names them).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { builtPages, siteDir } from './helpers.mjs';

const tokenPath = join(siteDir, 'app', 'theme', 'tokens.css');
const tokens = () => {
  assert.ok(existsSync(tokenPath), 'app/theme/tokens.css missing');
  return readFileSync(tokenPath, 'utf8');
};

// Color system v2.2 base tokens, per theme (owner canvas, Main.dc.html).
const V22 = {
  dark: { ground: '#0A0A0A', surface: '#191919', raised: '#232323', line: '#333333', 'line-strong': '#757575', muted: '#A8A8A8', ink: '#F7F7F7', pole: '#FFFFFF', heat: '#FF5A1F', worth: '#FFD60A', owner: '#4C9BE8', agent: '#3DBE5A', returned: '#A66BE0', 'soft-pct': '22%', 'line-pct': '62%', 'dot-pct': '80%' },
  light: { ground: '#F7F7F7', surface: '#FFFFFF', raised: '#EFEFEF', line: '#E0E0E0', 'line-strong': '#808080', muted: '#474747', ink: '#0A0A0A', pole: '#000000', heat: '#F04E12', worth: '#F5C400', owner: '#2F86DC', agent: '#27A046', returned: '#A66BE0', 'soft-pct': '22%', 'line-pct': '68%', 'dot-pct': '72%' },
};

// The declarations of the first rule whose selector list matches `selector`.
function block(css, selector) {
  const stripped = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const re = new RegExp(`(^|[},])\\s*([^{}]*${selector.replace(/[[\]().*+?^$|\\]/g, '\\$&')}[^{}]*)\\{([^{}]*)\\}`, 'm');
  const m = stripped.match(re);
  assert.ok(m, `no rule for ${selector}`);
  return Object.fromEntries([...m[3].matchAll(/(--[\w-]+)\s*:\s*([^;]+);?/g)].map((d) => [d[1].slice(2), d[2].trim()]));
}

function darkMediaBlock(css) {
  const stripped = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const m = stripped.match(/@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*([^{}]*)\{([^{}]*)\}\s*\}/);
  assert.ok(m, 'no @media (prefers-color-scheme: dark) rule');
  assert.match(m[1], /:root:not\(\[data-theme="light"\]\)/, 'system dark rule must yield to a manual light choice');
  return Object.fromEntries([...m[2].matchAll(/(--[\w-]+)\s*:\s*([^;]+);?/g)].map((d) => [d[1].slice(2), d[2].trim()]));
}

test('light is the default, a manual dark choice applies, and both carry the v2.2 values', () => {
  const css = tokens();
  const light = block(css, '[data-theme="light"]');
  const root = block(css, ':root');
  const dark = block(css, '[data-theme="dark"]');
  for (const [name, value] of Object.entries(V22.light)) {
    assert.equal(light[name]?.toUpperCase(), value.toUpperCase(), `light --${name}`);
    assert.equal(root[name]?.toUpperCase(), value.toUpperCase(), `:root --${name}`);
  }
  for (const [name, value] of Object.entries(V22.dark)) assert.equal(dark[name]?.toUpperCase(), value.toUpperCase(), `dark --${name}`);
});

test('the system dark preference uses exactly the manual dark values', () => {
  const css = tokens();
  assert.deepEqual(darkMediaBlock(css), block(css, '[data-theme="dark"]'));
});

test('every page applies a stored choice before first paint with a first-party inline script', () => {
  for (const { name, html } of builtPages()) {
    const head = html.match(/<head>([\s\S]*?)<\/head>/i);
    assert.ok(head, `${name}: no <head>`);
    const inline = [...head[1].matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
    assert.ok(inline.some((s) => s.includes('localStorage') && s.includes('data-theme')), `${name}: no inline theme script in <head>`);
  }
});

test('each color token states its one meaning (DDR-000M)', () => {
  const lines = tokens().split('\n');
  let colors = 0;
  lines.forEach((line, i) => {
    const m = line.match(/^\s*(--[\w-]+)\s*:\s*(#[0-9a-f]{3,8}|color-mix\()/i);
    if (!m) return;
    colors += 1;
    const sameLine = /\/\*.+\*\//.test(line);
    const prevLine = /^\s*\/\*.+\*\/\s*$/.test(lines[i - 1] ?? '');
    assert.ok(sameLine || prevLine, `${m[1]} (line ${i + 1}) has no meaning comment`);
  });
  assert.ok(colors > 0, 'no color tokens defined');
  const css = lines.join('\n');
  assert.match(css, /Grilling Board Redesign/, 'token file does not name its source');
  assert.match(css, /Color system v2\.2/, 'token file does not name the color system version');
});
