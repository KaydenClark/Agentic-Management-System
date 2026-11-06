import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseGlossary } from '../scripts/gen-glossary.mjs';

test('canonical glossary terms can precede the first explicit group', () => {
  const source = '# Glossary\n\nIntro.\n\n## Language\n\n**AMS**:\nShared system.\n\n**Workbench**:\nPeople and tools.\n\n### Governance core\n\n**Projection**:\n6: A dated snapshot.\n';
  const glossary = parseGlossary(source);
  assert.equal(glossary.intro, 'Intro.');
  assert.deepEqual(glossary.sections[0].groups, [
    { heading: 'AMS', id: 'group-ams', note: '', terms: [
      { term: 'AMS', id: 'ams', definition: 'Shared system.' },
      { term: 'Workbench', id: 'workbench', definition: 'People and tools.' },
    ] },
    { heading: 'Governance core', id: 'group-governance-core', note: '', terms: [
      { term: 'Projection', id: 'projection', definition: '6: A dated snapshot.' },
    ] },
  ]);
  assert.throws(() => parseGlossary('**Loose**:\nNo section.\n'), /outside a section/);
});
