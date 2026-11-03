// Safe snapshot of published AMS records. Private packets and skill text stay private.
// These trial predicates are development observations, never r1 audit scores.
const record = "https://github.com/KaydenClark/Agentic-Management-System/blob/b059a6a08db8876e17c426764f8e6acbbca0632c/workbench";
const comparison = `${record}/research/IMPROVEMENT-shared-skills-delivery-2026-11-02.md`;
const documentation = `${record}/feedback/REPORT-runbook-target-failure-2026-11-02.md`;
const firstAttempt = "https://github.com/KaydenClark/Agentic-Management-System/blob/dcad9c47d572e7ed51d2a1a6db50b3c1cbce45d8/workbench/feedback/REPORT-shared-skills-attempt-1-2026-11-02.md";
const pruningAttempt = `${firstAttempt}#separate-pruning-skill-suite`;
const checkerReport = "https://github.com/KaydenClark/Agentic-Management-System/blob/e8450d2277b97d9c6b891ffd19fbcfb25b4be480/workbench/feedback/coherence/CHECKER-REPAIR-2026-11-02.md";
const checkerRecord = "https://github.com/KaydenClark/Agentic-Management-System/blob/e8450d2277b97d9c6b891ffd19fbcfb25b4be480/workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/tasks/TK-001V/TASK.md";

export const repairEvidence = {
  checker: {
    source: checkerRecord,
    report: checkerReport,
    baseline: "408e851e5ec621bd00f32e9a382df8d9a06b505e",
    baselineSource: "https://github.com/KaydenClark/Agentic-Management-System/blob/408e851e5ec621bd00f32e9a382df8d9a06b505e/src/ams/coherence/up_to_spec.py",
    candidate: "7735c553bbe2cde0e5c5d6a26a56e7468773961b",
    candidateSource: "https://github.com/KaydenClark/Agentic-Management-System/blob/7735c553bbe2cde0e5c5d6a26a56e7468773961b/src/ams/coherence/up_to_spec.py",
    fixture: "ce9d9b71ef3709eddfc8fd615fe7280668e9f006",
    fixtureSource: checkerReport,
  },
  baseline: {
    skillsCommit: "fb7ad23c963e183b930b23bc5fdf4d309dff292a",
    model: "gpt-6.1-terra",
    configurationSource: `${firstAttempt}#later-trace-readback-same-attempt-original-ledgers-retained`,
    source: comparison,
    runs: [9, 10, 10].map((passed, i) => ({ id: `baseline-${i + 1}`, label: `Run ${i + 1}`, passed, checks: 11, source: comparison })),
  },
  candidate: {
    skillsCommit: "6f84573de47cbc7675876777e22e903ecd4783d1",
    source: firstAttempt,
    runs: [9, 8, 7].map((passed, i) => ({ id: `candidate-${i + 1}`, label: `Run ${i + 1}`, passed, checks: 11, source: firstAttempt })),
    audit: { level: "Broken", passed: 11, applicable: 78, qualification: "unqualified", source: firstAttempt },
  },
  pruning: {
    source: pruningAttempt,
    observations: [
      { label: "RUNBOOK exercise", before: 2983, after: 2897, note: "Target unmet; linked project sources were absent from the fixture." },
      { label: "Independent skill pruning", before: 1142, after: 1065, note: "Independent pruning and author walkthroughs occurred; semantic completeness remains unverified." },
      { label: "Shipment artifact", before: 793, after: 708, note: "Approximate goal missed despite staying under its ceiling." },
      { label: "Note without a target", before: 343, after: 218, note: "No target or ceiling was invented." },
    ],
    audit: { level: "Broken", passed: 6, applicable: 51 },
  },
  documentation: {
    source: documentation,
    observations: [
      { label: "Original", characters: 2983, source: "https://github.com/KaydenClark/Agentic-Management-System/blob/da27cc79474622613b75147b8c654e2961be100b/RUNBOOK.md" },
      { label: "First edit", characters: 3336, source: documentation },
      { label: "First reduction", characters: 3116, source: documentation },
      { label: "Resumed reduction", characters: 3036, source: documentation },
      { label: "Repeated failure", characters: 3025, source: documentation },
      { label: "Goal recovered", characters: 1193, source: "https://github.com/KaydenClark/Agentic-Management-System/blob/b059a6a08db8876e17c426764f8e6acbbca0632c/RUNBOOK.md" },
    ],
  },
};
