// npm run page-hashes: print each built page's route, current content hash and
// status (draft or approved), so an owner approval can be recorded against the
// exact content. Reads the last `npm run build`; --json prints JSON.
import { contentHash, hasDraftMark, readBuiltPages } from './draft-marks.mjs';

const rows = readBuiltPages().map((p) => ({ route: p.route, hash: contentHash(p.html), status: hasDraftMark(p.html) ? 'draft' : 'approved' }));

if (process.argv.includes('--json')) console.log(JSON.stringify(rows, null, 2));
else {
  const width = Math.max(...rows.map((r) => r.route.length));
  for (const r of rows) console.log(`${r.route.padEnd(width)}  ${r.hash}  ${r.status}`);
}
