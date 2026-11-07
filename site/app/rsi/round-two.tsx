// S-011 TK-003: shared-skill repair round two, the current result on /rsi.
// Charts are server-drawn bars and marks that need no interaction; every
// chart row links to its evidence entry on this page. The first attempt
// (repair.tsx) follows unchanged as history.
import { Fragment } from "react";
import { roundTwo, type ArmResult, type Run, type SkillResult } from "./round-two-data";
import styles from "./rsi.module.css";

const evidenceId = (skill: string) => `round-two-evidence-${skill}`;
const fraction = (pooled: string) => {
  const [passed, of] = pooled.split("/").map(Number);
  return { passed, of };
};
const runText = (r: Run) => (r.passed === null ? "ungraded" : `${r.pass ? "pass" : "fail"}, ${r.passed} of ${r.checks}`);
const armRuns = (a: ArmResult) => a.runs.map(runText).join("; ") + (a.note ? ` (${a.note})` : "");

function RunMarks({ runs }: { runs: Run[] }) {
  return (
    <span className={styles.runMarks}>
      {runs.map((r, i) => (
        <span
          key={r.id}
          data-run-result={r.pass === null ? "ungraded" : r.pass ? "pass" : "fail"}
          className={`${styles.runMark} ${r.pass ? styles.runPass : styles.runFail}`}
        >
          Run {i + 1}: {runText(r)}
        </span>
      ))}
    </span>
  );
}

function ArmRow({ role, arm, skill }: { role: "baseline" | "candidate"; arm: ArmResult; skill: string }) {
  const { passed, of } = fraction(arm.pooled ?? "0/1");
  return (
    <li data-arm-row={role} className={styles.armRow}>
      <a href={`#${evidenceId(skill)}`} className={styles.armLink}>
        <span>{role === "baseline" ? "Baseline" : "Candidate"}</span>
        <span className={styles.armTrack} aria-hidden="true">
          <span data-round-two-bar={role} className={`${styles.armBar} ${role === "candidate" ? styles.candidateBar : ""}`} style={{ width: `${(100 * passed) / of}%` }} />
        </span>
        <strong>
          {passed} of {of} · {arm.level}
        </strong>
      </a>
      <RunMarks runs={arm.runs} />
    </li>
  );
}

function comparisonText(base: ArmResult, cand: ArmResult) {
  return `baseline ${armRuns(base)}; candidate ${armRuns(cand)}`;
}

function SkillChart({ s }: { s: SkillResult }) {
  return (
    <li data-round-two-skill={s.skill} data-disposition={s.disposition.kind} className={styles.skillResult}>
      <h4>
        <code>{s.skill}</code> · {s.disposition.label}
      </h4>
      <p>{s.explanation}</p>
      <p className={styles.muted}>Mid tier, {s.baseline.mid.model}: checks passed, pooled across three runs, and each run graded.</p>
      <ul className={styles.armRows}>
        <ArmRow role="baseline" arm={s.baseline.mid} skill={s.skill} />
        <ArmRow role="candidate" arm={s.candidate.mid} skill={s.skill} />
      </ul>
      <div data-comparison-arms="" className={styles.comparisonArms}>
        <p>
          <strong>Comparison only, not gating.</strong> One run per arm; these runs do not decide the result.
        </p>
        <ul>
          <li>High, {s.baseline.high.model}: {comparisonText(s.baseline.high, s.candidate.high)}.</li>
          <li>Small, {s.baseline.small.model}: {comparisonText(s.baseline.small, s.candidate.small)}.</li>
        </ul>
      </div>
      <p data-disposition-detail="">
        <strong>{s.disposition.label}.</strong> {s.disposition.detail}
        {s.candidate.attempts ? ` ${s.candidate.attempts}` : null}
      </p>
    </li>
  );
}

