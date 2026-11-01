// Checks the prerendered demo Grill Board page (prototype, S-009).
// Run after `npm run build`: node --test tests/

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const site = join(dirname(fileURLToPath(import.meta.url)), "..");
const htmlPath = join(site, ".next/server/app/grill-board-demo.html");

function loadHtml() {
  assert.ok(existsSync(htmlPath), `missing ${htmlPath}; run npm run build first`);
  return readFileSync(htmlPath, "utf8");
}

// Visible text only: drop scripts, styles and tags, decode the few entities React emits.
function textOf(fragment) {
  return fragment
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&#x27;|&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ");
}

// Each list row is a <button data-card-row> with no nested button.
function rows(html) {
  return [...html.matchAll(/<button[^>]*data-card-row="([^"]+)"[^>]*>([\s\S]*?)<\/button>/g)].map((m) => ({
    id: m[1],
    text: textOf(m[2]),
  }));
}

function openCard(html) {
  const start = html.indexOf("data-open-card=");
  assert.ok(start > 0, "the open card is rendered");
  const end = html.indexOf("</article>", start);
  return textOf(html.slice(start, end));
}

const FORBIDDEN = /pull request|branch|commit|repo|deploy|code/i;

test("every card is labeled Sample", () => {
  const html = loadHtml();
  const list = rows(html);
  assert.equal(list.length, 8, "all eight sample cards are in the page");
  for (const r of list) assert.match(r.text, /\bSample\b/, `row ${r.id} shows Sample`);
  assert.match(openCard(html), /\bSample\b/, "the open card shows Sample");
});

test("no card text is about code or tooling", () => {
  const html = loadHtml();
  for (const r of rows(html)) assert.doesNotMatch(r.text, FORBIDDEN, `row ${r.id}`);
  assert.doesNotMatch(openCard(html), FORBIDDEN, "open card");
  // Cards that are not open carry their full text only in the page payload
  // (escaped JSON inside inline scripts); check every text field there too.
  const payload = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
  const fields = [
    ...payload.matchAll(
      /\\"(short|title|pWhy|vWhy|q|why|rec|owner|changes|impact|history|historyCount|flagText|label|hint|name|note|frame|goal)\\":\\"((?:[^"\\]|\\\\.)*)\\"/g,
    ),
  ];
  assert.ok(fields.filter((f) => f[1] === "q").length >= 8, "every card's question is in the payload");
  for (const [, key, value] of fields) assert.doesNotMatch(value, FORBIDDEN, `payload ${key}: ${value}`);
});

test("the page references no external origin", () => {
  const html = loadHtml();
  const attrs = [...html.matchAll(/\b(?:src|href|action|srcset|poster|data)=["']([^"']*)["']/gi)].map((m) => m[1]);
  for (const a of attrs) assert.doesNotMatch(a, /^(?:[a-z][a-z0-9+.-]*:)?\/\//i, `attribute value ${a}`);
  const urls = (html.match(/(?:https?:)?\/\/[a-z0-9.-]+\.[a-z]{2,}[^\s"'<>)]*/gi) ?? []).filter(
    (u) => !/^(?:https?:)?\/\/www\.w3\.org\//.test(u),
  );
  assert.deepEqual(urls, [], "no absolute URL in the page");
  assert.doesNotMatch(html, /fonts\.googleapis|fonts\.gstatic/);

  // Stylesheets the page links: fonts are self-hosted, no remote url() or @import.
  const cssLinks = [...html.matchAll(/<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"/g)].map((m) => m[1]);
  assert.ok(cssLinks.length > 0, "page links its stylesheet");
  const chunks = join(site, ".next/static/chunks");
  for (const href of cssLinks) {
    const file = join(chunks, href.split("/").pop());
    assert.ok(existsSync(file), `stylesheet ${href} is built`);
    const css = readFileSync(file, "utf8");
    assert.doesNotMatch(css, /url\(\s*["']?(?:https?:)?\/\//i, `${href} has no remote url()`);
    assert.doesNotMatch(css, /@import/i, `${href} has no @import`);
    assert.match(css, /IBM Plex Sans/, `${href} carries the self-hosted fonts`);
  }
  assert.ok(readdirSync(join(site, ".next/static/media")).some((f) => f.endsWith(".woff2")), "font files are bundled");
});
