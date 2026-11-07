import { Signal } from '../components/Signal';
import { readState } from './read-state';
import type { ReadResult } from './supabase';
import type { SkillAudit } from './audits';
import styles from './rsi.module.css';

export function AuditEvidence({loaded,now}:{loaded:ReadResult<SkillAudit[]>;now?:number}) {
  const state=readState(loaded,loaded.data.length===0,now);
  return <section className={styles.place} aria-labelledby="skill-audits" data-audits="" data-read-state={state}>
    <h2 id="skill-audits">Completed skill audits</h2>
    <p>The count is completed public audit runs, including failures and incomplete evidence. An incomplete run may not establish a whole assessment grade. Assessment grade is separate from each run outcome and does not establish qualification or demonstrated improvement. Audit scores describe checks. Ordinary skill uses and repair attempts are not audits.</p>
    {state==='failed' ? <Signal kind="heat" label="Audits unavailable"><p>The audit count is unknown because the public read failed. No earlier successful read is available in this response.</p></Signal> : <>
      {state==='stale' ? <Signal kind="heat" label="Audit data may be stale"><p>This retained successful read is older than five minutes. The refresh outcome is unknown; newer audits may be missing.</p></Signal> : null}
      <p className={styles.muted}>Last successful audit read: <time dateTime={loaded.readAt!}>{loaded.readAt}</time>. A read time is not a producer heartbeat.</p>
      {loaded.data.length === 0 ? <p>No completed public audits were present at this successful read{state==='stale' ? '; the current count is unknown' : ''}.</p> : <>
        <p><a href="#audit-rows">{loaded.data.length} completed audit{loaded.data.length===1?'':'s'}</a> in this read.</p>
        <ol id="audit-rows" className={styles.points}>{loaded.data.map(row => <li key={row.audit_run_id} className={styles.row} id={`rsi-audit-${row.audit_run_id}`} data-audit-id={row.audit_run_id}>
          <p><strong>{row.passed===true?'Passed':row.passed===false?'Failed':!row.evidence_complete?'Incomplete':row.quality_total===0 && row.regression_total===0 && row.critical_missed===null?'No applicable checks':'Unestablished'}</strong> · <code>{row.skill}</code>. Quality: {row.quality_total ? `${row.quality_passed} of ${row.quality_total}` : 'score unavailable'}. Regression: {row.regression_total ? `${row.regression_passed} of ${row.regression_total}` : 'score unavailable'}. Critical: {row.critical_missed===null?'Unknown':row.critical_missed?'Missed':'No miss recorded'}. Evidence: {row.evidence_complete?'complete':'incomplete'}.</p>
          <p>Assessment grade: <strong>{row.assessment_grade ?? 'Unknown'}</strong>.</p>
          <p>Audit <a href={`#rsi-audit-${row.audit_run_id}`}><code>{row.audit_run_id}</code></a>; set <code>{row.audit_set_id}</code>. Provider <code>{row.provider}</code>, model <code>{row.model}</code>, tier <code>{row.model_tier}</code>.</p>
          <p>Skills pin <code>{row.skills_commit}</code>; contract <code>{row.contract_version}</code>, digest <code>{row.contract_digest}</code>.</p>
          <p>Completed <time dateTime={row.completed_at}>{row.completed_at}</time>; recorded <time dateTime={row.recorded_at}>{row.recorded_at}</time>.</p>
        </li>)}</ol>
      </>}
    </>}
  </section>;
}
