import Board from "./Board";
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
        The real Grill Board runs on the owner&apos;s computer. Each question is backed by a Destination Question Card
        (DQC), which holds its proposal, reasons, source and history. Confirming preserves the exact displayed readback
        on that DQC; corrections and quality feedback retain their own state.
      </p>
      <p>
        After a round, an agent reviews changes and reconciles confirmed, authorized understanding into the relevant
        project records. Confirmation does not start implementation; execution has its own approval. A Too taxing
        flag holds a question for rewriting. This demo performs none of those real actions.
      </p>
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

        <Board topics={TOPICS} cards={CARDS}>
          <WhereAnswersGo />
        </Board>
      </div>
    </>
  );
}
