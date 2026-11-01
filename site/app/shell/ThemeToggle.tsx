"use client";

import { useEffect, useState } from "react";
import { THEME_STORAGE_KEY } from "./theme-script";

type Theme = "light" | "dark";

function effectiveTheme(): Theme {
  const chosen = document.documentElement.getAttribute("data-theme");
  if (chosen === "light" || chosen === "dark") return chosen;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

// Switches between light and dark. A choice overrides the system preference
// and is stored in localStorage; the inline head script reapplies it on load.
export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme | null>(null);

  useEffect(() => {
    setTheme(effectiveTheme());
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const follow = () => setTheme(effectiveTheme());
    media.addEventListener("change", follow);
    return () => media.removeEventListener("change", follow);
  }, []);

  function toggle() {
    const next: Theme = effectiveTheme() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try {
      localStorage.setItem(THEME_STORAGE_KEY, next);
    } catch {
      // Storage can be unavailable (private mode); the choice still applies.
    }
    setTheme(next);
  }

  return (
    <button
      type="button"
      className="theme-toggle"
      data-theme-toggle=""
      onClick={toggle}
      aria-label={theme ? `Theme: ${theme}. Switch to ${theme === "dark" ? "light" : "dark"}` : "Switch light or dark theme"}
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor" />
      </svg>
      <span>{theme === "dark" ? "Dark" : theme === "light" ? "Light" : "Theme"}</span>
    </button>
  );
}
