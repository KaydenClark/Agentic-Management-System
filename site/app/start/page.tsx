// /start: the canonical About introduction (S-003). /about is a compatibility alias. The Blueprint's elevator
// pitch as short screens, one idea and one picture each, then a toy that moves
// one sample piece of work through the real lifecycle, then the quickstart:
// a reading route through the site (S-003 Quickstart: no installation,
// credentials or command replay) and the setup-workbench step. The diagram,
// the toy and its no-JS fallback all read app/start/flow.mjs. Every claim links the
// committed record it comes from; owner feedback 2026-11-01 asked for no
// quote and no essay.
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { SOURCES as S, agentsAlso, orchestrators, ownerAlso, stages } from "./flow.mjs";
import { sources as skillSources, stages as skillStages } from "./skills.mjs";
import { SourceLinks } from "./SourceLinks";
import { Toy } from "./Toy";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "About | Agentic Management System",
  description: "About AMS: its purpose, people, methods, limits and first website, with a toy and a route for exploring it.",
};

const S003 = { label: "S-003", path: "workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md" };
const ARCH = { label: "Architecture", path: "ARCHITECTURE.md" };
const WORKBENCH = { label: "Workbench Node lifecycle", path: "workbench/tools/spec-workbench.mjs" };
const PYTHON = { label: "Python command-line tools", path: "src/ams/trials.py" };
const DDR000O = { label: "DDR-000O", path: "workbench/docs/ddr/000O-the-public-site-only-presents-and-reads-supabase.md" };
const ADR000G = { label: "ADR-000G", path: "workbench/docs/adr/000G-a-rule-is-enforced-only-when-code-refuses-and-a-test-shows-it.md" };
const SKILLS_MD = { label: "Workbench skills", path: "workbench/docs/SKILLS.md" };
const README_AGENTS = { label: "README, Working With Agents", path: "README.md" };
const MANIFEST = { label: "the manifest, skillPolicy", path: "workbench/manifest.json" };

const PARTS = ["Agents", "Workflows", "Intent capture", "Skills", "Tools"];


function Screen({ id, n, title, children }: { id: string; n: number; title: string; children: ReactNode }) {
  return (
    <section className={styles.screen} aria-labelledby={id}>
      <p className={styles.screenNo} aria-hidden="true">
        {String(n).padStart(2, "0")}
      </p>
      <h2 id={id}>{title}</h2>
      {children}
    </section>
  );
}

