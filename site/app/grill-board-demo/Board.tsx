"use client";

// Interactive part of the demo Grill Board. All state lives in this component:
// nothing is sent over the network, written to storage or kept after a reload.

import { useMemo, useState, type ReactNode } from "react";
import type { Card, Grade, Topic } from "./data";

type Verdict = "confirm" | "wording" | "why" | "change" | "later";
type LaneKey = "open" | "pending" | "stale" | "answered" | "later" | "applied" | "settled";
type Sort = "vp" | "pv" | "rev";

const LANES: { key: LaneKey; label: string; hue: string; rest: boolean }[] = [
  { key: "open", label: "All open", hue: "h-none", rest: false },
  { key: "pending", label: "To answer", hue: "h-owner", rest: false },
  { key: "stale", label: "Revisit", hue: "h-returned", rest: false },
  { key: "answered", label: "Answered · awaiting an agent", hue: "h-agent", rest: false },
  { key: "later", label: "Not now", hue: "h-owner", rest: true },
  { key: "applied", label: "Applied", hue: "h-agent", rest: true },
  { key: "settled", label: "Settled elsewhere", hue: "h-none", rest: true },
];
const LANE_NAME: Record<string, string> = {
  pending: "To answer",
  stale: "Revisit · re-answer",
  answered: "Answered · awaiting an agent",
  later: "Not now",
};
const LANE_HUE: Record<string, string> = { pending: "h-owner", stale: "h-returned", answered: "h-agent", later: "h-owner" };
const SCALE_BARS = { Blueprint: 4, Landmark: 3, Spec: 2, Task: 1 } as const;
const SCALE_LONG = {
  Blueprint: "Blueprint · the whole plan",
  Landmark: "Landmark · a direction",
  Spec: "Spec · one piece",
  Task: "Task · one step",
} as const;
const KINDS = ["Explore / settle decisions", "Unblock / direct work", "Review existing work"];
const rank = (g: Grade) => Number(g.slice(1));
const gradeClass = (g: Grade) => "grade n" + g.slice(1);

function Octagon() {
  return (
    <svg className="gl" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M8 2h8l6 6v8l-6 6H8l-6-6V8z" />
      <path d="M12 8v4" />
      <path d="M12 16h.01" />
    </svg>
  );
}
function Triangle() {
  return (
    <svg className="gl" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 4 2 20h20z" />
      <path d="M12 10v4" />
      <path d="M12 17h.01" />
    </svg>
  );
}
function FlagIcon({ flag }: { flag?: "block" | "risk" }) {
  return flag === "block" ? <Octagon /> : flag === "risk" ? <Triangle /> : null;
}

