// Browser verification for the built S-008 navigation. Start the built site and
// pass its URL as the first argument. Requires Playwright and Chromium.
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';
import { stages } from '../app/start/skills.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:3188';
const names = stages.flatMap(s => [...s.main, ...s.used]);
const browser = await chromium.launch({headless: true});
let checks = 0;
const check = (ok, msg) => { checks++; assert.ok(ok, msg); };
async function contents(page) {
  return page.evaluate(() => {
    const nav = document.querySelector('nav[aria-label="Skills wiki"]');
    const path = location.pathname.replace(/\/$/, '');
    const current = nav?.querySelectorAll('[aria-current="page"]');
    const links = [...(nav?.querySelectorAll('a[href]') ?? [])].map(a => a.getAttribute('href'));
    const toc = [...document.querySelectorAll('nav[aria-label="On this page"] a')].map(a => [a.getAttribute('href'), a.textContent.trim()]);
    const headings = [...document.querySelectorAll('article[data-skill] section[data-section] > h2')].map(h => ['#' + h.id, h.textContent.trim()]);
    return { links, current: [...(current ?? [])].map(a=>a.getAttribute('href')), path, toc, headings };
  });
}
function problems(data) {
  const out=[];
  if (data.current.length!==1 || data.current[0]!==data.path) out.push('current page');
  for (const name of names) if (!data.links.includes(`/skills/${name}`)) out.push(`missing ${name}`);
  if (!data.links.includes('/skills')) out.push('missing overview');
  if (data.path!=='/skills' && (!data.headings.length || JSON.stringify(data.toc)!==JSON.stringify(data.headings))) out.push('contents do not match headings');
  return out;
}
try {
  const context = await browser.newContext({ viewport:{width:1440,height:812} });
  const page = await context.newPage();
  for (const path of ['/skills', ...names.map(n=>`/skills/${n}`)]) {
    await page.goto(base+path, {waitUntil:'domcontentloaded'});
    const data=await contents(page); check(problems(data).length===0, `${path}: ${problems(data).join(', ')}`);
  }
  const good=await contents(page);
  check(problems({...good, current:[]}).includes('current page'), 'negative: missing current mark');
  check(problems({...good, links:good.links.filter(x=>x!=='/skills/grilling')}).some(x=>x==='missing grilling'), 'negative: missing article link');
  check(problems({...good, toc:[]}).includes('contents do not match headings'), 'negative: missing contents');
  await page.goto(base+'/start', {waitUntil:'domcontentloaded'});
  const chips=await page.locator('[data-skills-diagram] [data-skill] a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));
  check(names.every(n=>chips.includes(`/skills/${n}`)), 'start chips link all 39 articles');
  await context.close();
  for (const width of [375,1280,1440]) for (const theme of ['light','dark']) for (const javascriptEnabled of [true,false]) for (const zoom of [1,2]) {
    const c=await browser.newContext({viewport:{width,height:812}, colorScheme:theme, javaScriptEnabled:javascriptEnabled});
    const p=await c.newPage();
    await p.setContent('<script>window.__scriptCanary = true</script>');
    check(await p.evaluate(() => window.__scriptCanary === true) === javascriptEnabled, `script canary mismatch: expected ${javascriptEnabled}`);
    await p.goto(base+'/skills/grilling',{waitUntil:'load'});
    if (zoom===2) {
      const before=await p.locator('nav[aria-label="Skills wiki"] a').first().evaluate(el=>parseFloat(getComputedStyle(el).fontSize));
      await p.evaluate(() => { const sizes=[...document.querySelectorAll('*')].map(el=>[el,parseFloat(getComputedStyle(el).fontSize)]); for(const [el,size] of sizes) el.style.setProperty('font-size', `${size * 2}px`, 'important'); });
      const after=await p.locator('nav[aria-label="Skills wiki"] a').first().evaluate(el=>parseFloat(getComputedStyle(el).fontSize));
      check(Math.abs(after-before*2)<0.1, `text size failed to double: ${before} -> ${after}`);
    }
    if (javascriptEnabled) await p.waitForFunction(() => Math.abs(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sticky-header-height')) - Math.ceil(document.querySelector('header.topbar').getBoundingClientRect().height)) < 1);
    await p.evaluate(()=>scrollTo(0,700));
    const geometry=await p.evaluate(()=>{const h=document.querySelector('header.topbar').getBoundingClientRect();const n=document.querySelector('nav[aria-label="Skills wiki"]');const r=n.getBoundingClientRect();return {sticky:getComputedStyle(n).position==='sticky', top:r.top, bottom:r.bottom, header:h.bottom, width:document.documentElement.scrollWidth, client:document.documentElement.clientWidth};});
    check(geometry.width<=geometry.client, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: horizontal overflow`);
    if (geometry.sticky) check(geometry.top>=geometry.header-1 && geometry.bottom<=812+1, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: sticky overlap ${JSON.stringify(geometry)}`);
    const data=await contents(p); check(problems(data).length===0, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: ${problems(data)}`);
    const target=p.locator('nav[aria-label="On this page"] a').first();
    await target.click();
    const targetTop=await p.evaluate(()=>{const h=document.querySelector('header.topbar').getBoundingClientRect();const t=document.getElementById(decodeURIComponent(location.hash.slice(1))).getBoundingClientRect();return {header:h.bottom,top:t.top};});
    check(targetTop.top>=targetTop.header-1, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: heading hidden ${JSON.stringify(targetTop)}`);
    await p.goto(base+'/skills/grilling',{waitUntil:'load'});
    if (zoom===2) await p.evaluate(() => { const sizes=[...document.querySelectorAll('*')].map(el=>[el,parseFloat(getComputedStyle(el).fontSize)]); for(const [el,size] of sizes) el.style.setProperty('font-size', `${size * 2}px`, 'important'); });
    if (javascriptEnabled) await p.waitForFunction(() => Math.abs(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sticky-header-height')) - Math.ceil(document.querySelector('header.topbar').getBoundingClientRect().height)) < 1);
    let reached=false;
    for (let i=0;i<80;i++) {
      await p.keyboard.press('Tab');
      const state=await p.evaluate(()=>{const a=document.activeElement;const n=a?.closest('nav[aria-label="Skills wiki"]');if(!n)return null;const r=a.getBoundingClientRect(),h=document.querySelector('header.topbar').getBoundingClientRect();return {top:r.top,bottom:r.bottom,header:h.bottom};});
      if(state){reached=true;check(state.top>=state.header-1 && state.bottom<=813, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: keyboard obscured ${JSON.stringify(state)}`);break;}
    }
    check(reached, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: keyboard cannot reach wiki navigation`);
    await p.keyboard.press('Tab');
    const onSummary=await p.evaluate(()=>document.activeElement?.matches('nav[aria-label="Skills wiki"] summary'));
    check(onSummary, `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: stage summary is not next in tab order`);
    await p.keyboard.press('Enter');
    check(await p.evaluate(()=>document.activeElement?.parentElement?.open===true), `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: stage did not open from keyboard`);
    await p.keyboard.press('Tab');
    check(await p.evaluate(()=>document.activeElement?.matches('nav[aria-label="Skills wiki"] details[open] a')), `${width}/${theme}/js=${javascriptEnabled}/zoom=${zoom}: opened links unreachable`);
    await c.close();
  }
  // Actual keyboard traversal from the document start on the wide sidebar.
  const c=await browser.newContext({viewport:{width:1440,height:812}}); const p=await c.newPage();
  await p.goto(base+'/skills/grilling',{waitUntil:'load'});
  await p.locator('nav[aria-label="Skills wiki"] details').evaluateAll(ds => ds.forEach(d => { d.open = true; }));
  let seen=false;
  for (let i=0;i<100;i++) {
    await p.keyboard.press('Tab');
    const state=await p.evaluate(()=>{const a=document.activeElement;const n=a?.closest('nav[aria-label="Skills wiki"]');if(!n)return null;const r=a.getBoundingClientRect(),h=document.querySelector('header.topbar').getBoundingClientRect(),nr=n.getBoundingClientRect();return {top:r.top,bottom:r.bottom,header:h.bottom,navTop:nr.top,navBottom:nr.bottom};});
    if(state){seen=true;check(state.top>=state.header-1 && state.top>=state.navTop-1 && state.bottom<=Math.min(812,state.navBottom)+1, `keyboard focus obscured ${JSON.stringify(state)}`);}
    if(seen&&!state) break;
  }
  check(seen,'keyboard reaches sidebar from document start'); await c.close();
  console.log(`skills navigation: ${checks} checks passed`);
} finally { await browser.close(); }
