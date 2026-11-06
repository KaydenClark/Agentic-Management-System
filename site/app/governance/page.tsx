import task from "../../content/governance/task-lifecycle.json";
import flows from "../../content/governance/spec-flows.json";
import styles from "./page.module.css";

type Transition = { from: string; to: string; action: string };
function Diagram({ id, transitions, caption }: { id: string; transitions: Transition[]; caption: string }) {
  return (
    <figure className={styles.diagram} aria-labelledby={id}>
      <ol className={styles.edges}>
        {transitions.map(({ from, to, action }) => (
          <li key={`${from}-${to}`}>
            <span className={styles.pair}><strong>{from}</strong><span>→ to</span><strong>{to}</strong></span>
            <span>{action}.</span>
          </li>
        ))}
      </ol>
      <figcaption id={id}>{caption}</figcaption>
    </figure>
  );
}

export default function Governance() {
  return (
    <>
      <h1>How work moves</h1>
      <p className="lede">A request becomes bounded work, then a checked result. These diagrams explain the records and decisions along that route.</p>
      <section aria-labelledby="task-states">
        <h2 id="task-states">Task lifecycle</h2>
        <p>A Task is one bounded assignment. Its record accepts these states: {task.states.join(", ")}. The transitions below are the actions the current tools perform. A valid state does not necessarily have a tool action that moves a Task into it.</p>
        <Diagram id="task-flow-caption" transitions={task.transitions} caption="Each arrow is a tool action. The branches are alternatives, not one sequence." />
        <p>A dependency may also make ready work appear blocked until its prerequisite is satisfied. A close records a result; it is not independent review or owner acceptance.</p>
      </section>
      <section aria-labelledby="spec-states">
        <h2 id="spec-states">Spec lifecycle</h2>
        <p>A Spec describes a destination and the conditions for judging it. Its record accepts: {flows.spec.states.join(", ")}. The arrows show the status changes the current tools write; the other valid states do not imply additional automated transitions.</p>
        <Diagram id="spec-flow-caption" transitions={flows.spec.transitions} caption="Activation and completion have conditions. Completion requires the approved result on the declared default branch." />
      </section>
      <section aria-labelledby="delivery-flow">
        <h2 id="delivery-flow">From idea to delivery</h2>
        <p>These are stages of work, not record statuses. Journey includes implementation, checks, QA and submission; Judge includes review, verification and approval. Complete includes delivery and cleanup; delivery needs the permission applicable to that action.</p>
        <Diagram id="delivery-flow-caption" transitions={flows.delivery.transitions} caption="Each stage publishes its result; confirmation and execution approval are distinct decisions." />
      </section>
      <section aria-labelledby="review-flow">
        <h2 id="review-flow">Review and return</h2>
        <p>A reviewer judges a named candidate. A finding returns the affected work to its owner; the corrected candidate needs a fresh assessment. An owner finding can also return the work. A changed concept may return to earlier discovery and planning.</p>
        <Diagram id="review-flow-caption" transitions={flows.review.transitions} caption="Arrows show passing and return paths; they are alternatives. Approval binds the identified content. Delivery still needs its scoped permission; neither a merge nor an agent check supplies the owner's judgment." />
      </section>
    </>
  );
}
