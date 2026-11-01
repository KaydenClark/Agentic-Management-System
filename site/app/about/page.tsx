// /about: About, the last tour page (S-003 TK-003). About the AMS project:
// what this repository holds, its license, where it stands and how this site
// was built with the AMS. Not a biography. Every claim links the committed
// record it comes from; tests/about.test.mjs keeps the license line true to
// the LICENSE file.
import type { Metadata } from "next";
import Link from "next/link";
import { REPO_BLOB, Source } from "../tour/Source";
import styles from "../tour/tour.module.css";

export const metadata: Metadata = {
  title: "About | Agentic Management System",
  description: "What the Agentic Management System repository holds, its license, where it stands and how this site was built with it.",
};

const ADR = "workbench/docs/adr/";
const DDR = "workbench/docs/ddr/";
const S003 = "workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md";

const FOLDERS: { path: string; holds: string }[] = [
  { path: "workbench/", holds: "the records: plans, decisions, the wiki, feedback and the tools that check them" },
  { path: "site/", holds: "this website" },
  { path: "grill-board/", holds: "the owner's question-and-answer board, which runs only on the owner's own computer" },
  { path: "evals/", holds: "the improvement trials and their measured results" },
  { path: "src/ and tests/", holds: "the AMS software and its tests" },
  { path: "supabase/", holds: "the database changes behind the data the site reads" },
];

export default function About() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>About</h1>
        <p className="lede" data-opener="">
          This site and the Agentic Management System, or <dfn id="ams">AMS</dfn>, live in one public{" "}
          <dfn id="repository">repository</dfn>, a folder of files with its full history kept on GitHub. This page
          says what that folder holds, who may reuse it, how far along it is, and how this site was built with the
          system it describes.
        </p>
      </header>

      <section className={styles.section} aria-labelledby="holds">
        <h2 id="holds">What the repository holds</h2>
        <p>
          The records and tools that run the work, the website, and places for the parts still being built. The
          README is the map.
          <Source path="README.md">README, Project Folders</Source>
        </p>
        <dl className={styles.terms}>
          {FOLDERS.map((f) => (
            <div key={f.path}>
              <dt>
                <code>{f.path}</code>
              </dt>
              <dd>{f.holds}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className={styles.section} aria-labelledby="license">
        <h2 id="license">License</h2>
        <p>
          The decision is MIT, copyright Kayden Clark, so anyone who reuses the work must keep the credit. Applying
          the license text is the owner&apos;s step, and the LICENSE file is still empty, so the files themselves
          do not yet grant that license.
          <Source path={`${DDR}000R-the-license-is-mit-copyright-kayden-clark.md`}>DDR-000R</Source>
          <Source path="LICENSE">LICENSE</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="status">
        <h2 id="status">Where it stands</h2>
        <p>
          The architecture record marks itself partial. The Taskboard lists the work in progress, and the first Spec,
          S-001, is the yardstick for whether the system has arrived.
          <Source path="ARCHITECTURE.md">Architecture</Source>
          <Source path="TASKBOARD.md">Taskboard</Source>
          <Source path="workbench/specs/S-001-ams/SPEC.md">S-001</Source>
        </p>
      </section>

      <section className={styles.section} aria-labelledby="built">
        <h2 id="built">How this site was built</h2>
        <p>
          With the AMS itself, as its first trial: the build is the first round of the improvement loop, recorded
          from the start.
          <Source path={`${DDR}000W-the-first-rsi-trial-is-building-the-site.md`}>DDR-000W</Source>
        </p>
        <ul className={styles.list}>
          <li>
            The site is one Spec, <a href={`${REPO_BLOB}${S003}`}>S-003</a>, with its acceptance conditions and an
            evidence log of every finished Task.
            <Source path={S003}>S-003</Source>
          </li>
          <li>
            Agents build it. The website belongs to orchestrator A, an agent that coordinates the website work; two
            other orchestrators hold the local board with the improvement data, and the consistency checks, so no one agent holds every risk.
            <Source path={`${ADR}002Z-three-orchestrators-split-the-work-by-risk.md`}>ADR-002Z</Source>
          </li>
          <li>
            Each change goes from its own branch into <code>dev</code> after the <code>site builds</code> check
            passes: install, build and every test, the quickstart replay included. Only Kayden moves{" "}
            <code>dev</code> into <code>main</code>, the public version.
            <Source path={`${ADR}003I-only-main-dev-and-site-branches-deploy-to-vercel.md`}>ADR-003I</Source>
            <Source path="AGENTS.md">AGENTS.md, PR instructions</Source>
          </li>
          <li>
            The footer of every page names the commit it was built from and links it on GitHub.
            <Source path={S003}>S-003, Shell</Source>
          </li>
        </ul>
        <p>
          The words of this page, like every page, are drafted by agents from those records.
          <Source path={S003}>S-003, Voice</Source> Back to the{" "}
          <Link href="/">home page</Link>, or <Link href="/start">start the tour</Link> again.
        </p>
      </section>
    </div>
  );
}
