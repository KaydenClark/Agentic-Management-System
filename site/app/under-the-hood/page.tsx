// /under-the-hood: how the AMS built itself, from S-006's build_events rows
// (S-003 TK-006). Server-rendered: the rows are read at build time, and again
// at most every ten minutes after, with the publishable key over plain
// Supabase REST (app/under-the-hood/history.ts); the key stays on the server.
// The prose here explains how to read the page; every word of the history
// itself comes from a row.
import type { Metadata } from "next";
import { History, KINDS, historyView, readBuildEvents } from "./history";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Under the hood | Agentic Management System",
  description: "How the AMS built itself: every Spec, Task, pull request, commit, correction and return, in time order, each linked to where it was recorded.",
};

// Re-read the rows at most every ten minutes on the deployed site.
export const revalidate = 600;

const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";
const S006 = "workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md";
const MIGRATION = "supabase/migrations/20261101132456_build_events.sql";

// Read by computed name so Next does not inline the values into the build
// output (it inlines a literal process.env.NEXT_PUBLIC_* reference); they are
// read from the server's environment at build and at each revalidation.
const ENV_URL = ["NEXT_PUBLIC", "SUPABASE_URL"].join("_");
const ENV_KEY = ["NEXT_PUBLIC", "SUPABASE_ANON_KEY"].join("_");

export default async function UnderTheHood() {
  const { rows, note } = await readBuildEvents({ url: process.env[ENV_URL], key: process.env[ENV_KEY] });
  const view = historyView(rows);
  return (
    <div className={styles.page} data-hood-page="">
      <header className={styles.intro}>
        <p className="eyebrow">Under the hood</p>
        <h1>Under the hood</h1>
        <p className="lede" data-opener="">
          This page is the build diary of the Agentic Management System, or <dfn id="ams">AMS</dfn>, drawn line by line
          from the system&apos;s own logbook rather than written by hand. Each line is one event, oldest first: a{" "}
          <dfn id="spec">Spec</dfn>, a written plan for one change, or a <dfn id="task">Task</dfn>, one slice of that
          plan, being written down; an <dfn id="agent">agent</dfn>, an AI assistant that carries out work, taking a
          Task on and handing it back; a <dfn id="commit">commit</dfn>, one saved change to the files; a{" "}
          <dfn id="pull-request">pull request</dfn>, a proposed change put up for review, being opened and merged; and
          the corrections and returns where work came back to be redone. Every line links to the place it was
          recorded, so you can check it yourself.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="reading">
        <h2 id="reading">How to read it</h2>
        <p>
          The events are grouped by the hour they happened in, in Mountain time. Open an hour to see its events; the
          first hour starts open. Each event shows what kind of event it is, the time, what happened, and a short
          reference such as a commit code or a Spec and Task number. The text of what happened is a link to the
          original record on GitHub.
        </p>
        <p>
          The boxes above the hours choose which kinds of event to show. Most events are commits, so turning commits
          off leaves the plans, the reviews and the rework easier to follow. The boxes work without scripts, and
          nothing you choose is stored.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="colors">
        <h2 id="colors">What the colors mean</h2>
        <p>Each color on this page has one meaning and no other.</p>
        <ul className={styles.legend}>
          <li>
            <span className={`tone h-returned ${styles.swatch}`}>Purple</span> It came back for rework: a correction,
            such as a review finding or the owner asking for a change, or a pull request closed without being merged.
          </li>
          <li>
            <span className={`tone h-agent ${styles.swatch}`}>Green</span> An agent did it, as the record itself says:
            an agent taking a Task on or handing it back, or a commit whose recorded author is an agent.
          </li>
          <li>
            <span className={`tone h-none ${styles.swatch}`}>Grey</span> Everything else. Grey says nothing about who did
            the work: many commits were made by agents under the owner&apos;s name, and their records do not say so.
          </li>
        </ul>
      </section>

      <section className={styles.section} aria-labelledby="history-heading">
        <h2 id="history-heading">The build history</h2>
        <History view={view} note={note} styles={styles} labelledBy="history-heading" />
      </section>

      <section className={styles.section} aria-labelledby="kinds">
        <h2 id="kinds">The kinds of event</h2>
        <dl className={styles.kinds}>
          {Object.entries(KINDS).map(([kind, { label, about }]) => (
            <div key={kind} className={styles.kind}>
              <dt>{label}</dt>
              <dd>{about}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className={styles.section} aria-labelledby="source">
        <h2 id="source">Where the events come from</h2>
        <p>
          A local import reads the real records, the Git history, the pull requests and the Spec and Task files, and
          writes one row per event into a Supabase table. This page only reads that table, with a key that can read
          and cannot write, and writes nothing back. Rows marked as tests are hidden by the table&apos;s own rules and
          filtered again here, so they never appear.
          <span className={styles.source}>
            {" "}
            Sources: <a href={`${REPO_BLOB}${S006}`}>S-006, RSI data store</a>;{" "}
            <a href={`${REPO_BLOB}${MIGRATION}`}>the table&apos;s definition</a>.
          </span>
        </p>
        <p>
          The list is only as complete as the last import. Records that exist only on the development branch are not
          imported yet, and the import does not run on a schedule, so recent work can be missing until it runs again.
          Private links to agent working sessions are removed from the text before it is shown.
        </p>
      </section>
    </div>
  );
}