function DevObservations() {
  const p = roundTwo.pruning;
  const scale = 3200;
  const pct = (n: number) => `${(100 * n) / scale}%`;
  return (
    <figure id="round-two-pruning" className={styles.place} data-round-two-dev="" aria-labelledby="round-two-pruning-title">
      <figcaption>
        <p className="eyebrow">Development observation</p>
        <h3 id="round-two-pruning-title">{p.skills}: shortening the RUNBOOK</h3>
        <p>
          Development observation, not a held-out result: the real RUNBOOK case ({p.startLength} Unicode characters) was
          reused while these candidates were developed, so it no longer tests them fresh. The target is {p.target[0]}–{p.target[1]} characters,
          with a goal near {p.goal} and a ceiling of {p.ceiling}.
        </p>
      </figcaption>
      <p className={styles.muted}>
        Characters after each run, on a common scale from zero. The shaded band is the {p.target[0]}–{p.target[1]} target; the line marks the {p.ceiling} ceiling.
      </p>
      {p.groups.map((g) => (
        <section key={g.label} className={styles.devGroup} aria-label={g.label}>
          <h4>{g.label}</h4>
          <ul className={styles.devRuns}>
            {g.lengths.map((n, i) => (
              <li key={i} data-dev-length={n}>
                <span>Run {i + 1}: {n} characters</span>
                <span className={styles.devTrack} aria-hidden="true">
                  <span className={styles.devBand} style={{ left: pct(p.target[0]), width: pct(p.target[1] - p.target[0]) }} />
                  <span className={styles.devCeiling} style={{ left: pct(p.ceiling) }} />
                  <span className={styles.devBar} style={{ width: pct(n) }} />
                </span>
              </li>
            ))}
          </ul>
        </section>
      ))}
      <p>
        All ten candidate runs landed inside the target band, and none lost a must-keep literal ({p.mustKeepLost} lost). A second
        reproduction, {p.second.name} at {p.second.startLength} characters, stayed above the target in all {p.second.runs} runs.
        Both skills were returned to the owner unmerged; qualifying them would need a new held-out case.
      </p>
    </figure>
  );
}

function Evidence() {
  return (
    <section id="round-two-evidence" className={styles.place} data-round-two-evidence="" aria-labelledby="round-two-evidence-title">
      <h3 id="round-two-evidence-title">Round-two evidence</h3>
      <p>The identities and grades behind the charts above. Private prompts, transcripts, fixture contents and skill text are excluded.</p>
      <dl className={styles.terms}>
        <dt>Recorded</dt>
        <dd>{roundTwo.recorded}</dd>
        <dt>Harness</dt>
        <dd>{roundTwo.harness}</dd>
        <dt>Baseline pin</dt>
        <dd>
          Unmodified shared skills at <code>{roundTwo.baselinePin}</code>
        </dd>
        {roundTwo.contracts.map((c) => (
          <Fragment key={c.id}>
            <dt>Contract {c.id}</dt>
            <dd>
              SHA-256 <code>{c.sha256}</code>. {c.status}
            </dd>
          </Fragment>
        ))}
        <dt>Judge limits</dt>
        <dd>{roundTwo.judgeLimits}</dd>
      </dl>
      <h4>Model tiers</h4>
      <ul className={styles.evidenceList}>
        {roundTwo.tiers.map((t) => (
          <li key={t.tier}>
            <strong>{t.tier}</strong>, {t.role}: <code>{t.model}</code>
          </li>
        ))}
      </ul>
      {roundTwo.skills.map((s) => (
        <section key={s.skill} id={evidenceId(s.skill)} className={styles.skillEvidence} aria-labelledby={`${evidenceId(s.skill)}-title`}>
          <h4 id={`${evidenceId(s.skill)}-title`}>
            <code>{s.skill}</code>
          </h4>
          <ul className={styles.evidenceList}>
            <li>Recorded failure: {s.failure}.</li>
            <li>Contract {s.contract}; shared skills PR {s.pr}.</li>
            <li>
              Candidate <code>{s.candidate.sha}</code>.
            </li>
            <li>Independent Frontier review: {s.review}.</li>
            <li>
              Disposition: {s.disposition.label}.{" "}
              {s.mainCommit ? (
                <>
                  Merge commit on the shared skills main branch: <code>{s.mainCommit}</code>.
                </>
              ) : (
                "No merge commit."
              )}
            </li>
            {(["baseline", "candidate"] as const).flatMap((role) =>
              (["mid", "high", "small"] as const).map((tier) => {
                const a = s[role][tier];
                return (
                  <li key={`${role}-${tier}`}>
                    {role === "baseline" ? "Baseline" : "Candidate"}, {a.tier} <code>{a.model}</code>: {armRuns(a)}
                    {a.pooled ? `; pooled ${fraction(a.pooled).passed} of ${fraction(a.pooled).of}, ${a.level}` : "; comparison only"}.
                  </li>
                );
              }),
            )}
          </ul>
        </section>
      ))}
    </section>
  );
}

