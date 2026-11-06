// The skills wiki's frame (S-008): the navigation pane on the left of the
// index and every article, the page on the right; stacked on narrow screens.
import type { ReactNode } from "react";
import { WikiNav } from "./WikiNav";
import styles from "./skills.module.css";

export default function SkillsLayout({ children }: { children: ReactNode }) {
  return (
    <div className={styles.wiki}>
      <WikiNav />
      <div className={styles.wikiMain}>{children}</div>
    </div>
  );
}
