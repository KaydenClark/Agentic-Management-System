// The Quickstart's commands and the output each prints, in order: the one
// source the /quickstart page renders and tests/quickstart-replay.test.mjs
// replays on a fresh clone, so the page cannot show output the commands do
// not print. Plain JavaScript, typed by quickstart.d.mts. A step whose output
// is null shows none and is only required to succeed. exitCode (default 0) is
// the status the command must end with; the page shows a non-zero one.
// The output is what a reader's computer prints: one without Kayden's
// personal skill catalog in its home directory (the replay runs the commands
// with an empty HOME). If a replay fails
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
    exitCode: 1,
    output: [
      "blocking (1) - doctor exits 1 until repaired",
      "  personal-catalog-unavailable [blocks all, error]: Personal-catalog setup is incomplete; repair the stated discovery or ownership gap before selection or claims.",
      "informational (18) - reported only; nothing is blocked",
      "  legibility-undeclared [blocks none, attention]: workbench/manifest.json has no declared runtime surface for run, journey, measure; use workbench-layout.mjs declare-legibility to name commands, paths or pointers",
      "  permission-scope-drift [blocks none, error]: .claude/settings.json withholds declared lanes: docs (workbench/docs: no covering Edit allow rule); specs (workbench/specs: no covering Edit allow rule); wiki (workbench/wiki: no covering Edit allow rule); sessions (workbench/sessions: no covering Edit allow rule); feedback (workbench/feedback: no covering Edit allow rule)",
      "  skill-lane-missing [blocks none, error]: setup-workbench: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: map: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: plan: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: orchestrate: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: journey: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: jot: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: domain-modeling: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: grilling: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: code-review: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: pr: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: carry: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: reconcile: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: improve-workbench: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: evaluate-workbench: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: audit-workbench: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
      "  skill-lane-missing [blocks none, error]: author-skill: expected one personal source, found 0; make the catalog available to this host without copying it into the project.",
    ].join("\n"),
  },
];
