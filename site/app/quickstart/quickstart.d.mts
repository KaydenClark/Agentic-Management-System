// Types for quickstart.mjs, the one source /quickstart and its replay test read.

export type Step = {
  id: string;
  // Exactly what the reader types; a plain command with no shell syntax.
  command: string;
  // What the command prints, or null when the page shows none.
  output: string | null;
};

export const CLONE_URL: string;
export const REPO_DIR: string;
export const steps: readonly Step[];
