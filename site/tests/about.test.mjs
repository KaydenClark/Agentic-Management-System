// S-003 TK-003: About is about the AMS project (what this repository is, its
// license, its status and how this site was built), not a biography. Its
// license line must match the repository: it says the LICENSE file is empty
// exactly while it is. Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { builtPage, visibleText } from './helpers.mjs';
import { mainOf, repoLinks, repoRoot } from './tour-helpers.mjs';

const EMPTY = /LICENSE file is still empty/;

export function licenseProblems(text, licenseText) {
  const empty = licenseText.trim() === '';
  if (empty && !EMPTY.test(text)) return ['LICENSE is empty but the page does not say so'];
  if (!empty && EMPTY.test(text)) return ['the page says LICENSE is empty but it is not'];
  return [];
}

test('the license check catches a stale line (self-test)', () => {
  assert.deepEqual(licenseProblems('The LICENSE file is still empty.', ''), []);
  assert.deepEqual(licenseProblems('MIT applies.', 'MIT License'), []);
  assert.ok(licenseProblems('MIT applies.', '').length, 'an unstated empty LICENSE passes');
  assert.ok(licenseProblems('The LICENSE file is still empty.', 'MIT License').length, 'a stale empty claim passes');
});

test('/about states the license as the repository has it, sourced to DDR-000R', () => {
  const main = mainOf(builtPage('about.html').html);
  assert.deepEqual(licenseProblems(visibleText(main), readFileSync(join(repoRoot, 'LICENSE'), 'utf8')), []);
  assert.ok(repoLinks(main).some((l) => /ddr\/000R-/.test(l.path) && l.exists), 'no link to DDR-000R');
});

test('/about links the Spec this site is built under', () => {
  const links = repoLinks(mainOf(builtPage('about.html').html));
  assert.ok(links.some((l) => /S-003-showcase-site\/SPEC\.md$/.test(l.path) && l.exists), 'no link to S-003');
});
