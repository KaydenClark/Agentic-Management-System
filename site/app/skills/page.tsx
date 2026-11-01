// /skills: the skills wiki index (S-008). Kayden's skills grouped by the
// chart's seven Workbench stages, in chart order (app/start/skills.mjs), each
// stage with its gloss and note; main-flow skills first in the order they
// run, then the skills also used at that stage. Each entry is an article in
// content/skills/ and links its page.
import type { Metadata } from "next";
import Link from "next/link";
import { stages } from "../start/skills.mjs";
import { loadArticles } from "./content.mjs";
import type { Article } from "./content.mjs";
import { InlineNodes } from "./Markdown";
import styles from "./skills.module.css";

export const metadata: Metadata = {
  title: "Skills | Agentic Management System",
  description: "Articles on Kayden's skills, the written methods the agents load, grouped by the Workbench stage each one serves.",
};

function Entry({ article }: { article: Article }) {
  return (
    <li className={article.flow === "main" ? styles.entryMain : styles.entryUsed} data-skill={article.name} data-flow={article.flow}>
      {article.step ? (
        <span className={styles.step} aria-hidden="true">
          {article.step}
        </span>
      ) : null}
      <div className={styles.entryBody}>
        <Link className={styles.entryLink} href={`/skills/${article.name}`}>
          {article.name}
        </Link>
        <p className={styles.entrySummary} data-summary="">
          <InlineNodes nodes={article.summary} />
        </p>
      </div>
    </li>
  );
}

export default function SkillsIndex() {
  const articles = loadArticles();
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Skills wiki</p>
        <h1>Skills</h1>
        <p className="lede">
          A skill is a written method an agent loads before it does one kind of work, such as questioning a plan,
          building a Task or landing a change. These articles explain Kayden&apos;s skills in plain words, grouped by
          the Workbench stage each one serves, in the order of the chart on <Link href="/start">Start here</Link>. The
          skills themselves are kept private; each article is written for this site from one pinned commit of them,
          named at its end.
        </p>
      </header>

      <nav aria-label="Stages" className={styles.stageNav}>
        <ol>
          {stages.map((st) => (
            <li key={st.id}>
              <a href={`#${st.id}`}>{st.name}</a>
            </li>
          ))}
        </ol>
      </nav>

      {stages.map((st) => {
        const main = st.main.flatMap((n) => articles.filter((a) => a.name === n));
        const used = st.used.flatMap((n) => articles.filter((a) => a.name === n));
        return (
          <section key={st.id} id={st.id} className={styles.stage} aria-labelledby={`${st.id}-title`} data-stage={st.id}>
            <div className={styles.stageHead}>
              <h2 id={`${st.id}-title`}>{st.name}</h2>
              <p className={styles.gloss}>{st.gloss}</p>
              {st.note ? <p className={styles.note}>{st.note}</p> : null}
            </div>
            {main.length ? (
              <>
                <h3 className={styles.flowHead}>Main flow, in order</h3>
                <ol className={styles.entries} data-flow="main">
                  {main.map((a) => (
                    <Entry key={a.name} article={a} />
                  ))}
                </ol>
              </>
            ) : null}
            {used.length ? (
              <>
                <h3 className={styles.flowHead}>Also used at this stage</h3>
                <ul className={styles.entries} data-flow="used">
                  {used.map((a) => (
                    <Entry key={a.name} article={a} />
                  ))}
                </ul>
              </>
            ) : null}
            {!main.length && !used.length ? <p className={styles.gloss}>No articles in this stage yet.</p> : null}
          </section>
        );
      })}
    </div>
  );
}
