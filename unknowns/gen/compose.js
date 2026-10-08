// Lays the code-drawn lettering (overlay.html) over a generated video clip, frame by frame.
// Usage: NODE_PATH=/opt/node-tools/node_modules node compose.js --video out/clip.mp4 --scene hazen --out out/final.mp4 [--fps 24]
const { chromium } = require('playwright'); const { spawn, execSync } = require('child_process'); const path = require('path'); const fs = require('fs');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]); return a; }, []));
if (!args.video) { console.error('--video <clip.mp4> is required'); process.exit(2); }
(async () => {
  const fps = Number(args.fps || 24), scene = args.scene || 'hazen';
  const out = args.out || args.video.replace(/\.mp4$/, '-lettered.mp4');
  const dur = Number(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${args.video}"`).toString().trim());
  const n = Math.ceil(dur * fps);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGEERROR', e.message));
  await p.goto('file://' + path.join(__dirname, 'overlay.html') + `?scene=${scene}`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  // Input 0: the generated clip, scaled to exactly 1920x1080 (some models return 1088 rows). Input 1: overlay PNGs with alpha.
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', args.video, '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-filter_complex', '[0:v]scale=1920:1080,fps=' + fps + '[v];[v][1:v]overlay=shortest=1[o]', '-map', '[o]',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.__seek(t), i / fps);
    const buf = await p.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 48 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('wrote', out, `(${dur.toFixed(1)}s @ ${fps}fps)`);
})().catch(e => { console.error(e); process.exit(1); });
