// The one data file /start reads: the lifecycle of a piece of work, who holds
// it at each stage, and the split between the owner and the orchestrators.
// The lifecycle diagram, the toy and the toy's no-JS fallback all render from
// these lists, so they cannot disagree (tests/start-flow.test.mjs).
// Every stage cites the committed records it comes from (paths from the
// repository root). Plain JavaScript so the tests import it on any Node that
// runs npm test; its types are in flow.d.mts.

// The four signals /start uses, each with its one meaning (DDR-000M) and the
// tokens.css hue class that carries it (DDR-000Y). Nothing else is coloured.
export const HOLDERS = {
  owner: { label: "Kayden", ball: "Kayden has the ball", meaning: "Blue: it waits on the owner, Kayden.", hue: "h-owner" },
  agent: { label: "Agents", ball: "Agents have the ball", meaning: "Green: agents carry it.", hue: "h-agent" },
  returned: { label: "Returned", ball: "Returned for rework", meaning: "Purple: it came back for rework.", hue: "h-returned" },
  done: { label: "Done", ball: "Done: nothing waits on anyone", meaning: "Grey: done, nothing for you here.", hue: "h-none" },
};

const ADR = "workbench/docs/adr/";
const DDR = "workbench/docs/ddr/";
const src = {
  blueprint: { label: "Blueprint", path: "BLUEPRINT.md" },
  runbook: { label: "Runbook", path: "RUNBOOK.md" },
  agents: { label: "AGENTS.md", path: "AGENTS.md" },
  glossary: { label: "Glossary", path: "GLOSSARY.md" },
  ddr000A: { label: "DDR-000A", path: `${DDR}000A-the-ams-is-the-owner-s-agent-management-system.md` },
  ddr000F: { label: "DDR-000F", path: `${DDR}000F-delivery-runs-in-rounds-the-owner-approves-or-returns.md` },
  ddr000G: { label: "DDR-000G", path: `${DDR}000G-nothing-is-built-before-the-owner-confirms-a-readback.md` },
  ddr000H: { label: "DDR-000H", path: `${DDR}000H-confirmation-approval-and-the-two-delivery-paths.md` },
  ddr000M: { label: "DDR-000M", path: `${DDR}000M-colors-on-owner-pages-are-signals-with-one-meaning-each.md` },
  ddr000Y: { label: "DDR-000Y", path: `${DDR}000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md` },
  adr000P: { label: "ADR-000P", path: `${ADR}000P-a-capability-change-gets-one-short-spec.md` },
  adr000Q: { label: "ADR-000Q", path: `${ADR}000Q-each-task-is-its-own-runnable-file.md` },
  adr000R: { label: "ADR-000R", path: `${ADR}000R-a-task-is-one-agent-run.md` },
  adr001M: { label: "ADR-001M", path: `${ADR}001M-a-claim-is-a-pushed-branch-and-a-draft-pr.md` },
  adr001K: { label: "ADR-001K", path: `${ADR}001K-a-pr-merges-only-after-checks-on-the-combined-commit.md` },
  adr001E: { label: "ADR-001E", path: `${ADR}001E-a-spec-needs-fresh-context-review-of-the-exact-commit.md` },
  adr001H: { label: "ADR-001H", path: `${ADR}001H-done-requires-a-pushed-read-back-commit.md` },
  adr002P: { label: "ADR-002P", path: `${ADR}002P-no-session-holds-untrusted-input-secrets-and-outward-actions-together.md` },
  adr002W: { label: "ADR-002W", path: `${ADR}002W-three-strikes-then-stop.md` },
  adr002Z: { label: "ADR-002Z", path: `${ADR}002Z-three-orchestrators-split-the-work-by-risk.md` },
  adr003F: { label: "ADR-003F", path: `${ADR}003F-one-standing-campaign-approval-and-no-per-merge-gate.md` },
};
export const SOURCES = src;

// The sample piece of work the toy moves. It is an example, not a record.
export const SAMPLE = "Add a Glossary page to this site";

