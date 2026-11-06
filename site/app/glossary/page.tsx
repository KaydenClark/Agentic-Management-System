// /glossary: Glossary, a tour page (S-003 TK-003). Rendered from
// glossary.json, which scripts/gen-glossary.mjs generates from GLOSSARY.md
// (npm run glossary:gen); tests/glossary.test.mjs fails if either drifts, so
// this page never words a term differently from the project's one home for
// its language.
import type { Metadata } from "next";
import type { SignalKind } from "../components/Signal";
import { Fragment, type ReactNode } from "react";
import { REPO_BLOB, Source } from "../tour/Source";
import styles from "./glossary.module.css";
import glossary from "./glossary.json";

export const metadata: Metadata = {
  title: "Glossary | Agentic Management System",
  description: "The shared words of the Agentic Management System, exactly as GLOSSARY.md defines them.",
};

// Markdown inline text from GLOSSARY.md: [links](path), **bold** and `code`.
// A relative link is a path from the repository root, shown on GitHub.
function Inline({ md }: { md: string }) {
  const parts: ReactNode[] = [];
  const re = /\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`/g;
  let last = 0;
  for (let m = re.exec(md); m; m = re.exec(md)) {
    if (m.index > last) parts.push(md.slice(last, m.index));
    if (m[1]) parts.push(<a key={m.index} href={/^https?:/.test(m[2]) ? m[2] : `${REPO_BLOB}${m[2]}`}>{m[1]}</a>);
    else if (m[3]) parts.push(<strong key={m.index}>{m[3]}</strong>);
    else parts.push(<code key={m.index}>{m[4]}</code>);
    last = re.lastIndex;
  }
  if (last < md.length) parts.push(md.slice(last));
  return <>{parts}</>;
}

const groups = glossary.sections.flatMap(section => section.groups);
const terms = groups.flatMap(group => group.terms);
const termById = new Map(terms.map(term => [term.id, term]));
const explainedTermIds = new Set([
  "ams", "intent", "workbench", "rsi-loop", "improvement-attempt",
  "alignment-assessment", "alignment-score", "fitness-level",
  "implementation-task", "evaluation-task", "review-receipt", "human-qa-receipt",
  "evidence-audit", "improvement-record", "diagnostic", "test", "repaired", "declined", "accepted-open",
]);
const explainedGroupIds = new Set(["group-ams", "group-records", "group-feedback-dispositions"]);
const governancePlaneIds = new Set(["projection", "intent", "enduring-context", "grounding", "canon", "actuality"]);
const additionalGroups = groups
  .map(group => ({ ...group, terms: group.terms.filter(term => !explainedTermIds.has(term.id)) }))
  .filter(group => group.terms.length > 0);

function Definitions({ ids }: { ids: string[] }) {
  return (
    <dl className={styles.definitions}>
      {ids.map(id => {
        const term = termById.get(id);
        if (!term) throw new Error(`Unknown glossary term: ${id}`);
        return (
          <div key={id}>
            <dt id={term.id}>{governancePlaneIds.has(id) ? <a href={`/governance#plane-${id}`}>{term.term}</a> : term.term}</dt>
            <dd><Inline md={term.definition} /></dd>
          </div>
        );
      })}
    </dl>
  );
}

function Arrow({ className }: { className: string }) {
  return <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><path d="M2 8h12m-5-5 5 5-5 5" /></svg>;
}

function Flow({ children, signals = [] }: { children: ReactNode[]; signals?: (SignalKind | undefined)[] }) {
  return (
    <ol className={styles.flow}>
      {children.map((child, index) => <li key={index} className={signals[index] ? `tone h-${signals[index]}` : undefined} data-signal={signals[index]}>{child}{index < children.length - 1 ? <Arrow className={styles.flowArrow} /> : null}</li>)}
    </ol>
  );
}

function ContextLink({ href, children }: { href: string; children: ReactNode }) {
  return <p className={styles.context}><a href={href}>{children}</a></p>;
}

