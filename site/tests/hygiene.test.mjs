// TK-005: public hygiene and no third-party loads, over every file the built
// site serves (npm test; browser-free). The planted-fault cases plant into a
// copy of a real built page, so they prove the scan reads built output.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, servedFiles } from './helpers.mjs';
import { externalResources, hygieneFindings } from './hygiene.mjs';

const kindOf = (name) => (name.endsWith('.css') ? 'css' : name.endsWith('.html') ? 'html' : 'other');
const labels = (text) => hygieneFindings(text).map((f) => f.label);

// Fake values, assembled at run time so this file holds no key-shaped or
// path-shaped literal of its own.
const PLANTED = [
  ['host path', ['/ho', 'me/someone/project/site/app/page.tsx'].join('')],
  ['host path', ['/Us', 'ers/someone/Code/site'].join('')],
  ['host path', ['C:', '\\Users\\someone\\site'].join('')],
  ['host path', ['file:', '///C:/Users/someone/site'].join('')],
  ['host path', ['file:', '///tmp/build/site'].join('')],
  ['Supabase secret key', ['sb_', 'secret_', 'AbCdEf0123456789'].join('')],
  ['Supabase service role', ['service', '_role'].join('')],
  ['JWT-shaped token', ['ey', 'JhbGciOiJIUzI1NiJ9', '.', 'eyJyb2xlIjoiYW5vbiJ9', '.sig'].join('')],
  ['API token', ['gh', 'p_', 'a'.repeat(36)].join('')],
  ['email address', ['someone', '@', 'example.com'].join('')],
  ['private repository reference', ['GPT', '_OS'].join('')],
  ['agent session trace', ['claude.ai/code/', 'session_', '01AbCdEfGhIjKlMnOpQrStUv'].join('')],
];

test('hygiene: each planted fault in a copy of a built page is caught', () => {
  const { html } = builtPage('index.html');
  assert.deepEqual(labels(html), [], 'the unplanted copy must be clean for this test to mean anything');
  for (const [label, value] of PLANTED) {
    const planted = html.replace('</main>', `<p>${value}</p></main>`);
    assert.ok(labels(planted).includes(label), `planted ${label} not caught`);
  }
});

test('hygiene: the Supabase publishable key and ordinary prose pass', () => {
  assert.deepEqual(labels('sb_publishable_AbCdEf0123 ships; skills-installed-here; /homepage; the service role'), []);
  // Turbopack's runtime template for module file URLs names no machine.
  assert.deepEqual(labels('_.F=function(e,t){return`file:///${encodeURIComponent(t??"ROOT")}/`}'), []);
});

test('hygiene: no served file holds a host path, key, token or private record', () => {
  const files = servedFiles();
  assert.ok(files.some((f) => f.name.endsWith('.html')) && files.some((f) => f.name.endsWith('.js')), 'served output not found');
  const bad = files.flatMap((f) => hygieneFindings(f.text).map((x) => `${f.name} @${x.offset}: ${x.label}`));
  assert.deepEqual(bad, []);
});

test('third parties: each planted external font, script or stylesheet in a copy of a built page is caught', () => {
  const { html } = builtPage('index.html');
  assert.deepEqual(externalResources(html, 'html'), []);
  const plants = [
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter"/>',
    '<link rel="preconnect" href="https://fonts.gstatic.com"/>',
    '<script src="https://cdn.example.com/x.js"></script>',
    '<style>@font-face{font-family:X;src:url(https://fonts.gstatic.com/x.woff2)}</style>',
    '<img srcset="/a.png 1x, //cdn.example.com/a@2x.png 2x"/>',
    // A local first attribute must not hide an external one on the same tag.
    '<img src="/a.png" srcset="https://cdn.example.com/a.png 2x"/>',
    '<img alt="x" src="/a.png" srcset="/a.png 1x, /b.png 2x, https://cdn.example.com/c.png 3x"/>',
    '<video src="/v.mp4" poster="https://cdn.example.com/p.png"></video>',
    '<link rel="preload" as="image" href="/a.png" imagesrcset="https://cdn.example.com/a.png 2x"/>',
    '<object data="https://cdn.example.com/x.swf"></object>',
    '<form action="https://forms.example.com/submit"></form>',
    '<form action="/ok"><button formaction="https://forms.example.com/b">Go</button></form>',
    '<svg><image href="/a.png" xlink:href="https://cdn.example.com/a.svg"/></svg>',
    '<a href="/ok" ping="https://track.example.com/p">ok</a>',
    '<div style="background:url(https://cdn.example.com/bg.png)"></div>',
    "<img src='/a.png' srcset='https://cdn.example.com/single-quoted.png 2x'/>",
  ];
  for (const plant of plants) {
    assert.equal(externalResources(html.replace('</head>', `${plant}</head>`), 'html').length, 1, plant);
  }
  assert.equal(externalResources('@import "https://fonts.googleapis.com/css2?family=Inter";', 'css').length, 1);
  assert.equal(externalResources('a{background:url(/_next/static/media/x.woff2)}', 'css').length, 0);
  assert.equal(externalResources('<script src="https://abc.supabase.co/x.js"></script>', 'html').length, 0);
  // Links are not loads: an <a> or <area> href to another host passes.
  assert.equal(externalResources('<a href="https://example.com/">x</a><area href="https://example.com/"/>', 'html').length, 0);
  assert.equal(externalResources('<img src="/a.png" srcset="/a.png 1x, /b.png 2x"/><video src="/v.mp4" poster="/p.png"></video>', 'html').length, 0);
});

test('third parties: served HTML and CSS load nothing from another host but Supabase and GitHub', () => {
  const bad = servedFiles()
    .filter((f) => kindOf(f.name) !== 'other')
    .flatMap((f) => externalResources(f.text, kindOf(f.name)).map((u) => `${f.name}: ${u}`));
  assert.deepEqual(bad, []);
});
