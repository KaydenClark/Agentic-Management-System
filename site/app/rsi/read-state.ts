import type { ReadResult } from "./supabase";

export const READ_INTERVAL_SECONDS = 300;
export type ReadState = "populated" | "empty" | "stale" | "failed";

// Age describes the retained successful read. Next refreshes in the background,
// so an old timestamp does not establish that its latest refresh failed.
export function readState<T>(loaded: ReadResult<T>, empty: boolean, now = Date.now()): ReadState {
  if (!loaded.ok) return "failed";
  if (now - Date.parse(loaded.readAt) > READ_INTERVAL_SECONDS * 1000) return "stale";
  return empty ? "empty" : "populated";
}
