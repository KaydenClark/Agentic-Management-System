import {isReaderHref} from '../app/reader-links.mjs';
import {decode, parseAttrs} from './rsi-html.mjs';
import {routeOf} from '../scripts/page-hash.mjs';

export function readerLinkProblems(pages) {
  const byRoute = new Map(pages.map(page => [routeOf(page.name), page.html]));
  const problems = [];
  for (const {name, html} of pages) {
    const source = routeOf(name);
    const body = html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
    for (const match of body.matchAll(/<a\b([^>]*)>/gi)) {
      const raw = parseAttrs(match[1]).href;
      if (raw === undefined) continue;
      const href = decode(raw);
      if (!isReaderHref(href)) { problems.push(`${source}: reader exit ${href}`); continue; }
      const target = new URL(href, `https://site.invalid${source}`);
      const targetHtml = byRoute.get(target.pathname);
      if (!targetHtml) { problems.push(`${source}: missing page ${href}`); continue; }
      if (target.hash) {
        let id;
        try { id = decodeURIComponent(target.hash.slice(1)); } catch { problems.push(`${source}: invalid fragment ${href}`); continue; }
        const ids = [...targetHtml.matchAll(/\sid="([^"]+)"/g)].map(m => decode(m[1]));
        if (ids.filter(value => value === id).length !== 1) problems.push(`${source}: missing or duplicate fragment ${href}`);
      }
    }
  }
  return problems;
}
