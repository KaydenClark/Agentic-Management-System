// The site's reading order: one list, in the order a reader should go.
// The shell's navigation, its "n of N" position and any forward/back links
// read this list. Add an entry only for a route that exists.
export type NavEntry = {
  href: string;
  label: string;
};

export const nav: readonly NavEntry[] = [
  { href: "/", label: "Home" },
  { href: "/start", label: "Start here" },
  { href: "/how-it-works", label: "How it works" },
  { href: "/grill-board-demo", label: "Grill Board demo" },
  { href: "/rsi", label: "RSI results" },
];

// Index of the entry for `pathname` (trailing slash ignored), or -1.
export function readingIndex(pathname: string | null): number {
  if (!pathname) return -1;
  const path = pathname !== "/" && pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  return nav.findIndex((entry) => entry.href === path);
}
