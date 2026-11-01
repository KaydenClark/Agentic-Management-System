// The /rsi page's data seam (S-007 TK-002). Turns S-006's rsi_runs and
// rsi_results rows into the page's series: per task and per version, held-out
// and dev apart, one series per arm, provider, model and effort, so a model
// change always starts a new series. Runs on the server only. It counts rows
// and compares counts; it computes no statistic (headlines with intervals
// are TK-003 and come from the loop's own method).
import { SERIES, type SeriesId, type SeriesPlan, type Split } from "./series";

export type Strength = "recorded_fact" | "anecdote" | "single_trial" | "repeated_trials" | "held_out_with_interval";
export type Arm = "ams" | "no_ams" | "plain_instructions";
export type ExecutionState = "completed" | "runner_error" | "auth_error" | "timeout" | "capped";

// Columns shared by a run and each of its results (the schema's composite
// foreign key keeps them equal).
interface Provenance {
  arm: Arm;
  provider: string;
  model: string;
  effort: string;
  runtime_commit: string;
  controls_commit: string;
  skills_commit: string;
  grader_version: string;
  source_kind: string;
  source_ref: string;
  source_url: string | null;
  strength: Strength;
  is_test: boolean;
  detail?: Readonly<Record<string, unknown>> | null; // S-002 row contract keys; any may be absent
}

export interface RsiRun extends Provenance {
  id: number;
  run_key: string;
  state: "running" | "completed" | "stopped" | "failed";
  started_at: string;
  finished_at: string | null;
}

export interface RsiResult extends Provenance {
  id: number;
  run_id: number;
  task_id: string;
  split: "dev" | "held_out";
  trial: number;
  execution_state: ExecutionState;
  passed: boolean | null;
  score: number | string | null;
  cost_usd: number | string;
  input_tokens: number;
  output_tokens: number;
  turns: number;
  wall_seconds: number | string;
}

export interface RsiData {
  runs: readonly RsiRun[];
  results: readonly RsiResult[];
}

export interface SystemVersion {
  id: string;
  runtime: string;
  controls: string;
  skills: string;
}

export type MarkKind = "regression" | "variant" | "removed" | "disposition" | "stop-rule" | "failed-run";

export interface Mark {
  kind: MarkKind;
  label: string;
  detail?: string;
}

// One rendered number and exactly the rows behind it.
export interface Count {
  key: "passed" | "not-graded";
  passed?: number;
  of: number;
  rows: readonly RsiResult[];
}

export interface Point {
  version: SystemVersion;
  rows: readonly RsiResult[];
  runs: readonly RsiRun[];
  counts: readonly Count[];
  marks: readonly Mark[];
  labels: readonly string[];
}

export interface Series {
  key: string;
  taskId: string | null;
  arm: Arm;
  provider: string;
  model: string;
  effort: string;
  points: readonly Point[];
}

export interface SeriesView extends SeriesPlan {
  series: readonly Series[];
  versions: readonly SystemVersion[];
  empty: boolean;
}

const SPLIT_OF: Record<RsiResult["split"], Split> = { dev: "dev", held_out: "held-out" };

const versionOf = (r: Provenance): SystemVersion => ({
  id: `${r.runtime_commit}.${r.controls_commit}.${r.skills_commit}`,
  runtime: r.runtime_commit,
  controls: r.controls_commit,
  skills: r.skills_commit,
});

const text = (v: unknown): string | undefined => (typeof v === "string" && v.trim() ? v.trim() : undefined);

// S-002's stop rules in plain words (detail.stop_rule on a stopped run).
export const STOP_RULE_TEXT: Readonly<Record<string, string>> = {
  three_strikes: "three strikes: the same failure came back after two fixes",
  paid_plan_requested: "a paid plan was requested, which needs the owner",
  meter_spent: "the owner's token meter is spent",
  owner_stop: "the owner stopped the loop",
};

const DISPOSITION_TEXT: Readonly<Record<string, string>> = {
  retain: "Retained: the round kept this change",
  revise: "Revised: the round sent this change back for revision",
};

// Reads rsi_runs.detail by the S-002 row contract. Every key is optional; a
// missing or mistyped key is absent, never an error.
function runMarks(runs: readonly RsiRun[]): Mark[] {
  const marks: Mark[] = [];
  const detail = (r: RsiRun): Readonly<Record<string, unknown>> => (r.detail && typeof r.detail === "object" ? r.detail : {});
  const dispositions = new Set(runs.map((r) => text(detail(r).disposition)).filter((d): d is string => !!d));
  if (runs.some((r) => detail(r).variant === true)) {
    marks.push({ kind: "variant", label: "Variant: tried beside the accepted line; it never advances it" });
  }
  if (dispositions.has("remove")) marks.push({ kind: "removed", label: "Removed version: the round took this change out" });
  for (const d of ["retain", "revise"]) if (dispositions.has(d)) marks.push({ kind: "disposition", label: DISPOSITION_TEXT[d] });
  const stopped = runs.filter((r) => r.state === "stopped");
  if (stopped.length > 0) {
    const parts = stopped.map((r) => {
      const code = text(detail(r).stop_rule);
      const rule = code ? STOP_RULE_TEXT[code] ?? code.replace(/_/g, " ") : "rule not recorded";
      const note = text(detail(r).stop_note);
      return note ? `${rule}. Note: ${note}` : rule;
    });
    marks.push({ kind: "stop-rule", label: "Stop rule fired", detail: [...new Set(parts)].join("; ") });
  }
  if (runs.some((r) => r.state === "failed")) marks.push({ kind: "failed-run", label: "Failed run: the run itself failed; this is not a stop rule" });
  return marks;
}

