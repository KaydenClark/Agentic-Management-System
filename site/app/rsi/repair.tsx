import { repairEvidence as evidence } from "./repair-data";
import styles from "./rsi.module.css";

export function RepairEvidence() {
  return (
    <section className={`${styles.page} ${styles.repair}`} data-repair-evidence="" aria-labelledby="repair-title">
      <header className={styles.intro}>
        <p className="eyebrow">Development evidence</p>
        <h2 id="repair-title">Repairing shared skill delivery</h2>
        <p>
          Website work exposed recurring branch and cleanup failures, and a handoff procedure that conflicted with
          local session storage. The repair targets the shared methods, followed by the personal skill catalog used
          for later website work. This is a snapshot of <a href={evidence.baseline.source}>published evidence</a>.
        </p>
      </header>
      <figure className={styles.place} aria-labelledby="baseline-predicates">
        <figcaption>
          <h3 id="baseline-predicates">Baseline development checks</h3>
          <p>These are deterministic end-state predicates, not an Alignment Score or a skill acceptance result.</p>
        </figcaption>
        <p>
          Source-injected skills, not native activation; <a href={evidence.baseline.configurationSource}>model {evidence.baseline.model}, effort high (verified by trace readback)</a>.
          Baseline identity: <a href={evidence.baseline.source}><code>{evidence.baseline.skillsCommit}</code></a>.
        </p>
        <ul className={styles.evidenceBars}>
          {evidence.baseline.runs.map((run) => (
            <li key={run.id} data-predicate-run={run.id}>
              <a href={run.source}>{run.label}: {run.passed} of {run.checks} predicates passed</a>
              <span className={styles.evidenceTrack} role="img" aria-label={`${run.label}: ${run.passed} of ${run.checks} predicates passed`}>
                <span className={styles.evidenceBar} style={{ width: `${100 * run.passed / run.checks}%` }} />
              </span>
            </li>
          ))}
        </ul>
        <p>
          Assigned Tasks completed and protected unrelated and ignored evidence survived. Ref retention needs trace
          review; authority interpretation remains unqualified. True consecutive-Task behavior remains untested.
        </p>
      </figure>
      <figure className={styles.place} aria-labelledby="candidate-predicates">
        <figcaption>
          <h3 id="candidate-predicates">First workflow candidate</h3>
          <p>Development observations from the same fixed local jobs; not a useful-benefit headline.</p>
        </figcaption>
        <p>Candidate identity: <a href={evidence.candidate.source}><code>{evidence.candidate.skillsCommit}</code></a>.</p>
        <ul className={styles.evidenceBars}>
          {evidence.candidate.runs.map((run) => (
            <li key={run.id} data-candidate-run={run.id}>
              <a href={run.source}>{run.label}: {run.passed} of {run.checks} predicates passed</a>
              <span className={styles.evidenceTrack} role="img" aria-label={`${run.label}: ${run.passed} of ${run.checks} predicates passed`}>
                <span className={styles.evidenceBar} style={{ width: `${100 * run.passed / run.checks}%` }} />
              </span>
            </li>
          ))}
        </ul>
        <p>
          Some commits remained unpushed and a Task remained in progress with modified files. Preservation checks
          held, while authority and native refusal traces still need interpretation. The lower predicate counts
          do not establish source cause or a qualified regression.
        </p>
        <p data-reported-audit="">
          Reported bounded Alignment attempt: <a href={evidence.candidate.audit.source}>{evidence.candidate.audit.level}, {evidence.candidate.audit.passed} of {evidence.candidate.audit.applicable} applicable checks passed</a>.
          Evidence is incomplete and the evaluator is {evidence.candidate.audit.qualification}; most failed checks
          lack required proof rather than demonstrate an observed defect. Not accepted for merge or installation.
        </p>
        <p>The <a href={evidence.candidate.source}>earlier provisional workflow tally was 6 of 78</a>; the trace addendum supplies more proof without deleting that first ledger.</p>
      </figure>
      <section className={styles.place} aria-labelledby="pruning-suite">
        <h3 id="pruning-suite">Separate pruning exercises</h3>
        <p>
          Smaller text can still miss the requested goal. These development exercises use the same source candidate
          and a separate inventory; their counts are not pooled with the workflow comparison. The suite froze
          after drafting began and before outcomes were returned.
        </p>
        <ul className={styles.evidenceBars}>
          {evidence.pruning.observations.map((row) => (
            <li key={row.label} data-pruning-exercise="">
              <a href={evidence.pruning.source}>{row.label}: {row.before} → {row.after} Unicode characters</a>
              <p>{row.note}</p>
            </li>
          ))}
        </ul>
        <p>
          Separate reported bounded audit: <a href={evidence.pruning.source}>{evidence.pruning.audit.level}, {evidence.pruning.audit.passed} of {evidence.pruning.audit.applicable} applicable checks passed</a>.
          Full-check evidence is incomplete; qualification covers objective counts and bytes, not full semantic
          equivalence. Neither goal misses nor conservative stops establish source causality. No accepted repair.
        </p>
        <p>The <a href={evidence.pruning.source}>earlier provisional pruning tally was 3 of 51</a>; its original ledger is retained separately.</p>
      </section>
      <div className={styles.places}>
        <section className={styles.place} aria-labelledby="repair-next">
          <h3 id="repair-next">What remains</h3>
          <ul>
            <li>Candidate comparison pending for the final bundle; the first workflow attempt above remains part of its history.</li>
            <li>Audit pending for that final bundle: no qualifying fitness result is recorded.</li>
            <li>Installation and later use pending: a copied file alone cannot prove activation or use.</li>
            <li>A harness-ready comparison is pending under explicit local fixture permissions and fuller source context. Changed conditions will stay separate from this failed series.</li>
          </ul>
          <p>No demonstrated improvement, accepted repair or Human QA is claimed. Failed, incomplete and inconclusive evidence stays visible.</p>
        </section>
        <figure className={styles.place} aria-labelledby="documentation-failure">
          <figcaption>
            <h3 id="documentation-failure">A failure during the repair</h3>
            <p>
              Repeated edits pursued a ceiling instead of the requested small RUNBOOK.
              The <a href={evidence.documentation.source}>target is 900–1500 Unicode characters; the ceiling is 3000</a>.
              This is separate from the frozen skill comparison.
            </p>
          </figcaption>
          <ul className={styles.evidenceBars}>
            {evidence.documentation.observations.map((row) => (
              <li key={row.label} data-document-length={row.characters}>
                <a href={row.source}>{row.label}: {row.characters} characters</a>
                <span className={styles.evidenceTrack} role="img" aria-label={`${row.label}: ${row.characters} Unicode characters`}>
                  <span className={`${styles.evidenceBar} ${row.characters > 3000 ? styles.overBudget : ""}`} style={{ width: `${100 * row.characters / 3336}%` }} />
                </span>
              </li>
            ))}
          </ul>
          <p>
            The smaller document retains the real command surface and routes cleanup to the shared skill.
            Document length proves no future reliability; the <a href={evidence.documentation.source}>failed attempts and owner interventions</a> remain part of the record.
          </p>
        </figure>
      </div>
    </section>
  );
}
