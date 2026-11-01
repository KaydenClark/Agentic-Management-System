"use client";

// The sample agent notice above the board. Dismissing it is local state only;
// the board stores nothing and sends nothing. Light and dark are the shell's.

import { useState } from "react";

export function AgentBanner() {
  const [shown, setShown] = useState(true);
  if (!shown) return null;
  return (
    <div className="tone h-agent gb-strip gb-strip-agent">
      <span className="dot" />
      <span className="grow">
        Sample notice: an agent updated the board since you loaded it. Reload when you are between questions; your draft stays.
      </span>
      <button type="button" className="gb-strip-btn" onClick={() => setShown(false)}>Reload</button>
    </div>
  );
}
