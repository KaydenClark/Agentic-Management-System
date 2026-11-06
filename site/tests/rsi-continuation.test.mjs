// Synthetic contract fixtures only; none are imported by the website.
import './tsx-register.mjs';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const {run,results,V1,V2}=await import('../app/rsi/fixtures/cases.ts');
const {seriesViews,runsWithoutResults}=await import('../app/rsi/data.ts');
const loader=await import('../app/rsi/supabase.ts');
const {RsiView}=await import('../app/rsi/view.tsx');
const first=run({id:801,version:V1,started:'2026-11-01T10:00:00Z'});
const second=run({id:802,version:V2,started:'2026-11-02T10:00:00Z'});
const versionView=data=>seriesViews(data).find(view=>view.id==='dev-per-version');

test('different observed task sets never form one version trend or a regression',()=>{
 const data={runs:[first,second],results:[...results(first,'fixture-easy','dev',[true]),...results(second,'fixture-hard','dev',[false])]};
 const view=versionView(data);assert.equal(view.series.length,2);
 assert.ok(view.series.every(series=>series.points.length===1&&series.points.every(p=>!p.marks.some(m=>m.kind==='regression'))));
 assert.deepEqual(view.series.flatMap(s=>s.points.flatMap(p=>p.rows.map(r=>r.id))).sort(),data.results.map(r=>r.id).sort());
});
test('different per-task attempt coverage is separated even with identical task names',()=>{
 const data={runs:[first,second],results:[...results(first,'fixture-a','dev',[true,true]),...results(first,'fixture-b','dev',[true]),...results(second,'fixture-a','dev',[false]),...results(second,'fixture-b','dev',[false,false])]};
 assert.equal(versionView(data).series.length,2);
});
test('matching observed coverage stays descriptive, retaining failures and denominators',()=>{
 const data={runs:[first,second],results:[...results(first,'fixture-a','dev',[true,null]),...results(second,'fixture-a','dev',[false,null])]};
 const view=versionView(data);assert.equal(view.series.length,1);assert.equal(view.series[0].points.length,2);
 assert.deepEqual(view.series[0].points.map(p=>p.counts.map(c=>[c.key,c.of])),[[['passed',1],['not-graded',1]],[['passed',1],['not-graded',1]]]);
 const html=renderToStaticMarkup(createElement(RsiView,{views:seriesViews(data),unavailable:false}));
 assert.match(html,/immutable case versions.*unknown/i);
});
test('every public run without result rows remains visible with unknown grade',()=>{
 const runs=['running','completed','stopped','failed'].map((state,i)=>run({id:810+i,version:V1,started:'2026-11-01T10:00:00Z',state}));
 const data={runs,results:[]};const evidence=runsWithoutResults(data);assert.equal(evidence.length,4);
 const html=renderToStaticMarkup(createElement(RsiView,{views:seriesViews(data),unavailable:false,runEvidence:evidence}));
 for(const state of ['Running','Completed','Stopped','Failed'])assert.ok(html.includes(state));
 assert.match(html,/pass grade.*unknown/i);
});
const ENV={NEXT_PUBLIC_SUPABASE_URL:'https://fixture.supabase.co',NEXT_PUBLIC_SUPABASE_ANON_KEY:'fixture-publishable-key'};
const event={id:901,kind:'merge',subject:'194',summary:'Synthetic merge contract fixture',occurred_at:'2026-11-06T12:00:00Z',recorded_at:'2026-11-06T12:01:00Z',source_kind:'commit',source_ref:'a'.repeat(40),source_url:'https://github.com/KaydenClark/Agentic-Management-System/commit/'+ 'a'.repeat(40),strength:'recorded_fact',is_test:false};
const ok=body=>({ok:true,status:200,json:async()=>body});
test('public activity selects only approved columns, drops test rows and unselected detail',async()=>{
 const calls=[];const out=await loader.loadBuildEvents({env:ENV,fetchImpl:async(url,init)=>{calls.push({url:String(url),init});return ok([{...event,detail:{private:'MUST-NOT-EXPOSE'}},{...event,id:902,is_test:true}]);}});
 assert.equal(out.ok,true);assert.equal(out.data.events.length,1);assert.equal(out.data.unsupported,0);assert.ok(Number.isFinite(Date.parse(out.readAt)));
 const url=new URL(calls[0].url);assert.equal(url.pathname,'/rest/v1/build_events');assert.equal(url.searchParams.get('is_test'),'is.false');assert.ok(!url.searchParams.get('select').split(',').some(key=>['detail','summary'].includes(key)));
 assert.ok(!JSON.stringify(out).includes('MUST-NOT-EXPOSE'));assert.deepEqual(Object.keys(out.data.events[0]).sort(),Object.keys(event).filter(key=>key!=='summary').sort());
});
test('public activity distinguishes successful empty and failure without leaking keys',async()=>{
 const empty=await loader.loadBuildEvents({env:ENV,fetchImpl:async()=>ok([])});assert.equal(empty.ok,true);assert.deepEqual(empty.data,{events:[],unsupported:0});assert.ok(empty.readAt);
 for(const fetchImpl of [async()=>({ok:false,status:503}),async()=>ok({})]){
 const failed=await loader.loadBuildEvents({env:ENV,fetchImpl});assert.equal(failed.ok,false);assert.equal(failed.readAt,null);assert.ok(!JSON.stringify(failed).includes(ENV.NEXT_PUBLIC_SUPABASE_ANON_KEY));}
});

