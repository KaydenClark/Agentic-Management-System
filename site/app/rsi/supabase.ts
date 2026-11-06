// Server-side public PostgREST readers. No service key or private lineage.
// Each request bypasses fetch caching; cached.ts retains only fully validated
// successful envelopes, keeping failures distinct from a successful empty read.
import { emptyData, type RsiData, type RsiResult, type RsiRun } from "./data";

const RUN_COLUMNS = [
  "id", "run_key", "arm", "provider", "model", "effort", "runtime_commit", "controls_commit", "skills_commit",
  "grader_version", "state", "started_at", "finished_at", "source_kind", "source_ref", "source_url", "strength",
  "is_test", "detail",
].join(",");

const RESULT_COLUMNS = [
  "id", "run_id", "arm", "provider", "model", "effort", "runtime_commit", "controls_commit", "skills_commit",
  "grader_version", "task_id", "split", "trial", "execution_state", "passed", "score", "cost_usd", "input_tokens",
  "output_tokens", "turns", "wall_seconds", "metric_unknowns", "source_kind", "source_ref", "source_url", "strength", "is_test", "detail",
].join(",");

// Exclude summary and detail: arbitrary operational/private text is never a
// presentation contract. Unexpected response fields are discarded as well.
const EVENT_FIELDS = ["id", "kind", "subject", "occurred_at", "recorded_at", "source_kind", "source_ref", "source_url", "strength", "is_test"] as const;
const EVENT_COLUMNS = EVENT_FIELDS.join(",");
export interface BuildEvent {
  id: number;
  kind: "merge";
  subject: string;
  occurred_at: string;
  recorded_at: string;
  source_kind: "commit";
  source_ref: string;
  source_url: string;
  strength: "recorded_fact";
  is_test: boolean;
}
export interface BuildActivity { events: BuildEvent[]; unsupported: number }
export const emptyActivity: BuildActivity = { events: [], unsupported: 0 };
export type ReadResult<T> = { ok: true; data: T; readAt: string } | { ok: false; data: T; readAt: null; reason: string };

const PAGE = 1000; // Supabase's default PostgREST row cap per request.
const MAX_PAGES = 50;

export type LoadResult = ReadResult<RsiData>;

interface LoadOptions {
  env?: Readonly<Record<string, string | undefined>>;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
}

class LoadError extends Error {}

function validRow(table: string, value: unknown): boolean {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const row = value as Record<string, unknown>;
  const positiveInteger = (v: unknown) => typeof v === "number" && Number.isSafeInteger(v) && v > 0;
  if (!positiveInteger(row.id) || typeof row.is_test !== "boolean") return false;
  // Unsupported core fields are counted without being returned to the page.
  // A malformed row identity still fails the read rather than inventing counts.
  if (table === "build_events") return true;
  const labels = ["arm", "provider", "model", "effort", "source_kind", "source_ref", "strength"];
  if (labels.some((key) => typeof row[key] !== "string" || !(row[key] as string).trim())) return false;
  for (const key of ["runtime_commit", "controls_commit", "skills_commit", "grader_version"]) {
    if (typeof row[key] !== "string" || !/^[a-f0-9]{40}$/.test(row[key])) return false;
  }
  if (table === "rsi_runs") {
    return ["running", "completed", "stopped", "failed"].includes(String(row.state)) &&
      typeof row.started_at === "string" && Number.isFinite(Date.parse(row.started_at));
  }
  const metric = (v: unknown) => v === null ||
    ((typeof v === "number" || (typeof v === "string" && v.trim() !== "")) && Number.isFinite(Number(v)) && Number(v) >= 0);
  return positiveInteger(row.run_id) && positiveInteger(row.trial) &&
    typeof row.task_id === "string" && row.task_id.trim() !== "" &&
    ["dev", "held_out"].includes(String(row.split)) &&
    ["completed", "runner_error", "auth_error", "timeout", "capped"].includes(String(row.execution_state)) &&
    (row.passed === null || typeof row.passed === "boolean") &&
    ["cost_usd", "input_tokens", "output_tokens", "turns", "wall_seconds"].every((key) => metric(row[key]));
}

