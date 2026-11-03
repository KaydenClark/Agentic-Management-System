// /how-it-works: How it works, the second tour page (S-003 TK-002). The
// records, the lifecycle, and one real Spec and Task linked to their files on
// GitHub. Every claim links the committed record it comes from.
import type { Metadata } from "next";
import Link from "next/link";
import { Signal } from "../components/Signal";
import type { ReactNode } from "react";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "How it works | Agentic Management System",
  description: "The records the AMS keeps, the life of a piece of work, and one real Spec and Task from this site.",
};

const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";
const ADR = "workbench/docs/adr/";
// This revision contains the Spec and receipts described in the historical example.
const EXAMPLE_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/ce39c6a89f92dffaebecb468b367c49ab6577bd8/";
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
          In the Agentic Management System, or <dfn id="ams">AMS</dfn>, a request becomes written work before
          it is carried out. A <dfn id="spec">Spec</dfn> is a bounded destination with conditions for judging it;
          <dfn id="task"> <Link href="/glossary#implementation-task">Tasks</Link></dfn> plan and carry out execution through bounded assignments. AI assistants, called
          <dfn id="agent"> agents</dfn>, implement and check those assignments, then return the result with evidence.
          This page follows that path and distinguishes automated checks from human decisions.
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
          <dt>Landmark</dt>
          <dd>A larger direction that connects related Specs. The route is intent, Landmark, Spec, then Task;
            the Task carries a bounded piece of the destination into implementation and verification.</dd>
          <dt>Spec</dt>
          <dd>
            One named change in what the system can do. It holds the intent and who authorized it, the behavior wanted,
            and acceptance conditions, each with the check that proves it and a fault the check must catch. It describes
            the destination only; how the work got there is kept in its Wiki history page. Small edits need no Spec.
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
        <h2 id="lifecycle">From intent to a checked result</h2>
        <ol className={styles.list}>
          <li><strong>Agree on the destination.</strong> The owner explains what is wanted, why and within which
            boundaries. Questions and corrections change the written understanding before dependent work continues.</li>
          <li><strong>Assign one bounded piece.</strong> A Task names the result, its inputs and checks. One agent
            claims it so another worker does not change the same thing at the same time.</li>
          <li><strong>Implement, Check, QA and Submit.</strong> The agent changes the product, runs relevant checks,
            exercises the intended experience and returns a committed result with evidence and remaining gaps.</li>
          <li><strong>Judge and deliver the assembled result.</strong> An independent review examines the named
            candidate against its destination. Human QA records the owner’s actual experience. A checked merge
            does not by itself supply either judgment. Site changes go to dev; only the owner promotes dev to main.</li>
        </ol>
        <p>
          Feedback goes back to the record and person responsible for it. A failed comparison can motivate a
          bounded improvement to the method, followed by another comparison and a decision about what to keep.
          <Link href="/rsi"> RSI results</Link> keeps observed outcomes separate from claims of useful improvement.
          <Link href="/start#try"> Try the handoff toy</Link> to explore this path without changing real work.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="example">
        <h2 id="example">One real Spec and one real Task</h2>
        <p>
          <strong>
            Spec <a href={`${EXAMPLE_BLOB}${S003}SPEC.md`}>S-003</a>
          </strong>{" "}
          describes this site&apos;s shell and orientation tour at the recorded revision ce39c6a. At that point it is active, at priority 1, owned by Kayden with
          orchestrator A. Its acceptance conditions run from every page opening in plain language to the commit shown
          in each footer matching the deployment, and its work is split into seven Tasks, TK-001 to TK-007. None of
          its conditions is checked off yet.
        </p>
        <p>
          <strong>
            Task <a href={`${EXAMPLE_BLOB}${S003}tasks/TK-001/TASK.md`}>TK-001</a>
          </strong>{" "}
          built the shell every page uses: the navigation, light and dark themes, the commit shown in the footer and a
          home page rendered on the server. Its status is done. Its receipt records the tests written first and
          failing 10 of 14, then 14 of 14 passing from a fresh copy; pull request #13 merged into <code>dev</code> as
          commit c529821; a browser check at 375 pixels wide in both themes passing 15 of 15; and a Codex code and
          security review with no findings. It also records what it could not check: the footer of the live{" "}
          <code>dev</code> deployment was not fetched, because the Vercel connector, the tool agents use to reach the web
          host, refused the request, so that check stays open.
        </p>
        <p>
          The original explanation on this page was delivered by{" "}
          <a href={`${EXAMPLE_BLOB}${S003}tasks/TK-002/TASK.md`}>Task TK-002</a>. These are historical receipts, not the current state of every website Task. The example links keep their
          original revision, so later record moves or changes do not rewrite the evidence behind this account.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="governance">
        <h2 id="governance">Who may decide, and what counts as proof?</h2>
        <p>
          The owner’s request sets the purpose and scope. Project rules constrain permitted actions; the Spec
          states the outcome to judge, and the Task assigns a piece of work. A status view displays those records
          without granting permission. Together these boundaries keep an agent’s plan from becoming authority
          merely because it was written down.
        </p>
        <p>
          Tests give evidence about the behavior they exercised. An independent review challenges a named
          candidate; Human QA records a person’s actual judgment of the experience. Neither an agent’s
          self-check nor a green test is owner approval. Publishing a branch, merging into dev and promoting a
          site to production are separate actions, each with its own authority.
        </p>
        <p>
          The same distinction matters in learning: a recorded failure is an input, a proposed repair is a
          hypothesis, and a later comparison is evidence to assess. A repair or score alone proves no benefit.
          <Link href="/start#refuses"> Limits</Link> and <Link href="/rsi">RSI results</Link> explain what visitors
          can and cannot infer from what this website presents.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="grill-board">
        <h2 id="grill-board">The Grill Board brings questions to the owner</h2>
        <Signal kind="worth" label="Why the answer matters">
          <p>
            The Grill Board is the owner’s local place to answer choices that genuinely need human input. The
            questions should make sense without knowing the project’s code. For example, planning a picnic might
            need a date, the number of guests, a food budget and dietary needs. Those answers shape the work;
            asking a person to decipher an internal file path does not resolve the underlying choice.
          </p>
        </Signal>
        <p>
          In this project, answers and page-review judgments belong to the relevant work and identified content.
          A displayed card is not an answer or approval. The local board is separate from this presentation
          website: this section explains its role.
        </p>
        <Signal kind="returned" label="Returned for correction">
          <p>
            The <Link href="/start#try">handoff toy</Link> illustrates how work can return for correction.
            It does not submit questions or change the owner’s records.
          </p>
        </Signal>
      </section>

      <section className={styles.section} aria-labelledby="guarantees">
        <h2 id="guarantees">What the checks do and do not establish</h2>
        <p>
          A rule counts as enforced only when running code refuses the operation and a test demonstrates that
          refusal. Writing a rule or citing an existing file is not evidence that its intended behavior works.
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
            The Workbench Node lifecycle and Python command-line tools are working components. The assembled RSI loop has not been demonstrated as a runtime system.
            <Source path="ARCHITECTURE.md">Architecture</Source>
            <Source path="workbench/tools/spec-workbench.mjs">Workbench Node lifecycle</Source>
            <Source path="src/ams/trials.py">Python command-line tools</Source>
          </li>
          <li>
            The <Link href="/rsi">RSI results</Link> page shows shared-skill repair evidence and recorded trial
            results. Checks, failures and incomplete trials do not establish demonstrated improvement.
          </li>
        </ul>
      </section>
    </div>
  );
}
