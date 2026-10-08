// Preview a lettering layout on a plate: NODE_PATH=/opt/node-tools/node_modules node still.js <scene> <plate.png> <out.png> [t]
const { chromium } = require('playwright'); const path = require('path'); const { execSync } = require('child_process');
(async () => {
  const [scene, plate, out, t = '3'] = process.argv.slice(2);
  const tmp = out.replace(/\.png$/, '-overlay.png');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGEERROR', e.message));
  await p.goto('file://' + path.join(__dirname, 'overlay.html') + `?scene=${scene}&t=${t}`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: tmp, omitBackground: true }); await b.close();
  execSync(`ffmpeg -v error -y -i "${plate}" -i "${tmp}" -filter_complex "[0:v]scale=1920:1080[v];[v][1:v]overlay" -frames:v 1 "${out}"`);
  require('fs').unlinkSync(tmp); console.log('wrote', out);
})();
