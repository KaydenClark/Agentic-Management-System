// /rsi: the RSI chart page (S-007). Server-rendered and prerendered at build.
// TK-001 renders every planned series place from the empty fixture; TK-002
// swaps the fixture for Supabase rows through `seriesViews`.
import type { Metadata } from "next";
import { seriesViews, type SeriesView } from "./data";
import { emptyRows } from "./fixtures/empty";
import { SPLITS } from "./series";
import styles from "./rsi.module.css";

export const metadata: Metadata = {
  title: "RSI results | Agentic Management System",
  description: "Where the RSI loop's measured results will appear, per task and per version, held-out and dev kept apart.",
};

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

function SeriesPlace({ series }: { series: SeriesView }) {
  const headingId = `rsi-${series.id}`;
  return (
    <figure className={styles.place} data-chart-place={series.id} aria-labelledby={headingId}>
      <figcaption className={styles.caption}>
        <h3 id={headingId} className={styles.placeTitle}>{series.title}</h3>
        <p className={styles.muted}>{series.shows}</p>
      </figcaption>
      <div className={styles.plot} data-plot="" role="img" aria-label={`${series.title}: empty, no trials are recorded yet`} />
      {series.empty ? (
        <p className={styles.empty} data-empty-message="">No trials are recorded yet.</p>
      ) : (
        <p className={styles.empty} data-pending-chart="">Rows exist for this series; this page does not chart them yet.</p>
      )}
      <Explanation />
      <p className={styles.next} data-next-event="">
        <strong>Next expected event:</strong> {series.nextEvent.text}{" "}
        Source: <a href={series.nextEvent.source.href}>{series.nextEvent.source.label}</a>.
      </p>
    </figure>
  );
}

export default function RsiPage() {
  const views = seriesViews(emptyRows);
  return (
    <div className={styles.page} data-rsi-page="">
      <header className={styles.intro}>
        <p className="eyebrow">Results</p>
        <h1>RSI results</h1>
        <p className="lede">
          This page will show what the RSI loop measures: how each task and each version of the system did, including
          no change and regressions, with every number linked to the rows behind it. Nothing has been measured yet, so
          every place below is empty on purpose. No sample or placeholder data is shown.
        </p>
        <p className={styles.muted}>
          Colors: this page uses no signal colors yet. A grey dashed frame marks a chart place with nothing in it.
        </p>
      </header>
      {SPLITS.map(({ split, title, about }) => (
        <section key={split} className={styles.split} data-split={split} aria-labelledby={`rsi-split-${split}`}>
          <h2 id={`rsi-split-${split}`}>{title}</h2>
          <p className={styles.muted}>{about}</p>
          <div className={styles.places}>
            {views.filter((v) => v.split === split).map((series) => (
              <SeriesPlace key={series.id} series={series} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
