/**
 * tag_copyright_MASTER.cjs
 * Embeds copyright notice into every JSON, HTML, and DOCX in the MASTER folder.
 *
 * JSON  → adds "_copyright" as the FIRST key of the root object
 * HTML  → adds <!-- comment --> + <meta name="copyright"> inside <head>
 * DOCX  → adds <dc:rights> + <dc:description> to docProps/core.xml (document properties)
 *
 * Safe to re-run: idempotent — skips files that already carry the tag.
 */

'use strict';

const fs    = require('fs');
const path  = require('path');
const JSZip = require('jszip');

// ── copyright text ─────────────────────────────────────────────────────────
const COPYRIGHT = [
  'COPYRIGHT NOTICE - All original works retain the copyright of their original owners.',
  ' All else, as applicable, are copyright Josef Kulovany and zCHG.org pursuant but not',
  ' limited to https://zchg.org/t/legal-notice-copyright-applicable-ip-and-licensing-read-me/440',
  '\n\nALL APPLICABLE RIGHTS RESERVED.',
  '\n\nhttps://zchg.org/ - https://josefkulovany.com/law',
].join('');

const COPYRIGHT_ONELINE = COPYRIGHT.replace(/\n/g, '  ');

const MASTER = path.resolve(
  __dirname, '..',
  'Carl Miller', 'Corpus_Processed', 'MASTER'
);

// ── JSON handler ───────────────────────────────────────────────────────────
function tagJson(filePath) {
  const raw  = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(raw);

  if (data._copyright) {
    console.log(`  [skip]  ${path.basename(filePath)} — already tagged`);
    return;
  }

  // Rebuild with _copyright as first key
  const tagged = { _copyright: COPYRIGHT_ONELINE, ...data };
  fs.writeFileSync(filePath, JSON.stringify(tagged, null, 2), 'utf8');
  console.log(`  [json]  ${path.basename(filePath)}`);
}

// ── HTML handler ───────────────────────────────────────────────────────────
function tagHtml(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');

  if (html.includes('josefkulovany.com/law')) {
    console.log(`  [skip]  ${path.basename(filePath)} — already tagged`);
    return;
  }

  const htmlComment = `<!--\n  ${COPYRIGHT_ONELINE}\n-->\n`;

  const metaTag = `  <meta name="copyright" content="${COPYRIGHT_ONELINE.replace(/"/g, '&quot;')}">\n` +
                  `  <meta name="author"    content="Josef Kulovany / zCHG.org">\n`;

  // Insert HTML comment before <!DOCTYPE (or at very top)
  html = html.replace(/^(\s*<(!DOCTYPE|html)[^>]*>)/i, `${htmlComment}$1`);

  // Insert meta tags at end of <head> (just before </head>)
  html = html.replace(/<\/head>/i, `${metaTag}</head>`);

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`  [html]  ${path.basename(filePath)}`);
}

// ── DOCX handler ───────────────────────────────────────────────────────────
async function tagDocx(filePath) {
  const buf  = fs.readFileSync(filePath);
  const zip  = await JSZip.loadAsync(buf);

  const coreFile = zip.file('docProps/core.xml');
  if (!coreFile) {
    console.log(`  [warn]  ${path.basename(filePath)} — no docProps/core.xml found`);
    return;
  }

  let coreXml = await coreFile.async('string');

  if (coreXml.includes('josefkulovany.com/law')) {
    console.log(`  [skip]  ${path.basename(filePath)} — already tagged`);
    return;
  }

  // Escape special XML chars
  const esc = s => s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  const escapedCopyright = esc(COPYRIGHT_ONELINE);

  // Insert dc:rights + dc:description before closing </cp:coreProperties>
  const injection =
    `<dc:rights>${escapedCopyright}</dc:rights>` +
    `<dc:description>Josef Kulovany / zCHG.org — https://josefkulovany.com/law</dc:description>`;

  coreXml = coreXml.replace('</cp:coreProperties>', `${injection}</cp:coreProperties>`);

  zip.file('docProps/core.xml', coreXml);

  const outBuf = await zip.generateAsync({
    type: 'nodebuffer',
    compression: 'DEFLATE',
    compressionOptions: { level: 6 },
  });

  fs.writeFileSync(filePath, outBuf);
  console.log(`  [docx]  ${path.basename(filePath)}`);
}

// ── main ───────────────────────────────────────────────────────────────────
(async () => {
  console.log(`Tagging files in: ${MASTER}\n`);
  const entries = fs.readdirSync(MASTER);

  for (const name of entries) {
    const fp  = path.join(MASTER, name);
    const ext = path.extname(name).toLowerCase();
    if (ext === '.json') tagJson(fp);
    else if (ext === '.html') tagHtml(fp);
    else if (ext === '.docx') await tagDocx(fp);
  }

  console.log('\nDone.');
})();
