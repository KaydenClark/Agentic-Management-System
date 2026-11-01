"use client";

// Small client islands for the demo header and banner. They keep everything in the
// browser: the theme choice is the only thing stored (localStorage, this device).

import { useState } from "react";

export function ThemeToggle() {
  const toggle = () => {
    const root = document.documentElement;
    const current =
      root.dataset.gbTheme ?? (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    const next = current === "light" ? "dark" : "light";
    root.dataset.gbTheme = next;
    try {
      localStorage.setItem("gb-theme", next);
    } catch {
      // Storage may be unavailable; the choice then lasts for this page view only.
    }
  };
  return (
    <button type="button" className="gb-theme" onClick={toggle} aria-label="Switch light or dark theme">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor" />
      </svg>
      <span className="gb-dark-only">Dark</span>
      <span className="gb-light-only">Light</span>
    </button>
  );
}

export function HeaderSearch() {
  return (
    <form role="search" className="gb-search" onSubmit={(e) => e.preventDefault()}>
      <label htmlFor="gb-global-search" className="sr-only">Search the Dashboard</label>
      <input id="gb-global-search" type="search" placeholder="Search the Dashboard…" />
    </form>
  );
}

export function AgentBanner() {
  const [shown, setShown] = useState(true);
  if (!shown) return null;
  return (
    <div className="tone h-agent gb-strip gb-strip-agent">
      <span className="dot" />
      <span style={{ flex: 1 }}>
        Sample notice: an agent updated the board since you loaded it. Reload when you are between questions; your draft stays.
      </span>
      <button type="button" className="gb-strip-btn" onClick={() => setShown(false)}>Reload</button>
    </div>
  );
}
