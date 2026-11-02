// npm run page-hashes: print each built page's route and current content
// hash, the value the S-005 Grill Board binds an owner review to. Reads the
// last `npm run build`; --json prints JSON. The public site shows no review
// state.
import { contentHash, readBuiltPages } from './page-hash.mjs';

const rows = readBuiltPages().map((p) => ({ route: p.route, hash: contentHash(p.html) }));

if (process.argv.includes('--json')) console.log(JSON.stringify(rows, null, 2));
else {
  const width = Math.max(...rows.map((r) => r.route.length));
  for (const r of rows) console.log(`${r.route.padEnd(width)}  ${r.hash}`);
}
