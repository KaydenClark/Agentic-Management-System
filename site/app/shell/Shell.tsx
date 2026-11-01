import Link from "next/link";
import type { ReactNode } from "react";
import { DraftMark } from "./DraftMark";
import { Footer } from "./Footer";
import { PageOrder } from "./PageOrder";
import { ReadingNav } from "./ReadingNav";
import { ThemeToggle } from "./ThemeToggle";

// The shell every route gets from the root layout: a top bar with the site
// title, the reading-order links and the theme toggle; the page in <main>
// opening with the draft mark (until the owner approves the page) and ending
// with back and forward links in the reading order; the commit footer.
// Header, main and footer share one centred container (.container), so every
// page's content lines up with the header's edge.
// Pages render only their own content; they need not use this directly.
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="topbar">
        <div className="container topbar-inner">
          <Link className="brand" href="/">
            <span className="brand-name">AMS</span>
            <span className="eyebrow">Agentic Management System</span>
          </Link>
          <ReadingNav />
          <ThemeToggle />
        </div>
      </header>
      <main id="main" className="container content">
        <DraftMark />
        {children}
        <PageOrder />
      </main>
      <Footer />
    </div>
  );
}
