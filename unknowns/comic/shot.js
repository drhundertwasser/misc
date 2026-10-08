// Screenshot helper: node shot.js <file.html> <out.png> [t]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, out, t] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  p.on('pageerror', e => console.log('PAGEERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('file://' + path.resolve(file) + (t !== undefined ? `?capture=1&t=${t}` : ''));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  if (t !== undefined) await p.evaluate(tt => window.__seek && window.__seek(tt), Number(t));
  await p.screenshot({ path: out }); await b.close();
})();
