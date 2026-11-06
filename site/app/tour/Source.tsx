// A compact on-site citation. Source identity is metadata, not navigation.
import type { ReactNode } from "react";
import styles from "./tour.module.css";

export function Source({ path, revision: recordedRevision, expanded = false, children }: {
  path: string; revision?: string; expanded?: boolean; children: ReactNode;
}) {
  const revision = recordedRevision ?? process.env.AMS_COMMIT_SHA ?? "unknown";
  const generated = recordedRevision === undefined;
  const identity = `${path} at revision ${revision}`;
  return (
    <span className={styles.source} data-source-path={path} data-source-revision={revision} title={identity}>
      {" "}Source: {children} · {expanded ? <><code>{path}</code>{" at revision "}</> : null}
      <code data-review-exclude={generated ? "" : undefined}>{expanded ? revision : revision.slice(0, 7)}</code>.
      {!expanded ? (
        <span className={styles.sourceIdentity}> Public record {path} at revision{" "}
          <span data-review-exclude={generated ? "" : undefined}>{revision}</span>.
        </span>
      ) : null}
    </span>
  );
}