test('read states distinguish populated, empty, stale and failed using the successful envelope timestamp',async()=>{
 const {readState}=await import('../app/rsi/read-state.ts');
 const now=Date.parse('2026-11-06T12:10:00Z');
 const fresh={ok:true,data:[event],readAt:'2026-11-06T12:09:00Z'};
 assert.equal(readState(fresh,false,now),'populated');assert.equal(readState({...fresh,data:[]},true,now),'empty');
 assert.equal(readState({...fresh,readAt:'2026-11-06T12:00:00Z'},false,now),'stale');
 assert.equal(readState({...fresh,data:[],readAt:'2026-11-06T12:00:00Z'},true,now),'stale');
 assert.equal(readState({ok:false,data:[],readAt:null,reason:'Synthetic outage'},true,now),'failed');
});
test('activity renders safe on-site provenance and retains stale success, never arbitrary detail or private URLs',async()=>{
 const {ActivityEvidence}=await import('../app/rsi/activity.tsx');
 const {readerLinkProblems}=await import('./reader-links.mjs');
 const render=loaded=>renderToStaticMarkup(createElement(ActivityEvidence,{loaded,now:Date.parse('2026-11-06T12:10:00Z')}));
 const loaded={ok:true,data:{events:[event],unsupported:0},readAt:'2026-11-06T12:00:00Z'};const html=render(loaded);
 assert.match(html,/data-read-state="stale"/);assert.ok(html.includes('href="#rsi-event-901"'));assert.ok(html.includes('id="rsi-event-901"'));
 for(const value of [event.source_ref,event.source_url,event.occurred_at,event.recorded_at,loaded.readAt])assert.ok(html.includes(value));
 assert.deepEqual(readerLinkProblems([{name:'rsi.html',html}]),[]);assert.match(html,/refresh outcome is unknown/i);assert.match(html,/not.*useful improvement/i);
 const unsupported=render({...loaded,data:{events:[],unsupported:3},readAt:'2026-11-06T12:09:00Z'});assert.match(unsupported,/data-read-state="unsupported"/);assert.match(unsupported,/3 public rows are unsupported or refused/);assert.ok(!unsupported.includes('No public activity events were present'));
 const empty=render({...loaded,data:{events:[],unsupported:0},readAt:'2026-11-06T12:09:00Z'});assert.match(empty,/data-read-state="empty"/);assert.match(empty,/No public activity events/);
 const failed=render({ok:false,data:{events:[],unsupported:0},readAt:null,reason:'MUST-NOT-EXPOSE'});assert.match(failed,/data-read-state="failed"/);assert.ok(!failed.includes('MUST-NOT-EXPOSE'));assert.match(failed,/unknown/i);assert.ok(!failed.includes('No public activity events'));
});

test('a next supported event is read and rendered without a source list edit; source conflicts refuse',async()=>{
 const {ActivityEvidence}=await import('../app/rsi/activity.tsx');
 let rows=[event];const fetchImpl=async()=>ok(rows);
 const firstRead=await loader.loadBuildEvents({env:ENV,fetchImpl});assert.deepEqual(firstRead.data.events.map(row=>row.id),[901]);
 rows=[event,{...event,id:902,subject:'195',source_ref:'b'.repeat(40),source_url:event.source_url.replaceAll('a'.repeat(40),'b'.repeat(40))}];
 const secondRead=await loader.loadBuildEvents({env:ENV,fetchImpl});assert.equal(secondRead.ok,true);
 const html=renderToStaticMarkup(createElement(ActivityEvidence,{loaded:secondRead}));for(const id of [901,902])assert.ok(html.includes(`id="rsi-event-${id}"`));
 rows=[event,{...event,id:902}];assert.equal((await loader.loadBuildEvents({env:ENV,fetchImpl})).ok,false);
});

test('private core fields and unknown kinds cannot enter the public merge-fact projection',async()=>{
 const marker='PRIVATE-REVIEW-/Users/owner/criticism';
 const variants=[{summary:marker},{subject:marker},{kind:'private_review'},{source_kind:'path',source_ref:marker},{source_ref:marker},{source_url:'https://private.example/'+marker},{occurred_at:marker},{source_url:event.source_url.replaceAll('a'.repeat(40),'b'.repeat(40))}];
 for(const over of variants){
  const out=await loader.loadBuildEvents({env:ENV,fetchImpl:async()=>ok([{...event,...over}])});
  assert.ok(!JSON.stringify(out).includes(marker),'private core text escaped the projection');
  assert.equal(out.ok,true,'well-shaped unsupported rows must remain explicit, not erase the whole read');
  assert.equal(out.data.events.length+out.data.unsupported,1);
  if(!('summary' in over))assert.equal(out.data.unsupported,1);
 }
});
