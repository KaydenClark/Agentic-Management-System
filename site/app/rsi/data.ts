// The /rsi page's only data seam. TK-001 passes the empty fixture; S-007 TK-002
// replaces the caller's argument with rows read from Supabase with the
// publishable key. Nothing here reads Supabase, computes statistics or invents
// a value: a series with no rows is reported as empty.
import { SERIES, type SeriesId, type SeriesPlan } from "./series";

// One RSI trial result row as the page will receive it. The full field list
// (arm, version commits, provider, model, effort, cost, tokens, strength,
// source) arrives with S-006's result tables; TK-002 narrows this type to it.
export type RsiRow = Readonly<Record<string, unknown>>;

export type RowsBySeries = Readonly<Record<SeriesId, readonly RsiRow[]>>;

export interface SeriesView extends SeriesPlan {
  rows: readonly RsiRow[];
  empty: boolean;
}

export function seriesViews(rowsBySeries: RowsBySeries): SeriesView[] {
  return SERIES.map((plan) => {
    const rows = rowsBySeries[plan.id] ?? [];
    return { ...plan, rows, empty: rows.length === 0 };
  });
}
