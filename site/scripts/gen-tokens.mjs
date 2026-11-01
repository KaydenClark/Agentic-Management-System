// Generates the theme block of app/theme/tokens.css from
// ../grill-board/theme/tokens.json (DDR-000Y), the one record of the Grill
// Board theme. tests/tokens-json.test.mjs checks the block in tokens.css is
// this output byte for byte, so the block is never edited by hand.
//
//   node scripts/gen-tokens.mjs           print the block
//   node scripts/gen-tokens.mjs --write   replace the block in tokens.css
//
// The block holds the light rule, the manual dark rule, the system-dark rule
// and the .tone/.h-* mix rules. Type and spacing tokens are not in
// tokens.json; they stay hand-written outside the markers.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const siteDir = fileURLToPath(new URL('..', import.meta.url));
export const JSON_PATH = `${siteDir}../grill-board/theme/tokens.json`;
export const CSS_PATH = `${siteDir}app/theme/tokens.css`;
export const BEGIN = '/* BEGIN theme tokens: generated from grill-board/theme/tokens.json by scripts/gen-tokens.mjs; do not edit */';
export const END = '/* END theme tokens */';

function rule(selector, decls, meanings, indent = '') {
  const lines = Object.entries(decls).map(([name, value]) => {
    const meaning = meanings[name] ? ` /* ${meanings[name]} */` : '';
    return `${indent}  ${name}: ${value};${meaning}`;
  });
  return `${indent}${selector} {\n${lines.join('\n')}\n${indent}}`;
}

// The text that goes between BEGIN and END, starting and ending with a newline.
export function generate(json) {
  const { themes, meanings, mixes } = json;
  const light = { ...themes.light, 'color-scheme': 'light' };
  const dark = { ...themes.dark, 'color-scheme': 'dark' };
  const parts = [
    `/* Source: ${json.source.artifact}, version ${json.source.version}. Light is the default. */`,
    rule(':root,\n[data-theme="light"],\n.t-light', light, meanings),
    '/* A manual dark choice. */',
    rule('[data-theme="dark"],\n.t-dark', dark, meanings),
    '/* The system dark preference, unless the reader chose light. */',
    `@media (prefers-color-scheme: dark) {\n${rule(':root:not([data-theme="light"])', dark, meanings, '  ')}\n}`,
    '/* Mixes: pick a hue with .h-*, then use the .tone tokens. */',
    ...Object.entries(mixes).map(([selector, decls]) => rule(selector, decls, meanings)),
  ];
  return `\n${parts.join('\n\n')}\n`;
}

// Splits tokens.css text into [before, block, after] around the markers.
export function split(css) {
  const b = css.indexOf(BEGIN);
  const e = css.indexOf(END);
  if (b === -1 || e === -1 || e < b) throw new Error('tokens.css: BEGIN/END theme token markers missing or out of order');
  return [css.slice(0, b), css.slice(b + BEGIN.length, e), css.slice(e + END.length)];
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const block = generate(JSON.parse(readFileSync(JSON_PATH, 'utf8')));
  if (process.argv.includes('--write')) {
    const [before, , after] = split(readFileSync(CSS_PATH, 'utf8'));
    writeFileSync(CSS_PATH, `${before}${BEGIN}${block}${END}${after}`);
    console.log(`wrote the theme block of ${CSS_PATH}`);
  } else {
    process.stdout.write(`${BEGIN}${block}${END}\n`);
  }
}
