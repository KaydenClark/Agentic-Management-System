// The skills diagram on /start (screen 3): Kayden's skills grouped by the
// Workbench stage they serve, from his chart of 2026-11-01. Each stage lists
// its main-flow skills in the order they run, then the skills also used at
// that stage. Rendered by page.tsx and checked by tests/start-flow.test.mjs.
// Plain JavaScript so the tests import it on any Node; types in skills.d.mts.

export const stages = [
  {
    id: "route",
    name: "Route",
    gloss: "Choose a path",
    main: ["ask-workbench"],
    used: ["sitrep", "triage", "handoff", "setup-workbench"],
  },
  {
    id: "align",
    name: "Align",
    gloss: "Shared concept",
    main: ["grilling", "readback"],
    used: ["brainstorm", "grill-me", "grill-with-docs", "oracle", "wayfinder", "prototype", "explore-kb", "research", "domain-modeling", "jot"],
  },
  {
    id: "prepare",
    name: "Prepare",
    gloss: "Map and Plan",
    main: ["map", "plan"],
    used: [],
  },
  {
    id: "journey",
    name: "Journey",
    gloss: "Build each Task",
    main: ["carry", "orchestrate", "journey"],
    used: ["tdd", "diagnosing-bugs", "codebase-design", "pr"],
  },
  {
    id: "judge",
    name: "Judge",
    gloss: "Review, verify",
    main: ["code-review"],
    used: [],
    note: "Findings become a new Journey.",
  },
  {
    id: "complete",
    name: "Complete",
    gloss: "Land, preserve",
    main: ["land", "reconcile"],
    used: ["resolving-merge-conflicts", "promote"],
  },
  {
    id: "improve",
    name: "Improve",
    gloss: "Learn and fix",
    main: ["retro", "improve-workbench"],
    used: ["audit-workbench", "evaluate-workbench", "diagnose-and-propose", "author-skill", "writing-for-agents", "improve-codebase-architecture"],
    note: "Improvements kept after a fresh rerun feed the next loop, back to Route.",
  },
];

// The committed records the diagram's claims come from (paths from the
// repository root).
export const sources = [
  { label: "Skills by stage (Kayden's chart)", path: "workbench/landmarks/LMK-003-ams-website/specs/S-008-skills-wiki/skills-by-workbench-stage.svg" },
  { label: "Workbench skills", path: "workbench/docs/SKILLS.md" },
  { label: "Runbook", path: "RUNBOOK.md" },
];
