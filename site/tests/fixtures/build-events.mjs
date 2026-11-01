// Fixture build_events rows for the /under-the-hood render tests (S-003
// TK-006). Shaped like S-006's public.build_events rows; the text is test
// text, not history, and never reaches the built site. Listed out of time
// order on purpose so the page must sort them. The session id below is made
// up: the page must strip the trailer, not keep it.
const GH = 'https://github.com/KaydenClark/Agentic-Management-System';
const SESSION = ['https://claude.ai/code/', 'session_', '0FixtureFixtureFixture123'].join('');

export const FIXTURE_ROWS = Object.freeze([
  {
    id: 40, kind: 'return', subject: 'PR 26', summary: 'Closed unmerged: fixture sync attempt',
    occurred_at: '2026-11-01T13:44:05+00:00', source_url: `${GH}/pull/26`, is_test: false,
    detail: { pr: 26, reason: 'closed unmerged' },
  },
  {
    id: 10, kind: 'spec', subject: 'S-900', summary: 'S-900 - Fixture spec',
    occurred_at: '2026-11-01T12:56:08+00:00', source_url: `${GH}/blob/0000000/fixture/SPEC.md`, is_test: false,
    detail: { status: 'active' },
  },
  {
    id: 30, kind: 'correction', subject: 'PR 16', summary: 'Load fixture card contents from committed records only',
    occurred_at: '2026-11-01T13:20:00+00:00', source_url: `${GH}/pull/16#discussion_r1`, is_test: false,
    detail: { pr: 16, reviewer: 'fixture-reviewer' },
  },
  {
    id: 20, kind: 'commit', subject: 'abc1234', summary: `Add the fixture page Claude-Session: ${SESSION}`,
    occurred_at: '2026-11-01T13:05:00+00:00', source_url: `${GH}/commit/abc1234`, is_test: false,
    detail: { author: 'Kayden Clark' },
  },
  {
    id: 21, kind: 'commit', subject: 'def5678', summary: `Wire the fixture reader (see ${SESSION})`,
    occurred_at: '2026-11-01T13:06:00+00:00', source_url: `${GH}/commit/def5678`, is_test: false,
    detail: { author: 'Claude' },
  },
  {
    id: 25, kind: 'task_claimed', subject: 'S-900 TK-001', summary: 'Claim S-900 TK-001',
    occurred_at: '2026-11-01T13:10:00+00:00', source_url: `${GH}/commit/1111111`, is_test: false,
    detail: { spec: 'S-900', task: 'TK-001' },
  },
  {
    id: 12, kind: 'task', subject: 'S-900 TK-001', summary: 'Render the fixture rows in time order',
    occurred_at: '2026-11-01T12:57:00+00:00', source_url: `${GH}/blob/0000000/fixture/TASK.md`, is_test: false,
    detail: { spec: 'S-900', task: 'TK-001' },
  },
  {
    id: 35, kind: 'correction_fix', subject: '2222222', summary: 'Fix for review finding: fixture cards',
    occurred_at: '2026-11-01T13:24:22+00:00', source_url: `${GH}/commit/2222222`, is_test: false,
    detail: {},
  },
  {
    id: 36, kind: 'merge', subject: 'PR 16', summary: 'Merge the fixture board',
    occurred_at: '2026-11-01T13:30:00+00:00', source_url: `${GH}/commit/3333333`, is_test: false,
    detail: { pr: 16 },
  },
  // A test row: RLS hides these from the site key, and the page must drop one
  // that slips through anyway.
  {
    id: 99, kind: 'commit', subject: 'test999', summary: 'HIDDEN TEST ROW must never render',
    occurred_at: '2026-11-01T13:15:00+00:00', source_url: `${GH}/commit/9999999`, is_test: true,
    detail: {},
  },
  // No https source: cannot be linked, so it is not shown and is counted.
  {
    id: 98, kind: 'commit', subject: 'nolink1', summary: 'UNLINKED ROW must never render',
    occurred_at: '2026-11-01T13:16:00+00:00', source_url: null, is_test: false,
    detail: {},
  },
]);

// The order the shown rows must appear in: occurred_at, then id.
export const FIXTURE_ORDER = [10, 12, 20, 21, 25, 30, 35, 36, 40];
