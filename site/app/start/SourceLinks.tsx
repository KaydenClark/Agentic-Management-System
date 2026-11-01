// Small "source" links to the committed records a claim comes from.
import type { Source } from "./flow.mjs";
import styles from "./toy.module.css";

export const REPO_BLOB = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/";

export function SourceLinks({ sources }: { sources: readonly Source[] }) {
  return (
    <p className={styles.sources}>
      <span>Source</span>
      {sources.map((s) => (
        <a key={s.path} href={`${REPO_BLOB}${s.path}`}>
          {s.label}
        </a>
      ))}
    </p>
  );
}
