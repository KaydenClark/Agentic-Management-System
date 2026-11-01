// S-008 source check, not part of `npm test`: the skills repository is
// private and absent in CI. Given a checkout of it, checks that (a) every
// article in content/skills/ names a skill folder there and the checkout's
// HEAD is the pin (when the folder is a git checkout), and (b) no article
// shares a run of 10 or more consecutive normalized words with any file in
// its skill's folder. Findings print article, section, word offset and skill
// file, never the matched words. A flagged run may still be an allowed short
// quoted term or the skill's description phrase; a reviewer decides.
// Runs its planted-fault self-test (tests/fixtures/skills-source) first.
// Usage: npm run check:skills-source -- --skills DIR [--content DIR]
// Exit: 0 clean, 1 findings or a failed self-test, 2 usage.
import { existsSync } from 'node:fs';
import { SKILLS_PIN, contentDir } from '../app/skills/content.mjs';
import { siteDir } from './helpers.mjs';
import { selfTestProblems, sourceFindings } from './skills-source.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const skills = opt('--skills');
const content = opt('--content') ?? contentDir(siteDir);
if (!skills || !existsSync(skills)) {
  console.error('usage: npm run check:skills-source -- --skills DIR [--content DIR]   (DIR: a checkout of the skills repository at the pin)');
  process.exit(2);
}

const self = selfTestProblems();
if (self.length) {
  for (const p of self) console.log(`FAIL self-test: ${p}`);
  process.exit(1);
}
console.log('PASS self-test: planted copy, missing folder and wrong pin are each reported; clean fixtures pass');

const { names, findings } = sourceFindings(content, skills, SKILLS_PIN);
for (const f of findings) console.log(`${f.kind === 'note' ? 'NOTE' : 'FAIL'} ${f.message}`);
const failures = findings.filter((f) => f.kind !== 'note');
console.log(`${names.length} articles checked against the skills checkout (pin ${SKILLS_PIN.slice(0, 7)}): ${failures.length} finding(s)`);
process.exit(failures.length ? 1 : 0);