export default function Board({ topics, cards, children }: { topics: Topic[]; cards: Card[]; children?: ReactNode }) {
  const [topicKey, setTopicKey] = useState(topics[0].key);
  const [lane, setLane] = useState<LaneKey>("open");
  const [selId, setSelId] = useState(cards.find((c) => c.topic === topics[0].key)!.id);
  const [verdicts, setVerdicts] = useState<Record<string, Verdict>>({});
  const [picks, setPicks] = useState<Record<string, string>>({});
  const [ratings, setRatings] = useState<Record<string, number>>({});
  const [taxing, setTaxing] = useState<Record<string, boolean>>({});
  const [batch, setBatch] = useState<Record<string, boolean>>({});
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [comments, setComments] = useState<Record<string, string>>({});
  const [savedComment, setSavedComment] = useState<Record<string, boolean>>({});
  const [pFilter, setPFilter] = useState<Grade[]>([]);
  const [vFilter, setVFilter] = useState<Grade[]>([]);
  const [scaleFilter, setScaleFilter] = useState("");
  const [kindFilter, setKindFilter] = useState("");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<Sort>("vp");
  const [batchSize, setBatchSize] = useState(5);

  const laneOf = (c: Card): LaneKey => {
    const v = verdicts[c.id];
    if (v === "confirm") return "answered";
    if (v === "later") return "later";
    return c.lane;
  };

  const topic = topics.find((t) => t.key === topicKey) ?? topics[0];
  const inTopic = cards.filter((c) => c.topic === topic.key);

  const sorted = useMemo(() => {
    const list = [...cards];
    list.sort((a, b) => {
      if (sort === "rev") return b.rev - a.rev;
      if (sort === "pv") return rank(a.p) - rank(b.p) || rank(a.v) - rank(b.v);
      return rank(a.v) - rank(b.v) || rank(a.p) - rank(b.p);
    });
    return list;
  }, [cards, sort]);

  const needle = search.trim().toLowerCase();
  const isShown = (c: Card) =>
    c.topic === topic.key &&
    (lane === "open" || laneOf(c) === lane) &&
    (pFilter.length === 0 || pFilter.includes(c.p)) &&
    (vFilter.length === 0 || vFilter.includes(c.v)) &&
    (!scaleFilter || c.scale === scaleFilter) &&
    (!kindFilter || c.kind === kindFilter) &&
    (!needle || [c.short, c.title, c.q, c.why].some((s) => s.toLowerCase().includes(needle)));
  const shown = sorted.filter(isShown);

  const sel = cards.find((c) => c.id === selId) ?? cards[0];
  const verdict = verdicts[sel.id] ?? null;
  const pick = picks[sel.id] ?? null;
  const rating = ratings[sel.id] ?? 0;
  const order = shown.length ? shown : sorted.filter((c) => c.topic === topic.key);
  const idx = Math.max(0, order.findIndex((c) => c.id === sel.id));
  const go = (d: number) => setSelId(order[(idx + d + order.length) % order.length].id);
  const setVerdict = (name: Verdict) => setVerdicts({ ...verdicts, [sel.id]: name });

  const answeredNow = Object.keys(verdicts).length;
  const confirmedNow = Object.values(verdicts).filter((x) => x === "confirm").length;
  const pickedCount = Object.values(batch).filter(Boolean).length;
  const totalConfirmed = cards.filter((c) => verdicts[c.id] === "confirm").length;

  const pickTopic = (key: string) => {
    setTopicKey(key);
    setLane("open");
    const first = sorted.find((c) => c.topic === key);
    if (first) setSelId(first.id);
  };
  const toggleGrade = (list: Grade[], set: (g: Grade[]) => void, g: Grade) =>
    set(list.includes(g) ? list.filter((x) => x !== g) : [...list, g]);
  const clearFilters = () => {
    setLane("open");
    setPFilter([]);
    setVFilter([]);
    setScaleFilter("");
    setKindFilter("");
    setSearch("");
  };

  const noteLabel =
    verdict && verdict !== "confirm" && verdict !== "later"
      ? "Note · required for this verdict"
      : "Note · optional with Confirm, required with the three change verdicts";
  const saveLine =
    verdict === "confirm"
      ? `Kept in this browser only · on the real board this is written into ${sel.owner}`
      : verdict
        ? "Kept in this browser only · nothing is sent or saved"
        : `No verdict yet · ${idx + 1} of ${order.length} shown`;

  const laneCount = (k: LaneKey) =>
    k === "open" ? inTopic.length : inTopic.filter((c) => laneOf(c) === k).length;

  return (
    <div className="gb-cols">
      {/* Left rail */}
      <aside className="gb-rail">
        {/* A picture of the real Dashboard's sections, not links: the demo has only this board. */}
        <ul aria-label="Sections of the real Dashboard (not links in this demo)" className="gb-nav">
          <li className="gb-navitem">Destination Tracker</li>
          <li className="gb-navitem">Taskboard</li>
          <li className="gb-navitem is-current">Grilling Board</li>
          <li className="gb-navitem">Drafts to approve</li>
          <li className="gb-navitem">Wiki</li>
        </ul>

        <div className="gb-topics">
          <div className="gb-topics-head">
            <span className="gb-eyebrow">Topics</span>
            <span className="gb-count">{totalConfirmed} / {cards.length}</span>
          </div>
          {topics.map((t) => {
            const tc = cards.filter((c) => c.topic === t.key);
            const done = tc.filter((c) => verdicts[c.id] === "confirm").length;
            const hasRevisit = tc.some((c) => laneOf(c) === "stale");
            const hasWaiting = tc.some((c) => laneOf(c) === "answered");
            return (
              <button key={t.key} type="button" className="topic gb-topic" aria-pressed={t.key === topic.key} onClick={() => pickTopic(t.key)}>
                <span className="gb-topic-line">
                  <span className="gb-topic-label">{t.label}</span>
                  <span className="gb-count">{done}/{tc.length}</span>
                </span>
                <span className="gb-topic-bar">
                  <span className="gb-track"><span className="gb-fill" style={{ width: `${Math.round((100 * done) / tc.length)}%` }} /></span>
                  {hasRevisit && <span className="dot tone h-returned" title="Has a question to re-answer" />}
                  {hasWaiting && <span className="dot tone h-agent" title="Has answers awaiting an agent" />}
                </span>
              </button>
            );
          })}
        </div>

        <section aria-label="Rounds and promotion" className="gb-round">
          <div className="gb-eyebrow">This round</div>
          <div className="gb-round-line">Round 1 · {answeredNow} answered, {confirmedNow} confirmed</div>
          <button type="button" className="ghost semibold">End this round</button>
          <div className="gb-small">Records which cards are confirmed. Starts no agent, promotes nothing.</div>
          <div className="gb-rule" />
          <div className="gb-ready">
            <span className="dot tone h-agent" />
            <span className="grow">Confirmed, ready to promote</span>
            <span className="gb-round-count">{confirmedNow}</span>
          </div>
          <button type="button" className="ghost">Promote selected…</button>
          <div className="gb-small">In this demo, nothing is handed to an agent.</div>
        </section>

        <div className="gb-raillinks">
          <a className="textlink" href="#where-answers-go">Where a confirmed answer goes</a>
          <a className="textlink" href="#where-answers-go">About these sample questions</a>
        </div>
      </aside>

      {/* Question queue */}
      <section aria-label="Question queue" className="gb-queue">
        <div className="gb-qhead">
          <h2 className="gb-h1" data-topic-title="">{topic.label}</h2>
          <p className="gb-frame">Think about <span className="ink">{"{ " + topic.frame + " }"}</span></p>
          <div className="gb-progress-wrap">
            <div className="gb-progress">
              <div style={{ width: `${Math.round((100 * inTopic.filter((c) => verdicts[c.id] === "confirm").length) / inTopic.length)}%` }} />
            </div>
            <div className="gb-small">
              {inTopic.filter((c) => verdicts[c.id] === "confirm").length} of {inTopic.length} answered · {topic.goal}
            </div>
          </div>
        </div>

        <div role="group" aria-label="Where it is in the workflow" className="gb-lanes">
          {LANES.map((l) => (
            <button key={l.key} type="button" className="lane gb-lane" aria-pressed={l.key === lane} onClick={() => setLane(l.key)}>
              <span className={"dot tone " + l.hue + (l.rest ? " rest" : "")} />
              {l.label}
              <span className="gb-count">{laneCount(l.key)}</span>
            </button>
          ))}
        </div>

        <div className="gb-filters">
          <div role="group" aria-label="Priority" className="gb-chips">
            {(["P1", "P2", "P3", "P4"] as Grade[]).map((g) => (
              <button key={g} type="button" className={"chip " + gradeClass(g)} aria-pressed={pFilter.includes(g)} onClick={() => toggleGrade(pFilter, setPFilter, g)}>{g}</button>
            ))}
          </div>
          <div role="group" aria-label="Value" className="gb-chips">
            {(["V1", "V2", "V3", "V4"] as Grade[]).map((g) => (
              <button key={g} type="button" className={"chip " + gradeClass(g)} aria-pressed={vFilter.includes(g)} onClick={() => toggleGrade(vFilter, setVFilter, g)}>{g}</button>
            ))}
          </div>
          <details className="gb-more">
            <summary>More filters</summary>
            <div className="gb-more-in">
              <label htmlFor="gb-scale" className="sr-only">Scale</label>
              <select id="gb-scale" className="gb-select" value={scaleFilter} onChange={(e) => setScaleFilter(e.target.value)}>
                <option value="">Any scale</option>
                {(Object.keys(SCALE_LONG) as (keyof typeof SCALE_LONG)[]).map((s) => (
                  <option key={s} value={s}>{SCALE_LONG[s]}</option>
                ))}
              </select>
              <label htmlFor="gb-kind" className="sr-only">Kind of decision</label>
              <select id="gb-kind" className="gb-select" value={kindFilter} onChange={(e) => setKindFilter(e.target.value)}>
                <option value="">Any kind of decision</option>
                {KINDS.map((k) => (
                  <option key={k} value={k}>{k}</option>
                ))}
              </select>
              <label htmlFor="gb-qsearch" className="sr-only">Search these questions</label>
              <input id="gb-qsearch" type="search" className="gb-select gb-search-q" placeholder="Titles, questions, text…" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
          </details>
          <button type="button" className="gb-clear" onClick={clearFilters}>Clear</button>
        </div>

        <div className="gb-batch">
          <label htmlFor="gb-batch">Batch</label>
          <select id="gb-batch" className="gb-select" value={batchSize} onChange={(e) => setBatchSize(Number(e.target.value))}>
            <option value={3}>3 questions</option>
            <option value={5}>5 questions</option>
            <option value={10}>10 questions</option>
          </select>
          <button type="button" className="inkbtn" onClick={() => shown[0] && setSelId(shown[0].id)}>Start next {batchSize}</button>
          <button
            type="button"
            className="ghost"
            onClick={() => {
              const first = shown.find((c) => batch[c.id]);
              if (first) setSelId(first.id);
            }}
          >
            Start selected ({pickedCount})
          </button>
          <span className="gb-sort">
            <label htmlFor="gb-sort">Sort</label>
            <select id="gb-sort" className="gb-select" value={sort} onChange={(e) => setSort(e.target.value as Sort)}>
              <option value="vp">Value, then Priority</option>
              <option value="pv">Priority, then Value</option>
              <option value="rev">Newest revision</option>
            </select>
          </span>
        </div>

        <div className="gb-rows">
          {sorted.map((c) => {
            const n = SCALE_BARS[c.scale];
            const vd = verdicts[c.id];
            const current = c.id === sel.id;
            const dotHue = vd === "confirm" ? "h-agent" : vd === "later" ? "h-owner" : vd ? "h-returned" : LANE_HUE[c.lane];
            return (
              <div key={c.id} className="gb-rowwrap" hidden={!isShown(c)}>
                <label className="gb-pick">
                  <input type="checkbox" className="check" checked={!!batch[c.id]} onChange={() => setBatch({ ...batch, [c.id]: !batch[c.id] })} aria-label="Add to the batch" />
                </label>
                <button
                  type="button"
                  data-card-row={c.id}
                  className={"gb-row " + (current ? "row is-current" : "row")}
                  onClick={() => setSelId(c.id)}
                  aria-current={current ? "true" : undefined}
                >
                  <span className={"dot tone " + dotHue + (vd === "later" ? " rest" : "")} />
                  <span className="gb-row-main">
                    <span className="clamp gb-row-short">{c.short}</span>
                    <span className="gb-row-meta">
                      <span className="sample">Sample</span>
                      <span className="mono">{c.id}</span>
                      <span className="gb-bars" aria-hidden="true">
                        {[1, 2, 3, 4].map((k) => (
                          <span key={k} className={`bar bar-${k}${n >= k ? " on" : ""}`} />
                        ))}
                      </span>
                      <span>{c.scale}</span>
                      {c.lane === "stale" && !vd && (
                        <span className="tone h-returned gb-reanswer">· Re-answer</span>
                      )}
                      {taxing[c.id] && <span>· Too taxing</span>}
                    </span>
                    {c.flag && (
                      <span className="tone h-heat gb-flag">
                        <FlagIcon flag={c.flag} />
                        {c.flagText}
                      </span>
                    )}
                  </span>
                  <span className="gb-grades">
                    <span className={gradeClass(c.p)}>{c.p}</span>
                    <span className={gradeClass(c.v)}>{c.v}</span>
                  </span>
                </button>
              </div>
            );
          })}
          {shown.length === 0 && <div className="gb-empty">Nothing here needs you.</div>}
          <div className="gb-moreline">All {inTopic.length} sample questions in this topic are shown.</div>
        </div>
      </section>

      {/* The open card */}
      <section aria-label="The open card" className="gb-main">
        <article className="gb-card" data-open-card={sel.id} aria-label={"Sample card " + sel.id}>
          <div className="gb-cardmeta">
            <span className="sample">Sample</span>
            <span className={"tone gb-pill " + LANE_HUE[laneOf(sel)]}>
              <span className={"dot" + (laneOf(sel) === "later" ? " rest" : "")} />
              {LANE_NAME[laneOf(sel)]}
            </span>
            <span className="mono gb-metatext">{sel.id} · revision {sel.rev}</span>
            <span className="gb-metatext">{SCALE_LONG[sel.scale]} · {sel.kind}</span>
            {sel.flag && (
              <span className="tone h-heat gb-pill">
                <FlagIcon flag={sel.flag} />
                {sel.flagText}
              </span>
            )}
          </div>

          <h3 className="gb-h2">{sel.title}</h3>

          <div className="gb-why2">
            <details className="gb-whygrade">
              <summary><span className={gradeClass(sel.p)}>{sel.p}</span><span>Priority · why this grade</span></summary>
              <p>{sel.pWhy}</p>
            </details>
            <details className="gb-whygrade">
              <summary><span className={gradeClass(sel.v)}>{sel.v}</span><span>Value · why this grade</span></summary>
              <p>{sel.vWhy}</p>
            </details>
          </div>

          <div className="gb-block">
            <div className="gb-eyebrow">The question</div>
            <p className="gb-q">{sel.q}</p>
          </div>

          <div className="tone h-worth gb-box gb-box-worth">
            <div className="gb-boxhead">Why this choice matters</div>
            <p>{sel.why}</p>
          </div>

          <div className="tone h-agent gb-box gb-box-agent">
            <div className="gb-boxhead"><span className="dot rest" />Agent recommendation</div>
            <p>{sel.rec}</p>
          </div>

          <fieldset className="gb-opts">
            <legend className="gb-eyebrow">Pick an alternative</legend>
            {sel.options.map((o) => (
              <button
                key={o.key}
                type="button"
                className="opt tone h-agent gb-opt"
                aria-pressed={pick ? pick === o.key : !!o.recommended}
                onClick={() => setPicks({ ...picks, [sel.id]: o.key })}
              >
                <span className="radio" />
                <span className="gb-opt-text">
                  <span className="semibold">{o.label}</span>
                  <span className="gb-opt-hint">{o.hint}</span>
                </span>
                {o.recommended && <span className="tone h-agent outline gb-rectag">Recommended</span>}
              </button>
            ))}
          </fieldset>

          <section aria-label="What this concerns" className="gb-concerns">
            <div className="gb-eyebrow">What this concerns</div>
            <ul>
              {sel.concerns.map((c) => (
                <li key={c.name}>
                  <span className="textlink semibold">{c.name}</span>{" "}
                  <span className="quiet">— {c.note}</span>
                </li>
              ))}
            </ul>
            <div className="gb-wikirow">
              <span className="quiet">Read in the Wiki</span>
              {sel.wiki.map((w) => (
                <span key={w} className="wikichip">{w}</span>
              ))}
            </div>
            {sel.draft && (
              <span className="textlink gb-draftlink">Open the proposed wording in Drafts to approve →</span>
            )}
          </section>

          <div className="gb-folds">
            <details>
              <summary>Proposed changes</summary>
              <p>{sel.changes}</p>
            </details>
            <details>
              <summary>Consequences</summary>
              <p>{sel.impact}</p>
            </details>
            <details>
              <summary>History · {sel.historyCount}</summary>
              <p>{sel.history}</p>
            </details>
          </div>

          <div className="gb-verdict">
            <div className="gb-eyebrow">Your verdict</div>

            {taxing[sel.id] && (
              <div className="tone h-returned gb-callout">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M9 14 4 9l5-5" />
                  <path d="M4 9h11a5 5 0 0 1 0 10h-3" />
                </svg>
                <span>Flagged as too taxing. On the real board this question is rewritten before it is asked again.</span>
              </div>
            )}

            <div className="gb-verdicts">
              <button type="button" className="verdict confirm tone h-agent" aria-pressed={verdict === "confirm"} onClick={() => setVerdict("confirm")}>Confirm</button>
              <button type="button" className="verdict change tone h-returned" aria-pressed={verdict === "wording"} onClick={() => setVerdict("wording")}>Rework wording</button>
              <button type="button" className="verdict change tone h-returned" aria-pressed={verdict === "why"} onClick={() => setVerdict("why")}>Change the why</button>
              <button type="button" className="verdict change tone h-returned" aria-pressed={verdict === "change"} onClick={() => setVerdict("change")}>Change</button>
              <button type="button" className="verdict later tone h-owner" aria-pressed={verdict === "later"} onClick={() => setVerdict("later")}>Not now</button>
            </div>
            <label htmlFor="gb-note" className="gb-note-label">{noteLabel}</label>
            <textarea
              id="gb-note"
              rows={3}
              className="gb-textarea"
              placeholder="What should change, in your words"
              value={notes[sel.id] ?? ""}
              onChange={(e) => setNotes({ ...notes, [sel.id]: e.target.value })}
            />

            <div className="gb-ratebar">
              <span>Was this a good question?</span>
              <span role="group" aria-label="Rate this question, one to five" className="gb-stars">
                {[1, 2, 3, 4, 5].map((k) => (
                  <button key={k} type="button" className="star" aria-pressed={k <= rating} aria-label={`${k} of 5`} onClick={() => setRatings({ ...ratings, [sel.id]: k })}>★</button>
                ))}
              </span>
              <button type="button" className="taxing" aria-pressed={!!taxing[sel.id]} onClick={() => setTaxing({ ...taxing, [sel.id]: !taxing[sel.id] })}>Too taxing</button>
            </div>

            <details className="gb-comment">
              <summary>Comment on this question</summary>
              <div className="gb-comment-in">
                <label htmlFor="gb-qcomment" className="sr-only">Comment on this question</label>
                <textarea
                  id="gb-qcomment"
                  rows={2}
                  className="gb-textarea"
                  placeholder="A note for the agents; it does not answer the question"
                  value={comments[sel.id] ?? ""}
                  onChange={(e) => {
                    setComments({ ...comments, [sel.id]: e.target.value });
                    setSavedComment({ ...savedComment, [sel.id]: false });
                  }}
                />
                <button type="button" className="ghost" onClick={() => setSavedComment({ ...savedComment, [sel.id]: true })}>
                  {savedComment[sel.id] ? "Kept in this browser" : "Save comment"}
                </button>
              </div>
            </details>

            <div className="gb-foot">
              <span aria-live="polite">{saveLine}</span>
              <span className="gb-foot-nav">
                <button type="button" className="ghost" onClick={() => go(-1)}>Previous</button>
                <button type="button" className="inkbtn" onClick={() => go(1)}>Next question</button>
              </span>
            </div>
          </div>
        </article>
        {children}
      </section>
    </div>
  );
}
