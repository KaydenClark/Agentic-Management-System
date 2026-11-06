import task from "../../content/governance/task-lifecycle.json";
import flows from "../../content/governance/spec-flows.json";
import planes from "../../content/governance/planes.json";
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
      <section aria-labelledby="authority">
        <h2 id="authority">Who can decide?</h2>
        <p>Platform safety rules set the outer boundary. Within it, the owner’s current request sets the work; project instructions in AGENTS.md constrain it; an assigned Spec or Task narrows the work further. A written plan cannot grant itself permission.</p>
        <p><strong>Example:</strong> If the owner asks for a keyboard fix, the assignment can describe and test that fix. It cannot authorize unrelated changes outside the request or the project rules.</p>
        <h3>Different decisions, different evidence</h3>
        <p><strong>Confirmation</strong> records shared understanding. <strong>Execution approval</strong> permits the stated work. They can be given together, but one does not imply the other. <strong>Review</strong> is a separate assessment of identified work; <strong>Human QA</strong> is the owner’s actual judgment of an identified experience.</p>
        <p><strong>Example:</strong> The owner may confirm and approve a fix in one response. Later an independent reviewer checks the named result, and the owner may perform Human QA. A passing test or a merge supplies neither judgment.</p>
        <h3>What a check can establish</h3>
        <p>A check blocks or supports only what its consuming operation actually evaluates. Its result is evidence about the case it exercised, not a general approval.</p>
        <p><strong>Example:</strong> A test can block a build when a button cannot receive keyboard focus. Passing it does not prove that every page is accessible or that the owner accepted the experience.</p>
      </section>
      <section aria-labelledby="governance-stack">
        <h2 id="governance-stack">Six roles a claim can play</h2>
        <p>A governance plane is the role a claim plays for a particular target and operation. The planes classify claims, not whole files or folders. One Spec, for example, can contain a desired outcome, a governing condition and evidence, each playing a different role.</p>
        <p>The numbered order is a way to use the stack, not a ranking that resolves disagreement. The same claim, “the button supports keyboard use,” can express an owner’s intent, a governing requirement, a reported test result or an observation, depending on its source and purpose. Repeating the words alone does not make the claim authoritative or proven.</p>
        <figure className={styles.diagram} aria-labelledby="planes-caption">
          <ol className={styles.edges}>
            {planes.map(({ number, name, definition, example }) => (
              <li key={name}>
                <strong>{number}. {name}</strong>
                <span>{definition}</span>
                <span><strong>Example:</strong> {example}</span>
              </li>
            ))}
          </ol>
          <figcaption id="planes-caption">One illustrative button fix: different claims have different roles. These are not folders, stages or extra approval gates.</figcaption>
        </figure>
        <h3>Work down, then back up</h3>
        <p><strong>Down: 6 → 5 → 4 → 3 → 2 → 1.</strong> Start with a dated summary; develop the owner’s intent; update what is known; examine evidence; update what governs within existing authority; then change what exists.</p>
        <p><strong>Up: 1 → 2 → 3 → 4 → 5 → 6.</strong> Inspect what changed; reconcile governing claims if needed; record evidence; update what is known; record whether the intent was delivered; then summarize the result with its source revision or time and remaining gaps.</p>
        <p>For the button example, a stale summary prompts the owner’s request. The team uses current knowledge and test evidence to update the governing condition and repair the button. On the way back, it records what actually happened and what the test showed before updating the summary. This traversal grants no execution authority and does not establish owner acceptance or Human QA.</p>
        <p><a href="/glossary#governance-plane">Read the exact governance definitions in the glossary</a>.</p>
      </section>
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