export function RoundTwoEvidence() {
  return (
    <section id="round-two" className={`${styles.page} ${styles.repair}`} data-round-two="" aria-labelledby="round-two-title">
      <header className={styles.intro}>
        <p className="eyebrow">Shared-skill repair · round two · {roundTwo.recorded}</p>
        <h2 id="round-two-title">Shared-skill repairs, round two: the current result</h2>
        <p>
          Failures the owner found in five shared skills while this site was built were turned into fixed test
          reproductions. Each repaired skill, the candidate, ran three times beside the unmodified skill, the baseline,
          at the Mid tier, which decides. Three repairs moved from Broken to Excellent and were merged, one was merged
          on the owner&apos;s decision with no regression, and one was returned to the owner after three attempts.
        </p>
        <p>
          The first test contract, v1, was non-qualifying: the unmodified skills already scored Excellent for seven of
          eight skills, so it could not show a repair. The tests were rebuilt as contract v2 from the owner-found failures.
        </p>
      </header>
      <figure className={styles.place} data-round-two-chart="" aria-labelledby="round-two-chart-title">
        <figcaption>
          <h3 id="round-two-chart-title">Baseline and candidate, per skill</h3>
          <p className={styles.muted}>
            Bars show checks passed, pooled across the three Mid-tier runs, on a common scale from zero. Solid bars:
            baseline. Double-bordered bars: candidate. Each run is graded pass or fail; filled marks passed, dashed marks
            failed. The level is the fitness level: Excellent when all three runs pass, Broken when none do, and Broken
            whatever the count when a critical check fails, so a Broken row can include passing runs.
          </p>
        </figcaption>
        <ol className={styles.skillResults}>
          {roundTwo.skills.map((s) => (
            <SkillChart key={s.skill} s={s} />
          ))}
        </ol>
      </figure>
      <DevObservations />
      <p data-round-two-hold={roundTwo.onHold.skill} className={styles.note}>
        <code>{roundTwo.onHold.skill}</code> is on hold for the owner. No result is recorded for it.
      </p>
      <section className={styles.place} aria-labelledby="round-two-limits">
        <h3 id="round-two-limits">What round two shows</h3>
        <p>
          These are fitness levels on fixed reproductions of recorded failures. They have repeated runs and the prior
          version, but no control arm and no uncertainty interval, so this is not a held-out headline under the method
          below, and a level is not an Alignment Score. For the three repairs merged on their results, the recorded
          failure stopped reproducing in this harness.
        </p>
        <p>
          That does not establish broader benefit, native skill discovery, other hosts or later use. The merged repairs
          are not yet installed in the personal skill catalog; that installation is pending with the owner.
        </p>
      </section>
      <Evidence />
      <p className={styles.muted}>The first repair attempt, recorded 2026-11-02, follows unchanged as history.</p>
    </section>
  );
}
