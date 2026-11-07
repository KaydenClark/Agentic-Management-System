// Public projection only. Never select operational text or use a privileged key.
import type { ReadResult } from './supabase';
export interface SkillAudit {
  audit_run_id: string; audit_set_id: string; skill: string; skills_commit: string;
  contract_version: string; contract_digest: string; provider: string; model: string;
  model_tier: 'small' | 'mid' | 'high'; quality_passed: number; quality_total: number;
  regression_passed: number; regression_total: number; critical_missed: boolean | null;
  evidence_complete: boolean; passed: boolean | null; assessment_grade: 'Excellent' | 'Stable' | 'Functional' | 'Broken' | null; completed_at: string; recorded_at: string;
}
const fields = ['audit_run_id','audit_set_id','skill','skills_commit','contract_version','contract_digest','provider','model','model_tier','quality_passed','quality_total','regression_passed','regression_total','critical_missed','evidence_complete','passed','assessment_grade','completed_at','recorded_at'] as const;
const empty: SkillAudit[] = [];
type Options = { env?: Readonly<Record<string,string | undefined>>; fetchImpl?: typeof fetch; timeoutMs?: number };
// Refuse the entire read when a projected row is malformed: dropping it would
// turn an unknown count into an apparently complete count.
function valid(row: Record<string,unknown>): boolean {
  const label = (v: unknown) => typeof v === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,127}$/.test(v);
  const number = (v: unknown) => typeof v === 'number' && Number.isSafeInteger(v) && v >= 0;
  const date = (v: unknown) => typeof v === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)$/.test(v) && Number.isFinite(Date.parse(v));
  return ['audit_run_id','audit_set_id','skill','contract_version','provider'].every(k => label(row[k])) &&
    typeof row.model === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9_.:\/-]{0,127}$/.test(row.model) &&
    typeof row.skills_commit === 'string' && /^[a-f0-9]{40}$/.test(row.skills_commit) &&
    typeof row.contract_digest === 'string' && /^[a-f0-9]{64}$/.test(row.contract_digest) &&
    ['small','mid','high'].includes(String(row.model_tier)) &&
    ['quality_passed','quality_total','regression_passed','regression_total'].every(k => number(row[k])) &&
    Number(row.quality_passed) <= Number(row.quality_total) && Number(row.regression_passed) <= Number(row.regression_total) &&
    (row.critical_missed === null || typeof row.critical_missed === 'boolean') && typeof row.evidence_complete === 'boolean' &&
    (row.passed === null || typeof row.passed === 'boolean') && (row.assessment_grade === null || ['Excellent','Stable','Functional','Broken'].includes(String(row.assessment_grade))) && date(row.completed_at) && date(row.recorded_at);
}
// The audit route accepts only publishable credentials; service JWTs and
// secret keys must never be sent even when accidentally configured here.
function publicKey(key: string): boolean {
  if (key.startsWith('sb_publishable_')) return true;
  if (key.startsWith('sb_secret_')) return false;
  try { const parts = key.split('.'); if (parts.length !== 3) return false; const payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString()); return payload.role === 'anon'; } catch { return false; }
}
export async function loadSkillAudits(options: Options = {}): Promise<ReadResult<SkillAudit[]>> {
  const env = options.env ?? process.env; const base = env.NEXT_PUBLIC_SUPABASE_URL; const key = env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const fail = (): ReadResult<SkillAudit[]> => ({ok:false,data:empty,readAt:null,reason:'public audit read unavailable'});
  if (!base || !key || !publicKey(key)) return fail();
  try {
    const rows: SkillAudit[] = [];
    // Exhaust the ordered projection before reporting a count. A truncated or
    // failed page invalidates the whole envelope instead of returning a partial set.
    for (let page=0; page<50; page++) {
      const url = new URL('/rest/v1/rsi_skill_audit_results',base);
      url.searchParams.set('select',fields.join(',')); url.searchParams.set('order','completed_at.desc,audit_run_id.asc'); url.searchParams.set('limit','1000'); url.searchParams.set('offset',String(page*1000));
      const headers: Record<string,string> = {apikey:key,Accept:'application/json'}; if (!key.startsWith('sb_publishable_')) headers.Authorization=`Bearer ${key}`;
      const response = await (options.fetchImpl ?? fetch)(url.toString(),{headers,signal:AbortSignal.timeout(options.timeoutMs ?? 8000),cache:'no-store'});
      if (!response.ok) return fail(); const body: unknown = await response.json();
      if (!Array.isArray(body) || !body.every(v => v && typeof v === 'object' && !Array.isArray(v) && valid(v))) return fail();
      // Reproject unexpected fields away even if the server returns more than selected.
      rows.push(...body.map(v => Object.fromEntries(fields.map(k => [k,v[k]])) as unknown as SkillAudit));
      if (body.length < 1000) {
        if (new Set(rows.map(row=>row.audit_run_id)).size !== rows.length) return fail();
        return {ok:true,data:rows,readAt:new Date().toISOString()};
      }
    }
  } catch { return fail(); }
  return fail();
}
