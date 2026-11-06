// /rsi: the RSI chart page (S-007). A server component: it reads S-006's
// rsi_runs and rsi_results with the publishable key at build and on each
// revalidation, so the content is server-rendered and the key never ships to
// the browser. With no rows, or when the read fails, every chart place shows
// its honest empty state (TK-001). The skill trends (TK-002J) lead, drawn
// from the recorded loops only.
import type { Metadata } from "next";
import { seriesViews } from "./data";
import { loadRsiData } from "./supabase";
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
  const loaded = await loadRsiData();
  if (!loaded.ok) console.warn(`/rsi: results could not be loaded (${loaded.reason})`);
  return (
    <RsiView views={seriesViews(loaded.data)} unavailable={!loaded.ok} readAt={loaded.readAt}>
      <SkillTrends records={recordedLoops()} />
      <RoundTwoEvidence />
      <RepairEvidence />
    </RsiView>
  );
}
