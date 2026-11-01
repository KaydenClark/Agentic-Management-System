// TK-001 acceptance: no color, type or spacing literal exists outside the
// single token file, site/app/theme/tokens.css.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPages, sourceFiles } from './helpers.mjs';

const TOKEN_FILE = 'app/theme/tokens.css';
const COLOR_LITERAL = /#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/i;
const LENGTH_LITERAL = /(?<![\w-])-?\d*\.?\d+(?:px|rem|em|pt|pc|ch|ex|cm|mm|in|vh|vw|vmin|vmax)\b/i;
// Properties whose value must come from a token (or be a CSS-wide keyword).
const TOKEN_ONLY = /^(?:color|background(?:-color)?|border(?:-[a-z]+)*-color|outline-color|fill|stroke|accent-color|caret-color|text-decoration-color|font|font-family|font-size|font-weight|line-height|letter-spacing)$/;
const KEYWORD = /^(?:inherit|initial|unset|revert|currentcolor|transparent|none)$/i;

function declarations(css) {
  const stripped = css.replace(/\/\*[\s\S]*?\*\//g, '');
  return [...stripped.matchAll(/([a-z-]+)\s*:\s*([^;{}]+)(?=[;}])/gi)]
    .map((m) => ({ prop: m[1].toLowerCase(), value: m[2].trim() }));
}

function violations(css) {
  const found = [];
  for (const { prop, value } of declarations(css)) {
    if (prop.startsWith('--')) { found.push(`custom property ${prop} defined outside the token file`); continue; }
    if (COLOR_LITERAL.test(value)) found.push(`${prop}: ${value} (color literal)`);
    if (LENGTH_LITERAL.test(value)) found.push(`${prop}: ${value} (length literal)`);
    if (TOKEN_ONLY.test(prop) && !/^var\(--[\w-]+\)$/.test(value) && !KEYWORD.test(value)) found.push(`${prop}: ${value} (must use a token)`);
  }
  return found;
}

test('the checker catches literals (self-test)', () => {
  assert.ok(violations('a{color:#fff}').length);
  assert.ok(violations('a{padding:1rem}').length);
  assert.ok(violations('a{background:rgb(0 0 0)}').length);
  assert.ok(violations('a{color:red}').length);
  assert.ok(violations('a{font-family:Georgia}').length);
  assert.ok(violations('a{--x:1px}').length);
  assert.deepEqual(violations('a{color:var(--color-text);padding:var(--space-2);margin:0}'), []);
});

test('the token file exists and defines color, type and spacing tokens', () => {
  const tokens = sourceFiles('app/theme', ['tokens.css'])[0];
  assert.ok(tokens, `${TOKEN_FILE} missing`);
  for (const kind of ['--ground:', '--ink:', '--font-', '--text-', '--space-', '--radius-']) assert.ok(tokens.text.includes(kind), `no ${kind} tokens`);
});

test('no CSS outside tokens.css contains a color, type or spacing literal', () => {
  for (const f of sourceFiles('app', ['.css']).filter((f) => f.name !== TOKEN_FILE)) {
    assert.deepEqual(violations(f.text), [], f.name);
  }
});

test('no component source carries a color literal or a literal in an inline style', () => {
  for (const f of sourceFiles('app', ['.tsx', '.ts'])) {
    assert.doesNotMatch(f.text, COLOR_LITERAL, `${f.name}: color literal`);
    for (const m of f.text.matchAll(/style=\{\{([\s\S]*?)\}\}/g)) {
      assert.doesNotMatch(m[1], LENGTH_LITERAL, `${f.name}: length literal in style`);
      assert.doesNotMatch(m[1], /:\s*-?\d/, `${f.name}: numeric literal in style`);
    }
  }
});

test('built pages carry no inline style attributes with literals', () => {
  for (const { name, html } of builtPages()) {
    for (const m of html.matchAll(/\sstyle="([^"]*)"/gi)) {
      assert.deepEqual(violations(`x{${m[1]}}`), [], `${name}: style="${m[1]}"`);
    }
  }
});
