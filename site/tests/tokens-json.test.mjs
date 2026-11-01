// S-003 TK-007: every color token in app/theme/tokens.css equals the recorded
// Grill Board token in ../grill-board/theme/tokens.json (DDR-000Y). Both
// themes are checked, including the system-preference dark block, and so are
// the .tone and .h-* mix rules. A color token in one file but not the other
// fails, as does any changed value.
//
// Limit: tokens.json records colors and mixes only. Type and spacing tokens
// are not in it, so they are not compared here; tokens.test.mjs still forbids
// any color, type or spacing literal outside tokens.css.
//
// Vercel builds with root directory site/, so ../grill-board is not present
// there; this check runs in the local `npm test` only.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { siteDir } from './helpers.mjs';

const CSS_PATH = join(siteDir, 'app', 'theme', 'tokens.css');
const JSON_PATH = join(siteDir, '..', 'grill-board', 'theme', 'tokens.json');

const COLOR_VALUE = /#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\(|\bvar\(\s*--[\w-]+\s*[,)]/i;
// CSS named colors would also count; a bare word as a custom property value
// in tokens.css is treated as a color unless it is a known non-color keyword.
const NON_COLOR_WORD = /^(?:light|dark|normal|none|inherit|initial|unset|revert)$/i;

// Parse top-level and @media-nested rules into { selector, media, decls, list }:
// decls keeps the last value per name, list keeps every declaration in order.
export function parseRules(css) {
  const src = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const rules = [];
  const walk = (text, media) => {
    let i = 0;
    while (i < text.length) {
      const open = text.indexOf('{', i);
      if (open === -1) break;
      const head = text.slice(i, open).trim();
      // Find the matching close brace.
      let depth = 1;
      let j = open + 1;
      while (j < text.length && depth) {
        if (text[j] === '{') depth++;
        else if (text[j] === '}') depth--;
        j++;
      }
      const body = text.slice(open + 1, j - 1);
      if (head.startsWith('@')) walk(body, head);
      else {
        const list = [...body.matchAll(/(--[\w-]+)\s*:\s*([^;]+);?/g)].map((m) => [m[1], m[2].trim()]);
        rules.push({ selector: head.replace(/\s+/g, ' '), media, decls: Object.fromEntries(list), list });
      }
      i = j;
    }
  };
  walk(src, null);
  return rules;
}

