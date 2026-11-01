// TK-001 acceptance: a page's footer SHA must equal the build's commit and
// link to that commit on GitHub. Fails if any page shows another SHA.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPages, expectedCommit } from './helpers.mjs';

const REPO_COMMIT = 'https://github.com/KaydenClark/Agentic-Management-System/commit/';

test('every built page shows the build commit in its footer, linked to GitHub', () => {
  const sha = expectedCommit();
  assert.match(sha, /^[0-9a-f]{40}$/, 'expected a full 40-character commit SHA');
  const pages = builtPages();
  assert.ok(pages.length > 0, 'no built pages found');
  for (const { name, html } of pages) {
    const footer = html.match(/<footer[\s\S]*?<\/footer>/i);
    assert.ok(footer, `${name}: no <footer>`);
    const link = footer[0].match(/<a[^>]*data-commit-sha="([^"]*)"[^>]*>/i);
    assert.ok(link, `${name}: footer has no commit link (an <a> with data-commit-sha)`);
    assert.equal(link[1], sha, `${name}: footer SHA ${link[1]} differs from the build commit ${sha}`);
    assert.ok(link[0].includes(`href="${REPO_COMMIT}${sha}"`), `${name}: commit link does not point at ${REPO_COMMIT}${sha}`);
  }
});
