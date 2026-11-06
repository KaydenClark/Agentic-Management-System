"use client";

// The skills wiki's left navigation pane (S-008, after aihero.dev/skills):
// Overview, then each chart stage as a numbered group of its skills, main
// flow first in order, then the skills also used there. On the index every
// group is open; on an article the group holding it is open and the article
// is marked current, and the others fold. Wiki navigation, not page content: data-review-exclude keeps it out of
// every page's content hash, so adding an article clears no other approval.
import Link from "next/link";
import { usePathname } from "next/navigation";
import { stages } from "../start/skills.mjs";
import styles from "./skills.module.css";

export function WikiNav() {
  const path = (usePathname() ?? "").replace(/\/$/, "");
  const current = path.startsWith("/skills/") ? path.slice("/skills/".length) : null;
  return (
    <nav aria-label="Skills wiki" className={styles.wikiNav} data-review-exclude="">
      <Link className={styles.navOverview} href="/skills" aria-current={path === "/skills" ? "page" : undefined}>
        Overview
      </Link>
      <ol className={styles.navStages}>
        {stages.map((st, i) => {
          const names = [...st.main, ...st.used];
          return (
            <li key={st.id}>
              <details className={styles.navGroup} open={current === null || names.includes(current)}>
                <summary>
                  <span className={styles.navNum}>{i + 1}</span>
                  {st.name}
                </summary>
                <ol className={styles.navSkills}>
                  {names.map((name, k) => (
                    <li key={name} className={k === st.main.length ? styles.navAlso : undefined}>
                      <Link href={`/skills/${name}`} aria-current={name === current ? "page" : undefined}>
                        <span className={styles.navNum}>
                          {i + 1}.{k + 1}
                        </span>
                        {name}
                      </Link>
                    </li>
                  ))}
                </ol>
              </details>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
