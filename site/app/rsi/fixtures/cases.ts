// Labeled render-test fixtures for /rsi (S-007 TK-002). FIXTURE DATA ONLY:
// these rows are invented to exercise the page and are never shown on the
// site; the page itself imports none of them. Every value is shaped like a
// row of S-006's rsi_runs and rsi_results tables
// (supabase/migrations/20261101134221_rsi_rows.sql).
import type { RsiData, RsiResult, RsiRun } from "../data";

const commit = (c: string) => c.repeat(40).slice(0, 40);

export const V1 = { runtime_commit: commit("a1"), controls_commit: commit("b1"), skills_commit: commit("c1") };
export const V2 = { runtime_commit: commit("a2"), controls_commit: commit("b2"), skills_commit: commit("c2") };
export const V3 = { runtime_commit: commit("a3"), controls_commit: commit("b3"), skills_commit: commit("c3") };

type Version = typeof V1;

interface RunSpec {
  id: number;
  version: Version;
  model?: string;
  provider?: string;
  effort?: string;
  arm?: RsiRun["arm"];
  state?: RsiRun["state"];
  started: string;
  is_test?: boolean;
  detail?: Record<string, unknown>;
}

export function run(s: RunSpec): RsiRun {
  return {
    id: s.id,
    run_key: `fixture-run-${s.id}`,
    arm: s.arm ?? "ams",
    provider: s.provider ?? "fixture-provider",
    model: s.model ?? "fixture-model-a",
    effort: s.effort ?? "high",
    ...s.version,
    grader_version: commit("d0"),
    state: s.state ?? "completed",
    started_at: s.started,
    finished_at: s.state === "running" ? null : s.started,
    source_kind: "path",
    source_ref: `fixture/runs/${s.id}.json`,
    source_url: `https://github.com/KaydenClark/Agentic-Management-System/blob/main/fixture/runs/${s.id}.json`,
    strength: "single_trial",
    is_test: s.is_test ?? false,
    detail: s.detail ?? {},
  };
}

let nextResultId = 1000;

export function results(r: RsiRun, taskId: string, split: RsiResult["split"], passes: (boolean | null)[], over: Partial<RsiResult> = {}): RsiResult[] {
  return passes.map((passed, i) => ({
    id: nextResultId++,
    run_id: r.id,
    arm: r.arm,
    provider: r.provider,
    model: r.model,
    effort: r.effort,
    runtime_commit: r.runtime_commit,
    controls_commit: r.controls_commit,
    skills_commit: r.skills_commit,
    grader_version: r.grader_version,
    task_id: taskId,
    split,
    trial: i + 1,
    execution_state: passed === null ? "runner_error" : "completed",
    passed,
    score: null,
    cost_usd: 0.25,
    input_tokens: 1200,
    output_tokens: 300,
    turns: 4,
    wall_seconds: 61.5,
    source_kind: "path",
    source_ref: `fixture/results/${r.id}/${taskId}/${i + 1}.json`,
    source_url: null,
    strength: r.strength,
    is_test: r.is_test,
    detail: {},
    ...over,
  }));
}

// Empty: no rows at all, the state of the live tables today.
export const emptyCase: RsiData = { runs: [], results: [] };

// Link coverage: several tasks, versions and an ungraded trial, so the page
// renders pass counts and not-graded counts in both views.
const lc1 = run({ id: 1, version: V1, started: "2026-11-01T10:00:00Z" });
const lc2 = run({ id: 2, version: V2, started: "2026-11-02T10:00:00Z" });
export const linkCoverageCase: RsiData = {
  runs: [lc1, lc2],
  results: [
    ...results(lc1, "fixture-task-alpha", "dev", [true, false, null]),
    ...results(lc1, "fixture-task-beta", "held_out", [true, true]),
    ...results(lc2, "fixture-task-alpha", "dev", [true, true, true]),
    ...results(lc2, "fixture-task-beta", "held_out", [false, true]),
  ],
};

// Model change: the same task and arm, version two runs a different model.
// It must render as two series, never one line.
const mc1 = run({ id: 11, version: V1, model: "fixture-model-a", started: "2026-11-01T10:00:00Z" });
const mc2 = run({ id: 12, version: V2, model: "fixture-model-b", started: "2026-11-02T10:00:00Z" });
export const modelChangeCase: RsiData = {
  runs: [mc1, mc2],
  results: [...results(mc1, "fixture-task-gamma", "dev", [true, true]), ...results(mc2, "fixture-task-gamma", "dev", [true, false])],
};

// Regression: same model, version two passes fewer trials than version one.
const rg1 = run({ id: 21, version: V1, started: "2026-11-01T10:00:00Z" });
const rg2 = run({ id: 22, version: V2, started: "2026-11-02T10:00:00Z" });
export const regressionCase: RsiData = {
  runs: [rg1, rg2],
  results: [...results(rg1, "fixture-task-delta", "dev", [true, true, true]), ...results(rg2, "fixture-task-delta", "dev", [true, false, false])],
};

// Variant, removed version and a fired stop rule, as the loop records them on
// its run rows: a disposition in detail and a stopped state.
const dp1 = run({ id: 31, version: V1, started: "2026-11-01T10:00:00Z", detail: { disposition: "variant" } });
const dp2 = run({ id: 32, version: V2, started: "2026-11-02T10:00:00Z", detail: { disposition: "remove" } });
const dp3 = run({ id: 33, version: V3, started: "2026-11-03T10:00:00Z", state: "stopped", detail: { stop_rule: "three strikes" } });
export const dispositionCase: RsiData = {
  runs: [dp1, dp2, dp3],
  results: [
    ...results(dp1, "fixture-task-epsilon", "dev", [true]),
    ...results(dp2, "fixture-task-epsilon", "dev", [true]),
    ...results(dp3, "fixture-task-epsilon", "dev", [false]),
  ],
};

// Test rows: a marked test run and its marked test results beside one real
// row (the schema's foreign key keeps a result's is_test equal to its run's).
// No test row may render; the marker strings must not appear anywhere.
export const TEST_ROW_MARKER = "fixture-test-row-marker";
const tr1 = run({ id: 41, version: V1, started: "2026-11-01T10:00:00Z" });
const trTest = run({ id: 42, version: V2, started: "2026-11-02T10:00:00Z", is_test: true, model: `${TEST_ROW_MARKER}-model` });
export const testRowCase: RsiData = {
  runs: [tr1, trTest],
  results: [
    ...results(tr1, "fixture-task-zeta", "dev", [true]),
    ...results(trTest, `${TEST_ROW_MARKER}-task`, "dev", [false]),
    ...results(trTest, `${TEST_ROW_MARKER}-task-two`, "held_out", [true]),
  ],
};
