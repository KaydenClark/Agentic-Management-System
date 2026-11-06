// S-007 TK-002: /rsi reads Supabase on the server only. The publishable key
// may live in the server bundle but never in anything the site serves: the
// prerendered pages, their RSC payloads, or client JS and CSS. Run after
// `npm run build`; when the build ran with NEXT_PUBLIC_SUPABASE_ANON_KEY set,
// the exact value is searched for too.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { servedFiles } from './helpers.mjs';

test('no Supabase publishable key appears in served output', () => {
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const files = servedFiles();
  assert.ok(files.length > 0, 'no served files found; run npm run build');
  for (const { name, text } of files) {
    assert.doesNotMatch(text, /sb_publishable_/, `${name} carries a publishable key`);
    if (key) assert.ok(!text.includes(key), `${name} carries the build's publishable key`);
  }
});
