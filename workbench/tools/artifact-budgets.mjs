import fs from 'node:fs';
import path from 'node:path';

export function loadBudgets(root) {
  const policy = JSON.parse(fs.readFileSync(path.join(root, 'workbench/artifact-budgets.json'), 'utf8'));
  const validMax = n => Number.isSafeInteger(n) && n > 0 && policy.tiers.includes(n);
  if (policy.schemaVersion !== 1 || policy.unit !== 'unicode-code-points' ||
      !Array.isArray(policy.tiers) || !policy.tiers.length ||
      !policy.tiers.every(n => Number.isSafeInteger(n) && n > 0) ||
      !validMax(policy.defaultMaxCharacters) || policy.defaultMaxCharacters !== Math.max(...policy.tiers) || !policy.artifacts || typeof policy.artifacts !== 'object') {
    throw new Error('Invalid artifact budget policy');
  }
  for (const [name, rule] of Object.entries(policy.artifacts)) {
    const target = rule.targetCharacters;
    if (path.basename(name) !== name || !validMax(rule.maxCharacters) ||
        (target !== undefined && (!Array.isArray(target) || target.length !== 2 ||
          !target.every(validMax) || target[0] > target[1] || target[1] > rule.maxCharacters))) {
      throw new Error(`Invalid artifact budget: ${name}`);
    }
  }
  return policy;
}

export function budgetFor(policy, file) {
  return policy.artifacts[path.basename(file)] ?? { maxCharacters: policy.defaultMaxCharacters };
}

// Count the complete source, including markup, spaces, frontmatter and code.
// Normalize line endings so the same document has one count on every platform.
export function characterCount(source) {
  return [...source.replace(/\r\n?/g, '\n')].length;
}

export function budgetFailure(policy, file, source) {
  const count = characterCount(source);
  const max = budgetFor(policy, file).maxCharacters;
  return count > max ? `${file}: ${count} characters; maximum ${max}. Split or condense this artifact without losing required meaning.` : null;
}
