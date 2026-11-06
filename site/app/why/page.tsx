import type { Metadata } from "next";
import Link from "next/link";
import { Source } from "../tour/Source";
import styles from "../tour/tour.module.css";

export const metadata: Metadata = {
  title: "Why | Agentic Management System",
  description: "The problems AMS aims to address, its intended benefits and the evidence needed to show that it helps.",
};

export default function Why() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <h1>Why</h1>
        <p className="lede" data-opener="">
          An AI can produce something plausible while losing what you meant. The Agentic Management System, or
          <dfn id="ams"> AMS</dfn>, aims to keep the purpose, boundaries and corrections attached to the work.
          This page explains the problem and the intended benefits, then asks what evidence would show that the
          methods actually help.
        </p>
      </header>
      <section className={styles.section} aria-labelledby="words">
        <h2 id="words">Keep the meaning through the handoffs</h2>
        <p>
          A request rarely contains everything that matters. Questions reveal missing detail; feedback corrects
          an interpretation; later work depends on those answers. If each new worker starts from an incomplete
          account, a technically correct result can still miss the purpose. Written understanding gives the
          people and agents a shared place to recover what was wanted and why.
        </p>
        <p>
          The intended benefit is less rediscovery and fewer corrections caused by lost context. Clear assignments
          and a single owner for each decision also help workers act independently without silently widening the
          job. These are reasons to try the methods, not measured promises about every project.
          <Source path="BLUEPRINT.md">Blueprint</Source>
          <Source path="workbench/wiki/context-ams-purpose.md">AMS purpose</Source>
        </p>
      </section>
      <section className={styles.section} aria-labelledby="promises">
        <h2 id="promises">Make the result answerable to the request</h2>
        <p>
          AMS connects an intended outcome to bounded assignments, checks and a record of what happened.
          Someone examining a result should be able to find its purpose, its limits, the evidence and the
          remaining decisions. A green test shows what that test exercised; it does not automatically establish
          that the whole experience is useful or approved.
        </p>
        <p>
          Reusable methods make that route available beyond this one project. The owner and agents can choose
          methods for the job, keep each worker’s scope clear, and bring unresolved human choices back to the
          person who can answer them. <Link href="/how-it-works">How it works</Link> follows the records and
          handoffs; <Link href="/start">About</Link> introduces the project and its people.
        </p>
      </section>
      <section className={styles.section} aria-labelledby="site">
        <h2 id="site">Use real work to find the weak points</h2>
        <p>
          This website is the project’s first outside product. Building a useful explanation creates real choices,
          mistakes and verification work. That friction gives the team concrete issues to investigate. The
          project adds recursive self-improvement, or RSI: observe a problem, propose a bounded change, compare
          outcomes, decide what to keep and examine later use.
        </p>
        <p>
          A shorter instruction file, a repaired checker or a completed change is an observation about the work.
          To show useful improvement, the evidence must support a comparison and explain its effect on outcomes.
          Failed attempts and regressions remain part of that account. Repeating an unsupported success claim
          does not turn it into a result.
          <Source path="GLOSSARY.md">Glossary, RSI loop</Source>
        </p>
      </section>
      <section className={styles.section} aria-labelledby="bet">
        <h2 id="bet">What would show that it helps?</h2>
        <p>
          The important question is whether the methods improve the work someone actually wants to do. That
          needs comparisons with a stated task, version, context and measure, including failures and uncertainty.
          Evidence about one candidate or a development check cannot establish an improvement in the whole
          system over time. Nor does one successful demonstration establish a general benefit.
        </p>
        <p>
          <Link href="/rsi">RSI results</Link> is where to examine the available evidence and its limits. Where
          useful benefit has not been demonstrated, it remains unknown. The site itself runs no agents or writes
          to project records; <Link href="/start#refuses">Limits</Link> explains that presentation boundary.
          <Source path="workbench/docs/adr/000A-improvement-claims-need-held-out-ledger-evidence.md">ADR-000A</Source>
        </p>
      </section>
    </div>
  );
}
