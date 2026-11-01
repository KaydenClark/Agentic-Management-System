// Public-hygiene and third-party patterns for the built site (TK-005).
// Shapes follow workbench/tools/privacy.mjs, narrowed where minified framework
// code would trip them: its generic "password=" rule matches Next's own URL
// parser. A finding names its class and file offset, never the matched value,
// so a report cannot leak what it found.
export const HYGIENE_PATTERNS = Object.freeze([
  // A path on a developer's machine: home directories on Linux, macOS and
  // Windows, the root home, and file:// URLs naming a drive or a host
  // directory (Turbopack's runtime builds a bare `file:///${...}` template,
  // which names no machine).
  { label: 'host path', pattern: /(?:\/home\/|\/Users\/|\/root\/)[A-Za-z0-9._-]+|[A-Za-z]:\\{1,2}Users\\{1,2}[A-Za-z0-9._-]+|file:\/\/\/(?:[A-Za-z]:|tmp\/|var\/|private\/|opt\/)/g },
  // Supabase: the secret key and the legacy service-role key. The publishable
  // key (sb_publishable_) is meant to ship and is not matched.
  { label: 'Supabase secret key', pattern: /sb_secret_[A-Za-z0-9_-]+/g },
  { label: 'Supabase service role', pattern: /service_role/g },
  // Any JWT (header.payload); the site ships none, and Supabase's legacy
  // anon and service keys are JWTs.
  { label: 'JWT-shaped token', pattern: /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g },
  { label: 'private key block', pattern: /-----BEGIN [A-Z ]*PRIVATE KEY-----/g },
  { label: 'API token', pattern: /\b(?:sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_]{20,}|gh[oprsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[abpr]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b/g },
  { label: 'bearer token', pattern: /\bBearer\s+[A-Za-z0-9._~+/=-]{16,}/g },
  { label: 'email address', pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b/g },
  // Private records. AGENTS.md: the pre-repository Specs, owner decisions and
  // evidence live in the private GPT_OS repository and are not published
  // without the owner's go-ahead; agent session links (the Claude-Session
  // commit trailer) are private traces.
  { label: 'private repository reference', pattern: /GPT_OS/g },
  { label: 'agent session trace', pattern: /claude\.ai\/code\/session_[A-Za-z0-9]+|\bsession_0[A-Za-z0-9]{20,}/g },
]);

export function hygieneFindings(text) {
  const found = [];
  for (const { label, pattern } of HYGIENE_PATTERNS) {
    for (const m of text.matchAll(pattern)) found.push({ label, offset: m.index });
  }
  return found;
}

// Hosts other than the site that a page may load from (S-003: requests go
// only to the site, Supabase and GitHub links).
export function allowedHost(host) {
  return /(?:^|\.)supabase\.co$/.test(host) || host === 'github.com' || host.endsWith('.github.com') || host.endsWith('.githubusercontent.com');
}

// Resource references in served HTML and CSS that make a browser load from
// another host: script/img/iframe/media sources, every <link> (stylesheets,
// fonts, preconnects) and CSS url()/@import. <a href> is a link, not a load.
// Requests started by JS are caught by check:browser.
export function externalResources(text, kind) {
  const urls = [];
  if (kind === 'html') {
    for (const m of text.matchAll(/<(?:script|img|iframe|source|video|audio|embed|track|input)\b[^>]*?\s(?:src|srcset|poster)="([^"]*)"/gi)) urls.push(m[1]);
    for (const m of text.matchAll(/<link\b[^>]*?\shref="([^"]*)"/gi)) urls.push(m[1]);
    for (const m of text.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)) urls.push(...cssUrls(m[1]));
  } else if (kind === 'css') {
    urls.push(...cssUrls(text));
  }
  return urls
    .flatMap((u) => u.split(/\s*,\s*/).map((s) => s.trim().split(/\s+/)[0]))
    .filter((u) => /^(?:https?:)?\/\//i.test(u))
    .filter((u) => !allowedHost(new URL(u, 'https://site.invalid').hostname));
}

function cssUrls(css) {
  const out = [];
  for (const m of css.matchAll(/url\(\s*(['"]?)([^'")]+)\1\s*\)/gi)) out.push(m[2]);
  for (const m of css.matchAll(/@import\s+(['"])([^'"]+)\1/gi)) out.push(m[2]);
  return out;
}
