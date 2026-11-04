// Labeled render-test fixture for the /rsi skill trends (S-007 TK-002J).
// FIXTURE DATA ONLY: these loops are invented to exercise the chart and are
// never shown on the site; the page imports none of them. One fixture skill
// runs six loops that cover a test contract change, a model change, an
// attempt not kept that scored higher than the kept version, High and Small
// runs that scored differently from the deciding tier, and a regression.
import type { LoopRecord, Measured, SecondaryRun } from "../skill-loops";

export const FIXTURE_SKILL = "fixture-skill";
const MODEL_A = "fixture-model-a";
const MODEL_B = "fixture-model-b";

const m = (version: string, passed: number, level: Measured["level"], checks = 20): Measured => ({ version, passed, checks, level });
const runs = (high: number | null, small: number | null, checks = 20): SecondaryRun[] => [
  { tier: "High", model: "fixture-high-model", passed: high, checks },
  { tier: "Small", model: "fixture-small-model", passed: small, checks },
];

function loop(n: number, contract: string, model: string, start: Measured, kept: Measured | null, extra: Partial<LoopRecord> = {}): LoopRecord {
  return {
    skill: FIXTURE_SKILL,
    loop: n,
    contract,
    tier: "Mid",
    model,
    start: { ...start, secondary: runs(20, 4) },
    kept: kept ? { ...kept, secondary: runs(20, 20), keptStart: false } : { ...start, secondary: runs(20, 4), keptStart: true },
    notKept: [],
    outcome: "fixture outcome",
    evidence: "#fixture-evidence",
    source: "fixture",
    ...extra,
  };
}

export const multiLoopFixture: LoopRecord[] = [
  loop(1, "fx-v1", MODEL_A, m("fx0001", 10, "Broken"), m("fx0002", 14, "Functional")),
  // A rejected attempt scored 20 of 20; the kept version decides the point.
  loop(2, "fx-v1", MODEL_A, m("fx0002", 14, "Functional"), m("fx0003", 17, "Stable"), {
    notKept: [{ attempt: 1, version: "fx0003r", passed: 20, checks: 20, level: "Excellent", why: "fixture rejection" }],
  }),
  // A regression: the kept version scored lower than the loop before.
  loop(3, "fx-v1", MODEL_A, m("fx0003", 17, "Stable"), m("fx0004", 12, "Broken")),
  // A new test contract: a new line starts from the version re-measured.
  loop(4, "fx-v2", MODEL_A, m("fx0004", 8, "Broken"), m("fx0005", 15, "Functional")),
  // No candidate kept: the loop keeps its start score.
  loop(5, "fx-v2", MODEL_A, m("fx0005", 15, "Functional"), null, {
    notKept: [{ attempt: 1, version: "fx0006r", passed: 11, checks: 20, level: "Broken", why: "fixture rejection" }],
  }),
  // A new model: another new line.
  loop(6, "fx-v2", MODEL_B, m("fx0005", 16, "Stable"), m("fx0007", 20, "Excellent")),
];
