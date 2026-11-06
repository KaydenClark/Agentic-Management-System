import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const page = readFileSync(new URL('../app/grill-board-demo/page.tsx', import.meta.url), 'utf8');
const board = readFileSync(new URL('../app/grill-board-demo/Board.tsx', import.meta.url), 'utf8');

test('the demo distinguishes its local simulation from the current DQC lifecycle', () => {
  assert.match(page, /exact.*readback/i);
  assert.match(page, /round/i);
  assert.match(page, /does not.*(?:start|dispatch).*implementation/i);
  assert.doesNotMatch(page, /Answered · awaiting an agent|then as <strong>Applied/);
  assert.doesNotMatch(page, /<AgentBanner\s*\/>/);
  assert.doesNotMatch(board, /Confirmed, ready to promote|Promote selected/);
});
