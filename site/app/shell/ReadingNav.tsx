"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { nav, readingIndex } from "../nav";

// Reading-order links in the top bar, the current page marked with
// aria-current. Server-rendered at build time for each route; the client only
// keeps it current on navigation. The reader's "n of N" position sits with the
// back/forward links (PageOrder).
export function ReadingNav() {
  const index = readingIndex(usePathname());
  return (
    <nav aria-label="Reading order" className="topnav">
      <ol>
        {nav.map((entry, i) => (
          <li key={entry.href}>
            <Link className="navlink" href={entry.href} aria-current={i === index ? "page" : undefined}>
              {entry.label}
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}
