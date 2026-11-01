"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { nav, readingIndex } from "../nav";
import styles from "./page-order.module.css";

// Back and forward links in the reading order (app/nav.ts), at the end of
// every page in it. Server-rendered at build time for each route; a page
// outside the reading order (such as not-found) gets none.
export function PageOrder() {
  const index = readingIndex(usePathname());
  if (index < 0) return null;
  const prev = nav[index - 1];
  const next = nav[index + 1];
  return (
    <nav aria-label="Page order" className={styles.order}>
      {prev ? (
        <Link className={styles.link} rel="prev" href={prev.href}>
          <span className={styles.label}>Back</span>
          <span>{prev.label}</span>
        </Link>
      ) : null}
      {next ? (
        <Link className={`${styles.link} ${styles.next}`} rel="next" href={next.href}>
          <span className={styles.label}>Next</span>
          <span>{next.label}</span>
        </Link>
      ) : null}
    </nav>
  );
}
