// Safe summary of the S-011 shared-skill repair, round two (2026-11-03).
// Results, identities and limits only: private prompts, transcripts, fixture
// contents and skill source text stay private. Mid tier decides; High and
// Small ran once each as non-gating comparisons; Frontier judged and reviewed.
// Model roles follow ADR-003K tiers, with the exact model that ran as evidence.

export type Tier = "Frontier" | "High" | "Mid" | "Small";
export type Run = { id: string; passed: number | null; checks: number; pass: boolean | null };
export type ArmResult = { tier: Exclude<Tier, "Frontier">; model: string; level: string | null; pooled: string | null; runs: Run[]; note?: string };
export type Disposition = { kind: "merged" | "owner-merge" | "returned"; label: string; detail: string };
export type SkillResult = {
  skill: string;
  pr: number;
  failure: string;
  explanation: string;
  contract: string;
  baseline: { mid: ArmResult; high: ArmResult; small: ArmResult };
  candidate: { sha: string; attempts?: string; mid: ArmResult; high: ArmResult; small: ArmResult };
  review: string;
  disposition: Disposition;
  mainCommit: string | null;
};

export const MODELS = {
  Frontier: "claude-fable-5-1",
  High: "claude-opus-5-5",
  Mid: "claude-sonnet-5-5",
  Small: "claude-haiku-5-5",
} as const;

// "4/5" -> a run; "ungraded" -> a run with no count and no grade.
function run(id: string, result: string, pass: boolean | null, checks: number): Run {
  if (result === "ungraded") return { id, passed: null, checks, pass: null };
  const [passed] = result.split("/").map(Number);
  return { id, passed, checks, pass };
}

function arm(tier: ArmResult["tier"], checks: number, runs: [string, string, boolean | null][], level: string | null = null, pooled: string | null = null, note?: string): ArmResult {
  return { tier, model: MODELS[tier], level, pooled, runs: runs.map(([id, r, p]) => run(id, r, p, checks)), ...(note ? { note } : {}) };
}

