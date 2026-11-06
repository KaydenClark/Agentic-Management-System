import { Signal } from "../components/Signal";
import { readState } from "./read-state";
import type { BuildActivity, ReadResult } from "./supabase";
import styles from "./rsi.module.css";

export function ActivityEvidence({ loaded, now }: { loaded: ReadResult<BuildActivity>; now?: number }) {
  const state = readState(loaded, loaded.data.events.length === 0 && loaded.data.unsupported === 0, now);
  const events = [...loaded.data.events].sort((a, b) => Date.parse(b.occurred_at) - Date.parse(a.occurred_at) || b.id - a.id);
  // Bounded display, not a fabricated sample: every shown row comes from the
  // public reader. New supported rows require no source edit or manual list.
  const shown = events.slice(0, 50);
  return (
    <section className={styles.place} aria-labelledby="public-activity" data-activity="" data-read-state={state === "populated" && !events.length && loaded.data.unsupported ? "unsupported" : state}>
      <h2 id="public-activity">Recorded project activity</h2>
      <p>These public records describe what happened in the project. A merge is recorded activity, not evidence of useful improvement. Alignment assessments judge controls and evidence; useful improvement needs a qualified comparison and later use. The linked failure, repair, adoption and later-use lifecycle is not yet supplied by this public feed.</p>
      {state === "failed" ? (
        <Signal kind="heat" label="Activity unavailable"><p>Activity could not be loaded. The event count and last successful read are unknown for this response; a failed read cannot establish no activity.</p></Signal>
      ) : (
        <>
          {state === "stale" ? <Signal kind="heat" label="Activity may be stale"><p>The retained successful read is older than five minutes. Its refresh outcome is unknown; the server retries on later requests. This retained record may omit newer activity.</p></Signal> : null}
          <p className={styles.muted} data-review-exclude="">Last successful activity read: <time dateTime={loaded.readAt!}>{loaded.readAt}</time>. Status is assessed when the server renders this page.</p>
          {loaded.data.unsupported ? <p data-unsupported="">{loaded.data.unsupported} public rows are unsupported or refused and are not displayed. Only exact Git-derived merge facts have a reviewed public contract here; the complete activity count remains unknown.</p> : null}
          {shown.length ? (
            <>
              <p>Showing the latest {shown.length} of {events.length} supported merge events, ordered by event time. Read time, event time and record time have different meanings.</p>
              <details>
                <summary>Read the recorded events and their sources</summary>
                <ol className={styles.points}>
                  {shown.map((event) => (
                    <li key={event.id} id={`rsi-event-${event.id}`} className={styles.row} data-activity-event="">
                      <p><a href={`#rsi-event-${event.id}`}>Event {event.id}</a>: <strong>Git merge for PR {event.subject}</strong>. Kind <code>{event.kind}</code>; subject <code>{event.subject}</code>.</p>
                      <p>Occurred <time dateTime={event.occurred_at}>{event.occurred_at}</time>; recorded <time dateTime={event.recorded_at}>{event.recorded_at}</time>. Strength: <span data-strength="">{event.strength.replaceAll("_", " ")}</span>.</p>
                      <p>Source: <code>{event.source_kind} {event.source_ref}</code>{event.source_url ? <>. Source URL: <code>{event.source_url}</code></> : ". Source URL not recorded."}</p>
                    </li>
                  ))}
                </ol>
              </details>
            </>
          ) : loaded.data.unsupported ? <p>No supported merge facts can be displayed from this read; that does not establish no activity.</p> : <p>No public activity events were present at this successful read{state === "stale" ? "; current activity remains unknown" : ""}.</p>}
        </>
      )}
    </section>
  );
}
