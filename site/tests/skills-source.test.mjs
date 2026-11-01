// S-008: the skills source check's own planted-fault self-test, on fixtures
// only (the skills repository is private and absent in CI). The real check is
// `npm run check:skills-source -- --skills DIR` (tests/skills-source.check.mjs).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { selfTestProblems } from './skills-source.mjs';

test('the source check reports a copied run without its words, a missing folder and a wrong pin (self-test)', () => {
  assert.deepEqual(selfTestProblems(), []);
});
