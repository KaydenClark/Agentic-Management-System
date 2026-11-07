// /rsi reads existing public activity and trial contracts independently.
// Successful envelopes retain their actual origin-read times in Next's cache;
// stale timestamps and cold failures never establish an empty current store.
import type { Metadata } from "next";
import { seriesViews, runsWithoutResults } from "./data";
import { loadCachedEvidence } from "./cached";
import { readState } from "./read-state";
import { AuditEvidence } from "./audit-view";
import { ActivityEvidence } from "./activity";
import { RsiView } from "./view";
import { RepairEvidence } from "./repair";
import { RoundTwoEvidence } from "./round-two";
import { SkillTrends } from "./skill-trends";
import { recordedLoops } from "./skill-loops";

export const metadata: Metadata = {
  title: "RSI results | Agentic Management System",
  description: "The RSI loop's measured results, per task and per version, held-out and dev kept apart, every number linked to its rows.",
};

// Re-read Supabase at most every five minutes; the page stays prerendered.
export const revalidate = 300;

export default async function RsiPage() {
  const evidence = await loadCachedEvidence();
  const loaded = evidence.trials;
  const state = readState(loaded, loaded.data.results.length === 0 && loaded.data.runs.length === 0);
  return (
    <RsiView views={seriesViews(loaded.data)} runEvidence={runsWithoutResults(loaded.data)} unavailable={!loaded.ok} readAt={loaded.readAt} stale={state === "stale"}>
      <ActivityEvidence loaded={evidence.activity} />
      <AuditEvidence loaded={evidence.audits} />
      <SkillTrends records={recordedLoops()} />
      <RoundTwoEvidence />
      <RepairEvidence />
    </RsiView>
  );
}
