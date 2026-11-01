"use client";

import { usePathname } from "next/navigation";
import styles from "./draft-mark.module.css";

// The draft mark at the top of every page's <main> (S-003 TK-004). A page
// shows it until a committed record in approvals.json names the page's route
// and its current content hash. `npm run build` (scripts/build.mjs) builds
// once with no page approved, hashes every built page, and rebuilds with
// AMS_APPROVED_ROUTES naming the routes whose hash an approval matches; any
// other way of building leaves every mark in place. Server-rendered for each
// route, so it reads without scripts. The hash skips this element
// (data-review-mark), so showing or hiding the mark never changes a hash.
const approved: string[] = JSON.parse(process.env.AMS_APPROVED_ROUTES || "[]");

export function DraftMark() {
  const route = usePathname();
  if (approved.includes(route)) return null;
  return (
    <div data-review-mark="draft" role="note" className={`tone h-owner ${styles.mark}`}>
      <span className={styles.dot} aria-hidden="true" />
      <strong className={styles.label}>Draft</strong>
      <span>Not approved by the owner yet. This page may still change.</span>
    </div>
  );
}
