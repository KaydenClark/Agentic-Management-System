// The site's reading order: one list, in the order a reader should go.
// The shell's navigation, its "n of N" position and any forward/back links
// read this list. Add an entry only for a route that exists.
export type NavEntry = {
  href: string;
  label: string;
};

export const nav: readonly NavEntry[] = [
  { href: "/", label: "Home" },
  { href: "/start", label: "About" },
  { href: "/why", label: "Why" },
  { href: "/how-it-works", label: "How it works" },
  { href: "/grill-board-demo", label: "Grill Board demo" },
  { href: "/skills", label: "Skills" },
  { href: "/rsi", label: "RSI results" },
  { href: "/glossary", label: "Glossary" },
];

// Index of the entry for `pathname` (trailing slash ignored), or -1.
export function readingIndex(pathname: string | null): number {
  if (!pathname) return -1;
  const normalized = pathname !== "/" && pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  const path = normalized === "/about" ? "/start" : normalized;
  return nav.findIndex((entry) => entry.href === path);
}