// Only hex digits are case-insensitive; custom-property names and keywords keep their case.
const norm = (v) => v.replace(/\s+/g, ' ').replace(/\s*([,()])\s*/g, '$1').trim().replace(/#[0-9a-f]{3,8}\b/gi, (h) => h.toUpperCase());
const isColorish = (v) => COLOR_VALUE.test(v) || (/^[a-z]+$/i.test(v) && !NON_COLOR_WORD.test(v));

function themeOf(rule) {
  const sels = rule.selector.split(',').map((s) => s.trim());
  if (rule.media && /prefers-color-scheme:\s*dark/.test(rule.media)) return 'dark';
  if (rule.media) return null;
  if (sels.includes('[data-theme="dark"]')) return 'dark';
  if (sels.includes('[data-theme="light"]')) return 'light';
  return null;
}

function compareDecls(where, actual, expected, out) {
  for (const [name, value] of Object.entries(expected)) {
    if (!(name in actual)) out.push(`${where}: ${name} is in tokens.json but missing from tokens.css`);
    else if (norm(actual[name]) !== norm(value)) out.push(`${where}: ${name} is ${actual[name]} in tokens.css but ${value} in tokens.json`);
  }
  for (const [name, value] of Object.entries(actual)) {
    if (!(name in expected)) out.push(`${where}: ${name}: ${value} is in tokens.css but not in tokens.json`);
  }
}

// A color token may be declared once per rule and never with !important: the
// browser applies an !important or earlier duplicate the last-value compare would miss.
function checkDeclarations(where, rule, expected, out) {
  const isColor = (name, value) => name in expected || isColorish(value.replace(/!\s*important\s*$/i, '').trim());
  const counts = {};
  for (const [name, value] of rule.list) {
    if (!isColor(name, value)) continue;
    counts[name] = (counts[name] || 0) + 1;
    if (/!\s*important/i.test(value)) out.push(`${where}: ${name}: ${value} uses !important`);
  }
  for (const [name, n] of Object.entries(counts)) if (n > 1) out.push(`${where}: ${name} is declared ${n} times in one rule`);
}

// Every difference between a tokens.css text and a parsed tokens.json.
export function differences(css, json) {
  const out = [];
  const seen = { dark: 0, light: 0, mediaDark: 0 };
  const seenMix = new Set();
  for (const rule of parseRules(css)) {
    const theme = themeOf(rule);
    const where = rule.media ? `${rule.media} ${rule.selector}` : rule.selector;
    const mix = !theme && !rule.media && rule.selector in json.mixes ? json.mixes[rule.selector] : null;
    checkDeclarations(where, rule, theme ? json.themes[theme] : mix || {}, out);
    if (theme) {
      if (rule.media) seen.mediaDark++;
      else seen[theme]++;
      compareDecls(where, rule.decls, json.themes[theme], out);
      continue;
    }
    if (!rule.media && rule.selector in json.mixes) {
      seenMix.add(rule.selector);
      compareDecls(where, rule.decls, json.mixes[rule.selector], out);
      continue;
    }
    // Any other rule may hold type and spacing tokens, but no color token.
    // A name recorded in tokens.json may only be set in its recorded rule, whatever its value.
    const recorded = new Set([...Object.values(json.themes), ...Object.values(json.mixes)].flatMap((o) => Object.keys(o)));
    for (const [name, value] of Object.entries(rule.decls)) {
      if (recorded.has(name)) out.push(`${where}: ${name}: ${value} redeclares a recorded token outside its recorded rule`);
      else if (isColorish(value)) out.push(`${where}: ${name}: ${value} is a color token outside the recorded themes and mixes`);
    }
  }
  if (!seen.light) out.push('no [data-theme="light"] rule in tokens.css');
  if (!seen.dark) out.push('no [data-theme="dark"] rule in tokens.css');
  if (!seen.mediaDark) out.push('no @media (prefers-color-scheme: dark) rule in tokens.css');
  for (const sel of Object.keys(json.mixes)) if (!seenMix.has(sel)) out.push(`mix rule ${sel} is in tokens.json but missing from tokens.css`);
  return out;
}

const json = () => JSON.parse(readFileSync(JSON_PATH, 'utf8'));
const css = () => readFileSync(CSS_PATH, 'utf8');

test('every color token in tokens.css equals grill-board/theme/tokens.json, and none is extra or missing', () => {
  assert.deepEqual(differences(css(), json()), []);
});

test('a recorded token redeclared outside its recorded rule is reported, whatever its value', () => {
  // Codex review on PR #32: --soft-pct is a percentage, so a value-shape check missed it.
  const planted = css() + '\n:root { --soft-pct: 0%; }\n';
  assert.ok(differences(planted, json()).some((d) => d.includes('--soft-pct')), 'out-of-place percentage override');
});

test('only the exact recorded theme rules count, each exactly once', () => {
  // Codex review on PR #32: any rule inside a dark-preference media query was accepted as the dark theme.
  const darkDecls = Object.entries(json().themes.dark).map(([k, v]) => `${k}: ${v};`).join(' ');
  const outOfScope = css() + `\n@media (prefers-color-scheme: dark) { [data-theme="light"] { ${darkDecls} } }\n`;
  assert.ok(differences(outOfScope, json()).length > 0, 'dark-preference rule scoped to the light theme');
  const lightDecls = Object.entries(json().themes.light).map(([k, v]) => `${k}: ${v};`).join(' ');
  const twice = css() + `\n[data-theme="light"] { ${lightDecls} }\n`;
  assert.ok(differences(twice, json()).length > 0, 'a second light-theme rule');
});

test('the comparison fails on a copy with a planted stray color', () => {
  const planted = css().replace('--heat: #F04E12;', '--heat: #F04E12;\n  --stray: #FF00FF;');
  assert.notEqual(planted, css(), 'plant site not found in tokens.css');
  assert.deepEqual(differences(planted, json()), [':root, [data-theme="light"], .t-light: --stray: #FF00FF is in tokens.css but not in tokens.json']);
});

test('the comparison fails on a copy with a changed, a missing or an out-of-place color', () => {
  const base = css();
  const changed = base.replace('--owner: #4C9BE8;', '--owner: #4C9BE9;');
  assert.ok(differences(changed, json()).some((d) => d.includes('--owner is #4C9BE9')), 'changed dark value');
  const media = base.replace(/(@media[^{]*\{[^}]*?)--agent: #3DBE5A;/, '$1--agent: #3DBE5B;');
  assert.ok(differences(media, json()).some((d) => d.startsWith('@media') && d.includes('--agent')), 'changed system-dark value');
  const missing = base.replace('--returned: #A66BE0; /* returned (purple): it came back for rework */\n  --soft-pct: 22%;\n  --line-pct: 68%;', '--soft-pct: 22%;\n  --line-pct: 68%;');
  assert.ok(differences(missing, json()).some((d) => d.includes('--returned is in tokens.json but missing')), 'missing light token');
  const stray = base.replace('--space-4: 4px;', '--space-4: 4px;\n  --accent: #123456;');
  assert.ok(differences(stray, json()).some((d) => d.includes('--accent')), 'color token in the type and spacing block');
  const mix = base.replace('.h-none { --hue: var(--line-strong); }', '.h-none { --hue: var(--line); }');
  assert.ok(differences(mix, json()).some((d) => d.startsWith('.h-none')), 'changed mix');
  // Custom-property names are case-sensitive: a wrongly cased reference points at an undefined variable.
  const cased = base.replace('.h-none { --hue: var(--line-strong); }', '.h-none { --hue: var(--LINE-STRONG); }');
  assert.ok(differences(cased, json()).some((d) => d.startsWith('.h-none')), 'wrongly cased custom-property reference');
  const extraMix = base + '\n.h-extra { --hue: var(--heat); }\n';
  assert.ok(differences(extraMix, json()).some((d) => d.startsWith('.h-extra')), 'unrecorded mix rule');
  assert.deepEqual(differences(base, json()), []);
});

test('the comparison fails on a copy with a duplicate or !important color declaration', () => {
  const base = css();
  // The last declaration matches tokens.json, but the !important one wins in the browser.
  const dup = base.replace('--heat: #F04E12;', '--heat: #FF00FF !important; --heat: #F04E12;');
  assert.notEqual(dup, base, 'plant site not found in tokens.css');
  const found = differences(dup, json());
  assert.ok(found.some((d) => d.includes('--heat is declared 2 times')), `duplicate declaration: ${found}`);
  assert.ok(found.some((d) => d.includes('--heat') && d.includes('!important')), `!important: ${found}`);
  const important = base.replace('--worth: #FFD60A;', '--worth: #FFD60A !important;');
  assert.ok(differences(important, json()).some((d) => d.includes('--worth') && d.includes('!important')), 'single !important');
});

test('the comparison fails on a copy with a var() color that has a fallback or inner whitespace', () => {
  const base = css();
  const fallback = base + '\n:root { --heat: var(--worth, red); }\n';
  assert.ok(differences(fallback, json()).some((d) => d.startsWith(':root: --heat')), 'var() with a fallback');
  const spaced = base + '\n:root { --heat: var( --worth ); }\n';
  assert.ok(differences(spaced, json()).some((d) => d.startsWith(':root: --heat')), 'var() with inner whitespace');
});
