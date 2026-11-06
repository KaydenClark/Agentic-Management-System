// Module hooks that let render tests import the site's own .ts/.tsx modules
// with no new dependency: TypeScript (already a devDependency) strips types
// and compiles JSX for React's automatic runtime, and a CSS module import
// yields its class names. Only files under site/app/ are transpiled.
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';

const appDir = new URL('../app/', import.meta.url).href;

export async function resolve(specifier, context, next) {
  const parent = context.parentURL ?? '';
  if (parent.startsWith(appDir) && (specifier.startsWith('./') || specifier.startsWith('../')) && !/\.[cm]?[jt]sx?$|\.css$/.test(specifier)) {
    for (const ext of ['.ts', '.tsx', '/index.ts', '/index.tsx']) {
      const url = new URL(specifier + ext, parent);
      if (existsSync(fileURLToPath(url))) return { url: url.href, shortCircuit: true };
    }
  }
  return next(specifier, context);
}

export async function load(url, context, next) {
  if (url.startsWith(appDir) && url.endsWith('.module.css')) {
    return { format: 'module', shortCircuit: true, source: 'export default new Proxy({}, { get: (_, key) => String(key) });' };
  }
  if (url.startsWith(appDir) && /\.tsx?$/.test(url)) {
    const source = await readFile(fileURLToPath(url), 'utf8');
    const out = ts.transpileModule(source, {
      fileName: fileURLToPath(url),
      compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022, jsx: ts.JsxEmit.ReactJSX },
    });
    return { format: 'module', shortCircuit: true, source: out.outputText };
  }
  return next(url, context);
}
