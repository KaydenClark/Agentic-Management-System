import Link from "next/link";
import styles from "./tour/tour.module.css";

export default function Home() {
  return (
    <>
      <h1>Agentic Management System</h1>
      <p className="lede" data-opener="">
        Explore a way to turn what you want into checked work with AI. See how the system organizes the work,
        try a small demonstration, and examine the evidence behind its intended benefits.
      </p>
      <section className="card" aria-labelledby="explore">
        <h2 id="explore">Find your way in</h2>
        <ul className={styles.list}>
          <li><Link href="/start">About AMS</Link>: the introduction, people, toy and a starting point for your own setup.</li>
          <li><Link href="/why">Why it exists</Link>: the problems the methods address and the benefits still to prove.</li>
          <li><Link href="/how-it-works#example">One real piece of work</Link>: how a request became checked website changes.</li>
          <li><Link href="/skills">Skills</Link>: the written methods people and agents use along the way.</li>
          <li><Link href="/rsi">RSI results</Link>: what comparisons and failures can tell you about improvement.</li>
          <li><Link href="/start#refuses">Limits</Link>: what the website does, what it cannot prove and where human decisions remain.</li>
        </ul>
      </section>
      <section className="card" aria-labelledby="this-site">
        <h2 id="this-site">A website built with the system it explains</h2>
        <p>
          This is the AMS project’s first outside product. Building it gives the team real work from which to
          learn. The site presents explanations, demonstrations and published evidence; it does not operate
          agents or change project records. Every page’s footer identifies its build revision as text.
        </p>
      </section>
    </>
  );
}
