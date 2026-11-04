// S-007 TK-002J: "Is RSI improving each skill?" on /rsi. Server-drawn SVG,
// one chart per charted skill (one point per recorded loop, a running
// average, a fitness-level strip, a new line at each test contract or model
// change) and one skills-by-loops "Fitness level per loop" strip. Pure: it
// renders the loop records it is given, so render tests can feed a labeled
// fixture and the page feeds the recorded loops.
import { Fragment, type ReactNode } from "react";
import {
  AVERAGE_FROM,
  AVERAGE_WINDOW,
  FITNESS_LEVELS,
  NOT_CHARTED,
  RESTART_OFFSET,
  skillTrends,
  type BreakReason,
  type FitnessLevel,
  type LoopRecord,
  type SecondaryRun,
  type SkillTrend,
  type TrendLine,
  type TrendPoint,
} from "./skill-loops";
import styles from "./rsi.module.css";

const LEVEL_CLASS: Record<FitnessLevel, string> = {
  Excellent: styles.levelExcellent,
  Stable: styles.levelStable,
  Functional: styles.levelFunctional,
  Broken: styles.levelBroken,
};

const LEVEL_MEANING: Record<FitnessLevel, { hue: string; meaning: string }> = {
  Excellent: { hue: "green", meaning: "all three deciding runs passed" },
  Stable: { hue: "blue", meaning: "two of the three deciding runs passed" },
  Functional: { hue: "amber", meaning: "one of the three deciding runs passed" },
  Broken: { hue: "orange-red, trouble", meaning: "no deciding run passed, or a critical check failed" },
};

const pct = (share: number) => `${Math.round(share * 100)}%`;
const fraction = (passed: number, checks: number) => `${passed} of ${checks} checks (${pct(passed / checks)})`;
const BREAK_TEXT: Record<BreakReason, string> = { contract: "new test contract", model: "new model" };
const breakText = (b: BreakReason[]) => b.map((r) => BREAK_TEXT[r]).join(" and ");
const loopName = (n: number) => (n === 0 ? "start" : `loop ${n}`);

// Chart geometry, in SVG user units. The SVG draws marks only; every label is
// HTML placed beside it by percentage, so text contrast is decidable and the
// text reflows with the page.
const W = 300;
const X0 = 50;
const X1 = 250;
const TOP = 14;
const BASE = 156; // y of 0%
const H = 166;
const Y = (share: number) => TOP + (1 - share) * (BASE - TOP);
const left = (x: number) => ({ left: `${(100 * x) / W}%` });
const SHORT: Record<FitnessLevel, string> = { Excellent: "Ex", Stable: "St", Functional: "Fu", Broken: "Br" };

function secondaryMark(run: SecondaryRun, x: number, key: string) {
  if (run.passed === null) return null;
  const y = Y(run.passed / run.checks);
  const title = <title>{`${run.tier} run, comparison only: ${fraction(run.passed, run.checks)}`}</title>;
  return run.tier === "High" ? (
    <path key={key} data-secondary-mark="High" className={styles.secondaryMark} d={`M${x - 11} ${y - 5} l5 9 h-10 z`}>
      {title}
    </path>
  ) : (
    <rect key={key} data-secondary-mark="Small" className={styles.secondaryMark} x={x + 7} y={y - 4} width="8" height="8">
      {title}
    </rect>
  );
}

