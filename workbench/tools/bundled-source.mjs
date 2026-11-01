import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// Package identity is content-addressed. A skill installed without Git must
// never fabricate a commit or depend on a producer checkout for provenance.
export function bundledSource(root) {
  const marker = path.join(root, 'bundle.json');
  if (!fs.existsSync(marker)) return null;
  const bundle = JSON.parse(fs.readFileSync(marker, 'utf8'));
  if (bundle.schemaVersion !== 1 || !bundle.files || !bundle.source?.repository
      || !/^v\d+\.\d+\.\d+$/.test(bundle.source.release ?? '')) throw new Error('Invalid bundled Workbench identity.');
  const inventory = Object.entries(bundle.files).sort(([a], [b]) => a.localeCompare(b, 'en'));
  if (!inventory.length) throw new Error('Empty bundled Workbench inventory.');
  for (const [relative, expected] of inventory) {
    if (path.isAbsolute(relative) || relative.split('/').some(p => !p || p === '..' || p === '.')
        || !/^[0-9a-f]{64}$/.test(expected)) throw new Error('Unsafe bundled Workbench inventory.');
    let file = root;
    for (const part of relative.split('/')) {
      file = path.join(file, part);
      if (fs.lstatSync(file).isSymbolicLink()) throw new Error(`Linked package asset: ${relative}`);
    }
    if (!fs.statSync(file).isFile()) throw new Error(`Missing package asset: ${relative}`);
    if (crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex') !== expected) throw new Error(`Changed package asset: ${relative}`);
  }
  const digest = crypto.createHash('sha256').update(JSON.stringify(inventory)).digest('hex');
  if (digest !== bundle.source.sha256) throw new Error('Bundled Workbench inventory digest mismatch.');
  return { ...bundle.source, upstream: bundle.upstream };
}
