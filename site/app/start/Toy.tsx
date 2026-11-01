"use client";

// The /start toy: the reader moves one sample piece of work through the real
// lifecycle in flow.ts. It holds its state in memory only: no request, no
// storage, no cookie. Before scripts run (and without them) it renders every
// stage as a numbered list, so the server-rendered page carries all the text.
import { useEffect, useRef, useState } from "react";
import { HOLDERS, SAMPLE, lastStage, mainPath, stageById, stages, type Stage } from "./flow";
import { SourceLinks } from "./SourceLinks";
import styles from "./toy.module.css";

function Fallback() {
  return (
    <ol className={styles.fallback} data-toy-fallback="">
      {stages.map((s) => (
        <li key={s.id} data-stage={s.id} className={`tone ${HOLDERS[s.holder].hue} ${styles.fallbackItem}`}>
          <p className={styles.fallbackHead}>
            <strong>{s.name}</strong> <span className={styles.who}>{HOLDERS[s.holder].label}</span>
          </p>
          <p>{s.line}</p>
          {s.back ? (
            <p className={styles.branchNote}>
              {s.next?.label}: on to {stageById(s.next?.to ?? "").name}. {s.back.label}: to {stageById(s.back.to).name}.
            </p>
          ) : s.branch && s.next ? (
            <p className={styles.branchNote}>Then back to {stageById(s.next.to).name}.</p>
          ) : null}
          <SourceLinks sources={s.sources} />
        </li>
      ))}
    </ol>
  );
}

export function Toy() {
  const [live, setLive] = useState(false);
  const [trail, setTrail] = useState<string[]>([stages[0].id]);
  const [returns, setReturns] = useState(0);
  const primary = useRef<HTMLButtonElement>(null);
  useEffect(() => setLive(true), []);

  if (!live) return <Fallback />;

  const stage: Stage = stageById(trail[trail.length - 1]);
  const holder = HOLDERS[stage.holder];
  const atEnd = stage.id === lastStage.id;
  const onPath = mainPath.findIndex((s) => s.id === stage.id);
  const reached = new Set(trail);
  const go = (to: string) => {
    if (to === "returned") setReturns((n) => n + 1);
    setTrail((t) => [...t, to]);
  };
  const restart = () => {
    setTrail([stages[0].id]);
    setReturns(0);
    primary.current?.focus();
  };

  return (
    <div className={styles.toy} data-toy="" data-stage={stage.id} data-holder={stage.holder} data-last={lastStage.id}>
      <p className={styles.sample}>
        <span className="eyebrow">Sample work</span> {SAMPLE}
      </p>

      <ol className={styles.track} aria-label="Where the work is">
        {mainPath.map((s, i) => (
          <li
            key={s.id}
            className={`tone ${HOLDERS[s.holder].hue} ${styles.stop}`}
            data-now={s.id === stage.id ? "" : undefined}
            data-past={reached.has(s.id) && s.id !== stage.id ? "" : undefined}
            aria-current={s.id === stage.id ? "step" : undefined}
          >
            <span className={styles.stopDot} aria-hidden="true" />
            <span className={styles.stopName}>
              <span className={styles.visuallyHidden}>{i + 1}. </span>
              {s.name}
            </span>
          </li>
        ))}
      </ol>

      <div className={`tone ${holder.hue} ${styles.card}`} data-toy-card="" aria-live="polite" aria-atomic="true">
        <p className={styles.ball}>
          <span className={styles.ballDot} aria-hidden="true" />
          {holder.ball}
        </p>
        <h3 className={styles.stageName}>
          <span className={styles.stepNo}>{onPath >= 0 ? `Step ${onPath + 1} of ${mainPath.length}` : "Off the path"}</span>
          {stage.name}
        </h3>
        <p>{stage.line}</p>
        {returns > 0 ? (
          <p className={styles.returns}>
            Sent back {returns} {returns === 1 ? "time" : "times"} so far.
          </p>
        ) : null}
        <SourceLinks sources={stage.sources} />
      </div>

      <div className={styles.controls}>
        <button
          type="button"
          className={styles.button}
          onClick={() => setTrail((t) => (t.length > 1 ? t.slice(0, -1) : t))}
          disabled={trail.length === 1}
        >
          Back
        </button>
        <button
          ref={primary}
          type="button"
          className={`${styles.button} ${styles.primary}`}
          data-toy-primary=""
          onClick={() => (atEnd ? restart() : stage.next && go(stage.next.to))}
        >
          {atEnd ? "Start over" : stage.next?.label}
        </button>
        {stage.back ? (
          <button
            type="button"
            className={`${styles.button} tone h-returned ${styles.returnButton}`}
            data-toy-secondary=""
            onClick={() => stage.back && go(stage.back.to)}
          >
            {stage.back.label}
          </button>
        ) : null}
      </div>
    </div>
  );
}
