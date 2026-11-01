#!/usr/bin/env node
// Read-only evidence checks for one assignment. Git remains the recovery store;
// the existing Spec/Task owns disposition and the human/host owns release.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {declaredGit,findRoot,isMainModule,laneRelative,markdownLinkTargets,readManifest} from './workbench-paths.mjs';
import {findSpec} from './spec-workbench.mjs';

const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const SHA=/^[a-f0-9]{40,64}$/;
const objectFormats=new Map();
const gitObject=(root,bytes)=>crypto.createHash(objectFormats.get(root)??'sha1').update(Buffer.from(`blob ${bytes.length}\0`)).update(bytes).digest('hex');
const operations=['MERGE_HEAD','REBASE_HEAD','rebase-merge','rebase-apply','CHERRY_PICK_HEAD','REVERT_HEAD','BISECT_LOG','index.lock'];
const env={...process.env,GIT_OPTIONAL_LOCKS:'0',GIT_TERMINAL_PROMPT:'0'};
function fail(code,message){const error=new Error(message);error.code=code;throw error;}
function git(root,args,allowFailure=false){
 const r=spawnSync('git',['-C',root,...args],{env:args[0]==='ls-remote'?env:{...env,GIT_NO_LAZY_FETCH:'1',GIT_ALLOW_PROTOCOL:''},encoding:null,maxBuffer:64*1024*1024,timeout:15000});
 if(r.error||r.status!==0){if(allowFailure)return null;fail('git-unavailable',`Git evidence unavailable (${args[0]}).`);}
 return r.stdout;
}
const text=(root,args,optional=false)=>git(root,args,optional)?.toString('utf8').trim()??null;
const nul=bytes=>bytes.toString('utf8').split('\0').filter(Boolean);
function safePath(root,name){
 if(typeof name!=='string'||!name||name.includes('\0')||name.includes('\\')||path.isAbsolute(name)||name.split('/').some(x=>['..','.git'].includes(x)))fail('unsafe-path','Evidence path must remain within its repository.');
 const file=path.resolve(root,name);
 if(!file.startsWith(root+path.sep))fail('unsafe-path','Evidence path must remain within its repository.');
 let cursor=root;
 for(const part of name.split('/').filter(Boolean)){
  cursor=path.join(cursor,part);let stat;try{stat=fs.lstatSync(cursor);}catch(error){if(error.code==='ENOENT')break;throw error;}
  if(stat.isSymbolicLink()&&cursor!==file)fail('unsafe-link',`Directory link cannot be traversed: ${name}`);
 }
 return file;
}
function fingerprint(root,name){
 const file=safePath(root,name);let stat;try{stat=fs.lstatSync(file);}catch(error){if(error.code==='ENOENT')return{path:name,kind:'missing'};throw error;}
 if(stat.isSymbolicLink()){
  const target=fs.readlinkSync(file);const destination=path.resolve(path.dirname(file),target);
  if(path.isAbsolute(target)||!(destination===root||destination.startsWith(root+path.sep)))fail('unsafe-link',`Link leaves the repository: ${name}`);
  return{path:name,kind:'symlink',sha256:hash(Buffer.from(target)),gitObject:gitObject(root,Buffer.from(target)),mode:stat.mode&0o777,gitMode:'120000'};
 }
 if(stat.isDirectory())return{path:name,kind:fs.existsSync(path.join(file,'.git'))?'repository':'directory',mode:stat.mode&0o777};
 if(!stat.isFile()||stat.nlink!==1)fail('unsafe-file',`Not an ordinary single-link file: ${name}`);
 const bytes=fs.readFileSync(file);
 return{path:name,kind:'file',sha256:hash(bytes),gitObject:gitObject(root,bytes),mode:stat.mode&0o777,gitMode:stat.mode&0o111?'100755':'100644'};
}
function selectedIgnored(root,names){
 const out=[];
 function visit(name){
  const value=fingerprint(root,name);
  if(value.kind==='directory'){
   for(const entry of fs.readdirSync(safePath(root,name)).sort())visit(`${name}/${entry}`);
  }else if(value.kind!=='missing')out.push(name);
 }
 for(const name of names){safePath(root,name);const ignored=git(root,['check-ignore','--quiet','--',name],true)??git(root,['check-ignore','--quiet','--',`${name.replace(/\/$/,'')}/`],true);if(ignored===null)fail('not-ignored',`Selected private evidence is not ignored: ${name}`);visit(name);}
 return out;
}
function taskOwner(root,specId,taskId){
 const spec=findSpec(root,specId);const task=(spec.records??[]).find(row=>row.id===taskId);
 if(!task)fail('unknown-task','Closeout requires an existing record-backed Task.');
 return{specId:spec.id,taskId:task.id,specPath:spec.relativePath,taskPath:task.relativePath,claimant:task.currentClaimant,status:task.status};
}
function worktrees(root){
 const parts=nul(git(root,['worktree','list','--porcelain','-z']));const result=[];let item;
 for(const value of parts){
  if(value.startsWith('worktree ')){item={path:value.slice(9),head:null,branch:null,locked:false,bare:false};result.push(item);}
  else if(item&&value.startsWith('HEAD '))item.head=value.slice(5);
  else if(item&&value.startsWith('branch '))item.branch=value.slice(7);
  else if(item&&value.startsWith('locked'))item.locked=true;
  else if(item&&value==='bare')item.bare=true;
 }
 return result;
}
function inventory(root,{ignored=[]}={}){
 const findings=[];const names=new Set(nul(git(root,['ls-files','--cached','--others','--exclude-standard','-z'])));
 for(const name of selectedIgnored(root,ignored))names.add(name);
 const files=[];
 for(const name of [...names].sort()){
  try{files.push(fingerprint(root,name));}catch(error){findings.push({code:error.code??'unreadable-path',path:name,message:error.message});}
 }
 const indexFile=text(root,['rev-parse','--git-path','index']);const absoluteIndex=path.resolve(root,indexFile);
 const index={sha256:fs.existsSync(absoluteIndex)?hash(fs.readFileSync(absoluteIndex)):null,entries:git(root,['ls-files','--stage','-z']).toString('utf8'),flags:git(root,['ls-files','-v','-z']).toString('utf8')};
 const refs=(text(root,['for-each-ref','--format=%(refname)%09%(objectname)','refs/heads','refs/remotes','refs/stash','refs/recovery'])??'').split('\n').filter(Boolean).map(line=>{const[ref,commit]=line.split('\t');return{ref,commit};});
 const gitDir=text(root,['rev-parse','--absolute-git-dir']);const busy=operations.filter(name=>fs.existsSync(path.join(gitDir,name)));
 const ignoredNames=nul(git(root,['ls-files','--others','--ignored','--exclude-standard','--directory','-z']));
 return{head:text(root,['rev-parse','HEAD']),files,index,refs,stashes:(text(root,['stash','list','--format=%H'])??'').split('\n').filter(Boolean),worktrees:worktrees(root),status:git(root,['status','--porcelain=v1','-z','--untracked-files=all']).toString('utf8'),ignoredNames,busy,findings};
}
function context(project){
 const redirected=['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_NAMESPACE'].filter(name=>process.env[name]!==undefined);
 if(redirected.length)fail('git-context-override',`Clear Git context overrides before inventory: ${redirected.join(', ')}`);
 const root=fs.realpathSync(findRoot(project));const top=text(root,['rev-parse','--show-toplevel']);
 if(fs.realpathSync(top)!==root)fail('not-a-workbench','Workbench root must be a Git checkout root.');
 const format=text(root,['rev-parse','--show-object-format']);if(!['sha1','sha256'].includes(format))fail('unsupported-object-format','Git object format is unavailable.');objectFormats.set(root,format);
 const manifest=readManifest(root),branches=declaredGit(root);
 if(!manifest||!branches||!manifest.workbenchId)fail('not-a-workbench','A declared room identity and integration branch are required.');
 const origin=text(root,['remote','get-url','origin']);if(!origin)fail('remote-unavailable','The existing origin remote is required.');
 const roots=text(root,['rev-list','--max-parents=0','HEAD']).split('\n').sort();
 return{root,manifest,branches,repository:{workbenchId:manifest.workbenchId,originHash:hash(origin),roots},origin};
}
export function snapshotWorkspace(project,options){
 const c=context(project);const owner=taskOwner(c.root,options.spec,options.task);
 if(!options.owner||owner.claimant!==options.owner)fail('unknown-ownership','Snapshot owner must match the Task current claimant.');
 const ignored=options.ignored??[];const data={repository:c.repository,workspace:c.root,owner:{...owner,name:options.owner},scope:{ignored},...inventory(c.root,{ignored})};
 return{schemaVersion:1,operation:'snapshot',complete:data.findings.length===0&&data.busy.length===0,digest:hash(JSON.stringify(data)),data,limitations:['Local evidence contains paths and hashes; keep it in approved private recovery.','A pinned digest detects changed evidence; it does not authenticate the observer or certify semantic completeness.']};
}
function readJson(file){
 if(!file)fail('invalid-input','Evidence file is required.');const stat=fs.lstatSync(file);
 if(!stat.isFile()||stat.isSymbolicLink()||stat.nlink!==1||stat.size>64*1024*1024)fail('invalid-input','Evidence must be a bounded ordinary file.');
 try{return JSON.parse(fs.readFileSync(file,'utf8'));}catch{fail('invalid-input','Evidence is not valid JSON.');}
}
function remoteRefs(root,refs){
 const advertised=text(root,['ls-remote','--refs','origin',...refs],true);if(advertised===null)return null;
 return new Map(advertised.split('\n').filter(Boolean).map(line=>{const[commit,ref]=line.split('\t');return[ref,commit];}));
}
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sameFile=(a,b)=>a?.kind===b?.kind&&a?.sha256===b?.sha256&&a?.mode===b?.mode;
const nativeLinkMode=()=>process.platform==='darwin'?0o777&~process.umask():process.platform==='win32'?null:0o777;
function gitModeRepresentsFilesystem(file){
 if(file.mode===undefined)return true; // Index entries carry Git mode, not filesystem permissions.
 return file.kind==='symlink'?file.mode===nativeLinkMode():file.kind==='file'&&file.mode===(file.gitMode==='100755'?0o755:0o644);
}
function blobMatches(root,commit,name,file){
 if(!SHA.test(commit)||!file||!['file','symlink','missing'].includes(file.kind)||(file.kind!=='missing'&&!gitModeRepresentsFilesystem(file)))return false;
 const listing=text(root,['ls-tree','-z',commit,'--',name],true);
 if(file.kind==='missing')return listing==='';
 if(!listing)return false;
 const match=/^(\d+) blob ([a-f0-9]+)\t/.exec(listing);
 if(!match||match[1]!==file.gitMode)return false;
 const bytes=git(root,['cat-file','blob',match[2]],true);
 return bytes!==null&&hash(bytes)===file.sha256;
}
function independentCopyMatches(item,file,workspace){
 try{
  const stat=fs.lstatSync(item.copy),actual=fs.realpathSync(item.copy);
  return file?.kind==='file'&&stat.isFile()&&!stat.isSymbolicLink()&&stat.nlink===1&&(stat.mode&0o777)===file.mode&&actual!==workspace&&!actual.startsWith(workspace+path.sep)&&typeof item.reason==='string'&&item.reason.trim().length>0&&hash(fs.readFileSync(item.copy))===file.sha256;
 }catch{return false;}
}
function routeExists(root,integration,owner,candidate,ref){
 const read=name=>text(root,['show',`${integration}:${name}`],true);
 const spec=read(owner.specPath);
 if(!spec||!spec.includes(candidate)||!spec.includes(ref)||!/Next action:\s*\S|\*\*Next gate:\*\*\s*\S/i.test(spec)||!/Authority:\s*\S|execution instruction/i.test(spec)||!/Checks:\s*\S|Verification/i.test(spec))return false;
 const memory=`${laneRelative(root,'wiki')}/MEMORY.md`;
 function links(name){
  const prose=(read(name)??'').replace(/<!--[\s\S]*?-->/g,'').replace(/```[\s\S]*?```/g,'');
  return markdownLinkTargets(prose).flatMap(target=>{
   if(/^[a-z][a-z0-9+.-]*:/i.test(target)||target.startsWith('/'))return[];
   const next=path.posix.normalize(path.posix.join(path.posix.dirname(name),target));
   return next.startsWith('../')||next.split('/').includes('.git')?[]:[next];
  });
 }
 if(!links('AGENTS.md').includes('RUNBOOK.md'))return false;
 if(!links('RUNBOOK.md').includes(memory)&&!links('ARCHITECTURE.md').includes(memory))return false;
 const pending=[memory],seen=new Set();
 while(pending.length&&seen.size<512){
  const name=pending.shift();if(name===owner.specPath)return true;if(seen.has(name))continue;seen.add(name);
  for(const target of links(name))if(target===owner.specPath)return true;else if(target.endsWith('.md')&&!seen.has(target))pending.push(target);
 }
 return false;
}
function activity(root,now){
 // This observes Git operations. An idle Git checkout does not establish that
 // another chat, editor or process has released it; the owning host checks that.
 return{gitOperations:now.busy,host:'unverified',reason:'Read current named-writer handback and host activity before release.'};
}
export function checkWorkspace(project,options){
 const result={schemaVersion:1,operation:'check',readOnly:true,accounted:false,remoteRecoverable:false,complete:false,publication:'local-only',workspaceRelease:{eligible:false,state:'retained',reason:'Activity and release authority require current host/owner inspection.'},items:[],findings:[],limitations:['This checks structural evidence, not semantic fidelity or universal process inactivity.','The checker never fetches, preserves, publishes, deletes or releases a workspace.']};
 const finding=(code,details={})=>result.findings.push({code,...details});
 try{
  const c=context(project),baseline=readJson(options.baseline),dispositions=readJson(options.dispositions);
  if(baseline.schemaVersion!==1||baseline.operation!=='snapshot'||!baseline.data||hash(JSON.stringify(baseline.data))!==baseline.digest)fail('invalid-baseline','Starting snapshot digest does not match its data.');
  if(baseline.complete!==true||baseline.data.findings?.length||baseline.data.busy?.length)fail('incomplete-baseline','The starting inventory was incomplete or taken during a Git operation.');
  if(!same(baseline.data.repository,c.repository))fail('wrong-repository','Starting snapshot belongs to a different repository lineage or room.');
  if(!SHA.test(options.baselineCommit??''))fail('unpinned-baseline','Name the immutable commit that records the starting snapshot digest.');
  const owner=baseline.data.owner;
  if(!owner||typeof owner.taskPath!=='string'||typeof owner.specPath!=='string')fail('invalid-baseline','Starting snapshot has no owning Task.');
  safePath(c.root,owner.taskPath);safePath(c.root,owner.specPath);
  const actualOwner=taskOwner(c.root,owner.specId,owner.taskId);
  if(actualOwner.taskPath!==owner.taskPath||actualOwner.specPath!==owner.specPath||actualOwner.claimant!==owner.name)fail('wrong-owner','The baseline paths do not resolve to their named Task.');
  const pinned=text(c.root,['show',`${options.baselineCommit}:${owner.taskPath}`],true);
  if(!pinned?.includes(`Workspace baseline sha256:${baseline.digest}`)||git(c.root,['merge-base','--is-ancestor',baseline.data.head,options.baselineCommit],true)===null)fail('unpinned-baseline','The owning Task at the baseline commit does not bind this snapshot.');
  if(dispositions.schemaVersion!==1||!Array.isArray(dispositions.items))fail('invalid-dispositions','Dispositions require schemaVersion 1 and items.');
  result.owner={specId:owner.specId,taskId:owner.taskId,specPath:owner.specPath,taskPath:owner.taskPath};
  result.baseline={digest:baseline.digest,commit:options.baselineCommit};
  const now=inventory(c.root,baseline.data.scope);result.observedHead=now.head;result.findings.push(...now.findings);result.activity=activity(c.root,now);
  if(now.busy.length)finding('active-git-operation',{operations:now.busy});
  const declarations=new Map();
  for(const item of dispositions.items){
   if(!item||!['path','index','ref','stash','worktree'].includes(item.kind)){finding('unsupported-disposition');continue;}
   const states={path:['integrated','pushed-pending','local-only','blocked'],index:['integrated','pushed-pending'],ref:['integrated','pushed-pending'],stash:['integrated','pushed-pending'],worktree:['retained']};
   if(!states[item.kind].includes(item.state))finding('unsupported-disposition',{kind:item.kind});
   let identity=item.source??item.path??item.ref??item.commit;
   if(item.kind==='worktree'&&typeof identity==='string'){try{identity=fs.realpathSync(identity);}catch{identity=path.resolve(identity);}}
   const key=`${item.kind}:${identity}`;if(declarations.has(key))finding('duplicate-disposition',{item:key});declarations.set(key,item);
  }
  const integrationRef=`refs/heads/${c.branches.integrationBranch}`;
  const requested=new Set([integrationRef]);
  for(const item of dispositions.items)if(typeof item?.ref==='string'&&/^refs\/heads\/[A-Za-z0-9][A-Za-z0-9._/-]*$/.test(item.ref)&&!item.ref.includes('..'))requested.add(item.ref);
  const remote=remoteRefs(c.root,[...requested]);let recoverable=remote!==null;
  if(!remote)finding('remote-unavailable');
  const integration=remote?.get(integrationRef);
  if(!integration||git(c.root,['cat-file','-e',`${integration}^{commit}`],true)===null){recoverable=false;finding('integration-unavailable');}
  const verifiedTips=new Set(integration?[integration]:[]);
  const verifyRecovery=(item,file)=>{
   const candidate=item.commit;
   if(!SHA.test(candidate??'')){finding('invalid-candidate',{path:item.path});return false;}
   if(file&&!blobMatches(c.root,candidate,item.path,file)){const code=!['file','symlink','missing'].includes(file.kind)?'candidate-type-unverified':!gitModeRepresentsFilesystem(file)?'filesystem-mode-not-in-git':'candidate-bytes-differ';finding(code,{path:item.path});return false;}
   if(item.state==='integrated'){
    if(!integration||git(c.root,['merge-base','--is-ancestor',candidate,integration],true)===null){finding('not-integrated',{path:item.path});return false;}
    return true;
   }
   if(item.state!=='pushed-pending'||!requested.has(item.ref)||remote?.get(item.ref)!==candidate){finding('remote-tip-differs',{path:item.path,ref:item.ref});return false;}
   if(!integration||!routeExists(c.root,integration,owner,candidate,item.ref)){finding('missing-discovery-route',{path:item.path});return false;}
   verifiedTips.add(candidate);result.publication='pushed-pending';return true;
  };
  const before=new Map(baseline.data.files.map(file=>[file.path,file]));const current=new Map(now.files.map(file=>[file.path,file]));
  let accounted=now.findings.length===0&&!result.findings.some(item=>item.code==='unsupported-disposition'||item.code==='duplicate-disposition');
  if(!accounted)recoverable=false;
  for(const name of before.keys())if(!current.has(name)){
   try{const live=fingerprint(c.root,name);if(live.kind!=='missing')current.set(name,live);}
   catch(error){accounted=false;recoverable=false;finding(error.code??'unreadable-path',{path:name});}
  }
  for(const item of declarations.values())if(['ref','stash'].includes(item.kind)&&!verifyRecovery(item,null)){accounted=false;recoverable=false;}
  const integratedFile=(name,file)=>integration&&blobMatches(c.root,integration,name,file);
  for(const name of new Set([...before.keys(),...current.keys()])){
   const old=before.get(name),file=current.get(name)??{path:name,kind:'missing'};
   const item=declarations.get(`path:${name}`);
   const selectedPrivate=baseline.data.scope.ignored.some(prefix=>name===prefix||name.startsWith(prefix.replace(/\/$/,'')+'/'));
   if(sameFile(old,file)&&!selectedPrivate&&!item){result.items.push({kind:'path',path:name,disposition:'retained-unchanged'});continue;}
   if(['file','symlink'].includes(file.kind)&&!gitModeRepresentsFilesystem(file)&&(!item||['integrated','pushed-pending'].includes(item.state)))finding('filesystem-mode-not-in-git',{path:name});
   if(!item&&integratedFile(name,file)){result.items.push({kind:'path',path:name,disposition:'integrated'});continue;}
   if(!item){accounted=false;recoverable=false;finding('unaccounted-path',{path:name});continue;}
   if(['integrated','pushed-pending'].includes(item.state)){
    const ok=verifyRecovery(item,file);accounted&&=ok;recoverable&&=ok;result.items.push({kind:'path',path:name,disposition:ok?item.state:'incomplete'});
   }else if(item.state==='local-only'){
    const copyCurrent=independentCopyMatches(item,file,baseline.data.workspace);
    const copyOriginal=independentCopyMatches(item,old,baseline.data.workspace);
    const ok=copyCurrent||copyOriginal;
    accounted&&=ok;recoverable=false;if(!ok)finding('local-copy-unverified',{path:name});result.items.push({kind:'path',path:name,disposition:ok?'local-only':'incomplete',preservedVersion:copyCurrent?'current':copyOriginal?'original':null});
   }else if(item.state==='blocked'&&item.reason){recoverable=false;result.items.push({kind:'path',path:name,disposition:'blocked'});}
   else{accounted=false;recoverable=false;finding('unsupported-disposition',{path:name});}
  }
  const priorIndex=new Set(baseline.data.index.entries.split('\0').filter(Boolean));
  for(const entry of now.index.entries.split('\0').filter(Boolean)){
   const match=/^(\d+) ([a-f0-9]+) (\d)\t([\s\S]+)$/.exec(entry);
   if(!match||match[3]!=='0'){accounted=false;recoverable=false;finding('unmerged-index');continue;}
   const [,mode,object,,name]=match,declared=declarations.get(`index:${name}`);
   if(priorIndex.has(entry)&&!declared)continue;
   const bytes=git(c.root,['cat-file','blob',object],true);
   const staged={path:name,kind:mode==='120000'?'symlink':'file',sha256:bytes&&hash(bytes),gitMode:mode};
   if(declared){if(!verifyRecovery(declared,staged)){accounted=false;recoverable=false;finding('unaccounted-index',{path:name});}continue;}
   const live=current.get(name);
   if(live?.sha256===staged.sha256&&live.gitMode===mode)continue;
   if(integration&&blobMatches(c.root,integration,name,staged))continue;
   const item=declarations.get(`index:${name}`);
   if(!item||!verifyRecovery(item,staged)){accounted=false;recoverable=false;finding('unaccounted-index',{path:name});}
  }
  if(now.index.flags!==baseline.data.index.flags&&now.index.flags.split('\0').some(value=>/^[a-zS] /.test(value))){accounted=false;recoverable=false;finding('hidden-index-flags');}
  const currentStashes=new Set(now.stashes),oldStashes=new Set(baseline.data.stashes);
  for(const commit of new Set([...oldStashes,...currentStashes])){
   if(oldStashes.has(commit)&&currentStashes.has(commit))continue;
   const item=declarations.get(`stash:${commit}`);
   if(!item||item.commit!==commit||!verifyRecovery(item,null)){accounted=false;recoverable=false;finding(oldStashes.has(commit)?'missing-original-stash':'unaccounted-stash',{commit});}
  }
  const priorRefs=new Map(baseline.data.refs.map(ref=>[ref.ref,ref.commit]));
  for(const ref of now.refs){
   if(priorRefs.get(ref.ref)===ref.commit||ref.ref.startsWith('refs/remotes/')||ref.ref===integrationRef)continue;
   if(integration&&git(c.root,['merge-base','--is-ancestor',ref.commit,integration],true)!==null)continue;
   const item=declarations.get(`${ref.ref==='refs/stash'?'stash':'ref'}:${ref.ref}`)??(ref.ref==='refs/stash'?declarations.get(`stash:${ref.commit}`):undefined)??dispositions.items.find(item=>item.kind==='path'&&item.commit===ref.commit&&item.ref===ref.ref);
   if(!item||!verifyRecovery({...item,commit:ref.commit},null)){accounted=false;recoverable=false;finding('unaccounted-ref',{ref:ref.ref});}
  }
  // A disappearing original ref also needs a checked surviving recovery ref.
  for(const[ref,commit]of priorRefs){
   const moved=now.refs.find(row=>row.ref===ref);
   if(moved&&moved.commit!==commit&&git(c.root,['merge-base','--is-ancestor',commit,moved.commit],true)===null&&(!integration||git(c.root,['merge-base','--is-ancestor',commit,integration],true)===null)){
    const original=declarations.get(`ref:${ref}@${commit}`);
    if(!original||original.commit!==commit||!verifyRecovery(original,null)){accounted=false;recoverable=false;finding('lost-original-ref',{ref});}
   }
   if(moved||ref.startsWith('refs/remotes/'))continue;
   const item=declarations.get(`${ref==='refs/stash'?'stash':'ref'}:${ref}`);
   if(!item||item.commit!==commit||!verifyRecovery(item,null)){accounted=false;recoverable=false;finding('missing-original-ref',{ref});}
  }
  // Replacement or absence is not preservation. Check originals against the
  // replacement working tree/index, using only advertised, verified history.
  const allRefs=(text(c.root,['for-each-ref','--format=%(refname)%09%(objectname)%09%(symref)'])??'').split('\n').filter(Boolean).map(line=>{const[ref,commit,symref]=line.split('\t');return{ref,commit,symref};}).filter(row=>!row.symref&&row.ref!=='refs/stash');
  const advertisedName=ref=>ref.startsWith('refs/remotes/')?(ref.startsWith('refs/remotes/origin/')?`refs/heads/${ref.slice('refs/remotes/origin/'.length)}`:null):ref;
  const advertisedNames=[...new Set(allRefs.map(row=>advertisedName(row.ref)).filter(Boolean))];
  const advertised=advertisedNames.length?remoteRefs(c.root,advertisedNames):new Map();
  if(advertised===null){recoverable=false;finding('remote-unavailable');}
  const history=verifiedTips.size?git(c.root,['rev-list','--objects','--no-object-names','--missing=error',...verifiedTips,'--'],true):null;
  const remoteObjects=new Set(history?history.toString('utf8').split('\n').filter(Boolean):[]);
  if(verifiedTips.size&&!history){accounted=false;recoverable=false;finding('remote-history-unavailable');}
  // One reachability set for every item kind: integration, declared candidates
  // and each advertised origin tip present locally with complete history. A tip
  // whose history is incomplete is left out, so it verifies nothing.
  for(const tip of new Set(advertised?advertised.values():[]))if(!remoteObjects.has(tip)&&git(c.root,['cat-file','-e',`${tip}^{commit}`],true)!==null){
   const reached=git(c.root,['rev-list','--objects','--no-object-names','--missing=error',tip,'--'],true);
   if(reached)for(const object of reached.toString('utf8').split('\n'))if(object)remoteObjects.add(object);
  }
  // Unchanged is local retention, not remote recovery: inherited bytes count as
  // recoverable only when their exact Git object is in verified remote history.
  // Their untouched checkout permissions (a umask-0002 0664) are not content,
  // so only changed paths carry the filesystem-mode rule.
  for(const row of result.items)if(row.disposition==='retained-unchanged'){
   const old=before.get(row.path);if(!old||old.kind==='missing')continue;
   if(['file','symlink'].includes(old.kind)&&remoteObjects.has(old.gitObject))continue;
   recoverable=false;finding('retained-bytes-not-remote',{path:row.path});
  }
  // The same rule covers every other retained Git object, changed or inherited:
  // index entries, stashes, refs (tags and remote-tracking included), a detached
  // HEAD and other registered checkouts. Accounting rules above stay unchanged.
  // An annotated tag object is verified by its exact advertised value.
  const refInRemote=(ref,commit)=>remoteObjects.has(commit)||(Boolean(advertisedName(ref))&&advertised?.get(advertisedName(ref))===commit);
  for(const row of allRefs)if(!refInRemote(row.ref,row.commit)){recoverable=false;finding('retained-ref-not-remote',{ref:row.ref});}
  for(const commit of now.stashes)if(!remoteObjects.has(commit)){recoverable=false;finding('retained-stash-not-remote',{commit});}
  if(text(c.root,['symbolic-ref','-q','HEAD'],true)===null&&!remoteObjects.has(now.head)){recoverable=false;finding('retained-head-not-remote',{commit:now.head});}
  for(const entry of now.index.entries.split('\0').filter(Boolean)){
   const match=/^(\d+) ([a-f0-9]+) (\d)\t([\s\S]+)$/.exec(entry);if(!match)continue;
   const[,mode,object,,name]=match,live=current.get(name);
   if(remoteObjects.has(object)||(live?.gitObject===object&&live.gitMode===mode))continue;
   if(mode==='160000'&&integration&&text(c.root,['ls-tree',integration,'--',name],true)===`160000 commit ${object}\t${name}`)continue;
   recoverable=false;finding('retained-index-not-remote',{path:name});
  }
  for(const worktree of now.worktrees){
   const name=path.resolve(worktree.path);if(name===c.root||worktree.bare)continue;
   const status=fs.existsSync(name)?git(name,['status','--porcelain=v1','-z','--untracked-files=all','--ignored'],true):null;
   const flags=status===null?null:git(name,['ls-files','-v','-z'],true);
   const hidden=flags===null||nul(flags).some(value=>/^[a-zS] /.test(value));
   if(status===null||status.length||hidden||!remoteObjects.has(worktree.head)){recoverable=false;finding('retained-worktree-not-remote',{path:name,reason:status===null?'unreadable':status.length?'uncommitted-or-ignored-content':hidden?'hidden-index-flags':'head-not-remote'});}
  }
  for(const[name,old]of before){
   const live=current.get(name);if(old.kind==='missing'||sameFile(old,live))continue;
   const original=old.gitObject&&remoteObjects.has(old.gitObject)?git(c.root,['cat-file','blob',old.gitObject],true):null;
   if(original&&hash(original)===old.sha256&&gitModeRepresentsFilesystem(old))continue;
   const item=declarations.get(`path:${name}`);
   if(item?.state==='local-only'&&independentCopyMatches(item,old,baseline.data.workspace)){recoverable=false;continue;}
   accounted=false;recoverable=false;finding('original-bytes-unverified',{path:name,reason:gitModeRepresentsFilesystem(old)?'bytes-not-in-verified-history':'filesystem-mode-not-in-git'});
   const row=result.items.find(item=>item.kind==='path'&&item.path===name);if(row)row.disposition='incomplete';
  }
  const currentIndex=new Set(now.index.entries.split('\0').filter(Boolean));
  for(const entry of priorIndex){
   if(currentIndex.has(entry))continue;
   const match=/^(\d+) ([a-f0-9]+) (\d)\t([\s\S]+)$/.exec(entry);
   if(match&&remoteObjects.has(match[2]))continue;
   accounted=false;recoverable=false;finding('original-index-unverified',{path:match?.[4]??null});
  }
  const selected=baseline.data.scope.ignored??[];
  const ignoredUnselected=now.ignoredNames.filter(name=>!selected.some(prefix=>name===prefix||name.startsWith(prefix.replace(/\/$/,'')+'/')));
  if(ignoredUnselected.length){finding('unselected-ignored-evidence',{count:ignoredUnselected.length});recoverable=false;}
  const original=baseline.data.workspace;
  const oldWorktrees=new Map(baseline.data.worktrees.map(item=>[path.resolve(item.path),item]));
  for(const worktree of now.worktrees){
   const name=path.resolve(worktree.path),old=oldWorktrees.get(name);
   if(name===c.root||name===original)continue;
   const disposition=declarations.get(`worktree:${name}`);
   if(old&&same(old,worktree)&&!disposition)continue;
   if(!disposition||disposition.state!=='retained'||disposition.expectedHead!==worktree.head||!disposition.reason){accounted=false;recoverable=false;finding('unaccounted-worktree',{path:name});}
   else result.items.push({kind:'worktree',path:name,disposition:'retained-with-purpose',head:worktree.head});
  }
  for(const name of oldWorktrees.keys())if(name!==original&&!now.worktrees.some(item=>path.resolve(item.path)===name)){accounted=false;recoverable=false;finding('missing-original-worktree',{path:name});}
  const registered=now.worktrees.find(item=>path.resolve(item.path)===original);
  const removed=!fs.existsSync(original)&&!registered;
  if(removed)result.workspaceRelease={eligible:false,state:'removed',reason:'Source checkout and registration are absent; recovery proof is checked separately.'};
  if(registered?.locked)finding('worktree-locked');
  const finalRemote=remoteRefs(c.root,[...requested]);
  const finalAdvertised=advertisedNames.length?remoteRefs(c.root,advertisedNames):new Map();
  if(remote&&(!finalRemote||!same([...remote],[...finalRemote])||!advertised||!finalAdvertised||!same([...advertised],[...finalAdvertised]))){recoverable=false;finding('remote-changed-during-check');}
  result.remoteObservation={at:new Date().toISOString(),integration:integration??null};
  result.accounted=accounted;
  result.remoteRecoverable=recoverable;
  result.complete=accounted&&recoverable&&!result.findings.length;
  if(result.complete&&result.publication!=='pushed-pending')result.publication='integrated';
 }catch(error){finding(error.code??'evidence-unavailable',{message:error.message});}
 return result;
}
const USAGE='Usage: workspace-closeout.mjs snapshot --project PATH --spec S-ID --task TK-ID --owner NAME [--ignored RELATIVE_PATH] | check --project PATH --baseline FILE --baseline-commit SHA --dispositions FILE';
export function parseCloseoutArgs(argv){
 const command=argv[0],options={ignored:[]};if(!['snapshot','check'].includes(command))fail('invalid-command',USAGE);
 const allowed=new Map([['--project','project'],['--spec','spec'],['--task','task'],['--owner','owner'],['--ignored','ignored'],['--baseline','baseline'],['--baseline-commit','baselineCommit'],['--dispositions','dispositions']]);
 for(let i=1;i<argv.length;i++){
  const key=allowed.get(argv[i]);if(!key||!argv[i+1]||argv[i+1].startsWith('--'))fail('invalid-argument',USAGE);
  const value=argv[++i];if(key==='ignored')options.ignored.push(value);else if(Object.hasOwn(options,key))fail('invalid-argument','Duplicate closeout argument.');else options[key]=value;
 }
 return{command,options};
}
if(isMainModule(import.meta.url)){
 try{const{command,options}=parseCloseoutArgs(process.argv.slice(2));const result=command==='snapshot'?snapshotWorkspace(options.project??process.cwd(),options):checkWorkspace(options.project??process.cwd(),options);console.log(JSON.stringify(result,null,2));if(!result.complete)process.exitCode=1;}
 catch(error){console.log(JSON.stringify({schemaVersion:1,operation:'error',complete:false,findings:[{code:error.code??'unavailable',message:error.message}]}));process.exitCode=2;}
}
