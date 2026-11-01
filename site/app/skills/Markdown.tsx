// Renders the skills wiki's restricted Markdown (markdown.mjs) as React
// elements: no raw HTML ever reaches the page. Site links go through
// next/link; public links are plain anchors.
import Link from "next/link";
import type { ReactNode } from "react";
import type { Block, Inline } from "./markdown.mjs";
import styles from "./skills.module.css";

export function InlineNodes({ nodes }: { nodes: readonly Inline[] }): ReactNode {
  return nodes.map((n, k) => {
    switch (n.type) {
      case "text":
        return n.value;
      case "code":
        return (
          <code key={k} className={styles.code}>
            {n.value}
          </code>
        );
      case "strong":
        return (
          <strong key={k}>
            <InlineNodes nodes={n.children} />
          </strong>
        );
      case "em":
        return (
          <em key={k}>
            <InlineNodes nodes={n.children} />
          </em>
        );
      case "link":
        return n.href.startsWith("/") ? (
          <Link key={k} href={n.href}>
            <InlineNodes nodes={n.children} />
          </Link>
        ) : (
          <a key={k} href={n.href}>
            <InlineNodes nodes={n.children} />
          </a>
        );
    }
  });
}

export function Blocks({ blocks }: { blocks: readonly (Block & { id?: string })[] }) {
  return blocks.map((b, k) => {
    switch (b.type) {
      case "heading":
        return b.level === 2 ? (
          <h2 key={k} id={b.id}>
            <InlineNodes nodes={b.inline} />
          </h2>
        ) : (
          <h3 key={k} id={b.id} className={styles.h3}>
            <InlineNodes nodes={b.inline} />
          </h3>
        );
      case "paragraph":
        return (
          <p key={k}>
            <InlineNodes nodes={b.inline} />
          </p>
        );
      case "list": {
        const items = b.items.map((item, j) => (
          <li key={j}>
            <InlineNodes nodes={item} />
          </li>
        ));
        return b.ordered ? (
          <ol key={k} className={styles.list}>
            {items}
          </ol>
        ) : (
          <ul key={k} className={styles.list}>
            {items}
          </ul>
        );
      }
      case "table":
        // Fixed layout at the column's width with wrapping cells: a table
        // reflows at 375 px instead of scrolling the page.
        return (
          <table key={k} className={styles.table}>
            <thead>
              <tr>
                {b.header.map((cell, j) => (
                  <th key={j} scope="col">
                    <InlineNodes nodes={cell} />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {b.rows.map((row, r) => (
                <tr key={r}>
                  {row.map((cell, j) => (
                    <td key={j}>
                      <InlineNodes nodes={cell} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        );
      case "blockquote":
        return (
          <blockquote key={k} className={styles.quote}>
            {b.paragraphs.map((p, j) => (
              <p key={j}>
                <InlineNodes nodes={p} />
              </p>
            ))}
          </blockquote>
        );
      case "code":
        // Wrapped, never scrolled, so it needs no tab stop of its own.
        return (
          <pre key={k} className={styles.pre}>
            <code>{b.text}</code>
          </pre>
        );
    }
  });
}
