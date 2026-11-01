// Generates app/glossary/glossary.json from ../GLOSSARY.md, the one home of
// the project's terms, so the Glossary page cannot diverge from it.
//   node scripts/gen-glossary.mjs          print the JSON
//   node scripts/gen-glossary.mjs --write  write app/glossary/glossary.json
// tests/glossary.test.mjs fails `npm test` unless the committed JSON equals
// this output byte for byte. Text stays Markdown inline (links, **bold**,
// `code`); the page renders it.
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const siteDir = fileURLToPath(new URL('..', import.meta.url));
export const OUT = join(siteDir, 'app', 'glossary', 'glossary.json');

export const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const join1 = (lines) => lines.map((l) => l.trim()).join(' ').trim();

// GLOSSARY.md -> { intro, sections: [{ heading, groups: [{ heading, id, note, terms: [{ term, id, definition }] }] }] }.
// "##" opens a section, "###" a group; a paragraph "**Term**:" plus its lines
// is a term; any other paragraph in a group is its note. The title, the
// generated-from blockquote and blank groups are left out.
export function parseGlossary(md) {
  const out = { intro: '', sections: [] };
  const ids = new Set();
  const uniqueId = (base) => {
    let id = base;
    for (let n = 2; ids.has(id); n++) id = `${base}-${n}`;
    ids.add(id);
    return id;
  };
  let section = null;
  let group = null;
  for (const block of md.split(/\n\s*\n/)) {
    const text = block.trim();
    if (!text || text.startsWith('# ') || text.startsWith('>')) continue;
    const h2 = text.match(/^## (.+)$/);
    const h3 = text.match(/^### (.+)$/);
    if (h2) { section = { heading: h2[1].trim(), groups: [] }; out.sections.push(section); group = null; continue; }
    if (h3) {
      if (!section) throw new Error(`group ${h3[1]} is outside a section`);
      group = { heading: h3[1].trim(), id: uniqueId(`group-${slug(h3[1])}`), note: '', terms: [] };
      section.groups.push(group);
      continue;
    }
    const term = text.match(/^\*\*(.+?)\*\*:\s*([\s\S]+)$/);
    if (term) {
      if (!group) throw new Error(`term ${term[1]} is outside a group`);
      group.terms.push({ term: term[1].trim(), id: uniqueId(slug(term[1])), definition: join1(term[2].split('\n')) });
      continue;
    }
    if (group) group.note = join1([group.note, ...text.split('\n')]);
    else if (!section) out.intro = join1([out.intro, ...text.split('\n')]);
    else throw new Error(`paragraph outside a group: ${text.slice(0, 40)}`);
  }
  return out;
}

export const glossaryJson = (md) => `${JSON.stringify(parseGlossary(md), null, 2)}\n`;

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const json = glossaryJson(readFileSync(join(siteDir, '..', 'GLOSSARY.md'), 'utf8'));
  if (process.argv.includes('--write')) writeFileSync(OUT, json);
  else process.stdout.write(json);
}
