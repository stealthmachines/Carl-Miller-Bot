/**
 * tag_copyright_repo.cjs
 * Embeds the copyright notice into every taggable JSON in the full repo.
 *
 * SKIPPED (schema/infra would break):
 *   package.json, package-lock.json  — npm manifests
 *   mcp.json                         — MCP server config (strict schema)
 *   inference1.preset.json           — LM Studio preset
 *   erl-ledger.json                  — ERL infrastructure (keyed schema)
 *   wuwei-routing/state/health.json  — server runtime state
 *   node_modules/**                  — third-party packages
 *
 * ARRAY roots: logged and skipped (no first-key concept).
 * Idempotent — files already carrying the tag are skipped.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── copyright text ──────────────────────────────────────────────────────────
const COPYRIGHT = [
  'COPYRIGHT NOTICE - All original works retain the copyright of their original owners.',
  ' All else, as applicable, are copyright Josef Kulovany and zCHG.org pursuant but not',
  ' limited to https://zchg.org/t/legal-notice-copyright-applicable-ip-and-licensing-read-me/440',
  '\n\nALL APPLICABLE RIGHTS RESERVED.',
  '\n\nhttps://zchg.org/ - https://josefkulovany.com/law',
].join('');

const COPYRIGHT_ONELINE = COPYRIGHT.replace(/\n/g, '  ');

// ── exclusions (basename match) ─────────────────────────────────────────────
const SKIP_NAMES = new Set([
  'package.json',
  'package-lock.json',
  'mcp.json',
  'inference1.preset.json',
  'erl-ledger.json',
  'health.json',
]);

const ROOT = path.resolve(__dirname, '..');

// ── recursive file walker ───────────────────────────────────────────────────
function walk(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules') continue;
      walk(full, results);
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.json')) {
      if (!SKIP_NAMES.has(entry.name)) results.push(full);
    }
  }
  return results;
}

// ── tag a single JSON file ──────────────────────────────────────────────────
function tagJson(filePath) {
  const rel = path.relative(ROOT, filePath);
  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    console.log(`  [error] ${rel} — cannot read: ${e.message}`);
    return;
  }

  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    console.log(`  [error] ${rel} — invalid JSON: ${e.message}`);
    return;
  }

  if (Array.isArray(data)) {
    console.log(`  [skip]  ${rel} — array root (no first-key)`);
    return;
  }

  if (typeof data !== 'object' || data === null) {
    console.log(`  [skip]  ${rel} — non-object root`);
    return;
  }

  if (data._copyright) {
    console.log(`  [skip]  ${rel} — already tagged`);
    return;
  }

  const tagged = { _copyright: COPYRIGHT_ONELINE, ...data };
  try {
    fs.writeFileSync(filePath, JSON.stringify(tagged, null, 2), 'utf8');
    console.log(`  [json]  ${rel}`);
  } catch (e) {
    console.log(`  [error] ${rel} — cannot write: ${e.message}`);
  }
}

// ── main ────────────────────────────────────────────────────────────────────
(function main() {
  console.log(`Scanning: ${ROOT}\n`);
  const files = walk(ROOT);
  console.log(`Found ${files.length} taggable JSON file(s)\n`);
  for (const fp of files) tagJson(fp);
  console.log('\nDone.');
})();
