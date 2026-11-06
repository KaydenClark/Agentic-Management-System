// Safe snapshot of published AMS records. Private packets and skill text stay private.
// These trial predicates are development observations, never r1 audit scores.
// Source identities remain metadata; visitor links resolve to the summaries below.
const comparison = "#workflow-comparison-data";
const documentation = "#documentation-evidence";
const firstAttempt = "#candidate-evidence";
const pruningAttempt = "#pruning-evidence";
const checkerReport = "#checker-evidence";
const checkerRecord = "#checker-evidence";

export const repairEvidence = {
  snapshotDate: "2026-11-02",
  comparisonRecord: "IMPROVEMENT-shared-skills-delivery-2026-11-02.md @ b059a6a",
  candidateRecord: "REPORT-shared-skills-attempt-1-2026-11-02.md @ dcad9c4",
  checker: {
    reportRevision: "1c9516722a22157e1f78d2eccd9d445f5ae2018e",
    source: checkerRecord,
    report: checkerReport,
    baseline: "408e851e5ec621bd00f32e9a382df8d9a06b505e",
    baselineSource: "#checker-evidence",
    candidate: "7735c553bbe2cde0e5c5d6a26a56e7468773961b",
    candidateSource: "#checker-evidence",
    fixture: "ce9d9b71ef3709eddfc8fd615fe7280668e9f006",
    fixtureSource: checkerReport,
    assembly: "e882efe9d905f074a0b36bff8976e49da03cc028",
    assemblySource: "#checker-evidence",
  },
  baseline: {
    skillsCommit: "fb7ad23c963e183b930b23bc5fdf4d309dff292a",
    model: "gpt-6.1-terra",
    configurationSource: firstAttempt,
    source: comparison,
    runs: [9, 10, 10].map((passed, i) => ({ id: `baseline-${i + 1}`, label: `Run ${i + 1}`, passed, checks: 11, source: comparison })),
  },
  candidate: {
    skillsCommit: "6f84573de47cbc7675876777e22e903ecd4783d1",
    source: firstAttempt,
    runs: [9, 8, 7].map((passed, i) => ({ id: `candidate-${i + 1}`, label: `Run ${i + 1}`, passed, checks: 11, source: comparison })),
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
      { label: "Original", characters: 2983, source: "#documentation-evidence" },
      { label: "First edit", characters: 3336, source: documentation },
      { label: "First reduction", characters: 3116, source: documentation },
      { label: "Resumed reduction", characters: 3036, source: documentation },
      { label: "Repeated failure", characters: 3025, source: documentation },
      { label: "Goal recovered", characters: 1193, source: "#documentation-evidence" },
    ],
  },
};
