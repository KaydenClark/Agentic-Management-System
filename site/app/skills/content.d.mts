// Types for content.mjs, the skills wiki's article loader.

import type { SkillStage } from "../start/skills.mjs";
import type { Block, Inline } from "./markdown.mjs";

export type ChartSkill = {
  name: string;
  stage: SkillStage;
  flow: "main" | "used";
  // Position in the stage's main flow (1-based); null for skills also used.
  step: number | null;
};

export type ArticleSection = {
  title: string;
  id: string;
  blocks: (Block & { id?: string })[];
};

export type Article = {
  name: string;
  file: string;
  summary: Inline[];
  summaryText: string;
  pin: string;
  credit: "original" | "adapted";
  creditText: Inline[];
  creditLicense: string | null;
  stage: SkillStage;
  flow: "main" | "used";
  step: number | null;
  sections: ArticleSection[];
  links: string[];
  body: string;
};

export declare const SKILLS_PIN: string;
export declare const SKILLS_PIN_SHORT: string;
export declare const ORIGINAL_CREDIT: string;
export declare const LEADING_SECTIONS: readonly string[];
export declare const TRAILING_SECTIONS: readonly string[];
export declare const FIXED_SECTIONS: readonly string[];
export declare const REACH_FOR_HEADER: readonly string[];
export declare const FAQ_RANGE: readonly [number, number];
export declare const SITE_ROUTES: readonly string[];
export declare const PRIVATE_SKILLS_REPO: RegExp;

export declare function contentDir(siteDir?: string): string;
export declare function chartSkills(chart?: readonly SkillStage[]): ChartSkill[];
export declare function parseFrontMatter(src: string, file: string): { data: Record<string, string>; body: string; bodyLine: number };
export declare function hrefProblem(href: string, chart?: readonly SkillStage[]): string | null;
export declare function parseArticle(src: string, options?: { file?: string; chart?: readonly SkillStage[] }): Article;
export declare function loadArticles(dir?: string, options?: { chart?: readonly SkillStage[] }): Article[];
