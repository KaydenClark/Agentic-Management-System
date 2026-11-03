import { repairEvidence as evidence } from "./repair-data";
import styles from "./rsi.module.css";

function WorkflowComparison() {
  return (
    <figure className={`${styles.place} ${styles.comparison}`} data-evidence-chart="workflow" aria-labelledby="workflow-chart-title">
      <figcaption>
        <p className="eyebrow">Recorded development comparison</p>
        <h2 id="workflow-chart-title">Baseline and first workflow candidate</h2>
        <p>The first candidate matched the baseline once and passed fewer checks in the other runs.</p>
      </figcaption>
      <p className={styles.muted}>Passed checks per run · common scale from zero to eleven. Solid bars: baseline. Double-bordered bars: candidate.</p>
      <ol className={styles.comparisonRuns}>
        {evidence.baseline.runs.map((baseline, i) => {
          const candidate = evidence.candidate.runs[i];
          return (
            <li key={baseline.id} data-comparison-run={i + 1}>
              <h4>{baseline.label}</h4>
              {[{ ...baseline, label: "Baseline", candidate: false }, { ...candidate, label: "Candidate", candidate: true }].map((run) => (
                <a key={run.label} href="#workflow-comparison-data" className={styles.comparisonRow}>
                  <span>{run.label}</span>
                  <span className={styles.comparisonTrack} aria-hidden="true">
                    <span className={`${styles.comparisonBar} ${run.candidate ? styles.candidateBar : ""}`} style={{ width: `${100 * run.passed / run.checks}%` }} />
                  </span>
                  <strong>{run.passed} of {run.checks}</strong>
                </a>
              ))}
            </li>
          );
        })}
      </ol>
      <p>These are deterministic end-state predicates, not an Alignment Score. The counts alone establish neither cause nor useful benefit.</p>
      <details className={styles.evidenceDetails}>
        <summary>Comparison data and method</summary>
        <table id="workflow-comparison-data" className={styles.evidenceTable}>
          <caption>First workflow attempt · passed checks out of eleven in each run</caption>
          <thead><tr><th scope="col">Run</th><th scope="col">Baseline</th><th scope="col">Candidate</th></tr></thead>
          <tbody>{evidence.baseline.runs.map((run, i) => (
            <tr key={run.id}><th scope="row">{run.label}</th><td>{run.passed} of {run.checks}</td><td>{evidence.candidate.runs[i].passed} of {run.checks}</td></tr>
          ))}</tbody>
        </table>
        <p>Three fresh paired worker exercises used fixed local jobs, tools and budget, with source-injected skills.
          The tests checked delivery, preservation and cleanup end states. Model <code>{evidence.baseline.model}</code>, high effort;
          source injection does not prove native activation. Baseline <code>{evidence.baseline.skillsCommit}</code>;
          candidate <code>{evidence.candidate.skillsCommit}</code>.</p>
        <p>Recorded {evidence.snapshotDate}. Safe source identities: <code>{evidence.comparisonRecord}</code> and <code>{evidence.candidateRecord}</code>.
          This is the first attempt, not a live summary of all later work. Private prompts, raw traces and skill text are excluded.</p>
      </details>
    </figure>
  );
}

