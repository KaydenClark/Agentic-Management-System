// The /rsi page body (S-007). Pure: it renders the series views it is given
// and reads nothing, so render tests can feed it labeled fixtures and the
// page feeds it Supabase rows. Every number is a link to the rows behind it,
// and each row shows its strength label.
import type { Arm, Count, ExecutionState, Mark, Point, RsiResult, Series, SeriesView, Strength } from "./data";
import { SPLITS } from "./series";
import styles from "./rsi.module.css";

const STRENGTH: Record<Strength, string> = {
  recorded_fact: "Recorded fact",
  anecdote: "Anecdote",
  single_trial: "Single trial",
  repeated_trials: "Repeated trials",
  held_out_with_interval: "Held-out with interval",
};

const ARM: Record<Arm, string> = {
  ams: "AMS arm",
  no_ams: "No-AMS control arm",
  plain_instructions: "Plain-instructions control arm",
};

const STATE: Record<ExecutionState, string> = {
  completed: "completed",
  runner_error: "runner error",
  auth_error: "auth error",
  timeout: "timed out",
  capped: "capped",
};

const short = (commit: string) => commit.slice(0, 7);
const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

function Explanation() {
  return (
    <dl className={styles.terms} data-explanation="">
      <dt>Task</dt>
      <dd>A task is a repeatable test case: a fixed piece of work with a grader that decides pass or fail.</dd>
      <dt>Trial</dt>
      <dd>A trial is one attempt at a task, recorded as one row with its result, cost, tokens and source.</dd>
      <dt>Version</dt>
      <dd>A version is the system that ran the trial, named by the commits of its runtime, controls and skills. Changing any of them makes a new version.</dd>
    </dl>
  );
}

function countText(c: Count): string {
  if (c.key === "passed") return `${c.passed} of ${plural(c.of, "graded trial", "graded trials")} passed`;
  return `${plural(c.of, "trial", "trials")} not graded`;
}

function rowResult(r: RsiResult): string {
  if (r.execution_state !== "completed") return `not graded (${STATE[r.execution_state] ?? r.execution_state})`;
  if (r.passed === true) return "passed";
  if (r.passed === false) return "failed";
  return `scored ${r.score}, no pass grade`;
}

function Row({ row, placeId, runUrl }: { row: RsiResult; placeId: string; runUrl: string | null }) {
  const href = row.source_url ?? runUrl;
  const tokens = Number(row.input_tokens) + Number(row.output_tokens);
  return (
    <li data-row="" data-row-id={String(row.id)} id={`${placeId}-row-${row.id}`} className={styles.row}>
      Row {row.id}: task <code data-label="">{row.task_id}</code>, trial {row.trial}, {rowResult(row)}; cost ${String(row.cost_usd)},{" "}
      {tokens} tokens, {row.turns} turns. Strength: <span data-strength="" className={styles.strength}>{STRENGTH[row.strength] ?? row.strength}</span>.
      Source: {href ? <a href={href}>{row.source_kind} {row.source_ref}</a> : <code>{row.source_kind} {row.source_ref}</code>}.
    </li>
  );
}

function MarkItem({ mark }: { mark: Mark }) {
  return (
    <li data-mark={mark.kind} className={styles.mark}>
      <strong>{mark.label}</strong>
      {mark.detail ? (
        <>
          : <q data-label="">{mark.detail}</q>
        </>
      ) : null}
    </li>
  );
}

function PointItem({ point, rowsBase, placeId }: { point: Point; rowsBase: string; placeId: string }) {
  const runUrl = (id: number) => point.runs.find((r) => r.id === id)?.source_url ?? null;
  return (
    <li data-point="" data-version={point.version.id} className={styles.point}>
      <p className={styles.version}>
        Version{" "}
        <code data-label="">
          runtime {short(point.version.runtime)} · controls {short(point.version.controls)} · skills {short(point.version.skills)}
        </code>
      </p>
      <p className={styles.counts}>
        {point.counts.map((c, i) => (
          <span key={c.key}>
            {i > 0 ? "; " : null}
            <a data-number="" href={`#${rowsBase}-${c.key}`} data-row-ids={c.rows.map((r) => r.id).join(" ")}>
              {countText(c)}
            </a>
          </span>
        ))}
      </p>
      {point.marks.length > 0 ? (
        <ul className={styles.marks}>
          {point.marks.map((m) => (
            <MarkItem key={m.kind} mark={m} />
          ))}
        </ul>
      ) : null}
      {point.counts.map((c) => (
        <div key={c.key} id={`${rowsBase}-${c.key}`} data-rows="" className={styles.rows}>
          <p className={styles.rowsTitle}>Rows behind “{countText(c)}”</p>
          <ul>
            {c.rows.map((r) => (
              <Row key={r.id} row={r} placeId={placeId} runUrl={runUrl(r.run_id)} />
            ))}
          </ul>
        </div>
      ))}
    </li>
  );
}

// A small server-drawn line: x is the version's place in the page's version
// order, y the share of graded trials that passed. Drawn only from the counts
// shown beside it; the numbers themselves are in the linked list.
const W = 320;
const H = 96;
const PAD = 8;

