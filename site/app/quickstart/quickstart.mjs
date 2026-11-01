// The Quickstart's commands and the output each prints, in order: the one
// source the /quickstart page renders and tests/quickstart-replay.test.mjs
// replays on a fresh clone, so the page cannot show output the commands do
// not print. Plain JavaScript, typed by quickstart.d.mts. A step whose output
// is null shows none and is only required to succeed. If a replay fails
// because the room's state changed, update `output` here from
// `node tests/quickstart-replay.mjs`, and the page's words if they no longer fit.

export const CLONE_URL = "https://github.com/KaydenClark/Agentic-Management-System.git";
export const REPO_DIR = "Agentic-Management-System";

export const steps = [
  {
    id: "clone",
    command: `git clone ${CLONE_URL}`,
    output: null,
  },
  {
    id: "cd",
    command: `cd ${REPO_DIR}`,
    output: null,
  },
  {
    id: "doctor",
    command: "node workbench/tools/spec-workbench.mjs doctor",
    output: [
      "informational (2) - reported only; nothing is blocked",
      "  legibility-undeclared [blocks none, attention]: workbench/manifest.json has no declared runtime surface for run, journey, measure; use workbench-layout.mjs declare-legibility to name commands, paths or pointers",
      "  permission-scope-drift [blocks none, error]: .claude/settings.json withholds declared lanes: docs (workbench/docs: no covering Edit allow rule); specs (workbench/specs: no covering Edit allow rule); wiki (workbench/wiki: no covering Edit allow rule); sessions (workbench/sessions: no covering Edit allow rule); feedback (workbench/feedback: no covering Edit allow rule)",
      "ok - no blocking finding; attention and slice findings above stay visible",
    ].join("\n"),
  },
];
