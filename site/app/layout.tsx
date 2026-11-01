import type { ReactNode } from "react";
import "@fontsource/ibm-plex-sans/latin-400.css";
import "@fontsource/ibm-plex-sans/latin-500.css";
import "@fontsource/ibm-plex-sans/latin-600.css";
import "@fontsource/ibm-plex-sans/latin-700.css";
import "@fontsource/ibm-plex-mono/latin-400.css";
import "@fontsource/ibm-plex-mono/latin-500.css";
import "@fontsource/ibm-plex-mono/latin-700.css";
import "@fontsource/zilla-slab/latin-500.css";
import "@fontsource/zilla-slab/latin-600.css";
import "@fontsource/zilla-slab/latin-700.css";
import "./theme/tokens.css";
import "./globals.css";
import { Shell } from "./shell/Shell";
import { themeScript } from "./shell/theme-script";

export const metadata = {
  // Production domain (serves main, public). Dev previews stay on their
  // protected vercel.app URLs.
  metadataBase: new URL("https://www.workbenchsystem.app"),
  title: "Agentic Management System",
  description: "What the Agentic Management System is, why it exists and how it works.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    // The head script may set data-theme before React hydrates.
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