// The candidate version labels the loop gave this version's runs.
function versionLabels(runs: readonly RsiRun[]): string[] {
  return [...new Set(runs.map((r) => (r.detail && typeof r.detail === "object" ? text(r.detail.version) : undefined)).filter((v): v is string => !!v))];
}

function counts(rows: readonly RsiResult[]): Count[] {
  const graded = rows.filter((r) => r.passed !== null);
  const notGraded = rows.filter((r) => r.passed === null);
  const out: Count[] = [];
  if (graded.length) out.push({ key: "passed", passed: graded.filter((r) => r.passed === true).length, of: graded.length, rows: graded });
  if (notGraded.length) out.push({ key: "not-graded", of: notGraded.length, rows: notGraded });
  return out;
}

// A regression is a version whose share of passing graded trials is lower
// than the prior version's in the same series. Compared as whole counts
// (a/b < c/d as a*d < c*b); it is a recorded drop, not a significance test.
function passShareDrop(prev: Point, cur: Point): boolean {
  const p = prev.counts.find((c) => c.key === "passed");
  const c = cur.counts.find((k) => k.key === "passed");
  if (!p || !c) return false;
  return (c.passed ?? 0) * p.of < (p.passed ?? 0) * c.of;
}

export function seriesViews(data: RsiData): SeriesView[] {
  // Test and synthetic rows never reach the page, whatever the query did.
  const runs = new Map(data.runs.filter((r) => r.is_test === false).map((r) => [r.id, r]));
  const results = data.results.filter((r) => r.is_test === false && runs.has(r.run_id));

  return SERIES.map((plan) => {
    const rows = results.filter((r) => SPLIT_OF[r.split] === plan.split);

    // Versions in the order they first ran, so every series in a place
    // shares one x order.
    const firstRun = new Map<string, string>();
    for (const r of rows) {
      const v = versionOf(r).id;
      const at = runs.get(r.run_id)!.started_at;
      if (!firstRun.has(v) || at < firstRun.get(v)!) firstRun.set(v, at);
    }
    const versions = [...new Map(rows.map((r) => [versionOf(r).id, versionOf(r)])).values()].sort(
      (a, b) => firstRun.get(a.id)!.localeCompare(firstRun.get(b.id)!) || a.id.localeCompare(b.id),
    );
    const order = new Map(versions.map((v, i) => [v.id, i]));

    const groups = new Map<string, RsiResult[]>();
    for (const r of rows) {
      const key = [plan.view === "task" ? r.task_id : "", r.arm, r.provider, r.model, r.effort].join("\u0000");
      groups.set(key, [...(groups.get(key) ?? []), r]);
    }

    const series: Series[] = [...groups.entries()].map(([key, group]) => {
      const byVersion = new Map<string, RsiResult[]>();
      for (const r of group) byVersion.set(versionOf(r).id, [...(byVersion.get(versionOf(r).id) ?? []), r]);
      const points: Point[] = [];
      for (const [vid, vrows] of [...byVersion.entries()].sort((a, b) => order.get(a[0])! - order.get(b[0])!)) {
        const sorted = [...vrows].sort((a, b) => a.task_id.localeCompare(b.task_id) || a.run_id - b.run_id || a.trial - b.trial);
        const vruns = [...new Set(sorted.map((r) => r.run_id))].map((id) => runs.get(id)!);
        const point: Point = { version: versions[order.get(vid)!], rows: sorted, runs: vruns, counts: counts(sorted), marks: runMarks(vruns), labels: versionLabels(vruns) };
        const prev = points[points.length - 1];
        if (prev && passShareDrop(prev, point)) {
          point.marks = [{ kind: "regression", label: "Regression: fewer graded trials passed than on the prior version" }, ...point.marks];
        }
        points.push(point);
      }
      const head = group[0];
      return { key, taskId: plan.view === "task" ? head.task_id : null, arm: head.arm, provider: head.provider, model: head.model, effort: head.effort, points };
    });
    series.sort(
      (a, b) => order.get(a.points[0].version.id)! - order.get(b.points[0].version.id)! || (a.taskId ?? "").localeCompare(b.taskId ?? "") || a.key.localeCompare(b.key),
    );

    return { ...plan, series, versions, empty: series.length === 0 };
  });
}

export const emptyData: RsiData = { runs: [], results: [] };

export type { SeriesId };
