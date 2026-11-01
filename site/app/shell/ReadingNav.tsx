"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { nav, readingIndex } from "../nav";

// Reading-order navigation with the reader's position. Server-rendered at
// build time for each route; the client only keeps it current on navigation.
export function ReadingNav() {
  const index = readingIndex(usePathname());
  return (
    <nav aria-label="Reading order" className="reading-nav">
      <p className="eyebrow">
        Reading order{index >= 0 ? ` · ${index + 1} of ${nav.length}` : ""}
      </p>
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
