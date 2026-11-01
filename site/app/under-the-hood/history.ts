// /under-the-hood data and rendering (S-003 TK-006). Reads S-006's
// public.build_events rows with the publishable key over plain Supabase REST,
// server-side only, and renders them in time order. Every word inside the
// history region comes from a row (kind label, time, summary, subject) or is
// a count or time derived from rows; tests/under-the-hood.test.mjs renders
// this module on fixtures and fails on any other text.
//
// Written with createElement, not JSX, and with erasable TypeScript only, so
// Node's built-in type stripping can load it in the tests without a build.
import { createElement as h, type ReactNode } from "react";

export type BuildEvent = {
  id: number;
  kind: string;
  subject: string;
  summary: string;
  occurred_at: string;
  source_url: string | null;
  is_test: boolean;
  detail?: Record<string, unknown> | null;
};

export type Tone = "returned" | "agent" | "none";

// Filter categories, in display order. Each kind belongs to one.
export const CATEGORIES = [
  { id: "plans", label: "Specs and Tasks" },
  { id: "prs", label: "Pull requests" },
  { id: "commits", label: "Commits" },
  { id: "rework", label: "Corrections and returns" },
  { id: "other", label: "Other" },
] as const;
export type CategoryId = (typeof CATEGORIES)[number]["id"];

// The kinds S-006 writes, each with the plain label shown on an event and a
// one-line description for the page's key. A kind not listed here still
// renders, under Other, labelled from its name.
export const KINDS: Record<string, { label: string; category: CategoryId; about: string }> = {
  spec: { label: "Spec recorded", category: "plans", about: "A Spec, a written plan for one change, was committed." },
  spec_event: { label: "Spec log entry", category: "plans", about: "A line was added to a Spec's evidence log." },
  task: { label: "Task recorded", category: "plans", about: "A Task, one slice of a Spec for one agent run, was committed." },
  task_claimed: { label: "Task claimed", category: "plans", about: "An agent claimed a Task and started work on it." },
  task_receipt: { label: "Task handed back", category: "plans", about: "An agent recorded a receipt with the proof of a finished Task." },
  pr_opened: { label: "Pull request opened", category: "prs", about: "A proposed change was opened for review." },
  merge: { label: "Merged", category: "prs", about: "A reviewed change was merged into a shared branch." },
  commit: { label: "Commit", category: "commits", about: "One saved change to the files." },
  correction_fix: { label: "Fix for a correction", category: "commits", about: "The commit that fixed something a correction pointed out." },
  correction: { label: "Correction", category: "rework", about: "A review finding or an owner correction: something had to change." },
  return: { label: "Returned unmerged", category: "rework", about: "A proposed change was closed without being merged." },
};

