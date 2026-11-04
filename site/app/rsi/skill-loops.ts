// Skill trends on /rsi (S-007 TK-002J): one plotted point per skill per RSI
// loop, the Alignment Score of the version that loop kept, with its fitness
// level. Two halves:
//
// - LoopRecord is the stored shape of one loop for one skill. recordedLoops()
//   builds today's records from the safe summary of the shared-skill repair
//   round two (round-two-data.ts) plus the attempts it did not keep, below.
//   A later Task can feed the same shape from stored rows.
// - skillTrends() turns records into chart lines. It only arranges recorded
//   values: a new test contract or model starts a new line, the start point is
//   the version the loop started from, attempts not kept and High/Small runs
//   ride along as secondary marks and never become a point. The running
//   average is a plain mean of the points already drawn, for display only;
//   no statistic is computed here.
import { roundTwo, type ArmResult, type Run, type SkillResult } from "./round-two-data";

export type FitnessLevel = "Excellent" | "Stable" | "Functional" | "Broken";
export const FITNESS_LEVELS: readonly FitnessLevel[] = ["Excellent", "Stable", "Functional", "Broken"];

/** One assessed version: checks passed, pooled over the deciding runs. */
export interface Measured {
  version: string;
  passed: number;
  checks: number;
  level: FitnessLevel;
}

/** A High or Small tier run: a comparison only, never a deciding point. */
export interface SecondaryRun {
  tier: "High" | "Small";
  model: string;
  passed: number | null;
  checks: number;
  note?: string;
}

/** An improvement attempt the loop assessed and did not keep. */
export interface NotKeptAttempt extends Measured {
  attempt: number;
  why: string;
}

export interface LoopRecord {
  skill: string;
  /** 1 for the first loop recorded for this skill. */
  loop: number;
  /** The test contract the scores were measured under. */
  contract: string;
  /** The deciding tier and the exact model that ran it. */
  tier: string;
  model: string;
  /** The version the loop started from, measured in this loop. */
  start: Measured & { secondary: SecondaryRun[] };
  /** The version the loop kept. keptStart: no attempt was kept, so the start stands. */
  kept: Measured & { secondary: SecondaryRun[]; keptStart: boolean };
  notKept: NotKeptAttempt[];
  outcome: string;
  /** On-site anchor of the evidence behind the record. */
  evidence: string;
  /** Where the record comes from, in words. */
  source: string;
}

// Attempts round two assessed and did not keep, with their Mid-tier pooled
// scores, as recorded in the S-011 history (Resumed per-PR RSI round two).
// The charted candidate of a returned skill is added from round-two-data.ts.
export const NOT_KEPT_ATTEMPTS: Record<string, NotKeptAttempt[]> = {
  orchestrate: [
    { attempt: 1, version: "b61280d", passed: 27, checks: 27, level: "Excellent", why: "passed its trials but failed independent review" },
  ],
  handoff: [
    { attempt: 1, version: "96b9460", passed: 15, checks: 18, level: "Broken", why: "one run pushed an unrequested branch, and review failed" },
  ],
  land: [
    { attempt: 1, version: "5739c32", passed: 13, checks: 18, level: "Broken", why: "one run deleted uncontained work" },
    { attempt: 2, version: "fc1a080", passed: 16, checks: 18, level: "Broken", why: "review found three script defects" },
  ],
};

export const ROUND_TWO_SOURCE = `Shared-skill repair round two, recorded ${roundTwo.recorded} (S-011 history)`;

const LEVEL = new Set<string>(FITNESS_LEVELS);
function level(arm: ArmResult): FitnessLevel {
  if (!arm.level || !LEVEL.has(arm.level)) throw new Error(`no fitness level recorded for a ${arm.tier} arm`);
  return arm.level as FitnessLevel;
}

function pooled(version: string, arm: ArmResult): Measured {
  const [passed, checks] = (arm.pooled ?? "").split("/").map(Number);
  if (!Number.isInteger(passed) || !Number.isInteger(checks) || checks <= 0) throw new Error(`no pooled score recorded for ${version}`);
  return { version, passed, checks, level: level(arm) };
}

function secondary(arm: ArmResult): SecondaryRun[] {
  return arm.runs.map((r: Run) => ({ tier: arm.tier as SecondaryRun["tier"], model: arm.model, passed: r.passed, checks: r.checks, ...(arm.note ? { note: arm.note } : {}) }));
}

const contractId = (contract: string) => contract.split(",")[0].trim();

