import Link from "next/link";
import type { ReactNode } from "react";
import { Footer } from "./Footer";
import { ReadingNav } from "./ReadingNav";
import { ThemeToggle } from "./ThemeToggle";

// The shell every route gets from the root layout: header with the theme
// toggle, reading-order sidebar, the page in <main>, and the commit footer.
// Pages render only their own content; they need not use this directly.
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="topbar">
        <Link className="brand" href="/">
          <span className="brand-name">AMS</span>
          <span className="eyebrow">Agentic Management System</span>
        </Link>
        <ThemeToggle />
      </header>
      <div className="frame">
        <aside className="sidebar">
          <ReadingNav />
        </aside>
        <main id="main" className="content">
          {children}
        </main>
      </div>
      <Footer />
    </div>
  );
}
