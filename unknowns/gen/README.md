# gen — upgrading the frames with an image model (fal.ai)

`fal.js` submits a prompt to fal.ai's queue API and saves the result. It needs `FAL_KEY` in the
environment. It is deliberately dependency-free (Node 18+ `fetch`).

Two ways to use a frame:

1. **Text to image** — describe the scene in words. Prompt files live in `prompts/`.
   `node fal.js --prompt prompts/01-hazen.txt --out out/01-hazen-t2i.png`
2. **Image to image (edit)** — hand the model our rendered frame as a reference and ask it to redraw
   it at higher quality while keeping composition and text.
   `node fal.js --prompt prompts/01-hazen-edit.txt --image ../comic/out/frame-01.png --out out/01-hazen-edit.png`

Defaults: Seedream 4 (`fal-ai/bytedance/seedream/v4/text-to-image`, or `.../v4/edit` when `--image`
is given), 2048x1152. Override with `--model`, `--size`, `--seed`, `--n`.

Rendering a reference frame from the comic at a given second:
`cd ../comic && NODE_PATH=/opt/node-tools/node_modules node shot.js index.html out/frame-01.png 8.5`
