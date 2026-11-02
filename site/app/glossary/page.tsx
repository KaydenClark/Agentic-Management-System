// /glossary: Glossary, a tour page (S-003 TK-003). Rendered from
// glossary.json, which scripts/gen-glossary.mjs generates from GLOSSARY.md
// (npm run glossary:gen); tests/glossary.test.mjs fails if either drifts, so
// this page never words a term differently from the project's one home for
// its language.
import type { Metadata } from "next";
import { Fragment, type ReactNode } from "react";
import { REPO_BLOB, Source } from "../tour/Source";
import styles from "../tour/tour.module.css";
import glossary from "./glossary.json";

export const metadata: Metadata = {
  title: "Glossary | Agentic Management System",
  description: "The shared words of the Agentic Management System, exactly as GLOSSARY.md defines them.",
};

// Markdown inline text from GLOSSARY.md: [links](path), **bold** and `code`.
// A relative link is a path from the repository root, shown on GitHub.
function Inline({ md }: { md: string }) {
  const parts: ReactNode[] = [];
  const re = /\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`/g;
  let last = 0;
  for (let m = re.exec(md); m; m = re.exec(md)) {
    if (m.index > last) parts.push(md.slice(last, m.index));
    if (m[1]) parts.push(<a key={m.index} href={/^https?:/.test(m[2]) ? m[2] : `${REPO_BLOB}${m[2]}`}>{m[1]}</a>);
    else if (m[3]) parts.push(<strong key={m.index}>{m[3]}</strong>);
    else parts.push(<code key={m.index}>{m[4]}</code>);
    last = re.lastIndex;
  }
  if (last < md.length) parts.push(md.slice(last));
  return <>{parts}</>;
}

export default function Glossary() {
  return (
    <div className={styles.page}>
      <header className={styles.intro}>
        <p className="eyebrow">Tour</p>
        <h1>Glossary</h1>
        <p className="lede" data-opener="">
          These are the words the Agentic Management System, or <a href="#ams">AMS</a>, gives a fixed meaning, so
          that Kayden and every <dfn id="agent">agent</dfn>, an AI assistant doing the work, read them the same way.
          Each definition below is copied word for word from the project&apos;s{" "}
          <a href={`${REPO_BLOB}GLOSSARY.md`}>glossary file</a>, and the site&apos;s
          tests fail if this page and that file ever disagree.
        </p>
        <p>
          <Inline md={glossary.intro} />
          <Source path="GLOSSARY.md">GLOSSARY.md</Source>
        </p>
        <nav aria-label="Glossary groups">
          <ul className={styles.list}>
            {glossary.sections.flatMap((s) =>
              s.groups.map((g) => (
                <li key={g.id}>
                  <a href={`#${g.id}`}>{g.heading}</a>
                </li>
              )),
            )}
          </ul>
        </nav>
      </header>

      {glossary.sections.map((section) => (
        <Fragment key={section.heading}>
          {section.groups.map((group) => (
            <section key={group.id} className={styles.section} aria-labelledby={group.id}>
              <h2 id={group.id}>
                {section.heading}: {group.heading}
              </h2>
              {group.note ? (
                <p>
                  <Inline md={group.note} />
                </p>
              ) : null}
              <dl className={styles.terms}>
                {group.terms.map((t) => (
                  <Fragment key={t.id}>
                    <dt id={t.id}>{t.term}</dt>
                    <dd>
                      <Inline md={t.definition} />
                    </dd>
                  </Fragment>
                ))}
              </dl>
            </section>
          ))}
        </Fragment>
      ))}
    </div>
  );
}