export function kindLabel(kind: string): string {
  const known = KINDS[kind];
  if (known) return known.label;
  const words = kind.replace(/_/g, " ").trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

export function categoryOf(kind: string): CategoryId {
  return KINDS[kind]?.category ?? "other";
}

// Signal colors (DDR-000M, DDR-000Y): purple means it came back for rework;
// green means the row itself says an agent did it; everything else is grey.
const AGENT_AUTHOR = /^(?:claude|codex)\b/i;
export function toneOf(row: Pick<BuildEvent, "kind" | "detail">): Tone {
  if (row.kind === "correction" || row.kind === "return") return "returned";
  if (row.kind === "task_claimed" || row.kind === "task_receipt") return "agent";
  const author = row.detail?.author;
  if (row.kind === "commit" && typeof author === "string" && AGENT_AUTHOR.test(author)) return "agent";
  return "none";
}

// Agent session links are private traces (the site's hygiene check refuses
// them). They are removed at render; the rows are left as they are.
const SESSION_LINK = /\s*\(?\s*(?:see\s+)?(?:Claude-Session:\s*)?(?:https?:\/\/)?claude\.ai\/code\/session_[A-Za-z0-9]+\s*\)?/gi;
const SESSION_TRAILER = /\s*Claude-Session:\s*\S*/gi;
const SESSION_ID = /\s*\bsession_0[A-Za-z0-9]{20,}/g;
export function stripSessionLinks(text: string): string {
  return text.replace(SESSION_LINK, " ").replace(SESSION_TRAILER, " ").replace(SESSION_ID, " ").replace(/\s+/g, " ").trim();
}

// Times are shown in the owner's time zone.
const ZONE = "America/Denver";
const timeFmt = new Intl.DateTimeFormat("en-US", { timeZone: ZONE, hour: "numeric", minute: "2-digit" });
const dayFmt = new Intl.DateTimeFormat("en-US", { timeZone: ZONE, weekday: "long", month: "long", day: "numeric", year: "numeric" });
const hourFmt = new Intl.DateTimeFormat("en-US", { timeZone: ZONE, hour: "numeric" });
const zoneFmt = new Intl.DateTimeFormat("en-US", { timeZone: ZONE, timeZoneName: "short" });

export function eventTime(iso: string): string {
  return timeFmt.format(new Date(iso));
}

const HOUR = 3600 * 1000;
const hourStart = (iso: string) => Math.floor(new Date(iso).getTime() / HOUR) * HOUR;

// The heading of the hour an event falls in, e.g. "Sunday, November 1, 2026,
// 6 AM to 7 AM MST". The zone's offsets are whole hours, so a UTC hour is a
// local hour.
export function groupLabel(iso: string): string {
  const start = new Date(hourStart(iso));
  const end = new Date(start.getTime() + HOUR);
  const zone = zoneFmt.formatToParts(start).find((p) => p.type === "timeZoneName")?.value ?? "";
  return `${dayFmt.format(start)}, ${hourFmt.format(start)} to ${hourFmt.format(end)} ${zone}`.trim();
}

const httpsUrl = (url: string | null) => {
  if (!url) return false;
  try {
    return new URL(url).protocol === "https:";
  } catch {
    return false;
  }
};

export type HistoryEvent = { row: BuildEvent; summary: string; subject: string; category: CategoryId; tone: Tone };
export type HistoryGroup = { key: string; label: string; events: HistoryEvent[] };
export type HistoryView = {
  events: HistoryEvent[];
  groups: HistoryGroup[];
  skipped: number;
  counts: { id: CategoryId; label: string; count: number }[];
};

// Rows to what the page shows: test rows dropped, rows with no https source
// or no text counted and not shown, the rest ordered by occurred_at then id
// and grouped by hour.
export function historyView(rows: readonly BuildEvent[]): HistoryView {
  const real = rows.filter((r) => r && r.is_test === false && typeof r.occurred_at === "string" && !Number.isNaN(Date.parse(r.occurred_at)));
  const events: HistoryEvent[] = [];
  let skipped = 0;
  for (const row of real) {
    const summary = stripSessionLinks(String(row.summary ?? ""));
    const subject = stripSessionLinks(String(row.subject ?? ""));
    if (!httpsUrl(row.source_url) || !summary) {
      skipped += 1;
      continue;
    }
    events.push({ row, summary, subject, category: categoryOf(row.kind), tone: toneOf(row) });
  }
  events.sort((a, b) => Date.parse(a.row.occurred_at) - Date.parse(b.row.occurred_at) || a.row.id - b.row.id);
  const groups: HistoryGroup[] = [];
  for (const event of events) {
    const key = String(hourStart(event.row.occurred_at));
    let group = groups[groups.length - 1];
    if (!group || group.key !== key) {
      group = { key, label: groupLabel(event.row.occurred_at), events: [] };
      groups.push(group);
    }
    group.events.push(event);
  }
  const counts = CATEGORIES.map((c) => ({ id: c.id, label: c.label, count: events.filter((e) => e.category === c.id).length })).filter((c) => c.count > 0);
  return { events, groups, skipped, counts };
}

// Reading the rows: plain REST with the publishable key, test rows filtered
// by the query as well as by RLS, pages of 1000 followed. Never throws: a
// missing setting or a failed read gives no rows and a note saying why,
// without the address or the key.
const PAGE = 1000;
const MAX_PAGES = 50;
const COLUMNS = "id,kind,subject,summary,occurred_at,source_url,is_test,detail";

type FetchLike = (url: string, init?: RequestInit & { next?: { revalidate?: number } }) => Promise<Response>;

export async function readBuildEvents({ url, key, fetchImpl, revalidate = 600 }: { url?: string; key?: string; fetchImpl?: FetchLike; revalidate?: number }): Promise<{ rows: BuildEvent[]; note: string | null }> {
  if (!url || !key) return { rows: [], note: "The build history could not be read: the Supabase address or publishable key is not set for this build." };
  const doFetch: FetchLike = fetchImpl ?? ((u, init) => fetch(u, init));
  const rows: BuildEvent[] = [];
  try {
    for (let page = 0; page < MAX_PAGES; page += 1) {
      const q = new URL("/rest/v1/build_events", url);
      q.searchParams.set("select", COLUMNS);
      q.searchParams.set("is_test", "is.false");
      q.searchParams.set("order", "occurred_at.asc,id.asc");
      q.searchParams.set("limit", String(PAGE));
      q.searchParams.set("offset", String(page * PAGE));
      const res = await doFetch(q.toString(), {
        method: "GET",
        headers: { apikey: key, Authorization: `Bearer ${key}`, Accept: "application/json" },
        signal: AbortSignal.timeout(15000),
        next: { revalidate },
      });
      if (!res.ok) return { rows: [], note: `The build history could not be read: Supabase answered ${res.status}.` };
      const body: unknown = await res.json();
      if (!Array.isArray(body)) return { rows: [], note: "The build history could not be read: Supabase sent something other than a list of rows." };
      rows.push(...(body as BuildEvent[]));
      if (body.length < PAGE) break;
    }
  } catch {
    return { rows: [], note: "The build history could not be read: the request to Supabase failed." };
  }
  return { rows, note: null };
}

// Rendering.

type Styles = Readonly<Record<string, string>>;
const cx = (styles: Styles, ...names: string[]) => names.map((n) => styles[n] ?? "").filter(Boolean).join(" ") || undefined;

const S006_SPEC = "https://github.com/KaydenClark/Agentic-Management-System/blob/dev/workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md";

function EmptyState({ note, styles }: { note: string | null; styles: Styles }): ReactNode {
  return h(
    "div",
    { className: cx(styles, "empty"), "data-empty-state": "" },
    h("p", { className: cx(styles, "emptyTitle") }, note ? "No build events can be shown right now." : "No build events are recorded yet."),
    note ? h("p", { "data-read-note": "" }, note) : null,
    h(
      "p",
      { "data-next-event": "" },
      h("strong", null, "Next expected event:"),
      " the history import of the RSI data store (S-006) writes the next Spec, Task, pull request or commit row to Supabase, and this page shows it the next time the page is rebuilt. Source: ",
      h("a", { href: S006_SPEC }, "S-006, RSI data store"),
      ".",
    ),
  );
}

function Event({ event, styles }: { event: HistoryEvent; styles: Styles }): ReactNode {
  const { row } = event;
  return h(
    "li",
    { className: cx(styles, "event"), "data-event": "", "data-row-id": String(row.id), "data-kind": row.kind, "data-category": event.category },
    h(
      "span",
      { className: cx(styles, "meta") },
      h("span", { className: `tone h-${event.tone} ${cx(styles, "badge") ?? ""}`.trim(), "data-field": "kind" }, kindLabel(row.kind)),
      " ",
      h("time", { className: cx(styles, "time"), dateTime: row.occurred_at, "data-field": "time" }, eventTime(row.occurred_at)),
    ),
    " ",
    h("a", { className: cx(styles, "summary"), href: row.source_url ?? undefined, "data-field": "summary" }, event.summary),
    " ",
    h("span", { className: cx(styles, "subject"), "data-field": "subject" }, event.subject),
  );
}

export function History({ view, note = null, styles = {}, labelledBy }: { view: HistoryView; note?: string | null; styles?: Styles; labelledBy?: string }): ReactNode {
  if (!view.events.length) return h(EmptyState, { note, styles });
  const n = view.events.length;
  const s = view.skipped;
  const skippedText = s ? ` ${s} ${s === 1 ? "row" : "rows"} not shown because ${s === 1 ? "it has" : "they have"} no https source link or no text.` : "";
  return h(
    "section",
    { className: cx(styles, "history"), "data-history": "", "aria-labelledby": labelledBy },
    h("p", { className: cx(styles, "totals"), "data-totals": "" }, `${n} ${n === 1 ? "event" : "events"}, oldest first.${skippedText}`),
    h(
      "fieldset",
      { className: cx(styles, "filter"), "data-filter": "" },
      h("legend", null, "Show"),
      ...view.counts.map((c) =>
        h(
          "label",
          { key: c.id, className: cx(styles, "filterOption") },
          h("input", { type: "checkbox", defaultChecked: true, "data-filter-for": c.id, className: cx(styles, "check") }),
          ` ${c.label} (${c.count})`,
        ),
      ),
    ),
    ...view.groups.map((group, i) =>
      h(
        "details",
        { key: group.key, className: cx(styles, "group"), "data-group": group.key, open: i === 0 ? true : undefined },
        h(
          "summary",
          { className: cx(styles, "groupSummary") },
          h("span", { className: cx(styles, "when"), "data-field": "when" }, group.label),
          " ",
          h("span", { className: cx(styles, "count"), "data-field": "count" }, `${group.events.length} ${group.events.length === 1 ? "event" : "events"}`),
        ),
        h("ol", { className: cx(styles, "events") }, ...group.events.map((event) => h(Event, { key: event.row.id, event, styles }))),
      ),
    ),
  );
}
