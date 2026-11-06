// Server only. Keep the actual successful-read time *inside* the cached value.
// A refused/malformed/outage response throws rather than replacing that value.
// Qualified with real Next16.4.3 across a fresh process using the same .next
// cache; no claim of cross-host/deployment retention or a permanent archive.
import { unstable_cache } from "next/cache";
import { emptyData } from "./data";
import { loadBuildEvents, loadRsiData, emptyActivity, type BuildActivity, type LoadResult, type ReadResult } from "./supabase";
import { READ_INTERVAL_SECONDS } from "./read-state";

const trials = unstable_cache(async (base: string) => {
  const loaded = await loadRsiData({ env: { NEXT_PUBLIC_SUPABASE_URL: base, NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY } });
  if (!loaded.ok) throw new Error("public trial read unavailable");
  return loaded;
}, ["s007-public-trials-v1"], { revalidate: READ_INTERVAL_SECONDS });

const activity = unstable_cache(async (base: string) => {
  const loaded = await loadBuildEvents({ env: { NEXT_PUBLIC_SUPABASE_URL: base, NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY } });
  if (!loaded.ok) throw new Error("public activity read unavailable");
  return loaded;
}, ["s007-public-merge-facts-v2"], { revalidate: READ_INTERVAL_SECONDS });

export async function loadCachedEvidence(): Promise<{ trials: LoadResult; activity: ReadResult<BuildActivity> }> {
  const base = process.env.NEXT_PUBLIC_SUPABASE_URL;
  // Missing configuration is a failed read, not a successfully empty store.
  if (!base || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) return {
    trials: { ok: false, data: emptyData, readAt: null, reason: "public reader not configured" },
    activity: { ok: false, data: emptyActivity, readAt: null, reason: "public reader not configured" },
  };
  const [trialRead, activityRead] = await Promise.allSettled([trials(base), activity(base)]);
  return {
    trials: trialRead.status === "fulfilled" ? trialRead.value : { ok: false, data: emptyData, readAt: null, reason: "public trial read unavailable" },
    activity: activityRead.status === "fulfilled" ? activityRead.value : { ok: false, data: emptyActivity, readAt: null, reason: "public activity read unavailable" },
  };
}
