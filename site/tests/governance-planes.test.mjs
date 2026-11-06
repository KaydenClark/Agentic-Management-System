import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import planes from '../content/governance/planes.json' with { type: 'json' };

const glossary = readFileSync(new URL('../../GLOSSARY.md', import.meta.url), 'utf8');
const schema = readFileSync(new URL('../../workbench/wiki/SCHEMA.md', import.meta.url), 'utf8');
const expected = ['Projection','Intent','Enduring Context','Grounding','Canon','Actuality'];
function definitions(text) {
  return expected.map((name, i) => {
    const escaped=name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const match=text.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*\\n([^\\n]+)`));
    assert.ok(match, `missing glossary definition ${name}`);
    return {number:6-i, name, definition:match[1].replace(/^\d+:\s*/, '')};
  });
}
function check(value, text=glossary) {
  assert.deepEqual(value.map(({number,name,definition})=>({number,name,definition})), definitions(text));
  assert.ok(value.every(p=>typeof p.example==='string' && p.example.trim().length>20));
}
test('six displayed claim roles match the authoritative glossary in order',()=>{
  check(planes);
  assert.match(schema, /6 → 5 → 4 → 3 → 2 → 1/);
  assert.match(schema, /1 → 2 → 3 → 4 → 5 → 6/);
});
test('altered, missing and reordered roles or missing examples are rejected',()=>{
  assert.throws(()=>check(planes.slice(1)));
  assert.throws(()=>check([...planes].reverse()));
  assert.throws(()=>check(planes.map((p,i)=>i===0?{...p,definition:'Current truth'}:p)));
  assert.throws(()=>check(planes.map((p,i)=>i===1?{...p,example:''}:p)));
});

const { builtPage, visibleText } = await import('./helpers.mjs');
function pageProblems(html) {
  const section=html.match(/<section\b[^>]*aria-labelledby="governance-stack"[\s\S]*?<\/section>/i)?.[0] ?? '';
  const authority=html.match(/<section\b[^>]*aria-labelledby="authority"[\s\S]*?<\/section>/i)?.[0] ?? '';
  const text=visibleText(section), rules=visibleText(authority);
  const labels=[...text.matchAll(/\b([1-6])\s*\.\s+(Projection|Intent|Enduring Context|Grounding|Canon|Actuality)\b/g)].map(m=>`${m[1]} ${m[2]}`);
  const problems=[];
  if (JSON.stringify(labels)!==JSON.stringify(expected.map((n,i)=>`${6-i} ${n}`))) problems.push('roles missing or out of order');
  if ((text.match(/Example:/g)??[]).length!==6) problems.push('each role needs an example');
  for(const phrase of ['6 → 5 → 4 → 3 → 2 → 1','1 → 2 → 3 → 4 → 5 → 6','classify claims','grants no execution authority']) if(!text.includes(phrase)) problems.push(`missing ${phrase}`);
  for(const term of ['Confirmation','Execution approval','Review','Human QA','Platform safety','AGENTS.md','Example:']) if(!rules.includes(term)) problems.push(`missing ${term}`);
  if(!/href="\/glossary#governance-plane"/.test(section)) problems.push('missing glossary link');
  return problems;
}
test('the built governance page explains roles, authority and both directions',()=>{
  const html=builtPage('governance.html').html;
  assert.deepEqual(pageProblems(html), []);
  assert.ok(pageProblems(html.replace('6 → 5 → 4 → 3 → 2 → 1','missing direction')).length);
  assert.ok(pageProblems(html.replace('aria-labelledby="authority"','aria-labelledby="missing"')).length);
});
