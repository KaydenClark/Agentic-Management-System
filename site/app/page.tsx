export default function Home() {
  return (
    <>
      <p className="eyebrow">Start here</p>
      <h1>Agentic Management System</h1>
      <p className="lede" data-opener="">
        The Agentic Management System, or AMS, is a reusable system of workflows, rules, skills and tools
        for turning intent into outcomes with AI. People capture and develop what they want; AI assistants,
        called agents, carry out the work. Records preserve intent, decisions, corrections and proof through delivery.
      </p>
      <section className="card" aria-labelledby="this-site">
        <h2 id="this-site">This site</h2>
        <p>
          This project adds recursive self-improvement (RSI): building this site exposes problems in the methods,
          and bounded comparisons test whether repairs help. The site presents the records and evidence. The
          tour pages arrive one reviewed change at a time. The footer of every page names the exact commit it
          was built from, linked to the code on GitHub.
        </p>
      </section>
    </>
  );
}
