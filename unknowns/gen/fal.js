// Minimal fal.ai client (queue API) for image generation. Needs FAL_KEY in the environment.
// Usage:
//   node fal.js --prompt prompts/01-hazen.txt --out out/01-hazen-seedream.png
//   node fal.js --prompt prompts/01-hazen.txt --image ../comic/out/frame-01.png --out out/01-hazen-edit.png
// Options: --model <fal model id> (default: Seedream 4 text-to-image, or the edit model when --image is given)
//          --size 16:9 | 1:1 | 4:3 ... (default 16:9)   --n <count> (default 1)   --seed <int>
const fs = require('fs'), path = require('path');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]); return a; }, []));
const KEY = process.env.FAL_KEY;
if (!KEY) { console.error('FAL_KEY is not set. Add it as an environment secret and start a new session.'); process.exit(2); }
if (!args.prompt) { console.error('--prompt <file or text> is required'); process.exit(2); }
const prompt = fs.existsSync(args.prompt) ? fs.readFileSync(args.prompt, 'utf8').trim() : String(args.prompt);
const images = args.image ? String(args.image).split(',') : [];
const model = args.model || (images.length ? 'fal-ai/bytedance/seedream/v4/edit' : 'fal-ai/bytedance/seedream/v4/text-to-image');
const sizes = { '16:9': { width: 2048, height: 1152 }, '1:1': { width: 2048, height: 2048 }, '4:3': { width: 2048, height: 1536 }, '9:16': { width: 1152, height: 2048 } };
const body = { prompt, image_size: sizes[args.size || '16:9'] || sizes['16:9'], num_images: Number(args.n || 1), enable_safety_checker: true };
if (args.seed) body.seed = Number(args.seed);
if (images.length) body.image_urls = images.map(p => { const b = fs.readFileSync(p); const mime = p.endsWith('.jpg') || p.endsWith('.jpeg') ? 'image/jpeg' : 'image/png'; return `data:${mime};base64,${b.toString('base64')}`; });
const H = { Authorization: `Key ${KEY}`, 'Content-Type': 'application/json' };
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  console.log('model:', model); console.log('prompt:', prompt.slice(0, 160) + (prompt.length > 160 ? '…' : ''));
  let r = await fetch(`https://queue.fal.run/${model}`, { method: 'POST', headers: H, body: JSON.stringify(body) });
  if (!r.ok) { console.error('submit failed', r.status, await r.text()); process.exit(1); }
  const q = await r.json();
  const statusUrl = q.status_url, responseUrl = q.response_url;
  for (let i = 0; i < 300; i++) {
    await sleep(2000);
    const s = await (await fetch(statusUrl + '?logs=1', { headers: H })).json();
    if (s.status === 'COMPLETED') break;
    if (s.status === 'FAILED') { console.error('generation failed', JSON.stringify(s)); process.exit(1); }
    if (i % 5 === 0) console.log('status:', s.status, s.queue_position !== undefined ? `(queue ${s.queue_position})` : '');
  }
  const res = await (await fetch(responseUrl, { headers: H })).json();
  const imgs = res.images || (res.image ? [res.image] : []);
  if (!imgs.length) { console.error('no images in response', JSON.stringify(res).slice(0, 500)); process.exit(1); }
  const out = args.out || path.join('out', 'fal-' + Date.now() + '.png');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  for (let i = 0; i < imgs.length; i++) {
    const file = imgs.length === 1 ? out : out.replace(/(\.\w+)$/, `-${i + 1}$1`);
    const buf = Buffer.from(await (await fetch(imgs[i].url)).arrayBuffer());
    fs.writeFileSync(file, buf); console.log('wrote', file, `${(buf.length / 1024).toFixed(0)} KB`, imgs[i].width ? `${imgs[i].width}x${imgs[i].height}` : '');
  }
  if (res.seed !== undefined) console.log('seed:', res.seed);
})().catch(e => { console.error(e); process.exit(1); });