export const stages = [
  {
    id: "ask",
    name: "Ask",
    holder: "owner",
    line: "Kayden asks for a change and says why.",
    sources: [src.runbook, src.blueprint],
    next: { label: "Next: an agent reads it back", to: "readback" },
  },
  {
    id: "readback",
    name: "Read back",
    holder: "agent",
    line: "An agent writes the request down and reads it back: the idea, the direction, the cost, the reason and what will be made.",
    sources: [src.ddr000G, src.runbook],
    next: { label: "Next: Kayden confirms", to: "confirm" },
  },
  {
    id: "confirm",
    name: "Confirm",
    holder: "owner",
    line: "Kayden confirms what it means and approves the scope. Nothing is planned or built before this.",
    sources: [src.ddr000G, src.ddr000H],
    next: { label: "Next: write the Spec", to: "spec" },
  },
  {
    id: "spec",
    name: "Spec",
    holder: "agent",
    line: "An agent writes a Spec: one short plan for the change, with the checks that will prove it worked.",
    sources: [src.adr000P],
    next: { label: "Next: cut it into Tasks", to: "task" },
  },
  {
    id: "task",
    name: "Task",
    holder: "agent",
    line: "The Spec is cut into Tasks, each one small enough for a single agent run.",
    sources: [src.adr000Q, src.adr000R],
    next: { label: "Next: an agent claims a Task", to: "claim" },
  },
  {
    id: "claim",
    name: "Claim",
    holder: "agent",
    line: "An agent claims a Task by pushing its branch and opening a draft pull request, so no one else picks it up.",
    sources: [src.adr001M],
    next: { label: "Next: build it", to: "build" },
  },
  {
    id: "build",
    name: "Build",
    holder: "agent",
    line: "The agent writes tests that fail first, then the change that makes them pass.",
    sources: [src.agents],
    next: { label: "Next: run the checks", to: "check" },
  },
  {
    id: "check",
    name: "Check",
    holder: "agent",
    line: "The full set of checks runs on the combined commit. Proof, failures and limits are kept.",
    sources: [src.adr001K, src.runbook],
    next: { label: "Next: review", to: "review" },
  },
  {
    id: "review",
    name: "Review",
    holder: "agent",
    line: "A reviewer with fresh context checks the exact commit against the Spec.",
    sources: [src.adr001E],
    next: { label: "The review passes", to: "approve" },
    back: { label: "The review finds a problem", to: "returned" },
  },
  {
    id: "approve",
    name: "Approve",
    holder: "owner",
    line: "Kayden looks at the result and approves it, or sends it back saying what is wrong. For this site, only he moves work live.",
    sources: [src.ddr000F, src.ddr000H],
    next: { label: "Kayden approves", to: "done" },
    back: { label: "Kayden sends it back", to: "returned" },
  },
  {
    id: "returned",
    name: "Returned",
    holder: "returned",
    line: "The work goes back to the builder with what is wrong, and the next round starts from that answer. After three failed tries an agent stops and reports.",
    sources: [src.ddr000F, src.adr002W],
    next: { label: "Back to Build", to: "build" },
    branch: true,
  },
  {
    id: "done",
    name: "Done",
    holder: "done",
    line: "Merged. Done means the commit is pushed and read back, and the Task's receipt records the proof.",
    sources: [src.adr001H],
  },
];

// The main path, in order, without the returned loop.
export const mainPath = stages.filter((s) => !s.branch);
export const firstStage = stages[0];
export const lastStage = stages[stages.length - 1];
export const stageById = (id) => stages.find((s) => s.id === id) ?? firstStage;

// What the owner does beyond the lifecycle stages he holds.
export const ownerAlso = [
  { line: "Approves an improvement campaign once: its budget, round cap and stop rule. He does not approve every merge.", sources: [src.adr003F] },
];

// What agents do beyond the lifecycle stages they hold.
export const agentsAlso = [
  { line: "Merge work that is not deployed into main themselves, once checks pass.", sources: [src.ddr000H, src.adr003F] },
];

// The three orchestrators, all Claude, split by risk (ADR-002Z).
export const orchestrators = [
  { id: "A", name: "Website", does: "Builds this site; reaches the web host only by pushing to dev.", never: "Browses the web." },
  { id: "B", name: "Grill Board and RSI loop", does: "Runs the local Grill Board, the Python backend and the database keys on Kayden's own machine.", never: "Deploys anything." },
  { id: "C", name: "Coherence", does: "Checks the project stays true to its Specs, reviews Specs and does web research.", never: "Holds secrets or writes product code." },
];
