import lifecycle from "../../content/governance/task-lifecycle.json";

export default function Governance() {
  return (
    <>
      <h1>How a Task moves</h1>
      <p className="lede">A Task is one bounded piece of work. Its record says what is ready, underway, blocked or finished.</p>
      <section aria-labelledby="task-states">
        <h2 id="task-states">Task lifecycle</h2>
        <p>The record accepts these states: {lifecycle.states.join(", ")}. The transitions below are the actions the current tools perform. A valid state does not necessarily have a tool action that moves a Task into it.</p>
        <ol>
          {lifecycle.transitions.map(({ from, to, action }) => (
            <li key={`${from}-${to}`}><strong>{from} → {to}</strong>: {action}.</li>
          ))}
        </ol>
        <p>A dependency may also make ready work appear blocked until its prerequisite is satisfied. A close records a result; it is not independent review or owner acceptance.</p>
      </section>
    </>
  );
}
