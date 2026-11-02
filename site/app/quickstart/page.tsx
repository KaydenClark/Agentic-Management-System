// /quickstart: Quickstart, a tour page (S-003 TK-003). The shortest useful
// start on a fresh clone: the commands and their output come from
// quickstart.mjs, which tests/quickstart-replay.test.mjs replays on a fresh
// clone and compares, so the page shows only what the commands print.
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Source } from "../tour/Source";
import styles from "../tour/tour.module.css";
import { steps } from "./quickstart.mjs";

export const metadata: Metadata = {
  title: "Quickstart | Agentic Management System",
  description: "Copy the Agentic Management System to your computer and run its health check, with the output you should see.",
};

// What each step does, in plain words, by step id.
const SAY: Record<string, ReactNode> = {
  clone: (
    <>
      Copy the project from GitHub to your computer. Git prints its progress while it copies; that varies with your
      connection, so it is not shown here.
    </>
  ),
  cd: <>Move into the copy. This prints nothing.</>,
  doctor: (
    <>
      Run the health check. It reads the project&apos;s records and settings, and how your computer is set up to
      work on them, and reports anything wrong. On any computer but the owner&apos;s, you should see exactly this:
    </>
  ),
};

export default function Quickstart() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>Quickstart</h1>
        <p className="lede" data-opener="">
          The quickest way to see the Agentic Management System, or <dfn id="ams">AMS</dfn>, for yourself is to copy
          it to your own computer and run its health check. That takes three commands typed into a terminal, the
          text window where you give your computer commands. Nothing is installed, nothing is changed outside the
          copy, and the check only reports. On your computer it reports one problem that blocks work until it is
          repaired; this page shows it and explains why.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="need">
        <h2 id="need">What you need</h2>
        <p>
          Git, to copy the project, and Node.js 20 or later, to run the check. There is no application to install
          yet: the AMS today is its records and the tools that check them.
          <Source path="README.md">README, Getting Started</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="steps">
        <h2 id="steps">Three commands</h2>
        <ol className={styles.steps}>
          {steps.map((step) => (
            <li key={step.id}>
              <p>{SAY[step.id]}</p>
              <pre className={styles.terminal}>
                <span className={styles.prompt} aria-hidden="true">
                  ${" "}
                </span>
                <code data-command={step.id}>{step.command}</code>
              </pre>
              {step.output !== null ? (
                <pre className={styles.terminal} data-output={step.id}>
                  {step.output}
                </pre>
              ) : null}
              {step.exitCode ? (
                <p data-exit={step.id}>
                  It then stops with exit status {step.exitCode}. Your terminal does not usually print this, but any
                  status other than 0 means the command found something wrong.
                </p>
              ) : null}
            </li>
          ))}
        </ol>
        <p>
          The site&apos;s tests run these same commands on a fresh copy of the version you are reading and fail if
          the output or the exit status differs from what is shown here. They run them as a reader&apos;s computer
          would, with an empty home folder, so the result does not depend on whose computer runs the test.
          <Source path="site/tests/quickstart-replay.test.mjs">the replay test</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="read">
        <h2 id="read">Reading the result</h2>
        <p>
          Each indented line is a finding: a short name, how much it blocks, how serious it is, and what to do about
          it. The findings come in groups, each headed by a count: first those that block work, then those that are
          reported only. A healthy copy shows no blocking group, ends with a line starting with ok, and exits with
          status 0.
          <Source path="README.md">README, Getting Started</Source>
          <Source path="AGENTS.md">AGENTS.md, Testing instructions</Source>
        </p>
        <p>
          Your copy is not healthy yet, and that is not a fault in it. The one blocking finding,
          personal-catalog-unavailable, is marked blocks all: the check says to repair it before any work is picked
          up or claimed. Below it, each skill-lane-missing line names one skill the tools looked for and did
          not find. A skill is a written method an agent loads before doing a kind of work; the{" "}
          <Link href="/skills">Skills</Link> page describes them. The tools expect the owner&apos;s own skills
          installed in the home folder of the computer that runs them, and the project deliberately keeps them out
          of the repository, so the check reports this on a fresh copy anywhere else today.
          <Source path="workbench/tools/personal-skills.mjs">the skills check</Source>
          <Source path="workbench/manifest.json">the manifest, skillPolicy</Source>
        </p>
        <p>
          What you can do with the copy now is read it: every record, decision and check the site describes is in
          it. The other findings shown are real and open as well. They block nothing, and the check keeps them
          visible rather than hiding them, so that nothing reported is quietly forgotten.
        </p>
      </section>

      <section className={styles.section} aria-labelledby="next">
        <h2 id="next">Where to go next</h2>
        <p>
          The copy holds everything the site describes. Start with the README for the map of the project, then the
          Runbook, the operating manual, for the other checks and how work is run.
          <Source path="README.md">README</Source>
          <Source path="RUNBOOK.md">RUNBOOK</Source>
        </p>
        <p>
          If a word in the records is new to you, the <Link href="/glossary">Glossary</Link> has it, exactly as the
          project defines it. The <Link href="/rsi">RSI results</Link> page, next, shows where measured results will
          appear.
        </p>
      </section>
    </div>
  );
}
