// Reads S-006's RSI tables for /rsi with the publishable key (S-007 TK-002).
// Server only: page.tsx calls it while rendering on the server (at build and
// on revalidation), so the key stays in the server bundle and never reaches
// served HTML, RSC payloads or client JS. Plain fetch against PostgREST, no
// client library. Any failure (missing env, refused request, error status,
// unexpected body) returns the empty data marked unavailable; it never
// throws, so the build cannot fail on it.
import { emptyData, type RsiData, type RsiResult, type RsiRun } from "./data";

const RUN_COLUMNS = [
  "id", "run_key", "arm", "provider", "model", "effort", "runtime_commit", "controls_commit", "skills_commit",
  "grader_version", "state", "started_at", "finished_at", "source_kind", "source_ref", "source_url", "strength",
  "is_test", "detail",
].join(",");

const RESULT_COLUMNS = [
  "id", "run_id", "arm", "provider", "model", "effort", "runtime_commit", "controls_commit", "skills_commit",
  "grader_version", "task_id", "split", "trial", "execution_state", "passed", "score", "cost_usd", "input_tokens",
  "output_tokens", "turns", "wall_seconds", "source_kind", "source_ref", "source_url", "strength", "is_test", "detail",
].join(",");

const PAGE = 1000; // Supabase's default PostgREST row cap per request.
const MAX_PAGES = 50;

export type LoadResult = { ok: true; data: RsiData } | { ok: false; reason: string; data: RsiData };

interface LoadOptions {
  env?: Readonly<Record<string, string | undefined>>;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
}

class LoadError extends Error {}

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
    rows.push(...(body as T[]));
    if (body.length < PAGE) return rows;
  }
  throw new LoadError(`${table}: more rows than this page reads`);
}

export async function loadRsiData(options: LoadOptions = {}): Promise<LoadResult> {
  const env = options.env ?? process.env;
  const base = env.NEXT_PUBLIC_SUPABASE_URL;
  const key = env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!base || !key) return { ok: false, reason: "Supabase URL or publishable key not set", data: emptyData };
  const fetchImpl = options.fetchImpl ?? fetch;
  const timeoutMs = options.timeoutMs ?? 8000;
  try {
    const [runs, results] = await Promise.all([
      readTable<RsiRun>(base, key, "rsi_runs", RUN_COLUMNS, fetchImpl, timeoutMs),
      readTable<RsiResult>(base, key, "rsi_results", RESULT_COLUMNS, fetchImpl, timeoutMs),
    ]);
    // Row-level security and the query already exclude test rows; drop any
    // that arrive anyway.
    return { ok: true, data: { runs: runs.filter((r) => r?.is_test === false), results: results.filter((r) => r?.is_test === false) } };
  } catch (err) {
    return { ok: false, reason: err instanceof LoadError ? err.message : "unexpected read failure", data: emptyData };
  }
}
