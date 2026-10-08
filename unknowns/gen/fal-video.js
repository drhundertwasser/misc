// Minimal fal.ai image-to-video client (queue API). Needs FAL_KEY in the environment.
// Usage:
//   node fal-video.js --image out/01-hazen-t2i.png --prompt prompts/01-hazen-motion.txt --out out/01-hazen-seedance.mp4
// Options: --model <fal model id>  (default: Seedance 1.0 Pro image-to-video; also try kling)
//          --duration <seconds>    (default 5)   --seed <int>   --fixed  (keep camera still, Seedance only)
const fs = require('fs'), path = require('path');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]); return a; }, []));
const KEY = process.env.FAL_KEY;
if (!KEY) { console.error('FAL_KEY is not set.'); process.exit(2); }
if (!args.prompt || !args.image) { console.error('--prompt <file or text> and --image <png/jpg> are required'); process.exit(2); }
const MODELS = { seedance: 'fal-ai/bytedance/seedance/v1/pro/image-to-video', kling: 'fal-ai/kling-video/v2.5-turbo/pro/image-to-video' };
const model = MODELS[args.model] || args.model || MODELS.seedance;
const prompt = fs.existsSync(args.prompt) ? fs.readFileSync(args.prompt, 'utf8').trim() : String(args.prompt);
const img = fs.readFileSync(args.image);
const mime = /\.jpe?g$/i.test(args.image) ? 'image/jpeg' : 'image/png';
const body = { prompt, image_url: `data:${mime};base64,${img.toString('base64')}`, duration: String(args.duration || 5) };
if (model.includes('seedance')) { body.resolution = args.resolution || '1080p'; body.aspect_ratio = '16:9'; if (args.fixed) body.camera_fixed = true; if (args.seed) body.seed = Number(args.seed); }
if (model.includes('kling')) { body.negative_prompt = 'blur, distort, low quality, extra text, changed text, photorealistic'; body.cfg_scale = 0.5; }
const H = { Authorization: `Key ${KEY}`, 'Content-Type': 'application/json' };
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  console.log('model:', model); console.log('prompt:', prompt.slice(0, 160) + (prompt.length > 160 ? '…' : ''));
  const t0 = Date.now();
  let r = await fetch(`https://queue.fal.run/${model}`, { method: 'POST', headers: H, body: JSON.stringify(body) });
  if (!r.ok) { console.error('submit failed', r.status, await r.text()); process.exit(1); }
  const q = await r.json();
  for (let i = 0; i < 600; i++) {
    await sleep(3000);
    const s = await (await fetch(q.status_url + '?logs=1', { headers: H })).json();
    if (s.status === 'COMPLETED') break;
    if (s.status === 'FAILED') { console.error('generation failed', JSON.stringify(s)); process.exit(1); }
    if (i % 10 === 0) console.log('status:', s.status, s.queue_position !== undefined ? `(queue ${s.queue_position})` : '', `${Math.round((Date.now() - t0) / 1000)}s`);
  }
  const res = await (await fetch(q.response_url, { headers: H })).json();
  if (!res.video || !res.video.url) { console.error('no video in response', JSON.stringify(res).slice(0, 500)); process.exit(1); }
  const out = args.out || path.join('out', 'fal-video-' + Date.now() + '.mp4');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const buf = Buffer.from(await (await fetch(res.video.url)).arrayBuffer());
  fs.writeFileSync(out, buf);
  console.log('wrote', out, `${(buf.length / 1024).toFixed(0)} KB`, `in ${Math.round((Date.now() - t0) / 1000)}s`);
  if (res.seed !== undefined) console.log('seed:', res.seed);
})().catch(e => { console.error(e); process.exit(1); });
