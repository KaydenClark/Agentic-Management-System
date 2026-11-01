// /start: Start here, the first tour page (S-003 TK-002). What the AMS is and
// what it refuses to do. Every claim links the committed record it comes
// from; the owner is quoted only verbatim, with the dated record.
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Start here | Agentic Management System",
  description: "What the Agentic Management System is, who it serves and what it refuses to do.",
};

const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";

// A link to the committed record a claim comes from.
function Source({ path, children }: { path: string; children: ReactNode }) {
  return (
    <span className={styles.source}>
      {" "}
      Source: <a href={`${REPO_BLOB}${path}`}>{children}</a>.
    </span>
  );
}

const ADR = "workbench/docs/adr/";

export default function StartHere() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>Start here</h1>
        <p className="lede" data-opener="">
          The Agentic Management System, or <dfn id="ams">AMS</dfn>, is the way Kayden works with{" "}
          <dfn id="agent">agents</dfn>: AI assistants that can carry out a piece of work on their own. Every job starts
          as a written request, is cut into small steps, and counts as finished only when there is proof that it works.
          The AMS is just as clear about what it will not do: an agent does not delete work, spend money, send messages
          for anyone or publish private material unless it has first been told it may.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="what-it-is">
        <h2 id="what-it-is">What the AMS is</h2>
        <p>
          The AMS brings together everything Kayden uses to work with AI: the agents, the workflows they follow, the way
          his intent (what he wants, with his reasons and corrections) is written down, the skills agents use and the
          other tools, all in one improvement loop.
          <Source path="BLUEPRINT.md">Blueprint</Source>
        </p>
        <figure className={styles.quote} data-owner-quote="">
          <blockquote>
            <p>my full tool belt I use to work with AI wrapped up into one RSI loop that builds a website explaining itself.</p>
          </blockquote>
          <figcaption>
            Kayden, describing the AMS on 2026-10-31, as recorded in{" "}
            <a href={`${REPO_BLOB}workbench/wiki/context-ams-purpose.md`}>AMS purpose and first RSI loop</a>.
          </figcaption>
        </figure>
        <p>
          <dfn id="rsi">RSI</dfn> stands for recursive self-improvement through actual work: notice where work goes
          wrong, propose one bounded change, compare the outcomes, decide what to keep, and look again at later use. A
          record of the loop is not, by itself, proof that anything improved.
          <Source path="GLOSSARY.md">Glossary</Source>
        </p>
        <p>
          The first round of the loop builds this website. Building it gives the system real work in which to find
          problems, test improvements and explain what the results support.
          <Source path="BLUEPRINT.md">Blueprint</Source> Underneath sits the <dfn id="workbench">Workbench</dfn>, the
          working foundation of records and tools the AMS uses and repairs as it goes.
          <Source path="GLOSSARY.md">Glossary</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="who">
        <h2 id="who">Who it serves</h2>
        <ul className={styles.list}>
          <li>Kayden, who uses it to direct work done with AI and to understand that work.</li>
          <li>Agents, who need clear intent, a scoped assignment, methods they can use and evidence they can find again.</li>
          <li>
            Visitors to this site, who need an understandable account of the system that keeps what is planned apart from
            what has been shown to work.
          </li>
        </ul>
        <p>
          <Source path="BLUEPRINT.md">Blueprint, Who it serves</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="refuses">
        <h2 id="refuses">What it refuses to do</h2>
        <p>These limits are written into the records agents work from. Each one links the record that sets it.</p>
        <ul className={styles.list} data-refusals="">
          <li>
            <strong>Go beyond what was asked.</strong> An agent asks first before anything destructive, any paid
            service, any real widening of the job, or any outside change nobody requested.
            <Source path="AGENTS.md">AGENTS.md, Boundaries and delivery</Source>
          </li>
          <li>
            <strong>Leak.</strong> Secrets are never committed, and private research or traces are not published without
            the right authorization. This repository is public.
            <Source path="AGENTS.md">AGENTS.md, Boundaries and delivery</Source>
          </li>
          <li>
            <strong>Speak for anyone.</strong> No agent sends messages to other people without explicit authorization.
            <Source path="AGENTS.md">AGENTS.md, Boundaries and delivery</Source>
          </li>
          <li>
            <strong>Mistake appearances for proof.</strong> A template, a dashboard, a screenshot or a passing
            structural check is not proof that the system works reliably.
            <Source path="BLUEPRINT.md">Blueprint, Non-goals</Source>
          </li>
          <li>
            <strong>Call a rule enforced because it is written down.</strong> A rule counts as enforced only when running
            code refuses the forbidden step and a test shows the refusal.
            <Source path={`${ADR}000G-a-rule-is-enforced-only-when-code-refuses-and-a-test-shows-it.md`}>ADR-000G</Source>
          </li>
          <li>
            <strong>Hold every risk at once.</strong> An autonomous session holds at most two of these three: input it
            cannot trust, private data or credentials, and the power to act in the outside world.
            <Source path={`${ADR}002P-no-session-holds-untrusted-input-secrets-and-outward-actions-together.md`}>
              ADR-002P
            </Source>
          </li>
          <li>
            <strong>Retry until something passes.</strong> A failing step is tried at most three times; then the agent
            stops and reports.
            <Source path={`${ADR}002W-three-strikes-then-stop.md`}>ADR-002W</Source>
          </li>
          <li>
            <strong>Publish the site on its own.</strong> Agents merge site changes into a working copy called{" "}
            <code>dev</code>; only Kayden moves them on into <code>main</code>.
            <Source path="RUNBOOK.md">Runbook, Version control and publication</Source>
          </li>
          <li>
            <strong>Run anything from this site.</strong> This site only presents: it runs no agents and edits no
            records.
            <Source path="workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md">
              S-003, Decisions and contracts
            </Source>
          </li>
        </ul>
      </section>

      <section className={styles.section} aria-labelledby="technical">
        <h2 id="technical">For a technical reader</h2>
        <p>
          <strong>Authority order.</strong> Platform safety and host permissions bound everything. Inside them the
          owner&apos;s current request governs, then <code>AGENTS.md</code>, then the assigned{" "}
          <Link href="/how-it-works#spec">Spec</Link> or <Link href="/how-it-works#task">Task</Link>. Everything
          else an agent reads is evidence, not instruction.
          <Source path={`${ADR}000C-the-authority-order-for-agents.md`}>ADR-000C</Source>
        </p>
        <p>
          <strong>One home per truth.</strong> The Blueprint owns the destination, a Spec owns requirements, acceptance
          and evidence, a Task owns execution state and proof, decision records own decisions with their reasons, and
          the Glossary owns the words. The Taskboard is rendered from those records and never establishes state.
          <Source path="ARCHITECTURE.md">Architecture, Ownership</Source> How it works, the next page, walks through
          these records.
        </p>
        <p>
          <strong>Work split by risk.</strong> Three orchestrators, all Claude, divide the work. A builds this site and
          deploys only by pushing to <code>dev</code>, with no web browsing. B runs the local Grill Board, the Python
          backend and the Supabase keys on the owner&apos;s own machine, and never deploys. C checks that the project
          stays true to its Specs, reviews Specs independently and does web research, holding no secrets and writing no
          product code.
          <Source path={`${ADR}002Z-three-orchestrators-split-the-work-by-risk.md`}>ADR-002Z</Source>
        </p>
        <p>
          <strong>Committed or it did not happen.</strong> A stop hook for Claude Code and Codex blocks the end of a turn
          once while there is uncommitted work, with instructions to commit it; if the agent still cannot, it may stop
          and the owner sees a warning.
          <Source path=".agents/hooks/require-committed.sh">require-committed.sh</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="today">
        <h2 id="today">Where it stands today</h2>
        <ul className={styles.list}>
          <li>
            The AMS runtime software does not exist yet; today the system is its records, tools and the agents working
            from them.
            <Source path="ARCHITECTURE.md">Architecture, Bird&apos;s-eye view</Source>
          </li>
          <li>
            The RSI loop has recorded no trials, so the <Link href="/rsi">RSI results</Link> page is empty on purpose.
          </li>
          <li>
            None of the acceptance conditions of this site&apos;s own Spec, S-003, is checked off yet, and every page
            stays a draft until Kayden approves it.
            <Source path="workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md">S-003</Source>
          </li>
        </ul>
      </section>
    </div>
  );
}
