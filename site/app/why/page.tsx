// /why: Why, a tour page (S-003 TK-003). Why the AMS exists, what it
// promises, why its first work is this site, and why it treats its own value
// as unproven. Every claim links the committed record it comes from; the one
// owner quote is verbatim with its dated source.
import type { Metadata } from "next";
import Link from "next/link";
import { REPO_BLOB, Source } from "../tour/Source";
import styles from "../tour/tour.module.css";

export const metadata: Metadata = {
  title: "Why | Agentic Management System",
  description: "Why the Agentic Management System exists, what it promises and why it counts nothing as proven without evidence.",
};

const ADR = "workbench/docs/adr/";
const DDR = "workbench/docs/ddr/";
const PURPOSE = "workbench/wiki/context-ams-purpose.md";

export default function Why() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>Why</h1>
        <p className="lede" data-opener="">
          Kayden works with many <dfn id="agent">agents</dfn>, AI assistants that carry out work on their own, and
          with the instructions, habits and tools that go with them. The Agentic Management System, or{" "}
          <dfn id="ams">AMS</dfn>, exists to keep all of that in one place, to keep what he meant attached to the
          work, and to learn from each round of work which changes actually help. This page says why it was built
          and why it treats its own value as unproven until the numbers say otherwise.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="words">
        <h2 id="words">In Kayden&apos;s words</h2>
        <figure className={styles.quote} data-owner-quote="">
          <blockquote>
            <p>my full tool belt I use to work with AI wrapped up into one RSI loop that builds a website explaining itself.</p>
          </blockquote>
          <figcaption>
            Kayden, 2026-10-31, describing the AMS. Recorded in{" "}
            <a href={`${REPO_BLOB}${PURPOSE}`}>AMS purpose and first RSI loop</a>.
          </figcaption>
        </figure>
        <p>
          The same record adds his reason: the work repairs the broken Workbench, the working foundation underneath,
          and creates the system on top of it that runs it. In this repository the Workbench is the controls,
          lifecycle tools and templates agents work with.
          <Source path={PURPOSE}>AMS purpose</Source>
          <Source path="README.md">README</Source>
        </p>
        <p>
          RSI stands for recursive self-improvement. Here it means improving through actual work: notice where work
          goes wrong, try one bounded change, compare the results and decide what to keep.
          <Source path="GLOSSARY.md">Glossary, RSI loop</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="promises">
        <h2 id="promises">What it promises</h2>
        <p>
          The Blueprint, the short page that says where the system is going, lists five outcomes. They are the
          intent, not a claim that each one works today.
          <Source path="BLUEPRINT.md">Blueprint, Promised outcomes</Source>
        </p>
        <ul className={styles.list}>
          <li>Keep what was asked, the reasons and every correction attached from the request to the result.</li>
          <li>Connect agents, workflows, skills and tools with a clear owner for each and the context each needs.</li>
          <li>Repair the Workbench where it has been shown to fail, while building useful abilities on top of it.</li>
          <li>Learn from real work: note the friction, test small improvements, compare and carry forward what holds.</li>
          <li>Explain itself through a website whose claims link to evidence and whose demonstrations show the behavior.</li>
        </ul>
        <p>
          It serves three readers: Kayden, who directs the work and needs to understand it; the agents, which need
          clear intent, a scoped assignment, the methods to use and evidence they can find again; and visitors to
          this site, who need an honest account that separates what is intended from what is shown to work.
          <Source path="BLUEPRINT.md">Blueprint, Who it serves</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="site">
        <h2 id="site">Why its first job is this website</h2>
        <p>
          A system that claims to manage work needs real work to be tested on. The first round of the loop builds
          this site, so building it supplies the friction to find, the improvements to try and the results to
          explain.
          <Source path="BLUEPRINT.md">Blueprint, What it is</Source>
        </p>
        <p>
          The first trial is the whole build. Each build run is recorded as data from the start, and after the build
          the loop keeps running on the improvements that follow. A separate, made-up first trial was considered and
          rejected.
          <Source path={`${DDR}000W-the-first-rsi-trial-is-building-the-site.md`}>DDR-000W</Source>
        </p>
        <p>
          The site itself only presents. It runs no agents, edits no records and only reads the data it shows.
          <Source path={`${DDR}000O-the-public-site-only-presents-and-reads-supabase.md`}>DDR-000O</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="bet">
        <h2 id="bet">Why it calls itself a bet</h2>
        <p>
          The AMS changes only the software around a model, its instructions and its skills, never the model itself.
          Its premise, that working inside it beats working without it, is recorded as a hypothesis to test, not a
          settled fact. It will be compared with two controls, no AMS and generic instructions, on tasks held back
          from the work it was tuned on, and the site reports the result either way.
          <Source path={`${DDR}000C-the-ams-changes-runtime-controls-and-skills-never-weights.md`}>DDR-000C</Source>
        </p>
        <p>
          Until that evidence exists, no page claims the AMS improves outcomes. A static score, a shorter prompt or
          one successful demo does not count.
          <Source path={`${ADR}000A-improvement-claims-need-held-out-ledger-evidence.md`}>ADR-000A</Source> Charts
          start empty rather than show invented numbers.
          <Source path={`${DDR}000T-charts-start-blank-and-data-is-never-fabricated.md`}>DDR-000T</Source>
        </p>
        <p>
          Next, <Link href="/how-it-works">How it works</Link> shows the records that carry the work.
        </p>
      </section>
    </div>
  );
}
