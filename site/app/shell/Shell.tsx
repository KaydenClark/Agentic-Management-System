import type { ReactNode } from "react";
import { Footer } from "./Footer";
import { PageOrder } from "./PageOrder";
import { Header } from "./Header";

// The shell every route gets from the root layout: a top bar with the site
// title, the reading-order links and the theme toggle; the page in <main>,
// ending with back and forward links in the reading order; the commit footer.
// The persistent header spans the viewport; main and footer keep their
// independent centered reading column.
// Pages render only their own content; they need not use this directly.
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <Header />
      <main id="main" className="container content">
        {children}
        <PageOrder />
      </main>
      <Footer />
    </div>
  );
}
