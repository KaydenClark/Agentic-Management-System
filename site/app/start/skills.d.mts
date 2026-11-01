// Types for skills.mjs, the skills diagram's data on /start.

import type { Source } from "./flow.mjs";

export type SkillStage = {
  id: string;
  name: string;
  gloss: string;
  // The main-flow skills, in the order they run.
  main: readonly string[];
  // Skills also used at this stage.
  used: readonly string[];
  // Where the work goes next when it leaves this stage another way.
  note?: string;
};

export declare const stages: readonly SkillStage[];
export declare const sources: readonly Source[];
