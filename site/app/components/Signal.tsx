import type { ReactNode } from "react";
import styles from "./signal.module.css";

export type SignalKind = "agent" | "owner" | "worth" | "heat" | "returned";

// Soft signals explain a role or condition at rest. The words carry the
// meaning too; color never establishes approval, priority or live status.
export function Signal({ kind, label, children }: { kind: SignalKind; label: string; children: ReactNode }) {
  return (
    <div className={`tone h-${kind} ${styles.signal}`} data-signal={kind}>
      <p className={styles.label}>{label}</p>
      {children}
    </div>
  );
}
