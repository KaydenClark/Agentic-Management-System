// Native disclosure keeps full provenance available without interrupting reading.
import type { Source as SourceRecord } from "./flow.mjs";
import { Source } from "../tour/Source";
import styles from "./toy.module.css";

export function SourceLinks({ sources }: { sources: readonly SourceRecord[] }) {
  return (
    <details className={styles.sources}>
      <summary>Source identities</summary>
      <ul>{sources.map(source => <li key={source.path}><Source path={source.path} expanded>{source.label}</Source></li>)}</ul>
    </details>
  );
}
