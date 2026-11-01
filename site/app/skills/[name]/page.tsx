// /skills/<name>: one skills wiki article (S-008), statically generated for
// every file in content/skills/ and nothing else (no dynamic fallback).
// Layout after aihero.dev's skill pages: the stage label (linking its place
// on the index), the skill name as title, the summary as lead, the article's
// sections, then the credit line and the skills commit it was written from.
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SKILLS_PIN_SHORT, loadArticles } from "../content.mjs";
import { Blocks, InlineNodes } from "../Markdown";
import order from "../../shell/page-order.module.css";
import styles from "../skills.module.css";

type Params = { params: Promise<{ name: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return loadArticles().map((a) => ({ name: a.name }));
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { name } = await params;
  const article = loadArticles().find((a) => a.name === name);
  return article ? { title: `${article.name} | Skills | Agentic Management System`, description: article.summaryText } : {};
}

export default async function SkillArticle({ params }: Params) {
  const { name } = await params;
  const articles = loadArticles();
  const k = articles.findIndex((a) => a.name === name);
  if (k < 0) notFound();
  const a = articles[k];
  const prev = articles[k - 1];
  const next = articles[k + 1];
  return (
    <>
      <article className={styles.article} data-skill={a.name} aria-labelledby="skill-title">
        <header className={styles.intro}>
          <p className={styles.stageLabel}>
            <Link href={`/skills#${a.stage.id}`} data-stage-link={a.stage.id}>
              {a.stage.name} stage
            </Link>
            <span>
              {" · "}
              {a.flow === "main" ? `main flow, step ${a.step} of ${a.stage.main.length}` : "also used"}
            </span>
          </p>
          <h1 id="skill-title" className={styles.title}>
            {a.name}
          </h1>
          <p className="lede" data-summary="">
            <InlineNodes nodes={a.summary} />
          </p>
        </header>
        {a.sections.map((s) => (
          <section key={s.id} className={styles.section} aria-labelledby={s.id} data-section={s.id}>
            <h2 id={s.id}>{s.title}</h2>
            <Blocks blocks={s.blocks} />
          </section>
        ))}
        <div className={styles.credit} data-credit-block="">
          <p data-credit={a.credit}>
            <InlineNodes nodes={a.creditText} />
          </p>
          <p className={styles.pin}>
            Skills commit{" "}
            <code className={styles.code} title={a.pin} data-pin={a.pin}>
              {SKILLS_PIN_SHORT}
            </code>
            {a.creditLicense ? ` · Source license: ${a.creditLicense}` : null}
          </p>
        </div>
      </article>
      {/* Wiki navigation, not article content: kept out of the content hash so
          adding an article clears no other article's approval. */}
      <nav aria-label="Skill order" className={order.order} data-review-exclude="">
        <p className={order.position}>
          Skills · {k + 1} of {articles.length}
        </p>
        <Link className={order.link} rel="prev" href={prev ? `/skills/${prev.name}` : "/skills"}>
          <span className={order.label}>Back</span>
          <span>{prev ? prev.name : "All skills"}</span>
        </Link>
        <Link className={`${order.link} ${order.next}`} rel="next" href={next ? `/skills/${next.name}` : "/skills"}>
          <span className={order.label}>Next</span>
          <span>{next ? next.name : "All skills"}</span>
        </Link>
      </nav>
    </>
  );
}
