// Renders the comic to an MP4 by seeking frame-by-frame and piping PNGs into ffmpeg.
// Usage: node export.js [out.mp4] [fps]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const out = process.argv[2] || path.join(__dirname, 'out', 'unknowns-sample.mp4'), fps = Number(process.argv[3] || 30);
  require('fs').mkdirSync(path.dirname(out), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  p.on('pageerror', e => console.log('PAGEERROR', e.message));
  await p.goto('file://' + path.join(__dirname, 'index.html') + '?capture=1');
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const dur = await p.evaluate(() => window.__duration); const n = Math.ceil(dur * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.__seek(t), i / fps);
    const buf = await p.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('wrote', out, `(${dur.toFixed(1)}s @ ${fps}fps)`);
})();