export function RepairEvidence() {
  return (
    <section className={`${styles.page} ${styles.repair}`} data-repair-evidence="" aria-labelledby="repair-title">
      <WorkflowComparison />
      <header className={styles.intro}>
        <p className="eyebrow">Development evidence</p>
        <h2 id="repair-title">Project tools and shared-skill repair evidence</h2>
        <p>
          This page records a bounded checker repair to AMS project tooling alongside earlier shared-skill delivery
          attempts. Charts, supporting data, methods and limitations are presented here, including the <a href={evidence.baseline.source}>comparison data</a>.
        </p>
      </header>
      <section id="checker-evidence" className={styles.place} data-checker-repair="" aria-labelledby="checker-repair">
        <h3 id="checker-repair">A checker that called a file reference proof</h3>
        <p>
          The original up-to-Spec checker at <code>{evidence.checker.baseline}</code>
          {" "}reported a checked criterion as false <code>met</code> because its unrelated <code>Evidence:</code> file existed.
          File presence and commit ancestry do not verify behavior. The repair in
          candidate <code>{evidence.checker.candidate}</code>{" "}reports checked criteria as <code>unknown</code> while
          retaining resolved references; unchecked criteria remain <code>not met</code>.
        </p>
        <p>The finding, repair, observed outcomes and limitations are summarized here from the safe evidence report.</p>
        <p className={styles.muted}>Evidence identity: <code>CHECKER-REPAIR-2026-11-02.md</code> at <code>{evidence.checker.reportRevision}</code>.
          The findings, observed outcomes and limitations from that safe report are summarized below.</p>
        <p>
          On fixture <code>{evidence.checker.fixture}</code>, replay changed
          three false <code>met</code> results to <code>unknown</code>, including an ancestor-only reference, and kept
          their references. A second unrelated existing file reproduced the same pattern. Missing and unmerged references
          stayed <code>unknown</code>; the unchecked criterion stayed <code>not met</code>. This recurrence is within the
          same fixture, not later-use evidence. The safe report records
          33 focused checks passed and a source-suite result of 809 passed, 5 skipped, 1 failed. The failure was an
          inherited AGENTS.md length check (3215 against a 3000-character ceiling), not a checker assertion. A later
          recovery candidate passed hygiene after that separate control change.
        </p>
        <p>
          A separate observer, without inspecting the tests, replay script or expected answers, ran the checker on synthetic
          S-900 fixture records: 0 met, 1 not met, 5 unknown, with no false <code>met</code>. The missing and unmerged
          references were routed to S-013. This is an independent synthetic observation, not evidence of automatic detection
          or broader benefit; the safe report records its method and limits.
        </p>
        <p>
          Fresh Luna CLI use on S-001 returned 0 met, 6 not met, 2 unknown; on S-003 it returned 0 met, 8 not met,
          0 unknown. This is later real use of the checker, not evidence of missing historical behavior or a Spec verdict.
          Automatic skill discovery and other hosts remain unverified. The original false report remains historical evidence;
          the checker source is included in recovery assembly
          <code>{evidence.checker.assembly}</code>, and the Task is closed. Combined recovery checks and
          review status remain separate from this bounded result. These observations establish
          no semantic verification, generalized benefit, whole-Spec acceptance, owner QA or completed learning cycle. The
          broader control-pruning attempt repeated its goal-versus-
          ceiling failure and required owner and root intervention, so this is not evidence of a fully autonomous end-to-end
          learning cycle.
        </p>
      </section>
      <figure className={styles.place} aria-labelledby="baseline-predicates">
        <figcaption>
          <h3 id="baseline-predicates">Baseline development checks</h3>
          <p>These are deterministic end-state predicates, not an Alignment Score or a skill acceptance result.</p>
        </figcaption>
        <p>
          Source-injected skills, not native activation; model {evidence.baseline.model}, effort high (verified by trace readback).
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
      <figure id="candidate-evidence" className={styles.place} aria-labelledby="candidate-predicates">
        <figcaption>
          <h3 id="candidate-predicates">First workflow candidate</h3>
          <p>Development observations from the same fixed local jobs; not a useful-benefit headline.</p>
        </figcaption>
        <p>Candidate identity: <code>{evidence.candidate.skillsCommit}</code>.</p>
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
          Reported bounded Alignment attempt: {evidence.candidate.audit.level}, {evidence.candidate.audit.passed} of {evidence.candidate.audit.applicable} applicable checks passed.
          Evidence is incomplete and the evaluator is {evidence.candidate.audit.qualification}; most failed checks
          lack required proof rather than demonstrate an observed defect. Not accepted for merge or installation.
        </p>
        <p>The earlier provisional workflow tally was 6 of 78; the trace addendum supplies more proof without deleting that first ledger.</p>
      </figure>
      <section id="pruning-evidence" className={styles.place} aria-labelledby="pruning-suite">
        <h3 id="pruning-suite">Separate pruning exercises</h3>
        <p>
          Smaller text can still miss the requested goal. These development exercises use the same source candidate
          and a separate inventory; their counts are not pooled with the workflow comparison. The suite froze
          after drafting began and before outcomes were returned.
        </p>
        <ul className={styles.evidenceBars}>
          {evidence.pruning.observations.map((row) => (
            <li key={row.label} data-pruning-exercise="">
              {row.label}: {row.before} → {row.after} Unicode characters
              <p>{row.note}</p>
            </li>
          ))}
        </ul>
        <p>
          Separate reported bounded audit: {evidence.pruning.audit.level}, {evidence.pruning.audit.passed} of {evidence.pruning.audit.applicable} applicable checks passed.
          Full-check evidence is incomplete; qualification covers objective counts and bytes, not full semantic
          equivalence. Neither goal misses nor conservative stops establish source causality. No accepted repair.
        </p>
        <p>The earlier provisional pruning tally was 3 of 51; its original ledger is retained separately.</p>
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
        <figure id="documentation-evidence" className={styles.place} data-evidence-chart="documentation" aria-labelledby="documentation-failure">
          <figcaption>
            <h3 id="documentation-failure">A failure during the repair</h3>
            <p>
              Repeated edits pursued a ceiling instead of the requested small RUNBOOK.
              The target is 900–1500 Unicode characters; the ceiling is 3000.
              This is separate from the frozen skill comparison.
            </p>
          </figcaption>
          <ul className={styles.evidenceBars}>
            {evidence.documentation.observations.map((row) => (
              <li key={row.label} data-document-length={row.characters}>
                {row.label}: {row.characters} characters
                <span className={styles.evidenceTrack} role="img" aria-label={`${row.label}: ${row.characters} Unicode characters`}>
                  <span className={`${styles.evidenceBar} ${row.characters > 3000 ? styles.overBudget : ""}`} style={{ width: `${100 * row.characters / 3336}%` }} />
                </span>
              </li>
            ))}
          </ul>
          <p>
            The smaller document retains the real command surface and routes cleanup to the shared skill.
            Document length proves no future reliability; the failed attempts and owner interventions remain part of the record.
          </p>
        </figure>
      </div>
    </section>
  );
}
