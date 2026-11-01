// /start: Start here, the first tour page (S-003). The Blueprint's elevator
// pitch as short screens, one idea and one picture each, then a toy that moves
// one sample piece of work through the real lifecycle. The diagram, the toy
// and its no-JS fallback all read app/start/flow.mjs. Every claim links the
// committed record it comes from; owner feedback 2026-11-01 asked for no
// quote and no essay.
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { HOLDERS, SOURCES as S, agentsAlso, mainPath, orchestrators, ownerAlso, stageById, stages, type Holder } from "./flow.mjs";
import { SourceLinks } from "./SourceLinks";
import { Toy } from "./Toy";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Start here | Agentic Management System",
  description: "What the Agentic Management System is, the problem it solves and how a piece of work moves through it, as pictures and a toy.",
};

const S003 = { label: "S-003", path: "workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md" };
const ARCH = { label: "Architecture", path: "ARCHITECTURE.md" };
const DDR000O = { label: "DDR-000O", path: "workbench/docs/ddr/000O-the-public-site-only-presents-and-reads-supabase.md" };
const ADR000G = { label: "ADR-000G", path: "workbench/docs/adr/000G-a-rule-is-enforced-only-when-code-refuses-and-a-test-shows-it.md" };

const PARTS = ["Agents", "Workflows", "Intent capture", "Skills", "Tools"];
const CARRIED = ["What you meant", "Why", "Corrections", "Proof"];

