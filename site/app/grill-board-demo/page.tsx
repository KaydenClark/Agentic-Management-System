import Board from "./Board";
import { AgentBanner, HeaderSearch, ThemeToggle } from "./Islands";
import { CARDS, TOPICS } from "./data";

export const metadata = {
  title: "Grilling Board · demo with sample questions",
  description: "A demo of the Grill Board with sample, everyday questions. Nothing you do here is sent or saved.",
};

function WhereAnswersGo() {
  return (
    <section id="where-answers-go" aria-labelledby="where-answers-go-title" className="gb-where">
      <div className="eyebrow">About this demo</div>
      <h2 id="where-answers-go-title">Where a confirmed answer goes</h2>
      <p>
        Every card on this page is a sample with a made-up, everyday question. Everything you click stays in this
        browser tab: nothing is sent, saved or shared, and reloading starts over. Only your light or dark choice is
        remembered on this device.
      </p>
      <p>
        The real Grill Board runs on the owner&apos;s own computer, not on this site. Agents post only the questions
        that need the owner&apos;s answer. When the owner confirms one:
      </p>
      <ol>
        <li>
          The answer is written straight into the record that owns the question, for example the reunion plan&apos;s
          Venue section. There is no second confirmation step.
        </li>
        <li>
          The card shows as <strong>Answered · awaiting an agent</strong> until an agent has made the change it asks
          for, then as <strong>Applied</strong>.
        </li>
        <li>
          Ratings and the &ldquo;too taxing&rdquo; flag are kept as records too. A question flagged too taxing is
          rewritten before it is asked again.
        </li>
      </ol>
      <p className="gb-small">
        Each color means one thing: orange is trouble, yellow is why a choice is worth it, blue waits on you, green is
        the agents, purple came back to you. Grey needs nothing from you.
      </p>
    </section>
  );
}

export default function GrillBoardDemoPage() {
  return (
    <div className="gb-root">
      <header className="gb-header">
        <div className="gb-header-in">
          <div className="gb-brand">
            <span className="gb-brand-name">Workbench</span>
            <span className="gb-brand-sub">Dashboard · demo</span>
          </div>
          <HeaderSearch />
          <ThemeToggle />
        </div>
      </header>

      <div className="gb-strip gb-strip-demo">
        <span className="sample">Sample</span>
        <span style={{ flex: 1 }}>
          A demo board with sample questions. Nothing you do here is sent or saved.{" "}
          <a className="textlink" href="#where-answers-go">Where a confirmed answer goes</a>
        </span>
      </div>
      <AgentBanner />

      <Board topics={TOPICS} cards={CARDS}>
        <WhereAnswersGo />
      </Board>
    </div>
  );
}
