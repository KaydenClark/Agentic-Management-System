import Board from "./Board";
import { AgentBanner } from "./Islands";
import { CARDS, TOPICS } from "./data";
import "./board.css";

export const metadata = {
  title: "Grill Board demo | Agentic Management System",
  description: "A demo of the Grill Board with sample, everyday questions. Nothing you do here is sent or saved.",
};

function WhereAnswersGo() {
  return (
    <section id="where-answers-go" aria-labelledby="where-answers-go-title" className="gb-where" data-where-answers-go="">
      <div className="gb-eyebrow">About this demo</div>
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
    <>
      <header className="gb-intro">
        <span className="eyebrow">Demo · sample questions</span>
        <h1>Grill Board demo</h1>
        <p data-opener="">
          The Grill Board is where the owner answers the questions agents cannot settle alone. This demo shows it with
          made-up, everyday questions about a family reunion, a corner bakery and a community garden. Rate a question,
          flag it as too taxing or pick an answer: nothing you do here is sent or saved.{" "}
          <a href="#where-answers-go">Where a confirmed answer goes</a>.
        </p>
      </header>

      <div className="gb-root">
        <div className="gb-strip gb-strip-demo">
          <span className="sample">Sample</span>
          <span className="grow">
            A demo board with sample questions. Nothing you do here is sent or saved.{" "}
            <a className="textlink" href="#where-answers-go">Where a confirmed answer goes</a>
          </span>
        </div>
        <AgentBanner />

        <Board topics={TOPICS} cards={CARDS}>
          <WhereAnswersGo />
        </Board>
      </div>
    </>
  );
}