async function readTable<T>(base: string, key: string, table: string, columns: string, fetchImpl: typeof fetch, timeoutMs: number): Promise<T[]> {
  const rows: T[] = [];
  for (let page = 0; page < MAX_PAGES; page++) {
    const url = new URL(`/rest/v1/${table}`, base);
    url.searchParams.set("select", columns);
    url.searchParams.set("is_test", "is.false");
    url.searchParams.set("order", "id.asc");
    url.searchParams.set("limit", String(PAGE));
    url.searchParams.set("offset", String(page * PAGE));
    let res: Response;
    try {
      res = await fetchImpl(url.toString(), {
        headers: { apikey: key, Authorization: `Bearer ${key}`, Accept: "application/json" },
        signal: AbortSignal.timeout(timeoutMs),
        cache: "no-store", // only validated successful envelopes are cached by cached.ts
      });
    } catch (err) {
      throw new LoadError(`${table}: request failed (${err instanceof Error ? err.name : "error"})`);
    }
    if (!res.ok) throw new LoadError(`${table}: HTTP ${res.status}`);
    let body: unknown;
    try {
      body = await res.json();
    } catch {
      throw new LoadError(`${table}: response was not JSON`);
    }
    if (!Array.isArray(body)) throw new LoadError(`${table}: response was not a row list`);
    if (!body.every((row) => validRow(table, row))) throw new LoadError(`${table}: response contained malformed rows`);
    const projected = table === "build_events"
      ? body.map((row) => Object.fromEntries(EVENT_FIELDS.map((key) => [key, row[key]])))
      : body;
    rows.push(...(projected as T[]));
    if (body.length < PAGE) return rows;
  }
  throw new LoadError(`${table}: more rows than this page reads`);
}

export async function loadRsiData(options: LoadOptions = {}): Promise<LoadResult> {
  const env = options.env ?? process.env;
  const base = env.NEXT_PUBLIC_SUPABASE_URL;
  const key = env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!base || !key) return { ok: false, reason: "Supabase URL or publishable key not set", data: emptyData, readAt: null };
  const fetchImpl = options.fetchImpl ?? fetch;
  const timeoutMs = options.timeoutMs ?? 8000;
  try {
    const [runs, results] = await Promise.all([
      readTable<RsiRun>(base, key, "rsi_runs", RUN_COLUMNS, fetchImpl, timeoutMs),
      readTable<RsiResult>(base, key, "rsi_results", RESULT_COLUMNS, fetchImpl, timeoutMs),
    ]);
    // Row-level security and the query already exclude test rows; drop any
    // that arrive anyway.
    return { ok: true, readAt: new Date().toISOString(), data: { runs: runs.filter((r) => r?.is_test === false), results: results.filter((r) => r?.is_test === false) } };
  } catch (err) {
    return { ok: false, reason: err instanceof LoadError ? err.message : "unexpected read failure", data: emptyData, readAt: null };
  }
}

// The first reviewed public producer path is exact Git-derived merge facts.
// Other kinds/locators need their own safe contract, not a general text filter.
function supportedMerge(row: Record<string, unknown>): boolean {
  const iso = (v: unknown) => typeof v === "string" &&
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/.test(v) && Number.isFinite(Date.parse(v));
  return row.kind === "merge" && row.source_kind === "commit" && row.strength === "recorded_fact" &&
    typeof row.subject === "string" && /^[1-9]\d*$/.test(row.subject) && Number.isSafeInteger(Number(row.subject)) &&
    typeof row.source_ref === "string" && /^[a-f0-9]{40}$/.test(row.source_ref) &&
    row.source_url === `https://github.com/KaydenClark/Agentic-Management-System/commit/${row.source_ref}` &&
    iso(row.occurred_at) && iso(row.recorded_at);
}

// Independent stream: an activity-read failure cannot erase trial evidence.
export async function loadBuildEvents(options: LoadOptions = {}): Promise<ReadResult<BuildActivity>> {
  const env = options.env ?? process.env;
  const base = env.NEXT_PUBLIC_SUPABASE_URL;
  const key = env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!base || !key) return { ok: false, reason: "public data reader is not configured", data: emptyActivity, readAt: null };
  try {
    const rows = await readTable<Record<string, unknown>>(base, key, "build_events", EVENT_COLUMNS, options.fetchImpl ?? fetch, options.timeoutMs ?? 8000);
    const publicRows = rows.filter((row) => row.is_test === false);
    if (new Set(publicRows.map((row) => row.id)).size !== publicRows.length) throw new LoadError("build_events: conflicting row identities");
    const events = publicRows.filter(supportedMerge) as unknown as BuildEvent[];
    if (new Set(events.map((row) => row.source_ref)).size !== events.length) throw new LoadError("build_events: conflicting source identities");
    return { ok: true, data: { events, unsupported: publicRows.length - events.length }, readAt: new Date().toISOString() };
  } catch (err) {
    return { ok: false, reason: err instanceof LoadError ? err.message : "unexpected activity read failure", data: emptyActivity, readAt: null };
  }
}