function fromRoundTwo(s: SkillResult): LoopRecord {
  const kept = s.disposition.kind !== "returned";
  const short = (sha: string) => sha.slice(0, 7);
  const start = { ...pooled(short(roundTwo.baselinePin), s.baseline.mid), secondary: [...secondary(s.baseline.high), ...secondary(s.baseline.small)] };
  const candidate = { ...pooled(short(s.candidate.sha), s.candidate.mid), secondary: [...secondary(s.candidate.high), ...secondary(s.candidate.small)] };
  const earlier = NOT_KEPT_ATTEMPTS[s.skill] ?? [];
  const notKept = kept
    ? earlier
    : [...earlier, { attempt: earlier.length + 1, version: candidate.version, passed: candidate.passed, checks: candidate.checks, level: candidate.level, why: "equal to the baseline; the stop rule ended qualification" }];
  return {
    skill: s.skill,
    loop: 1,
    contract: contractId(s.contract),
    tier: "Mid",
    model: s.baseline.mid.model,
    start,
    kept: kept ? { ...candidate, keptStart: false } : { ...start, keptStart: true },
    notKept,
    outcome: s.disposition.label,
    evidence: `#round-two-evidence-${s.skill}`,
    source: ROUND_TWO_SOURCE,
  };
}

/** Every loop recorded so far, one per charted skill: round two is loop 1. */
export function recordedLoops(): LoopRecord[] {
  return roundTwo.skills.map(fromRoundTwo);
}

/** Recorded, but measured another way or on hold: not charted. */
export const NOT_CHARTED = {
  length: roundTwo.pruning.skills,
  onHold: roundTwo.onHold.skill,
};

// ---- Chart lines -----------------------------------------------------------

export type BreakReason = "contract" | "model";

export interface TrendPoint {
  kind: "start" | "loop";
  /** The loop the point ends; 0 for the first start point. */
  loop: number;
  /** Horizontal place in loop units: a new line's start sits just after the loop it follows. */
  at: number;
  measured: Measured;
  /** Alignment Score as a share from 0 to 1. */
  score: number;
  keptStart: boolean;
  secondary: SecondaryRun[];
  /** Attempts in this loop that were not kept (loop points only). */
  notKept: NotKeptAttempt[];
  /** Plain mean of the line's last points up to this one; display only. */
  average: number;
  /** Lower than the line's previous point. */
  regression: boolean;
  evidence: string;
}

export interface TrendLine {
  contract: string;
  tier: string;
  model: string;
  /** Why this line starts a new line; empty for a skill's first line. */
  breaks: BreakReason[];
  points: TrendPoint[];
}

export interface SkillTrend {
  skill: string;
  lines: TrendLine[];
  /** The latest recorded loop. */
  loops: number;
  latest: TrendPoint;
  outcome: string;
  source: string;
}

/** Points averaged by the running-average line. */
export const AVERAGE_WINDOW = 10;
/** A line draws its running average once it has this many points. */
export const AVERAGE_FROM = 3;
/** Where a new line's start sits after the loop it follows, in loop units. */
export const RESTART_OFFSET = 0.4;

const share = (m: Measured) => m.passed / m.checks;

export function skillTrends(records: readonly LoopRecord[]): SkillTrend[] {
  const bySkill = new Map<string, LoopRecord[]>();
  for (const r of records) bySkill.set(r.skill, [...(bySkill.get(r.skill) ?? []), r]);
  return [...bySkill].map(([skill, list]) => {
    const loops = [...list].sort((a, b) => a.loop - b.loop);
    loops.forEach((r, i) => {
      if (i > 0 && r.loop === loops[i - 1].loop) throw new Error(`${skill}: loop ${r.loop} is recorded twice`);
      if (r.loop < 1 || !Number.isInteger(r.loop)) throw new Error(`${skill}: loop ${r.loop} is not a loop number`);
    });
    const lines: TrendLine[] = [];
    const point = (line: TrendLine, p: Omit<TrendPoint, "score" | "average" | "regression">): TrendPoint => {
      const prior = line.points.slice(-(AVERAGE_WINDOW - 1));
      const score = share(p.measured);
      const window = [...prior.map((q) => q.score), score];
      const last = line.points.at(-1);
      return { ...p, score, average: window.reduce((a, b) => a + b, 0) / window.length, regression: last ? score < last.score : false };
    };
    for (const r of loops) {
      let line = lines.at(-1);
      const breaks: BreakReason[] = [];
      if (line && line.contract !== r.contract) breaks.push("contract");
      if (line && line.model !== r.model) breaks.push("model");
      if (!line || breaks.length > 0) {
        line = { contract: r.contract, tier: r.tier, model: r.model, breaks, points: [] };
        lines.push(line);
        const at = r.loop - 1 + (breaks.length > 0 ? RESTART_OFFSET : 0);
        line.points.push(point(line, { kind: "start", loop: r.loop - 1, at, measured: r.start, keptStart: false, secondary: r.start.secondary, notKept: [], evidence: r.evidence }));
      }
      const { secondary: sec, keptStart, ...measured } = r.kept;
      line.points.push(point(line, { kind: "loop", loop: r.loop, at: r.loop, measured, keptStart, secondary: sec, notKept: r.notKept, evidence: r.evidence }));
    }
    const last = loops.at(-1)!;
    return { skill, lines, loops: last.loop, latest: lines.at(-1)!.points.at(-1)!, outcome: last.outcome, source: last.source };
  });
}
