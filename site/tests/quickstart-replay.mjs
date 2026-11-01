// Replays the Quickstart (app/quickstart/quickstart.mjs) on a fresh clone and
// returns what each step printed. Used by tests/quickstart-replay.test.mjs;
// `node tests/quickstart-replay.mjs` prints the replayed output of each step.
//
// Clone source: the page tells the reader to clone from GitHub. The replay
// clones this repository's committed HEAD instead (the commit under test, not
// the working tree, and no network), into a new temporary directory under the
// system temp dir, which is removed afterwards. So that the clone is in the
// state a reader's GitHub clone is in (the default branch `main` checked out
// and tracking `origin/main`), the replay checks the commit out as `main` and
// points `origin/main` and `origin` at it and at the GitHub URL. CI checkouts
// are shallow and detached, so without this the clone would differ from a
// reader's in ways the page does not cover.
//
// Output normalisation: line endings become \n and trailing whitespace at the
// end of the whole output is dropped. Nothing else: the commands shown print
// no SHA, date, path or timing. A step the page shows no output for (the
// clone, whose progress lines vary with the network, and `cd`) must succeed
// but its output is not compared.
import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { siteDir } from './helpers.mjs';

export const quickstart = await import(pathToFileURL(join(siteDir, 'app', 'quickstart', 'quickstart.mjs')).href);
const repoRoot = join(siteDir, '..');

export const normalise = (s) => s.replace(/\r\n?/g, '\n').replace(/\s+$/, '');

const git = (cwd, ...args) => execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();

// Shell metacharacters would mean the page's command is not the plain argv
// the replay runs.
const PLAIN = /^[\w./:@=+-]+(?: [\w./:@=+-]+)*$/;

export function replay({ steps, CLONE_URL, REPO_DIR } = quickstart) {
  const home = mkdtempSync(join(tmpdir(), 'ams-quickstart-'));
  const head = git(repoRoot, 'rev-parse', 'HEAD');
  let cwd = home;
  const results = [];
  try {
    for (const step of steps) {
      if (!PLAIN.test(step.command)) throw new Error(`step ${step.id}: "${step.command}" is not a plain command`);
      const [cmd, ...args] = step.command.split(' ');
      let out;
      if (cmd === 'cd') {
        if (args.length !== 1) throw new Error(`step ${step.id}: cd takes one directory`);
        cwd = join(cwd, args[0]);
        out = '';
      } else if (cmd === 'git' && args[0] === 'clone') {
        if (args.length !== 2 || args[1] !== CLONE_URL) throw new Error(`step ${step.id}: expected git clone ${CLONE_URL}`);
        git(cwd, 'clone', '--quiet', repoRoot, REPO_DIR);
        const dir = join(cwd, REPO_DIR);
        git(dir, 'fetch', '--quiet', repoRoot, 'HEAD');
        git(dir, 'checkout', '--quiet', '-B', 'main', 'FETCH_HEAD');
        git(dir, 'update-ref', 'refs/remotes/origin/main', 'FETCH_HEAD');
        git(dir, 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/main');
        git(dir, 'branch', '--quiet', '--set-upstream-to=origin/main', 'main');
        git(dir, 'remote', 'set-url', 'origin', CLONE_URL);
        const cloned = git(dir, 'rev-parse', 'HEAD');
        if (cloned !== head) throw new Error(`clone is at ${cloned}, expected ${head}`);
        out = '';
      } else {
        const file = cmd === 'node' ? process.execPath : cmd;
        out = execFileSync(file, args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
      }
      results.push({ id: step.id, command: step.command, output: normalise(out) });
    }
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
  return { head, results };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { head, results } = replay();
  console.log(`# replayed at ${head}`);
  for (const r of results) console.log(`$ ${r.command}\n${r.output}`);
}
