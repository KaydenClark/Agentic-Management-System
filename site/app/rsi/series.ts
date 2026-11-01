// The planned RSI series (S-007 Desired Behavior: per task and per version,
// held-out and dev visibly separate). Each next expected event is taken from
// the planned records that will first write rows for it; none carries a date,
// because none of those records sets one.
//
// Visible text here must hold no digit: the empty page shows no number of any
// kind (DDR-000T). Record IDs live only in link targets.

export type Split = "held-out" | "dev";
export type View = "task" | "version";

export type SeriesId = `${Split}-per-${View}`;

export interface NextEvent {
  text: string;
  source: { label: string; href: string };
}

export interface SeriesPlan {
  id: SeriesId;
  split: Split;
  view: View;
  title: string;
  shows: string;
  nextEvent: NextEvent;
}

const REPO = "https://github.com/KaydenClark/Agentic-Management-System/blob/main/workbench/landmarks";
const S002 = `${REPO}/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop`;

export const SPLITS: { split: Split; title: string; about: string }[] = [
  {
    split: "held-out",
    title: "Held-out tasks",
    about:
      "Held-out tasks are kept aside: the loop never studies or tunes on them, so they show whether a change helps on work it was not fitted to. Only held-out results can support a headline.",
  },
  {
    split: "dev",
    title: "Dev tasks",
    about:
      "Dev tasks are the working set: the loop studies their failures to choose its next change. They show where it is learning, not whether the change generalises.",
  },
];

export const SERIES: SeriesPlan[] = [
  {
    id: "held-out-per-task",
    split: "held-out",
    view: "task",
    title: "Held-out results per task",
    shows: "Each held-out task's pass results, one line per task, across versions.",
    nextEvent: {
      text: "No Task to create or run held-out tasks is planned yet. The RSI loop shows no public number until several held-out tasks have rows from repeated trials, so this place stays empty until then.",
      source: { label: "the RSI loop Spec (held-out before public)", href: `${S002}/SPEC.md` },
    },
  },
  {
    id: "held-out-per-version",
    split: "held-out",
    view: "version",
    title: "Held-out results per version",
    shows: "Each system version's pass results over the held-out tasks, with the prior version and the control arms beside it.",
    nextEvent: {
      text: "Also waiting on held-out tasks, which no Task plans yet. A version comparison here needs held-out rows, the control arms, the prior version and an interval.",
      source: { label: "the RSI loop Spec (held-out before public)", href: `${S002}/SPEC.md` },
    },
  },
  {
    id: "dev-per-task",
    split: "dev",
    view: "task",
    title: "Dev results per task",
    shows: "Each dev task's pass results, one line per task, across versions.",
    nextEvent: {
      text: "The noise-floor run: the current version run against itself, repeatedly, on a small fixed set of dev tasks, to record how often each task's result flips by chance. It waits on the RSI result tables in the data store and on the owner's standing campaign approval.",
      source: { label: "the noise-floor Task of the RSI loop", href: `${S002}/tasks/TK-002/TASK.md` },
    },
  },
  {
    id: "dev-per-version",
    split: "dev",
    view: "version",
    title: "Dev results per version",
    shows: "Each system version's pass results over the dev tasks, with the control arms beside it.",
    nextEvent: {
      text: "The noise-floor run gives the current version its first dev rows. A second version appears only after one full round of the loop: a failed row, one change, and a rerun against the current version and the controls.",
      source: { label: "the one-round Task of the RSI loop", href: `${S002}/tasks/TK-004/TASK.md` },
    },
  },
];