function SeriesLine({ series, versionOrder, label }: { series: Series; versionOrder: readonly string[]; label: string }) {
  const n = Math.max(1, versionOrder.length - 1);
  const coords = series.points.map((p) => {
    const c = p.counts.find((k) => k.key === "passed");
    const x = PAD + (versionOrder.indexOf(p.version.id) / n) * (W - 2 * PAD);
    const y = c ? PAD + (1 - (c.passed ?? 0) / c.of) * (H - 2 * PAD) : null;
    return { x, y, regression: p.marks.some((m) => m.kind === "regression") };
  });
  const drawn = coords.filter((c): c is { x: number; y: number; regression: boolean } => c.y !== null);
  const line = drawn.length >= 2 && drawn.length === coords.length;
  return (
    <svg className={styles.line} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${label}: pass share per version; the numbers are listed below`}>
      <rect className={styles.frame} x="0.5" y="0.5" width={W - 1} height={H - 1} />
      {line ? <polyline className={styles.stroke} points={drawn.map((c) => `${c.x},${c.y}`).join(" ")} /> : null}
      {drawn.map((c, i) =>
        c.regression ? (
          <rect key={i} className={styles.regressionDot} x={c.x - 4} y={c.y - 4} width="8" height="8" />
        ) : (
          <circle key={i} className={styles.dot} cx={c.x} cy={c.y} r="3.5" />
        ),
      )}
    </svg>
  );
}

function SeriesBlock({ series, index, view }: { series: Series; index: number; view: SeriesView }) {
  const label = `${series.taskId ? `Task ${series.taskId}, ` : ""}${ARM[series.arm] ?? series.arm}, ${series.model}`;
  return (
    <section
      className={styles.series}
      data-series={`${view.id}-${index}`}
      data-arm={series.arm}
      data-provider={series.provider}
      data-model={series.model}
      data-effort={series.effort}
      aria-label={label}
    >
      <h4 className={styles.seriesTitle}>
        {series.taskId ? (
          <>
            Task <code data-label="">{series.taskId}</code>,{" "}
          </>
        ) : null}
        {ARM[series.arm] ?? series.arm}
      </h4>
      <p className={styles.provenance} data-provenance="">
        Provider <code data-label="">{series.provider}</code>, model <code data-label="">{series.model}</code>, effort{" "}
        <code data-label="">{series.effort}</code>. A different provider, model or effort starts a new series.
      </p>
      <SeriesLine series={series} versionOrder={view.versions.map((v) => v.id)} label={label} />
      <ol className={styles.points}>
        {series.points.map((p, i) => (
          <PointItem key={p.version.id} point={p} rowsBase={`${view.id}-s${index}-p${i}`} placeId={view.id} />
        ))}
      </ol>
    </section>
  );
}

function SeriesPlace({ series: view }: { series: SeriesView }) {
  const headingId = `rsi-${view.id}`;
  return (
    <figure className={styles.place} data-chart-place={view.id} aria-labelledby={headingId}>
      <figcaption className={styles.caption}>
        <h3 id={headingId} className={styles.placeTitle}>{view.title}</h3>
        <p className={styles.muted}>{view.shows}</p>
      </figcaption>
      {view.empty ? (
        <>
          <div className={styles.plot} data-plot="" role="img" aria-label={`${view.title}: empty, no trials are recorded yet`} />
          <p className={styles.empty} data-empty-message="">No trials are recorded yet.</p>
        </>
      ) : (
        <div className={styles.filled} data-plot="">
          {view.series.map((s, i) => (
            <SeriesBlock key={s.key} series={s} index={i} view={view} />
          ))}
        </div>
      )}
      <Explanation />
      <p className={styles.next} data-next-event="">
        <strong>Next expected event:</strong> {view.nextEvent.text}{" "}
        Source: <a href={view.nextEvent.source.href}>{view.nextEvent.source.label}</a>.
      </p>
    </figure>
  );
}

export function RsiView({ views, unavailable }: { views: readonly SeriesView[]; unavailable: boolean }) {
  const anyRows = views.some((v) => !v.empty);
  return (
    <div className={styles.page} data-rsi-page="">
      <header className={styles.intro}>
        <p className="eyebrow">Results</p>
        <h1>RSI results</h1>
        {anyRows ? (
          <p className="lede">
            What the RSI loop has measured: how each task and each version of the system did, including no change and
            regressions. Every number links to the rows behind it, and each row shows how strong its evidence is.
          </p>
        ) : (
          <p className="lede">
            This page will show what the RSI loop measures: how each task and each version of the system did, including
            no change and regressions, with every number linked to the rows behind it. Nothing has been measured yet, so
            every place below is empty on purpose. No sample or placeholder data is shown.
          </p>
        )}
        {unavailable ? (
          <p className={styles.note} data-load-note="">
            Results could not be loaded from the data store just now, so every place shows its empty state. The page
            tries again on its next refresh.
          </p>
        ) : null}
        <p className={styles.muted}>
          Colors: this page uses no signal colors yet. A grey dashed frame marks a chart place with nothing in it; a
          square point marks a regression.
        </p>
      </header>
      {SPLITS.map(({ split, title, about }) => (
        <section key={split} className={styles.split} data-split={split} aria-labelledby={`rsi-split-${split}`}>
          <h2 id={`rsi-split-${split}`}>{title}</h2>
          <p className={styles.muted}>{about}</p>
          <div className={styles.places}>
            {views
              .filter((v) => v.split === split)
              .map((view) => (
                <SeriesPlace key={view.id} series={view} />
              ))}
          </div>
        </section>
      ))}
    </div>
  );
}
