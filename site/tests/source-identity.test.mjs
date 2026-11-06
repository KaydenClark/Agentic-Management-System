import './tsx-register.mjs';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {contentHash} from '../scripts/page-hash.mjs';
const {Source} = await import('../app/tour/Source.tsx');
const render = props => `<main id="main">${renderToStaticMarkup(createElement(Source, props, 'Record'))}</main>`;

test('current build provenance stays available without invalidating unrelated content hashes', () => {
  const before = process.env.AMS_COMMIT_SHA;
  try {
    process.env.AMS_COMMIT_SHA = 'a'.repeat(40);
    const first = render({path:'GLOSSARY.md'});
    process.env.AMS_COMMIT_SHA = 'b'.repeat(40);
    const second = render({path:'GLOSSARY.md'});
    assert.ok(first.includes('a'.repeat(40)) && second.includes('b'.repeat(40)));
    assert.equal(contentHash(first),contentHash(second));
    assert.notEqual(contentHash(second),contentHash(render({path:'BLUEPRINT.md'})));
    const historical = render({path:'GLOSSARY.md',revision:'a'.repeat(40)});
    assert.notEqual(contentHash(historical),contentHash(render({path:'GLOSSARY.md',revision:'a'.repeat(39)+'b'})));
    assert.doesNotMatch(first,/<a\b/);
  } finally {
    if (before === undefined) delete process.env.AMS_COMMIT_SHA;
    else process.env.AMS_COMMIT_SHA = before;
  }
});