export const roundTwo = {
  recorded: "2026-11-03",
  harness: "Claude Code 2.1.310, with isolated workers: no personal skill catalog, project instruction files, MCP servers or web tools",
  baselinePin: "fb7ad23c963e183b930b23bc5fdf4d309dff292a",
  contracts: [
    { id: "v1", sha256: "197858fec1e23882857684d67e847a20566a38232f662412621ebe68d382ec8d", status: "Non-qualifying: the unmodified baseline already scored Excellent for seven of eight skills." },
    { id: "v2", sha256: "bf493e93b4e9e0426a2cf1af2c9867215bf3ac73be4ebc498c9f740868267e3b", status: "Reproductions of owner-found failures; qualifying where the baseline reproduced the failure." },
  ],
  tiers: [
    { tier: "Mid" as Tier, role: "Deciding trials: three baseline and three candidate runs per skill", model: MODELS.Mid },
    { tier: "High" as Tier, role: "Comparison only, one baseline and one candidate run, not gating", model: MODELS.High },
    { tier: "Small" as Tier, role: "Comparison only, one baseline and one candidate run, not gating", model: MODELS.Small },
    { tier: "Frontier" as Tier, role: "Judge for checks that need judgment, and independent review", model: MODELS.Frontier },
  ],
  judgeLimits: "The Frontier judge is unqualified on the Quality rows HO-07 and PR-08 (v1) and HO2-05 and SW2-05 (v2).",
  skills: [
    {
      skill: "setup-workbench",
      pr: 63,
      failure: "Adoption kept a CONTINUE-style continuation pointer and never raised it",
      explanation: "When it adopted an existing project, the skill carried an old continuation-pointer file forward and never asked the owner about it. The reproduced check failed in all three baseline runs and passed in all three candidate runs.",
      contract: "v2",
      baseline: {
        mid: arm("Mid", 5, [["mid-b1", "4/5", false], ["mid-b2", "4/5", false], ["mid-b3", "4/5", false]], "Broken", "12/15"),
        high: arm("High", 5, [["high-b1", "ungraded", null]], null, null, "grader error, kept as an evidence gap"),
        small: arm("Small", 5, [["small-b1", "4/5", false]]),
      },
      candidate: {
        sha: "378658d1b2a7ba276202e4d0058a794a1a25185a",
        mid: arm("Mid", 5, [["mid-c1", "5/5", true], ["mid-c2", "5/5", true], ["mid-c3", "4/5", true]], "Excellent", "14/15"),
        high: arm("High", 5, [["high-c1", "5/5", true]]),
        small: arm("Small", 5, [["small-c1", "0/5", false]], null, null, "no activity in the run"),
      },
      review: "PASS WITH NOTES",
      disposition: { kind: "merged", label: "Merged", detail: "Broken to Excellent at the Mid tier; merged into the shared skills main branch." },
      mainCommit: "8dc3b636e039a13434f0ddf5f4403f7402683982",
    },
    {
      skill: "orchestrate",
      pr: 62,
      failure: "One Spec's work scattered across many per-Task branches",
      explanation: "One Spec's work was spread over a separate branch per Task instead of one Feature branch. The v2 reproduction did not reproduce, so the qualifying test is the first contract's one-branch check, which failed in one of three baseline runs and passed in all three candidate runs.",
      contract: "v1, where its failure reproduced",
      baseline: {
        mid: arm("Mid", 9, [["mid-b1", "9/9", true], ["mid-b2", "9/9", true], ["mid-b3", "8/9", false]], "Broken", "26/27"),
        high: arm("High", 9, [["high-b1", "9/9", true]]),
        small: arm("Small", 9, [["small-b1", "9/9", true]]),
      },
      candidate: {
        sha: "aebb3098f0f119e15b1ca773b7bf2a96aba54d6c",
        attempts: "The first candidate b61280d passed its trials but failed review: its description was stripped, a branch convention was hardcoded and duties were dropped.",
        mid: arm("Mid", 9, [["mid-c1-a2", "9/9", true], ["mid-c2-a2", "9/9", true], ["mid-c3-a2", "9/9", true]], "Excellent", "27/27"),
        high: arm("High", 9, [["high-c1-a2", "9/9", true]]),
        small: arm("Small", 9, [["small-c1-a2", "9/9", true]]),
      },
      review: "PASS WITH NOTES",
      disposition: { kind: "merged", label: "Merged", detail: "Broken to Excellent at the Mid tier; merged into the shared skills main branch." },
      mainCommit: "1e41c87",
    },
    {
      skill: "handoff",
      pr: 59,
      failure: "Handoff committed and pushed instead of kept local and ignored",
      explanation: "Asked for a handoff, agents committed and pushed the handoff note instead of keeping it as a local, ignored file. That happened in every baseline run and in no candidate run.",
      contract: "v2",
      baseline: {
        mid: arm("Mid", 6, [["mid-b1", "1/6", false], ["mid-b2", "1/6", false], ["mid-b3", "1/6", false]], "Broken", "3/18"),
        high: arm("High", 6, [["high-b1", "1/6", false]]),
        small: arm("Small", 6, [["small-b1", "1/6", false]]),
      },
      candidate: {
        sha: "28749fb7793ac9dacb948dce72b634ba540a7bd1",
        attempts: "Attempt 1, 96b9460, was Broken 15 of 18: one run pushed an unrequested branch, and review failed.",
        mid: arm("Mid", 6, [["mid-c1-a2", "6/6", true], ["mid-c2-a2", "6/6", true], ["mid-c3-a2", "6/6", true]], "Excellent", "18/18"),
        high: arm("High", 6, [["high-c1-a2", "6/6", true]]),
        small: arm("Small", 6, [["small-c1-a2", "6/6", true]]),
      },
      review: "PASS WITH NOTES",
      disposition: { kind: "merged", label: "Merged", detail: "Broken to Excellent at the Mid tier; merged into the shared skills main branch." },
      mainCommit: "2c2dfef",
    },
    {
      skill: "journey",
      pr: 60,
      failure: "Harness branch prefix and false completion (not reproduced on Claude Mid)",
      explanation: "The recorded failures were a harness-specific branch prefix and a claim of completion with work left unpushed. Neither failure reproduced at the Mid tier, so this is a regression check only: the candidate matched the baseline.",
      contract: "v1, regression check only",
      baseline: {
        mid: arm("Mid", 10, [["mid-b1", "10/10", true], ["mid-b2", "10/10", true], ["mid-b3", "10/10", true]], "Excellent", "30/30"),
        high: arm("High", 10, [["high-b1", "10/10", true]]),
        small: arm("Small", 10, [["small-b1", "10/10", true]]),
      },
      candidate: {
        sha: "2567c74328cbe2eb9a8e9bfa9fde7b57c4dab315",
        attempts: "The first review failed; the re-review passed with notes.",
        mid: arm("Mid", 10, [["mid-c1-a2", "10/10", true], ["mid-c2-a2", "10/10", true], ["mid-c3-a2", "10/10", true]], "Excellent", "30/30"),
        high: arm("High", 10, [["high-c1-a2", "10/10", true]]),
        small: arm("Small", 10, [["small-c1-a2", "10/10", true]]),
      },
      review: "PASS WITH NOTES, after an earlier FAIL",
      disposition: { kind: "owner-merge", label: "Merged on owner decision", detail: "No regression: Excellent before and after. The owner chose to merge it; because the failures did not reproduce, it is not a proven fix." },
      mainCommit: "03fcdb2",
    },
    {
      skill: "land",
      pr: 61,
      failure: "Asked to clean up scattered Spec branches, agents renamed or kept them instead of consolidating",
      explanation: "Asked to clean up a Spec's scattered branches, agents renamed or kept them instead of consolidating them onto one branch. The third candidate scored equal to the baseline; two Mid runs never used the consolidation path. The likely gap is selection: the request does not name the skill, so workers treat it as a rename.",
      contract: "v2",
      baseline: {
        mid: arm("Mid", 6, [["mid-b1", "5/6", false], ["mid-b2", "6/6", true], ["mid-b3", "5/6", false]], "Broken", "16/18"),
        high: arm("High", 6, [["high-b1", "4/6", false]]),
        small: arm("Small", 6, [["small-b1", "4/6", false]]),
      },
      candidate: {
        sha: "9eca0b3c81b8a6d0c5e649e5259a2a3cc648a8b7",
        attempts: "Attempt 1 was Broken 13 of 18, and one run deleted uncontained work. Attempt 2 was Broken 16 of 18, and review found three script defects. Attempt 3, charted here, was Broken 16 of 18, equal to the baseline.",
        mid: arm("Mid", 6, [["mid-c1-a3", "6/6", true], ["mid-c2-a3", "5/6", false], ["mid-c3-a3", "5/6", false]], "Broken", "16/18"),
        high: arm("High", 6, [["high-c1-a3", "0/6", false]]),
        small: arm("Small", 6, [["small-c1-a3", "4/6", false]]),
      },
      review: "PASS WITH NOTES, script safe",
      disposition: { kind: "returned", label: "Not merged", detail: "Returned to the owner after three attempts: the third candidate was equal to the baseline, and the stop rule ends qualification there." },
      mainCommit: null,
    },
  ] satisfies SkillResult[],
  // Development observations: the RUNBOOK case was reused while developing
  // these candidates, so it is no longer held out for them.
  pruning: {
    skills: "prune-artifact and writing-for-agents",
    startLength: 3116,
    target: [900, 1500] as const,
    goal: 900,
    ceiling: 3000,
    groups: [
      { label: "Baseline calibration (v2)", lengths: [2978, 2985, 2999] },
      { label: "prune-artifact candidate 81e2d8b", lengths: [1204, 1338, 1491, 1236, 1256] },
      { label: "prune-artifact candidate a616dad", lengths: [1235, 1269, 1399, 1299, 1466] },
    ],
    mustKeepLost: 0,
    second: { name: "ARCHITECTURE.md", startLength: 3119, runs: 8 },
  },
  onHold: { skill: "author-skill" },
};