export default function Glossary() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <h1>Glossary</h1>
        <p className="lede" data-opener="">
          Shared words help people and <dfn id="agent">agents</dfn>, AI assistants doing the work,
          carry <a href="#intent">intent</a> into outcomes through the Agentic Management System,
          or <a href="#ams">AMS</a>. Follow the connections, then read the exact definitions.
        </p>
        <nav aria-label="Glossary groups">
          <ul className={styles.index}>
            {groups.map(group => <li key={group.id}><a href={`#${group.id}`}>{group.heading}</a></li>)}
          </ul>
        </nav>
      </header>

      <section className={styles.section} aria-labelledby="group-ams">
        <h2 id="group-ams">From intent to outcomes</h2>
        <figure className={styles.diagram} aria-labelledby="intent-caption">
          <Flow signals={[undefined, undefined, "agent"]}>{[
            <strong key="people">People</strong>,
            <Fragment key="intent"><a href="#intent">Intent</a><span>Reasons · boundaries · corrections</span></Fragment>,
            <Fragment key="agents"><a href="#agent">Work with agents</a><span>Workflows · rules · skills · tools</span></Fragment>,
            <strong key="outcomes">Verified outcomes</strong>,
          ]}</Flow>
          <figcaption id="intent-caption">People develop intent with AI; agents carry it into verified outcomes.
            The <a href="#workbench">Workbench</a> brings the people, records and tools together.</figcaption>
        </figure>
        <Definitions ids={["ams", "intent", "workbench"]} />
        <ContextLink href="/start#what-it-is">Explore what AMS brings together</ContextLink>

        <h3 id="learning-through-work">Learning through work</h3>
        <figure className={styles.diagram} aria-labelledby="loop-caption">
          <Flow>{[
            <span key="observe">Observe friction</span>, <span key="change">Propose a bounded change</span>,
            <span key="compare">Compare outcomes</span>, <a key="disposition" href="#group-feedback-dispositions">Decide a disposition</a>,
            <span key="later">Examine later use</span>,
          ]}</Flow>
          <figcaption id="loop-caption">An <a href="#rsi-loop">RSI loop</a> follows the change through later use.
            An <a href="#improvement-attempt">improvement attempt</a> is one assessed candidate version.
            Recording the loop alone proves no improvement.</figcaption>
        </figure>
        <Definitions ids={["rsi-loop", "improvement-attempt"]} />

        <figure className={styles.diagram} aria-labelledby="assessment-caption">
          <p className={styles.origin}><a href="#alignment-assessment">Alignment assessment</a><span>Named candidate + scope · three runs</span></p>
          <ul className={styles.branches}>
            <li><Arrow className={styles.branchArrow} /><a href="#alignment-score">Alignment Score</a><span>Share of applicable checks passed</span></li>
            <li><Arrow className={styles.branchArrow} /><a href="#fitness-level">Fitness level</a><span>Passing runs + Critical failures</span></li>
          </ul>
          <figcaption id="assessment-caption">One assessment produces two different descriptions. Neither a score
            nor a fitness classification establishes acceptance.</figcaption>
        </figure>
        <Definitions ids={["alignment-assessment", "alignment-score", "fitness-level"]} />
        <ContextLink href="/rsi">Read the RSI evidence and its limits</ContextLink>
      </section>

      <section className={styles.section} aria-labelledby="group-records">
        <h2 id="group-records">Records: work, tests and judgment</h2>
        <div className={styles.comparison}>
          <div>
            <h3>Assign work</h3>
            <figure className={styles.miniDiagram} aria-labelledby="implementation-caption">
              <Flow>{[<span key="spec">Spec</span>, <a key="task" href="#implementation-task">Implementation Task</a>, <span key="proof">Execution + proof</span>]}</Flow>
              <figcaption id="implementation-caption">An assigned slice owns the work and its proof.</figcaption>
            </figure>
            <Definitions ids={["implementation-task"]} />
          </div>
          <div>
            <h3>Test repeatedly</h3>
            <figure className={styles.miniDiagram} aria-labelledby="evaluation-caption">
              <p className={styles.origin}><a href="#evaluation-task">Evaluation task</a><span>Repeatable test case</span></p>
              <ul className={styles.trials}><li><Arrow className={styles.branchArrow} />A trial</li><li><Arrow className={styles.branchArrow} />Another trial…</li></ul>
              <figcaption id="evaluation-caption">Each attempt at the case is a trial. These are tests, not implementation assignments.</figcaption>
            </figure>
            <Definitions ids={["evaluation-task"]} />
          </div>
        </div>
        <ContextLink href="/how-it-works#example">Follow a real implementation assignment</ContextLink>
        <ContextLink href="/governance">See the Task lifecycle</ContextLink>
        <figure className={styles.diagram} aria-labelledby="judgment-caption">
          <p className={styles.origin}>Candidate + scope</p>
          <ul className={styles.branches}>
            <li><Arrow className={styles.branchArrow} /><a href="#review-receipt">Review receipt</a><span>Reviewer involvement · findings · limits</span></li>
            <li><Arrow className={styles.branchArrow} /><a href="#human-qa-receipt">Human QA receipt</a><span>Sourced human judgment</span></li>
          </ul>
          <figcaption id="judgment-caption">Review records an actual assessment. Human QA records human judgment;
            agent checks cannot supply it.</figcaption>
        </figure>
        <Definitions ids={["review-receipt", "human-qa-receipt", "evidence-audit", "improvement-record"]} />
        <ContextLink href="/how-it-works#governance">Return to who decides and what counts as proof</ContextLink>
      </section>

      <section className={styles.section} aria-labelledby="group-feedback-dispositions">
        <h2 id="group-feedback-dispositions">Feedback dispositions</h2>
        <p><Inline md={groups.find(group => group.id === "group-feedback-dispositions")!.note} /></p>
        <figure className={styles.diagram} aria-labelledby="disposition-caption">
          <p className={styles.origin}>Finding</p>
          <ul className={`${styles.branches} ${styles.dispositions}`}>
            {[
              ["diagnostic", "Make visible"], ["test", "Detect"], ["repaired", "Implement + verify"],
              ["declined", "Decision + reason"], ["accepted-open", "Follow-up stays open"],
            ].map(([id, cue]) => <li key={id}><Arrow className={styles.branchArrow} /><a href={`#${id}`}>{id}</a><span>{cue}</span></li>)}
          </ul>
          <figcaption id="disposition-caption">These are different ways to handle a finding, not a sequence of required steps.</figcaption>
        </figure>
        <Definitions ids={["diagnostic", "test", "repaired", "declined", "accepted-open"]} />
        <ContextLink href="/rsi">Explore the RSI evidence</ContextLink>
        <ContextLink href="/how-it-works#governance">Back to how it works</ContextLink>
      </section>
      {additionalGroups.map(group => {
        const headingId = explainedGroupIds.has(group.id) ? `${group.id}-additional` : group.id;
        return (
          <section key={group.id} className={styles.section} aria-labelledby={headingId}>
            <h2 id={headingId}>{explainedGroupIds.has(group.id) ? `More ${group.heading.toLowerCase()}` : group.heading}</h2>
            <Definitions ids={group.terms.map(term => term.id)} />
          </section>
        );
      })}
      <p className={styles.source}><Inline md={glossary.intro} /> Definitions are copied from the project glossary.
        <Source path="GLOSSARY.md">GLOSSARY.md</Source></p>
    </div>
  );
}
