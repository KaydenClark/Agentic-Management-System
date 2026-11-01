// A link to the committed record a claim comes from, for the tour pages that
// are prose (Why, Quickstart, Glossary, About). Links point at blob/dev, the
// branch the site is built from.
import type { ReactNode } from "react";
import styles from "./tour.module.css";

export const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";

export function Source({ path, children }: { path: string; children: ReactNode }) {
  return (
    <span className={styles.source}>
      {" "}
      Source: <a href={`${REPO_BLOB}${path}`}>{children}</a>.
    </span>
  );
}
