// /how-it-works: How it works, the second tour page (S-003 TK-002). The
// records, the lifecycle, and one real Spec and Task linked to their files on
// GitHub. Every claim links the committed record it comes from.
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "How it works | Agentic Management System",
  description: "The records the AMS keeps, the life of a piece of work, and one real Spec and Task from this site.",
};

const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";
const ADR = "workbench/docs/adr/";
const S003 = "workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/";

// A link to the committed record a claim comes from.
function Source({ path, children }: { path: string; children: ReactNode }) {
  return (
    <span className={styles.source}>
      {" "}
      Source: <a href={`${REPO_BLOB}${path}`}>{children}</a>.
    </span>
  );
}

export default function HowItWorks() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>How it works</h1>
        <p className="lede" data-opener="">
          In the Agentic Management System, or <dfn id="ams">AMS</dfn>, work is written down before it is done. A request becomes a <dfn id="spec">Spec</dfn>: a short
          written plan for one change, with the conditions that will show it worked. Each Spec is cut into{" "}
          <dfn id="task">Tasks</dfn>, each small enough for one <dfn id="agent">agent</dfn>, an AI assistant that
          carries out work, to finish in a single run. The agent hands back proof, and only Kayden, the owner, moves
          finished work into the main version of the site.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="records">
        <h2 id="records">The records</h2>
        <p>
          The records are plain text files in this public repository, and each kind of truth has one home; other files
          link to that home rather than repeat it.
          <Source path={`${ADR}001D-each-kind-of-truth-has-one-home.md`}>ADR-001D</Source>
        </p>
        <dl className={styles.records}>
          <dt>Blueprint</dt>
          <dd>
            Where the system is going: what it is, who it serves, the outcomes it promises and what it will not do.
            <Source path="BLUEPRINT.md">BLUEPRINT.md</Source>
          </dd>
          <dt>Spec</dt>
          <dd>
            One named change in what the system can do. It holds the intent and who authorized it, the behavior wanted,
            and acceptance conditions, each with the check that proves it and a fault the check must catch, followed by
            an append-only log of evidence. Small edits need no Spec.
            <Source path={`${ADR}000P-a-capability-change-gets-one-short-spec.md`}>ADR-000P</Source>
            <Source path={`${S003}SPEC.md`}>S-003, for the shape</Source>
          </dd>
          <dt>Task</dt>
          <dd>
            One slice of a Spec for one agent run, in its own file: the assignment, acceptance, status, who claimed it,
            and a receipt with the proof. It must be runnable from a clean copy of the repository using only the Task,
            its Spec and the files it cites. Further work becomes a new Task.
            <Source path={`${ADR}000Q-each-task-is-its-own-runnable-file.md`}>ADR-000Q</Source>
            <Source path={`${ADR}000R-a-task-is-one-agent-run.md`}>ADR-000R</Source>
          </dd>
          <dt>Decision records</dt>
          <dd>
            One short file per decision: what was decided, what was considered and rejected, the consequences, and
            where the decision came from.
            <Source path={`${ADR}000C-the-authority-order-for-agents.md`}>an example, ADR-000C</Source>
          </dd>
          <dt>Glossary</dt>
          <dd>
            The shared words and what each one means.
            <Source path="GLOSSARY.md">GLOSSARY.md</Source>
          </dd>
          <dt>Taskboard</dt>
          <dd>
            A generated view of active work, rendered from the Specs and Tasks. It displays state; it never sets it.
            <Source path="TASKBOARD.md">TASKBOARD.md</Source>
            <Source path="ARCHITECTURE.md">Architecture, Invariants</Source>
          </dd>
        </dl>
      </section>

      <section className={styles.section} aria-labelledby="lifecycle">
        <h2 id="lifecycle">The life of a piece of work</h2>
        <p>
          <Link href="/start#flow">Start here</Link> shows the path from a request to done, with who holds the work at
          each stage, as a diagram and a toy. These are the rules behind its last steps.
        </p>
        <ol className={styles.list}>
          <li>
            <strong>Merge.</strong> A pull request merges only after it is brought up to date with its target branch and
            passes checks on that combined commit. Site work targets <code>dev</code>.
            <Source path={`${ADR}001K-a-pr-merges-only-after-checks-on-the-combined-commit.md`}>ADR-001K</Source>
          </li>
          <li>
            <strong>Close.</strong> Done requires the result commit to be pushed and read back from the remote branch.
            The Task&apos;s receipt records the commit, the tests and what remains open.
            <Source path={`${ADR}001H-done-requires-a-pushed-read-back-commit.md`}>ADR-001H</Source>
          </li>
          <li>
            <strong>Accept.</strong> A Spec is accepted only against its stated conditions and the delivered result,
            after a fresh-context reviewer passes the exact commit. Every Task being done is a coordination check, not
            acceptance.
            <Source path={`${ADR}000S-a-spec-is-accepted-against-its-conditions.md`}>ADR-000S</Source>
            <Source path={`${ADR}001E-a-spec-needs-fresh-context-review-of-the-exact-commit.md`}>ADR-001E</Source>
          </li>
          <li>
            <strong>Clean up.</strong> Specs and Tasks are scaffolding. At close, lasting knowledge moves to its owner
            and the scaffolding is deleted in the same change.
            <Source path={`${ADR}000T-scaffolding-is-deleted-at-close.md`}>ADR-000T</Source>
          </li>
        </ol>
        <p>
          A Spec&apos;s status is one of planned, active, blocked, needs-review, complete or superseded. A Task&apos;s
          is one of ready, in-progress, blocked, needs-review, done or deferred.
          <Source path="workbench/tools/spec-workbench.mjs">spec-workbench.mjs</Source>
          <Source path="workbench/tools/task-record.mjs">task-record.mjs</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="example">
        <h2 id="example">One real Spec and one real Task</h2>
        <p>
          <strong>
            Spec <a href={`${REPO_BLOB}${S003}SPEC.md`}>S-003, Showcase site shell and orientation tour</a>
          </strong>{" "}
          is the Spec for this site. It is active, at priority 1, owned by Kayden with orchestrator A. It sets eleven
          acceptance conditions, from every tour page having a plain-language opener to a quickstart that replays on a
          fresh copy of the repository, and it plans seven Tasks, TK-001 to TK-007. None of its conditions is checked
          off yet.
        </p>
        <p>
          <strong>
            Task <a href={`${REPO_BLOB}${S003}tasks/TK-001/TASK.md`}>TK-001</a>
          </strong>{" "}
          built the shell every page uses: the navigation, light and dark themes, the commit shown in the footer and a
          home page rendered on the server. Its status is done. Its receipt records the tests written first and
          failing 10 of 14, then 14 of 14 passing from a fresh copy; pull request #13 merged into <code>dev</code> as
          commit c529821; a browser check at 375 pixels wide in both themes passing 15 of 15; and a Codex code and
          security review with no findings. It also records what it could not check: the footer of the live{" "}
          <code>dev</code> deployment was not fetched, because the connector refused, so that stays open.
        </p>
        <p>
          This page is itself the work of{" "}
          <a href={`${REPO_BLOB}${S003}tasks/TK-002/TASK.md`}>Task TK-002</a>. Task files are scaffolding and are deleted
          when their Spec closes, so these links will change; the site&apos;s tests fail on a link to a file that no
          longer exists.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="guarantees">
        <h2 id="guarantees">Guarantees and limits</h2>
        <p>
          Code checks structure; agents carry judgment. A rule counts as enforced only when running code refuses the
          operation and a test shows the refusal, so the steps above are decided rules, and this page does not claim
          which of them code enforces today.
          <Source path={`${ADR}000G-a-rule-is-enforced-only-when-code-refuses-and-a-test-shows-it.md`}>ADR-000G</Source>
        </p>
        <ul className={styles.list}>
          <li>
            Review and owner checks of the experience are recorded only when they actually happen on identified
            content; an agent cannot supply the owner&apos;s judgment.
            <Source path="ARCHITECTURE.md">Architecture, Invariants</Source>
            <Source path="GLOSSARY.md">Glossary, Human QA receipt</Source>
          </li>
          <li>
            The AMS runtime software does not exist yet.
            <Source path="ARCHITECTURE.md">Architecture, Bird&apos;s-eye view</Source>
          </li>
          <li>
            No improvement has been measured yet; the <Link href="/rsi">RSI results</Link> page, next in the reading
            order, shows where results will appear.
          </li>
        </ul>
      </section>
    </div>
  );
}