function Legend({ holders }: { holders: Holder[] }) {
  return (
    <ul className={styles.legend} aria-label="What the colours mean">
      {holders.map((h) => (
        <li key={h} className={`tone ${HOLDERS[h].hue}`}>
          <span className={styles.dot} aria-hidden="true" />
          {HOLDERS[h].meaning}
        </li>
      ))}
    </ul>
  );
}

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
  const returned = stages.find((s) => s.branch);
  const sendsBack = stages.filter((s) => s.back);
  const ownerStages = stages.filter((s) => s.holder === "owner");
  const agentStages = stages.filter((s) => s.holder === "agent");

  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>Start here</h1>
        <p className="lede" data-opener="">
          The Agentic Management System, or <dfn id="ams">AMS</dfn>, is how Kayden runs his{" "}
          <dfn id="agent">agents</dfn>: AI assistants that carry out a piece of work on their own. This page shows it
          in pictures, then hands you a toy: move one piece of work from an idea to done and see who holds it at each
          step.
        </p>
        <p className={styles.jump}>
          <a href="#try">Skip to the toy</a>
        </p>
      </header>

      <Screen id="what-it-is" n={1} title="What the AMS is">
        <p className={styles.say}>
          One system for everything Kayden uses to work with AI, run as one loop that improves itself through real
          work.
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

      <Screen id="problem" n={2} title="The problem it solves">
        <p className={styles.say}>
          Hand work to an AI and the meaning can get lost on the way. The AMS keeps it attached from the request to
          the result, and nothing counts as done without proof.
        </p>
        <figure className={styles.figure}>
          <div className={styles.lanes}>
            <div className={styles.lane} data-lane="without">
              <p className={styles.laneName}>Without it</p>
              <div className={styles.laneRow}>
                <span className={styles.end}>Request</span>
                <ul className={styles.lost}>
                  {CARRIED.map((c) => (
                    <li key={c}>
                      <s>{c}</s>
                    </li>
                  ))}
                </ul>
                <span className={styles.end}>A result, but is it right?</span>
              </div>
            </div>
            <div className={styles.lane} data-lane="with">
              <p className={styles.laneName}>With the AMS</p>
              <div className={styles.laneRow}>
                <span className={styles.end}>Request</span>
                <ul className={styles.kept}>
                  {CARRIED.map((c) => (
                    <li key={c}>{c}</li>
                  ))}
                </ul>
                <span className={styles.end}>The result, with its proof</span>
              </div>
            </div>
          </div>
          <figcaption>
            Without a system, what you meant, why, your corrections and the proof fall away between the request and the
            result. With the AMS all four travel with the work.
          </figcaption>
        </figure>
        <SourceLinks sources={[S.blueprint, S.adr001H]} />
      </Screen>

      <Screen id="flow" n={3} title="How a piece of work moves">
        <p className={styles.say}>
          Every change takes the same path. Colour shows who holds it; work that fails a review or Kayden&apos;s look
          comes back and goes round again.
        </p>
        <figure className={styles.figure}>
          <div className={styles.flow} data-flow-diagram="">
            <ol className={styles.flowPath}>
              {mainPath.map((s, i) => (
                <li key={s.id} data-stage={s.id} className={`tone ${HOLDERS[s.holder].hue} ${styles.node}`}>
                  <span className={styles.nodeNo}>{i + 1}</span>
                  <span className={styles.nodeName}>{s.name}</span>
                  <span className={styles.nodeWho}>{HOLDERS[s.holder].label}</span>
                </li>
              ))}
            </ol>
            {returned ? (
              <div className={styles.loop}>
                <p className={styles.loopFrom}>{sendsBack.map((s) => s.name).join(" or ")} can send it back</p>
                <ul className={styles.loopPath}>
                  <li data-stage={returned.id} className={`tone ${HOLDERS[returned.holder].hue} ${styles.node}`}>
                    <span className={styles.nodeNo}>Loop</span>
                    <span className={styles.nodeName}>{returned.name}</span>
                    <span className={styles.nodeWho}>{HOLDERS[returned.holder].label}</span>
                  </li>
                </ul>
                <p className={styles.loopFrom}>then back to {stageById(returned.next?.to ?? "").name}</p>
              </div>
            ) : null}
          </div>
          <figcaption>
            In order: {mainPath.map((s) => `${s.name} (${HOLDERS[s.holder].label})`).join(", ")}.{" "}
            {sendsBack.map((s) => s.name).join(" and ")} can send work to {returned?.name}, which leads back to{" "}
            {stageById(returned?.next?.to ?? "").name}.
          </figcaption>
        </figure>
        <Legend holders={["owner", "agent", "returned", "done"]} />
        <SourceLinks sources={[S.runbook, S.ddr000F, S.ddr000M, S.ddr000Y]} />
      </Screen>

      <Screen id="try" n={4} title="Try it: move one piece of work">
        <p className={styles.say}>
          Press the big button to pass the work on. At Review and Approve you choose: pass it, or send it back and
          watch it come round again.
        </p>
        <Toy />
      </Screen>

      <Screen id="who" n={5} title="Who does what">
        <p className={styles.say}>
          Kayden decides what and whether. Agents do everything in between, and three of them split the risky parts
          so none holds them all.
        </p>
        <figure className={styles.figure}>
          <div className={styles.split}>
            <div className={`tone h-owner ${styles.side}`}>
              <p className={styles.sideName}>
                <span className={styles.dot} aria-hidden="true" />
                Kayden
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
          <figcaption>What Kayden does, and the lifecycle stages agents carry.</figcaption>
        </figure>
        <SourceLinks sources={[S.ddr000G, S.ddr000H, S.ddr000F, S.adr003F]} />

        <figure className={styles.figure}>
          <div className={styles.tree}>
            <p className={`tone h-owner ${styles.treeTop}`}>
              <span className={styles.dot} aria-hidden="true" />
              Kayden, the owner
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
            Three orchestrators, all Claude, work for Kayden. No session holds untrusted input, secrets and the power
            to act in the outside world all at once.
          </figcaption>
        </figure>
        <SourceLinks sources={[S.adr002Z, S.adr002P]} />
      </Screen>

      <Screen id="refuses" n={6} title="What it refuses to do">
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
            <strong>Mistake looks for proof.</strong> A screenshot or a passing structural check is not proof that it works.
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
        <ul className={styles.today}>
          <li>
            The AMS runtime software does not exist yet; today the system is its records, tools and agents.
            <SourceLinks sources={[ARCH]} />
          </li>
          <li>
            No improvement has been measured yet, so the <Link href="/rsi">RSI results</Link> page is empty on purpose.
          </li>
          <li>
            Every page of this site, this one included, is a draft until Kayden approves it.
            <SourceLinks sources={[S003]} />
          </li>
        </ul>
        <p className={styles.say}>
          Next, <Link href="/how-it-works">How it works</Link> opens the records behind each stage.
        </p>
      </Screen>
    </div>
  );
}
