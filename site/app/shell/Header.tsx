"use client";

import Link from "next/link";
import { useEffect, useRef } from "react";
import { ReadingNav } from "./ReadingNav";
import { ThemeToggle } from "./ThemeToggle";

export function Header() {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const header = ref.current;
    if (!header) return;
    const root = document.documentElement;
    const measure = () => {
      root.style.setProperty("--sticky-header-height", `${Math.ceil(header.getBoundingClientRect().height)}px`);
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(header);

    // A directly loaded fragment can be positioned before fonts and the
    // header settle. Reveal it once using the measured sticky clearance.
    const revealInitialHash = () => {
      if (!window.location.hash) return;
      let id: string;
      try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
      measure();
      document.getElementById(id)?.scrollIntoView({ block: "start" });
    };
    let active = true;
    document.fonts.ready.then(() => { if (active) revealInitialHash(); });
    return () => {
      active = false;
      observer.disconnect();
      root.style.removeProperty("--sticky-header-height");
    };
  }, []);

  return (
    <header className="topbar" ref={ref}>
      <div className="topbar-inner">
        <Link className="brand" href="/" aria-label="Home" title="Home">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
            <path d="m3 10 9-7 9 7M5 9v12h5v-7h4v7h5V9" />
          </svg>
        </Link>
        <ReadingNav />
        <ThemeToggle />
      </div>
    </header>
  );
}
