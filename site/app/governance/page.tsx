import lifecycle from "../../content/governance/task-lifecycle.json";
import styles from "./page.module.css";

export default function Governance() {
  return (
    <>
      <h1>How a Task moves</h1>
      <p className="lede">A Task is one bounded piece of work. Its record says what is ready, underway, blocked or finished.</p>
      <section aria-labelledby="task-states">
        <h2 id="task-states">Task lifecycle</h2>
        <p>The record accepts these states: {lifecycle.states.join(", ")}. The transitions below are the actions the current tools perform. A valid state does not necessarily have a tool action that moves a Task into it.</p>
        <figure className={styles.diagram} aria-labelledby="task-flow-caption">
          <ol className={styles.edges}>
            {lifecycle.transitions.map(({ from, to, action }) => (
              <li key={`${from}-${to}`}>
                <span className={styles.pair}><strong>{from}</strong><span aria-label="to">→</span><strong>{to}</strong></span>
                <span>{action}.</span>
              </li>
            ))}
          </ol>
          <figcaption id="task-flow-caption">Each arrow is a tool action. The branches are alternatives, not one sequence.</figcaption>
        </figure>
        <p>A dependency may also make ready work appear blocked until its prerequisite is satisfied. A close records a result; it is not independent review or owner acceptance.</p>
      </section>
    </>
  );
}
