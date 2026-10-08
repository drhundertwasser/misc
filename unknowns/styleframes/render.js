// Renders every frame in ./frames to a PNG in ./out, then builds a contact sheet.
// Usage: node render.js [frame-name-filter]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const filter = process.argv[2] || '';
  const framesDir = path.join(__dirname, 'frames'); const outDir = path.join(__dirname, 'out');
  fs.mkdirSync(outDir, { recursive: true });
  const files = fs.readdirSync(framesDir).filter(f => f.endsWith('.html') && f.includes(filter)).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  for (const f of files) {
    await page.goto('file://' + path.join(framesDir, f));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const out = path.join(outDir, f.replace('.html', '.png'));
    await page.screenshot({ path: out });
    console.log('rendered', out);
  }
  if (!filter) {
    const pngs = fs.readdirSync(outDir).filter(f => /^\d\d-.*\.png$/.test(f)).sort();
    const cells = pngs.map(p => `<figure><img src="${p}"><figcaption>${p.replace('.png','').replace(/-/g,' ')}</figcaption></figure>`).join('');
    const html = `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#111;color:#eee;font:16px Inter,sans-serif}
      .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:14px}figure{margin:0}img{width:100%;display:block;border-radius:4px}
      figcaption{padding:6px 2px 0;text-transform:capitalize}</style><div class="grid">${cells}</div>`;
    fs.writeFileSync(path.join(outDir, 'contact-sheet.html'), html);
    const rows = Math.ceil(pngs.length / 4);
    await page.setViewportSize({ width: 1600, height: 14 + rows * (14 + 213 + 30) });
    await page.goto('file://' + path.join(outDir, 'contact-sheet.html'));
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(outDir, 'contact-sheet.png'), fullPage: true });
    console.log('contact sheet written');
  }
  await browser.close();
})();
