// TK-001 acceptance: a page's footer SHA must equal the build's commit and
// keep that identity on-site. Fails if any page shows another SHA.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPages, expectedCommit } from './helpers.mjs';


test('every built page shows the build commit in its footer, without an outbound link', () => {
  const sha = expectedCommit();
  assert.match(sha, /^[0-9a-f]{40}$/, 'expected a full 40-character commit SHA');
  const pages = builtPages();
  assert.ok(pages.length > 0, 'no built pages found');
  for (const { name, html } of pages) {
    const footer = html.match(/<footer[\s\S]*?<\/footer>/i);
    assert.ok(footer, `${name}: no <footer>`);
    const link = footer[0].match(/<span[^>]*data-commit-sha="([^"]*)"[^>]*>/i);
    assert.ok(link, `${name}: footer has no commit identity`);
    assert.equal(link[1], sha, `${name}: footer SHA ${link[1]} differs from the build commit ${sha}`);
    assert.doesNotMatch(footer[0], /href="https:\/\/github\.com/, `${name}: footer sends readers to GitHub`);
  }
});
