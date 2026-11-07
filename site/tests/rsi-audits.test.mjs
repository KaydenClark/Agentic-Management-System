import './tsx-register.mjs';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const {loadSkillAudits}=await import('../app/rsi/audits.ts');
const {AuditEvidence}=await import('../app/rsi/audit-view.tsx');
const env={NEXT_PUBLIC_SUPABASE_URL:'https://fixture.supabase.co',NEXT_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_fixture'};
const row={audit_run_id:'run-1',audit_set_id:'set-1',skill:'journey',skills_commit:'a'.repeat(40),contract_version:'skill-audit-v1',contract_digest:'b'.repeat(64),provider:'openai',model:'codex',model_tier:'mid',quality_passed:3,quality_total:4,regression_passed:2,regression_total:2,critical_missed:true,evidence_complete:true,passed:false,completed_at:'2026-11-07T12:00:00Z',recorded_at:'2026-11-07T12:01:00Z'};
const ok=body=>({ok:true,status:200,json:async()=>body});
const render=(loaded,now=Date.parse('2026-11-07T12:02:00Z'))=>renderToStaticMarkup(createElement(AuditEvidence,{loaded,now}));
test('reads public projection and shows completed failures with provenance and independent scores',async()=>{
 let call; const loaded=await loadSkillAudits({env,fetchImpl:async(url,init)=>{call={url:new URL(url),init};return ok([{...row,private_field:'SECRET'}]);}});
 assert.equal(loaded.ok,true); assert.equal(call.url.pathname,'/rest/v1/rsi_skill_audit_results'); assert.equal(call.url.searchParams.get('order'),'completed_at.desc,audit_run_id.asc'); assert.equal(call.url.searchParams.has('is_test'),false); assert.equal(call.init.headers.Authorization,undefined); assert.ok(!JSON.stringify(loaded).includes('SECRET')); assert.ok(render({...loaded,readAt:'2026-11-07T12:01:00Z'}).includes('href="#rsi-audit-run-1"'));
 const html=render({...loaded,readAt:'2026-11-07T12:01:00Z'}); for(const text of ['1 completed audit','Failed','3 of 4','2 of 2','Missed','run-1','set-1',row.skills_commit,row.contract_digest,'openai','codex','mid'])assert.ok(html.includes(text),text);
});
test('empty, failed, stale and incomplete audit states are distinct',async()=>{
 const empty=await loadSkillAudits({env,fetchImpl:async()=>ok([])}); assert.match(render({...empty,readAt:'2026-11-07T12:01:00Z'}),/No completed public audits/);
 const failed=await loadSkillAudits({env,fetchImpl:async()=>({ok:false,status:503})}); assert.match(render(failed),/count is unknown/i); assert.doesNotMatch(render(failed),/No completed public audits/);
 const loaded=await loadSkillAudits({env,fetchImpl:async()=>ok([{...row,critical_missed:null,evidence_complete:false,passed:null}])}); const html=render({...loaded,readAt:'2026-11-07T11:00:00Z'}); assert.match(html,/data-read-state="stale"/);assert.match(html,/Incomplete/);assert.match(html,/Unknown/);
});
test('refuses malformed identities, conflicting rows and recognized secret credentials',async()=>{
 for(const rows of [[{...row,skills_commit:'private/path'}],[row,row]])assert.equal((await loadSkillAudits({env,fetchImpl:async()=>ok(rows)})).ok,false);
 let called=false;const result=await loadSkillAudits({env:{...env,NEXT_PUBLIC_SUPABASE_ANON_KEY:'sb_secret_fixture'},fetchImpl:async()=>{called=true;return ok([])}});assert.equal(result.ok,false);assert.equal(called,false);
});

test('model handles with slashes and legacy anon JWTs work; service JWTs never leave',async()=>{
 const jwt=role=>'x.'+Buffer.from(JSON.stringify({role})).toString('base64url')+'.x'; let headers;
 const out=await loadSkillAudits({env:{...env,NEXT_PUBLIC_SUPABASE_ANON_KEY:jwt('anon')},fetchImpl:async(url,init)=>{headers=init.headers;return ok([{...row,model:'openai/codex'}])}}); assert.equal(out.ok,true); assert.equal(headers.Authorization,'Bearer '+jwt('anon'));
 let called=false;const denied=await loadSkillAudits({env:{...env,NEXT_PUBLIC_SUPABASE_ANON_KEY:jwt('service_role')},fetchImpl:async()=>{called=true;return ok([])}}); assert.equal(denied.ok,false);assert.equal(called,false);
});

test('empty score denominators are unavailable and do not create an assessment grade',async()=>{
 const loaded=await loadSkillAudits({env,fetchImpl:async()=>ok([{...row,quality_passed:0,quality_total:0,regression_passed:0,regression_total:0,passed:null,evidence_complete:false,critical_missed:null}])});
 const html=render(loaded);assert.match(html,/Quality: score unavailable/);assert.match(html,/Regression: score unavailable/);assert.doesNotMatch(html,/0 of 0/);assert.match(html,/whole assessment grade/);
});