function TrendChart({ trend, maxLoop }: { trend: SkillTrend; maxLoop: number }) {
  const span = Math.max(1, maxLoop);
  const X = (at: number) => X0 + (at / span) * (X1 - X0);
  const step = (X1 - X0) / span;
  // Strip cells stay apart even where a new line starts just after a loop.
  const cell = Math.min(step * (trend.lines.length > 1 ? RESTART_OFFSET - 0.04 : 0.8), 2 * X0, 2 * (W - X1));
  const points = trend.lines.flatMap((l) => l.points);
  const summary = trend.lines
    .map((l) => l.points.map((p) => `${p.kind === "start" ? (p.loop === 0 ? "start" : `restart after loop ${p.loop}`) : loopName(p.loop)} ${pct(p.score)} ${p.measured.level}`).join(", "))
    .join("; then a new line: ");
  const breaks = trend.lines.filter((l) => l.breaks.length > 0).map((l) => ({ line: l, x: X(l.points[0].at - RESTART_OFFSET / 2) }));
  return (
    <div className={styles.trendFigure}>
      {breaks.length > 0 ? (
        <div className={styles.chartBreaks}>
          {breaks.map(({ line, x }, i) => (
            <span key={i} className={`${styles.chartLabel} ${x > W / 2 ? styles.labelEnd : ""} ${i % 2 ? styles.labelLower : ""}`} style={x > W / 2 ? { right: `${100 - (100 * x) / W}%` } : left(x)} data-break-label={line.breaks.join(" ")}>
              {line.breaks.map((b) => (b === "contract" ? `new contract ${line.contract}` : "new model")).join(", ")}
            </span>
          ))}
        </div>
      ) : null}
      <div className={styles.chartAxis} aria-hidden="true">
        {[1, 0.5, 0].map((t) => (
          <span key={t} className={styles.axisLabel} style={{ top: `${(100 * Y(t)) / H}%` }}>
            {pct(t)}
          </span>
        ))}
      </div>
      <svg className={styles.trendChart} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${trend.skill}: Alignment Score per loop, ${summary}. The values are listed below the chart.`}>
        {[0, 0.5, 1].map((t) => (
          <line key={t} className={styles.gridLine} x1={0} x2={W} y1={Y(t)} y2={Y(t)} />
        ))}
        {breaks.map(({ line, x }, i) => (
          <g key={`break-${i}`} data-break={line.breaks.join(" ")}>
            <title>{breakText(line.breaks)}</title>
            <line className={styles.breakLine} x1={x} x2={x} y1={0} y2={BASE} />
          </g>
        ))}
        {trend.lines.map((line, li) => (
          <g key={`line-${li}`} data-trend-line={li} data-contract={line.contract} data-model={line.model}>
            {line.points.length > 1 ? <polyline className={styles.trendLine} points={line.points.map((p) => `${X(p.at)},${Y(p.score)}`).join(" ")} /> : null}
            {line.points.length >= AVERAGE_FROM ? (
              <polyline data-running-average="" className={styles.averageLine} points={line.points.map((p) => `${X(p.at)},${Y(p.average)}`).join(" ")} />
            ) : null}
            {line.points.map((p, pi) => {
              const x = X(p.at);
              const prevAt = pi > 0 ? line.points[pi - 1].at : p.at;
              return (
                <g key={pi}>
                  {p.notKept.map((a, ai) => (
                    <circle
                      key={`a${ai}`}
                      data-not-kept={a.version}
                      className={styles.notKeptMark}
                      cx={X(prevAt + ((ai + 1) / (p.notKept.length + 1)) * (p.at - prevAt))}
                      cy={Y(a.passed / a.checks)}
                      r="4"
                    >
                      <title>{`Attempt ${a.attempt} ${a.version}, not kept: ${fraction(a.passed, a.checks)}, ${a.level}`}</title>
                    </circle>
                  ))}
                  {p.secondary.map((r, ri) => secondaryMark(r, x, `s${ri}`))}
                  {p.regression ? <circle data-regression="" className={styles.regressionRing} cx={x} cy={Y(p.score)} r="10" /> : null}
                  <circle
                    data-trend-point={p.kind}
                    data-loop={p.loop}
                    data-score={p.measured.passed + "/" + p.measured.checks}
                    data-level={p.measured.level}
                    className={`${styles.trendPoint} ${LEVEL_CLASS[p.measured.level]}`}
                    cx={x}
                    cy={Y(p.score)}
                    r="6"
                  >
                    <title>{`${p.kind === "start" ? "Start" : loopName(p.loop)}: ${fraction(p.measured.passed, p.measured.checks)}, ${p.measured.level}`}</title>
                  </circle>
                </g>
              );
            })}
          </g>
        ))}
      </svg>
      <div className={styles.chartTicks} aria-hidden="true">
        {Array.from({ length: span + 1 }, (_, k) => (
          <span key={k} className={styles.tickLabel} style={left(X(k))}>
            {k === 0 ? "start" : span <= 3 ? `loop ${k}` : k}
          </span>
        ))}
      </div>
      <div className={styles.chartStrip} data-level-strip="">
        {points.map((p, i) => (
          <span key={i} className={`${styles.stripCell} ${LEVEL_CLASS[p.measured.level]}`} style={{ left: `${(100 * (X(p.at) - cell / 2)) / W}%`, width: `${(100 * cell) / W}%` }} title={p.measured.level}>
            {cell >= 70 ? (
              <>
                <span>{p.measured.level}</span>
                <span>{pct(p.score)}</span>
              </>
            ) : (
              SHORT[p.measured.level]
            )}
          </span>
        ))}
      </div>
    </div>
  );
}

function secondaryText(runs: SecondaryRun[]) {
  return runs
    .map((r) => `${r.tier} run (${r.model}): ${r.passed === null ? "ungraded" : fraction(r.passed, r.checks)}${r.note ? `, ${r.note}` : ""}`)
    .join("; ");
}

function PointText({ p, line, li }: { p: TrendPoint; line: TrendLine; li: number }) {
  const name =
    p.kind === "start"
      ? li === 0
        ? `Start, version ${p.measured.version}`
        : `Restart after loop ${p.loop} (${breakText(line.breaks)}), version ${p.measured.version} measured again`
      : `${loopName(p.loop)[0].toUpperCase()}${loopName(p.loop).slice(1)}, ${p.keptStart ? `no attempt kept, so the start version ${p.measured.version} stands` : `kept version ${p.measured.version}`}`;
  return (
    <li data-trend-point-text={p.kind} data-loop={p.loop}>
      <a href={p.evidence}>
        {name}: {fraction(p.measured.passed, p.measured.checks)}, {p.measured.level}.
      </a>
      {p.regression ? <strong data-regression-text=""> Lower than the point before.</strong> : null}
      {p.notKept.length > 0 ? (
        <ul className={styles.trendSubList}>
          {p.notKept.map((a) => (
            <li key={a.version} data-not-kept-text={a.version}>
              Not kept, attempt {a.attempt} <code>{a.version}</code>: {fraction(a.passed, a.checks)}, {a.level}; {a.why}.
            </li>
          ))}
        </ul>
      ) : null}
      {p.secondary.length > 0 ? <p className={styles.trendSecondary}>Comparison only, not deciding: {secondaryText(p.secondary)}.</p> : null}
    </li>
  );
}

function TrendCard({ trend, maxLoop }: { trend: SkillTrend; maxLoop: number }) {
  const first = trend.lines[0].points[0];
  return (
    <li className={styles.trendCard} data-trend-skill={trend.skill} data-lines={trend.lines.length}>
      <h3 className={styles.trendTitle}>
        <code>{trend.skill}</code>
      </h3>
      <p className={styles.trendOutcome} data-trend-outcome="">
        {trend.outcome}: {first.measured.level} {pct(first.score)} at the start, {trend.latest.measured.level} {pct(trend.latest.score)} after {loopName(trend.loops)}.
      </p>
      <ul className={styles.trendMeta} data-trend-provenance="">
        {trend.lines.map((l, li) => (
          <li key={li}>
            {trend.lines.length > 1 ? `Line ${li + 1}${l.breaks.length ? ` (${breakText(l.breaks)})` : ""}: ` : null}
            Test contract <code>{l.contract}</code>, deciding tier {l.tier}, <code>{l.model}</code>
          </li>
        ))}
      </ul>
      <TrendChart trend={trend} maxLoop={maxLoop} />
      <ol className={styles.trendPoints} data-trend-points="">
        {trend.lines.map((l, li) =>
          l.points.map((p, pi) => <PointText key={`${li}-${pi}`} p={p} line={l} li={li} />),
        )}
      </ol>
    </li>
  );
}

function LevelSwatch({ level }: { level: FitnessLevel }) {
  return (
    <span className={`${styles.levelSwatch} ${LEVEL_CLASS[level]}`} aria-hidden="true">
      {SHORT[level]}
    </span>
  );
}

function MarkSwatch({ children }: { children: ReactNode }) {
  return (
    <svg className={styles.swatch} viewBox="0 0 28 18" aria-hidden="true">
      {children}
    </svg>
  );
}

function Legend() {
  return (
    <div className={styles.trendLegend} data-trend-legend="">
      <h3 className={styles.legendTitle}>What the colors and marks mean</h3>
      <ul>
        {FITNESS_LEVELS.map((l) => (
          <li key={l} data-legend-level={l}>
            <LevelSwatch level={l} />
            <span>
              <strong>{l}</strong> ({LEVEL_MEANING[l].hue}): {LEVEL_MEANING[l].meaning}.
            </span>
          </li>
        ))}
      </ul>
      <p className={styles.muted}>
        These four colors mean fitness levels and nothing else on this page, except that orange-red means trouble
        everywhere here: a Broken level, or results that could not be loaded. Each cell also carries the level&apos;s
        name or its two-letter short form, so the colors are never the only cue.
      </p>
      <ul>
        <li>
          <MarkSwatch>
            <circle className={`${styles.trendPoint} ${styles.levelExcellent}`} cx="14" cy="9" r="6" />
          </MarkSwatch>
          <span>A plotted point: the Alignment Score of the version a loop kept, filled with its level.</span>
        </li>
        <li>
          <MarkSwatch>
            <circle className={styles.notKeptMark} cx="14" cy="9" r="4" />
          </MarkSwatch>
          <span>Dashed hollow circle: an attempt the loop did not keep. It never decides a point.</span>
        </li>
        <li>
          <MarkSwatch>
            <path className={styles.secondaryMark} d="M3 4 l5 9 h-10 z" transform="translate(4 0)" />
            <rect className={styles.secondaryMark} x="17" y="5" width="8" height="8" />
          </MarkSwatch>
          <span>Hollow triangle: a High tier run. Hollow square: a Small tier run. Comparison only; they never decide a point.</span>
        </li>
        <li>
          <MarkSwatch>
            <circle className={styles.regressionRing} cx="14" cy="9" r="7" />
          </MarkSwatch>
          <span>Dashed ring: a point lower than the one before it on its line.</span>
        </li>
        <li>
          <MarkSwatch>
            <line className={styles.averageLine} x1="2" x2="26" y1="9" y2="9" />
          </MarkSwatch>
          <span>
            Thick line: the running average, a plain mean of up to the last {AVERAGE_WINDOW} points, drawn once a line
            has {AVERAGE_FROM} points. It is a display aid, not a statistical test.
          </span>
        </li>
        <li>
          <MarkSwatch>
            <line className={styles.breakLine} x1="14" x2="14" y1="1" y2="17" />
          </MarkSwatch>
          <span>Dashed upright line: a new test contract or model. Scores compare only within one, so a new line starts.</span>
        </li>
      </ul>
    </div>
  );
}

function LevelPerLoop({ trends, maxLoop }: { trends: SkillTrend[]; maxLoop: number }) {
  const columns = Array.from({ length: Math.max(1, maxLoop) + 1 }, (_, k) => k);
  return (
    <figure className={styles.place} data-level-per-loop="" aria-labelledby="level-per-loop-title">
      <figcaption>
        <h3 id="level-per-loop-title" className={styles.placeTitle}>
          Fitness level per loop
        </h3>
        <p className={styles.muted}>Every charted skill, one cell per loop, colored and named by its fitness level, with its Alignment Score.</p>
      </figcaption>
      <div className={styles.levelScroll}>
        <table className={styles.levelTable}>
          <thead>
            <tr>
              <th scope="col">Skill</th>
              {columns.map((k) => (
                <th key={k} scope="col">
                  {k === 0 ? "Start" : `Loop ${k}`}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {trends.map((t) => {
              const byLoop = new Map<number, { p: TrendPoint; brk: BreakReason[] }>();
              t.lines.forEach((l, li) =>
                l.points.forEach((p, pi) => {
                  if (p.kind === "loop" || (li === 0 && pi === 0)) byLoop.set(p.loop, { p, brk: pi === 1 ? l.breaks : [] });
                }),
              );
              return (
                <tr key={t.skill} data-level-row={t.skill}>
                  <th scope="row">
                    <code>{t.skill}</code>
                  </th>
                  {columns.map((k) => {
                    const c = byLoop.get(k);
                    if (!c) return <td key={k} className={styles.levelNone} data-level-cell="none">Not recorded</td>;
                    return (
                      <td key={k} className={`${styles.levelCell} ${LEVEL_CLASS[c.p.measured.level]} ${c.brk.length ? styles.levelBreak : ""}`} data-level-cell={c.p.measured.level} data-loop={k} data-break={c.brk.join(" ") || undefined}>
                        <a href={c.p.evidence}>
                          {c.brk.length ? <span className={styles.levelBreakText}>{breakText(c.brk)}</span> : null}
                          <span className={styles.levelName}>{c.p.measured.level}</span>
                          <span>{pct(c.p.score)}</span>
                        </a>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </figure>
  );
}

export function SkillTrends({ records }: { records: readonly LoopRecord[] }) {
  const trends = skillTrends(records);
  const maxLoop = Math.max(1, ...trends.map((t) => t.loops));
  const [lengthA, lengthB] = NOT_CHARTED.length.split(" and ");
  return (
    <section id="skill-trends" className={`${styles.page} ${styles.trends}`} data-skill-trends="" aria-labelledby="skill-trends-title">
      <header className={styles.intro}>
        <p className="eyebrow">Skill trends · {maxLoop === 1 ? "one RSI loop recorded" : `${maxLoop} RSI loops recorded`}</p>
        <h2 id="skill-trends-title">Is RSI improving each skill?</h2>
        <p>
          Each RSI loop adds one point per skill: the Alignment Score of the version that loop kept. Higher is better, and
          a line that climbs over loops means the loop is improving that skill.{" "}
          {maxLoop === 1
            ? "One loop is recorded so far, so each skill shows two points: its start and its loop-1 result. Every new loop adds a point."
            : null}
        </p>
      </header>
      <dl className={styles.trendTerms} data-trend-explanation="">
        <div>
          <dt>One loop</dt>
          <dd>Find a recorded failure, assess up to three repaired versions, and keep one that passes its trials and review, or keep the version it started from.</dd>
        </div>
        <div>
          <dt>The plotted point</dt>
          <dd>The Alignment Score: checks passed, pooled over the three deciding runs at the Mid tier, as a percentage. The first point is the version the loop started from.</dd>
        </div>
        <div>
          <dt>Fitness level</dt>
          <dd>Excellent when all three deciding runs pass, Stable at two, Functional at one and Broken at none; a critical failure makes it Broken whatever the count.</dd>
        </div>
        <div>
          <dt>High and Small</dt>
          <dd>One run each on a stronger and a smaller model, for comparison. They are drawn as small marks and never decide a point.</dd>
        </div>
      </dl>
      <Legend />
      <ul className={styles.trendGrid}>
        {trends.map((t) => (
          <TrendCard key={t.skill} trend={t} maxLoop={maxLoop} />
        ))}
      </ul>
      <LevelPerLoop trends={trends} maxLoop={maxLoop} />
      <p className={styles.note} data-not-charted="">
        Not charted: <code>{lengthA}</code> and <code>{lengthB}</code> are measured by document length, not an Alignment
        Score (see <a href="#round-two-pruning">their development observations</a>), and <code>{NOT_CHARTED.onHold}</code> is on hold
        for the owner, with no result. Source of the points: {trends[0]?.source ?? "no loop recorded"}; the evidence for every
        point is linked from it.
      </p>
    </section>
  );
}