export default function StartHere() {
  const ownerStages = stages.filter((s) => s.holder === "owner");
  const agentStages = stages.filter((s) => s.holder === "agent");

  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>About</h1>
        <p className="lede" data-opener="">
          The Agentic Management System, or <dfn id="ams">AMS</dfn>, brings people and AI assistants together to
          turn <dfn id="intent">intent</dfn>—what you want, why and within what boundaries—into checked outcomes.
          The assistants, called <dfn id="agent">agents</dfn>, carry out the work. This introduction explains the
          system in pictures, lets you try a small demonstration, and points to the evidence and limits.
        </p>
        <p className={styles.jump}>
          <a href="#try">Try the toy</a> <a href="#refuses">Limits</a> <a href="#built">The project</a> <a href="#quickstart">Where to go next</a>
        </p>
      </header>

      <Screen id="what-it-is" n={1} title="What the AMS is">
        <p className={styles.say}>
          Workflows, rules, skills and tools that anyone can reuse to carry intent through AI work into reality.
          This project adds RSI to test and improve those methods through real work.
        </p>
        <figure className={styles.figure}>
          <div className={styles.hub}>
            <svg className={styles.ring} viewBox="0 0 200 200" aria-hidden="true" focusable="false">
              <defs>
                <marker id="ring-head" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M0 0 L10 5 L0 10 z" className={styles.ringHead} />
                </marker>
              </defs>
              <path d="M100 18 A82 82 0 1 1 30 57" className={styles.ringPath} markerEnd="url(#ring-head)" />
            </svg>
            <p className={styles.core}>AMS</p>
            <ul className={styles.parts}>
              {PARTS.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          </div>
          <figcaption>
            Agents, workflows, intent capture, skills and tools in one loop. The loop is called <dfn id="rsi">RSI</dfn>,
            recursive self-improvement: find where work goes wrong, try one bounded fix, compare, keep what helps. Its
            first round builds this website.
          </figcaption>
        </figure>
        <SourceLinks sources={[S.blueprint, S.ddr000A, S.glossary]} />
      </Screen>

      <Screen id="problem" n={2} title="Why keep intent with the work?">
        <p className={styles.say}>
          A useful result needs to reflect what you meant, including the reasons, corrections and boundaries.
          AMS gives that understanding a lasting home and gives each piece of work a clear owner.
          <Link href="/why#words"> Why</Link> explores the problem, the intended benefits and what evidence would
          show that the methods help. These are goals, not a promise that every project improves.
        </p>
      </Screen>

      <Screen id="flow" n={3} title="How a piece of work moves">
        <p className={styles.say}>
          The methods below cover agreeing what is wanted, preparing work, carrying it out and judging the result.
          A skill is a written method an agent uses for a particular job; the work selects the methods it needs.
          <Link href="/how-it-works"> How it works</Link> explains the records and decisions behind the stages.
        </p>
        <figure className={styles.figure}>
          <ol className={styles.skillStages} data-skills-diagram="">
            {skillStages.map((st) => (
              <li key={st.id} data-skill-stage={st.id} className={styles.skillStage}>
                <div className={styles.skillStageHead}>
                  <p className={styles.skillStageName}>{st.name}</p>
                  <p className={styles.skillStageGloss}>{st.gloss}</p>
                </div>
                <div className={styles.skillStageBody}>
                  <ul className={styles.skillMain} aria-label={`${st.name}: main flow`}>
                    {st.main.map((k) => (
                      <li key={k} data-skill={k} data-main="">
                        <Link className={styles.skillLink} href={`/skills/${k}`}>
                          {k}
                        </Link>
                      </li>
                    ))}
                  </ul>
                  {st.used.length ? (
                    <ul className={styles.skillUsed} aria-label={`${st.name}: also used`}>
                      {st.used.map((k) => (
                        <li key={k} data-skill={k}>
                          <Link className={styles.skillLink} href={`/skills/${k}`}>
                            {k}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  ) : null}
                  {st.note ? <p className={styles.skillNote}>↻ {st.note}</p> : null}
                </div>
              </li>
            ))}
          </ol>
          <figcaption>
            In order: {skillStages.map((st) => `${st.name} (${st.main.join(", then ")})`).join("; ")}. Solid chips are
            the main flow, run in order; outlined chips are other skills used at that stage.
          </figcaption>
        </figure>
        <ul className={styles.skillKey} aria-label="What the chips mean">
          <li>
            <span className={styles.keyMain} aria-hidden="true" />
            Main flow
          </li>
          <li>
            <span className={styles.keyUsed} aria-hidden="true" />
            Used at this stage
          </li>
        </ul>
        <SourceLinks sources={skillSources} />
      </Screen>

      <Screen id="try" n={4} title="Try it: move one piece of work">
        <p className={styles.say}>
          Press the big button to pass the work on. At Review and Approve you choose: pass it, or send it back and
          watch it come around again.
        </p>
        <Toy />
      </Screen>

      <Screen id="who" n={5} title="Who does what">
        <p className={styles.say}>
          The owner sets the intent and makes the approval decisions. Agents do everything in between, and three of them split the risky parts
          so none holds them all.
        </p>
        <figure className={styles.figure}>
          <div className={styles.split}>
            <div className={`tone h-owner ${styles.side}`}>
              <p className={styles.sideName}>
                <span className={styles.dot} aria-hidden="true" />
                Owner
              </p>
              <ul>
                {ownerStages.map((s) => (
                  <li key={s.id}>
                    <strong>{s.name}.</strong> {s.line}
                  </li>
                ))}
                {ownerAlso.map((o) => (
                  <li key={o.line}>{o.line}</li>
                ))}
              </ul>
            </div>
            <div className={`tone h-agent ${styles.side}`}>
              <p className={styles.sideName}>
                <span className={styles.dot} aria-hidden="true" />
                Agents
              </p>
              <ul className={styles.chips}>
                {agentStages.map((s) => (
                  <li key={s.id}>{s.name}</li>
                ))}
              </ul>
              <ul>
                {agentsAlso.map((o) => (
                  <li key={o.line}>{o.line}</li>
                ))}
              </ul>
            </div>
          </div>
          <figcaption>What the owner does, and the lifecycle stages agents carry.</figcaption>
        </figure>
        <SourceLinks sources={[S.ddr000G, S.ddr000H, S.ddr000F, S.adr003F]} />

        <figure className={styles.figure}>
          <div className={styles.tree}>
            <p className={`tone h-owner ${styles.treeTop}`}>
              <span className={styles.dot} aria-hidden="true" />
              The owner
            </p>
            <ul className={styles.treeRow}>
              {orchestrators.map((o) => (
                <li key={o.id} className={`tone h-agent ${styles.orch}`}>
                  <p className={styles.orchName}>
                    {o.id}. {o.name}
                  </p>
                  <p>{o.does}</p>
                  <p className={styles.never}>Never: {o.never}</p>
                </li>
              ))}
            </ul>
          </div>
          <figcaption>
            This project separates website, local data and consistency work into orchestration roles. Different AI assistants can carry those roles. No session holds untrusted input, secrets and the power
            to act in the outside world all at once.
          </figcaption>
        </figure>
        <SourceLinks sources={[S.adr002Z, S.adr002P]} />
      </Screen>

      <Screen id="refuses" n={6} title="Limits: what it refuses to do">
        <p>
          This website runs no agents and writes no project records. Its toy is an illustration, not a control for
          real work. Published activity, a passing check and an audit score are different from demonstrated
          improvement. <Link href="/how-it-works#guarantees">Checks and human judgment</Link> explain why those
          boundaries matter; <Link href="/rsi">RSI results</Link> presents the evidence and its remaining gaps.
        </p>
        <ul className={styles.refusals} data-refusals="">
          <li>
            <strong>Go past the ask.</strong> Nothing destructive, paid or wider in scope without asking first.
            <SourceLinks sources={[S.agents]} />
          </li>
          <li>
            <strong>Leak.</strong> No secrets committed, no private research published.
            <SourceLinks sources={[S.agents, S.blueprint]} />
          </li>
          <li>
            <strong>Speak for anyone.</strong> No messages sent without authorization.
            <SourceLinks sources={[S.agents]} />
          </li>
          <li>
            <strong>Take appearances as proof.</strong> A screenshot or a passing structural check is not proof that it works.
            <SourceLinks sources={[S.blueprint]} />
          </li>
          <li>
            <strong>Call a written rule enforced.</strong> Only code that refuses, and a test that shows it, counts.
            <SourceLinks sources={[ADR000G]} />
          </li>
          <li>
            <strong>Retry forever.</strong> Three strikes, then stop and report.
            <SourceLinks sources={[S.adr002W]} />
          </li>
          <li>
            <strong>Run anything from this site.</strong> It only presents: no agents, no edited records.
            <SourceLinks sources={[S003, DDR000O]} />
          </li>
        </ul>
      </Screen>

      <Screen id="today" n={7} title="Where it stands today">
        <ul id="status" className={styles.today}>
          <li>
            The Workbench Node lifecycle and Python command-line tools are working components; the assembled RSI loop has not been demonstrated as a runtime system.
            <SourceLinks sources={[ARCH, WORKBENCH, PYTHON]} />
          </li>
          <li>
            The <Link href="/rsi">RSI results</Link> page contains development evidence from shared-skill repair
            attempts, including checks, failures and remaining gaps. This evidence does not establish demonstrated
            improvement.
          </li>
        </ul>
      </Screen>

      <section id="built" className={styles.screen} aria-labelledby="project">
        <h2 id="project">The project behind this website</h2>
        <p>
          Kayden Clark created this AMS project to develop reusable ways of working with AI. This website is its
          first outside product: its development follows the methods it explains. Friction from the
          build supplies issues to investigate and bounded improvements to compare; merely recording a repair
          does not show that it helped.
        </p>
        <h3 id="holds">What the project files hold</h3>
        <p>
          The Workbench holds the intended outcomes, assignments, decisions, knowledge and feedback. The local
          Grill Board helps the owner answer questions about the work; Python tools handle stored evidence.
          This website presents explanations and reads published results. These components have different jobs
          and permissions; <Link href="/how-it-works#grill-board">the Grill Board</Link> and
          <Link href="/how-it-works#governance"> governance</Link> sections explain those boundaries.
        </p>
        <h3 id="license">License and delivery</h3>
        <p>
          The project uses the MIT License, copyright 2026 Kayden Clark. Reuse and modification are allowed under
          its terms, including keeping its copyright and permission notice. Website changes are checked on dev;
          only the owner promotes them to the public main version. The footer displays the build revision as text.
        </p>
        <SourceLinks sources={[S003, { label: "DDR-000R", path: "workbench/docs/ddr/000R-the-license-is-mit-copyright-kayden-clark.md" }, { label: "LICENSE", path: "LICENSE" }]} />
      </section>

      <Screen id="quickstart" n={8} title="Quickstart: where to go from here">
        <p className={styles.say}>
          Four stops take you through the rest of the site, with nothing to install. Take them in order; each one
          teaches one thing.
        </p>
        <ol className={styles.route} data-route="">
          <li>
            <strong>The introduction.</strong> You have just read it: the screens above say what the AMS is, the
            problem it solves and how a piece of work moves. <Link href="/why">Why</Link> adds what the system is
            for and what it promises.
          </li>
          <li>
            <strong>A real piece of work.</strong> <Link href="/how-it-works#example">How it works</Link> follows
            a real Spec, a bounded destination with acceptance conditions, and two of its Tasks that plan and carry out execution from this site. You can
            see how work was split up, checked and handed back, including what the recorded checks could not prove.
          </li>
          <li>
            <strong>A demonstration and the skills.</strong> The <a href="#try">toy</a> on this page shows who holds
            the work at each step, and the <Link href="/skills">Skills</Link> wiki summarizes each written method an agent
            loads before it acts.
          </li>
          <li>
            <strong>The evidence and its limits.</strong> <Link href="/rsi">RSI results</Link> shows development
            evidence from repair attempts and is where measured results will appear. The repair evidence alone does
            not prove improvement; <Link href="/why#bet">Why it calls itself a bet</Link> explains that distinction.
          </li>
        </ol>
        <div className={styles.setup} data-setup-step="">
          <p className={styles.say}>
            Then, to set up a Workbench of your own, use the{" "}
            <Link href="/skills/setup-workbench">setup-workbench</Link> skill.
          </p>
          <p>
            A Workbench is the set of project files that tells agents the rules, holds the queue of work and says how
            to check it. The setup-workbench skill is the method the project names for preparing, adopting, updating or
            checking one. It belongs to Kayden&apos;s own skill collection rather than this repository, so the
            Skills page describes what it does and what it needs.
          </p>
          <SourceLinks sources={[SKILLS_MD, README_AGENTS, MANIFEST]} />
        </div>
        <p>
          New words along the way are in the <Link href="/glossary">Glossary</Link>, and{" "}
          <a href="#holds">the project files</a> explain where the different parts live.
        </p>
      </Screen>
    </div>
  );
}
