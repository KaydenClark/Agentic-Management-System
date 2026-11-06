import {test} from 'node:test';
import assert from 'node:assert/strict';
import {builtPages} from './helpers.mjs';
import {isReaderHref} from '../app/reader-links.mjs';
import {readerLinkProblems} from './reader-links.mjs';

const pages = target => [{name:'index.html',html:`<main id="main"><a href="${target}">Read</a></main>`},{name:'start.html',html:'<main id="main"><h2 id="meaning">Meaning</h2></main>'}];
test('reader policy rejects external, disguised and broken destinations', () => {
  assert.deepEqual(readerLinkProblems(pages('/start#meaning')), []);
  for (const target of ['https://github.com/x/y','HTTPS://GitHub.COM/x/y','//github.com/x/y','/\\github.com/x/y','https&#58;//github.com/x/y','mailto:x@example.com','/start#missing','/missing#meaning']) {
    assert.ok(readerLinkProblems(pages(target)).length, target);
  }
  assert.ok(!isReaderHref('\nhttps://example.com'));
  assert.ok(!isReaderHref('/start\n'));
  assert.deepEqual(readerLinkProblems(pages('#main')), []);
});
test('every built reader link stays on-site and resolves its page and fragment', () => {
  assert.deepEqual(readerLinkProblems(builtPages()), []);
});
