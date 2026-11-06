import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loadArticles, contentDir} from '../app/skills/content.mjs';
import {builtPage, siteDir, visibleText} from './helpers.mjs';
import {readPage} from './rsi-html.mjs';

// Exact attribution wording, with public source URIs made readable rather
// than clickable. The existing author, revision, adaptation and license
// statements remain the article's source of truth.
function citationText(nodes) {
  return nodes.map(node => node.type === 'text' || node.type === 'code' ? node.value :
    node.type === 'link' ? `${citationText(node.children)} (${node.href})` : citationText(node.children)).join('');
}
function attributionProblems(html, article) {
  const node = readPage(html, ['data-credit']).find(node => node.attrs['data-credit']);
  if (!node) return ['credit missing'];
  const problems = [];
  const plain = value => value.replace(/\s+/g,' ').trim();
  if (plain(node.text) !== plain(citationText(article.creditText))) problems.push('credit wording, author, change notice or source URI lost');
  const sources = readPage(html, ['data-credit-source']).map(node => node.attrs['data-credit-source']);
  if (JSON.stringify(sources) !== JSON.stringify(article.creditSources)) problems.push('source or license URI identity lost');
  if (/<a\b/i.test(html.match(/<p\b[^>]*data-credit="[^"]*"[^>]*>([\s\S]*?)<\/p>/)?.[1] ?? '')) problems.push('credit is a reader exit');
  return problems;
}

test('every credit retains exact attribution and public URI identities on-site', () => {
  const articles = loadArticles(contentDir(siteDir));
  assert.equal(articles.length,39);
  assert.equal(articles.filter(article => article.creditSources.length).length,28);
  for (const article of articles) {
    assert.deepEqual(attributionProblems(builtPage(`skills/${article.name}.html`).html, article), [], article.name);
  }
  const article = articles.find(article => article.name === 'improve-workbench');
  const html = builtPage('skills/improve-workbench.html').html;
  const text = visibleText(html);
  for (const value of ['Ryan Lopopolo','Harness Engineering','226c8d35','CC BY 4.0','ownership routing, feedback records and dispositions added','https://github.com/lopopolo/harness-engineering','https://creativecommons.org/licenses/by/4.0/']) assert.ok(text.includes(value),value);
  assert.ok(attributionProblems(html.replace('Ryan Lopopolo','Unknown'),article).length);
  assert.ok(attributionProblems(html.replace('226c8d35',''),article).length);
  assert.ok(attributionProblems(html.replaceAll('https://creativecommons.org/licenses/by/4.0/',''),article).length);
  assert.ok(attributionProblems(html.replace('ownership routing, feedback records and dispositions added',''),article).length);
});
