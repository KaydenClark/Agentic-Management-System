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
import "./board.css";

// Applies a saved light or dark choice before the board paints; with none saved
// the board follows the system theme through CSS.
const THEME_SCRIPT =
  "try{var t=localStorage.getItem('gb-theme');if(t==='light'||t==='dark')document.documentElement.dataset.gbTheme=t}catch(e){}";

export default function GrillBoardDemoLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <script dangerouslySetInnerHTML={{ __html: THEME_SCRIPT }} />
      {children}
    </>
  );
}
